# Dispatch: Milestone 3 — Brand Locks, Components & Packaging (R3)

**Agent Role**: Typography, Brand & Distribution Worker
**Working Directory**: `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_brand_packaging`
**Project Root**: `/Users/arianawajntraub/Documents/antigravity/star-union`
**Authoritative Request**: `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md`
**Project Plan**: `/Users/arianawajntraub/Documents/antigravity/star-union/PROJECT.md`
**Test Suite**: `/Users/arianawajntraub/Documents/antigravity/star-union/tests/test_e2e_suite.py`
**Test Runner**: `python3 tests/run_tests.py -v --milestone M3`

---

## MANDATORY INTEGRITY WARNING
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

---

## Detailed Implementation Tasks

### 1. Feature F7: WhatsApp Modal Script & ISO Form Integration
- **Script Injection**:
  Add `<script src="../assets/js/starunion-b2b.js"></script>` just before `</body>` in the 4 remaining pages that lack it:
  1. `la-empresa/index.html`
  2. `certificacion-iso/index.html`
  3. `limpieza-en-altura/index.html`
  4. `dossier/index.html` (note relative path for dossier)
- **ISO Contact Form Refinement (`certificacion-iso/index.html`)**:
  - Locate the quote/contact form.
  - Ensure the `<form>` element has class `js-b2b-quote-form` (or preserves its existing classes plus `js-b2b-quote-form`).
  - Add explicit `name` attributes to all form fields:
    - Empresa: `name="empresa"`
    - Nombre: `name="nombre"`
    - Email: `name="email"`
    - Teléfono: `name="telefono"`
    - Mensaje / Requerimiento: `name="mensaje"`
  - Ensure the submit button has `type="submit"`.
- **External Image Replacement in `certificacion-iso/index.html`**:
  - Locate line ~186 or where the external Wikimedia Commons image is used: `https://upload.wikimedia.org/...`
  - Replace the external URL with a local verified asset: `../logo-tuv.png` or `../assets/img/tuv-iso-9001-badge.png` (verify which file exists in the directory).

### 2. Feature F8: Brand Safety, Terminology & Lockfile Harmonization
- **PPE / Height Cleaning Safety Term (`limpieza-en-altura/index.html`)**:
  - Locate line ~244: `"casco con barbijo"`.
  - Replace `"casco con barbijo"` with `"casco con barbiquejo homologado"`. (Barbijo is COVID medical mask; barbiquejo is helmet chin strap).
- **Banner Badge Contrast (`index.html:396`)**:
  - In `index.html` line ~396 (Cobertura Regional Propia banner inside `bg-brand` container):
  - Change class from `bg-brand/10 text-brand border border-brand/20` to `bg-white/15 text-white border border-white/25 font-bold text-xs uppercase px-3 py-1 rounded-full inline-block mb-3 tracking-wider` so that text is clearly legible with high contrast against the dark green background.
- **Lockfile Harmonization (`BRAND_AND_CONNECTORS.lock.json`)**:
  - Harmonize the JSON structure to include both nested blocks and preserve existing flat keys (for brand firewall CLI compatibility):
    ```json
    {
      "brandId": "4 - STAR UNION (Limpieza B2B)",
      "version": "2.0.0",
      "voiceAndLanguageLock": {
        "pronoun": "voseo",
        "genderFree": true,
        "tone": "corporativo B2B institucional",
        "forbiddenWords": [
          "barbijo",
          "covid",
          "chicos",
          "empleaditas",
          "mucamas",
          "barato",
          "low cost"
        ]
      },
      "designAndPaletteLock": {
        "dominantColor": "#ffffff",
        "dominantColorPercentage": "80-85%",
        "institutionalGreen": "#03582d",
        "institutionalGreenDark": "#133522",
        "institutionalGreenPercentage": "12-15%",
        "accentYellow": "#ffcc29",
        "accentYellowPercentage": "<=5%",
        "typography": "Open Sans"
      },
      "connectorsLock": {
        "whatsappB2B": "+5491168019958",
        "emailB2B": "contacto@starunion.com.ar",
        "crmUrl": "https://script.google.com/macros/s/AKfycbyfP_L-p3_C0R_p5q_wA3zK/exec"
      },
      "allowedColors": [
        "#03582d",
        "#133522",
        "#0e2719",
        "#ffcc29",
        "#ffffff",
        "#f9fafb",
        "#f3f4f6",
        "#e5e7eb",
        "#111827",
        "#374151",
        "#4b5563"
      ],
      "forbiddenClasses": [
        "bg-blue-",
        "text-blue-",
        "border-blue-",
        "bg-red-",
        "text-red-",
        "border-red-",
        "bg-orange-",
        "text-orange-",
        "border-orange-",
        "bg-purple-",
        "text-purple-",
        "border-purple-",
        "bg-pink-",
        "text-pink-",
        "border-pink-"
      ],
      "forbiddenTerms": [
        "barbijo",
        "covid",
        "chicos",
        "empleaditas",
        "mucamas",
        "barato",
        "low cost"
      ]
    }
    ```

### 3. Feature F9: Clean HostGator ZIP Packaging & Robots Check
- **Linktree Robots Check**:
  - Verify that `accesos/index.html` has `<meta name="robots" content="noindex, nofollow">`.
- **Packaging Generation**:
  - Run the clean packaging command from the project root:
    ```bash
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
      -x "brochures/editables/*" \
      -x "tests/*"
    ```
  - Verify with `unzip -l SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` that no `.git`, `.agents`, `*.md`, or internal files are included.

---

## Verification & Reporting
1. Run `python3 tests/run_tests.py -v --milestone M3` and record output.
2. Run full suite `python3 tests/run_tests.py -v` to ensure 0 regressions.
3. Write complete report in `.agents/teamwork/worker_m3_brand_packaging/handoff.md`.
4. Send completion message back to orchestrator.


## 2026-10-28T15:47:59Z

You are worker_m3_brand_packaging.
Your working directory is: /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_brand_packaging

MANDATORY FIRST STEPS:
1. Read /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md
2. Read your detailed dispatch instructions at /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_brand_packaging/DISPATCH.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

SCOPE OF WORK:
- Feature F7: Inject '../assets/js/starunion-b2b.js' before </body> in la-empresa/index.html, certificacion-iso/index.html, limpieza-en-altura/index.html, and dossier/index.html.
  In certificacion-iso/index.html: add name attributes (empresa, nombre, email, telefono, mensaje) to quote form fields, ensure js-b2b-quote-form class, ensure type="submit" button, and replace external Wikimedia TÜV image with local asset (e.g. ../logo-tuv.png or verified local badge).
- Feature F8: Fix 'casco con barbijo' to 'casco con barbiquejo homologado' in limpieza-en-altura/index.html:244. Fix badge contrast in index.html:396 (Cobertura Regional Propia -> bg-white/15 text-white border-white/25). Harmonize BRAND_AND_CONNECTORS.lock.json with nested blocks while preserving legacy flat keys.
- Feature F9: Verify accesos/index.html has noindex, nofollow robots meta tag. Regenerate SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip excluding internal files (.git*, .agents*, *.md, *.json, tests/*, etc.).

VERIFICATION:
Run:
python3 tests/run_tests.py -v --milestone M3
and
python3 tests/run_tests.py -v

Document all changes, file paths, commands and test outputs in /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_brand_packaging/handoff.md.
When finished, notify me via send_message.
