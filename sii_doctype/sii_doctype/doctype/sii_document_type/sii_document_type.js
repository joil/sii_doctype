// Copyright (c) 2026, Jose Pino and contributors
// For license information, please see license.txt

frappe.ui.form.on("SII Document Type", {
	refresh(frm) {
		frm.set_df_property("code", "read_only", !frm.is_new());
	},
});
