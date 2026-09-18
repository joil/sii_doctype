# Copyright (c) 2026, Jose Pino and contributors
# For license information, please see license.txt

import frappe

from sii_doctype.catalog import LEGACY_SII_DOCTYPE_MAP, SII_DOCUMENT_TYPES, TRANSACTION_DOCTYPES
from sii_doctype.custom_fields import remove_legacy_sales_invoice_bill_no, setup_custom_fields


def after_install():
	setup_sii_doctype_app()


def after_migrate():
	setup_sii_doctype_app()


def before_tests():
	setup_sii_doctype_app()


def setup_sii_doctype_app():
	sync_sii_document_types()
	migrate_legacy_sii_doctype_labels()
	setup_custom_fields()
	copy_sales_invoice_bill_no_to_folio()
	remove_legacy_sales_invoice_bill_no()


def sync_sii_document_types():
	for values in SII_DOCUMENT_TYPES:
		code = values["code"]
		if frappe.db.exists("SII Document Type", code):
			doc = frappe.get_doc("SII Document Type", code)
			doc.update(values)
			doc.save(ignore_permissions=True)
		else:
			frappe.get_doc({"doctype": "SII Document Type", **values}).insert(ignore_permissions=True)


def migrate_legacy_sii_doctype_labels():
	for doctype in TRANSACTION_DOCTYPES:
		if not frappe.db.has_column(doctype, "sii_doctype"):
			continue
		for label, code in LEGACY_SII_DOCTYPE_MAP.items():
			frappe.db.sql(
				f"UPDATE `tab{doctype}` SET sii_doctype=%s WHERE sii_doctype=%s",
				(code, label),
			)


def copy_sales_invoice_bill_no_to_folio():
	if not frappe.db.has_column("Sales Invoice", "bill_no"):
		return
	if not frappe.db.has_column("Sales Invoice", "sii_folio"):
		return
	if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "bill_no"}):
		return

	frappe.db.sql(
		"""
		UPDATE `tabSales Invoice`
		SET sii_folio = bill_no
		WHERE IFNULL(sii_folio, 0) = 0 AND IFNULL(bill_no, 0) != 0
		"""
	)
