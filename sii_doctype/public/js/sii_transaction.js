// Copyright (c) 2026, Jose Pino and contributors
// For license information, please see license.txt

const SII_FILTER_FIELD = {
	"Sales Invoice": "allow_sales",
	"Purchase Invoice": "allow_purchase",
	"Delivery Note": "allow_delivery_note",
	"Purchase Receipt": "allow_purchase_receipt",
};

function setup_sii_form(frm) {
	const filter_field = SII_FILTER_FIELD[frm.doctype];
	if (!filter_field) {
		return;
	}

	frm.set_query("sii_doctype", () => ({
		filters: {
			[filter_field]: 1,
			disabled: 0,
		},
	}));
	frm.set_query("tpo_doc_ref", "sii_references", () => ({
		filters: { disabled: 0 },
	}));
}

function apply_sii_type_flags(frm) {
	if (!frm.doc.sii_doctype) {
		return;
	}

	frappe.db.get_value(
		"SII Document Type",
		frm.doc.sii_doctype,
		["is_credit_note", "is_debit_note", "document_name"],
		(r) => {
			if (!r) {
				return;
			}
			if (cint(r.is_credit_note) && frm.fields_dict.is_return) {
				frm.set_value("is_return", 1);
			}
			if (cint(r.is_debit_note) && frm.fields_dict.is_debit_note) {
				frm.set_value("is_debit_note", 1);
			}
		}
	);
}

["Sales Invoice", "Purchase Invoice", "Delivery Note", "Purchase Receipt"].forEach((doctype) => {
	frappe.ui.form.on(doctype, {
		setup: setup_sii_form,
		sii_doctype: apply_sii_type_flags,
	});
});
