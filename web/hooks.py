# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "web"
app_title = "Frappe Gis Spatial Manager"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Gis Spatial Manager - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/web/css/web.bundle.css"
app_include_js = "/assets/web/js/web.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Gis Spatial Manager Entry": {
        "validate": "web.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "web.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "web.tasks.hourly_sync"
    ],
    "daily": [
        "web.tasks.daily_reconciliation"
    ],
    "weekly": [
        "web.tasks.weekly_digest"
    ]
}
