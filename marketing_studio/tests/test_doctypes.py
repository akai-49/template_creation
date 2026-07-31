"""DocType lifecycle tests: validation, versioning, duplication, log clearing."""

import json

import frappe
from frappe.tests import IntegrationTestCase

from marketing_studio.api.template import create_version, duplicate_template
from marketing_studio.setup_blocks import STANDARD_BLOCKS, seed_blocks


class TestMarketingTemplate(IntegrationTestCase):
	def make(self, **kwargs):
		values = {
			"doctype": "Marketing Template",
			"title": "Lifecycle",
			"template_type": "Email",
			"layout": json.dumps({"blocks": []}),
		}
		values.update(kwargs)
		return frappe.get_doc(values).insert(ignore_permissions=True)

	def test_layout_must_be_valid_json(self):
		with self.assertRaises(frappe.ValidationError):
			self.make(layout="{oops")

	def test_empty_layout_defaults_to_an_empty_block_list(self):
		self.assertEqual(json.loads(self.make(layout=None).layout), {"blocks": []})

	def test_dict_layout_is_serialised(self):
		doc = self.make(layout={"blocks": [{"type": "Text"}]})
		self.assertIsInstance(doc.layout, str)
		self.assertEqual(json.loads(doc.layout)["blocks"][0]["type"], "Text")

	def test_publishing_snapshots_a_version(self):
		doc = self.make(layout=json.dumps({"blocks": [{"type": "Text"}]}))
		self.assertEqual(frappe.db.count("Marketing Template Version", {"template": doc.name}), 0)

		doc.status = "Published"
		doc.save()

		versions = frappe.get_all(
			"Marketing Template Version", filters={"template": doc.name}, fields=["layout_snapshot"]
		)
		self.assertEqual(len(versions), 1)
		self.assertEqual(json.loads(versions[0].layout_snapshot)["blocks"][0]["type"], "Text")

	def test_republishing_the_same_status_does_not_snapshot_again(self):
		doc = self.make(status="Published")
		doc.title = "Renamed"
		doc.save()
		self.assertEqual(frappe.db.count("Marketing Template Version", {"template": doc.name}), 1)

	def test_explicit_version_carries_its_label(self):
		doc = self.make()
		version = create_version(doc.name, version_label="before the redesign")
		self.assertEqual(
			frappe.db.get_value("Marketing Template Version", version, "version_label"),
			"before the redesign",
		)

	def test_duplicate_starts_as_an_unpublished_copy(self):
		source = self.make(title="Original", status="Published", is_default=1)
		copy = frappe.get_doc("Marketing Template", duplicate_template(source.name))
		self.assertEqual(copy.title, "Original Copy")
		self.assertEqual(copy.status, "Draft")
		self.assertEqual(copy.is_default, 0)
		self.assertEqual(copy.layout, source.layout)
		self.assertNotEqual(copy.name, source.name)


class TestMarketingFormSubmission(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.template = frappe.get_doc(
			{
				"doctype": "Marketing Template",
				"title": "Submission Fixture",
				"template_type": "Web Form",
				"status": "Published",
			}
		).insert(ignore_permissions=True)

	def make(self, **kwargs):
		values = {
			"doctype": "Marketing Form Submission",
			"template": self.template.name,
			"submitted_data": json.dumps({"a": 1}),
		}
		values.update(kwargs)
		return frappe.get_doc(values).insert(ignore_permissions=True)

	def test_submitted_data_must_be_valid_json(self):
		with self.assertRaises(frappe.ValidationError):
			self.make(submitted_data="{oops")

	def test_clear_old_logs_keeps_recent_submissions(self):
		doc = self.make()
		frappe.get_doc("Marketing Form Submission", doc.name).clear_old_logs(days=365)
		self.assertTrue(frappe.db.exists("Marketing Form Submission", doc.name))

	def test_clear_old_logs_removes_expired_submissions(self):
		doc = self.make()
		frappe.db.set_value(
			"Marketing Form Submission", doc.name, "creation", "2020-01-01 00:00:00", update_modified=False
		)
		frappe.get_doc("Marketing Form Submission", doc.name).clear_old_logs(days=30)
		self.assertFalse(frappe.db.exists("Marketing Form Submission", doc.name))


class TestBlockSeeding(IntegrationTestCase):
	def test_seeding_is_idempotent(self):
		seed_blocks()
		before = frappe.db.count("Marketing Block")
		seed_blocks()
		self.assertEqual(frappe.db.count("Marketing Block"), before)
		self.assertGreaterEqual(before, len(STANDARD_BLOCKS))

	def test_default_props_must_be_valid_json(self):
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Marketing Block",
					"block_name": "Broken Props Block",
					"block_type": "Text",
					"default_props": "{oops",
				}
			).insert(ignore_permissions=True)
