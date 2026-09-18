# Copyright (c) 2026, Jose Pino and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class SIIDocumentType(Document):
	def validate(self):
		self.code = (self.code or "").strip()
		if not self.code.isdigit():
			frappe.throw(_("El código SII debe ser numérico."))
		self.sort_code = cint(self.code)

		if not any(
			cint(self.get(field))
			for field in (
				"allow_sales",
				"allow_purchase",
				"allow_delivery_note",
				"allow_purchase_receipt",
			)
		):
			frappe.throw(_("Selecciona al menos un DocType de ERPNext donde aplique este tipo SII."))
