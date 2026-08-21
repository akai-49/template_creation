# Copyright (c) 2026, Abhishek and Contributors
# See license.txt

import json

import frappe
from frappe.tests import IntegrationTestCase


class TestMarketingBlock(IntegrationTestCase):
	def make(self, **kwargs):
		values = {
			"doctype": "Marketing Block",
			"block_name": "Test Block",
			"block_type": "Text",
		}
		values.update(kwargs)
		return frappe.get_doc(values).insert(ignore_permissions=True)

	def test_defaults(self):
		doc = self.make(block_name="Defaults Block")
		self.assertEqual(doc.category, "Content")
		self.assertEqual(doc.is_active, 1)
		self.assertEqual(doc.is_standard, 0)

	def test_empty_default_props_becomes_empty_object(self):
		doc = self.make(block_name="Empty Props Block", default_props=None)
		self.assertEqual(json.loads(doc.default_props), {})

	def test_dict_default_props_is_serialised(self):
		doc = self.make(block_name="Dict Props Block", default_props={"color": "#fff"})
		self.assertIsInstance(doc.default_props, str)
		self.assertEqual(json.loads(doc.default_props)["color"], "#fff")

	def test_invalid_default_props_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.make(block_name="Invalid Props Block", default_props="{oops")

	def test_block_name_is_named_and_unique(self):
		self.make(block_name="Unique Block")
		self.assertTrue(frappe.db.exists("Marketing Block", "Unique Block"))
		with self.assertRaises(frappe.DuplicateEntryError):
			self.make(block_name="Unique Block")

	def test_block_name_is_required(self):
		# block_name drives autoname (`field:block_name`), so a missing value fails
		# naming validation rather than the generic mandatory-field check.
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{"doctype": "Marketing Block", "block_type": "Text"}
			).insert(ignore_permissions=True)
