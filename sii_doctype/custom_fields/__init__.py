from frappe.custom.doctype.custom_field.custom_field import create_custom_fields, delete_custom_fields

from sii_doctype.catalog import TRANSACTION_DOCTYPES

MODULE = "Sii Doctype"

COMMON_FIELD_FLAGS = {
	"module": MODULE,
	"is_system_generated": 1,
	"translatable": 0,
}


def _transaction_fields(insert_after: str) -> list[dict]:
	return [
		{
			**COMMON_FIELD_FLAGS,
			"fieldname": "sii_section",
			"label": "SII Chile",
			"fieldtype": "Section Break",
			"insert_after": insert_after,
			"collapsible": 0,
		},
		{
			**COMMON_FIELD_FLAGS,
			"fieldname": "sii_doctype",
			"label": "Tipo de Documento SII",
			"fieldtype": "Link",
			"options": "SII Document Type",
			"insert_after": "sii_section",
			"bold": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"reqd": 0,
			"description": "Código DTE del SII de Chile",
		},
		{
			**COMMON_FIELD_FLAGS,
			"fieldname": "sii_column_break",
			"fieldtype": "Column Break",
			"insert_after": "sii_doctype",
		},
		{
			**COMMON_FIELD_FLAGS,
			"fieldname": "sii_folio",
			"label": "Folio SII",
			"fieldtype": "Int",
			"insert_after": "sii_column_break",
			"bold": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"non_negative": 1,
			"no_copy": 1,
			"reqd": 0,
			"description": "Folio del DTE. Debe ser mayor a 0. Único por empresa y tipo.",
		},
		{
			**COMMON_FIELD_FLAGS,
			"fieldname": "sii_references",
			"label": "Referencias SII",
			"fieldtype": "Table",
			"options": "SII Document Reference",
			"insert_after": "sii_folio",
			"description": "Nodo Referencia del DTE: 801 Orden de Compra, 802 Nota de Pedido, 803 Contrato, u otro DTE.",
		},
	]


def get_custom_fields() -> dict[str, list[dict]]:
	return {
		"Sales Invoice": _transaction_fields("due_date"),
		"Purchase Invoice": _transaction_fields("bill_no"),
		"Delivery Note": _transaction_fields("posting_date"),
		"Purchase Receipt": _transaction_fields("supplier_delivery_note"),
	}


def setup_custom_fields():
	create_custom_fields(get_custom_fields(), ignore_validate=True, update=True)


def remove_legacy_sales_invoice_bill_no():
	delete_custom_fields({"Sales Invoice": ["bill_no"]})


def remove_custom_fields():
	fields = ["sii_section", "sii_doctype", "sii_column_break", "sii_folio", "sii_references"]
	delete_custom_fields({doctype: fields for doctype in TRANSACTION_DOCTYPES})
	remove_legacy_sales_invoice_bill_no()
