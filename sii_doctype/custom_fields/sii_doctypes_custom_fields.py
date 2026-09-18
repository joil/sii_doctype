# Shim for the previous after_migrate hook path.


def create_sii_doctypes_custom_fields():
	from sii_doctype.install import setup_sii_doctype_app

	setup_sii_doctype_app()
