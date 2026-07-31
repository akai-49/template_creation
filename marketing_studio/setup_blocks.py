import json

import frappe

PADDING = {"paddingTop": 12, "paddingBottom": 12, "paddingLeft": 24, "paddingRight": 24}

STANDARD_BLOCKS = [
	{
		"block_name": "Header",
		"block_type": "Header",
		"category": "Layout",
		"icon": "layout-header",
		"default_props": {"backgroundColor": "#ffffff", **PADDING},
	},
	{
		"block_name": "Footer",
		"block_type": "Footer",
		"category": "Layout",
		"icon": "layout-footer",
		"default_props": {"backgroundColor": "#f5f5f5", "text": "© Your Company", **PADDING},
	},
	{
		"block_name": "Section",
		"block_type": "Section",
		"category": "Layout",
		"icon": "square",
		"default_props": {
			"backgroundColor": "#ffffff",
			"paddingTop": 24,
			"paddingBottom": 24,
			"paddingLeft": 24,
			"paddingRight": 24,
		},
	},
	{
		"block_name": "Columns",
		"block_type": "Columns",
		"category": "Layout",
		"icon": "columns",
		"default_props": {"backgroundColor": "#ffffff", "gap": 16, **PADDING},
	},
	{
		"block_name": "Text",
		"block_type": "Text",
		"category": "Content",
		"icon": "type",
		"default_props": {
			"text": "Edit this text",
			"color": "#111111",
			"backgroundColor": "",
			"fontSize": 16,
			"fontWeight": "normal",
			"align": "left",
			"paddingTop": 12,
			"paddingBottom": 12,
			"paddingLeft": 24,
			"paddingRight": 24,
		},
	},
	{
		"block_name": "Heading",
		"block_type": "Text",
		"category": "Content",
		"icon": "heading",
		"default_props": {
			"text": "Heading",
			"color": "#111111",
			"backgroundColor": "",
			"fontSize": 28,
			"fontWeight": "bold",
			"align": "left",
			"paddingTop": 12,
			"paddingBottom": 12,
			"paddingLeft": 24,
			"paddingRight": 24,
		},
	},
	{
		"block_name": "Button",
		"block_type": "Button",
		"category": "Content",
		"icon": "mouse-pointer-click",
		"default_props": {
			"label": "Click Here",
			"url": "#",
			"width": "auto",
			"style": "rounded",
			"textColor": "#ffffff",
			"backgroundColor": "#5b21b6",
			"fontSize": 16,
			"fontWeight": "bold",
			"align": "left",
			"paddingTop": 12,
			"paddingBottom": 12,
			"paddingLeft": 24,
			"paddingRight": 24,
		},
	},
	{
		"block_name": "Image",
		"block_type": "Image",
		"category": "Media",
		"icon": "image",
		"default_props": {
			"src": "",
			"alt": "",
			"width": 100,
			"align": "center",
			"paddingTop": 12,
			"paddingBottom": 12,
			"paddingLeft": 24,
			"paddingRight": 24,
		},
	},
	{
		"block_name": "Video",
		"block_type": "Video",
		"category": "Media",
		"icon": "video",
		"default_props": {"url": "", "thumbnail": "", **PADDING},
	},
	{
		"block_name": "Divider",
		"block_type": "Divider",
		"category": "Layout",
		"icon": "minus",
		"default_props": {"color": "#e5e7eb", "thickness": 1, **PADDING},
	},
	{
		"block_name": "Spacer",
		"block_type": "Spacer",
		"category": "Layout",
		"icon": "move-vertical",
		"default_props": {"height": 24, **PADDING},
	},
	{
		"block_name": "Social Icons",
		"block_type": "Social Icons",
		"category": "Social",
		"icon": "share-2",
		"default_props": {"facebook": "", "twitter": "", "instagram": "", "linkedin": "", **PADDING},
	},
	{
		"block_name": "Form Field",
		"block_type": "Form Field",
		"category": "Form",
		"icon": "list-checks",
		"default_props": {
			"label": "Field",
			"fieldtype": "Data",
			"required": False,
			"placeholder": "",
			**PADDING,
		},
	},
	{
		"block_name": "Custom HTML",
		"block_type": "HTML",
		"category": "Content",
		"icon": "code",
		"default_props": {"html": "<div></div>", **PADDING},
	},
]


def seed_blocks():
	for block in STANDARD_BLOCKS:
		if frappe.db.exists("Marketing Block", block["block_name"]):
			continue
		doc = frappe.new_doc("Marketing Block")
		doc.block_name = block["block_name"]
		doc.block_type = block["block_type"]
		doc.category = block["category"]
		doc.icon = block["icon"]
		doc.default_props = json.dumps(block["default_props"])
		doc.is_standard = 1
		doc.is_active = 1
		doc.insert(ignore_permissions=True)
		print(f"Seeded block: {block['block_name']}")
	print("Block library seeded.")


def update_block_defaults():
	"""Refresh default_props on already-seeded standard blocks (schema changed after first seed)."""
	for block in STANDARD_BLOCKS:
		if not frappe.db.exists("Marketing Block", block["block_name"]):
			continue
		frappe.db.set_value(
			"Marketing Block",
			block["block_name"],
			"default_props",
			json.dumps(block["default_props"]),
		)
		print(f"Updated defaults: {block['block_name']}")
	print("Block defaults updated.")
