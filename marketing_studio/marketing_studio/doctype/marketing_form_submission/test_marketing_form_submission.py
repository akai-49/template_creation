# Copyright (c) 2026, Abhishek and Contributors
# See license.txt

import json

import frappe
from frappe.tests import IntegrationTestCase

# `campaign` links to Marketing Campaign, owned by msuite_workspace. Pulling in its
# full fixture graph is unnecessary for these tests and can drag in unrelated (and
# occasionally broken) doctype chains from other installed apps.
IGNORE_TEST_RECORD_DEPENDENCIES = ["Marketing Campaign"]


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

	def test_template_is_required(self):
		with self.assertRaises(frappe.MandatoryError):
			frappe.get_doc(
				{"doctype": "Marketing Form Submission", "submitted_data": json.dumps({"a": 1})}
			).insert(ignore_permissions=True)

	def test_unknown_template_is_rejected(self):
		with self.assertRaises(frappe.LinkValidationError):
			self.make(template="MKT-TPL-does-not-exist")

	def test_submitted_data_must_be_valid_json(self):
		with self.assertRaises(frappe.ValidationError):
			self.make(submitted_data="{oops")

	def test_empty_submitted_data_defaults_to_an_empty_object(self):
		doc = self.make(submitted_data=None)
		self.assertEqual(json.loads(doc.submitted_data), {})

	def test_dict_submitted_data_is_serialised(self):
		doc = self.make(submitted_data={"name": "Ada"})
		self.assertIsInstance(doc.submitted_data, str)
		self.assertEqual(json.loads(doc.submitted_data)["name"], "Ada")

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

	def test_clear_old_logs_only_touches_this_doctype(self):
		submission = self.make()
		frappe.db.set_value(
			"Marketing Form Submission",
			submission.name,
			"creation",
			"2020-01-01 00:00:00",
			update_modified=False,
		)
		other_template = self.template.name
		frappe.get_doc("Marketing Form Submission", submission.name).clear_old_logs(days=30)
		self.assertFalse(frappe.db.exists("Marketing Form Submission", submission.name))
		# The linked template itself must survive the log-clearing sweep.
		self.assertTrue(frappe.db.exists("Marketing Template", other_template))
