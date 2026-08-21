# Copyright (c) 2026, Abhishek and Contributors
# See license.txt

import json

import frappe
from frappe.tests import IntegrationTestCase

from marketing_studio.api.template import create_version, duplicate_template


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

	def test_title_is_required(self):
		with self.assertRaises(frappe.MandatoryError):
			frappe.get_doc(
				{"doctype": "Marketing Template", "template_type": "Email"}
			).insert(ignore_permissions=True)

	def test_status_defaults_to_draft(self):
		self.assertEqual(self.make().status, "Draft")

	def test_layout_must_be_valid_json(self):
		with self.assertRaises(frappe.ValidationError):
			self.make(layout="{oops")

	def test_empty_layout_defaults_to_an_empty_block_list(self):
		self.assertEqual(json.loads(self.make(layout=None).layout), {"blocks": []})

	def test_dict_layout_is_serialised(self):
		doc = self.make(layout={"blocks": [{"type": "Text"}]})
		self.assertIsInstance(doc.layout, str)
		self.assertEqual(json.loads(doc.layout)["blocks"][0]["type"], "Text")

	def test_unknown_category_is_rejected(self):
		with self.assertRaises(frappe.LinkValidationError):
			self.make(category="Does Not Exist")

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

	def test_draft_never_snapshots(self):
		doc = self.make()
		doc.title = "Still Draft"
		doc.save()
		self.assertEqual(frappe.db.count("Marketing Template Version", {"template": doc.name}), 0)

	def test_explicit_version_carries_its_label(self):
		doc = self.make()
		version = create_version(doc.name, version_label="before the redesign")
		self.assertEqual(
			frappe.db.get_value("Marketing Template Version", version, "version_label"),
			"before the redesign",
		)

	def test_unlabelled_version_gets_a_timestamp_label(self):
		doc = self.make()
		version = create_version(doc.name)
		label = frappe.db.get_value("Marketing Template Version", version, "version_label")
		# frappe.utils.now() -> "YYYY-MM-DD HH:MM:SS[.ffffff]"
		self.assertRegex(label, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?$")

	def test_duplicate_starts_as_an_unpublished_copy(self):
		source = self.make(title="Original", status="Published", is_default=1)
		copy = frappe.get_doc("Marketing Template", duplicate_template(source.name))
		self.assertEqual(copy.title, "Original Copy")
		self.assertEqual(copy.status, "Draft")
		self.assertEqual(copy.is_default, 0)
		self.assertEqual(copy.layout, source.layout)
		self.assertNotEqual(copy.name, source.name)

	def test_cannot_delete_template_with_versions(self):
		doc = self.make()
		create_version(doc.name, version_label="v1")
		with self.assertRaises(frappe.LinkExistsError):
			doc.delete()
