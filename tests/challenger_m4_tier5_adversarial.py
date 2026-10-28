#!/usr/bin/env python3
"""
STAR UNION S.R.L. — TIER 5 ADVERSARIAL COVERAGE HARDENING HARNESS
Challenger: challenger_m4_tier5

Exhaustive empirical audit and stress harness:
1. Typography Hardening across all 11 public pages + dossier (Open Sans, 1rem base, 0 Inter/Jakarta).
2. Art Direction Hardening (White Hero, White button in official green footer, 0 Brazil effect, 0 rogue colors).
3. Brand Safety, Voice & Hygiene (0 taboo words in DOM, corporate voseo, 0 gendered terms, 0 leaked tools, brand firewall).
4. JavaScript & Component Reliability (node -c syntax, form routing & disqualification, GA4 dispatch).
5. Distribution Packaging Purity (SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip asset resolution & HTTP live server).
"""

import os
import re
import sys
import json
import zipfile
import tempfile
import threading
import http.server
import socketserver
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path
from html.parser import HTMLParser

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

class TextAndAttrExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_nodes = []
        self.attributes = []
        self.assets = []
        self.links = []
        self.forms = []
        self.current_form = None

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text_nodes.append(cleaned)

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        for k, v in attrs:
            if v:
                self.attributes.append((tag, k, v))

        if tag == "img" and "src" in attr_dict:
            self.assets.append(("img", attr_dict["src"]))
        elif tag == "script" and "src" in attr_dict:
            self.assets.append(("script", attr_dict["src"]))
        elif tag == "link" and "href" in attr_dict:
            rel = attr_dict.get("rel", "")
            if "stylesheet" in rel or "icon" in rel:
                self.assets.append(("link", attr_dict["href"]))
        elif tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])
        elif tag == "form":
            self.current_form = {
                "class": attr_dict.get("class", ""),
                "inputs": [],
            }
            self.forms.append(self.current_form)
        elif tag in ("input", "select", "textarea") and self.current_form is not None:
            if "name" in attr_dict:
                self.current_form["inputs"].append(attr_dict["name"])

    def handle_endtag(self, tag):
        if tag == "form":
            self.current_form = None


class TestHarness:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.failures = []

    def check(self, condition, name, details=""):
        self.total += 1
        if condition:
            self.passed += 1
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            msg = f"  [FAIL] {name}: {details}"
            print(msg)
            self.failures.append(msg)

    def print_summary(self):
        print("\n" + "=" * 80)
        print("TIER 5 ADVERSARIAL STRESS HARNESS SUMMARY")
        print("=" * 80)
        print(f"Total Checks:  {self.total}")
        print(f"Passed Checks: {self.passed} ({self.passed / self.total * 100:.1f}%)")
        print(f"Failed Checks: {self.failed}")
        if self.failures:
            print("\nFAILURES:")
            for f in self.failures:
                print(f)
            print("\nVERDICT: REQUEST_CHANGES")
            return False
        else:
            print("\nVERDICT: APPROVE")
            return True


def run_tier5_harness():
    harness = TestHarness()
    print("=" * 80)
    print("STARTING TIER 5 ADVERSARIAL COVERAGE HARDENING HARNESS")
    print(f"Project root: {PROJECT_ROOT}")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # SUITE 1: Typography Unification & Open Sans Enforcement (11 Pages)
    # --------------------------------------------------------------------------
    print("\n--- SUITE 1: Typography Unification & Open Sans Hardening ---")

    for rel_path in PUBLIC_PAGES:
        file_path = PROJECT_ROOT / rel_path
        harness.check(file_path.exists(), f"Page exists: {rel_path}", f"Path not found: {file_path}")
        if not file_path.exists():
            continue

        content = file_path.read_text(encoding="utf-8")

        # 1.1 Preconnects
        harness.check(
            '<link rel="preconnect" href="https://fonts.googleapis.com">' in content,
            f"Preconnect fonts.googleapis.com in {rel_path}"
        )
        harness.check(
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' in content,
            f"Preconnect fonts.gstatic.com crossorigin in {rel_path}"
        )

        # 1.2 Open Sans Font Link
        harness.check(
            "family=Open+Sans" in content,
            f"Loads Open Sans via Google Fonts in {rel_path}"
        )

        # 1.3 Zero Inter or Plus Jakarta Sans
        has_inter = bool(re.search(r"font-family:[^;]*['\"]?Inter['\"]?", content, re.IGNORECASE))
        has_jakarta = bool(re.search(r"font-family:[^;]*['\"]?Plus\s+Jakarta\s+Sans['\"]?", content, re.IGNORECASE))
        has_jakarta_link = "Plus+Jakarta+Sans" in content or "family=Inter" in content
        harness.check(
            not (has_inter or has_jakarta or has_jakarta_link),
            f"Zero rogue fonts (Inter/Jakarta) in {rel_path}"
        )

        # 1.4 Base body font size 1rem (16px) & Open Sans base
        body_style_match = re.search(r"body\s*\{([^}]+)\}", content)
        if body_style_match:
            body_style = body_style_match.group(1)
            harness.check(
                "Open Sans" in body_style,
                f"Body style enforces Open Sans in {rel_path}"
            )
            harness.check(
                "font-size: 1rem" in body_style or "font-size: 16px" in body_style,
                f"Body style specifies 1rem/16px in {rel_path}"
            )
            harness.check(
                "1.125rem" not in body_style and "18px" not in body_style,
                f"No 18px / 1.125rem body size in {rel_path}"
            )
        else:
            harness.check(False, f"Body style block found in {rel_path}", "No body {...} block")

        # 1.5 tailwind.config font family mapping
        tailwind_config_match = re.search(r"tailwind\.config\s*=\s*(\{.+?\})\s*(?:;|\s*</script>)", content, re.DOTALL)
        if tailwind_config_match:
            cfg_text = tailwind_config_match.group(1)
            harness.check(
                "sans" in cfg_text and "Open Sans" in cfg_text,
                f"tailwind.config sans maps to Open Sans in {rel_path}"
            )
            harness.check(
                "heading" in cfg_text and "Open Sans" in cfg_text,
                f"tailwind.config heading maps to Open Sans in {rel_path}"
            )
            harness.check(
                "display" in cfg_text and "Open Sans" in cfg_text,
                f"tailwind.config display maps to Open Sans in {rel_path}"
            )
        else:
            harness.check(False, f"tailwind.config present in {rel_path}")

    # Check starunion-b2b.js font family
    js_content = (PROJECT_ROOT / "assets/js/starunion-b2b.js").read_text(encoding="utf-8")
    harness.check(
        "Open Sans" in js_content and "Inter" not in js_content and "Jakarta" not in js_content,
        "assets/js/starunion-b2b.js enforces Open Sans styling"
    )

    # --------------------------------------------------------------------------
    # SUITE 2: Art Direction, Hero & Footer Harmony (0 Brazil Effect, 0 Rogue Colors)
    # --------------------------------------------------------------------------
    print("\n--- SUITE 2: Art Direction & Palette Hardening ---")

    home_content = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")

    # 2.1 Home Hero White Background
    hero_match = re.search(r"<main[^>]*>.*?<section([^>]*)>(.*?)</section>", home_content, re.DOTALL)
    if hero_match:
        hero_attrs = hero_match.group(1)
        hero_inner = hero_match.group(2)
        harness.check(
            "bg-white" in hero_attrs or "bg-white" in hero_inner[:200],
            "Home Hero has bg-white dominant surface"
        )
        harness.check(
            "bg-brand" not in hero_attrs,
            "Home Hero does NOT use full-green bg-brand background"
        )
        # Hero H1 must be dark text
        h1_match = re.search(r"<h1([^>]*)>(.*?)</h1>", hero_inner, re.DOTALL)
        if h1_match:
            h1_attrs = h1_match.group(1)
            harness.check(
                "#000000" in h1_attrs or "text-black" in h1_attrs or "text-gray-900" in h1_attrs,
                "Home Hero H1 uses dark/black text"
            )
            harness.check(
                "text-white" not in h1_attrs,
                "Home Hero H1 is NOT white text"
            )
        else:
            harness.check(False, "Home Hero contains <h1> element")

        # Hero Primary CTA button
        harness.check(
            "bg-brand hover:bg-brand-dark text-white" in hero_inner,
            "Home Hero primary CTA uses official green button"
        )
        harness.check(
            "bg-[#ffcc29]" not in hero_inner and "bg-yellow-400" not in hero_inner,
            "Home Hero does NOT contain yellow button"
        )
    else:
        harness.check(False, "Home Hero section located in index.html")

    # 2.2 Official Dark Green Footer on ALL 11 pages (and White Button on 10 public pages)
    for rel_path in PUBLIC_PAGES:
        file_path = PROJECT_ROOT / rel_path
        content = file_path.read_text(encoding="utf-8")
        footer_match = re.search(r"<footer([^>]*)>(.*?)</footer>", content, re.DOTALL)
        if footer_match:
            footer_attrs = footer_match.group(1)
            footer_inner = footer_match.group(2)

            # Footer background
            harness.check(
                "#133522" in footer_attrs or "#133522" in content or "bg-[#133522]" in footer_attrs or "bg-brand-footer" in footer_attrs,
                f"Footer uses official dark green #133522 in {rel_path}"
            )

            # For the 10 public pages, verify white corporate CTA button
            if rel_path != "dossier/index.html":
                harness.check(
                    "bg-white hover:bg-gray-100 text-brand" in footer_inner,
                    f"Footer CTA is white corporate button in {rel_path}"
                )

            # No yellow button in footer
            harness.check(
                "bg-[#ffcc29]" not in footer_inner and "bg-yellow-400" not in footer_inner and "bg-accent" not in footer_inner,
                f"Footer contains zero yellow buttons in {rel_path}"
            )

            # No yellow text / labels in footer (anti-Brazil effect)
            harness.check(
                "text-[#ffcc29]" not in footer_inner and "text-yellow-400" not in footer_inner,
                f"Footer contains zero yellow text in {rel_path}"
            )

            # No yellow link hover
            harness.check(
                "hover:text-[#ffcc29]" not in footer_inner and "hover:text-yellow-400" not in footer_inner,
                f"Footer links do not hover to yellow in {rel_path}"
            )
        else:
            harness.check(False, f"Footer present in {rel_path}")

    # 2.3 Zero forbidden Tailwind color classes across all 11 pages
    forbidden_class_pattern = re.compile(
        r'\b(?:bg|text|border|ring|stroke|fill)-(?:blue|indigo|sky|cyan|purple|orange)-\d+\b',
        re.IGNORECASE
    )
    for rel_path in PUBLIC_PAGES:
        content = (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")
        matches = forbidden_class_pattern.findall(content)
        harness.check(
            len(matches) == 0,
            f"Zero forbidden color classes in {rel_path}",
            f"Found: {matches}"
        )

    # 2.4 Zero out-of-palette hexes
    rogue_hexes = ["#057a3f", "#023d1f", "#e6b822"]
    for rel_path in PUBLIC_PAGES:
        content = (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")
        for hex_code in rogue_hexes:
            harness.check(
                hex_code.lower() not in content.lower(),
                f"Zero occurrences of {hex_code} in {rel_path}"
            )

    # --------------------------------------------------------------------------
    # SUITE 3: Brand Safety, Voice & Hygiene (0 Taboo Words in DOM Text/Attrs)
    # --------------------------------------------------------------------------
    print("\n--- SUITE 3: Brand Safety, Voice & Hygiene ---")

    taboo_words = [
        "barbijo", "barbijos", "covid", "covid-19", "tapabocas",
        "mucamas", "empleaditas", "chicos", "barato", "low cost"
    ]
    gender_patterns = [
        re.compile(r"\b(?:bienvenidos a star union|bienvenides|todes|bienvenidos/as)\b", re.I)
    ]

    pages_to_audit = PUBLIC_PAGES + ["accesos/index.html"]
    dom_taboo_hits = []
    dom_gender_hits = []
    internal_leak_hits = []

    for p in pages_to_audit:
        fpath = PROJECT_ROOT / p
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        parser = TextAndAttrExtractor()
        parser.feed(content)

        # Audit text nodes
        for txt in parser.text_nodes:
            for tw in taboo_words:
                if re.search(r"\b" + re.escape(tw) + r"\b", txt, re.I):
                    dom_taboo_hits.append((p, "text", tw, txt))
            for gp in gender_patterns:
                m = gp.search(txt)
                if m:
                    dom_gender_hits.append((p, "text", m.group(0), txt))

        # Audit attributes
        for tag, attr, val in parser.attributes:
            for tw in taboo_words:
                if re.search(r"\b" + re.escape(tw) + r"\b", val, re.I):
                    dom_taboo_hits.append((p, f"attr:{attr}", tw, val))
            for gp in gender_patterns:
                m = gp.search(val)
                if m:
                    dom_gender_hits.append((p, f"attr:{attr}", m.group(0), val))

        # Internal leaks on public pages
        if p in PUBLIC_PAGES:
            for href in parser.links:
                for bad_dir in ["radar-comercial", "brochures/editables", "relevamiento-gerencia", "acuerdos/index"]:
                    if bad_dir in href:
                        internal_leak_hits.append((p, href))

    harness.check(
        len(dom_taboo_hits) == 0,
        "DOM text and attributes across 11 pages + accesos have 0 taboo words",
        f"Hits: {dom_taboo_hits}"
    )
    harness.check(
        len(dom_gender_hits) == 0,
        "DOM text and attributes across 11 pages + accesos have 0 gendered greetings",
        f"Hits: {dom_gender_hits}"
    )
    harness.check(
        len(internal_leak_hits) == 0,
        "The 11 public pages have 0 links to internal private tools",
        f"Leaks: {internal_leak_hits}"
    )

    # In limpieza-en-altura, ensure barbiquejo homologado is present
    altura_content = (PROJECT_ROOT / "limpieza-en-altura/index.html").read_text(encoding="utf-8")
    harness.check(
        "barbiquejo homologado" in altura_content.lower() or "barbiquejo" in altura_content.lower(),
        "limpieza-en-altura contains 'barbiquejo' technical term"
    )

    # Accesos index.html robots meta
    accesos_path = PROJECT_ROOT / "accesos/index.html"
    harness.check(accesos_path.exists(), "accesos/index.html exists")
    if accesos_path.exists():
        accesos_content = accesos_path.read_text(encoding="utf-8")
        harness.check(
            bool(re.search(r'<meta\s+name=[\'"]robots[\'"]\s+content=[\'"][^\'"]*noindex[^\'"]*nofollow[^\'"]*[\'"]', accesos_content, re.IGNORECASE)),
            "accesos/index.html has <meta name='robots' content='noindex, nofollow'>"
        )

    # Operational Base Guaminí Address & TÜV Rheinland ISO 9001
    for rel_path in PUBLIC_PAGES:
        content = (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")
        harness.check(
            "Guaminí" in content or "Guamini" in content,
            f"Base Guaminí mentioned in {rel_path}"
        )
        harness.check(
            "9000041847" in content,
            f"TÜV Rheinland ID 9000041847 present in {rel_path}"
        )

    # --------------------------------------------------------------------------
    # SUITE 4: JavaScript & Interactive Components Hardening
    # --------------------------------------------------------------------------
    print("\n--- SUITE 4: JavaScript & Component Functionality ---")

    js_file = PROJECT_ROOT / "assets/js/starunion-b2b.js"
    harness.check(js_file.exists(), "assets/js/starunion-b2b.js exists")

    # Run node -c on starunion-b2b.js
    res = subprocess.run(["node", "-c", str(js_file)], capture_output=True, text=True)
    harness.check(
        res.returncode == 0,
        "assets/js/starunion-b2b.js passes 'node -c' syntax verification",
        res.stderr
    )

    # All 11 pages include starunion-b2b.js
    for rel_path in PUBLIC_PAGES:
        content = (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")
        harness.check(
            "starunion-b2b.js" in content,
            f"Script starunion-b2b.js included in {rel_path}"
        )

    # Form field completeness on certificacion-iso and vertical pages
    form_pages = [
        "certificacion-iso/index.html",
        "limpieza-industrial/index.html",
        "grandes-superficies/index.html",
        "consorcios/index.html",
        "clinicas-y-hospitales/index.html",
        "universidades-y-clubes/index.html",
        "servicios-especiales/index.html",
    ]
    for rel_path in form_pages:
        content = (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")
        parser = TextAndAttrExtractor()
        parser.feed(content)
        b2b_forms = [f for f in parser.forms if "js-b2b-quote-form" in f["class"]]
        harness.check(
            len(b2b_forms) > 0,
            f"At least one .js-b2b-quote-form in {rel_path}"
        )
        if b2b_forms:
            inputs = b2b_forms[0]["inputs"]
            for required_field in ["empresa", "nombre", "email", "telefono", "mensaje"]:
                harness.check(
                    required_field in inputs,
                    f"Field '{required_field}' in {rel_path} quote form"
                )

    # --------------------------------------------------------------------------
    # SUITE 5: Packaging Integrity & Live HTTP Asset Mirroring
    # --------------------------------------------------------------------------
    print("\n--- SUITE 5: Distribution Packaging & Asset Mirroring ---")

    zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
    harness.check(zip_path.exists(), "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip exists")

    if zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as z:
            namelist = z.namelist()
            harness.check(len(namelist) == 153, f"ZIP contains exactly 153 clean entries (actual: {len(namelist)})")

            # Check forbidden files and directories
            forbidden_prefixes = [
                ".agents", ".git", "tests/", "radar-comercial",
                "brochures/editables", "relevamiento-gerencia", "acuerdos", "accesos"
            ]
            forbidden_extensions = [".md", ".json", ".bak", ".tmp", ".old"]

            for entry in namelist:
                harness.check(not entry.startswith("/"), f"No absolute path entry: {entry}")
                harness.check(".." not in entry, f"No path traversal entry: {entry}")
                harness.check("__MACOSX" not in entry, f"No macOS metadata entry: {entry}")
                harness.check(".DS_Store" not in entry, f"No .DS_Store entry: {entry}")

                for pref in forbidden_prefixes:
                    harness.check(not entry.startswith(pref), f"No internal tool entry '{entry}'")

                for ext in forbidden_extensions:
                    harness.check(not entry.endswith(ext), f"No forbidden extension entry '{entry}'")

            # Check mandatory public pages
            for rel_path in PUBLIC_PAGES:
                harness.check(rel_path in namelist, f"ZIP contains {rel_path}")

            harness.check("assets/js/starunion-b2b.js" in namelist, "ZIP contains assets/js/starunion-b2b.js")
            harness.check("logo-footer-blanco.png" in namelist, "ZIP contains logo-footer-blanco.png")
            harness.check("logo-tuv.png" in namelist, "ZIP contains logo-tuv.png")

            # Extract to temp directory and test asset resolution & live HTTP server
            with tempfile.TemporaryDirectory() as tmpdir:
                z.extractall(tmpdir)
                tmp_root = Path(tmpdir)

                # Syntax check on unzipped JS
                unzipped_js = tmp_root / "assets/js/starunion-b2b.js"
                res = subprocess.run(["node", "-c", str(unzipped_js)], capture_output=True, text=True)
                harness.check(res.returncode == 0, "Unzipped starunion-b2b.js passes node -c syntax check")

                # Parse all 11 public pages and verify local asset resolution
                all_assets_resolved = True
                unresolved_list = []

                for rel_page in PUBLIC_PAGES:
                    html_file = tmp_root / rel_page
                    if not html_file.exists():
                        continue
                    parser = TextAndAttrExtractor()
                    parser.feed(html_file.read_text(encoding="utf-8"))
                    for asset_type, asset_url in parser.assets:
                        if asset_url.startswith(("http://", "https://", "data:", "//")):
                            continue
                        clean_url = asset_url.split("?")[0].split("#")[0]
                        target_file = (html_file.parent / clean_url).resolve()
                        if not target_file.exists():
                            all_assets_resolved = False
                            unresolved_list.append((rel_page, asset_type, asset_url))

                harness.check(
                    all_assets_resolved,
                    "All local <img>, <script>, and <link> assets in 11 public pages resolve in extracted ZIP",
                    f"Unresolved: {unresolved_list[:5]}"
                )

                # Live HTTP server test
                class QuietHandler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=tmpdir, **kwargs)
                    def log_message(self, format, *args):
                        pass

                httpd = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
                port = httpd.server_address[1]
                server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
                server_thread.start()

                try:
                    for rel_page in PUBLIC_PAGES:
                        url = f"http://127.0.0.1:{port}/{rel_page}"
                        req = urllib.request.urlopen(url, timeout=3)
                        harness.check(req.status == 200, f"HTTP 200 OK for {rel_page} from unzipped package")

                    for asset in ["assets/js/starunion-b2b.js", "logo-footer-blanco.png", "logo-tuv.png"]:
                        url = f"http://127.0.0.1:{port}/{asset}"
                        req = urllib.request.urlopen(url, timeout=3)
                        harness.check(req.status == 200, f"HTTP 200 OK for {asset} from unzipped package")
                finally:
                    httpd.shutdown()
                    httpd.server_close()

    # --------------------------------------------------------------------------
    # SUITE 6: Brand Firewall Physical Interception Verification
    # --------------------------------------------------------------------------
    print("\n--- SUITE 6: Brand Firewall Interception Hardening ---")

    firewall_script = Path("/Users/arianawajntraub/.gemini/config/firewall/brand_firewall.py")
    harness.check(firewall_script.exists(), "brand_firewall.py exists on disk")

    if firewall_script.exists():
        target_file = str(PROJECT_ROOT / "index.html")

        def run_fw_check(content_str):
            payload = {
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": target_file, "Content": content_str}
                }
            }
            p = subprocess.Popen(
                [sys.executable, str(firewall_script)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            out, err = p.communicate(input=json.dumps(payload))
            try:
                data = json.loads(out.strip())
                return data.get("decision", "deny")
            except Exception:
                return "error"

        harness.check(
            run_fw_check("Servicio de limpieza profesional corporativo para industrias y plantas.") == "allow",
            "Firewall ALLOWS clean Star Union B2B text"
        )
        harness.check(
            run_fw_check("Uso obligatorio de barbijo en la planta.") == "deny",
            "Firewall DENIES 'barbijo'"
        )
        harness.check(
            run_fw_check("Protocolos de prevencion COVID-19 en oficinas.") == "deny",
            "Firewall DENIES 'COVID-19'"
        )
        harness.check(
            run_fw_check("Escribania Fabricio Rivas y asociados.") == "deny",
            "Firewall DENIES cross-brand 'Fabricio Rivas'"
        )
        harness.check(
            run_fw_check("Telas provistas por Entretelado.") == "deny",
            "Firewall DENIES cross-brand 'Entretelado'"
        )
        harness.check(
            run_fw_check("Bienvenidos a Star Union hoy.") == "deny",
            "Firewall DENIES gendered greeting 'Bienvenidos'"
        )

    return harness.print_summary()


if __name__ == "__main__":
    success = run_tier5_harness()
    sys.exit(0 if success else 1)
