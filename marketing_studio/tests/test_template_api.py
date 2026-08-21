"""API-level tests for marketing_studio.api.template.

Run with:
    sites$ ../env/bin/python -m frappe.utils.bench_helper frappe \
        --site mc.localhost run-tests --app marketing_studio
"""

import json
from contextlib import contextmanager

import frappe
from frappe.tests import IntegrationTestCase
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from marketing_studio.api.template import (
	create_template,
	create_version,
	get_block_library,
	get_template,
	list_templates,
	list_versions,
	publish_template,
	save_template_layout,
	submit_form,
)

SUBMIT_CMD = "marketing_studio.api.template.submit_form"


def make_user(email, roles):
	if not frappe.db.exists("User", email):
		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": email.split("@")[0],
				"send_welcome_email": 0,
			}
		)
		user.insert(ignore_permissions=True)
		if roles:
			user.add_roles(*roles)
	return email


def make_template(**kwargs):
	values = {
		"doctype": "Marketing Template",
		"title": "Test Template",
		"template_type": "Email",
		"layout": json.dumps({"blocks": []}),
	}
	values.update(kwargs)
	return frappe.get_doc(values).insert(ignore_permissions=True)


TEST_IP = "198.51.100.7"


@contextmanager
def fake_request(cmd, window=60):
	"""The rate limiter no-ops without a request; give it one."""
	request = Request(EnvironBuilder(method="POST", path=f"/api/method/{cmd}").get_environ())
	old_request = getattr(frappe.local, "request", None)
	old_form_dict = frappe.local.form_dict
	# Built exactly as frappe.rate_limiter builds it — a pre-made key, so it has to be
	# deleted with the raw redis call (delete_value would prefix it a second time).
	counter_key = frappe.cache.make_key(f"rl:{cmd}:{TEST_IP}") + f":{window}".encode()
	try:
		frappe.cache.delete(counter_key)
		frappe.local.request = request
		frappe.local.request_ip = TEST_IP
		frappe.local.form_dict = frappe._dict(cmd=cmd)
		yield
	finally:
		frappe.local.request = old_request
		frappe.local.form_dict = old_form_dict
		frappe.cache.delete(counter_key)


class TestTemplatePermissions(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.manager = make_user("ms-manager@example.com", ["System Manager"])
		cls.outsider = make_user("ms-outsider@example.com", [])
		cls.template = make_template(title="Perm Fixture")

	def setUp(self):
		super().setUp()
		self.addCleanup(frappe.set_user, "Administrator")

	def as_outsider(self):
		frappe.set_user(self.outsider)

	def test_reads_are_denied_without_permission(self):
		self.as_outsider()
		for call in (
			lambda: get_template(self.template.name),
			lambda: list_versions(self.template.name),
		):
			with self.assertRaises(frappe.PermissionError):
				call()

	def test_list_endpoints_do_not_leak_rows(self):
		self.as_outsider()
		# get_list raises rather than returning rows the user may not read.
		with self.assertRaises(frappe.PermissionError):
			list_templates()
		with self.assertRaises(frappe.PermissionError):
			get_block_library()

	def test_writes_are_denied_without_permission(self):
		self.as_outsider()
		with self.assertRaises(frappe.PermissionError):
			create_template(title="Nope", template_type="Email")
		with self.assertRaises(frappe.PermissionError):
			save_template_layout(self.template.name, {"blocks": []})
		with self.assertRaises(frappe.PermissionError):
			publish_template(self.template.name)
		with self.assertRaises(frappe.PermissionError):
			create_version(self.template.name)

	def test_permitted_user_can_round_trip_a_template(self):
		frappe.set_user(self.manager)
		name = create_template(title="Round Trip", template_type="Email")
		save_template_layout(name, {"blocks": [{"type": "Text"}]})

		doc = get_template(name)
		self.assertEqual(doc["layout"], {"blocks": [{"type": "Text"}]})

		self.assertEqual(publish_template(name)["status"], "Published")
		self.assertTrue(any(t.name == name for t in list_templates(status="Published")))

	def test_preview_html_is_sanitised_before_storage(self):
		frappe.set_user(self.manager)
		name = create_template(title="Preview", template_type="Email")
		save_template_layout(
			name,
			{"blocks": []},
			preview_html="<div>hi</div><script>alert(1)</script>",
		)
		stored = frappe.db.get_value("Marketing Template", name, "preview_html")
		self.assertNotIn("<script>", stored)
		self.assertIn("hi", stored)

	def test_malformed_layout_is_rejected(self):
		frappe.set_user(self.manager)
		with self.assertRaises(frappe.ValidationError):
			create_template(title="Bad JSON", template_type="Email", layout="{not json")

	def test_create_template_rejects_unknown_category(self):
		frappe.set_user(self.manager)
		with self.assertRaises(frappe.LinkValidationError):
			create_template(title="Bad Category", template_type="Email", category="No Such Category")

	def test_create_template_strips_html_from_title(self):
		frappe.set_user(self.manager)
		name = create_template(title="<b>Bold</b> Title", template_type="Email")
		self.assertEqual(frappe.db.get_value("Marketing Template", name, "title"), "Bold Title")

	def test_list_templates_filters_by_type_status_and_category(self):
		frappe.set_user(self.manager)
		if not frappe.db.exists("Marketing Template Category", "API Test Category"):
			frappe.get_doc(
				{"doctype": "Marketing Template Category", "category_name": "API Test Category"}
			).insert(ignore_permissions=True)
		name = create_template(title="Filter Me", template_type="SMS", category="API Test Category")

		results = list_templates(template_type="SMS", category="API Test Category")
		self.assertTrue(any(t.name == name for t in results))
		self.assertTrue(all(t.template_type == "SMS" for t in results))

		self.assertFalse(any(t.name == name for t in list_templates(status="Published")))

	def test_get_block_library_parses_default_props_and_filters_inactive(self):
		frappe.set_user(self.manager)
		active = frappe.get_doc(
			{
				"doctype": "Marketing Block",
				"block_name": "API Active Block",
				"block_type": "Text",
				"default_props": {"color": "#fff"},
				"is_active": 1,
			}
		).insert(ignore_permissions=True)
		inactive = frappe.get_doc(
			{
				"doctype": "Marketing Block",
				"block_name": "API Inactive Block",
				"block_type": "Text",
				"is_active": 0,
			}
		).insert(ignore_permissions=True)

		blocks = {b.name: b for b in get_block_library()}
		self.assertIn(active.name, blocks)
		self.assertEqual(blocks[active.name].default_props, {"color": "#fff"})
		self.assertNotIn(inactive.name, blocks)


class TestSubmitForm(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.form = make_template(title="Contact Form", template_type="Web Form", status="Published")
		cls.draft = make_template(title="Draft Form", template_type="Web Form")
		cls.email = make_template(title="Not A Form", template_type="Email", status="Published")

	def setUp(self):
		super().setUp()
		frappe.set_user("Guest")
		self.addCleanup(frappe.set_user, "Administrator")

	def submit(self, **kwargs):
		kwargs.setdefault("template", self.form.name)
		kwargs.setdefault("data", json.dumps({"name": "Ada", "email": "ada@example.com"}))
		return submit_form(**kwargs)

	def test_guest_can_submit_a_published_web_form(self):
		result = self.submit()
		self.assertEqual(result["status"], "ok")
		doc = frappe.get_doc("Marketing Form Submission", result["submission"])
		self.assertEqual(doc.submitter_email, "ada@example.com")
		self.assertEqual(json.loads(doc.submitted_data)["name"], "Ada")

	def test_unpublished_and_non_form_templates_are_refused(self):
		with self.assertRaises(frappe.ValidationError):
			self.submit(template=self.draft.name)
		with self.assertRaises(frappe.ValidationError):
			self.submit(template=self.email.name)

	def test_unknown_template_does_not_leak_existence(self):
		with self.assertRaises(frappe.DoesNotExistError):
			self.submit(template="MKT-TPL-does-not-exist")

	def test_html_in_values_is_stripped(self):
		result = self.submit(
			data=json.dumps({"name": "<script>alert(1)</script>Ada", "message": "<b>hi</b>"})
		)
		stored = json.loads(
			frappe.db.get_value("Marketing Form Submission", result["submission"], "submitted_data")
		)
		self.assertNotIn("<script>", stored["name"])
		self.assertNotIn("<b>", stored["message"])

	def test_oversized_payload_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.submit(data=json.dumps({"note": "x" * 40_000}))

	def test_non_json_and_non_object_payloads_are_rejected(self):
		for payload in ("{not json", json.dumps(["a", "b"]), json.dumps("hello")):
			with self.assertRaises(frappe.ValidationError):
				self.submit(data=payload)

	def test_too_many_fields_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.submit(data=json.dumps({f"f{i}": i for i in range(200)}))

	def test_invalid_email_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.submit(data=json.dumps({"email": "not-an-email"}))

	def test_honeypot_swallows_the_submission(self):
		before = frappe.db.count("Marketing Form Submission")
		result = self.submit(honeypot="i am a bot")
		self.assertEqual(result["status"], "ok")
		self.assertNotIn("submission", result)
		self.assertEqual(frappe.db.count("Marketing Form Submission"), before)

	def test_rate_limit_blocks_the_eleventh_submission_in_a_minute(self):
		with fake_request(SUBMIT_CMD):
			for _ in range(10):
				self.submit()
			with self.assertRaises(frappe.RateLimitExceededError):
				self.submit()
