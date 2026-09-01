app_name = "marketing_studio"
app_title = "Marketing Studio"
app_publisher = "Abhishek"
app_description = "Drag-and-drop marketing template builder for email, web forms and landing pages"
app_email = "abhishek.dev.4949@gmail.com"
app_license = "mit"
app_icon_title = "Marketing Studio"
app_icon_route = "/marketing-studio"

# Apps
# ------------------

# Marketing Form Submission links to "Marketing Campaign", which msuite_workspace owns.
required_apps = ["msuite_workspace"]

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "marketing_studio",
		"logo": "/assets/marketing_studio/logo.svg",
		"title": "Marketing Studio",
		"route": "/marketing-studio",
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/marketing_studio/css/marketing_studio.css"
# app_include_js = "/assets/marketing_studio/js/marketing_studio.js"

# include js, css files in header of web template
# web_include_css = "/assets/marketing_studio/css/marketing_studio.css"
# web_include_js = "/assets/marketing_studio/js/marketing_studio.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "marketing_studio/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "marketing_studio/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

website_route_rules = [
	{"from_route": "/marketing-studio", "to_route": "marketing_studio"},
	{"from_route": "/marketing-studio/<path:app_path>", "to_route": "marketing_studio"},
]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "marketing_studio.utils.jinja_methods",
# 	"filters": "marketing_studio.utils.jinja_filters"
# }

# Installation
# ------------

after_install = "marketing_studio.setup_blocks.seed_blocks"

# Uninstallation
# ------------

before_uninstall = "marketing_studio.uninstall.before_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "marketing_studio.utils.before_app_install"
# after_app_install = "marketing_studio.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "marketing_studio.utils.before_app_uninstall"
# after_app_uninstall = "marketing_studio.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "marketing_studio.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "marketing_studio.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"marketing_studio.tasks.all"
# 	],
# 	"daily": [
# 		"marketing_studio.tasks.daily"
# 	],
# 	"hourly": [
# 		"marketing_studio.tasks.hourly"
# 	],
# 	"weekly": [
# 		"marketing_studio.tasks.weekly"
# 	],
# 	"monthly": [
# 		"marketing_studio.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "marketing_studio.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "marketing_studio.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "marketing_studio.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "marketing_studio.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["marketing_studio.utils.before_request"]
# after_request = ["marketing_studio.utils.after_request"]

# Job Events
# ----------
# before_job = ["marketing_studio.utils.before_job"]
# after_job = ["marketing_studio.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"marketing_studio.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# Submissions are lead data, not logs: Log Settings will pick this up as a default
# retention row and then hard-delete rows older than it, so the window is a full year.
# Change it in Desk (Log Settings) if that's wrong for your retention policy.
default_log_clearing_doctypes = {
	"Marketing Form Submission": 365,
}

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

override_doctype_class = {"Desktop Icon": "marketing_studio.overrides.desktop_icon.CustomDesktopIcon"}

doctype_js = {"Desktop Icon": "public/js/desktop_icon.js"}
