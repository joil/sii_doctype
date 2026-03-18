import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_sii_doctypes_custom_fields():
    """
    Crea los campos custom para los doctypes de sii.
    """
    
    # Purchase Invoice
    field_purchase_invoice_sii_doctype = {
        "doctype": "Custom Field",
        "dt": "Purchase Invoice",
        "fieldname": "sii_doctype",
        "label": "Tipo de Documento",
        "fieldtype": "Select",
        "options": "\nFactura Afecta\nFactura Exenta\nNota de Crédito\nNota de Débito\nFactura de Compra",
        "insert_after": "bill_no",
        "reqd": 0,
        "unique": 0,
        "bold": 1,
        "translatable": 0,
        "hidden": 0,
        "description": "Tipo de Documento",
    }

    # Verificar si ya existe
    existing_purchase_invoice = frappe.db.exists("Custom Field", {"dt": "Purchase Invoice", "fieldname": "sii_doctype"})
    if existing_purchase_invoice:
        # Si existe, actualizar
        cf = frappe.get_doc("Custom Field", existing_purchase_invoice)
        cf.update(field_purchase_invoice_sii_doctype)
        cf.save()
        frappe.msgprint("El campo 'sii_doctype' actualizado exitosamente")
    else:
        # Crear el campo
        try:
            # Create and insert the Custom Field document
            custom_field_doc = frappe.get_doc(field_purchase_invoice_sii_doctype)
            custom_field_doc.insert()
            frappe.db.commit() # Commit the changes
            frappe.msgprint(f"Custom field {field_purchase_invoice_sii_doctype['fieldname']} created successfully.")
        except Exception as e:
            frappe.msgprint(f"Failed to create custom field: {e}")

    frappe.clear_cache(doctype="Purchase Invoice")

    # Purchase Receipt

    # Sales Invoice
    field_sales_invoice_sii_doctype = {
        "doctype": "Custom Field",
        "dt": "Sales Invoice",
        "fieldname": "sii_doctype",
        "label": "Tipo de Documento",
        "fieldtype": "Select",
        "options": "\nFactura Afecta\nFactura Exenta\nNota de Crédito\nNota de Débito\nBoleta Afecta\nBoleta Exenta\nComprobantes Pago Electrónico",
        "insert_after": "due_date",
        "reqd": 0,
        "unique": 0,
        "bold": 1,
        "translatable": 0,
        "hidden": 0,
        "description": "Tipo de Documento",
    }

    # Verificar si ya existe
    existing_sales_invoice = frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "sii_doctype"})
    if existing_sales_invoice:
        # Si existe, actualizar
        cf = frappe.get_doc("Custom Field", existing_sales_invoice)
        cf.update(field_sales_invoice_sii_doctype)
        cf.save()
        frappe.msgprint("El campo 'sii_doctype' actualizado exitosamente")
    else:
        # Crear el campo
        try:
            # Create and insert the Custom Field document
            custom_field_doc = frappe.get_doc(field_sales_invoice_sii_doctype)
            custom_field_doc.insert()
            frappe.db.commit() # Commit the changes
            frappe.msgprint(f"Custom field {field_sales_invoice_sii_doctype['fieldname']} created successfully.")
        except Exception as e:
            frappe.msgprint(f"Failed to create custom field: {e}")

    frappe.clear_cache(doctype="Sales Invoice")

    field_sales_invoice_bill_no = {
        "doctype": "Custom Field",
        "dt": "Sales Invoice",
        "fieldname": "bill_no",
        "label": "Número de Documento",
        "fieldtype": "Int",
        "insert_after": "sii_doctype",
        "reqd": 0,
        "unique": 0,
        "bold": 1,
        "translatable": 0,
        "hidden": 0,
        "description": "Número de Documento",
    }

    # Verificar si ya existe
    existing_sales_invoice_bill_no = frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "bill_no"})
    if existing_sales_invoice_bill_no:
        # Si existe, actualizar
        cf = frappe.get_doc("Custom Field", existing_sales_invoice_bill_no)
        cf.update(field_sales_invoice_bill_no)
        cf.save()
        frappe.msgprint("El campo 'bill_no' actualizado exitosamente")
    else:
        # Crear el campo
        try:
            # Create and insert the Custom Field document
            custom_field_doc = frappe.get_doc(field_sales_invoice_bill_no)
            custom_field_doc.insert()
            frappe.db.commit() # Commit the changes
            frappe.msgprint(f"Custom field {field_sales_invoice_bill_no['fieldname']} created successfully.")
        except Exception as e:
            frappe.msgprint(f"Failed to create custom field: {e}")

    frappe.clear_cache(doctype="Sales Invoice")

    # Sales Order
