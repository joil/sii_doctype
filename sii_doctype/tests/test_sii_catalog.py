# Copyright (c) 2026, Jose Pino and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, nowdate

from sii_doctype.catalog import LEGACY_SII_DOCTYPE_MAP, SII_DOCUMENT_TYPES, SII_REFERENCE_TYPES
from sii_doctype.install import setup_sii_doctype_app
from sii_doctype.validations import (
	validate_sii_required_on_submit,
	validate_sii_transaction,
)


class TestSIICatalog(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		setup_sii_doctype_app()

	def test_catalog_has_official_dte_codes(self):
		codes = {row["code"] for row in SII_DOCUMENT_TYPES}
		self.assertEqual(
			codes,
			{"33", "34", "39", "41", "43", "46", "48", "52", "56", "61", "110", "111", "112"},
		)
		self.assertEqual(len(SII_DOCUMENT_TYPES), 13)

	def test_sync_creates_document_types(self):
		for row in SII_DOCUMENT_TYPES:
			self.assertTrue(frappe.db.exists("SII Document Type", row["code"]))
			doc = frappe.get_doc("SII Document Type", row["code"])
			self.assertEqual(doc.document_name, row["document_name"])
			self.assertEqual(doc.allow_sales, row["allow_sales"])
			self.assertEqual(doc.allow_purchase, row["allow_purchase"])
			self.assertEqual(doc.allow_delivery_note, row["allow_delivery_note"])
			self.assertEqual(doc.allow_purchase_receipt, row["allow_purchase_receipt"])

	def test_custom_fields_are_links(self):
		for doctype in ("Sales Invoice", "Purchase Invoice", "Delivery Note", "Purchase Receipt"):
			field = frappe.get_meta(doctype).get_field("sii_doctype")
			self.assertIsNotNone(field, f"falta sii_doctype en {doctype}")
			self.assertEqual(field.fieldtype, "Link")
			self.assertEqual(field.options, "SII Document Type")
			folio = frappe.get_meta(doctype).get_field("sii_folio")
			self.assertIsNotNone(folio, f"falta sii_folio en {doctype}")
			self.assertEqual(folio.fieldtype, "Int")
			refs = frappe.get_meta(doctype).get_field("sii_references")
			self.assertIsNotNone(refs, f"falta sii_references en {doctype}")
			self.assertEqual(refs.fieldtype, "Table")
			self.assertEqual(refs.options, "SII Document Reference")

	def test_sales_invoice_no_longer_has_custom_bill_no(self):
		self.assertFalse(
			frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "bill_no"})
		)

	def test_legacy_labels_map_to_sii_codes(self):
		self.assertEqual(LEGACY_SII_DOCTYPE_MAP["Factura Afecta"], "33")
		self.assertEqual(LEGACY_SII_DOCTYPE_MAP["Nota de Crédito"], "61")
		self.assertEqual(LEGACY_SII_DOCTYPE_MAP["Factura de Compra"], "46")

	def test_honorarios_is_purchase_only(self):
		doc = frappe.get_doc("SII Document Type", "48")
		self.assertEqual(doc.document_name, "Boleta de Honorarios Electrónica")
		self.assertEqual(doc.allow_purchase, 1)
		self.assertEqual(doc.allow_sales, 0)
		self.assertEqual(doc.is_honorarios, 1)

	def test_honorarios_not_allowed_on_sales_invoice(self):
		doc = frappe.new_doc("Sales Invoice")
		doc.company = frappe.db.get_value("Company", {}, "name")
		doc.sii_doctype = "48"
		doc.sii_folio = 12
		self.assertRaises(frappe.ValidationError, validate_sii_transaction, doc)

	def test_guia_is_not_allowed_on_sales_invoice(self):
		doc = frappe.new_doc("Sales Invoice")
		doc.company = frappe.db.get_value("Company", {}, "name")
		doc.sii_doctype = "52"
		doc.sii_folio = 10
		self.assertRaises(frappe.ValidationError, validate_sii_transaction, doc)

	def test_credit_note_requires_is_return(self):
		doc = frappe.new_doc("Sales Invoice")
		doc.company = frappe.db.get_value("Company", {}, "name")
		doc.sii_doctype = "61"
		doc.sii_folio = 11
		doc.is_return = 0
		self.assertRaises(frappe.ValidationError, validate_sii_transaction, doc)

	def test_chile_company_requires_folio_on_submit(self):
		company = frappe.db.get_value("Company", {}, "name")
		previous_country = frappe.db.get_value("Company", company, "country")
		frappe.db.set_value("Company", company, "country", "Chile")
		try:
			doc = frappe.new_doc("Sales Invoice")
			doc.company = company
			doc.sii_doctype = "33"
			doc.sii_folio = 0
			self.assertRaises(frappe.ValidationError, validate_sii_required_on_submit, doc)
		finally:
			frappe.db.set_value("Company", company, "country", previous_country)

	def test_duplicate_outgoing_folio(self):
		company = frappe.db.get_value("Company", {}, "name")
		customer = _ensure_customer()
		item = _ensure_item()
		if not company or not customer or not item:
			self.skipTest("Faltan masters de ERPNext para crear una Sales Invoice")

		first = _make_sales_invoice(company, customer, item, sii_doctype="33", sii_folio=88001)
		first.insert(ignore_permissions=True)
		second = _make_sales_invoice(company, customer, item, sii_doctype="33", sii_folio=88001)
		self.assertRaises(frappe.ValidationError, second.insert, ignore_permissions=True)

	def test_reference_types_include_orden_de_compra(self):
		codes = {row["code"] for row in SII_REFERENCE_TYPES}
		self.assertTrue({"801", "802", "803", "HES", "SET"}.issubset(codes))
		for row in SII_REFERENCE_TYPES:
			self.assertTrue(frappe.db.exists("SII Reference Type", row["code"]))
		self.assertEqual(frappe.db.get_value("SII Reference Type", "801", "reference_name"), "Orden de Compra")
		self.assertEqual(frappe.db.get_value("SII Reference Type", "33", "category"), "DTE")

	def test_reference_requires_folio(self):
		doc = frappe.new_doc("Sales Invoice")
		doc.company = frappe.db.get_value("Company", {}, "name")
		doc.append(
			"sii_references",
			{"tpo_doc_ref": "801", "folio_ref": "", "ind_global": 0},
		)
		self.assertRaises(frappe.ValidationError, validate_sii_transaction, doc)


def _ensure_customer():
	name = frappe.db.get_value("Customer", {}, "name")
	if name:
		return name
	group = frappe.db.get_value("Customer Group", {"is_group": 0}, "name")
	territory = frappe.db.get_value("Territory", {"is_group": 0}, "name")
	if not group or not territory:
		return None
	doc = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": "Cliente SII Catalog Test",
			"customer_type": "Company",
			"customer_group": group,
			"territory": territory,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_item():
	if frappe.db.exists("Item", "ITEM-SII-CATALOG"):
		return "ITEM-SII-CATALOG"
	group = frappe.db.get_value("Item Group", {"is_group": 0}, "name")
	uom = frappe.db.get_single_value("Stock Settings", "stock_uom") or "Nos"
	if not group:
		return None
	doc = frappe.get_doc(
		{
			"doctype": "Item",
			"item_code": "ITEM-SII-CATALOG",
			"item_name": "Item SII Catalog",
			"item_group": group,
			"stock_uom": uom,
			"is_stock_item": 0,
			"is_sales_item": 1,
			"is_purchase_item": 1,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _make_sales_invoice(company, customer, item, sii_doctype, sii_folio):
	return frappe.get_doc(
		{
			"doctype": "Sales Invoice",
			"customer": customer,
			"company": company,
			"posting_date": nowdate(),
			"due_date": add_days(nowdate(), 30),
			"sii_doctype": sii_doctype,
			"sii_folio": sii_folio,
			"items": [{"item_code": item, "qty": 1, "rate": 1000}],
		}
	)
