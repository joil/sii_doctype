# Copyright (c) 2026, Jose Pino and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class SIIReferenceType(Document):
	def validate(self):
		self.code = (self.code or "").strip()
		if not self.code:
			frappe.throw(_("El código SII es obligatorio."))
		if self.code.isdigit():
			self.sort_code = cint(self.code)
		else:
			self.code = self.code.upper()
			self.sort_code = 9000
