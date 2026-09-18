app_name = "sii_doctype"
app_title = "Sii Doctype"
app_publisher = "Jose Pino"
app_description = "Catálogo de tipos de documentos electrónicos (DTE) del SII de Chile"
app_email = "joil@joil.cl"
app_license = "mit"

# Apps
# ------------------

required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sii_doctype",
# 		"logo": "/assets/sii_doctype/logo.png",
# 		"title": "Sii Doctype",
# 		"route": "/sii_doctype",
# 		"has_permission": "sii_doctype.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sii_doctype/css/sii_doctype.css"
# app_include_js = "/assets/sii_doctype/js/sii_doctype.js"

# include js, css files in header of web template
# web_include_css = "/assets/sii_doctype/css/sii_doctype.css"
# web_include_js = "/assets/sii_doctype/js/sii_doctype.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sii_doctype/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

doctype_js = {
	"Sales Invoice": "public/js/sii_transaction.js",
	"Purchase Invoice": "public/js/sii_transaction.js",
	"Delivery Note": "public/js/sii_transaction.js",
	"Purchase Receipt": "public/js/sii_transaction.js",
}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sii_doctype/public/icons.svg"

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

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sii_doctype.utils.jinja_methods",
# 	"filters": "sii_doctype.utils.jinja_filters"
# }

# Installation
# ------------

after_install = "sii_doctype.install.after_install"

# Uninstallation
# ------------

before_uninstall = "sii_doctype.uninstall.before_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sii_doctype.utils.before_app_install"
# after_app_install = "sii_doctype.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sii_doctype.utils.before_app_uninstall"
# after_app_uninstall = "sii_doctype.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sii_doctype.notifications.get_notification_config"

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

after_migrate = ["sii_doctype.install.after_migrate"]

doc_events = {
	"Sales Invoice": {
		"validate": "sii_doctype.validations.validate_sii_transaction",
		"before_submit": "sii_doctype.validations.validate_sii_required_on_submit",
	},
	"Purchase Invoice": {
		"validate": "sii_doctype.validations.validate_sii_transaction",
		"before_submit": "sii_doctype.validations.validate_sii_required_on_submit",
	},
	"Delivery Note": {
		"validate": "sii_doctype.validations.validate_sii_transaction",
		"before_submit": "sii_doctype.validations.validate_sii_required_on_submit",
	},
	"Purchase Receipt": {
		"validate": "sii_doctype.validations.validate_sii_transaction",
		"before_submit": "sii_doctype.validations.validate_sii_required_on_submit",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sii_doctype.tasks.all"
# 	],
# 	"daily": [
# 		"sii_doctype.tasks.daily"
# 	],
# 	"hourly": [
# 		"sii_doctype.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sii_doctype.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sii_doctype.tasks.monthly"
# 	],
# }

# Testing
# -------

before_tests = "sii_doctype.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sii_doctype.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sii_doctype.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sii_doctype.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sii_doctype.utils.before_request"]
# after_request = ["sii_doctype.utils.after_request"]

# Job Events
# ----------
# before_job = ["sii_doctype.utils.before_job"]
# after_job = ["sii_doctype.utils.after_job"]

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
# 	"sii_doctype.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

