# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "web"
app_title = "Frappe Gis Spatial Manager"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Gis Spatial Manager for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/web/css/web.bundle.css"
app_include_js = "/assets/web/js/web.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "web.engine.on_document_submit",
        "on_cancel": "web.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "web.engine.daily_scheduled_sync"
    ]
}
