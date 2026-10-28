# Project: Star Union S.R.L. — Visual Polish, Art Direction & Brand Verification

## Architecture
- **Tech Stack**: Static multi-page corporate website (HTML5, Tailwind CSS via CDN runtime config, Vanilla JavaScript modules).
- **Public Surface (10 Pages + Dossier)**:
  1. `index.html` (Home / Portada)
  2. `la-empresa/index.html` (Infraestructura Guaminí 800 m², taller electromecánico, flota, historia)
  3. `certificacion-iso/index.html` (ISO 9001:2015 TÜV Rheinland, certificado descargable, auditorías)
  4. `limpieza-industrial/index.html` (Plantas, industrias, centros logísticos)
  5. `limpieza-en-altura/index.html` (Silletas, balancines, hidrolavado, normas ARAA)
  6. `grandes-superficies/index.html` (Centros comerciales, hipermercados, áreas públicas)
  7. `consorcios/index.html` (Torres corporativas, oficinas, amenities)
  8. `clinicas-y-hospitales/index.html` (Áreas críticas, bioseguridad, quirófanos)
  9. `universidades-y-clubes/index.html` (Colegios, campus universitarios, clubes)
  10. `servicios-especiales/index.html` (Final de obra, desinfección, espacios verdes)
  11. `dossier/index.html` (Dossier interactivo de servicios y diferenciales)
- **Shared Assets & Scripts**:
  - `assets/js/starunion-b2b.js`: Micro-filtro modal de WhatsApp (B2B Lead vs RRHH) y despacho de eventos GA4 (Modal unificado en Open Sans).
  - `assets/img/`, `brochures/img/`: Activos visuales locales, logos e infraestructura.
  - `logo-footer-blanco.png`: Logo institucional para footer oficial.
- **Brand Lockfile & Governance**:
  - `BRAND_AND_CONNECTORS.lock.json`: Paleta permitida, conectores aislados, términos prohibidos.
  - `GEMINI.md`: Regla local de hierro para Star Union B2B.
  - `MEMORIA_VIVA_ACUERDOS_STAR_UNION.md`: Memoria viva de acuerdos comerciales y operacionales.
  - `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip`: Paquete limpio distribuible para producción.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Typography Unification in `<head>` & `<style>` | Universal Google Fonts links with preconnects (Open Sans 300..800), standard base body font-size 1rem (16px), line-height 1.6, clean bg-white across all 11 HTML pages, elimination of Inter and Plus Jakarta Sans | M1 | Survey Typography §4.1 (DONE) |
| F2 | Typography Unification in `tailwind.config` | Standardize inline `tailwind.config` across all 11 files with `Open Sans` for `sans`, `heading`, and `display` | M1 | Survey Typography §4.2 (DONE) |
| F3 | Editorial Heading Hierarchy Standard | Align H1, H2, H3, H4, lead and paragraph classes for consistent typographic rhythm across the site | M1 | Survey Typography §4.4 (DONE) |
| F4 | Hero Section B2B Art Direction Polish | Refactor Home (`index.html`) Hero from full-green background (`bg-brand`) and yellow button to pure white (`bg-white`) / pearl gray (`#f9fafb`), dark H1 (`#000000`), institutional green primary CTA (`bg-brand hover:bg-brand-dark text-white rounded-lg`), white secondary CTA with border, and micro yellow star | M2 | Survey Art Direction §1.2 & §4.2 |
| F5 | Footer Official Unification (No Brazil Effect) | Eliminate Brazil-flag contrast on dark green `#133522` / `#0e2719` across all 10 public pages: replace yellow button with white corporate button (`bg-white hover:bg-gray-100 text-brand rounded-lg shadow-sm`), replace yellow text/labels with white/pearl, replace link hover from yellow to white, clean duplicate comments | M2 | Survey Art Direction §1.2 & §4.1 |
| F6 | Palette & Color Cleanup | Replace red alert classes in `index.html:200` with subtle corporate neutral gray; convert yellow badges in `index.html:379` and `certificacion-iso:245` to `bg-brand/10 text-brand border-brand/20`; fix out-of-palette hexes (`#057a3f`, `#023d1f`, `#e6b822`) in `la-empresa`, `limpieza-en-altura`, and `dossier` | M2 | Survey Art Direction §1.1 & §4.2 |
| F7 | WhatsApp B2B Filter & Conector Expansion | Inject `assets/js/starunion-b2b.js` into 4 missing pages (`la-empresa`, `certificacion-iso`, `limpieza-en-altura`, `dossier`); modal font in Open Sans verified; fix ISO contact form fields with `name=` attributes and submit handler; replace external Wikimedia TÜV image with local verified asset | M3 | Survey Brand/Packaging §1.3 & Art Direction §1.6 |
| F8 | Brand Safety, Term & Lockfile Alignment | Fix `"casco con barbijo"` in `limpieza-en-altura:244` to `"casco con barbiquejo homologado"`; verify 0 occurrences of gendered greetings or leaked internal links; harmonize `BRAND_AND_CONNECTORS.lock.json` with nested structure while keeping legacy keys | M3 | Survey Brand/Packaging §1.2 & §1.7 |
| F9 | Clean HostGator ZIP Packaging | Regenerate `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` with clean reproducible exclusion of `.agents*`, `.git*`, `*.md`, `*.json`, and private management directories; verify Linktree `/accesos/` | M3 | Survey Brand/Packaging §1.6 |
| F10 | Comprehensive E2E Verification & Forensic Audit | Run programmatic test suite validating typography (11/11 Open Sans, 0 Inter/Jakarta, 0 18px body), color compliance (0 forbidden classes, 0 Brazil effect), brand firewall validation, and zip integrity | M4 | All Surveys §5 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Typography Unification (R1) | F1, F2, F3: Open Sans 100% across 10 public pages + dossier, base 1rem (16px), tailwind.config standardization, heading hierarchy, modal font fix | none | DONE |
| M2 | Art Direction & Palette Refinement (R2) | F4, F5, F6: Hero B2B white redesign, Footer unificado sin efecto Brasil, palette hex cleanup, badge refinement | M1 | DONE |
| M3 | Brand Locks, Components & Distribution (R3) | F7, F8, F9: WhatsApp filter script expansion, barbiquejo term fix, lockfile harmonization, clean ZIP generation | M2 | PLANNED |
| M4 | Final E2E Test Suite & Forensic Integrity Audit | F10: Programmatic verification suite, 100% pass across typography, colors, brand locks, and forensic integrity audit | M3 | PLANNED |

## Code Layout
- `index.html`: Home page (Hero, 7 verticals, operational differentials, lead form, footer).
- `la-empresa/index.html`: Infrastructure & Guaminí page.
- `certificacion-iso/index.html`: Quality & TÜV Rheinland page.
- `limpieza-industrial/index.html`: Industry vertical page.
- `limpieza-en-altura/index.html`: Height cleaning vertical page.
- `grandes-superficies/index.html`: Commercial centers vertical page.
- `consorcios/index.html`: Towers & corporate buildings page.
- `clinicas-y-hospitales/index.html`: Healthcare facilities page.
- `universidades-y-clubes/index.html`: Education & clubs page.
- `servicios-especiales/index.html`: Specialized services page.
- `dossier/index.html`: Executive presentation dossier.
- `assets/js/starunion-b2b.js`: WhatsApp modal & GA4 event dispatcher.
- `BRAND_AND_CONNECTORS.lock.json`: Project lockfile.
- `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip`: Distribution package.
