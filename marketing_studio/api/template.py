import json

import frappe
from frappe import _


@frappe.whitelist()
def get_block_library():
	blocks = frappe.get_all(
		"Marketing Block",
		filters={"is_active": 1},
		fields=["name", "block_name", "block_type", "category", "icon", "default_props", "thumbnail"],
		order_by="category asc, block_name asc",
	)
	for block in blocks:
		if block.default_props:
			try:
				block.default_props = json.loads(block.default_props)
			except ValueError:
				block.default_props = {}
	return blocks


@frappe.whitelist()
def list_templates(template_type=None, status=None, category=None):
	filters = {}
	if template_type:
		filters["template_type"] = template_type
	if status:
		filters["status"] = status
	if category:
		filters["category"] = category
	return frappe.get_all(
		"Marketing Template",
		filters=filters,
		fields=[
			"name",
			"title",
			"template_type",
			"status",
			"category",
			"thumbnail",
			"modified",
			"is_default",
		],
		order_by="modified desc",
	)


@frappe.whitelist()
def get_template(name):
	doc = frappe.get_doc("Marketing Template", name)
	doc.check_permission("read")
	data = doc.as_dict()
	if data.get("layout"):
		try:
			data["layout"] = json.loads(data["layout"])
		except ValueError:
			data["layout"] = {"blocks": []}
	else:
		data["layout"] = {"blocks": []}
	return data


@frappe.whitelist()
def create_template(title, template_type, category=None, layout=None):
	doc = frappe.new_doc("Marketing Template")
	doc.title = title
	doc.template_type = template_type
	doc.category = category
	doc.layout = _dumps(layout) if layout else json.dumps({"blocks": []})
	doc.insert()
	return doc.name


@frappe.whitelist()
def save_template_layout(name, layout, preview_html=None):
	doc = frappe.get_doc("Marketing Template", name)
	doc.check_permission("write")
	doc.layout = _dumps(layout)
	if preview_html is not None:
		doc.preview_html = preview_html
	doc.save()
	return {"name": doc.name, "modified": doc.modified}


@frappe.whitelist()
def duplicate_template(name, title=None):
	source = frappe.get_doc("Marketing Template", name)
	source.check_permission("read")
	new = frappe.copy_doc(source)
	new.title = title or f"{source.title} Copy"
	new.status = "Draft"
	new.is_default = 0
	new.insert()
	return new.name


@frappe.whitelist()
def create_version(name, version_label=None):
	template = frappe.get_doc("Marketing Template", name)
	template.check_permission("read")
	version = frappe.new_doc("Marketing Template Version")
	version.template = name
	version.version_label = version_label or frappe.utils.now()
	version.layout_snapshot = template.layout
	version.insert()
	return version.name


@frappe.whitelist()
def list_versions(name):
	return frappe.get_all(
		"Marketing Template Version",
		filters={"template": name},
		fields=["name", "version_label", "creation", "owner"],
		order_by="creation desc",
	)


@frappe.whitelist()
def publish_template(name):
	doc = frappe.get_doc("Marketing Template", name)
	doc.check_permission("write")
	doc.status = "Published"
	doc.published_on = frappe.utils.now()
	doc.save()
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist(allow_guest=True)
def submit_form(template, data, campaign=None):
	tpl = frappe.get_doc("Marketing Template", template)
	if tpl.template_type != "Web Form":
		frappe.throw(_("Template is not a Web Form template"))

	payload = json.loads(data) if isinstance(data, str) else data
	submission = frappe.new_doc("Marketing Form Submission")
	submission.template = template
	submission.campaign = campaign
	submission.submitter_name = payload.get("name")
	submission.submitter_email = payload.get("email")
	submission.submitted_data = json.dumps(payload)
	submission.insert(ignore_permissions=True)
	frappe.db.commit()
	return {"status": "ok", "submission": submission.name}


def _dumps(value):
	if isinstance(value, str):
		return value
	return json.dumps(value)
