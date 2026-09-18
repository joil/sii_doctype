# Copyright (c) 2026, Jose Pino and contributors
# For license information, please see license.txt

from sii_doctype.custom_fields import remove_custom_fields


def before_uninstall():
	remove_custom_fields()
