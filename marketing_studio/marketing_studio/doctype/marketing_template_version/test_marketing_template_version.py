# Copyright (c) 2026, Abhishek and Contributors
# See license.txt

import json

import frappe
from frappe.tests import IntegrationTestCase


class TestMarketingTemplateVersion(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.template = frappe.get_doc(
			{
				"doctype": "Marketing Template",
				"title": "Version Fixture",
				"template_type": "Email",
			}
		).insert(ignore_permissions=True)

	def make(self, **kwargs):
		values = {
			"doctype": "Marketing Template Version",
			"template": self.template.name,
			"layout_snapshot": json.dumps({"blocks": []}),
		}
		values.update(kwargs)
		return frappe.get_doc(values).insert(ignore_permissions=True)

	def test_template_is_required(self):
		with self.assertRaises(frappe.MandatoryError):
			frappe.get_doc(
				{"doctype": "Marketing Template Version", "layout_snapshot": json.dumps({"blocks": []})}
			).insert(ignore_permissions=True)

	def test_unknown_template_is_rejected(self):
		with self.assertRaises(frappe.LinkValidationError):
			self.make(template="MKT-TPL-does-not-exist")

	def test_layout_snapshot_must_be_valid_json(self):
		with self.assertRaises(frappe.ValidationError):
			self.make(layout_snapshot="{oops")

	def test_empty_layout_snapshot_defaults_to_an_empty_block_list(self):
		doc = self.make(layout_snapshot=None)
		self.assertEqual(json.loads(doc.layout_snapshot), {"blocks": []})

	def test_dict_layout_snapshot_is_serialised(self):
		doc = self.make(layout_snapshot={"blocks": [{"type": "Image"}]})
		self.assertIsInstance(doc.layout_snapshot, str)
		self.assertEqual(json.loads(doc.layout_snapshot)["blocks"][0]["type"], "Image")
