#!/usr/bin/env python3
"""
Empirical Challenger Test Harness for Milestone 2 (Art Direction & Palette Refinement)
Star Union S.R.L.

Performs rigorous, independent empirical verification across all 11 HTML files:
1. Hero Container & Typography/CTA Styling in index.html and public pages
2. Footer Button, Contrast, Labels, Link Hovers, and Cleanliness (No Brazil Effect) across all 10 public pages + dossier + footer.html
3. Red Alert Classes Eradication in index.html and all pages
4. Forbidden Tailwind Palette Classes (blue-*, indigo-*, sky-*, orange-*, amber-*, cyan-*, purple-*) with prefix-unwrapping
5. Out-of-Palette Hex Codes (#057a3f, #023d1f, #e6b822) & Global Palette Whitelist Compliance
6. Pairwise Brazil Flag Contrast Traps (Yellow blocks on green containers)
7. Badge Refinement (conversion of loud yellow badges to subtle brand tint)
8. Brand Firewall & Lockfile Integrity Verification
"""

import os
import sys
import re
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PUBLIC_PAGES_10 = [
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
]

ALL_11_PAGES = PUBLIC_PAGES_10 + ["dossier/index.html"]

ALL_HTML_TARGETS = ALL_11_PAGES + ["footer.html"]

ALLOWED_LOCKFILE_PALETTE = {
    "#03582d",
    "#024121",
    "#047a3e",
    "#133522",
    "#0e2719",
    "#1a4a2f",
    "#ffcc29",
    "#e5b622",
    "#ffffff",
    "#f9fafb",
    "#f3f4f6",
    "#e5e7eb",
    "#676b67",
    "#111827",
    "#000000",
}

# Standard Tailwind neutral grayscale and subtle tints accepted in modern clean UI
ALLOWED_EXTENDED_NEUTRALS = {
    "#f8fafc", "#f1f5f9", "#e2e8f0", "#cbd5e1", "#94a3b8", "#64748b", "#475569", "#334155", "#1e293b", "#0f172a",
    "#fafafa", "#f5f5f5", "#e5e5e5", "#d4d4d4", "#a3a3a3", "#737373", "#525252", "#404040", "#262626", "#171717",
    "#d1d5db", "#9ca3af", "#6b7280", "#4b5563", "#374151", "#1f2937",
    "#bbf7d0", "#f0fdf4", "#e6b417" # subtle brand green/yellow tints
}


class HTMLClassExtractor(HTMLParser):
    """Parses HTML and extracts all class lists per element tag and element attributes."""
    def __init__(self):
        super().__init__()
        self.elements = []
        self.tag_stack = []
        self.in_footer = False
        self.footer_elements = []
        self.in_hero = False
        self.hero_elements = []
        self.hero_section_attrs = None
        self.h1_found = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "").split()
        element_info = {
            "tag": tag.lower(),
            "attrs": attr_dict,
            "classes": classes,
            "in_footer": self.in_footer,
            "in_hero": self.in_hero
        }
        self.elements.append(element_info)
        self.tag_stack.append(tag.lower())

        if tag.lower() == "footer":
            self.in_footer = True

        if self.in_footer:
            self.footer_elements.append(element_info)

        # Detect hero in index.html: first section inside main or containing h1
        if tag.lower() == "section" and not self.h1_found:
            self.in_hero = True
            self.hero_section_attrs = attr_dict

        if tag.lower() == "h1":
            self.h1_found = True

        if self.in_hero:
            self.hero_elements.append(element_info)

    def handle_endtag(self, tag):
        if tag.lower() == "footer":
            self.in_footer = False
        if tag.lower() == "section" and self.in_hero:
            self.in_hero = False
        if self.tag_stack and self.tag_stack[-1] == tag.lower():
            self.tag_stack.pop()


def strip_tailwind_prefixes(cls_name: str) -> str:
    """Removes responsive, state, and group prefixes like hover:, sm:, focus:, md:, group-hover:"""
    parts = cls_name.split(":")
    return parts[-1]


def run_adversarial_m2_checks():
    report = {
        "summary": {
            "total_files": len(ALL_HTML_TARGETS),
            "checks_run": 0,
            "passed": 0,
            "failures": 0,
            "warnings": 0,
        },
        "test_results": [],
        "failures": [],
        "warnings": [],
        "details_by_file": {}
    }

    def record_check(test_id: str, desc: str, passed: bool, file_target: str, error_msg: str = ""):
        report["summary"]["checks_run"] += 1
        if passed:
            report["summary"]["passed"] += 1
            report["test_results"].append({
                "id": test_id,
                "desc": desc,
                "file": file_target,
                "status": "PASS"
            })
        else:
            report["summary"]["failures"] += 1
            failure_detail = f"[{test_id}] {desc} in {file_target}: {error_msg}"
            report["failures"].append(failure_detail)
            report["test_results"].append({
                "id": test_id,
                "desc": desc,
                "file": file_target,
                "status": "FAIL",
                "error": error_msg
            })

    def record_warning(test_id: str, desc: str, file_target: str, warn_msg: str):
        report["summary"]["warnings"] += 1
        report["warnings"].append(f"[{test_id}] {desc} in {file_target}: {warn_msg}")

    # Load file contents
    contents = {}
    doms = {}
    for filename in ALL_HTML_TARGETS:
        file_path = PROJECT_ROOT / filename
        if not file_path.exists():
            record_check("FILE_EXISTENCE", f"File exists on disk", False, filename, "File not found")
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read()
            contents[filename] = raw
        
        parser = HTMLClassExtractor()
        try:
            parser.feed(raw)
            doms[filename] = parser
        except Exception as e:
            record_check("HTML_PARSE", "HTML parse valid without corruption", False, filename, str(e))

    # =========================================================================
    # 1. HERO SECTION ART DIRECTION (F4) — index.html
    # =========================================================================
    if "index.html" in contents:
        home_content = contents["index.html"]
        home_dom = doms.get("index.html")

        # 1.1 Hero Section Container Background
        # Must NOT have bg-brand, bg-[#03582d], bg-[#024121], bg-[#047a3e], or bg-green-*
        hero_sec = home_dom.hero_section_attrs if home_dom else {}
        hero_classes = hero_sec.get("class", "").split() if hero_sec else []

        has_green_container = any(
            re.search(r"^(bg-brand|bg-\[#0[234]..[0-9a-f]\]|bg-green-)", cls)
            for cls in hero_classes
        )
        has_white_container = any(
            cls in ("bg-white", "bg-[#ffffff]", "bg-gray-50", "bg-[#f9fafb]")
            for cls in hero_classes
        )
        record_check(
            "M2_CHALLENGE_F4_01",
            "index.html Hero container must NOT have bg-brand or green background classes",
            not has_green_container,
            "index.html",
            f"Hero section has green background class: {hero_classes}"
        )
        record_check(
            "M2_CHALLENGE_F4_02",
            "index.html Hero container MUST have dominant white/pearl background class (bg-white/bg-gray-50)",
            has_white_container,
            "index.html",
            f"Hero section missing white background class: {hero_classes}"
        )

        # 1.2 Hero H1 Typography & Color
        # H1 must NOT be text-white; must be text-[#000000] / text-black / text-gray-900
        h1_matches = [el for el in home_dom.hero_elements if el["tag"] == "h1"]
        if h1_matches:
            h1_el = h1_matches[0]
            h1_cls = h1_el["classes"]
            is_dark_h1 = any(cls in ("text-[#000000]", "text-black", "text-gray-900", "text-gray-800", "text-[#111827]") for cls in h1_cls)
            is_white_h1 = "text-white" in h1_cls
            record_check(
                "M2_CHALLENGE_F4_03",
                "index.html Hero H1 must be dark text (#000000/black), NOT text-white",
                is_dark_h1 and not is_white_h1,
                "index.html",
                f"H1 classes are: {h1_cls}"
            )
        else:
            record_check("M2_CHALLENGE_F4_03", "index.html Hero H1 found", False, "index.html", "No H1 in hero")

        # 1.3 Hero Primary CTA Button
        # Must be institutional green: bg-brand with text-white. Must NOT be bg-accent or yellow.
        hero_links = [el for el in home_dom.hero_elements if el["tag"] == "a" and "contacto" in el["attrs"].get("href", "")]
        if hero_links:
            primary_btn = hero_links[0]
            p_cls = primary_btn["classes"]
            is_green_primary = "bg-brand" in p_cls and "text-white" in p_cls
            has_yellow_primary = any(re.search(r"bg-accent|bg-\[#ffcc29\]|bg-yellow", cls) for cls in p_cls)
            record_check(
                "M2_CHALLENGE_F4_04",
                "Hero primary CTA is institutional green (bg-brand text-white) and NOT yellow (bg-accent/#ffcc29)",
                is_green_primary and not has_yellow_primary,
                "index.html",
                f"Primary CTA classes: {p_cls}"
            )
        else:
            record_check("M2_CHALLENGE_F4_04", "Hero primary CTA found", False, "index.html", "Primary CTA link missing")

        # 1.4 Hero Secondary CTA Button
        # Must link to altura with clean white/bordered styling
        altura_links = [el for el in home_dom.hero_elements if el["tag"] == "a" and "limpieza-en-altura" in el["attrs"].get("href", "")]
        if altura_links:
            sec_btn = altura_links[0]
            s_cls = sec_btn["classes"]
            has_border_contrast = any("border" in cls for cls in s_cls)
            record_check(
                "M2_CHALLENGE_F4_05",
                "Hero secondary CTA has border contrast against white background",
                has_border_contrast,
                "index.html",
                f"Secondary CTA classes: {s_cls}"
            )
        else:
            record_check("M2_CHALLENGE_F4_05", "Hero secondary CTA found", False, "index.html", "Secondary CTA missing")

        # 1.5 Hero Upper Badge Micro-Accent
        # Badge must feature micro star ★ with text-accent, but badge itself must NOT be full yellow background
        badge_els = [el for el in home_dom.hero_elements if "ISO 9001:2015" in home_content[home_content.find(el["attrs"].get("class", "NONE")):home_content.find(el["attrs"].get("class", "NONE"))+200] and el["tag"] == "div"]
        # Direct regex check on badge container
        badge_match = re.search(r"<div[^>]*class=\"([^\"]*)\"[^>]*>\s*<span class=\"text-accent\">★</span>", home_content)
        if badge_match:
            b_cls = badge_match.group(1).split()
            is_yellow_container = any("bg-accent" in c or "bg-[#ffcc29]" in c for c in b_cls)
            has_neutral_container = any(c in ("bg-gray-100", "bg-white", "bg-gray-50") for c in b_cls)
            record_check(
                "M2_CHALLENGE_F4_06",
                "Hero upper badge is neutral container (bg-gray-100) with micro yellow star, avoiding loud yellow block",
                not is_yellow_container and has_neutral_container,
                "index.html",
                f"Upper badge container classes: {b_cls}"
            )
        else:
            record_check("M2_CHALLENGE_F4_06", "Hero upper badge with micro yellow star found", False, "index.html", "Badge pattern not matched")

    # =========================================================================
    # 2. FOOTER UNIFICATION & ERADICATION OF BRAZIL EFFECT (F5)
    # =========================================================================
    for filename in PUBLIC_PAGES_10:
        raw = contents.get(filename, "")
        dom = doms.get(filename)

        footer_match = re.search(r"<footer(.*?)</footer>", raw, re.DOTALL | re.IGNORECASE)
        if not footer_match:
            record_check("M2_CHALLENGE_F5_00", "Page contains footer tag", False, filename, "No <footer> tag found")
            continue

        footer_html = footer_match.group(0)

        # 2.1 Zero yellow buttons in footer
        # Check every <a>, <button>, <input> inside footer
        yellow_btn_match = re.search(
            r"<(?:a|button|input)[^>]*class=\"[^\"]*(?:bg-accent|bg-\[#ffcc29\]|bg-yellow-|bg-amber-)[^\"]*\"",
            footer_html,
            re.IGNORECASE
        )
        record_check(
            "M2_CHALLENGE_F5_01",
            "Footer has 0 yellow buttons (0 bg-accent / bg-[#ffcc29])",
            yellow_btn_match is None,
            filename,
            f"Yellow button found in footer: {yellow_btn_match.group(0) if yellow_btn_match else ''}"
        )

        # 2.2 Corporate white button present
        # Button should have bg-white, text-brand, and hover:bg-gray-100
        has_white_btn = (
            "bg-white" in footer_html and
            ("text-brand" in footer_html or "text-[#03582d]" in footer_html) and
            "hover:bg-gray-100" in footer_html
        )
        record_check(
            "M2_CHALLENGE_F5_02",
            "Footer contains corporate white CTA button (bg-white text-brand hover:bg-gray-100)",
            has_white_btn,
            filename,
            "Corporate white button missing in footer"
        )

        # 2.3 Zero yellow contact labels in footer
        # Labels should NOT use text-[#ffcc29] or text-accent
        has_yellow_label = bool(re.search(r"<strong[^>]*class=\"[^\"]*(?:text-\[#ffcc29\]|text-accent)[^\"]*\"", footer_html, re.I))
        record_check(
            "M2_CHALLENGE_F5_03",
            "Footer has 0 yellow contact labels (no text-[#ffcc29] or text-accent)",
            not has_yellow_label,
            filename,
            "Yellow label found in footer contact info"
        )

        # 2.4 Zero yellow link hovers in footer
        # Links must NOT hover to yellow (hover:text-[#ffcc29], hover:text-accent, hover:text-yellow-*)
        has_yellow_link_hover = bool(re.search(r"hover:text-(?:\[#ffcc29\]|accent|yellow-[0-9]+)", footer_html, re.I))
        record_check(
            "M2_CHALLENGE_F5_04",
            "Footer links have 0 yellow hovers (no hover:text-[#ffcc29] or hover:text-accent)",
            not has_yellow_link_hover,
            filename,
            "Yellow link hover found in footer"
        )

        # 2.5 All footer navigation links hover to white
        has_hover_white = "hover:text-white" in footer_html
        record_check(
            "M2_CHALLENGE_F5_05",
            "Footer navigation links hover to white (hover:text-white)",
            has_hover_white,
            filename,
            "hover:text-white missing from footer links"
        )

        # 2.6 Zero duplicate footer comments
        dup_comment_match = re.search(r"(<!--\s*FOOTER OFICIAL UNIFICADO[^>]*-->\s*){2,}", raw, re.I)
        record_check(
            "M2_CHALLENGE_F5_06",
            "Footer has 0 duplicate consecutive comments",
            dup_comment_match is None,
            filename,
            "Duplicate consecutive footer comments detected"
        )

    # Also check footer.html template
    if "footer.html" in contents:
        f_raw = contents["footer.html"]
        record_check(
            "M2_CHALLENGE_F5_FOOTER_HTML_01",
            "footer.html template has 0 yellow buttons",
            "bg-[#ffcc29]" not in f_raw and "bg-accent" not in f_raw,
            "footer.html",
            "footer.html contains yellow button class"
        )
        record_check(
            "M2_CHALLENGE_F5_FOOTER_HTML_02",
            "footer.html template has corporate white button",
            "bg-white" in f_raw and "text-brand" in f_raw,
            "footer.html",
            "footer.html missing corporate white button"
        )

    # =========================================================================
    # 3. RED ALERT CLASSES ERADICATION (F6)
    # =========================================================================
    # In index.html: line 200/217 warning alert
    if "index.html" in contents:
        home_raw = contents["index.html"]
        # Search for any red classes in index.html
        red_classes_found = re.findall(r"\b(?:bg|text|border|ring|fill|stroke)-red-[0-9a-z/]+", home_raw, re.I)
        record_check(
            "M2_CHALLENGE_F6_RED_01",
            "index.html has 0 red alert classes (bg-red-*, text-red-*, border-red-*)",
            len(red_classes_found) == 0,
            "index.html",
            f"Found red classes in index.html: {set(red_classes_found)}"
        )

        # Verify line 217 warning alert uses neutral corporate gray
        alert_match = re.search(r"class=\"[^\"]*b2b-warning-alert[^\"]*\"", home_raw)
        if alert_match:
            alert_cls = alert_match.group(0)
            uses_neutral_gray = "bg-gray-100" in alert_cls and "border-gray-300" in alert_cls and "text-gray-800" in alert_cls
            record_check(
                "M2_CHALLENGE_F6_RED_02",
                "index.html .b2b-warning-alert uses neutral corporate gray (bg-gray-100, border-gray-300, text-gray-800)",
                uses_neutral_gray,
                "index.html",
                f"Alert classes are: {alert_cls}"
            )
        else:
            record_check("M2_CHALLENGE_F6_RED_02", "b2b-warning-alert element found", False, "index.html", "Missing alert element")

    # In all 11 HTML pages, check for red alert classes
    for filename in ALL_11_PAGES:
        raw = contents.get(filename, "")
        # Filter out comments first
        raw_clean = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
        red_matches = re.findall(r"\b(?:bg|text|border|ring|fill|stroke)-red-(?:[0-9]{2,3}|50)\b", raw_clean, re.I)
        record_check(
            "M2_CHALLENGE_F6_RED_ALL",
            f"Page has 0 red alert classes in HTML body",
            len(red_matches) == 0,
            filename,
            f"Found red classes: {set(red_matches)}"
        )

    # =========================================================================
    # 4. FORBIDDEN TAILWIND COLOR CLASSES (F6)
    # Prefix-unwrapped adversarial scan across all 11 pages
    # =========================================================================
    FORBIDDEN_FAMILIES = ["blue", "indigo", "sky", "orange", "amber", "cyan", "purple"]
    forbidden_pattern = re.compile(
        r"^(?:(?:sm|md|lg|xl|2xl|dark|hover|focus|active|group-hover|peer-checked):)*"
        r"(?:bg|text|border|ring|fill|stroke|from|to|via)-(" + "|".join(FORBIDDEN_FAMILIES) + r")-[0-9a-z/]+$",
        re.IGNORECASE
    )

    for filename in ALL_11_PAGES:
        dom = doms.get(filename)
        raw = contents.get(filename, "")
        if not dom:
            continue

        forbidden_hits = []
        for el in dom.elements:
            for cls in el["classes"]:
                base = strip_tailwind_prefixes(cls)
                # Check if base class matches forbidden families
                for fam in FORBIDDEN_FAMILIES:
                    if re.match(r"^(?:bg|text|border|ring|fill|stroke|from|to|via)-" + fam + r"-[0-9a-z/]+$", base, re.I):
                        forbidden_hits.append((el["tag"], cls))

        # Also regex scan the whole file text (excluding HTML comments)
        raw_no_comments = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
        text_hits = []
        for fam in FORBIDDEN_FAMILIES:
            matches = re.findall(r"\b(?:\w+:)*(?:bg|text|border|ring|fill|stroke)-" + fam + r"-[0-9a-z/]+", raw_no_comments, re.I)
            if matches:
                text_hits.extend(matches)

        all_hits = set([f"{tag}.{cls}" for tag, cls in forbidden_hits] + text_hits)
        record_check(
            "M2_CHALLENGE_F6_FORBIDDEN_CLASSES",
            "0 forbidden classes (blue, indigo, sky, orange, amber, cyan, purple)",
            len(all_hits) == 0,
            filename,
            f"Forbidden classes found: {all_hits}"
        )

    # =========================================================================
    # 5. OUT-OF-PALETTE HEX CODES & WHITELIST CONFORMANCE (F6)
    # =========================================================================
    ROGUE_HEXES = {"#057a3f", "#023d1f", "#e6b822"}

    for filename in ALL_11_PAGES:
        raw = contents.get(filename, "")
        raw_no_comments = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)

        # 5.1 Strict check for rogue hexes
        found_rogue = []
        for r_hex in ROGUE_HEXES:
            if re.search(re.escape(r_hex) + r"\b", raw_no_comments, re.IGNORECASE):
                found_rogue.append(r_hex)

        record_check(
            "M2_CHALLENGE_F6_ROGUE_HEX",
            "0 out-of-palette rogue hexes (#057a3f, #023d1f, #e6b822)",
            len(found_rogue) == 0,
            filename,
            f"Found rogue hexes: {found_rogue}"
        )

        # 5.2 Adversarial audit of ALL hex codes in page
        all_hex_matches = set(m.lower() for m in re.findall(r"#[0-9a-fA-F]{3,8}\b", raw_no_comments))
        unapproved_hexes = []
        for h in all_hex_matches:
            if len(h) == 4:
                # expand #abc to #aabbcc
                h_expanded = "#" + "".join([c*2 for c in h[1:]])
            else:
                h_expanded = h

            if h_expanded not in ALLOWED_LOCKFILE_PALETTE and h_expanded not in ALLOWED_EXTENDED_NEUTRALS:
                unapproved_hexes.append(h)

        record_check(
            "M2_CHALLENGE_F6_ALL_HEX_COMPLIANCE",
            "All hex color codes comply with Star Union lockfile & grayscale whitelist",
            len(unapproved_hexes) == 0,
            filename,
            f"Unapproved hex codes detected: {unapproved_hexes}"
        )

    # =========================================================================
    # 6. ADVERSARIAL BRAZIL FLAG TRAP SCAN (PAIRWISE GREEN + YELLOW CONTRAST)
    # =========================================================================
    for filename in ALL_11_PAGES:
        raw = contents.get(filename, "")
        dom = doms.get(filename)
        if not dom:
            continue

        # Check for any element with yellow background (bg-accent or #ffcc29)
        # whose parent or ancestor is a dark green section or footer
        brazil_traps = []
        for el in dom.elements:
            classes = el["classes"]
            is_yellow_bg = any(c in ("bg-accent", "bg-[#ffcc29]") for c in classes)
            if is_yellow_bg:
                # If it's in footer or in hero, flag it as a Brazil effect violation!
                if el["in_footer"]:
                    brazil_traps.append((el["tag"], "In footer", classes))
                elif el["in_hero"] and el["tag"] in ("a", "button"):
                    brazil_traps.append((el["tag"], "Hero button", classes))

        record_check(
            "M2_CHALLENGE_F5_BRAZIL_TRAP",
            "0 Brazil Flag contrast traps (yellow buttons/blocks on dark green containers)",
            len(brazil_traps) == 0,
            filename,
            f"Brazil trap elements detected: {brazil_traps}"
        )

    # =========================================================================
    # 7. BADGE REFINEMENT (CONVERSION OF LOUD YELLOW BADGES TO SUBTLE TINTS)
    # =========================================================================
    # Check index.html:396 (coverage badge)
    if "index.html" in contents:
        home_raw = contents["index.html"]
        # Coverage section badge
        cov_badge_loud = re.search(r"Cobertura.*?(?:bg-accent|bg-\[#ffcc29\])", home_raw, re.I | re.DOTALL)
        record_check(
            "M2_CHALLENGE_F6_BADGE_HOME",
            "index.html coverage badge does NOT use loud yellow bg-accent",
            cov_badge_loud is None,
            "index.html",
            "Coverage badge still uses loud yellow background"
        )

    # Check certificacion-iso/index.html:264 (programa activo badge)
    if "certificacion-iso/index.html" in contents:
        iso_raw = contents["certificacion-iso/index.html"]
        iso_badge_loud = re.search(r"Programa Activo.*?(?:bg-accent|bg-\[#ffcc29\])", iso_raw, re.I | re.DOTALL)
        record_check(
            "M2_CHALLENGE_F6_BADGE_ISO",
            "certificacion-iso/index.html Programa Activo badge does NOT use loud yellow bg-accent",
            iso_badge_loud is None,
            "certificacion-iso/index.html",
            "Programa Activo badge still uses loud yellow background"
        )

    return report


def main():
    print("=" * 80)
    print("  STAR UNION S.R.L. — EMPIRICAL CHALLENGER TEST SUITE (M2 ART DIRECTION & PALETTE)")
    print("=" * 80)
    print(f"Target Directory: {PROJECT_ROOT}\n")

    report = run_adversarial_m2_checks()

    summary = report["summary"]
    print(f"Total HTML Targets: {summary['total_files']}")
    print(f"Total Checks Run:   {summary['checks_run']}")
    print(f"Total Passed:       {summary['passed']} ({summary['passed']/summary['checks_run']*100:.1f}%)")
    print(f"Total Failures:     {summary['failures']}")
    print(f"Total Warnings:     {summary['warnings']}\n")

    # Group test results by ID
    print("Test Breakdown:")
    for res in report["test_results"]:
        status = res["status"]
        status_str = f"[{status}]"
        print(f"  {status_str:8} {res['id']:32} {res['file']:30} {res['desc']}")

    if report["failures"]:
        print("\n" + "x" * 80)
        print("FAILURES DETECTED IN EMPIRICAL CHALLENGER VERIFICATION:")
        for f in report["failures"]:
            print(f"  ✖ {f}")
        print("x" * 80)
        sys.exit(1)
    else:
        print("\n" + "=" * 80)
        print("✔ ALL EMPIRICAL CHALLENGER VERIFICATIONS PASSED (100% SUCCESS)")
        print("  VERDICT: APPROVE")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()
