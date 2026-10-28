## 2026-10-28T14:32:52Z
You are the Worker for Milestone 1: Typography Unification (R1) for Star Union S.R.L.
Your assigned working directory is:
/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m1_typography

MANDATORY FIRST STEPS:
You MUST read the following files before starting your work:
- /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md (MANDATORY)
- /Users/arianawajntraub/Documents/antigravity/star-union/PROJECT.md
- /Users/arianawajntraub/Documents/antigravity/star-union/BRAND_AND_CONNECTORS.lock.json
- /Users/arianawajntraub/Documents/antigravity/star-union/GEMINI.md
- /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/explorer_survey_typography/handoff.md (Contains exact line numbers and templates)

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Scope & Owned Files:
You exclusively own and will modify:
1. index.html
2. la-empresa/index.html
3. certificacion-iso/index.html
4. limpieza-industrial/index.html
5. limpieza-en-altura/index.html
6. grandes-superficies/index.html
7. consorcios/index.html
8. clinicas-y-hospitales/index.html
9. universidades-y-clubes/index.html
10. servicios-especiales/index.html
11. dossier/index.html

Implementation Tasks:
1. Google Fonts Universal en <head> con preconnects en los 11 archivos:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
```
Eliminar cualquier enlace a Inter o Plus Jakarta Sans.

2. Estandarizar tailwind.config en los 11 archivos:
```javascript
tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Open Sans"', 'sans-serif'],
                heading: ['"Open Sans"', 'sans-serif'],
                display: ['"Open Sans"', 'sans-serif']
            },
            colors: {
                brand: { DEFAULT: '#03582d', dark: '#024121', light: '#047a3e' },
                accent: { DEFAULT: '#ffcc29', hover: '#e5b622' },
                neutral: { custom: '#676b67', dark: '#111827', light: '#ffffff' }
            }
        }
    }
}
```

3. Estandarizar regla maestra en <style> en los 11 archivos:
```css
body {
    font-family: 'Open Sans', sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    color: #676b67;
    background-color: #ffffff;
}
h1, h2, h3, h4, .font-heading, .font-display {
    font-family: 'Open Sans', sans-serif;
    color: #000000;
}
```
En certificacion-iso/index.html, asegurar <body class="... bg-white ..."> (cambiar bg-gray-50 a bg-white).

4. Verificar que no quede ningún salto de tamaño corporal ni fuente (Open Sans 100% uniforme a 16px base).

5. Ejecutar validaciones en la terminal:
- grep de Inter y Plus Jakarta Sans (debe dar 0).
- grep de Open Sans (debe dar 11 coincidencias).
- grep de font-size: 1.125rem (debe dar 0).

Deliverables:
- Maintain progress.md in your working directory.
- Write handoff.md in /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m1_typography/handoff.md documenting all edits, before/after, and test commands/outputs.
- Call send_message to report completion to parent orchestrator.
