# Scope: Milestone 1 — Typography Unification (R1)

## Architecture & Interfaces
- Target: Unify typography across all 10 public HTML pages + `dossier/index.html`.
- Single official font: `Open Sans` (weights 300 to 800).
- Standard body base size: `1rem` (16px), `line-height: 1.6`.
- Eliminate all references and imports of `Inter` and `Plus Jakarta Sans`.
- Eliminate `body { font-size: 1.125rem; }` from `index.html` and `certificacion-iso/index.html`.
- Add `<link rel="preconnect">` to all 11 files.
- Standardize `tailwind.config` across all 11 files with `Open Sans` for `sans`, `heading`, and `display`.
- Standardize heading hierarchy (H1, H2, H3, H4) per `PROJECT.md § Interface Contracts`.

## Files Owned
- `/Users/arianawajntraub/Documents/antigravity/star-union/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/la-empresa/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/certificacion-iso/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/limpieza-industrial/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/limpieza-en-altura/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/grandes-superficies/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/consorcios/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/clinicas-y-hospitales/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/universidades-y-clubes/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/servicios-especiales/index.html`
- `/Users/arianawajntraub/Documents/antigravity/star-union/dossier/index.html`

## Reference Survey
- Read `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/explorer_survey_typography/handoff.md` for exact line numbers and replacement snippets.

## Completion Criteria
1. Exactly 11/11 pages import Open Sans with preconnects.
2. 0 imports of `Inter` or `Plus Jakarta Sans` in public pages or dossier.
3. 0 occurrences of `body { font-size: 1.125rem;` in public pages or dossier.
4. Reviewer approval and Forensic Auditor clean verdict.
