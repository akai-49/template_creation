frappe.ui.form.on("Desktop Icon", {
	link_type: function (frm) {
		if (frm.doc.link_type === "External") {
			frm.set_value("link_to", "");
		} else if (frm.doc.link_type === "Workspace Sidebar") {
			frm.set_value("link", "");
		}
	}
});
