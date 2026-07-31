import frappe

# The app ships a desk icon and a workspace sidebar via hooks/fixtures. Both live in
# core doctypes, so uninstalling the app leaves them behind pointing at a dead route.
DESK_ICON_ROUTE = "/marketing-studio"
WORKSPACE_SIDEBAR = "Templates"


def before_uninstall():
	for name in frappe.get_all(
		"Desktop Icon",
		filters={"app": "marketing_studio", "link": DESK_ICON_ROUTE},
		pluck="name",
	):
		frappe.delete_doc("Desktop Icon", name, ignore_permissions=True, force=True)

	if frappe.db.exists("Workspace Sidebar", {"name": WORKSPACE_SIDEBAR, "app": "marketing_studio"}):
		frappe.delete_doc("Workspace Sidebar", WORKSPACE_SIDEBAR, ignore_permissions=True, force=True)
