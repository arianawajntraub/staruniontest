#!/usr/bin/env python3
"""
Auditor M2 Forensic Verification Script
Independently verifies art direction, palette refinement, and brand integrity for Milestone 2.
"""
import os
import re
import sys

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"

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
]

ALL_PAGES = PUBLIC_PAGES + ["dossier/index.html"]

errors = []

def record_error(msg):
    errors.append(msg)
    print(f"❌ FAIL: {msg}")

def record_pass(msg):
    print(f"✔ PASS: {msg}")

print("================================================================================")
print("🔍 AUDITOR M2 INDEPENDENT FORENSIC VERIFICATION")
print("================================================================================")

# 1. HERO B2B REDESIGN AUTHENTICITY
print("\n--- CHECK 1: Hero B2B Redesign Authenticity (index.html) ---")
with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()

# Check section background
if 'class="bg-white pt-16 pb-20 border-b border-gray-100 relative overflow-hidden"' in index_html:
    record_pass("Hero container uses bg-white with subtle gray bottom border")
else:
    record_error("Hero container does not match expected B2B white styling")

# Check H1 color
if 'class="text-5xl md:text-6xl lg:text-[4.25rem] font-extrabold tracking-tight mb-6 leading-[1.08] text-[#000000]"' in index_html:
    record_pass("Hero H1 uses dark text #000000")
else:
    record_error("Hero H1 does not match expected #000000 styling")

# Check primary CTA
if 'bg-brand hover:bg-brand-dark text-white font-bold px-8 py-4 rounded-lg shadow-sm transition' in index_html:
    record_pass("Hero primary CTA uses institutional green bg-brand with white text")
else:
    record_error("Hero primary CTA not found or improperly styled")

# Check secondary CTA
if 'bg-white text-brand border border-gray-200 hover:bg-gray-50 font-bold px-7 py-4 rounded-lg shadow-sm transition' in index_html:
    record_pass("Hero secondary CTA uses white button with gray border and green text")
else:
    record_error("Hero secondary CTA not found or improperly styled")

# Check upper badge and micro-star
if '<span class="text-accent">★</span>' in index_html and 'bg-gray-100 border border-gray-200 text-gray-800' in index_html:
    record_pass("Hero upper badge has micro yellow star accent")
else:
    record_error("Hero upper badge missing micro yellow star accent")

# Check red alert elimination
if 'bg-red-50' in index_html or 'border-red-200' in index_html or 'text-red-800' in index_html:
    record_error("Red warning classes still present in index.html")
else:
    record_pass("Red warning classes completely eradicated from index.html")

# 2. FOOTER UNIFICATION ACROSS ALL 10 PUBLIC PAGES + TEMPLATE
print("\n--- CHECK 2: Footer Unification Across All 10 Public Pages + footer.html ---")
footer_files = PUBLIC_PAGES + ["footer.html"]
for page in footer_files:
    fpath = os.path.join(BASE_DIR, page)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    footer_m = re.search(r'<footer[^>]*class=[\"\']([^\"\']+)[\"\'][^>]*>([\s\S]*?)</footer>', content)
    if not footer_m:
        record_error(f"{page}: Missing <footer> element")
        continue
    
    fclasses = footer_m.group(1)
    fbody = footer_m.group(2)

    if 'bg-[#133522]' not in fclasses:
        record_error(f"{page}: Footer missing bg-[#133522]")
    
    if 'text-[#ffcc29]' in fbody:
        record_error(f"{page}: Footer contains text-[#ffcc29] (yellow labels)")
    
    if 'hover:text-[#ffcc29]' in fbody:
        record_error(f"{page}: Footer contains hover:text-[#ffcc29] (yellow link hover)")
        
    if 'bg-[#ffcc29]' in fbody or 'bg-accent' in fbody:
        record_error(f"{page}: Footer contains yellow button (bg-[#ffcc29] or bg-accent)")
        
    if 'bg-white hover:bg-gray-100 text-brand' not in fbody:
        record_error(f"{page}: Footer missing corporate white button (bg-white hover:bg-gray-100 text-brand)")

    # Check for duplicate comments
    if '<!-- FOOTER OFICIAL UNIFICADO (#133522 CON LOGO BLANCO REAL) -->\n        <!-- FOOTER OFICIAL UNIFICADO' in content:
        record_error(f"{page}: Duplicate consecutive footer comments detected")

record_pass(f"All {len(footer_files)} footer files verified clean, unified, and free of Brazil-flag contrast")

# 3. PALETTE PURITY & FORBIDDEN CLASSES
print("\n--- CHECK 3: Palette Purity & Zero Forbidden Classes Across All 11 Pages ---")
forbidden_classes = ["blue-", "indigo-", "sky-", "orange-", "cyan-", "purple-"]
for page in ALL_PAGES:
    fpath = os.path.join(BASE_DIR, page)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for fc in forbidden_classes:
        m = re.findall(r'class=[\"\'][^\"\']*?\b' + fc + r'[^\"\']*?[\"\']', content)
        if m:
            record_error(f"{page}: Forbidden class '{fc}' found: {m}")

# Check rogue hexes
rogue_hexes = ["#057a3f", "#023d1f", "#e6b822"]
for page in ALL_PAGES:
    fpath = os.path.join(BASE_DIR, page)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for rh in rogue_hexes:
        if rh in content:
            record_error(f"{page}: Rogue hex '{rh}' found")

record_pass("Zero forbidden classes and zero rogue hexes across all 11 pages")

# 4. BRAND LOCK COMPLIANCE
print("\n--- CHECK 4: Brand Lock Compliance ---")
forbidden_brand_terms = [
    "Fabricio Rivas",
    "rivas-2026",
    "399457913",
    "536338759",
    "552000200",
    "Entretelado",
    "entretelado.com.ar",
    "Zaguán",
    "zaguan",
    "Bienvenides",
    "bienvenides",
    "todes",
    "Todes",
    "Bienvenidos a Star Union",
]
for page in ALL_PAGES:
    fpath = os.path.join(BASE_DIR, page)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    for fbt in forbidden_brand_terms:
        if fbt in content:
            record_error(f"{page}: Forbidden brand term '{fbt}' detected")

# Check for visible "LOGO BLANCO" text nodes
for page in ALL_PAGES:
    fpath = os.path.join(BASE_DIR, page)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    clean = re.sub(r"<!--[\s\S]*?-->", "", content)
    hits = re.findall(r">[^<]*\bLOGO BLANCO\b[^<]*<", clean, re.IGNORECASE)
    if hits:
        record_error(f"{page}: Visible 'LOGO BLANCO' placeholder text found: {hits}")

record_pass("Brand locks verified clean (zero gendered terms, zero cross-contamination, zero visible placeholders)")

# SUMMARY & VERDICT
print("\n================================================================================")
if errors:
    print(f"❌ AUDIT FAILED with {len(errors)} error(s). Verdict: INTEGRITY VIOLATION")
    sys.exit(1)
else:
    print("✔ AUDIT SUCCESS: All forensic checks passed. Verdict: CLEAN")
    sys.exit(0)
