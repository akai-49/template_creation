"""Coverage for app-level logic that doesn't belong to a single doctype:
setup/seed scripts, the shared `ensure_json` helper, and hook overrides.
"""

from contextlib import contextmanager
import json

import frappe
from frappe.tests import IntegrationTestCase

from marketing_studio.setup_blocks import STANDARD_BLOCKS, seed_blocks, update_block_defaults
from marketing_studio.uninstall import DESK_ICON_ROUTE, WORKSPACE_SIDEBAR, before_uninstall
from marketing_studio.utils import ensure_json


@contextmanager
def _allow_workspace_sidebar_insert():
	"""Frappe v16 marks Workspace Sidebar as an inert archive whose rows can
	only be created during migration, patch, or install. Enable in_patch
	strictly for fixture insertion and restore the prior flag state.
	"""
	previous = getattr(frappe.flags, "in_patch", None)
	frappe.flags.in_patch = True
	try:
		yield
	finally:
		frappe.flags.in_patch = previous


class TestBlockSeeding(IntegrationTestCase):
	def test_seeding_is_idempotent(self):
		seed_blocks()
		before = frappe.db.count("Marketing Block")
		seed_blocks()
		self.assertEqual(frappe.db.count("Marketing Block"), before)
		self.assertGreaterEqual(before, len(STANDARD_BLOCKS))

	def test_seeding_marks_blocks_standard_and_active(self):
		seed_blocks()
		doc = frappe.get_doc("Marketing Block", STANDARD_BLOCKS[0]["block_name"])
		self.assertEqual(doc.is_standard, 1)
		self.assertEqual(doc.is_active, 1)

	def test_update_block_defaults_refreshes_existing_blocks_only(self):
		seed_blocks()
		name = STANDARD_BLOCKS[0]["block_name"]
		frappe.db.set_value("Marketing Block", name, "default_props", json.dumps({"stale": True}))

		update_block_defaults()

		refreshed = json.loads(frappe.db.get_value("Marketing Block", name, "default_props"))
		self.assertEqual(refreshed, STANDARD_BLOCKS[0]["default_props"])
		# A block that was never seeded must not be created by the refresh pass.
		self.assertFalse(frappe.db.exists("Marketing Block", "Never Seeded Block"))


class TestEnsureJson(IntegrationTestCase):
	def test_none_and_empty_string_use_the_default(self):
		self.assertEqual(json.loads(ensure_json(None, "Field")), {})
		self.assertEqual(json.loads(ensure_json("", "Field", {"blocks": []})), {"blocks": []})

	def test_dict_and_list_are_serialised(self):
		self.assertEqual(json.loads(ensure_json({"a": 1}, "Field")), {"a": 1})
		self.assertEqual(json.loads(ensure_json([1, 2], "Field")), [1, 2])

	def test_valid_json_string_passes_through_unchanged(self):
		raw = json.dumps({"a": 1})
		self.assertEqual(ensure_json(raw, "Field"), raw)

	def test_invalid_json_string_throws(self):
		with self.assertRaises(frappe.ValidationError):
			ensure_json("{oops", "Field")


class TestDesktopIconOverride(IntegrationTestCase):
	def test_external_link_clears_link_to(self):
		doc = frappe.get_doc(
			{
				"doctype": "Desktop Icon",
				"label": "MS External Icon",
				"icon_type": "Link",
				"link_type": "External",
				"link": "/marketing-studio",
				"link_to": "Marketing Template",
			}
		).insert(ignore_permissions=True)
		self.assertIsNone(doc.link_to)
		self.assertEqual(doc.link, "/marketing-studio")

	def test_workspace_sidebar_link_clears_link(self):
		with _allow_workspace_sidebar_insert():
			sidebar = frappe.get_doc(
				{"doctype": "Workspace Sidebar", "title": "MS Override Test Sidebar"}
			).insert(ignore_permissions=True)
		doc = frappe.get_doc(
			{
				"doctype": "Desktop Icon",
				"label": "MS Sidebar Icon",
				"icon_type": "Link",
				"link_type": "Workspace Sidebar",
				"link": "/marketing-studio",
				"link_to": sidebar.name,
			}
		).insert(ignore_permissions=True)
		self.assertIsNone(doc.link)
		self.assertEqual(doc.link_to, sidebar.name)


class TestUninstallCleanup(IntegrationTestCase):
	def setUp(self):
		super().setUp()
		# Guard against a leftover fixture from an earlier interrupted run.
		if frappe.db.exists("Workspace Sidebar", WORKSPACE_SIDEBAR):
			frappe.delete_doc("Workspace Sidebar", WORKSPACE_SIDEBAR, ignore_permissions=True, force=True)

	def test_before_uninstall_removes_the_app_desk_icon(self):
		frappe.get_doc(
			{
				"doctype": "Desktop Icon",
				"label": "MS Uninstall Icon",
				"icon_type": "App",
				"link_type": "External",
				"link": DESK_ICON_ROUTE,
				"app": "marketing_studio",
			}
		).insert(ignore_permissions=True)

		before_uninstall()

		self.assertFalse(
			frappe.db.exists("Desktop Icon", {"app": "marketing_studio", "link": DESK_ICON_ROUTE})
		)

	def test_before_uninstall_removes_the_workspace_sidebar(self):
		with _allow_workspace_sidebar_insert():
			frappe.get_doc(
				{
					"doctype": "Workspace Sidebar",
					"title": WORKSPACE_SIDEBAR,
					"app": "marketing_studio",
				}
			).insert(ignore_permissions=True)

		before_uninstall()

		self.assertFalse(frappe.db.exists("Workspace Sidebar", WORKSPACE_SIDEBAR))

	def test_before_uninstall_leaves_unrelated_records_alone(self):
		other = frappe.get_doc(
			{
				"doctype": "Desktop Icon",
				"label": "Unrelated App Icon",
				"icon_type": "App",
				"link_type": "External",
				"link": "/some-other-app",
				"app": "some_other_app",
			}
		).insert(ignore_permissions=True)

		before_uninstall()

		self.assertTrue(frappe.db.exists("Desktop Icon", other.name))
