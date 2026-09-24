# Copyright (c) 2026, Jose Pino and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, flt

from sii_doctype.catalog import ALLOW_FIELD_BY_DOCTYPE, TRANSACTION_DOCTYPES

CHILE_COUNTRY_CODES = {"CL", "CHL"}
CHILE_COUNTRY_NAMES = {"chile"}


def company_is_chile(company: str | None) -> bool:
	if not company:
		return False

	country = frappe.db.get_value("Company", company, "country")
	if not country:
		return False

	if str(country).strip().lower() in CHILE_COUNTRY_NAMES:
		return True

	if str(country).strip().upper() in CHILE_COUNTRY_CODES:
		return True

	code = frappe.db.get_value("Country", country, "code")
	return bool(code) and str(code).upper() in CHILE_COUNTRY_CODES


def get_sii_type(code: str | None):
	if not code:
		return None

	if not frappe.db.exists("SII Document Type", code):
		frappe.throw(_("El tipo de documento SII {0} no existe.").format(code))

	return frappe.get_cached_doc("SII Document Type", code)


def is_outgoing_document(doc, sii_type) -> bool:
	if doc.doctype in ("Sales Invoice", "Delivery Note"):
		return True
	if doc.doctype == "Purchase Invoice":
		return bool(cint(sii_type.issued_by_company))
	return False


def validate_sii_transaction(doc, method=None):
	if doc.doctype not in TRANSACTION_DOCTYPES:
		return

	_validate_references(doc)

	if not doc.meta.has_field("sii_doctype"):
		return

	sii_code = doc.get("sii_doctype")
	folio = cint(doc.get("sii_folio"))
	if not sii_code and not folio:
		return

	if folio and not sii_code:
		frappe.throw(_("Indica el tipo de documento SII junto con el folio."))

	sii_type = get_sii_type(sii_code)
	if not sii_type:
		return

	_validate_type_enabled(sii_type)
	_validate_type_allowed(doc, sii_type)
	_validate_folio_value(folio)
	_validate_note_flags(doc, sii_type)
	_validate_exempt_taxes(doc, sii_type)
	_validate_unique_folio(doc, sii_type, folio)


def validate_sii_required_on_submit(doc, method=None):
	if doc.doctype not in TRANSACTION_DOCTYPES:
		return
	if not doc.meta.has_field("sii_doctype"):
		return
	if not company_is_chile(doc.get("company")):
		return

	if not doc.get("sii_doctype"):
		frappe.throw(_("Las empresas de Chile deben indicar el tipo de documento SII antes de enviar."))

	if not cint(doc.get("sii_folio")):
		frappe.throw(_("Las empresas de Chile deben indicar un folio SII mayor a 0 antes de enviar."))

	sii_type = get_sii_type(doc.get("sii_doctype"))
	_validate_return_against(doc, sii_type)


def _validate_type_enabled(sii_type):
	if cint(sii_type.disabled):
		frappe.throw(_("El tipo de documento SII {0} está deshabilitado.").format(sii_type.code))


def _validate_type_allowed(doc, sii_type):
	allow_field = ALLOW_FIELD_BY_DOCTYPE.get(doc.doctype)
	if allow_field and not cint(sii_type.get(allow_field)):
		frappe.throw(
			_("El tipo SII {0} ({1}) no aplica en {2}.").format(
				sii_type.code, sii_type.document_name, _(doc.doctype)
			)
		)


def _validate_folio_value(folio: int):
	if folio < 0:
		frappe.throw(_("El folio SII no puede ser negativo."))


def _validate_note_flags(doc, sii_type):
	if cint(sii_type.is_credit_note):
		if doc.doctype in ("Sales Invoice", "Purchase Invoice") and not cint(doc.get("is_return")):
			frappe.throw(
				_("El tipo SII {0} es nota de crédito: marca el documento como devolución.").format(
					sii_type.code
				)
			)

	if cint(sii_type.is_debit_note):
		if doc.doctype == "Sales Invoice" and not cint(doc.get("is_debit_note")):
			frappe.throw(
				_("El tipo SII {0} es nota de débito: marca Is Debit Note en la factura de venta.").format(
					sii_type.code
				)
			)
		if doc.doctype == "Purchase Invoice" and cint(doc.get("is_return")):
			frappe.throw(
				_("El tipo SII {0} es nota de débito y no debe marcarse como devolución.").format(sii_type.code)
			)

	if cint(doc.get("is_return")) and not cint(sii_type.is_credit_note):
		if doc.doctype in ("Sales Invoice", "Purchase Invoice"):
			frappe.throw(
				_("Una devolución debe usar una nota de crédito SII (61 o 112), no el tipo {0}.").format(
					sii_type.code
				)
			)

	if cint(doc.get("is_debit_note")) and not cint(sii_type.is_debit_note):
		frappe.throw(
			_("Una nota de débito debe usar un tipo SII de débito (56 o 111), no el tipo {0}.").format(
				sii_type.code
			)
		)


def _validate_return_against(doc, sii_type):
	if not sii_type:
		return
	if cint(sii_type.is_credit_note) and doc.doctype in ("Sales Invoice", "Purchase Invoice"):
		if not doc.get("return_against"):
			frappe.throw(
				_("Las notas de crédito SII deben indicar el documento de origen (Return Against).")
			)


def _validate_exempt_taxes(doc, sii_type):
	if cint(sii_type.get("is_honorarios")):
		return
	if not cint(sii_type.is_exempt):
		return
	if flt(doc.get("total_taxes_and_charges")) > 0.005:
		frappe.throw(
			_("El tipo SII {0} es exento y el documento tiene impuestos gravados.").format(sii_type.code)
		)


def _validate_unique_folio(doc, sii_type, folio: int):
	if not folio:
		return

	filters = {
		"company": doc.company,
		"sii_doctype": doc.sii_doctype,
		"sii_folio": folio,
	}
	if doc.get("name"):
		filters["name"] = ["!=", doc.name]

	if not is_outgoing_document(doc, sii_type):
		party_field = "supplier" if doc.meta.has_field("supplier") else None
		if party_field and doc.get(party_field):
			filters[party_field] = doc.get(party_field)

	duplicate = frappe.db.exists(doc.doctype, filters)
	if not duplicate:
		return

	frappe.throw(
		_("Ya existe {0} {1} con tipo SII {2} y folio {3}.").format(
			_(doc.doctype), duplicate, sii_type.code, folio
		)
	)


def _validate_references(doc):
	if not doc.meta.has_field("sii_references"):
		return

	for i, row in enumerate(doc.get("sii_references") or [], start=1):
		row.nro_lin_ref = i
		if not row.tpo_doc_ref:
			frappe.throw(_("La referencia SII #{0} debe indicar el tipo (TpoDocRef).").format(i))

		if not frappe.db.exists("SII Reference Type", row.tpo_doc_ref):
			frappe.throw(_("El tipo de referencia SII {0} no existe.").format(row.tpo_doc_ref))

		ref_type = frappe.get_cached_doc("SII Reference Type", row.tpo_doc_ref)
		if cint(ref_type.disabled):
			frappe.throw(_("El tipo de referencia SII {0} está deshabilitado.").format(ref_type.code))

		if row.cod_ref and str(row.cod_ref) not in {"1", "2", "3"}:
			frappe.throw(_("El código de referencia de la línea {0} debe ser 1, 2 o 3.").format(i))

		if not cint(row.ind_global) and not (row.folio_ref or "").strip():
			frappe.throw(
				_("La referencia SII #{0} debe tener folio, salvo que sea una referencia global.").format(i)
			)
