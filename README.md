# Sii Doctype

Catálogo de tipos de documentos electrónicos (DTE) del [SII de Chile](https://www.sii.cl/) para ERPNext v16.

La app registra los códigos oficiales DTE, la Boleta de Honorarios Electrónica (BHE) y los **tipos de referencia** del DTE (801 Orden de Compra, 802 Nota de Pedido, 803 Contrato, etc.). Los enlaza a facturas y guías de ERPNext y valida folio, tipo, referencias y notas de crédito/débito. **No emite XML, CAF ni Track ID**: eso corresponde a una app de facturación electrónica.

Requiere **ERPNext**. Compatible con Frappe/ERPNext version-16.

## Instalación

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench --site $SITE install-app sii_doctype
```

Al instalar (y en cada `bench migrate`) la app:

1. Crea o actualiza **SII Document Type** (13 tipos) y **SII Reference Type** (801-815, HES, SET y los DTE como referencia).
2. Agrega la sección **SII Chile** (tipo, folio y tabla de referencias) en Sales Invoice, Purchase Invoice, Delivery Note y Purchase Receipt.
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
| Referencias SII | Tabla `TpoDocRef` / `FolioRef` / `FchRef` / `CodRef` (801, 802, 803, otro DTE, etc.). |

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
| 48 | Boleta de Honorarios Electrónica | | Sí (recibida) | | | Honorarios; no es boleta 39/41 |
| 52 | Guía de Despacho Electrónica | | | Sí | Sí | |
| 56 | Nota de Débito Electrónica | Sí | Sí | | | |
| 61 | Nota de Crédito Electrónica | Sí | Sí | | | |
| 110 | Factura de Exportación Electrónica | Sí | | | | Exportación |
| 111 | Nota de Débito de Exportación Electrónica | Sí | | | | Exportación |
| 112 | Nota de Crédito de Exportación Electrónica | Sí | | | | Exportación |

Puedes deshabilitar un tipo en el maestro; no se podrá usar en transacciones.

## Referencias SII (801, 802, 803, …)

En el DTE el nodo `Referencia` apunta a otro documento (`TpoDocRef`). No es el tipo de **este** documento (33, 61, 48…); es a qué se **refiere**.

El maestro **SII Reference Type** incluye:

| Código | Nombre | Uso típico |
| --- | --- | --- |
| 801 | Orden de Compra | OC del cliente |
| 802 | Nota de Pedido | Pedido interno o del cliente |
| 803 | Contrato | Contrato o convenio |
| 804 | Resolución | Resolución administrativa |
| 805 | Proceso ChileCompra | Licitación |
| 806 | Ficha ChileCompra | Ficha del proceso |
| 807 | DUS | Exportación |
| 808 | B/L | Conocimiento de embarque |
| 809 | AWB | Guía aérea |
| 810 | MIC/DTA | Transporte internacional |
| 811 | Carta de Porte | Transporte |
| 812 | Resolución SNA | Servicios de exportación |
| 813 | Pasaporte | Identificación en algunos casos |
| 814 | Certificado de Depósito Bolsa Prod. Chile | |
| 815 | Vale de Prenda Bolsa Prod. Chile | |
| HES | Hoja de Entrada de Servicios | ChileCompra |
| SET | Set de Pruebas | Certificación SII |

También se cargan los DTE (33, 52, 61, etc.) como referencias, para anular o corregir otro documento tributario.

En la factura, en **Referencias SII**, agrega filas:

1. Tipo de referencia (p. ej. 801).
2. Folio / n.º (puede ser alfanumérico, p. ej. `OC-2026-15`). Obligatorio salvo *Referencia global*.
3. Fecha de la referencia.
4. Código 1 (anula), 2 (corrige texto) o 3 (corrige montos), si aplica — sobre todo en NC/ND.
5. Razón, opcional.

Puedes tener varias referencias en el mismo DTE.

## Validaciones

Si se indica tipo o folio (en borrador o al guardar):

- El tipo debe existir, estar habilitado y aplicar al DocType.
- El folio no puede ser negativo.
- Guía 52 no se usa en facturas.
- NC (61, 112) exige documento de devolución (`is_return`).
- ND de venta (56, 111) exige *Is Debit Note*.
- Una devolución de factura no puede usar un tipo que no sea NC.
- Tipos exentos (34, 41) no admiten impuestos gravados de IVA. El tipo 48 (honorarios) sí permite retención.
- El folio es único por compañía + tipo. En documentos recibidos (compra o recibo, salvo tipo 46) también por proveedor.
- Cada referencia SII debe tener tipo y folio (o marcarse como global). El `CodRef`, si existe, es 1, 2 o 3.

Al **enviar** un documento de una compañía de Chile (país `Chile` o código `CL`):

- Tipo SII y folio > 0 son obligatorios.
- Las NC deben indicar el documento de origen (*Return Against*).

## Boletas de Honorarios Electrónicas (tipo 48)

Las BHE **no son DTE** (no uses 39 ni 41). Un profesional te las emite en el SII; tú las registras como **compra recibida**.

1. Crea al emisor como **Proveedor** (RUT del profesional).
2. Crea una **Factura de Compra** (Purchase Invoice).
3. En **SII Chile**: tipo `48 - Boleta de Honorarios Electrónica` y el **folio** de la BHE.
4. En **Supplier Invoice No** (`bill_no`) puedes repetir el folio o la referencia del SII.
5. El ítem debe ser un servicio (no inventario). El monto es el **bruto** de la boleta.
6. La retención de honorarios no va como IVA: usa **Tax Withholding** de ERPNext (o una cuenta de retención en el asiento). No marques IVA en impuestos.

El folio es único por compañía + proveedor + tipo 48. No uses este tipo en Factura de Venta: la empresa no emite BHE por este catálogo.

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
