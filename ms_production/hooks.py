import frappe
from . import __version__ as app_version

app_name = "ms_production"
app_title = "Ms Production"
app_publisher = "Abhishek Chougule"
app_description = "Machine Shop Production"
app_email = "chouguleabhis@gmail.com"
app_license = "Developer MrAbhi"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ms_production/css/ms_production.css"
# app_include_js = "/assets/ms_production/js/ms_production.js"

# include js, css files in header of web template
# web_include_css = "/assets/ms_production/css/ms_production.css"
# web_include_js = "/assets/ms_production/js/ms_production.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ms_production/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "ms_production.utils.jinja_methods",
#	"filters": "ms_production.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ms_production.install.before_install"
# after_install = "ms_production.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ms_production.uninstall.before_uninstall"
# after_uninstall = "ms_production.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ms_production.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"ms_production.tasks.all"
#	],
#	"daily": [
#		"ms_production.tasks.daily"
#	],
#	"hourly": [
#		"ms_production.tasks.hourly"
#	],
#	"weekly": [
#		"ms_production.tasks.weekly"
#	],
#	"monthly": [
#		"ms_production.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "ms_production.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ms_production.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ms_production.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ms_production.utils.before_request"]
# after_request = ["ms_production.utils.after_request"]

# Job Events
# ----------
# before_job = ["ms_production.utils.before_job"]
# after_job = ["ms_production.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ms_production.auth.validate"
# ]

 

# Call the add_hooks function to attach the hooks


doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    # "Production":  {
        # /home/quantbitserver/bench06-alpha/apps/ms_production/ms_production/hooks.py
        # "before_save": "ms_production.ms_production.doctype.production.events.on_status_click"
    # }
}
