# Survey Report: Brand Locks, Components & Packaging

**Agent:** Explorer Survey Brand & Packaging  
**Working Directory:** `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/explorer_survey_brand_packaging`  
**Date:** 2026-10-28T14:28:00Z  
**Type:** Hard Handoff (Investigation Complete)

---

## 1. Observation

### Obs 1.1: Presentation of 7 Verticals across `index.html` and Inner Pages
- **`index.html` lines 280–374**: Section `<section id="donde-limpiamos">` renders a 3-column grid containing 6 vertical cards:
  1. `limpieza-industrial/index.html` (line 297, badge: "ISO 9001 en Zona Productiva", image: `assets/img/vertical-industrial.png`)
  2. `consorcios/index.html` (line 310, badge: "Exclusivo Oficinas y Grandes Torres", image: `assets/img/vertical-corporativo.png`)
  3. `clinicas-y-hospitales/index.html` (line 323, badge: "Bioseguridad y Áreas Críticas", image: `https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d...`)
  4. `universidades-y-clubes/index.html` (line 336, badge: "UTDT · Lincoln · BDS · Club de Amigos", image: `assets/img/vertical-educacion.png`)
  5. `limpieza-en-altura/index.html` (line 349, badge: "Cuadrillas Propias · Normas ARAA", image: `assets/img/altura-curtain-wall-1.jpg`)
  6. `grandes-superficies/index.html` (line 362, badge: "Alto Tránsito Público y Comercial", image: `https://images.unsplash.com/photo-1519567241046-7f570eee3ce6...`)
- **`index.html` lines 390–457**: The 7th vertical (`servicios-especiales/index.html`) is presented in its own dedicated section `<section id="servicios-especiales">` ("Divisiones Técnicas y Servicios Especiales") with tabs for Altura, Obra, Jardinería, Plagas and direct link at line 404 (`href="servicios-especiales/index.html"`).
- **Navigation dropdown (`index.html` lines 116–137)**: Contains direct links to all 7 verticals.
- **Modular Hero Layout in Inner Pages**: The 6 industry vertical pages (`limpieza-industrial`, `grandes-superficies`, `consorcios`, `clinicas-y-hospitales`, `universidades-y-clubes`, `servicios-especiales`) share a unified 7-col/5-col hero layout:
  - Left: Title, badge, copy, 2 CTAs (`#contacto` and `../la-empresa/index.html`).
  - Right: Category hero image (from `brochures/img/`), secondary photo, and side box with `assets/img/tuv-iso-9001-qr.png` + `assets/img/cleany-hd.png`.
- **Photo Integrity**: A full regex scan of all `<img>` tags across all 11 pages (10 public + dossier) identified **100 local image tags**. Every single local image path resolves to an existing file on disk (**0 missing local images**).

### Obs 1.2: Presentation of 4 Operational Differentials
1. **Base Propia Guaminí 800 m²**:
   - `index.html` line 83: `📍 Base Operativa Central: Guaminí 5657, CABA (800 m²)`.
   - `index.html` lines 473, 517–611: Section detailing 800 m², taller electromecánico (desde 2010), arenado y pintura, aula práctica con 6 superficies de pisos (`assets/img/base-guamini-1.jpg`, `base-guamini-2.jpg`, `base-guamini-3.jpg`).
   - `la-empresa/index.html` lines 138–350: 8 individual detail cards covering all facets of Guaminí infrastructure.
   - `dossier/index.html` lines 169–245: 6 photographic cards of Guaminí.
   - *Address anomaly observed*: In `index.html` line 779, `footer.html` line 13, `universidades-y-clubes` lines 264 & 321, and `limpieza-industrial` lines 264 & 321, the address is written as `Guaminí 5052 / 5657 (C1439HAW), CABA (800 m²)`, whereas the top bar and `BRAND_AND_CONNECTORS.lock.json` state `Guaminí 5657, C1440 CABA`.
2. **Reloj Biométrico 15 min & Cobertura < 2 hs**:
   - `index.html` line 477: "Control Biométrico con Alerta a los 15 Minutos: Reloj biométrico conectado por red y 220V en el objetivo; si un operario no ficha al inicio del turno, a los 15 minutos envía alerta por email al supervisor activando el relevo en menos de 2 horas."
   - `index.html` lines 537–542: KPI callouts `15 min Alerta Biométrica` and `< 2 hs Reemplazo en sitio`.
   - `la-empresa/index.html` lines 304–320: Card #7 dedicated to Biometric Clock.
   - `dossier/index.html` line 304: Photo `assets/img/base-guamini-biometrico.jpg`.
3. **Flota Propia Ford Transit**:
   - `MEMORIA_VIVA_ACUERDOS_STAR_UNION.md` section 1.1: "Flota de Unidades Móviles (Ford Transit): Son parte de la flota general de logística y soporte operativo de Star Union (van a todos los objetivos a llevar maquinaria, insumos y personal). NO se comunican como exclusivas de 'Final de Obra'."
   - `servicios-especiales/index.html` lines 7, 146, 157: "Desplegamos unidades móviles Ford Transit..."
   - `la-empresa/index.html` line 255: `src="../assets/img/base-guamini-transit.jpg"` ("Flota propia de utilitarios ploteados Star Union S.R.L.").
   - `dossier/index.html` line 241: `src="../assets/img/base-guamini-transit.jpg"` ("Flota Propia Star Union").
   - `index.html` lines 169, 528, 591: Refers generically to "flota de utilitarios" and "Flota Propia", without explicitly mentioning the "Ford Transit" model name.
4. **Certificación ISO 9001:2015 TÜV Rheinland**:
   - Full presence across all pages: Certificado Nº 01 10006 2529826, ID Certipedia 9000041847, link to `https://www.certipedia.com/quality_marks/9000041847`.
   - `certificacion-iso/index.html` includes downloadable PDF (`certificado-iso-starunion.pdf`), high-res certificate image (`certificado-iso-starunion.jpg`), and audit performance KPIs (Ferroclor 96/100, 438 direct staff, 5S protocols, LAV/LUT machinery).

### Obs 1.3: Forbidden Term Anomaly in `limpieza-en-altura/index.html`
- In `limpieza-en-altura/index.html` line 244:
  `Silletas ergonómicas con cuerda de trabajo y cuerda de vida independiente, salvacabo, casco con barbijo y ventosas de sujeción.`
- The phrase `"casco con barbijo"` introduces the word `"barbijo"`, which is listed as a forbidden term in `BRAND_AND_CONNECTORS.lock.json` line 59. The correct technical industrial term in Argentina is **`barbiquejo`** (mentonera/barbiquejo de casco de seguridad industrial homologado bajo norma IRAM 3620).

---

### Obs 2: Footer Logo Across All 10 Pages and Dossier
- Tool run: `grep_search` on `logo-footer-blanco` across `*.html`.
  Found in all 10 public pages, dossier, and template:
  1. `index.html`: Line 773: `<img src="logo-footer-blanco.png" alt="Star Union S.R.L." class="h-12 w-auto object-contain">`
  2. `la-empresa/index.html`: Line 457: `<img src="../logo-footer-blanco.png" ...>`
  3. `certificacion-iso/index.html`: Line 347: `<img src="../logo-footer-blanco.png" ...>`
  4. `limpieza-industrial/index.html`: Line 315: `<img src="../logo-footer-blanco.png" ...>`
  5. `limpieza-en-altura/index.html`: Line 392: `<img src="../logo-footer-blanco.png" ...>`
  6. `grandes-superficies/index.html`: Line 315: `<img src="../logo-footer-blanco.png" ...>`
  7. `consorcios/index.html`: Line 315: `<img src="../logo-footer-blanco.png" ...>`
  8. `clinicas-y-hospitales/index.html`: Line 315: `<img src="../logo-footer-blanco.png" ...>`
  9. `universidades-y-clubes/index.html`: Line 315: `<img src="../logo-footer-blanco.png" ...>`
  10. `servicios-especiales/index.html`: Line 315: `<img src="../logo-footer-blanco.png" ...>`
  11. `dossier/index.html`: Line 614: `<img src="../logo-footer-blanco.png" ...>`
  12. `footer.html`: Line 7: `<img src="../logo-footer-blanco.png" ...>`
- Existence on disk: `/Users/arianawajntraub/Documents/antigravity/star-union/logo-footer-blanco.png` exists (size: 235,728 bytes).
- Placeholder text scan: `grep_search` for `LOGO BLANCO` returned 15 matches, **100% of which are inside HTML comment lines** (e.g. `<!-- FOOTER OFICIAL UNIFICADO (#133522 CON LOGO BLANCO REAL) -->`). Regex search `>[^<]*LOGO BLANCO[^<]*<` yielded **0 matches**. There is zero visible placeholder text anywhere in the rendered DOM.

---

### Obs 3: WhatsApp Routing Script (`assets/js/starunion-b2b.js`)
- Inspection of `assets/js/starunion-b2b.js`:
  - Lines 84–135: Captures all `a[href*="api.whatsapp.com"], a[href*="wa.me"]` and prevents default click.
  - Injects modal `#su-wa-filter-modal` with two buttons:
    1. `#su-wa-go-b2b`: "🏢 Solicitar Cotización para mi Empresa / Institución →" (dispatches GA4 event `contacto_wa_empresa_b2b` and opens the original commercial WhatsApp URL).
    2. `#su-wa-go-rrhh`: "👷 Busco Trabajo / Enviar CV a Recursos Humanos" (redirects to `/index.html#postularse` without triggering any GA4 or Ads conversion).
- **Critical Flaws Found in WhatsApp Script Implementation**:
  1. **Script missing from 4 pages**:
     - `la-empresa/index.html` (has WhatsApp links on lines 46 & 417, but no script tag for `starunion-b2b.js`).
     - `certificacion-iso/index.html` (has WhatsApp link on line 54, but no script tag).
     - `limpieza-en-altura/index.html` (has WhatsApp links on lines 69 & 373, but no script tag).
     - `dossier/index.html` (has WhatsApp link on line 583, but no script tag).
     *Result:* On these 4 pages, any job applicant clicking WhatsApp immediately bypasses the filter and contacts Mauro's commercial WhatsApp directly, polluting ads data.
  2. **Typography violation in modal**: Line 93 of `assets/js/starunion-b2b.js` has hardcoded inline style `font-family:Inter,sans-serif;`. This violates requirement R1 (which mandates unified `Open Sans`).
  3. **Path routing risk**: Line 102 uses hardcoded root path `href="/index.html#postularse"`. When hosted under a subfolder (e.g. `https://wajntraub.ar/staruniontest/`), this redirects to domain root rather than the project's staging base.

---

### Obs 4: Scan for Prohibited Public Links to Internal Tools
- Ripgrep scan across all 11 public pages + templates for:
  - `radar-comercial`
  - `brochures/editables`
  - `relevamiento-gerencia`
  - `acuerdos`
- **Result:** **0 public links found**.
- These tools are linked exclusively from `/accesos/index.html` (lines 109, 113, 125, 129), which is the private management Linktree for Ariana and Mauro.
- `/accesos/index.html` has `<meta name="robots" content="noindex, nofollow">` and is not linked from any public page.

---

### Obs 5: Language Neutrality and Gender Formatting
- Ripgrep regex scan for `\bbienvenid[a-z/]*\b`, `\btodes\b`, and slash endings `/[aeo]s\b`:
  - `bienvenidos`, `bienvenides`, `bienvenidos/as`: **0 matches** in HTML, JS, or TXT. (Matches only in `GEMINI.md` where the prohibition is defined).
  - `todes`: **0 matches**.
  - `/[aeo]s\b`: **0 matches**.
  - Public pages consistently use natural neutral corporate phrasing: *"Te damos la bienvenida"*, *"Equipo profesional"*, *"Personal en nómina directa"*, *"Quienes integran la empresa"*.

---

### Obs 6: Packaging Logic of `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` & Linktree
- ZIP file inspection: `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` (75,852,350 bytes, last modified Oct 28 10:59).
- Comparison of repo files vs ZIP contents:
  - **Correctly excluded from ZIP**: `accesos/`, `acuerdos/`, `radar-comercial/`, `relevamiento-gerencia/`, `brochures/editables/`, `*.md` files (`AUDITORIA_REAL...`, `BENCHMARK...`, `BRAND_AND_CONNECTORS.lock.json`, `GEMINI.md`, `MEMORIA_VIVA...`, `README.md`).
  - **Leak / Accidental inclusion detected**: `.agents/skills/star-union-sistema-integral/` was included in the zip file (2 directories).
  - **Linktree `/accesos/index.html`**: Verified clean. It provides quick access to:
    1. The 10 public pages (`../index.html`, `../la-empresa/index.html`, etc.)
    2. Dossier Ejecutivo (`../dossier/index.html`)
    3. Management tools (`acuerdos`, `relevamiento-gerencia`, `brochures`, `radar-comercial`).

---

### Obs 7: Brand Firewall Schema Discrepancy & Verification Tests
- Execution of `/Users/arianawajntraub/.gemini/config/firewall/validate_brand_output.py`:
  ```bash
  python3 ~/.gemini/config/firewall/validate_brand_output.py --project "4 - STAR UNION (Limpieza B2B)" --file index.html
  ```
  Result:
  ```
  ✅ AUDITORÍA APROBADA PARA: 4 - STAR UNION (Limpieza B2B)
     • Pronombre/Tono verificado: None
     • Conectores aislados verificados: OK (0 cruces externos)
  ```
- **Code Inspection of `/Users/arianawajntraub/.gemini/config/firewall/brand_firewall.py`**:
  Lines 82–129 and `validate_brand_output.py` lines 36–39 query the following JSON keys:
  - `lock.get("voiceAndLanguageLock", {})`
    - `voice.get("forbiddenTerms", [])`
    - `voice.get("forbiddenGenderRegex")`
    - `voice.get("primaryPronoun")`
  - `lock.get("designAndPaletteLock", {})`
    - `design.get("allowedHexColors", [])`
  - `lock.get("connectorsLock", {})`
    - `connectors.get("forbiddenExternalIds", [])`
- **Current Content of `/Users/arianawajntraub/Documents/antigravity/star-union/BRAND_AND_CONNECTORS.lock.json`**:
  Uses flat root-level keys:
  - `"forbidden_terms": [...]` (instead of `voiceAndLanguageLock.forbiddenTerms`)
  - `"allowed_palette": [...]` (instead of `designAndPaletteLock.allowedHexColors`)
  - `"language_mode": "VOSEO_ARGENTINO_CORPORATIVO_SIN_MARCA_DE_GENERO"` (instead of `voiceAndLanguageLock.primaryPronoun`)
  - `"connectors": {...}` (instead of `connectorsLock`)
- **Direct Consequence Tested**:
  A test string containing `"Bienvenidos a Star Union, tenemos barbijo y paritarias de Fabricio Rivas"` was evaluated by `check_text_against_lock()` and returned `True` (Allowed!) because `voice.get("forbiddenTerms")` was empty due to the schema mismatch.

---

## 2. Logic Chain

1. **Premise 1 (Verticals & Differentials)**:
   - `index.html` showcases 6 verticals in the main grid and the 7th in a dedicated interactive section, with navigation menus linking all 7.
   - All 100 local images across the 11 pages are physically present and load without error.
   - However, in `limpieza-en-altura/index.html` line 244, the phrase `"casco con barbijo"` introduces a forbidden term. Replacing it with `"casco con barbiquejo"` maintains semantic accuracy for industrial safety while achieving 100% compliance with brand lock rules.
2. **Premise 2 (Footer Logo)**:
   - All 10 public pages, `dossier/index.html`, and `footer.html` reference `logo-footer-blanco.png`.
   - The string `"LOGO BLANCO"` occurs only in HTML developer comments and 0 times in visible text nodes. Acceptance criterion regarding footer logo is already 100% satisfied.
3. **Premise 3 (WhatsApp Routing)**:
   - `assets/js/starunion-b2b.js` provides an effective two-way bifurcator (GA4 B2B lead event for corporate inquiries, `/index.html#postularse` for job seekers).
   - Because 4 pages (`la-empresa/index.html`, `certificacion-iso/index.html`, `limpieza-en-altura/index.html`, `dossier/index.html`) lack the `<script src=".../assets/js/starunion-b2b.js"></script>` tag, visitors clicking WhatsApp on those pages bypass the modal entirely. Adding the script tag to those 4 pages completes the defense.
   - Removing `font-family:Inter,sans-serif;` from the modal's inline style and switching to `Open Sans` aligns the modal with requirement R1.
4. **Premise 4 (Public Tool Isolation)**:
   - Scans confirm 0 leaks of `radar-comercial`, `brochures/editables`, `relevamiento-gerencia`, or `acuerdos` in any public page.
   - `accesos/index.html` is private (`noindex, nofollow`), unlinked from the public site, fulfilling requirement R3.
5. **Premise 5 (Language Neutrality)**:
   - Star Union consistently uses neutral phrasing across all 10 public pages and the dossier. No instances of gendered or faux-inclusive greetings exist.
6. **Premise 6 (ZIP Packaging & Reproducibility)**:
   - `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` currently protects management tools from export, but includes `.agents/skills/`.
   - A standardized packaging script or one-line command with explicit `-x ".agents*"` exclusions guarantees clean, repeatable distribution.
7. **Premise 7 (Firewall Alignment)**:
   - The brand firewall scripts (`brand_firewall.py` and `validate_brand_output.py`) were built expecting a nested schema (`voiceAndLanguageLock`, `designAndPaletteLock`, `connectorsLock`).
   - Updating `BRAND_AND_CONNECTORS.lock.json` to include both the nested objects and preserving legacy keys restores instant, automated verification by the firewall.

---

## 3. Caveats

- **No Caveats** regarding local files: all 11 HTML pages, JS files, lockfiles, and images were inspected directly on the local filesystem.
- The external Unsplash images used in `clinicas-y-hospitales` and `grandes-superficies` cards in `index.html` were not downloaded locally, though they resolve to live CDNs. If offline self-containment is desired in future milestones, local assets from `brochures/img/` can substitute them.

---

## 4. Conclusion & Proposed Action Plan

### Core Findings Summary
1. **Verticals & Photos**: All 7 verticals are present and linked. All 100 local images resolve properly.
2. **Footer Logo**: 100% compliant. Real white logo referenced in 11/11 pages, 0 visible placeholder strings.
3. **WhatsApp Filter**: Logic is solid, but **4 pages are missing the script tag** (`la-empresa`, `certificacion-iso`, `limpieza-en-altura`, `dossier`). Modal inline style needs `Open Sans`.
4. **Internal Security**: 100% compliant. Public pages contain 0 links to internal management tools.
5. **Gender Neutrality**: 100% compliant. No forbidden greetings.
6. **Barbijo Term Correction**: Change `"casco con barbijo"` to `"casco con barbiquejo"` in `limpieza-en-altura/index.html:244`.
7. **Packaging**: Exclude `.agents*` when re-generating `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip`.
8. **Brand Lockfile Schema**: Harmonize `BRAND_AND_CONNECTORS.lock.json` with `brand_firewall.py` schema so automated pre-flight checks enforce all rules.

---

### Concrete Proposed Changes for Implementation Workers

#### Proposal A: Add `starunion-b2b.js` to the 4 missing pages
In:
- `/Users/arianawajntraub/Documents/antigravity/star-union/la-empresa/index.html` (before `</body>`)
- `/Users/arianawajntraub/Documents/antigravity/star-union/certificacion-iso/index.html` (before `</body>`)
- `/Users/arianawajntraub/Documents/antigravity/star-union/limpieza-en-altura/index.html` (before `</body>`)
- `/Users/arianawajntraub/Documents/antigravity/star-union/dossier/index.html` (before `</body>`)

Snippet:
```html
    <!-- MOTOR DE CONVERSIÓN B2B Y MICRO-FILTRO DE WHATSAPP -->
    <script src="../assets/js/starunion-b2b.js"></script>
```

#### Proposal B: Update Modal Font in `assets/js/starunion-b2b.js`
In `/Users/arianawajntraub/Documents/antigravity/star-union/assets/js/starunion-b2b.js`:
- Line 93: Change `font-family:Inter,sans-serif;` to `font-family:'Open Sans',sans-serif;`.
- Line 102: Change `href="/index.html#postularse"` to relative or intelligent target: `href="../index.html#postularse"`.

#### Proposal C: Fix Safety Term in `limpieza-en-altura/index.html`
In `/Users/arianawajntraub/Documents/antigravity/star-union/limpieza-en-altura/index.html` line 244:
```html
<!-- BEFORE -->
Silletas ergonómicas con cuerda de trabajo y cuerda de vida independiente, salvacabo, casco con barbijo y ventosas de sujeción.

<!-- AFTER -->
Silletas ergonómicas con cuerda de trabajo y cuerda de vida independiente, salvacabo, casco con barbiquejo homologado y ventosas de sujeción.
```

#### Proposal D: Harmonize `BRAND_AND_CONNECTORS.lock.json`
Update `/Users/arianawajntraub/Documents/antigravity/star-union/BRAND_AND_CONNECTORS.lock.json` to include the standard nested blocks (`voiceAndLanguageLock`, `designAndPaletteLock`, `connectorsLock`) while preserving the existing keys:
```json
{
  "project_number": 4,
  "project_id": "4 - STAR UNION (Limpieza B2B)",
  "projectId": "STAR_UNION_B2B",
  "displayName": "4 - STAR UNION (Limpieza B2B)",
  "brand_name": "Star Union S.R.L.",
  "domain": "www.starunion.com.ar",
  "staging_url": "https://wajntraub.ar/staruniontest/",
  "github_repo": "https://github.com/arianawajntraub/staruniontest.git",
  "local_workspace": "/Users/arianawajntraub/Documents/antigravity/star-union",
  "language_mode": "VOSEO_ARGENTINO_CORPORATIVO_SIN_MARCA_DE_GENERO",
  "voiceAndLanguageLock": {
    "primaryPronoun": "VOSEO_ARGENTINO_CORPORATIVO_SIN_MARCA_DE_GENERO",
    "forbiddenTerms": [
      "Fabricio Rivas",
      "rivas-2026",
      "399457913",
      "536338759",
      "552000200",
      "Entretelado",
      "entretelado.com.ar",
      "Zaguán",
      "zaguan",
      "Bienvenides",
      "bienvenides",
      "todes",
      "Todes",
      "Bienvenidos a Star Union",
      "barbijo",
      "barbijos",
      "tapabocas",
      "COVID-19",
      "paritaria",
      "paritarias",
      "post-paritaria",
      "postparitaria",
      "comparar tu servicio actual"
    ],
    "forbiddenGenderRegex": "\\b(bienvenidos|bienvenides|bienvenidos/as|todes)\\b",
    "supportedLanguages": ["es-AR"]
  },
  "designAndPaletteLock": {
    "allowedHexColors": [
      "#03582D",
      "#024121",
      "#047A3E",
      "#133522",
      "#0E2719",
      "#1A4A2F",
      "#FFCC29",
      "#E5B622",
      "#FFFFFF",
      "#F9FAFB",
      "#F3F4F6",
      "#E5E7EB",
      "#676B67",
      "#111827",
      "#000000"
    ],
    "typography": ["Open Sans"]
  },
  "connectorsLock": {
    "domain": "www.starunion.com.ar",
    "whatsapp": "+5491122759369",
    "googleAdsCustomerId": "4477242318",
    "ga4PropertyId": "356146296",
    "ga4MeasurementId": "G-YDDJQHK8VC",
    "forbiddenExternalIds": [
      "empty-morning-01858808",
      "4943884874",
      "escribanofabriciorivas.com"
    ]
  },
  "allowed_palette": [ ... ],
  "connectors": { ... },
  "forbidden_terms": [ ... ]
}
```

#### Proposal E: Packaging Command for Regenerating Clean ZIP
To regenerate `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` cleanly:
```bash
cd /Users/arianawajntraub/Documents/antigravity/star-union
rm -f SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip
zip -r SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip . \
  -x ".git*" \
  -x ".agents*" \
  -x "*.md" \
  -x "*.json" \
  -x "*.zip" \
  -x ".DS_Store" \
  -x "accesos/*" \
  -x "acuerdos/*" \
  -x "radar-comercial/*" \
  -x "relevamiento-gerencia/*" \
  -x "brochures/editables/*"
```

---

## 5. Verification Method

To independently verify these findings:

1. **Verify 0 visible 'LOGO BLANCO' occurrences**:
   ```bash
   python3 -c "
   import re, glob
   files = glob.glob('/Users/arianawajntraub/Documents/antigravity/star-union/**/*.html', recursive=True)
   hits = []
   for f in files:
       content = open(f, encoding='utf-8').read()
       # remove comments
       clean = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
       if 'LOGO BLANCO' in clean.upper():
           hits.append(f)
   print('Visible LOGO BLANCO hits:', hits)
   "
   ```
2. **Verify WhatsApp script missing from 4 pages**:
   ```bash
   grep -L "starunion-b2b.js" \
     /Users/arianawajntraub/Documents/antigravity/star-union/{la-empresa,certificacion-iso,limpieza-en-altura,dossier}/index.html
   ```
3. **Verify 0 public leaks of internal tools**:
   ```bash
   grep -rnE "(radar-comercial|brochures/editables|relevamiento-gerencia|acuerdos/index)" \
     /Users/arianawajntraub/Documents/antigravity/star-union/{index.html,la-empresa,certificacion-iso,limpieza-industrial,limpieza-en-altura,grandes-superficies,consorcios,clinicas-y-hospitales,universidades-y-clubes,servicios-especiales,dossier}/
   ```
4. **Verify Brand Firewall pre-flight**:
   ```bash
   python3 /Users/arianawajntraub/.gemini/config/firewall/validate_brand_output.py \
     --project "4 - STAR UNION (Limpieza B2B)" \
     --file /Users/arianawajntraub/Documents/antigravity/star-union/index.html
   ```
