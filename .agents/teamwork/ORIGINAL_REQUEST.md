# Original User Request

## 2026-10-28T14:10:22Z

Requested team: Dirección de Arte, Diseño UX/UI Corporativo B2B y Verificación de Marca Star Union

Unificar el sistema tipográfico y pulir la Dirección de Arte y los detalles estéticos de las 10 páginas públicas del sitio web de Star Union S.R.L. (`https://wajntraub.ar/staruniontest/`) y su Dossier Comercial (`/dossier/`) para transmitir la categoría corporativa e industrial impecable de la empresa de Mauro Repetto (blanco dominante `#ffffff`, aire visual generoso, sobriedad ejecutiva B2B, cero colores ajenos a la marca y sin saturación verde+amarillo tipo "bandera de Brasil").

Working directory: /Users/arianawajntraub/Documents/antigravity/star-union
Integrity mode: development

## Requirements

### R1. Unificación Tipográfica Absoluta en las 10 Páginas Públicas y el Dossier
Unificar el 100% de las páginas públicas (`index.html`, `la-empresa/index.html`, `certificacion-iso/index.html`, `limpieza-industrial/index.html`, `limpieza-en-altura/index.html`, `grandes-superficies/index.html`, `consorcios/index.html`, `clinicas-y-hospitales/index.html`, `universidades-y-clubes/index.html`, `servicios-especiales/index.html`) y `dossier/index.html` bajo una única familia tipográfica y escala editorial coherente (`Open Sans` como base oficial del sitio), eliminando el salto actual donde la Home e ISO usan `Open Sans` a `18px` (`1.125rem`) mientras las páginas internas mezclan `Inter` + `Plus Jakarta Sans` a `16px`. Ajustar pesos, interlineados (`line-height`), jerarquías de títulos (`H1`, `H2`, `H3`), subtítulos y cuerpo de texto (`1rem` / `16px` limpio y proporcionado) para que navegar entre la Home y cualquier vertical se sienta un único sitio corporativo de primer nivel.

### R2. Dirección de Arte Corporativa B2B (Blanco Dominante, Aire Visual y Cero "Efecto Bandera de Brasil")
Pulir los detalles estéticos de la Home (`index.html`) y de las páginas interiores respetando estrictamente la paleta oficial de Star Union:
- **80-85% Blanco Puro (`#ffffff`) y Gris Perla muy sutil (`#f9fafb`)** con amplios márgenes, respiro visual entre secciones y bordes finos (`#e5e7eb`).
- **12-15% Verde Institucional (`#03582d` y `#133522` solo en el footer)** para botones primarios, acentos sobrios y navegación activa.
- **Máximo 3-5% Amarillo Estrella (`#ffcc29`)** exclusivamente como micro-detalle puntual (un punto, un filete fino o la estrella del logo), prohibiendo bloques grandes amarillos pegados a bloques verdes que generen efecto visual "bandera de Brasil" o "kermés".
- **Cero colores fuera de marca:** eliminar cualquier rastro de clases Tailwind `blue-*`, `indigo-*`, `sky-*`, `orange-*` o `amber-*` estridentes en el sitio público.

### R3. Pulido de Componentes Visuales, Tarjetas, Fotografías y Consistencia de Cabecera/Pie
Refinar en la Home y páginas interiores la presentación visual de:
- Tarjetas de las 7 verticales, diferenciales operativos (Base Propia Guaminí 800 m², Reloj Biométrico 15 min, Flota Propia Ford Transit, Certificación ISO 9001 TÜV Rheinland) y grillas de fotos reales para que tengan proporciones armónicas, sombras suaves y textos legibles sin bloques apelmazados.
- Mantener intactos los candados de marca de Star Union (`BRAND_AND_CONNECTORS.lock.json`): lenguaje neutro corporativo sin marca de género (prohibido "Bienvenidos/as/es"), cero barbijos/COVID, logo blanco real en el footer (`logo-footer-blanco.png`), micro-filtro de WhatsApp B2B vs. RRHH (`assets/js/starunion-b2b.js`) y actualización automática del paquete limpio `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` y del Linktree Central (`/accesos/index.html`).

## Acceptance Criteria

### Verificación Programática y de Marca
- [ ] **Unificación Tipográfica 10/10:** Las 10 páginas públicas y `dossier/index.html` cargan exactamente la misma fuente (`Open Sans`) en `<head>`, la misma configuración en `tailwind.config` y el mismo tamaño base de `body` sin mezclar `Open Sans` con `Plus Jakarta Sans`/`Inter`.
- [ ] **Cero Colores Ajenos o Efecto Brasil:** Un escaneo sobre las 10 páginas públicas confirma `0` clases `blue-`, `indigo-`, `sky-`, `orange-`, `cyan-` o `purple-`, y el color `#ffcc29` se usa únicamente en micro-acentos puntuales sobre fondo blanco o en el logo oficial.
- [ ] **Candado de Marca Star Union:** El validador `brand_firewall.py` y un chequeo de integridad confirman `0` apariciones de `"LOGO BLANCO"`, `0` links públicos a herramientas internas (`radar-comercial`, `brochures/editables`, `relevamiento-gerencia`, `acuerdos`), y que `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` queda regenerado con las páginas pulidas.
