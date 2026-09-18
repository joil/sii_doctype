# Sii Doctype

Catálogo de tipos de documentos electrónicos (DTE) del [SII de Chile](https://www.sii.cl/) para ERPNext v16.

La app registra los códigos oficiales DTE, los enlaza a facturas y guías de ERPNext, y valida folio, tipo y notas de crédito/débito. **No emite XML, CAF ni Track ID**: eso corresponde a una app de facturación electrónica.

Requiere **ERPNext**. Compatible con Frappe/ERPNext version-16.

## Instalación

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench --site $SITE install-app sii_doctype
```

Al instalar (y en cada `bench migrate`) la app:

1. Crea o actualiza el DocType **SII Document Type** con los 12 DTE.
2. Agrega la sección **SII Chile** en Sales Invoice, Purchase Invoice, Delivery Note y Purchase Receipt.
3. Migra etiquetas antiguas del `Select` (`Factura Afecta` → `33`, etc.).
4. Copia `bill_no` custom de Sales Invoice a `sii_folio` y elimina ese campo custom.

Para desinstalar:

```bash
bench --site $SITE uninstall-app sii_doctype
```

Se eliminan los Custom Fields de la app. Los registros de **SII Document Type** se borran con el DocType.

## Uso

En el escritorio, busca **SII Document Type** para ver o editar el catálogo.

En Factura de Venta, Factura de Compra, Nota de Entrega y Recibo de Compra aparece la sección **SII Chile**:

| Campo | Descripción |
| --- | --- |
| Tipo de Documento SII | Link al catálogo. Solo muestra tipos válidos para ese DocType. |
| Folio SII | Número de folio del DTE. No se copia al duplicar. Debe ser mayor a 0. |

Al elegir una nota de crédito o débito, el formulario marca automáticamente *Is Return* o *Is Debit Note* si el DocType lo permite.

## Catálogo DTE

Los códigos se sincronizan desde `sii_doctype/catalog.py` en cada install/migrate.

| Código | Documento | Venta | Compra | Guía (DN) | Recibo (PR) | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| 33 | Factura Electrónica | Sí | Sí (recibida) | | | |
| 34 | Factura No Afecta o Exenta Electrónica | Sí | Sí (recibida) | | | Exento |
| 39 | Boleta Electrónica | Sí | | | | |
| 41 | Boleta Exenta Electrónica | Sí | | | | Exento |
| 43 | Liquidación Factura Electrónica | Sí | | | | |
| 46 | Factura de Compra Electrónica | | Sí (emitida por la empresa) | | | Folio propio |
| 52 | Guía de Despacho Electrónica | | | Sí | Sí | |
| 56 | Nota de Débito Electrónica | Sí | Sí | | | |
| 61 | Nota de Crédito Electrónica | Sí | Sí | | | |
| 110 | Factura de Exportación Electrónica | Sí | | | | Exportación |
| 111 | Nota de Débito de Exportación Electrónica | Sí | | | | Exportación |
| 112 | Nota de Crédito de Exportación Electrónica | Sí | | | | Exportación |

Puedes deshabilitar un tipo en el maestro; no se podrá usar en transacciones.

## Validaciones

Si se indica tipo o folio (en borrador o al guardar):

- El tipo debe existir, estar habilitado y aplicar al DocType.
- El folio no puede ser negativo.
- Guía 52 no se usa en facturas.
- NC (61, 112) exige documento de devolución (`is_return`).
- ND de venta (56, 111) exige *Is Debit Note*.
- Una devolución de factura no puede usar un tipo que no sea NC.
- Tipos exentos (34, 41) no admiten impuestos gravados.
- El folio es único por compañía + tipo. En documentos recibidos (compra o recibo, salvo tipo 46) también por proveedor.

Al **enviar** un documento de una compañía de Chile (país `Chile` o código `CL`):

- Tipo SII y folio > 0 son obligatorios.
- Las NC deben indicar el documento de origen (*Return Against*).

## Migración desde el Select anterior

Si ya existía el campo `sii_doctype` como Select, se convierte a Link y se mapean los valores:

| Etiqueta anterior | Código |
| --- | --- |
| Factura Afecta | 33 |
| Factura Exenta | 34 |
| Boleta Afecta | 39 |
| Boleta Exenta | 41 |
| Factura de Compra | 46 |
| Nota de Débito | 56 |
| Nota de Crédito | 61 |
| Comprobantes Pago Electrónico | 39 |

En Sales Invoice, el custom field `bill_no` pasa a `sii_folio`. El `bill_no` nativo de Purchase Invoice (n.º de factura del proveedor) no se toca.

## Tests

```bash
bench --site $SITE set-config allow_tests true
bench --site $SITE run-tests --app sii_doctype
```

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/sii_doctype
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## License

mit
