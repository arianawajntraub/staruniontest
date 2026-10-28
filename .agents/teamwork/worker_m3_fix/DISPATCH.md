# Dispatch: Worker M3 Fix — JavaScript Syntax, Form Fallbacks & Clean Packaging

**Role**: Fix Worker (JavaScript & Packaging)
**Working Directory**: `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_fix`
**Project Root**: `/Users/arianawajntraub/Documents/antigravity/star-union`
**Authoritative Request**: `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md`
**Challenger 1 Report**: `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/challenger_m3_1/handoff.md`
**Challenger 2 Report**: `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/challenger_m3_2/handoff.md`

---

## MANDATORY INTEGRITY WARNING
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

---

## Required Tasks

### 1. Fix SyntaxError in `assets/js/starunion-b2b.js`
In `assets/js/starunion-b2b.js`:
- Line 86:
  Fix unescaped double quotes in querySelectorAll:
  `var waLinks = document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]');`
- Lines 93–104:
  Fix unescaped double quotes inside `modal.innerHTML = [...]`. Use single quotes for HTML attribute values (e.g. `<div style='...'>`, `id='su-wa-close'`) or template literals with proper escaping so that JavaScript compiles cleanly.
- Verify with `node -c assets/js/starunion-b2b.js` (must exit with 0).

### 2. Support Multi-Field Form Inputs (Fix Lead Data Loss)
In `assets/js/starunion-b2b.js`:
In the `.js-b2b-quote-form` submit handler (around lines 36–95), support both `index.html` fields and vertical page fields (`certificacion-iso` and 6 vertical pages):
```javascript
const empresa = (form.querySelector('[name="empresa"]')?.value || '').trim();
const nombre = (form.querySelector('[name="nombre"]')?.value || '').trim();
const cargo = (form.querySelector('[name="cargo"]')?.value || '').trim();
const email = (form.querySelector('[name="email"]')?.value || '').trim();
const telefono = (form.querySelector('[name="telefono"]')?.value || '').trim();
const contacto = cargo || [email, telefono].filter(Boolean).join(' · ');

const tipo = form.querySelector('[name="tipo_organizacion"]')?.value || '';
const servicio = form.querySelector('[name="servicio_requerido"]')?.value || 'Relevamiento Técnico B2B';
const ubicacion = form.querySelector('[name="ubicacion"]')?.value || 'AMBA';
const escala = (form.querySelector('[name="escala"]')?.value || '').trim();
const mensaje = (form.querySelector('[name="mensaje"]')?.value || '').trim();
const detalle = escala || mensaje;
```
In `cuerpo`:
```javascript
`• Email / Teléfono: ${contacto}`,
...
detalle ? `• Detalle adicional: ${detalle}` : ''
```

### 3. Exclude / Remove Stale Backup Files & Rebuild Distribution ZIP
- If `indexEX` or `limpieza-industrial/indexVIEJO` exist on disk, remove them or ensure zip command excludes `-x "*indexEX*" -x "*indexVIEJO*"`.
- Rebuild `SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip` cleanly:
  ```bash
  zip -r SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip . \
    -x ".git*" \
    -x ".agents*" \
    -x "*.md" \
    -x "*.json" \
    -x "*.zip" \
    -x ".DS_Store" \
    -x "*indexEX*" \
    -x "*indexVIEJO*" \
    -x "accesos/*" \
    -x "acuerdos/*" \
    -x "radar-comercial/*" \
    -x "relevamiento-gerencia/*" \
    -x "brochures/editables/*" \
    -x "tests/*"
  ```
- Test unzipping `assets/js/starunion-b2b.js` to a temp directory and run `node -c` on it.
- Verify neither `indexEX` nor `indexVIEJO` are inside the zip.

---

## Verification
Execute and verify:
1. `node -c assets/js/starunion-b2b.js`
2. `python3 tests/challenger_m3_verify.py`
3. `python3 tests/run_tests.py -v --milestone M3`
4. `python3 tests/run_tests.py -v`

Document all fixes, commands, and outputs in `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_fix/handoff.md`.
Notify orchestrator via `send_message`.


## 2026-10-28T16:17:03Z
[Message] timestamp=2026-10-28T16:17:03Z sender=e86356a5-39e5-4a9e-ba35-f025439cb0eb priority=MESSAGE_PRIORITY_HIGH
You are worker_m3_fix.
Working directory: /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_fix
Project root: /Users/arianawajntraub/Documents/antigravity/star-union

MANDATORY FIRST STEPS:
1. Read /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md
2. Read your detailed dispatch instructions at /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_fix/DISPATCH.md
3. Read /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/challenger_m3_1/handoff.md
4. Read /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/challenger_m3_2/handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

SCOPE:
1. Fix SyntaxError in assets/js/starunion-b2b.js (unescaped double quotes on line 86 querySelectorAll and lines 93-104 modal.innerHTML).
2. Add multi-field fallbacks in assets/js/starunion-b2b.js submit handler for name='email', name='telefono', and name='mensaje' from vertical pages.
3. Exclude / delete stale backup files (indexEX, limpieza-industrial/indexVIEJO) and rebuild SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip cleanly.
4. Run:
   node -c assets/js/starunion-b2b.js
   python3 tests/challenger_m3_verify.py
   python3 tests/run_tests.py -v --milestone M3
   python3 tests/run_tests.py -v

Document everything in /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m3_fix/handoff.md and notify me via send_message.
