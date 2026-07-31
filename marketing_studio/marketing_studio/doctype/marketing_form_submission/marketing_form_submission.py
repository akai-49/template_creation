# Copyright (c) 2026, Abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Now

from marketing_studio.utils import ensure_json


class MarketingFormSubmission(Document):
	def validate(self):
		self.submitted_data = ensure_json(self.submitted_data, "Submitted Data", {})

	@staticmethod
	def clear_old_logs(days=365):
		"""Log Settings interface. Retention is editable in Desk under Log Settings.

		This deletes lead data, so the default is deliberately a full year.
		"""
		table = frappe.qb.DocType("Marketing Form Submission")
		frappe.db.delete(table, filters=(table.creation < (Now() - Interval(days=days))))
