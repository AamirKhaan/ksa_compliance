import frappe


def execute():
    """Remove Address doctype customizations (custom_area, custom_building_number)."""
    fields = [
        'Address-custom_area',
        'Address-custom_building_number',
    ]
    for field in fields:
        if frappe.db.exists('Custom Field', field):
            frappe.delete_doc('Custom Field', field)

    frappe.db.commit()

    frappe.db.sql("""
        ALTER TABLE `tabAddress`
        DROP COLUMN IF EXISTS `custom_area`,
        DROP COLUMN IF EXISTS `custom_building_number`
    """)
