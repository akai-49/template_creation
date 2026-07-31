# Copyright (c) 2026, Abhishek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from marketing_studio.utils import ensure_json


class MarketingTemplate(Document):
	def validate(self):
		self.layout = ensure_json(self.layout, "Layout", {"blocks": []})

	def on_update(self):
		# Snapshot on the transition into Published so every live version is recoverable.
		if self.status == "Published" and self.has_value_changed("status"):
			self.snapshot_version()

	def snapshot_version(self, version_label=None):
		"""Store the current layout as a Marketing Template Version and return it."""
		return frappe.get_doc(
			{
				"doctype": "Marketing Template Version",
				"template": self.name,
				"version_label": version_label or frappe.utils.now(),
				"layout_snapshot": self.layout,
			}
		).insert(ignore_permissions=True)
