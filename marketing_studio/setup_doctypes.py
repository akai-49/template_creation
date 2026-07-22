import frappe

MODULE = "Marketing Studio"

DEFAULT_PERM = [
	{
		"role": "System Manager",
		"read": 1,
		"write": 1,
		"create": 1,
		"delete": 1,
		"report": 1,
		"export": 1,
		"print": 1,
		"email": 1,
		"share": 1,
	}
]


def create_doctypes():
	create_marketing_template_category()
	create_marketing_block()
	create_marketing_template()
	create_marketing_template_version()
	create_marketing_campaign()
	create_marketing_form_submission()
	frappe.db.commit()
	print("Marketing Studio doctypes created/verified.")


def _create(name, payload):
	if frappe.db.exists("DocType", name):
		print(f"DocType already exists: {name}")
		return
	doc = frappe.get_doc(payload)
	doc.insert(ignore_permissions=True)
	print(f"Created DocType: {name}")


def create_marketing_template_category():
	_create(
		"Marketing Template Category",
		{
			"doctype": "DocType",
			"name": "Marketing Template Category",
			"module": MODULE,
			"custom": 0,
			"autoname": "field:category_name",
			"naming_rule": "By fieldname",
			"fields": [
				{
					"fieldname": "category_name",
					"label": "Category Name",
					"fieldtype": "Data",
					"reqd": 1,
					"unique": 1,
					"in_list_view": 1,
				},
				{
					"fieldname": "description",
					"label": "Description",
					"fieldtype": "Small Text",
				},
			],
			"permissions": DEFAULT_PERM,
		},
	)


def create_marketing_block():
	_create(
		"Marketing Block",
		{
			"doctype": "DocType",
			"name": "Marketing Block",
			"module": MODULE,
			"custom": 0,
			"autoname": "field:block_name",
			"naming_rule": "By fieldname",
			"fields": [
				{
					"fieldname": "block_name",
					"label": "Block Name",
					"fieldtype": "Data",
					"reqd": 1,
					"unique": 1,
					"in_list_view": 1,
				},
				{
					"fieldname": "block_type",
					"label": "Block Type",
					"fieldtype": "Select",
					"options": "Section\nText\nImage\nButton\nColumns\nDivider\nSpacer\nHeader\nFooter\nSocial Icons\nVideo\nForm Field\nHTML",
					"reqd": 1,
					"in_list_view": 1,
					"in_standard_filter": 1,
				},
				{
					"fieldname": "category",
					"label": "Category",
					"fieldtype": "Select",
					"options": "Layout\nContent\nMedia\nForm\nSocial",
					"default": "Content",
					"in_standard_filter": 1,
				},
				{
					"fieldname": "column_break_icon",
					"fieldtype": "Column Break",
				},
				{
					"fieldname": "icon",
					"label": "Icon",
					"fieldtype": "Data",
					"description": "Icon name shown in the block palette",
				},
				{
					"fieldname": "is_standard",
					"label": "Is Standard",
					"fieldtype": "Check",
					"read_only": 1,
					"default": "0",
				},
				{
					"fieldname": "is_active",
					"label": "Is Active",
					"fieldtype": "Check",
					"default": "1",
				},
				{
					"fieldname": "section_break_config",
					"fieldtype": "Section Break",
					"label": "Configuration",
				},
				{
					"fieldname": "default_props",
					"label": "Default Props (JSON)",
					"fieldtype": "Code",
					"options": "JSON",
				},
				{
					"fieldname": "thumbnail",
					"label": "Thumbnail",
					"fieldtype": "Attach Image",
				},
			],
			"permissions": DEFAULT_PERM,
		},
	)


def create_marketing_template():
	_create(
		"Marketing Template",
		{
			"doctype": "DocType",
			"name": "Marketing Template",
			"module": MODULE,
			"custom": 0,
			"autoname": "format:MKT-TPL-{#####}",
			"naming_rule": "Expression",
			"title_field": "title",
			"fields": [
				{
					"fieldname": "title",
					"label": "Title",
					"fieldtype": "Data",
					"reqd": 1,
					"in_list_view": 1,
				},
				{
					"fieldname": "template_type",
					"label": "Template Type",
					"fieldtype": "Select",
					"options": "Email\nWeb Form\nLanding Page\nSMS\nPopup",
					"reqd": 1,
					"in_list_view": 1,
					"in_standard_filter": 1,
				},
				{
					"fieldname": "status",
					"label": "Status",
					"fieldtype": "Select",
					"options": "Draft\nPublished\nArchived",
					"default": "Draft",
					"in_list_view": 1,
					"in_standard_filter": 1,
				},
				{
					"fieldname": "column_break_cat",
					"fieldtype": "Column Break",
				},
				{
					"fieldname": "category",
					"label": "Category",
					"fieldtype": "Link",
					"options": "Marketing Template Category",
				},
				{
					"fieldname": "subject",
					"label": "Subject",
					"fieldtype": "Data",
					"depends_on": "eval:doc.template_type=='Email'",
				},
				{
					"fieldname": "is_default",
					"label": "Is Default",
					"fieldtype": "Check",
					"default": "0",
				},
				{
					"fieldname": "section_break_layout",
					"fieldtype": "Section Break",
					"label": "Layout",
				},
				{
					"fieldname": "layout",
					"label": "Layout (JSON)",
					"fieldtype": "Code",
					"options": "JSON",
					"description": "Drag-and-drop block tree serialized as JSON",
				},
				{
					"fieldname": "preview_html",
					"label": "Preview HTML",
					"fieldtype": "Code",
					"options": "HTML",
					"read_only": 1,
				},
				{
					"fieldname": "thumbnail",
					"label": "Thumbnail",
					"fieldtype": "Attach Image",
				},
				{
					"fieldname": "section_break_meta",
					"fieldtype": "Section Break",
					"label": "Meta",
					"collapsible": 1,
				},
				{
					"fieldname": "tags_csv",
					"label": "Tags",
					"fieldtype": "Data",
				},
				{
					"fieldname": "published_on",
					"label": "Published On",
					"fieldtype": "Datetime",
					"read_only": 1,
				},
			],
			"permissions": DEFAULT_PERM,
		},
	)


def create_marketing_template_version():
	_create(
		"Marketing Template Version",
		{
			"doctype": "DocType",
			"name": "Marketing Template Version",
			"module": MODULE,
			"custom": 0,
			"autoname": "hash",
			"naming_rule": "Random",
			"fields": [
				{
					"fieldname": "template",
					"label": "Template",
					"fieldtype": "Link",
					"options": "Marketing Template",
					"reqd": 1,
					"in_list_view": 1,
				},
				{
					"fieldname": "version_label",
					"label": "Version Label",
					"fieldtype": "Data",
					"in_list_view": 1,
				},
				{
					"fieldname": "layout_snapshot",
					"label": "Layout Snapshot (JSON)",
					"fieldtype": "Code",
					"options": "JSON",
				},
			],
			"permissions": DEFAULT_PERM,
		},
	)


def create_marketing_campaign():
	_create(
		"Marketing Campaign",
		{
			"doctype": "DocType",
			"name": "Marketing Campaign",
			"module": MODULE,
			"custom": 0,
			"autoname": "format:CAMP-{#####}",
			"naming_rule": "Expression",
			"title_field": "campaign_name",
			"fields": [
				{
					"fieldname": "campaign_name",
					"label": "Campaign Name",
					"fieldtype": "Data",
					"reqd": 1,
					"in_list_view": 1,
				},
				{
					"fieldname": "template",
					"label": "Template",
					"fieldtype": "Link",
					"options": "Marketing Template",
					"in_list_view": 1,
				},
				{
					"fieldname": "status",
					"label": "Status",
					"fieldtype": "Select",
					"options": "Draft\nScheduled\nSent\nCompleted\nPaused",
					"default": "Draft",
					"in_list_view": 1,
					"in_standard_filter": 1,
				},
				{
					"fieldname": "column_break_sched",
					"fieldtype": "Column Break",
				},
				{
					"fieldname": "scheduled_on",
					"label": "Scheduled On",
					"fieldtype": "Datetime",
				},
				{
					"fieldname": "sent_on",
					"label": "Sent On",
					"fieldtype": "Datetime",
					"read_only": 1,
				},
				{
					"fieldname": "audience_segment",
					"label": "Audience Segment",
					"fieldtype": "Small Text",
				},
				{
					"fieldname": "section_break_stats",
					"fieldtype": "Section Break",
					"label": "Stats",
				},
				{
					"fieldname": "recipient_count",
					"label": "Recipient Count",
					"fieldtype": "Int",
					"read_only": 1,
					"default": "0",
				},
				{
					"fieldname": "sent_count",
					"label": "Sent Count",
					"fieldtype": "Int",
					"read_only": 1,
					"default": "0",
				},
				{
					"fieldname": "column_break_stats2",
					"fieldtype": "Column Break",
				},
				{
					"fieldname": "open_count",
					"label": "Open Count",
					"fieldtype": "Int",
					"read_only": 1,
					"default": "0",
				},
				{
					"fieldname": "click_count",
					"label": "Click Count",
					"fieldtype": "Int",
					"read_only": 1,
					"default": "0",
				},
			],
			"permissions": DEFAULT_PERM,
		},
	)


def create_marketing_form_submission():
	_create(
		"Marketing Form Submission",
		{
			"doctype": "DocType",
			"name": "Marketing Form Submission",
			"module": MODULE,
			"custom": 0,
			"autoname": "hash",
			"naming_rule": "Random",
			"fields": [
				{
					"fieldname": "template",
					"label": "Template",
					"fieldtype": "Link",
					"options": "Marketing Template",
					"reqd": 1,
					"in_list_view": 1,
				},
				{
					"fieldname": "campaign",
					"label": "Campaign",
					"fieldtype": "Link",
					"options": "Marketing Campaign",
				},
				{
					"fieldname": "submitter_name",
					"label": "Submitter Name",
					"fieldtype": "Data",
					"in_list_view": 1,
				},
				{
					"fieldname": "submitter_email",
					"label": "Submitter Email",
					"fieldtype": "Data",
					"options": "Email",
					"in_list_view": 1,
				},
				{
					"fieldname": "submitted_data",
					"label": "Submitted Data (JSON)",
					"fieldtype": "Code",
					"options": "JSON",
				},
			],
			"permissions": DEFAULT_PERM,
		},
	)
