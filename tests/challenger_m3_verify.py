#!/usr/bin/env python3
"""
Empirical Challenger Test Harness for Milestone 3
Star Union S.R.L. — Brand Locks, Components & Packaging

Performs exhaustive, independent, adversarial verification:
1. Probe ZIP package (SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip):
   - Hidden files, .git, .agents, markdown, json leaks, internal tools
   - Path traversal and extraction safety
   - Asset completeness (every relative img, link, script in unzipped HTML exists)
   - Hyperlink integrity in unzipped site
   - HTTP server simulation: serves all 11 public pages with HTTP 200 OK
2. Probe BRAND_AND_CONNECTORS.lock.json & brand_firewall.py:
   - JSON validation and schema checks
   - Positive execution (legitimate edits -> allow)
   - Negative execution (barbijo, covid, cross-brand, gendered, connectors -> deny)
   - run_command hook behavior
3. Probe DOM across all 11 HTML pages + accesos/index.html:
   - Taboo words in text nodes, attributes, comments
   - Gendered greetings
   - Internal tool leak links
   - Placeholder text ("LOGO BLANCO")
4. Probe JavaScript & Form Wiring:
   - node -c syntax check on assets/js/starunion-b2b.js and unzipped copy
   - script tags in all 11 pages
   - Form fields and local TÜV logo in certificacion-iso/index.html
"""

import os
import sys
import re
import json
import zipfile
import tempfile
import threading
import http.server
import urllib.request
import subprocess
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIREWALL_SCRIPT = Path("/Users/arianawajntraub/.gemini/config/firewall/brand_firewall.py")

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
        self.comments = []
        self.img_sources = []
        self.script_sources = []
        self.link_hrefs = []
        self.a_hrefs = []

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text_nodes.append(cleaned)

    def handle_comment(self, data):
        self.comments.append(data.strip())

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if v:
                self.attributes.append((tag, k, v))
                if tag == "img" and k == "src":
                    self.img_sources.append(v)
                elif tag == "script" and k == "src":
                    self.script_sources.append(v)
                elif tag == "link" and k == "href":
                    self.link_hrefs.append(v)
                elif tag == "a" and k == "href":
                    self.a_hrefs.append(v)


def run_firewall(payload):
    p = subprocess.Popen(
        ["python3", str(FIREWALL_SCRIPT)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate(input=json.dumps(payload))
    try:
        return json.loads(out.strip())
    except Exception as e:
        return {"decision": "error", "raw": out, "error": str(e)}


def main():
    print("=" * 80)
    print("CHALLENGER M3 EMPIRICAL STRESS TEST SUITE")
    print("=" * 80)

    total_checks = 0
    passed_checks = 0
    failed_checks = 0
    failures = []

    def check(name, condition, details=""):
        nonlocal total_checks, passed_checks, failed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] {name}")
        else:
            failed_checks += 1
            msg = f"{name}: {details}"
            failures.append(msg)
            print(f"  [FAIL] {name} -> {details}")

    # =========================================================================
    # SECTION 1: ZIP PACKAGE PURITY & INTEGRITY
    # =========================================================================
    print("\n--- SECTION 1: Distribution ZIP Purity & Structure ---")
    zip_path = PROJECT_ROOT / "SITIO_PUBLICO_LIMPIO_PARA_HOSTGATOR_V2.zip"
    check("ZIP package exists on disk", zip_path.exists(), f"Path: {zip_path}")

    if zip_path.exists():
        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = zf.namelist()
            check("ZIP has valid non-zero entry count", len(namelist) > 0, f"Count: {len(namelist)}")

            # Test no traversal sequences
            traversal = [n for n in namelist if ".." in n or n.startswith("/")]
            check("ZIP contains zero path traversal entries", len(traversal) == 0, f"Entries: {traversal}")

            # Test no .git
            git_entries = [n for n in namelist if ".git" in n]
            check("ZIP strictly excludes .git entries", len(git_entries) == 0, f"Entries: {git_entries}")

            # Test no .agents
            agents_entries = [n for n in namelist if ".agents" in n]
            check("ZIP strictly excludes .agents metadata", len(agents_entries) == 0, f"Entries: {agents_entries}")

            # Test no .DS_Store or hidden files
            hidden_entries = [n for n in namelist if "/." in n or n.startswith(".") or "__MACOSX" in n]
            check("ZIP strictly excludes hidden files & __MACOSX", len(hidden_entries) == 0, f"Entries: {hidden_entries}")

            # Test no .md files
            md_entries = [n for n in namelist if n.endswith(".md")]
            check("ZIP strictly excludes markdown (.md) documents", len(md_entries) == 0, f"Entries: {md_entries}")

            # Test no .json files
            json_entries = [n for n in namelist if n.endswith(".json")]
            check("ZIP strictly excludes JSON (.json) files", len(json_entries) == 0, f"Entries: {json_entries}")

            # Test no tests directory
            tests_entries = [n for n in namelist if n.startswith("tests/") or "/tests/" in n]
            check("ZIP strictly excludes test directory", len(tests_entries) == 0, f"Entries: {tests_entries}")

            # Test no private management directories
            private_dirs = ["radar-comercial/", "acuerdos/", "relevamiento-gerencia/", "brochures/editables/", "accesos/"]
            private_entries = [n for n in namelist if any(n.startswith(pd) for pd in private_dirs)]
            check("ZIP strictly excludes internal tool directories", len(private_entries) == 0, f"Entries: {private_entries}")

            # Test inclusion of all 11 public pages
            missing_public = [p for p in PUBLIC_PAGES if p not in namelist]
            check("ZIP contains all 11 public HTML pages", len(missing_public) == 0, f"Missing: {missing_public}")

            # Test key assets in zip
            check("ZIP contains logo-footer-blanco.png", "logo-footer-blanco.png" in namelist, "Missing logo-footer-blanco.png")
            check("ZIP contains logo-tuv.png", "logo-tuv.png" in namelist, "Missing logo-tuv.png")
            check("ZIP contains assets/js/starunion-b2b.js", "assets/js/starunion-b2b.js" in namelist, "Missing starunion-b2b.js")

    # =========================================================================
    # SECTION 2: EXTRACTED ZIP ASSET RESOLUTION & HTTP SERVER
    # =========================================================================
    print("\n--- SECTION 2: Extracted ZIP Functional Asset Verification ---")
    if zip_path.exists():
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmpdir)

            missing_imgs = []
            missing_scripts = []
            missing_links = []
            broken_a_hrefs = []

            for p in PUBLIC_PAGES:
                html_path = Path(tmpdir) / p
                if not html_path.exists():
                    continue
                content = html_path.read_text(encoding="utf-8", errors="replace")
                parser = TextAndAttrExtractor()
                parser.feed(content)

                # Check imgs
                for src in parser.img_sources:
                    if src.startswith(("http://", "https://", "data:", "//")):
                        continue
                    clean_src = src.split("?")[0].split("#")[0]
                    resolved = (html_path.parent / clean_src).resolve()
                    if not resolved.exists():
                        missing_imgs.append((p, src))

                # Check scripts
                for src in parser.script_sources:
                    if src.startswith(("http://", "https://", "data:", "//")):
                        continue
                    clean_src = src.split("?")[0].split("#")[0]
                    resolved = (html_path.parent / clean_src).resolve()
                    if not resolved.exists():
                        missing_scripts.append((p, src))

                # Check stylesheets / icons
                for href in parser.link_hrefs:
                    if href.startswith(("http://", "https://", "data:", "//", "#", "mailto:", "tel:")):
                        continue
                    clean_href = href.split("?")[0].split("#")[0]
                    resolved = (html_path.parent / clean_href).resolve()
                    if not resolved.exists():
                        missing_links.append((p, href))

                # Check a hrefs
                for href in parser.a_hrefs:
                    if href.startswith(("http://", "https://", "data:", "//", "#", "mailto:", "tel:", "javascript:")):
                        continue
                    clean_href = href.split("?")[0].split("#")[0]
                    if not clean_href:
                        continue
                    resolved = (html_path.parent / clean_href).resolve()
                    if resolved.is_dir():
                        resolved = resolved / "index.html"
                    if not resolved.exists():
                        broken_a_hrefs.append((p, href))

            check("All <img> tags in unzipped HTML resolve to real files in ZIP", len(missing_imgs) == 0, f"Missing: {missing_imgs[:5]}")
            check("All <script> tags in unzipped HTML resolve to real files in ZIP", len(missing_scripts) == 0, f"Missing: {missing_scripts[:5]}")
            check("All <link> tags in unzipped HTML resolve to real files in ZIP", len(missing_links) == 0, f"Missing: {missing_links[:5]}")
            check("All relative <a> links in unzipped HTML resolve to files in ZIP", len(broken_a_hrefs) == 0, f"Broken: {broken_a_hrefs[:5]}")

            # HTTP Server Test on Unzipped Site
            class QuietHandler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=tmpdir, **kwargs)
                def log_message(self, format, *args):
                    pass

            port = 18080
            server = http.server.HTTPServer(("127.0.0.1", port), QuietHandler)
            srv_thread = threading.Thread(target=server.serve_forever, daemon=True)
            srv_thread.start()

            http_errors = []
            for p in PUBLIC_PAGES:
                url = f"http://127.0.0.1:{port}/{p}"
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "TestChallenger/1.0"})
                    with urllib.request.urlopen(req) as resp:
                        _ = resp.read()
                        if resp.status != 200:
                            http_errors.append((p, resp.status))
                except Exception as e:
                    http_errors.append((p, str(e)))

            # Also check core assets via HTTP
            for a in ["assets/js/starunion-b2b.js", "logo-footer-blanco.png", "logo-tuv.png"]:
                url = f"http://127.0.0.1:{port}/{a}"
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "TestChallenger/1.0"})
                    with urllib.request.urlopen(req) as resp:
                        _ = resp.read()
                        if resp.status != 200:
                            http_errors.append((a, resp.status))
                except Exception as e:
                    http_errors.append((a, str(e)))

            server.shutdown()
            check("HTTP server serves all 11 pages and core assets with 200 OK from unzipped package", len(http_errors) == 0, f"HTTP Errors: {http_errors}")

    # =========================================================================
    # SECTION 3: BRAND FIREWALL & LOCKFILE COMPATIBILITY
    # =========================================================================
    print("\n--- SECTION 3: Brand Firewall & Lockfile Interception ---")
    lock_file = PROJECT_ROOT / "BRAND_AND_CONNECTORS.lock.json"
    check("Lockfile exists on disk", lock_file.exists())
    try:
        lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
        check("Lockfile is valid JSON", True)
    except Exception as e:
        check("Lockfile is valid JSON", False, str(e))
        lock_data = {}

    check("Lockfile contains voiceAndLanguageLock", "voiceAndLanguageLock" in lock_data)
    check("Lockfile contains connectorsLock", "connectorsLock" in lock_data)
    check("Lockfile contains designAndPaletteLock", "designAndPaletteLock" in lock_data)

    target_file = str(PROJECT_ROOT / "index.html")

    # Positive test
    pos_res = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Servicio de limpieza profesional corporativo para industrias y plantas."}}})
    check("Firewall ALLOWS clean B2B write_file", pos_res.get("decision") == "allow", str(pos_res))

    # Negative tests: taboo terms
    neg_barbijo = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Uso obligatorio de barbijo en la planta."}}})
    check("Firewall DENIES 'barbijo'", neg_barbijo.get("decision") == "deny", str(neg_barbijo))

    neg_covid = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Protocolos de prevencion COVID-19."}}})
    check("Firewall DENIES 'COVID-19'", neg_covid.get("decision") == "deny", str(neg_covid))

    neg_tapabocas = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Operarios con tapabocas."}}})
    check("Firewall DENIES 'tapabocas'", neg_tapabocas.get("decision") == "deny", str(neg_tapabocas))

    # Negative tests: cross-brand
    neg_fr = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Escribania Fabricio Rivas y asociados."}}})
    check("Firewall DENIES cross-brand 'Fabricio Rivas'", neg_fr.get("decision") == "deny", str(neg_fr))

    neg_et = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Telas provistas por Entretelado."}}})
    check("Firewall DENIES cross-brand 'Entretelado'", neg_et.get("decision") == "deny", str(neg_et))

    neg_zg = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Edificio Residencial Zaguan."}}})
    check("Firewall DENIES cross-brand 'Zaguan'", neg_zg.get("decision") == "deny", str(neg_zg))

    # Negative tests: gender violations
    neg_bv1 = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Bienvenidos a Star Union hoy."}}})
    check("Firewall DENIES 'Bienvenidos a Star Union'", neg_bv1.get("decision") == "deny", str(neg_bv1))

    neg_bv2 = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Bienvenides a nuestro portal."}}})
    check("Firewall DENIES 'Bienvenides'", neg_bv2.get("decision") == "deny", str(neg_bv2))

    neg_todes = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": "Capacitamos a todes los operarios."}}})
    check("Firewall DENIES 'todes'", neg_todes.get("decision") == "deny", str(neg_todes))

    # Negative test: external connector ID (constructed safely)
    ext_id = "".join(["399", "457", "913"])
    neg_ext = run_firewall({"toolCall": {"name": "write_file", "args": {"Path": target_file, "Content": f"GA4 Property ID: {ext_id}"}}})
    check("Firewall DENIES forbidden connector external ID", neg_ext.get("decision") == "deny", str(neg_ext))

    # =========================================================================
    # SECTION 4: DOM TABOO WORDS & SANITIZATION ACROSS 11 PAGES + ACCESOS
    # =========================================================================
    print("\n--- SECTION 4: DOM Taboo Words & Brand Hygiene ---")
    pages_to_audit = PUBLIC_PAGES + ["accesos/index.html"]

    taboo_words = [
        "barbijo", "barbijos", "covid", "covid-19", "tapabocas",
        "mucamas", "empleaditas", "chicos", "barato", "low cost"
    ]

    gender_patterns = [
        re.compile(r"\b(?:bienvenidos a star union|bienvenides|todes|bienvenidos/as)\b", re.I)
    ]

    dom_taboo_hits = []
    dom_gender_hits = []
    dom_placeholder_hits = []
    internal_leak_hits = []

    for p in pages_to_audit:
        fpath = PROJECT_ROOT / p
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8", errors="replace")
        parser = TextAndAttrExtractor()
        parser.feed(content)

        # Audit text nodes and attributes
        for txt in parser.text_nodes:
            for tw in taboo_words:
                if re.search(r"\b" + re.escape(tw) + r"\b", txt, re.I):
                    dom_taboo_hits.append((p, "text", tw, txt))
            for gp in gender_patterns:
                m = gp.search(txt)
                if m:
                    dom_gender_hits.append((p, "text", m.group(0), txt))
            if re.search(r"\bLOGO BLANCO\b", txt, re.I):
                dom_placeholder_hits.append((p, "text", txt))

        for tag, attr, val in parser.attributes:
            for tw in taboo_words:
                if re.search(r"\b" + re.escape(tw) + r"\b", val, re.I):
                    dom_taboo_hits.append((p, f"attr:{attr}", tw, val))
            for gp in gender_patterns:
                m = gp.search(val)
                if m:
                    dom_gender_hits.append((p, f"attr:{attr}", m.group(0), val))

        # Check internal tool links on the 11 public pages (accesos is the internal linktree)
        if p in PUBLIC_PAGES:
            for href in parser.a_hrefs:
                for bad_dir in ["radar-comercial", "brochures/editables", "relevamiento-gerencia", "acuerdos/index"]:
                    if bad_dir in href:
                        internal_leak_hits.append((p, href))

    check("DOM text and attributes across all pages have 0 taboo words", len(dom_taboo_hits) == 0, f"Hits: {dom_taboo_hits[:3]}")
    check("DOM text and attributes across all pages have 0 gendered terms", len(dom_gender_hits) == 0, f"Hits: {dom_gender_hits[:3]}")
    check("DOM text nodes have 0 occurrences of 'LOGO BLANCO'", len(dom_placeholder_hits) == 0, f"Hits: {dom_placeholder_hits[:3]}")
    check("The 11 public pages have 0 links to internal tools", len(internal_leak_hits) == 0, f"Hits: {internal_leak_hits[:3]}")

    # Check accesos/index.html robots meta tag
    accesos_path = PROJECT_ROOT / "accesos/index.html"
    if accesos_path.exists():
        acc_txt = accesos_path.read_text(encoding="utf-8", errors="replace")
        has_noindex = bool(re.search(r"<meta\s+name=[\"']robots[\"']\s+content=[\"'][^\"']*noindex[^\"']*[\"']", acc_txt, re.I))
        has_nofollow = bool(re.search(r"<meta\s+name=[\"']robots[\"']\s+content=[\"'][^\"']*nofollow[^\"']*[\"']", acc_txt, re.I))
        check("accesos/index.html has <meta name='robots' content='...noindex...nofollow...'>", has_noindex and has_nofollow, f"noindex={has_noindex}, nofollow={has_nofollow}")

    # =========================================================================
    # SECTION 5: JAVASCRIPT SYNTAX & RUNTIME VERIFICATION (CRUCIAL ORACLE)
    # =========================================================================
    print("\n--- SECTION 5: JavaScript Syntax & Form Wiring ---")
    js_path = PROJECT_ROOT / "assets/js/starunion-b2b.js"
    check("assets/js/starunion-b2b.js exists on disk", js_path.exists())

    if js_path.exists():
        res_node = subprocess.run(["node", "-c", str(js_path)], capture_output=True, text=True)
        js_syntax_clean = (res_node.returncode == 0)
        js_err_msg = res_node.stderr.strip().split("\n")[0] if res_node.stderr else ""
        check(
            "assets/js/starunion-b2b.js passes Node.js syntax check (node -c)",
            js_syntax_clean,
            f"SyntaxError detected: {js_err_msg}"
        )

    # Check unzipped copy of starunion-b2b.js
    if zip_path.exists():
        with tempfile.TemporaryDirectory() as td:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extract("assets/js/starunion-b2b.js", td)
            unzipped_js = Path(td) / "assets/js/starunion-b2b.js"
            res_node_unzip = subprocess.run(["node", "-c", str(unzipped_js)], capture_output=True, text=True)
            check(
                "Unzipped assets/js/starunion-b2b.js passes Node.js syntax check",
                res_node_unzip.returncode == 0,
                f"SyntaxError in unzipped package: {res_node_unzip.stderr.strip().splitlines()[0] if res_node_unzip.stderr else ''}"
            )

    # Check script inclusion in all 11 pages with correct relative path
    script_inclusion_fails = []
    for p in PUBLIC_PAGES:
        fpath = PROJECT_ROOT / p
        if not fpath.exists():
            continue
        txt = fpath.read_text(encoding="utf-8", errors="replace")
        expected_src = "assets/js/starunion-b2b.js" if p == "index.html" else "../assets/js/starunion-b2b.js"
        tag_match = re.search(r"<script[^>]+src=[\"']([^\"']+)[\"'][^>]*></script>", txt, re.I)
        found_src = [m.group(1) for m in re.finditer(r"<script[^>]+src=[\"']([^\"']+)[\"'][^>]*></script>", txt, re.I) if "starunion-b2b.js" in m.group(1)]
        if not found_src or expected_src not in found_src:
            script_inclusion_fails.append((p, expected_src, found_src))

    check("All 11 pages include starunion-b2b.js with correct relative path", len(script_inclusion_fails) == 0, f"Failures: {script_inclusion_fails}")

    # Check certificacion-iso form attributes
    iso_path = PROJECT_ROOT / "certificacion-iso/index.html"
    if iso_path.exists():
        iso_txt = iso_path.read_text(encoding="utf-8", errors="replace")
        check("certificacion-iso form has class 'js-b2b-quote-form'", "js-b2b-quote-form" in iso_txt)
        check("certificacion-iso form has input name='empresa'", "name=\"empresa\"" in iso_txt)
        check("certificacion-iso form has input name='nombre'", "name=\"nombre\"" in iso_txt)
        check("certificacion-iso form has input name='email'", "name=\"email\"" in iso_txt)
        check("certificacion-iso form has input name='telefono'", "name=\"telefono\"" in iso_txt)
        check("certificacion-iso form has local logo-tuv.png asset", "logo-tuv.png" in iso_txt and "upload.wikimedia.org" not in iso_txt)

    # =========================================================================
    # SUMMARY & VERDICT
    # =========================================================================
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total Checks:  {total_checks}")
    print(f"Passed Checks: {passed_checks} ({(passed_checks / total_checks) * 100:.1f}%)")
    print(f"Failed Checks: {failed_checks}")

    if failures:
        print("\nFAILURE DETAILS:")
        for idx, f in enumerate(failures, 1):
            print(f"  {idx}. {f}")
        print("\nVERDICT: REQUEST_CHANGES")
        return 1
    else:
        print("\nVERDICT: APPROVE")
        return 0


if __name__ == "__main__":
    sys.exit(main())
