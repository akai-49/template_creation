# Copyright (c) 2026, Abhishek and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from marketing_studio.utils import ensure_json


class MarketingBlock(Document):
	def validate(self):
		self.default_props = ensure_json(self.default_props, "Default Props", {})
