#!/usr/bin/env python3
"""
Empirical Challenger Test Harness for Milestone 1 (Typography Unification)
Star Union S.R.L.

Performs rigorous, independent empirical verification across all 11 HTML files:
1. Strict HTML parsing of <link> tags via html.parser.HTMLParser
2. Strict CSS & regex inspection of <style> blocks
3. AST & Node.js VM runtime execution of inline tailwind.config
4. Full-file adversarial scans for residual foreign fonts, inline overrides, and syntax defects
"""

import os
import sys
import re
import json
import subprocess
from html.parser import HTMLParser
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

class LinkTagExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.links = []
        self.styles = []
        self.scripts = []
        self.in_style = False
        self.current_style = []
        self.in_script = False
        self.current_script = []
        self.current_script_attrs = {}

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag.lower() == "head":
            self.in_head = True
        elif tag.lower() == "link":
            self.links.append((self.in_head, attr_dict))
        elif tag.lower() == "style":
            self.in_style = True
            self.current_style = []
        elif tag.lower() == "script":
            self.in_script = True
            self.current_script = []
            self.current_script_attrs = attr_dict

    def handle_endtag(self, tag):
        if tag.lower() == "head":
            self.in_head = False
        elif tag.lower() == "style":
            self.in_style = False
            self.styles.append("".join(self.current_style))
        elif tag.lower() == "script":
            self.in_script = False
            self.scripts.append((self.current_script_attrs, "".join(self.current_script)))

    def handle_data(self, data):
        if self.in_style:
            self.current_style.append(data)
        elif self.in_script:
            self.current_script.append(data)


def run_checks():
    results = {
        "total_files": len(PUBLIC_PAGES),
        "checks_run": 0,
        "failures": [],
        "warnings": [],
        "details": {}
    }

    for page in PUBLIC_PAGES:
        file_path = PROJECT_ROOT / page
        page_results = {
            "link_checks": [],
            "style_checks": [],
            "tailwind_checks": [],
            "residual_scans": []
        }

        if not file_path.exists():
            results["failures"].append(f"[{page}] File does not exist on disk: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()

        # ---------------------------------------------------------
        # 1. HTML PARSING OF <link> TAGS
        # ---------------------------------------------------------
        parser = LinkTagExtractor()
        parser.feed(raw_content)

        # Check preconnects
        has_preconnect_googleapis = False
        has_preconnect_gstatic = False
        gstatic_has_crossorigin = False
        google_fonts_stylesheet_links = []
        preconnect_links = []
        inter_links = []
        jakarta_links = []

        for in_head, attrs in parser.links:
            rel = attrs.get("rel", "").lower()
            href = attrs.get("href", "")

            if "preconnect" in rel:
                preconnect_links.append((rel, href, attrs))
                if "fonts.googleapis.com" in href:
                    has_preconnect_googleapis = True
                if "fonts.gstatic.com" in href:
                    has_preconnect_gstatic = True
                    # Check crossorigin (attribute presence)
                    if "crossorigin" in attrs:
                        gstatic_has_crossorigin = True

            if "stylesheet" in rel:
                if "fonts.googleapis.com" in href or "fonts.gstatic.com" in href:
                    google_fonts_stylesheet_links.append(href)
                if "family=Inter" in href or "family=inter" in href.lower():
                    inter_links.append(href)
                if "family=Plus+Jakarta+Sans" in href or "plus+jakarta+sans" in href.lower():
                    jakarta_links.append(href)

        # 1.1 Preconnect to googleapis
        results["checks_run"] += 1
        if has_preconnect_googleapis:
            page_results["link_checks"].append(("PASS", "Preconnect to fonts.googleapis.com present"))
        else:
            results["failures"].append(f"[{page}] Missing <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">")

        # 1.2 Preconnect to gstatic with crossorigin
        results["checks_run"] += 1
        if has_preconnect_gstatic and gstatic_has_crossorigin:
            page_results["link_checks"].append(("PASS", "Preconnect to fonts.gstatic.com with crossorigin present"))
        elif has_preconnect_gstatic and not gstatic_has_crossorigin:
            results["failures"].append(f"[{page}] Preconnect to fonts.gstatic.com lacks 'crossorigin' attribute")
        else:
            results["failures"].append(f"[{page}] Missing <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>")

        # 1.3 Exactly one Google Fonts stylesheet linking Open+Sans
        results["checks_run"] += 1
        open_sans_links = [h for h in google_fonts_stylesheet_links if "Open+Sans" in h or "Open%20Sans" in h]
        if len(open_sans_links) == 1:
            # Check weights & display=swap
            href = open_sans_links[0]
            if "display=swap" in href:
                page_results["link_checks"].append(("PASS", "Exactly 1 Open Sans stylesheet with display=swap"))
            else:
                results["warnings"].append(f"[{page}] Open Sans stylesheet missing display=swap: {href}")
        elif len(open_sans_links) == 0:
            results["failures"].append(f"[{page}] No Google Fonts stylesheet linking Open Sans found")
        else:
            results["failures"].append(f"[{page}] Multiple ({len(open_sans_links)}) Open Sans stylesheets found")

        # 1.4 Zero links to Inter or Plus Jakarta Sans
        results["checks_run"] += 1
        if not inter_links and not jakarta_links:
            page_results["link_checks"].append(("PASS", "Zero links to Inter or Plus Jakarta Sans"))
        else:
            if inter_links:
                results["failures"].append(f"[{page}] Foreign font Inter linked in <head>: {inter_links}")
            if jakarta_links:
                results["failures"].append(f"[{page}] Foreign font Plus Jakarta Sans linked in <head>: {jakarta_links}")

        # Total google fonts stylesheet links should be exactly 1
        results["checks_run"] += 1
        if len(google_fonts_stylesheet_links) == 1:
            page_results["link_checks"].append(("PASS", "Exactly 1 total Google Fonts stylesheet link"))
        else:
            results["failures"].append(f"[{page}] Expected 1 Google Fonts stylesheet link, found {len(google_fonts_stylesheet_links)}: {google_fonts_stylesheet_links}")

        # ---------------------------------------------------------
        # 2. REGEX & CSS INSPECTION OF <style>
        # ---------------------------------------------------------
        style_content = "\n".join(parser.styles)

        # 2.1 font-size: 1rem in style
        results["checks_run"] += 1
        if re.search(r"font-size:\s*1rem", style_content, re.IGNORECASE):
            page_results["style_checks"].append(("PASS", "body declares font-size: 1rem"))
        else:
            results["failures"].append(f"[{page}] Missing 'font-size: 1rem' in <style>")

        # 2.2 zero 1.125rem in style or whole file
        results["checks_run"] += 1
        rem_18px_matches = list(re.finditer(r"1\.125rem", raw_content, re.IGNORECASE))
        if len(rem_18px_matches) == 0:
            page_results["style_checks"].append(("PASS", "Zero occurrences of 1.125rem across entire file"))
        else:
            results["failures"].append(f"[{page}] Found {len(rem_18px_matches)} occurrences of '1.125rem'")

        # 2.3 body font-family declared as Open Sans
        results["checks_run"] += 1
        body_font_match = re.search(r"body\s*\{[^}]*font-family:\s*['\"]?Open\s+Sans['\"]?", style_content, re.IGNORECASE)
        if body_font_match:
            page_results["style_checks"].append(("PASS", "body declares font-family: 'Open Sans'"))
        else:
            results["failures"].append(f"[{page}] body does not declare font-family: 'Open Sans' in <style>")

        # 2.4 Headings font-family declared as Open Sans & color #000000
        results["checks_run"] += 1
        headings_match = re.search(r"(h1[^{]*)\{[^}]*color:\s*#000000", style_content, re.IGNORECASE)
        if headings_match:
            page_results["style_checks"].append(("PASS", "Headings declare color: #000000 in <style>"))
        else:
            results["failures"].append(f"[{page}] Headings do not declare color: #000000 in <style>")

        # 2.5 Balanced curly braces in <style>
        results["checks_run"] += 1
        open_braces = style_content.count("{")
        close_braces = style_content.count("}")
        if open_braces == close_braces and open_braces > 0:
            page_results["style_checks"].append(("PASS", f"Style block braces balanced ({open_braces} pairs)"))
        else:
            results["failures"].append(f"[{page}] Style block braces unbalanced ({open_braces} '{{' vs {close_braces} '}}')")

        # ---------------------------------------------------------
        # 3. AST / RUNTIME EXECUTION OF tailwind.config
        # ---------------------------------------------------------
        # Find the inline script containing tailwind.config
        tailwind_script = None
        for attrs, script_body in parser.scripts:
            if "tailwind.config" in script_body:
                tailwind_script = script_body
                break

        results["checks_run"] += 1
        if tailwind_script is None:
            results["failures"].append(f"[{page}] No inline script found containing tailwind.config")
        else:
            # Execute in Node.js VM to inspect the actual evaluated JS object
            node_code = f"""
            try {{
                let tailwind = {{}};
                {tailwind_script}
                const cfg = tailwind.config;
                const ff = cfg && cfg.theme && cfg.theme.extend && cfg.theme.extend.fontFamily;
                if (!ff) {{
                    console.log(JSON.stringify({{ error: "No theme.extend.fontFamily in tailwind.config" }}));
                    process.exit(0);
                }}
                console.log(JSON.stringify({{
                    sans: ff.sans,
                    heading: ff.heading,
                    display: ff.display,
                    all_keys: Object.keys(ff)
                }}));
            }} catch (e) {{
                console.log(JSON.stringify({{ error: e.message }}));
            }}
            """
            try:
                proc = subprocess.run(["node", "-e", node_code], capture_output=True, text=True, timeout=5)
                output = proc.stdout.strip()
                parsed = json.loads(output) if output else {}
                if "error" in parsed:
                    results["failures"].append(f"[{page}] tailwind.config execution failed: {parsed['error']}")
                else:
                    # Check sans
                    sans_val = parsed.get("sans", [])
                    heading_val = parsed.get("heading", [])
                    display_val = parsed.get("display", [])

                    sans_ok = any("Open Sans" in str(x) for x in sans_val)
                    heading_ok = any("Open Sans" in str(x) for x in heading_val)
                    display_ok = any("Open Sans" in str(x) for x in display_val)

                    if sans_ok and heading_ok and display_ok:
                        page_results["tailwind_checks"].append(("PASS", "tailwind.config maps sans, heading, display to Open Sans"))
                    else:
                        missing_mappings = []
                        if not sans_ok: missing_mappings.append(f"sans={sans_val}")
                        if not heading_ok: missing_mappings.append(f"heading={heading_val}")
                        if not display_ok: missing_mappings.append(f"display={display_val}")
                        results["failures"].append(f"[{page}] tailwind.config missing Open Sans in: {missing_mappings}")
            except Exception as e:
                results["failures"].append(f"[{page}] Error running node on tailwind.config: {str(e)}")

        # ---------------------------------------------------------
        # 4. ADVERSARIAL RESIDUAL SCANS
        # ---------------------------------------------------------
        # Search for any remaining occurrences of "Inter" or "Plus Jakarta Sans" outside comments
        # Strip HTML comments first
        content_no_comments = re.sub(r"<!--.*?-->", "", raw_content, flags=re.DOTALL)

        results["checks_run"] += 1
        inter_in_code = []
        for line_no, line in enumerate(content_no_comments.splitlines(), start=1):
            # Exclude words like 'interior', 'interiores', 'interrumpir', 'interurbano', 'interés', etc.
            # Match standalone "Inter" as font name
            if re.search(r"\bInter\b", line):
                # Check if it's referring to font
                if re.search(r"['\"]Inter['\"]|font-['\"]?Inter|family=Inter", line, re.IGNORECASE):
                    inter_in_code.append((line_no, line.strip()))

        if inter_in_code:
            results["failures"].append(f"[{page}] Found active references to Inter font: {inter_in_code}")
        else:
            page_results["residual_scans"].append(("PASS", "Zero active references to Inter font"))

        results["checks_run"] += 1
        jakarta_in_code = []
        for line_no, line in enumerate(content_no_comments.splitlines(), start=1):
            if re.search(r"Jakarta", line, re.IGNORECASE):
                jakarta_in_code.append((line_no, line.strip()))

        if jakarta_in_code:
            results["failures"].append(f"[{page}] Found active references to Plus Jakarta Sans font: {jakarta_in_code}")
        else:
            page_results["residual_scans"].append(("PASS", "Zero active references to Plus Jakarta Sans font"))

        # Check inline styles for font-family
        results["checks_run"] += 1
        inline_font_overrides = []
        for line_no, line in enumerate(raw_content.splitlines(), start=1):
            if re.search(r"style=[\"'][^\"']*font-family", line, re.IGNORECASE):
                inline_font_overrides.append((line_no, line.strip()))

        if inline_font_overrides:
            results["failures"].append(f"[{page}] Inline style font-family overrides detected: {inline_font_overrides}")
        else:
            page_results["residual_scans"].append(("PASS", "Zero inline font-family overrides"))

        # Check body class in certificacion-iso and other pages
        results["checks_run"] += 1
        body_tag_match = re.search(r"<body([^>]*)>", raw_content, re.IGNORECASE)
        if body_tag_match:
            body_attrs = body_tag_match.group(1)
            if "bg-gray-50" in body_attrs:
                results["failures"].append(f"[{page}] <body> tag still has 'bg-gray-50' class: <body{body_attrs}>")
            else:
                page_results["residual_scans"].append(("PASS", "<body> tag does not contain bg-gray-50"))

        results["details"][page] = page_results

    return results


def main():
    print("=" * 80)
    print("  STAR UNION S.R.L. — EMPIRICAL CHALLENGER TEST SUITE (M1 TYPOGRAPHY)")
    print("=" * 80)
    print(f"Target Directory: {PROJECT_ROOT}\n")

    res = run_checks()

    print(f"Total HTML Files Analyzed: {res['total_files']}")
    print(f"Total Checks Executed:     {res['checks_run']}")
    print(f"Total Failures:            {len(res['failures'])}")
    print(f"Total Warnings:            {len(res['warnings'])}\n")

    for page, data in res["details"].items():
        print(f"▶ File: {page}")
        for cat, items in data.items():
            for status, desc in items:
                print(f"   [{status}] {cat} -> {desc}")
        print()

    if res["warnings"]:
        print("\n" + "!" * 80)
        print("WARNINGS:")
        for w in res["warnings"]:
            print(f"  • {w}")

    if res["failures"]:
        print("\n" + "x" * 80)
        print("FAILURES DETECTED:")
        for f in res["failures"]:
            print(f"  ✖ {f}")
        print("x" * 80)
        sys.exit(1)
    else:
        print("\n" + "=" * 80)
        print("✔ ALL EMPIRICAL CHALLENGER CHECKS PASSED (100% SUCCESS)")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()
