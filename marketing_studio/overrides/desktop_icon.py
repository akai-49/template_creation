import frappe
from frappe.desk.doctype.desktop_icon.desktop_icon import DesktopIcon


class CustomDesktopIcon(DesktopIcon):
	def validate(self):
		if self.link_type == "External":
			self.link_to = None
		elif self.link_type == "Workspace Sidebar":
			self.link = None
		super().validate()

	def _validate_links(self):
		if self.link_type == "External":
			self.link_to = None
		elif self.link_type == "Workspace Sidebar":
			self.link = None
		super()._validate_links()
