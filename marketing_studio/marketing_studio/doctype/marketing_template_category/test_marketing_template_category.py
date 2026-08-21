# Copyright (c) 2026, Abhishek and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestMarketingTemplateCategory(IntegrationTestCase):
	def make(self, **kwargs):
		values = {"doctype": "Marketing Template Category", "category_name": "Newsletters"}
		values.update(kwargs)
		return frappe.get_doc(values).insert(ignore_permissions=True)

	def test_named_by_category_name(self):
		doc = self.make(category_name="Named Category")
		self.assertEqual(doc.name, "Named Category")

	def test_category_name_is_required(self):
		# category_name drives autoname (`field:category_name`), so a missing value
		# fails naming validation rather than the generic mandatory-field check.
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({"doctype": "Marketing Template Category"}).insert(ignore_permissions=True)

	def test_category_name_is_unique(self):
		self.make(category_name="Unique Category")
		with self.assertRaises(frappe.DuplicateEntryError):
			self.make(category_name="Unique Category")

	def test_cannot_delete_category_linked_from_a_template(self):
		category = self.make(category_name="Linked Category")
		frappe.get_doc(
			{
				"doctype": "Marketing Template",
				"title": "Uses Category",
				"template_type": "Email",
				"category": category.name,
			}
		).insert(ignore_permissions=True)

		with self.assertRaises(frappe.LinkExistsError):
			category.delete()
