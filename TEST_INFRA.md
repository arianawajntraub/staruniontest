# TEST INFRASTRUCTURE SPECIFICATION: STAR UNION S.R.L.
**Documento Maestro de Arquitectura y Especificación de Pruebas E2E (Dual Track)**
**Versión:** 1.0.0 · **Fecha:** 2026-10-28 · **Estado:** ACTIVO
**Proyecto:** `4 - STAR UNION (Limpieza B2B)` · **Dominio:** `www.starunion.com.ar`

---

## 1. Test Philosophy: Opaque-Box & Requirement-Driven

El sistema de pruebas E2E de Star Union S.R.L. implementa una filosofía de **caja opaca (opaque-box testing)** estrictamente guiada por especificaciones y requerimientos:
1. **Independencia de Implementación:** Las pruebas inspeccionan el comportamiento observable, la estructura del DOM renderizable, la presencia de activos, la coherencia cromática y las reglas de marca desde la perspectiva del cliente corporativo y los estándares de auditoría B2B de Mauro Repetto.
2. **Fuente de Verdad Autoritativa:** Cada aserción se deriva directamente de:
   - `ORIGINAL_REQUEST.md` (Requerimientos R1, R2, R3).
   - `PROJECT.md` (§ Feature Inventory F1–F10, Milestones M1–M4).
   - `BRAND_AND_CONNECTORS.lock.json` (Paleta permitida, conectores aislados, términos prohibidos).
   - `GEMINI.md` (Regla local de hierro para Star Union B2B).
   - Informes de relevamiento de los agentes Explorer (`explorer_survey_typography`, `explorer_survey_art_direction`, `explorer_survey_brand_packaging`).
3. **No Intrusión:** El código de prueba reside en `tests/` y jamás altera archivos del sitio público ni herramientas de gestión.
4. **Verificabilidad Progresiva:** La suite clasifica los casos de prueba según los hitos de implementación (M1: Tipografía, M2: Dirección de Arte y Color, M3: Candados de Marca y Distribución, M4: Auditoría Forense Integral), permitiendo comprobar avances incrementales sin falsos bloqueos.

---

## 2. Feature Inventory (F1 to F10)

| ID | Característica / Módulo | Descripción Funcional | Hito |
| :--- | :--- | :--- | :---: |
| **F1** | Tipografía en `<head>` y `<style>` | Vínculos universales a Google Fonts con preconnects (Open Sans 300..800), cuerpo base `1rem` (16px), interlineado `1.6`, fondo `bg-white` en las 11 páginas HTML, eliminación de Inter y Plus Jakarta Sans. | M1 |
| **F2** | Tipografía en `tailwind.config` | Estandarización de `tailwind.config` inline en los 11 archivos con `Open Sans` para `sans`, `heading` y `display`. | M1 |
| **F3** | Jerarquía Editorial de Encabezados | Alineación armónica de H1, H2, H3, H4, bajadas (`lead`) y párrafos, color `#000000` para títulos y `#676b67` para textos de lectura. | M1 |
| **F4** | Hero B2B Blanco en Portada | Refactorización del Hero de `index.html` de fondo verde pleno a blanco puro / gris perla (`#ffffff` / `#f9fafb`), H1 negro, botón primario verde institucional y botón secundario blanco con borde gris. | M2 |
| **F5** | Footer Oficial sin Efecto Brasil | Erradicación del contraste amarillo estridente sobre fondo verde oscuro (`#133522` / `#0e2719`) en las 10 páginas públicas: botón blanco corporativo, textos y enlaces en blanco perla, sin comentarios HTML duplicados. | M2 |
| **F6** | Limpieza Cromática y de Paleta | Reemplazo de alerta roja en `index.html:200` por gris institucional; conversión de badges amarillos en `index.html:379` y `certificacion-iso:245` a verde sutil; corrección de hexadecimales fuera de paleta (`#057a3f`, `#023d1f`, `#e6b822`); 0 clases Tailwind prohibidas. | M2 |
| **F7** | Filtro WhatsApp B2B y Conectores | Inyección de `assets/js/starunion-b2b.js` en las 4 páginas faltantes (`la-empresa`, `certificacion-iso`, `limpieza-en-altura`, `dossier`); modal con fuente Open Sans; formulario de cotización ISO con atributos `name=` y submit handler; reemplazo de imagen externa de TÜV por activo local. | M3 |
| **F8** | Seguridad de Marca y Alineación de Candados | Corrección de "casco con barbijo" a "casco con barbiquejo homologado" en `limpieza-en-altura:244`; 0 términos prohibidos o saludos con género; armonización de `BRAND_AND_CONNECTORS.lock.json` con estructura anidada; 0 fugas de herramientas internas; logo blanco verificado en 11/11 páginas. | M3 |
| **F9** | Empaquetado Limpio para HostGator | Generación reproducible de `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` con exclusión de `.agents*`, `.git*`, `*.md`, `*.json` y módulos de gestión; verificación de Linktree privado `/accesos/`. | M3 |
| **F10**| Auditoría Forense y Verificación E2E | Verificación integral automatizada de activos locales (100 imágenes), navegación entre 7 verticales, 4 diferenciales operativos y ejecución del cortafuegos de marca. | M4 |

---

## 3. Four-Tier Test Case Design (120 Casos de Prueba)

El diseño de la suite se estructura en cuatro niveles rigurosos:

```
┌────────────────────────────────────────────────────────────────────────┐
│                TIER 4: Escenarios B2B Reales y Forenses (12)           │
├────────────────────────────────────────────────────────────────────────┤
│          TIER 3: Integración Cruzada y Combinaciones Pairwise (18)      │
├────────────────────────────────────────────────────────────────────────┤
│             TIER 2: Casos de Borde, Límites y Resiliencia (40)         │
├────────────────────────────────────────────────────────────────────────┤
│              TIER 1: Cobertura Funcional F1 a F10 (50 Casos)           │
└────────────────────────────────────────────────────────────────────────┘
```

---

### TIER 1: Cobertura Funcional Directa (50 Casos de Prueba, 5 por Característica)

#### F1: Tipografía en `<head>` y `<style>`
- `test_t1_f1_01_preconnect_google_fonts`: Valida que las 11 páginas incluyan `<link rel="preconnect" href="https://fonts.googleapis.com">` y `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`.
- `test_t1_f1_02_open_sans_font_link`: Valida que las 11 páginas carguen la hoja de estilos de Google Fonts con la familia `Open+Sans` en pesos 300..800.
- `test_t1_f1_03_eradication_of_inter_in_head`: Valida 0 referencias a `family=Inter` en `<head>` en las 11 páginas.
- `test_t1_f1_04_eradication_of_jakarta_in_head`: Valida 0 referencias a `family=Plus+Jakarta+Sans` en `<head>` en las 11 páginas.
- `test_t1_f1_05_body_base_font_size_1rem`: Valida que la regla `<style>` de `body` declare `font-size: 1rem` (o herencia base sin forzar `1.125rem`) y `line-height: 1.6`.

#### F2: Tipografía en `tailwind.config`
- `test_t1_f2_01_tailwind_config_sans_open_sans`: Valida que `tailwind.config` declare `sans: ['"Open Sans"', 'sans-serif']` en las 11 páginas.
- `test_t1_f2_02_tailwind_config_heading_open_sans`: Valida que `tailwind.config` declare `heading: ['"Open Sans"', 'sans-serif']` en las 11 páginas.
- `test_t1_f2_03_tailwind_config_display_open_sans`: Valida que `tailwind.config` declare `display: ['"Open Sans"', 'sans-serif']` como alias compatible en las 11 páginas.
- `test_t1_f2_04_tailwind_config_palette_structure`: Valida que `tailwind.config` contenga los objetos `colors.brand`, `colors.accent` y `colors.neutral`.
- `test_t1_f2_05_tailwind_config_no_foreign_fonts`: Valida que `tailwind.config` no defina `Inter` ni `Plus Jakarta Sans` en ninguna de las 11 páginas.

#### F3: Jerarquía Editorial de Encabezados
- `test_t1_f3_01_headings_color_pure_black`: Valida que la regla de encabezados `h1, h2, h3, h4` en `<style>` asigne `color: #000000` en las 11 páginas.
- `test_t1_f3_02_body_text_color_neutral`: Valida que la regla de `body` en `<style>` asigne `color: #676b67` en las 11 páginas.
- `test_t1_f3_03_inner_pages_h1_scale`: Valida que los títulos `H1` en páginas interiores utilicen escala consistente (`font-extrabold` y escala tipográfica armónica).
- `test_t1_f3_04_no_inline_style_font_overrides`: Valida que ningún elemento del cuerpo contenga atributos `style="font-family: ..."` que sobreescriban Open Sans.
- `test_t1_f3_05_body_background_pure_white`: Valida que el fondo base de `body` sea `#ffffff` (`bg-white`) en las 10 páginas públicas e ISO.

#### F4: Hero B2B Blanco en Portada (`index.html`)
- `test_t1_f4_01_home_hero_not_full_green`: Valida que la sección Hero de `index.html` no contenga la clase `bg-brand` en su contenedor de primer pliegue.
- `test_t1_f4_02_home_hero_dark_h1`: Valida que el título H1 del Hero de `index.html` sea de color oscuro (`text-[#000000]` o similar) y no blanco sobre verde.
- `test_t1_f4_03_home_hero_primary_cta_green`: Valida que el botón CTA principal del Hero de `index.html` sea verde institucional (`bg-brand hover:bg-brand-dark text-white`).
- `test_t1_f4_04_home_hero_secondary_cta_white`: Valida que el CTA secundario del Hero sea blanco corporativo con borde sutil (`bg-white text-brand border border-gray-200`).
- `test_t1_f4_05_home_hero_micro_accent_star`: Valida que el badge superior del Hero contenga la estrella amarilla `text-accent` como micro-detalle puntual (≤ 16px).

#### F5: Footer Oficial sin Efecto Brasil
- `test_t1_f5_01_footer_no_yellow_button`: Valida que en las 10 páginas públicas el botón del footer no use clases amarillas (`bg-[#ffcc29]`, `bg-accent`).
- `test_t1_f5_02_footer_corporate_white_button`: Valida que el botón de solicitud del footer use estilo corporativo blanco (`bg-white text-brand`).
- `test_t1_f5_03_footer_no_yellow_labels`: Valida que las etiquetas de contacto en el footer no contengan `text-[#ffcc29]`.
- `test_t1_f5_04_footer_links_hover_white`: Valida que los enlaces de verticales en el footer no usen `hover:text-[#ffcc29]`.
- `test_t1_f5_05_footer_no_duplicate_comments`: Valida que no existan comentarios duplicados consecutivos `<!-- FOOTER OFICIAL UNIFICADO... -->`.

#### F6: Limpieza Cromática y de Paleta
- `test_t1_f6_01_zero_forbidden_blue_classes`: Valida 0 apariciones de clases `blue-*`, `indigo-*`, `sky-*` en las 11 páginas.
- `test_t1_f6_02_zero_forbidden_orange_classes`: Valida 0 apariciones de clases `orange-*`, `amber-*` en las 11 páginas.
- `test_t1_f6_03_zero_forbidden_cyan_purple_classes`: Valida 0 apariciones de clases `cyan-*`, `purple-*` en las 11 páginas.
- `test_t1_f6_04_home_red_warning_eliminated`: Valida que `index.html:200` no contenga clases `bg-red-*`, `border-red-*`, `text-red-*`.
- `test_t1_f6_05_out_of_palette_hex_cleanup`: Valida 0 apariciones de `#057a3f`, `#023d1f` y `#e6b822` en los archivos HTML.

#### F7: Filtro WhatsApp B2B y Conectores
- `test_t1_f7_01_starunion_b2b_js_in_11_pages`: Valida que las 11 páginas incluyan la etiqueta `<script src="...assets/js/starunion-b2b.js">`.
- `test_t1_f7_02_b2b_modal_font_open_sans`: Valida que `assets/js/starunion-b2b.js` use `Open Sans` en su estilo inyectado y no `Inter`.
- `test_t1_f7_03_iso_form_name_attributes`: Valida que el formulario de contacto en `certificacion-iso/index.html` incluya atributos `name=` en sus campos.
- `test_t1_f7_04_iso_form_b2b_class`: Valida que el formulario en `certificacion-iso/index.html` tenga la clase `js-b2b-quote-form`.
- `test_t1_f7_05_iso_page_local_tuv_image`: Valida que `certificacion-iso/index.html` no cargue imágenes de Wikimedia y utilice el activo local verificado.

#### F8: Seguridad de Marca y Alineación de Candados
- `test_t1_f8_01_altura_barbiquejo_correction`: Valida que `limpieza-en-altura/index.html` mencione `"barbiquejo"` y 0 veces `"barbijo"`.
- `test_t1_f8_02_zero_gendered_greetings`: Valida 0 apariciones de `"Bienvenidos a Star Union"`, `"bienvenides"`, `"todes"`, `"bienvenidos/as"`.
- `test_t1_f8_03_zero_leaks_of_internal_tools`: Valida que ninguna de las 11 páginas enlace a `radar-comercial`, `brochures/editables`, `relevamiento-gerencia` ni `acuerdos/index`.
- `test_t1_f8_04_footer_logo_reference_11_pages`: Valida que las 11 páginas referencien `logo-footer-blanco.png`.
- `test_t1_f8_05_zero_visible_logo_blanco_text`: Valida 0 apariciones del texto visible `"LOGO BLANCO"` en el DOM renderizable.

#### F9: Empaquetado Limpio para HostGator
- `test_t1_f9_01_zip_file_exists`: Valida que `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` exista físicamente en el directorio raíz del proyecto.
- `test_t1_f9_02_zip_excludes_agents_directory`: Valida que el ZIP no contenga entradas que comiencen con `.agents`.
- `test_t1_f9_03_zip_excludes_markdown_docs`: Valida que el ZIP no contenga archivos `.md` de documentación interna.
- `test_t1_f9_04_zip_excludes_internal_tools`: Valida que el ZIP no contenga `radar-comercial/`, `acuerdos/`, `relevamiento-gerencia/` ni `brochures/editables/`.
- `test_t1_f9_05_accesos_linktree_noindex`: Valida que `/accesos/index.html` contenga `<meta name="robots" content="noindex, nofollow">`.

#### F10: Auditoría Forense y Verificación E2E
- `test_t1_f10_01_all_100_local_images_exist`: Valida que las 100 rutas locales de imágenes `<img src="...">` existan en disco sin enlaces rotos.
- `test_t1_f10_02_all_7_verticals_linked`: Valida que `index.html` enlace a las 7 páginas de verticales (`limpieza-industrial`, `limpieza-en-altura`, `grandes-superficies`, `consorcios`, `clinicas-y-hospitales`, `universidades-y-clubes`, `servicios-especiales`).
- `test_t1_f10_03_operational_differentials_present`: Valida la presencia de los 4 diferenciales clave (Guaminí 800 m², Reloj Biométrico 15 min, Flota Ford Transit, ISO 9001).
- `test_t1_f10_04_iso_official_data_accuracy`: Valida la presencia del N° de Certificado `01 10006 2529826` y Certipedia ID `9000041847`.
- `test_t1_f10_05_brand_lockfile_integrity`: Valida que `BRAND_AND_CONNECTORS.lock.json` contenga la paleta permitida, conectores de Star Union y términos prohibidos.

---

### TIER 2: Casos de Borde, Límites y Resiliencia (40 Casos de Prueba)

- `test_t2_b01_font_link_query_format`: Valida la sintaxis del URL de Google Fonts con parámetros ordenados `family=Open+Sans:ital,wght@...` y `display=swap`.
- `test_t2_b02_preconnect_cors_attribute`: Valida que `preconnect` a `gstatic.com` tenga el atributo `crossorigin`.
- `test_t2_b03_no_insecure_http_font_links`: Valida que no existan enlaces a fuentes con protocolo inseguro `http://`.
- `test_t2_b04_style_tag_css_syntax`: Valida que las reglas CSS en `<style>` no tengan llaves desbalanceadas.
- `test_t2_b05_tailwind_config_json_parseable`: Valida que el objeto de extensión en `tailwind.config` contenga sintaxis JavaScript válida.
- `test_t2_b06_tailwind_no_duplicate_font_keys`: Valida que `fontFamily` no contenga claves duplicadas en la configuración.
- `test_t2_b07_tailwind_cdn_script_present`: Valida que el script de Tailwind CDN preceda la configuración inline en el `<head>`.
- `test_t2_b08_headings_inheritance_in_cards`: Valida que encabezados H3 y H4 dentro de grillas y tarjetas mantengan color negro `#000000`.
- `test_t2_b09_responsive_h1_classes_mobile`: Valida que las clases de H1 contemplen breakpoints móviles (`sm:`, `lg:`) para evitar desbordes en 320px.
- `test_t2_b10_microcopy_minimum_size`: Valida que badges y etiquetas de pie no bajen de `text-xs` (12px) garantizando legibilidad.
- `test_t2_b11_line_height_proportions`: Valida que los párrafos de cuerpo usen `leading-relaxed` (1.6) o `leading-normal` sin compresión visual.
- `test_t2_b12_hero_badge_contrast_ratio`: Valida que el badge de certificación del Hero ofrezca contraste legible contra fondo claro.
- `test_t2_b13_hero_primary_button_contrast`: Valida que el texto blanco sobre `bg-brand` (#03582d) supere la relación de contraste WCAG AA (≥ 4.5:1).
- `test_t2_b14_hero_secondary_button_border`: Valida que el botón secundario incluya clase de borde (`border`) para contraste sobre blanco.
- `test_t2_b15_hero_accent_star_inline_flex`: Valida que la estrella amarilla no altere la alineación vertical del badge (`inline-flex items-center`).
- `test_t2_b16_footer_white_button_hover_contrast`: Valida que el botón blanco del footer declare estado hover distinguible (`hover:bg-gray-100`).
- `test_t2_b17_footer_phone_uri_schemes`: Valida que los enlaces telefónicos usen el esquema `tel:` con números válidos.
- `test_t2_b18_footer_email_uri_scheme`: Valida que el enlace de correo use `mailto:comercial@starunion.com.ar`.
- `test_t2_b19_footer_address_postal_code`: Valida que la dirección en el pie mencione el código postal de CABA.
- `test_t2_b20_footer_logo_dimensions`: Valida que la imagen del logo en el pie incluya clases de contención dimensional (`h-12 w-auto object-contain`).
- `test_t2_b21_hex_case_insensitivity_matching`: Valida que las comparaciones de color hexadecimal no fallen por diferencias de mayúsculas/minúsculas.
- `test_t2_b22_palette_opacity_modifiers`: Valida que las clases de opacidad (`bg-brand/10`, `border-brand/20`) deriven de colores oficiales.
- `test_t2_b23_zero_inline_style_rogue_hex`: Valida que ningún elemento contenga atributos `style="...#hex..."` con colores no autorizados.
- `test_t2_b24_whatsapp_modal_singleton_instance`: Valida que `starunion-b2b.js` verifique la existencia previa del modal antes de crearlo en el DOM.
- `test_t2_b25_whatsapp_e164_format`: Valida que el conector de WhatsApp en `BRAND_AND_CONNECTORS.lock.json` y los scripts use formato internacional `+5491122759369`.
- `test_t2_b26_ga4_dispatcher_safeguard`: Valida que `starunion-b2b.js` verifique `typeof gtag === 'function'` antes de emitir eventos de conversión.
- `test_t2_b27_b2b_form_required_fields`: Valida que los campos clave de cotización posean validación requerida.
- `test_t2_b28_forbidden_terms_word_boundaries`: Valida que la detección de términos prohibidos use límites de palabra (`\b`) para no generar falsos positivos con palabras válidas.
- `test_t2_b29_gender_neutrality_accents`: Valida que la expresión regular de género detecte variantes con tilde o caracteres especiales.
- `test_t2_b30_utf8_encoding_declaration`: Valida que las 11 páginas declaren `<meta charset="UTF-8">` en el bloque inicial de `<head>`.
- `test_t2_b31_viewport_meta_declaration`: Valida que las 11 páginas contengan la etiqueta meta de viewport responsive.
- `test_t2_b32_zip_file_readable_archive`: Valida que el archivo ZIP pueda ser abierto e inspeccionado por la biblioteca `zipfile` sin errores de compresión.
- `test_t2_b33_zip_no_root_path_traversal`: Valida que las rutas de los archivos dentro del ZIP sean relativas y seguras.
- `test_t2_b34_noindex_meta_tag_syntax`: Valida que la etiqueta `noindex` en `/accesos/index.html` tenga sintaxis estándar HTML5.
- `test_t2_b35_operational_address_consistency`: Valida que la mención de Guaminí use el número oficial `5657`.
- `test_t2_b36_transit_fleet_mention_neutral`: Valida que las menciones a unidades utilitarias Ford Transit no se declaren como exclusivas de final de obra.
- `test_t2_b37_biometric_alert_timing_15m`: Valida que se consigne el tiempo de alerta biométrica en 15 minutos.
- `test_t2_b38_biometric_replacement_timing_2h`: Valida que se consigne el tiempo máximo de relevo en menos de 2 horas.
- `test_t2_b39_certipedia_verification_link`: Valida que los enlaces a TÜV apunten al dominio oficial `www.certipedia.com`.
- `test_t2_b40_no_broken_internal_anchors`: Valida que los enlaces con ancla interna (ej. `#contacto`, `#donde-limpiamos`) correspondan a identificadores presentes en la página.

---

### TIER 3: Integración Cruzada y Combinaciones Pairwise (18 Casos de Prueba)

- `test_t3_c01_font_links_match_tailwind_config`: Valida que la fuente Open Sans solicitada en `<head>` coincida con la definida en `tailwind.config`.
- `test_t3_c02_body_size_cascades_to_lead`: Valida que la fijación de `1rem` en el body no fracture el tamaño visual de los párrafos introductorios.
- `test_t3_c03_modal_inherits_page_typography`: Valida que el modal de `starunion-b2b.js` adopte `Open Sans` alineándose con la tipografía de la página anfitriona.
- `test_t3_c04_tailwind_palette_matches_lockfile`: Valida que los colores de `tailwind.config` coincidan exactamente con `allowed_palette` de `BRAND_AND_CONNECTORS.lock.json`.
- `test_t3_c05_hero_cta_footer_cta_harmony`: Valida la coherencia de diseño entre el CTA principal del Hero y el CTA del Footer.
- `test_t3_c06_hero_white_ratio_overall`: Valida que la transformación del Hero a blanco eleve el porcentaje de blanco/gris perla de `index.html` al rango 80-85%.
- `test_t3_c07_footer_logo_matches_filesystem`: Valida que el archivo referenciado en el footer exista y tenga dimensiones no nulas en disco.
- `test_t3_c08_modal_buttons_color_harmony`: Valida que los botones del modal de WhatsApp respeten la paleta institucional de Star Union.
- `test_t3_c09_form_submit_ga4_event_wiring`: Valida que el envío de cotizaciones despache eventos de analítica bajo las claves autorizadas en el candado.
- `test_t3_c10_zip_package_excludes_lockfile_and_secrets`: Valida que el paquete de distribución no contenga credenciales ni archivos de candado.
- `test_t3_c11_zip_retains_all_11_pages`: Valida que el archivo ZIP contenga exactamente las 11 páginas del sitio público.
- `test_t3_c12_zip_retains_assets_directory`: Valida que el archivo ZIP incluya la estructura completa de `assets/img/` y `assets/js/`.
- `test_t3_c13_zip_contains_footer_logo`: Valida que `logo-footer-blanco.png` se encuentre incluido en la raíz del paquete ZIP.
- `test_t3_c14_zip_zero_forbidden_classes`: Valida que los archivos HTML contenidos en el ZIP no incluyan clases de color ajenas a la marca.
- `test_t3_c15_zip_contains_starunion_b2b_js`: Valida que `assets/js/starunion-b2b.js` forme parte del paquete distribuible.
- `test_t3_c16_h1_visual_scale_harmony`: Valida la concordancia entre los H1 de portada y los H1 de páginas interiores.
- `test_t3_c17_hero_copy_voseo_neutral`: Valida que los textos del Hero respeten el voseo corporativo sin marcas de género.
- `test_t3_c18_footer_hexes_match_lockfile`: Valida que los fondos de pie (`#133522` y `#024121`) figuren explícitamente en la paleta autorizada.

---

### TIER 4: Escenarios B2B Reales y Forenses (12 Casos de Prueba)

- `test_t4_s01_journey_industrial_manager`: Recorrido completo: Home $\rightarrow$ Vertical Industrial $\rightarrow$ Validación de ISO 9001 $\rightarrow$ Base Guaminí $\rightarrow$ Botón WhatsApp con modal de derivación B2B.
- `test_t4_s02_journey_corporate_tower_admin`: Recorrido: Vertical Consorcios y Oficinas $\rightarrow$ Reloj Biométrico (15 min / < 2 hs) $\rightarrow$ Atención telefónica 0810-333-8646.
- `test_t4_s03_journey_hospital_director`: Recorrido: Vertical Clínicas y Hospitales $\rightarrow$ Protocolos de bioseguridad $\rightarrow$ Ausencia total de alusiones a barbijos o estética pandemia.
- `test_t4_s04_journey_procurement_auditor`: Recorrido: Certificación ISO 9001 $\rightarrow$ Certificado PDF descargable $\rightarrow$ Validación Certipedia ID 9000041847 $\rightarrow$ Formulario técnico.
- `test_t4_s05_journey_height_cleaning_specialist`: Recorrido: Vertical Limpieza en Altura $\rightarrow$ Normas ARAA $\rightarrow$ Cuadrillas propias $\rightarrow$ Mención técnica "barbiquejo homologado".
- `test_t4_s06_journey_educational_campus`: Recorrido: Vertical Universidades y Clubes $\rightarrow$ Referencias institucionales $\rightarrow$ Tono corporativo de alta jerarquía.
- `test_t4_s07_journey_retail_center_manager`: Recorrido: Vertical Grandes Superficies $\rightarrow$ Alto tránsito $\rightarrow$ Protocolos de maquinaria LAV/LUT.
- `test_t4_s08_journey_specialized_services_client`: Recorrido: Servicios Especiales $\rightarrow$ Flota Ford Transit $\rightarrow$ Final de obra y divisiones técnicas.
- `test_t4_s09_journey_executive_investor_dossier`: Recorrido: Dossier Ejecutivo interactivo $\rightarrow$ Navegación por pestañas $\rightarrow$ Tipografía Open Sans unificada $\rightarrow$ Footer limpio sin amarillo.
- `test_t4_s10_forensic_crawler_zero_internal_leaks`: Escaneo tipo araña web forense que comprueba que ninguna página pública permita rastrear herramientas privadas de gerencia.
- `test_t4_s11_forensic_brand_firewall_validation`: Ejecución del motor del cortafuegos de marca (`brand_firewall.py`) asegurando 0 cruces de clientes o conectores ajenos.
- `test_t4_s12_forensic_zip_packaging_mirror`: Comparación forense entre el árbol público del repositorio y el contenido del archivo ZIP distribuible.

---

## 4. Matriz de Trazabilidad de Hitos (Progressive Testability)

| Hito | Alcance de Implementación | Pruebas Asociadas | Estado de Aprobación Esperado |
| :---: | :--- | :--- | :---: |
| **M1** | Tipografía Unificada (Open Sans 100%, 1rem base, tailwind.config) | F1 (5), F2 (5), F3 (5) + Casos T2/T3 tipográficos | **PASS** tras completar Milestone 1 |
| **M2** | Dirección de Arte y Color (Hero blanco, Footer sin Brasil, Limpieza Hex) | F4 (5), F5 (5), F6 (5) + Casos T2/T3 de color | **PASS** tras completar Milestone 2 |
| **M3** | Candados de Marca, Conectores y Empaquetado (WhatsApp, Barbiquejo, ZIP) | F7 (5), F8 (5), F9 (5) + Casos T2/T3/T4 de marca | **PASS** tras completar Milestone 3 |
| **M4** | Auditoría Forense y Verificación E2E Total | F10 (5) + Suite completa (120 pruebas) | **100% PASS** al cierre de M4 |

---

## 5. Instrucciones de Ejecución del Test Runner

El ejecutor oficial de pruebas proporciona salida coloreada por consola, desglose detallado por nivel y código de salida `0` al completar exitosamente:

```bash
# Ejecución estándar vía Python 3
python3 tests/run_tests.py

# O mediante script bash wrapper
bash tests/run_tests.sh

# Ejecución por nivel específico
python3 tests/run_tests.py --tier 1
python3 tests/run_tests.py --tier 2
python3 tests/run_tests.py --tier 3
python3 tests/run_tests.py --tier 4

# Ejecución por hito específico
python3 tests/run_tests.py --milestone M1
python3 tests/run_tests.py --milestone M2
python3 tests/run_tests.py --milestone M3
```
