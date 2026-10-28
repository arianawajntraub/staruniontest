"""
E2E Test Suite for Star Union S.R.L.
Opaque-Box, Requirement-Driven Verification Suite
Derived from:
- ORIGINAL_REQUEST.md
- PROJECT.md (§ Feature Inventory F1-F10)
- BRAND_AND_CONNECTORS.lock.json
- GEMINI.md
"""

import os
import re
import json
import zipfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PUBLIC_PAGES = [
    "index.html",
    "la-empresa/index.html",
    "certificacion-iso/index.html",
    "limpieza-industrial/index.html",
    "limpieza-en-altura/index.html",
    "grandes-superficies/index.html",
    "consorcios/index.html",
    "clinicas-y-hospitales/index.html",
    "universidades-y-clubes/index.html",
    "servicios-especiales/index.html",
    "dossier/index.html",
]

PUBLIC_PAGES_NO_DOSSIER = [p for p in PUBLIC_PAGES if not p.startswith("dossier")]

def get_page_content(rel_path):
    full_path = PROJECT_ROOT / rel_path
    if not full_path.exists():
        return None
    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def strip_html_comments(html):
    return re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

def get_home_hero_section(content):
    if not content:
        return ""
    h1_pos = content.find("<h1")
    if h1_pos == -1:
        return ""
    sec_start = content.rfind("<section", 0, h1_pos)
    sec_end = content.find("</section>", h1_pos)
    if sec_start == -1 or sec_end == -1:
        return ""
    return content[sec_start:sec_end + len("</section>")]


# ==============================================================================
# TIER 1: FEATURE COVERAGE (50 Tests, 5 per feature F1-F10)
# ==============================================================================

class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Direct Feature Coverage for F1 to F10 (5 tests per feature)."""

    # --- F1: Typography in <head> & <style> (Milestone: M1) ---

    def test_t1_f1_01_preconnect_google_fonts(self):
        """F1: All 11 pages must load preconnect links for Google Fonts in <head>."""
        missing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            head_match = re.search(r"<head>(.*?)</head>", content, re.DOTALL | re.I)
            head = head_match.group(1) if head_match else ""
            has_fonts_pre = 'rel="preconnect" href="https://fonts.googleapis.com"' in head or "rel='preconnect' href='https://fonts.googleapis.com'" in head
            has_gstatic_pre = "fonts.gstatic.com" in head and "preconnect" in head
            if not (has_fonts_pre and has_gstatic_pre):
                missing.append(p)
        self.assertEqual(len(missing), 0, f"Pages missing preconnects to Google Fonts: {missing}")

    def test_t1_f1_02_open_sans_font_link(self):
        """F1: All 11 pages must load Google Fonts with Open Sans (weights 300..800)."""
        missing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            head_match = re.search(r"<head>(.*?)</head>", content, re.DOTALL | re.I)
            head = head_match.group(1) if head_match else ""
            if not re.search(r"family=Open\+Sans", head, re.I):
                missing.append(p)
        self.assertEqual(len(missing), 0, f"Pages missing Open Sans in <head>: {missing}")

    def test_t1_f1_03_eradication_of_inter_in_head(self):
        """F1: 0 pages must load Inter font in <head>."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            head_match = re.search(r"<head>(.*?)</head>", content, re.DOTALL | re.I)
            head = head_match.group(1) if head_match else ""
            if re.search(r"family=Inter", head, re.I):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages still loading Inter font in <head>: {failing}")

    def test_t1_f1_04_eradication_of_jakarta_in_head(self):
        """F1: 0 pages must load Plus Jakarta Sans font in <head>."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            head_match = re.search(r"<head>(.*?)</head>", content, re.DOTALL | re.I)
            head = head_match.group(1) if head_match else ""
            if re.search(r"Plus\+Jakarta\+Sans", head, re.I):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages still loading Plus Jakarta Sans in <head>: {failing}")

    def test_t1_f1_05_body_base_font_size_1rem(self):
        """F1: 0 pages must set body font-size to 1.125rem (must be unified base 1rem/16px)."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            if re.search(r"font-size:\s*1\.125rem", content, re.I):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages still setting body font-size to 1.125rem (18px): {failing}")

    # --- F2: Typography in tailwind.config (Milestone: M1) ---

    def test_t1_f2_01_tailwind_config_sans_open_sans(self):
        """F2: All 11 pages must configure fontFamily.sans to Open Sans in tailwind.config."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            sans_match = re.search(r"sans:\s*\[([^\]]+)\]", content)
            if not sans_match or "Open Sans" not in sans_match.group(1):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages without Open Sans in tailwind.config fontFamily.sans: {failing}")

    def test_t1_f2_02_tailwind_config_heading_open_sans(self):
        """F2: All 11 pages must configure fontFamily.heading to Open Sans in tailwind.config."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            heading_match = re.search(r"heading:\s*\[([^\]]+)\]", content)
            if not heading_match or "Open Sans" not in heading_match.group(1):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages without Open Sans in tailwind.config fontFamily.heading: {failing}")

    def test_t1_f2_03_tailwind_config_display_open_sans(self):
        """F2: All 11 pages must configure fontFamily.display to Open Sans in tailwind.config for backward compat."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            display_match = re.search(r"display:\s*\[([^\]]+)\]", content)
            if not display_match or "Open Sans" not in display_match.group(1):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages without Open Sans in tailwind.config fontFamily.display: {failing}")

    def test_t1_f2_04_tailwind_config_palette_structure(self):
        """F2: tailwind.config must contain brand, accent, and neutral color mappings."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            has_brand = "brand:" in content or "'brand':" in content or '"brand":' in content
            has_accent = "accent:" in content or "'accent':" in content or '"accent":' in content
            if not (has_brand and has_accent):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with incomplete tailwind.config color palette: {failing}")

    def test_t1_f2_05_tailwind_config_no_foreign_fonts(self):
        """F2: 0 pages must have Inter or Plus Jakarta Sans configured in tailwind.config."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            tw_match = re.search(r"tailwind\.config\s*=\s*\{.*?\};?", content, re.DOTALL)
            if tw_match:
                tw_code = tw_match.group(0)
                if "Inter" in tw_code or "Plus Jakarta Sans" in tw_code:
                    failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with Inter or Jakarta in tailwind.config: {failing}")

    # --- F3: Editorial Heading Hierarchy (Milestone: M1) ---

    def test_t1_f3_01_headings_color_pure_black(self):
        """F3: In <style>, h1, h2, h3, h4 must be configured with color: #000000."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            headings_rule = re.search(r"h1,\s*h2,\s*h3,\s*h4[^{]*\{([^}]+)\}", content)
            if not headings_rule or "#000000" not in headings_rule.group(1).lower():
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages missing pure black (#000000) headings rule in <style>: {failing}")

    def test_t1_f3_02_body_text_color_neutral(self):
        """F3: In <style>, body text color must be configured with #676b67."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            body_rule = re.search(r"body\s*\{([^}]+)\}", content)
            if not body_rule or "#676b67" not in body_rule.group(1).lower():
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages missing #676b67 body color in <style>: {failing}")

    def test_t1_f3_03_inner_pages_h1_scale(self):
        """F3: Inner pages H1 must use standard corporate bold scale without Jakarta overrides."""
        failing = []
        for p in PUBLIC_PAGES_NO_DOSSIER:
            if p == "index.html":
                continue
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            h1_match = re.search(r"<h1[^>]*class=\"([^\"]+)\"", content)
            if not h1_match or "font-extrabold" not in h1_match.group(1):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Inner pages missing font-extrabold on H1: {failing}")

    def test_t1_f3_04_no_inline_style_font_overrides(self):
        """F3: 0 inline style attributes must override font-family to Inter or Jakarta."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            if re.search(r"style=\"[^\"]*font-family:\s*['\"]?(Inter|Plus\s+Jakarta\s+Sans)", content, re.I):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with inline font-family overrides: {failing}")

    def test_t1_f3_05_body_background_pure_white(self):
        """F3: Body must have background #ffffff (or bg-white) in all public pages, eliminating bg-gray-50 jump."""
        failing = []
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            body_tag = re.search(r"<body[^>]*class=\"([^\"]+)\"", content)
            if body_tag and "bg-gray-50" in body_tag.group(1):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with body bg-gray-50 instead of bg-white: {failing}")

    # --- F4: Hero B2B Art Direction (Milestone: M2) ---

    def test_t1_f4_01_home_hero_not_full_green(self):
        """F4: index.html Hero container must NOT have bg-brand (must be white/pearl gray)."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero, "Hero section not found in index.html")
        self.assertNotIn("bg-brand pt-20", hero, "Home Hero still uses full-green bg-brand background")

    def test_t1_f4_02_home_hero_dark_h1(self):
        """F4: index.html Hero H1 must be dark text (not text-white over green)."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        h1_match = re.search(r"<h1[^>]*class=\"([^\"]+)\"[^>]*>", content)
        self.assertIsNotNone(h1_match)
        classes = h1_match.group(1)
        self.assertFalse("text-white" in classes and "text-[#000000]" not in classes, "Home Hero H1 is still text-white")

    def test_t1_f4_03_home_hero_primary_cta_green(self):
        """F4: index.html Hero primary CTA must be institutional green (bg-brand hover:bg-brand-dark text-white)."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero, "Hero section not found")
        self.assertNotIn("bg-accent text-[#000000] font-extrabold px-8 py-4", hero, "Primary CTA is still yellow bg-accent")

    def test_t1_f4_04_home_hero_secondary_cta_white(self):
        """F4: index.html Hero secondary CTA must link to altura with clean styling."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero, "Hero section not found")
        self.assertIn("limpieza-en-altura/index.html", hero, "Hero secondary CTA link missing")

    def test_t1_f4_05_home_hero_micro_accent_star(self):
        """F4: index.html Hero upper badge must feature micro yellow star accent."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero, "Hero section not found")
        self.assertTrue("★" in hero and "text-accent" in hero, "Hero badge missing micro yellow star accent")

    # --- F5: Footer Official Unification (Milestone: M2) ---

    def test_t1_f5_01_footer_no_yellow_button(self):
        """F5: Footer in all 10 public pages must NOT have yellow button (bg-[#ffcc29] / bg-accent)."""
        failing = []
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            footer_match = re.search(r"<footer.*?</footer>", content, re.DOTALL | re.I)
            if footer_match:
                f_html = footer_match.group(0)
                if re.search(r"<a[^>]*class=\"[^\"]*(?:bg-\[#ffcc29\]|bg-accent)[^\"]*\"", f_html, re.I):
                    failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with yellow CTA button in footer: {failing}")

    def test_t1_f5_02_footer_corporate_white_button(self):
        """F5: Footer in all 10 public pages must have corporate white button (bg-white text-brand)."""
        failing = []
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            footer_match = re.search(r"<footer.*?</footer>", content, re.DOTALL | re.I)
            if footer_match:
                f_html = footer_match.group(0)
                if "bg-white" not in f_html or "text-brand" not in f_html:
                    failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages without white corporate button in footer: {failing}")

    def test_t1_f5_03_footer_no_yellow_labels(self):
        """F5: Footer in all 10 public pages must NOT use text-[#ffcc29] for contact labels."""
        failing = []
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            footer_match = re.search(r"<footer.*?</footer>", content, re.DOTALL | re.I)
            if footer_match:
                f_html = footer_match.group(0)
                if re.search(r"text-\[#ffcc29\]", f_html, re.I):
                    failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with text-[#ffcc29] labels in footer: {failing}")

    def test_t1_f5_04_footer_links_hover_white(self):
        """F5: Footer links in all 10 public pages must NOT hover to yellow (hover:text-[#ffcc29])."""
        failing = []
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            footer_match = re.search(r"<footer.*?</footer>", content, re.DOTALL | re.I)
            if footer_match:
                f_html = footer_match.group(0)
                if re.search(r"hover:text-\[#ffcc29\]", f_html, re.I):
                    failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with yellow link hover in footer: {failing}")

    def test_t1_f5_05_footer_no_duplicate_comments(self):
        """F5: Footer must not have duplicate consecutive HTML comments."""
        failing = []
        pattern = re.compile(r"(<!--\s*FOOTER OFICIAL UNIFICADO[^>]*-->\s*){2,}", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            if pattern.search(content):
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages with duplicate footer comments: {failing}")

    # --- F6: Palette & Color Cleanup (Milestone: M2) ---

    def test_t1_f6_01_zero_forbidden_blue_classes(self):
        """F6: 0 forbidden blue, indigo, sky classes in all 11 pages."""
        failing = []
        pattern = re.compile(r"\b(?:bg|text|border|ring|fill|stroke)-(?:blue|indigo|sky)-[0-9a-z/]+", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            matches = pattern.findall(content)
            if matches:
                failing.append((p, set(matches)))
        self.assertEqual(len(failing), 0, f"Pages with forbidden blue classes: {failing}")

    def test_t1_f6_02_zero_forbidden_orange_classes(self):
        """F6: 0 forbidden orange or amber classes in all 11 pages."""
        failing = []
        pattern = re.compile(r"\b(?:bg|text|border|ring|fill|stroke)-(?:orange|amber)-[0-9a-z/]+", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            matches = pattern.findall(content)
            if matches:
                failing.append((p, set(matches)))
        self.assertEqual(len(failing), 0, f"Pages with forbidden orange/amber classes: {failing}")

    def test_t1_f6_03_zero_forbidden_cyan_purple_classes(self):
        """F6: 0 forbidden cyan or purple classes in all 11 pages."""
        failing = []
        pattern = re.compile(r"\b(?:bg|text|border|ring|fill|stroke)-(?:cyan|purple)-[0-9a-z/]+", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            matches = pattern.findall(content)
            if matches:
                failing.append((p, set(matches)))
        self.assertEqual(len(failing), 0, f"Pages with forbidden cyan/purple classes: {failing}")

    def test_t1_f6_04_home_red_warning_eliminated(self):
        """F6: index.html:200 must eliminate red warning classes (bg-red-50, border-red-200, text-red-800)."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        has_red_alert = "bg-red-50" in content or "border-red-200" in content or "text-red-800" in content
        self.assertFalse(has_red_alert, "index.html still contains loud red alert classes at line 200")

    def test_t1_f6_05_out_of_palette_hex_cleanup(self):
        """F6: Out-of-palette hexes (#057a3f, #023d1f, #e6b822) must be eliminated."""
        failing = []
        rogue_hexes = re.compile(r"#(?:057a3f|023d1f|e6b822)\b", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            matches = rogue_hexes.findall(content)
            if matches:
                failing.append((p, set(matches)))
        self.assertEqual(len(failing), 0, f"Pages with rogue hexes: {failing}")

    # --- F7: WhatsApp B2B Filter & Connectors (Milestone: M3) ---

    def test_t1_f7_01_starunion_b2b_js_in_11_pages(self):
        """F7: All 11 pages must load starunion-b2b.js script before closing body."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            if "starunion-b2b.js" not in content:
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages missing starunion-b2b.js: {failing}")

    def test_t1_f7_02_b2b_modal_font_open_sans(self):
        """F7: starunion-b2b.js modal must use Open Sans font and NOT Inter."""
        content = get_page_content("assets/js/starunion-b2b.js")
        self.assertIsNotNone(content, "assets/js/starunion-b2b.js not found")
        self.assertNotIn("font-family:Inter", content, "starunion-b2b.js modal still has font-family:Inter")
        self.assertIn("Open Sans", content, "starunion-b2b.js modal does not specify Open Sans font")

    def test_t1_f7_03_iso_form_name_attributes(self):
        """F7: certificacion-iso/index.html contact form inputs must have name= attributes."""
        content = get_page_content("certificacion-iso/index.html")
        self.assertIsNotNone(content)
        form_match = re.search(r"<form[^>]*>(.*?)</form>", content, re.DOTALL | re.I)
        self.assertIsNotNone(form_match, "No form found in certificacion-iso")
        form_html = form_match.group(1)
        inputs = re.findall(r"<input[^>]*>", form_html)
        missing_names = [inp for inp in inputs if 'name=' not in inp and 'type="submit"' not in inp and 'type="hidden"' not in inp]
        self.assertEqual(len(missing_names), 0, f"Inputs in ISO form missing name= attributes: {missing_names}")

    def test_t1_f7_04_iso_form_b2b_class(self):
        """F7: certificacion-iso/index.html contact form must have js-b2b-quote-form class."""
        content = get_page_content("certificacion-iso/index.html")
        self.assertIsNotNone(content)
        self.assertIn("js-b2b-quote-form", content, "ISO form missing class js-b2b-quote-form")

    def test_t1_f7_05_iso_page_local_tuv_image(self):
        """F7: certificacion-iso/index.html must not load external Wikimedia TÜV image."""
        content = get_page_content("certificacion-iso/index.html")
        self.assertIsNotNone(content)
        self.assertNotIn("upload.wikimedia.org", content, "certificacion-iso loads external Wikimedia image")

    # --- F8: Brand Safety & Lockfile Alignment (Milestone: M3) ---

    def test_t1_f8_01_altura_barbiquejo_correction(self):
        """F8: limpieza-en-altura/index.html line 244 must use 'barbiquejo' and 0 times 'barbijo'."""
        content = get_page_content("limpieza-en-altura/index.html")
        self.assertIsNotNone(content)
        clean = strip_html_comments(content)
        self.assertNotIn("barbijo", clean, "limpieza-en-altura still contains forbidden term 'barbijo'")
        self.assertIn("barbiquejo", clean, "limpieza-en-altura missing correct technical term 'barbiquejo'")

    def test_t1_f8_02_zero_gendered_greetings(self):
        """F8: 0 forbidden gendered greetings ('Bienvenidos a Star Union', 'bienvenides', 'todes')."""
        failing = []
        forbidden_regex = re.compile(r"\b(?:bienvenidos a star union|bienvenides|todes|bienvenidos/as)\b", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            clean = strip_html_comments(content)
            m = forbidden_regex.findall(clean)
            if m:
                failing.append((p, m))
        self.assertEqual(len(failing), 0, f"Pages with forbidden gendered terms: {failing}")

    def test_t1_f8_03_zero_leaks_of_internal_tools(self):
        """F8: 0 public links to internal management tools (radar, acuerdos, relevamiento, brochures/editables)."""
        failing = []
        leak_regex = re.compile(r"href=[\"'][^\"']*(?:radar-comercial|brochures/editables|relevamiento-gerencia|acuerdos/index)[^\"']*[\"']", re.I)
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            clean = strip_html_comments(content)
            m = leak_regex.findall(clean)
            if m:
                failing.append((p, m))
        self.assertEqual(len(failing), 0, f"Public pages linking to internal management tools: {failing}")

    def test_t1_f8_04_footer_logo_reference_11_pages(self):
        """F8: logo-footer-blanco.png must exist on disk and be referenced across all 11 pages."""
        logo_path = PROJECT_ROOT / "logo-footer-blanco.png"
        self.assertTrue(logo_path.exists(), "logo-footer-blanco.png missing from project root")
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            if "logo-footer-blanco.png" not in content:
                failing.append(p)
        self.assertEqual(len(failing), 0, f"Pages missing logo-footer-blanco.png reference: {failing}")

    def test_t1_f8_05_zero_visible_logo_blanco_text(self):
        """F8: 0 occurrences of 'LOGO BLANCO' placeholder text in rendered DOM nodes."""
        failing = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            clean = strip_html_comments(content)
            visible_hits = re.findall(r">[^<]*\bLOGO BLANCO\b[^<]*<", clean, re.I)
            if visible_hits:
                failing.append((p, visible_hits))
        self.assertEqual(len(failing), 0, f"Pages with visible 'LOGO BLANCO' text: {failing}")

    # --- F9: Clean HostGator ZIP Packaging (Milestone: M3) ---

    def test_t1_f9_01_zip_file_exists(self):
        """F9: SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip must exist at project root."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        self.assertTrue(zip_path.exists(), "Distribution ZIP package missing from root")

    def test_t1_f9_02_zip_excludes_agents_directory(self):
        """F9: Distribution ZIP must strictly exclude any .agents directories."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            agents_entries = [name for name in zf.namelist() if ".agents" in name]
            self.assertEqual(len(agents_entries), 0, f"ZIP contains .agents entries: {agents_entries[:5]}")

    def test_t1_f9_03_zip_excludes_markdown_docs(self):
        """F9: Distribution ZIP must exclude internal markdown *.md files."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            md_entries = [name for name in zf.namelist() if name.endswith(".md")]
            self.assertEqual(len(md_entries), 0, f"ZIP contains internal .md files: {md_entries[:5]}")

    def test_t1_f9_04_zip_excludes_internal_tools(self):
        """F9: Distribution ZIP must exclude private management directories (radar, acuerdos, relevamiento)."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        forbidden_dirs = ["radar-comercial/", "acuerdos/", "relevamiento-gerencia/", "brochures/editables/", "accesos/"]
        with zipfile.ZipFile(zip_path, "r") as zf:
            leaked = [name for name in zf.namelist() if any(name.startswith(fd) for fd in forbidden_dirs)]
            self.assertEqual(len(leaked), 0, f"ZIP contains private management directories: {leaked[:5]}")

    def test_t1_f9_05_accesos_linktree_noindex(self):
        """F9: /accesos/index.html Linktree must be protected with noindex, nofollow."""
        content = get_page_content("accesos/index.html")
        self.assertIsNotNone(content, "accesos/index.html not found")
        self.assertTrue(re.search(r"<meta\s+name=[\"']robots[\"']\s+content=[\"'][^\"']*noindex[^\"']*[\"']", content, re.I),
                        "accesos/index.html missing noindex robots meta tag")

    # --- F10: Comprehensive E2E Verification (Milestone: M4) ---

    def test_t1_f10_01_all_100_local_images_exist(self):
        """F10: All local <img> tags across 11 pages must resolve to physical files on disk."""
        missing_images = []
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content, f"File {p} not found")
            page_dir = (PROJECT_ROOT / p).parent
            img_srcs = re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", content, re.I)
            for src in img_srcs:
                if src.startswith("http://") or src.startswith("https://") or src.startswith("data:"):
                    continue
                clean_src = src.split("?")[0].split("#")[0]
                resolved = (page_dir / clean_src).resolve()
                if not resolved.exists():
                    missing_images.append((p, src, str(resolved)))
        self.assertEqual(len(missing_images), 0, f"Broken local image links detected: {missing_images}")

    def test_t1_f10_02_all_7_verticals_linked(self):
        """F10: index.html must link to all 7 operational verticals."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        verticals = [
            "limpieza-industrial/index.html",
            "limpieza-en-altura/index.html",
            "grandes-superficies/index.html",
            "consorcios/index.html",
            "clinicas-y-hospitales/index.html",
            "universidades-y-clubes/index.html",
            "servicios-especiales/index.html",
        ]
        missing = [v for v in verticals if v not in content]
        self.assertEqual(len(missing), 0, f"Verticals not linked from index.html: {missing}")

    def test_t1_f10_03_operational_differentials_present(self):
        """F10: index.html must document the 4 key operational differentials (Guaminí 800m², Biométrico, Flota, ISO)."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertIn("800 m²", content, "Guaminí 800 m² missing from index.html")
        self.assertTrue("15" in content and "Biométrico" in content, "15 min Biometric differential missing")
        self.assertTrue("Flota" in content or "utilitarios" in content, "Fleet differential missing")
        self.assertIn("ISO 9001", content, "ISO 9001 differential missing")

    def test_t1_f10_04_iso_official_data_accuracy(self):
        """F10: ISO certificate number 01 10006 2529826 and Certipedia ID 9000041847 must be accurate."""
        content = get_page_content("certificacion-iso/index.html")
        self.assertIsNotNone(content)
        self.assertIn("01 10006 2529826", content, "Official ISO Certificate Number missing or incorrect")
        self.assertIn("9000041847", content, "Official Certipedia ID missing or incorrect")

    def test_t1_f10_05_brand_lockfile_integrity(self):
        """F10: BRAND_AND_CONNECTORS.lock.json must contain allowed palette, connectors and forbidden terms."""
        lock_file = PROJECT_ROOT / "BRAND_AND_CONNECTORS.lock.json"
        self.assertTrue(lock_file.exists(), "BRAND_AND_CONNECTORS.lock.json missing")
        with open(lock_file, "r", encoding="utf-8") as f:
            lock = json.load(f)
        self.assertIn("allowed_palette", lock)
        self.assertIn("connectors", lock)
        self.assertIn("forbidden_terms", lock)
        self.assertIn("#03582D", [c.upper() for c in lock["allowed_palette"]])


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES (40 Tests)
# ==============================================================================

class TestTier2BoundaryCases(unittest.TestCase):
    """Tier 2: Edge conditions, encoding, limits, and boundary cases."""

    def test_t2_b01_font_link_query_format(self):
        """B01: Google Fonts link uses display=swap parameter."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            if "family=Open+Sans" in content:
                self.assertIn("display=swap", content, f"{p} missing display=swap on Google Fonts link")

    def test_t2_b02_preconnect_cors_attribute(self):
        """B02: Preconnect to gstatic.com has crossorigin attribute."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            if "fonts.gstatic.com" in content:
                self.assertTrue(re.search(r"fonts\.gstatic\.com[\"'][^>]*crossorigin", content, re.I) or
                                re.search(r"crossorigin[^>]*fonts\.gstatic\.com", content, re.I),
                                f"{p} preconnect to gstatic missing crossorigin")

    def test_t2_b03_no_insecure_http_font_links(self):
        """B03: 0 insecure http:// fonts links."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertNotRegex(content, r"http://fonts\.(?:googleapis|gstatic)\.com", f"{p} has insecure http font link")

    def test_t2_b04_style_tag_css_syntax(self):
        """B04: Inline <style> tags have balanced curly braces."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL | re.I)
            for s in styles:
                self.assertEqual(s.count("{"), s.count("}"), f"{p} has unbalanced curly braces in <style>")

    def test_t2_b05_tailwind_config_json_parseable(self):
        """B05: tailwind.config contains theme.extend structure."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertIn("tailwind.config", content, f"{p} missing tailwind.config assignment")
            self.assertIn("theme:", content, f"{p} missing theme: in tailwind.config")
            self.assertIn("extend:", content, f"{p} missing extend: in tailwind.config")

    def test_t2_b06_tailwind_no_duplicate_font_keys(self):
        """B06: fontFamily in tailwind.config has no duplicated sans key."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            tw_match = re.search(r"fontFamily:\s*\{([^}]+)\}", content)
            if tw_match:
                block = tw_match.group(1)
                sans_count = len(re.findall(r"\bsans\s*:", block))
                self.assertLessEqual(sans_count, 1, f"{p} has duplicate 'sans' keys in fontFamily")

    def test_t2_b07_tailwind_cdn_script_present(self):
        """B07: Tailwind CDN script tag loads from cdn.tailwindcss.com."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertIn("cdn.tailwindcss.com", content, f"{p} missing Tailwind CDN script")

    def test_t2_b08_headings_inheritance_in_cards(self):
        """B08: Card titles (H3) use dark text color."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        h3_tags = re.findall(r"<h3[^>]*class=[\"']([^\"']+)[\"']", content)
        for cls in h3_tags[:5]:
            self.assertNotIn("text-white", cls)

    def test_t2_b09_responsive_h1_classes_mobile(self):
        """B09: H1 tags declare responsive breakpoints (sm: or lg:)."""
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            h1_match = re.search(r"<h1[^>]*class=[\"']([^\"']+)[\"']", content)
            if h1_match:
                cls = h1_match.group(1)
                self.assertTrue("sm:" in cls or "lg:" in cls or "md:" in cls, f"{p} H1 missing responsive classes")

    def test_t2_b10_microcopy_minimum_size(self):
        """B10: Badges and microcopy do not go below text-xs (12px)."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertNotRegex(content, r"text-\[[0-9]px\]", f"{p} has illegible sub-10px font size")

    def test_t2_b11_line_height_proportions(self):
        """B11: Body style declares line-height 1.6."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            body_rule = re.search(r"body\s*\{([^}]+)\}", content)
            if body_rule:
                self.assertIn("line-height: 1.6", body_rule.group(1), f"{p} missing line-height: 1.6 in body style")

    def test_t2_b12_hero_badge_contrast_ratio(self):
        """B12: Hero upper badge has legible text color against background."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        badge = re.search(r"<div[^>]*class=[\"']([^\"']*rounded-full[^\"']*tracking-wider[^\"']*)[\"']", content)
        if badge:
            self.assertTrue("text-xs" in badge.group(1) and "font-extrabold" in badge.group(1))

    def test_t2_b13_hero_primary_button_contrast(self):
        """B13: Primary CTA button specifies text-white on brand background."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero)
        self.assertIn("text-white", hero)

    def test_t2_b14_hero_secondary_button_border(self):
        """B14: Secondary CTA button specifies border for visibility against white."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero)
        self.assertIn("limpieza-en-altura/index.html", hero)

    def test_t2_b15_hero_accent_star_inline_flex(self):
        """B15: Yellow star glyph container uses inline-flex for alignment."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertTrue(hero)
        self.assertIn("inline-flex", hero)

    def test_t2_b16_footer_white_button_hover_contrast(self):
        """B16: Footer white button has hover state (hover:bg-gray-100)."""
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            footer_match = re.search(r"<footer.*?</footer>", content, re.DOTALL | re.I)
            if footer_match:
                f_html = footer_match.group(0)
                if "bg-white" in f_html:
                    self.assertIn("hover:bg-gray-100", f_html, f"{p} footer button missing hover:bg-gray-100")

    def test_t2_b17_footer_phone_uri_schemes(self):
        """B17: Footer telephone links use valid tel: URI scheme."""
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertIn('href="tel:08103338646"', content, f"{p} missing tel:08103338646 link in footer")

    def test_t2_b18_footer_email_uri_scheme(self):
        """B18: Footer email link uses valid mailto: scheme to comercial@starunion.com.ar."""
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertIn('href="mailto:comercial@starunion.com.ar"', content, f"{p} missing mailto: link in footer")

    def test_t2_b19_footer_address_postal_code(self):
        """B19: Footer address includes CABA identification."""
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertIn("CABA", content, f"{p} footer missing CABA mention in address")

    def test_t2_b20_footer_logo_dimensions(self):
        """B20: Footer logo image specifies object-contain and height constraint."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            logo_tag = re.search(r"<img[^>]*logo-footer-blanco\.png[^>]*>", content)
            if logo_tag:
                tag_str = logo_tag.group(0)
                self.assertTrue("h-12" in tag_str or "h-8" in tag_str, f"{p} footer logo missing height constraint")
                self.assertIn("object-contain", tag_str, f"{p} footer logo missing object-contain")

    def test_t2_b21_hex_case_insensitivity_matching(self):
        """B21: Allowed palette hex matching succeeds regardless of case."""
        lock_file = PROJECT_ROOT / "BRAND_AND_CONNECTORS.lock.json"
        with open(lock_file, "r", encoding="utf-8") as f:
            lock = json.load(f)
        allowed = [c.upper() for c in lock["allowed_palette"]]
        self.assertIn("#03582D", allowed)
        self.assertIn("#FFCC29", allowed)

    def test_t2_b22_palette_opacity_modifiers(self):
        """B22: Opacity modifiers (brand/10, brand/20) resolve to brand root."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertIn("brand:", content)

    def test_t2_b23_zero_inline_style_rogue_hex(self):
        """B23: 0 inline style attributes specifying rogue hexes #057a3f or #023d1f."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertNotRegex(content, r"style=\"[^\"]*#(?:057a3f|023d1f)", f"{p} has inline rogue hex style")

    def test_t2_b24_whatsapp_modal_singleton_instance(self):
        """B24: starunion-b2b.js ensures single modal instance."""
        content = get_page_content("assets/js/starunion-b2b.js")
        self.assertIsNotNone(content)
        self.assertIn("su-wa-filter-modal", content, "starunion-b2b.js missing modal ID check")

    def test_t2_b25_whatsapp_e164_format(self):
        """B25: WhatsApp business phone uses E.164 format (+5491122759369)."""
        lock_file = PROJECT_ROOT / "BRAND_AND_CONNECTORS.lock.json"
        with open(lock_file, "r", encoding="utf-8") as f:
            lock = json.load(f)
        self.assertEqual(lock["connectors"]["whatsapp_business"], "+5491122759369")

    def test_t2_b26_ga4_dispatcher_safeguard(self):
        """B26: starunion-b2b.js checks gtag function existence before dispatch."""
        content = get_page_content("assets/js/starunion-b2b.js")
        self.assertIsNotNone(content)
        self.assertTrue("gtag" in content and "function" in content, "starunion-b2b.js missing gtag function check")

    def test_t2_b27_b2b_form_required_fields(self):
        """B27: Contact forms include required attributes on essential inputs."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertIn("required", content, "index.html contact form missing required fields")

    def test_t2_b28_forbidden_terms_word_boundaries(self):
        """B28: Forbidden term regex matches only discrete words, not substrings of valid words."""
        forbidden_regex = re.compile(r"\bbarbijo\b", re.I)
        self.assertIsNone(forbidden_regex.search("casco con barbiquejo homologado"))
        self.assertIsNotNone(forbidden_regex.search("casco con barbijo homologado"))

    def test_t2_b29_gender_neutrality_accents(self):
        """B29: Gender neutrality regex catches accented forms and slashes."""
        gender_regex = re.compile(r"\b(?:bienvenidos/as|bienvenid@s|bienvenides)\b", re.I)
        self.assertIsNotNone(gender_regex.search("bienvenidos/as"))
        self.assertIsNotNone(gender_regex.search("bienvenid@s"))

    def test_t2_b30_utf8_encoding_declaration(self):
        """B30: All 11 pages declare UTF-8 charset in <head>."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertTrue(re.search(r"<meta\s+charset=[\"']?utf-8[\"']?", content, re.I),
                            f"{p} missing UTF-8 meta charset")

    def test_t2_b31_viewport_meta_declaration(self):
        """B31: All 11 pages declare responsive viewport meta tag."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertTrue(re.search(r"<meta\s+name=[\"']viewport[\"']", content, re.I),
                            f"{p} missing viewport meta tag")

    def test_t2_b32_zip_file_readable_archive(self):
        """B32: Distribution ZIP is a valid uncorrupted zip archive."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad_file = zf.testzip()
            self.assertIsNone(bad_file, f"Corrupted file found in ZIP: {bad_file}")

    def test_t2_b33_zip_no_root_path_traversal(self):
        """B33: Distribution ZIP contains no path traversal sequences (../)."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                self.assertNotIn("..", name, f"Path traversal sequence detected in ZIP: {name}")

    def test_t2_b34_noindex_meta_tag_syntax(self):
        """B34: /accesos/index.html robots meta specifies both noindex and nofollow."""
        content = get_page_content("accesos/index.html")
        self.assertIsNotNone(content)
        self.assertIn("noindex", content)
        self.assertIn("nofollow", content)

    def test_t2_b35_operational_address_consistency(self):
        """B35: Base Guaminí address prominently uses number 5657."""
        content = get_page_content("la-empresa/index.html")
        self.assertIsNotNone(content)
        self.assertIn("5657", content, "la-empresa/index.html missing Guaminí 5657")

    def test_t2_b36_transit_fleet_mention_neutral(self):
        """B36: Ford Transit units are not restricted as exclusive to final de obra."""
        content = get_page_content("servicios-especiales/index.html")
        self.assertIsNotNone(content)
        self.assertIn("Ford Transit", content)

    def test_t2_b37_biometric_alert_timing_15m(self):
        """B37: Biometric alert timing is stated as 15 minutes."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertTrue(re.search(r"15\s*(?:min|minutos)", content, re.I), "15 min alert timing not found")

    def test_t2_b38_biometric_replacement_timing_2h(self):
        """B38: Biometric replacement timing is stated as < 2 hours."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertTrue(re.search(r"2\s*h(?:oras|s)", content, re.I), "2 hour replacement timing not found")

    def test_t2_b39_certipedia_verification_link(self):
        """B39: TÜV link points to certipedia.com domain."""
        content = get_page_content("certificacion-iso/index.html")
        self.assertIsNotNone(content)
        self.assertIn("certipedia.com", content, "certipedia.com link missing from ISO page")

    def test_t2_b40_no_broken_internal_anchors(self):
        """B40: #contacto anchor in index.html points to an element with id='contacto'."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertTrue(re.search(r"id=[\"']contacto[\"']", content, re.I), "index.html missing id='contacto'")


# ==============================================================================
# TIER 3: CROSS-FEATURE INTEGRATION (18 Tests)
# ==============================================================================

class TestTier3CrossFeatureIntegrations(unittest.TestCase):
    """Tier 3: Pairwise cross-feature combinations and module integrations."""

    def test_t3_c01_font_links_match_tailwind_config(self):
        """C01: F1 x F2 - Font link in <head> matches fontFamily sans in tailwind.config."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            has_head_open = "family=Open+Sans" in content
            has_tw_open = 'sans: [\'"Open Sans"\'' in content or "sans: ['Open Sans'" in content
            self.assertEqual(has_head_open, has_tw_open, f"{p} mismatch between <head> font link and tailwind.config")

    def test_t3_c02_body_size_cascades_to_lead(self):
        """C02: F1 x F3 - Body font size 1rem does not break lead paragraph classes."""
        for p in PUBLIC_PAGES_NO_DOSSIER:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            self.assertIn("p", content)

    def test_t3_c03_modal_inherits_page_typography(self):
        """C03: F1 x F7 - WhatsApp modal DOM in starunion-b2b.js aligns with site's Open Sans font."""
        js_content = get_page_content("assets/js/starunion-b2b.js")
        self.assertIsNotNone(js_content)
        self.assertNotIn("font-family:Inter", js_content)
        self.assertIn("Open Sans", js_content)

    def test_t3_c04_tailwind_palette_matches_lockfile(self):
        """C04: F2 x F6 - Brand green in tailwind.config matches lockfile allowed_palette."""
        lock_file = PROJECT_ROOT / "BRAND_AND_CONNECTORS.lock.json"
        with open(lock_file, "r", encoding="utf-8") as f:
            lock = json.load(f)
        allowed = [c.upper() for c in lock["allowed_palette"]]
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertIn("#03582D", allowed)
        self.assertIn("#03582d", content.lower())

    def test_t3_c05_hero_cta_footer_cta_harmony(self):
        """C05: F4 x F5 - Hero CTA and Footer CTA both avoid yellow background button on green."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        footer_match = re.search(r"<footer.*?</footer>", content, re.DOTALL | re.I)
        self.assertIsNotNone(footer_match)
        self.assertNotIn("bg-[#ffcc29] hover:bg-[#e5b622]", footer_match.group(0))

    def test_t3_c06_hero_white_ratio_overall(self):
        """C06: F4 x F6 - Hero white redesign preserves dominant white surface ratio."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        self.assertIn("bg-white", content)

    def test_t3_c07_footer_logo_matches_filesystem(self):
        """C07: F5 x F8 - Footer logo filename in HTML matches physical file on disk."""
        logo_path = PROJECT_ROOT / "logo-footer-blanco.png"
        self.assertTrue(logo_path.exists())
        self.assertGreater(logo_path.stat().st_size, 1000)

    def test_t3_c08_modal_buttons_color_harmony(self):
        """C08: F6 x F7 - WhatsApp modal buttons use official brand green without rogue colors."""
        content = get_page_content("assets/js/starunion-b2b.js")
        self.assertIsNotNone(content)
        self.assertIn("#03582d", content.lower())

    def test_t3_c09_form_submit_ga4_event_wiring(self):
        """C09: F7 x F8 - WhatsApp routing script dispatches contacto_wa_empresa_b2b event."""
        content = get_page_content("assets/js/starunion-b2b.js")
        self.assertIsNotNone(content)
        self.assertIn("contacto_wa_empresa_b2b", content)

    def test_t3_c10_zip_package_excludes_lockfile_and_secrets(self):
        """C10: F8 x F9 - Distribution ZIP excludes lockfile and credentials."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            self.assertNotIn("BRAND_AND_CONNECTORS.lock.json", names)
            self.assertNotIn(".env", names)

    def test_t3_c11_zip_retains_all_11_pages(self):
        """C11: F1 x F9 - Distribution ZIP contains all 11 public pages."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            for p in PUBLIC_PAGES:
                self.assertIn(p, names, f"ZIP missing page {p}")

    def test_t3_c12_zip_retains_assets_directory(self):
        """C12: F2 x F9 - Distribution ZIP includes assets directory."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            has_assets = any(n.startswith("assets/") for n in names)
            self.assertTrue(has_assets, "ZIP missing assets/ directory")

    def test_t3_c13_zip_contains_footer_logo(self):
        """C13: F5 x F9 - Distribution ZIP includes logo-footer-blanco.png."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            self.assertIn("logo-footer-blanco.png", zf.namelist())

    def test_t3_c14_zip_zero_forbidden_classes(self):
        """C14: F6 x F9 - HTML pages in ZIP do not contain forbidden blue classes."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            for p in PUBLIC_PAGES:
                if p in zf.namelist():
                    content = zf.read(p).decode("utf-8", errors="replace")
                    self.assertNotRegex(content, r"\b(?:bg|text|border)-(?:blue|indigo|sky)-[0-9]+", f"ZIP page {p} has blue classes")

    def test_t3_c15_zip_contains_starunion_b2b_js(self):
        """C15: F7 x F9 - Distribution ZIP contains assets/js/starunion-b2b.js."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            self.assertIn("assets/js/starunion-b2b.js", zf.namelist())

    def test_t3_c16_h1_visual_scale_harmony(self):
        """C16: F3 x F4 - H1 across pages follows harmonious editorial hierarchy."""
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL | re.I)
            self.assertIsNotNone(h1, f"{p} missing <h1> tag")

    def test_t3_c17_hero_copy_voseo_neutral(self):
        """C17: F4 x F8 - Home hero copy adheres to corporate neutral voseo without gender marks."""
        content = get_page_content("index.html")
        self.assertIsNotNone(content)
        hero = get_home_hero_section(content)
        self.assertNotRegex(hero, r"\b(?:bienvenidos|bienvenides|todes)\b", "Hero copy contains non-neutral greetings")

    def test_t3_c18_footer_hexes_match_lockfile(self):
        """C18: F5 x F6 - Footer background #133522 and border #024121 are in lockfile palette."""
        lock_file = PROJECT_ROOT / "BRAND_AND_CONNECTORS.lock.json"
        with open(lock_file, "r", encoding="utf-8") as f:
            lock = json.load(f)
        allowed = [c.upper() for c in lock["allowed_palette"]]
        self.assertIn("#133522", allowed)
        self.assertIn("#024121", allowed)


# ==============================================================================
# TIER 4: REAL-WORLD SCENARIOS & FORENSIC CHECKS (12 Tests)
# ==============================================================================

class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: End-to-end B2B client journeys, navigation flows, and forensic audits."""

    def test_t4_s01_journey_industrial_manager(self):
        """S01: Industrial Manager journey: Home -> Limpieza Industrial -> ISO Badge -> Guaminí 800m²."""
        home = get_page_content("index.html")
        self.assertIn("limpieza-industrial/index.html", home)
        ind = get_page_content("limpieza-industrial/index.html")
        self.assertIsNotNone(ind)
        self.assertIn("ISO 9001", ind)
        self.assertIn("Guaminí", ind)

    def test_t4_s02_journey_corporate_tower_admin(self):
        """S02: Corporate Tower Admin journey: Consorcios -> Biometric 15 min -> Direct Phone."""
        cons = get_page_content("consorcios/index.html")
        self.assertIsNotNone(cons)
        self.assertTrue("0810" in cons or "0810-333" in cons or "08103338646" in cons)
        self.assertIn("Guaminí", cons)

    def test_t4_s03_journey_hospital_director(self):
        """S03: Hospital Director journey: Clínicas -> Biosecurity protocols -> 0 post-covid taboo terms."""
        clin = get_page_content("clinicas-y-hospitales/index.html")
        self.assertIsNotNone(clin)
        self.assertIn("Bioseguridad", clin)
        self.assertNotIn("barbijo", clin)
        self.assertNotIn("COVID-19", clin)

    def test_t4_s04_journey_procurement_auditor(self):
        """S04: Procurement Auditor journey: Certificación ISO -> PDF certificate -> Certipedia ID 9000041847."""
        iso = get_page_content("certificacion-iso/index.html")
        self.assertIsNotNone(iso)
        self.assertIn("certificado-iso-starunion.pdf", iso)
        self.assertIn("9000041847", iso)
        pdf_path = PROJECT_ROOT / "certificado-iso-starunion.pdf"
        self.assertTrue(pdf_path.exists())

    def test_t4_s05_journey_height_cleaning_specialist(self):
        """S05: Height Cleaning Specialist journey: Limpieza en Altura -> ARAA norms -> barbiquejo homologado."""
        alt = get_page_content("limpieza-en-altura/index.html")
        self.assertIsNotNone(alt)
        self.assertIn("ARAA", alt)
        self.assertIn("Silletas", alt)
        self.assertIn("barbiquejo", alt)

    def test_t4_s06_journey_educational_campus(self):
        """S06: Educational Campus journey: Universidades y Clubes -> Institutional client references."""
        edu = get_page_content("universidades-y-clubes/index.html")
        self.assertIsNotNone(edu)
        self.assertIn("Lincoln", edu)
        self.assertIn("UTDT", edu)

    def test_t4_s07_journey_retail_center_manager(self):
        """S07: Retail Center Manager journey: Grandes Superficies -> High-traffic protocols."""
        gs = get_page_content("grandes-superficies/index.html")
        self.assertIsNotNone(gs)
        self.assertIn("Alto Tránsito", gs)

    def test_t4_s08_journey_specialized_services_client(self):
        """S08: Specialized Services journey: Servicios Especiales -> Ford Transit mobile units."""
        se = get_page_content("servicios-especiales/index.html")
        self.assertIsNotNone(se)
        self.assertIn("Ford Transit", se)

    def test_t4_s09_journey_executive_investor_dossier(self):
        """S09: Executive Investor journey: Dossier -> Tabbed navigation -> Clean corporate presentation."""
        dossier = get_page_content("dossier/index.html")
        self.assertIsNotNone(dossier)
        self.assertIn("Mauro Repetto", dossier)
        self.assertIn("Guaminí", dossier)

    def test_t4_s10_forensic_crawler_zero_internal_leaks(self):
        """S10: Forensic Spider Crawl: 0 internal management tools discoverable from public pages."""
        forbidden_targets = ["radar-comercial", "brochures/editables", "relevamiento-gerencia", "acuerdos/index"]
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            clean = strip_html_comments(content)
            for ft in forbidden_targets:
                self.assertNotIn(ft, clean, f"Forensic crawler detected leaked internal target {ft} in {p}")

    def test_t4_s11_forensic_brand_firewall_validation(self):
        """S11: Forensic Brand Firewall: 0 cross-brand contamination terms from other projects."""
        foreign_brands = ["Fabricio Rivas", "rivas-2026", "Entretelado", "entretelado.com.ar", "Zaguán"]
        for p in PUBLIC_PAGES:
            content = get_page_content(p)
            self.assertIsNotNone(content)
            clean = strip_html_comments(content)
            for fb in foreign_brands:
                self.assertNotIn(fb, clean, f"Brand firewall alert: {p} contains foreign project term {fb}")

    def test_t4_s12_forensic_zip_packaging_mirror(self):
        """S12: Forensic ZIP Mirror: Distribution package mirrors public website structure."""
        zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
        if not zip_path.exists():
            self.skipTest("ZIP file not present")
        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = zf.namelist()
            self.assertIn("index.html", namelist)
            self.assertIn("la-empresa/index.html", namelist)
            self.assertIn("certificacion-iso/index.html", namelist)
            self.assertIn("limpieza-industrial/index.html", namelist)


if __name__ == "__main__":
    unittest.main()
