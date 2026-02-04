import json

import frappe


def execute():
    """
    Remove the ZATCA Workspace feedback and link section added by
    _2025_05_11_add_feedback_links_block. Deletes the Custom HTML Block,
    removes the "Feedback and Links" heading, and removes the block from
    the ZATCA Workspace content.
    """
    block_name = "ZATCA Workspace - Feedback and Link Section"

    # 1. Delete the Custom HTML Block if it exists
    if frappe.db.exists("Custom HTML Block", block_name):
        frappe.delete_doc("Custom HTML Block", block_name)
        frappe.db.commit()

    # 2. Remove the custom block from the ZATCA Workspace via DB to avoid validation issues
    if not frappe.db.exists("Workspace", "ZATCA"):
        return

    # Update content JSON (remove the custom_block and "Feedback and Links" heading)
    content_json = frappe.db.get_value("Workspace", "ZATCA", "content")
    if content_json:
        content = json.loads(content_json)

        def should_remove(item):
            if item.get("type") == "custom_block":
                return item.get("data", {}).get("custom_block_name") == block_name
            if item.get("type") == "header":
                text = item.get("data", {}).get("text") or ""
                return "Feedback and Links" in text
            return False

        content = [item for item in content if not should_remove(item)]
        frappe.db.set_value(
            "Workspace", "ZATCA", "content", json.dumps(content), update_modified=False
        )

    # Delete Workspace Custom Block child rows
    frappe.db.delete(
        "Workspace Custom Block",
        {"parent": "ZATCA", "custom_block_name": block_name},
    )

    frappe.db.commit()
