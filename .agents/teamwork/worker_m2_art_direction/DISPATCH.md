## 2026-10-28T15:11:09Z

You are the Worker for Milestone 2: Art Direction & Palette Refinement (R2) of Star Union S.R.L.
Your assigned working directory is:
/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m2_art_direction

MANDATORY FIRST STEPS:
You MUST read the following files before starting your work:
- /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md (MANDATORY)
- /Users/arianawajntraub/Documents/antigravity/star-union/PROJECT.md
- /Users/arianawajntraub/Documents/antigravity/star-union/BRAND_AND_CONNECTORS.lock.json
- /Users/arianawajntraub/Documents/antigravity/star-union/GEMINI.md
- /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/explorer_survey_art_direction/handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Scope & Tasks for Milestone 2 (Art Direction & Palette Refinement):

1. Hero Section B2B Redesign in index.html (F4):
   - Refactor Hero section container from full-green (bg-brand pt-20...) to pure white (bg-white pt-16 pb-20 border-b border-gray-100 relative overflow-hidden or bg-[#f9fafb]).
   - Change H1 from text-white to text-[#000000] font-extrabold.
   - Change paragraph lead from text-white/90 to text-[#676b67] text-lg.
   - Upper badge: Change from bg-brand-dark/80 border border-white/20 text-white to subtle institutional: bg-gray-100 border border-gray-200 text-gray-800 text-xs font-bold px-4 py-1.5 rounded-full (preserve micro yellow star <span class="text-accent">★</span>).
   - Primary CTA button: Change from yellow (bg-accent text-[#000000]) to institutional green: bg-brand hover:bg-brand-dark text-white font-bold px-8 py-4 rounded-lg shadow-sm transition.
   - Secondary CTA button: Change to bg-white text-brand border border-gray-200 hover:bg-gray-50 font-bold px-7 py-4 rounded-lg shadow-sm transition.
   - Ensure the right-column Hero cards / stats have white/pearl backgrounds, dark text, and subtle borders.

2. Footer Official Unification across all 10 public pages (F5):
   Files:
   - index.html
   - la-empresa/index.html
   - certificacion-iso/index.html
   - limpieza-industrial/index.html
   - limpieza-en-altura/index.html
   - grandes-superficies/index.html
   - consorcios/index.html
   - clinicas-y-hospitales/index.html
   - universidades-y-clubes/index.html
   - servicios-especiales/index.html
   (Verify dossier/index.html as well).
   Changes:
   - Keep dark green background bg-[#133522] and white logo logo-footer-blanco.png.
   - In contact box: Replace <strong class="text-[#ffcc29] uppercase"> with <strong class="text-white/95 uppercase font-semibold">.
   - In vertical links list: Replace hover:text-[#ffcc29] with hover:text-white transition duration-150.
   - In CTA button: Replace yellow button <a href="#contacto" class="... bg-[#ffcc29] hover:bg-[#e5b622] text-[#000000] ..."> with corporate white button:
     <a href="#contacto" class="block text-center bg-white hover:bg-gray-100 text-brand font-bold text-xs uppercase tracking-wider py-3 px-4 rounded-lg transition shadow-sm">Solicitar Relevamiento Sin Cargo</a>
   - Deduplicate comment <!-- FOOTER OFICIAL UNIFICADO... --> where repeated twice.

3. Palette & Color Cleanup (F6):
   - In index.html:200: Replace b2b-warning-alert classes bg-red-50 border-red-200 text-red-800 with corporate neutral: bg-gray-100 border border-gray-300 text-gray-800 p-3 rounded-lg text-xs font-semibold.
   - In index.html:379: Replace badge bg-accent text-[#000000] with bg-brand/10 text-brand border border-brand/20 font-bold.
   - In certificacion-iso/index.html:245: Replace badge bg-accent text-[#000000] with bg-brand/10 text-brand border border-brand/20 font-bold.
   - In la-empresa/index.html: In tailwind.config, replace #057a3f with #047a3e, #023d1f with #024121, #e6b822 with #e5b622. In floating WhatsApp button (line 46), replace hover:bg-[#023d1f] with hover:bg-brand-dark.
   - In limpieza-en-altura/index.html: In tailwind.config, replace #057a3f with #047a3e, #023d1f with #024121. In floating WhatsApp button (line 69), replace hover:bg-[#023d1f] with hover:bg-brand-dark.
   - In dossier/index.html: In tailwind.config, replace #057a3f with #047a3e, #023d1f with #024121.

4. Run Verification Tests:
   - python3 tests/run_tests.py --milestone M2 (All 32 tests must pass!)
   - python3 tests/run_tests.py --milestone M1 (Must remain 34/34 passing!)

Deliverables:
- Maintain progress.md in your working directory.
- Write handoff.md in /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/worker_m2_art_direction/handoff.md.
- Call send_message to report completion to parent orchestrator.
