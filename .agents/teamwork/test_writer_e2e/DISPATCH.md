## 2026-10-28T14:32:52Z
You are the Test Writer for the E2E Testing Track of Star Union S.R.L.
Your assigned working directory is:
/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/test_writer_e2e

MANDATORY FIRST STEPS:
You MUST read the following files before starting your work:
- /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/ORIGINAL_REQUEST.md (MANDATORY)
- /Users/arianawajntraub/Documents/antigravity/star-union/PROJECT.md
- /Users/arianawajntraub/Documents/antigravity/star-union/BRAND_AND_CONNECTORS.lock.json
- /Users/arianawajntraub/Documents/antigravity/star-union/GEMINI.md
- All 3 survey handoffs in /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/explorer_survey_*/handoff.md

Your Mission (Dual Track E2E Testing):
Design and build an opaque-box, requirement-driven E2E test suite for Star Union derived directly from user requirements and PROJECT.md § Feature Inventory.

Deliverables:
1. Create /Users/arianawajntraub/Documents/antigravity/star-union/TEST_INFRA.md following the template:
- Test Philosophy: Opaque-box, requirement-driven.
- Feature Inventory (F1 to F10).
- 4-Tier Test Case Design:
  - Tier 1: Feature Coverage (≥5 test cases per feature across F1-F10).
  - Tier 2: Boundary & Corner Cases (≥5 per feature where applicable).
  - Tier 3: Cross-Feature Combinations (Pairwise coverage).
  - Tier 4: Real-World Application Scenarios (B2B client journeys & integrity checks).
  Total tests: ~110+ comprehensive checks.

2. Create the test suite in /Users/arianawajntraub/Documents/antigravity/star-union/tests/ (e.g., tests/test_e2e_suite.py) and a test runner script (e.g. tests/run_tests.sh or python3 tests/test_e2e_suite.py):
- Implement programmatic checks for:
  - Typography: Open Sans loaded in head with preconnects, tailwind.config fonts, 1rem base body, 0 Inter/Jakarta.
  - Colors: 0 forbidden classes (blue-*, indigo-*, sky-*, orange-*, amber-*, cyan-*, purple-*), no Brazil-flag effect (no yellow button on green hero or green footer), official palette adherence.
  - Brand Locks: 0 visible 'LOGO BLANCO', footer logo logo-footer-blanco.png exists and is referenced in 11/11 pages, 0 forbidden gendered terms, 0 leaks of internal tools (radar-comercial, relevamiento-gerencia, etc.) in public pages.
  - WhatsApp Filter: starunion-b2b.js present in all 11 pages with Open Sans modal.
  - Distribution Packaging: validates SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip structure when present (excludes .agents*, *.md, internal tools).
- The test runner must provide colored console output, per-tier breakdown, pass/fail counts, and exit code 0 on complete pass.

3. Execute the test runner, document which tests pass now (e.g. brand checks already passing) and which are expected to pass as milestones progress.

4. Publish /Users/arianawajntraub/Documents/antigravity/star-union/TEST_READY.md when test infrastructure and test cases are ready.

Deliverables:
- Maintain progress.md in your working directory.
- Write handoff.md in /Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/test_writer_e2e/handoff.md.
- Call send_message to report completion to parent orchestrator.
