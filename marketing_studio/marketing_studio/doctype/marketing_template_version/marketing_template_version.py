# Copyright (c) 2026, Abhishek and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from marketing_studio.utils import ensure_json


class MarketingTemplateVersion(Document):
	def validate(self):
		self.layout_snapshot = ensure_json(self.layout_snapshot, "Layout Snapshot", {"blocks": []})
