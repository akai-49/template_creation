import frappe

# `creation`/`modified` are framework columns, so they can't carry `search_index` in the
# DocType JSON. These queries sort/filter on them: template listing, version history and
# log clearing.
INDEXES = {
	"Marketing Template": ["modified"],
	"Marketing Form Submission": ["creation"],
	"Marketing Template Version": ["creation"],
}


def execute():
	for doctype, fields in INDEXES.items():
		if frappe.db.table_exists(doctype):
			frappe.db.add_index(doctype, fields)
