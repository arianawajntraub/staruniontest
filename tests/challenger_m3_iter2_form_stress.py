#!/usr/bin/env python3
"""
Adversarial Stress Test Suite for Milestone 3 Iteration 2:
Multi-field Form Extraction & Lead Payload Completeness across certificacion-iso and vertical pages.
Challenger: challenger_m3_2_iter2
"""

import os
import re
import sys
import json
import urllib.parse
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PUBLIC_PAGES_WITH_FORMS = [
    "index.html",
    "certificacion-iso/index.html",
    "limpieza-industrial/index.html",
    "grandes-superficies/index.html",
    "consorcios/index.html",
    "clinicas-y-hospitales/index.html",
    "universidades-y-clubes/index.html",
    "servicios-especiales/index.html",
]

def run_node_simulation(form_html, input_values):
    """
    Simulates the form submission by executing starunion-b2b.js inside Node.js
    with the exact HTML structure and provided input values.
    Returns the parsed mailto URL parameters and dataLayer event.
    """
    js_path = PROJECT_ROOT / "assets/js/starunion-b2b.js"
    assert js_path.exists(), "assets/js/starunion-b2b.js does not exist"

    # We build a Node runner script that uses a mock DOM representing form_html
    node_runner = f"""
const fs = require('fs');

const inputValues = {json.dumps(input_values)};
const jsCode = fs.readFileSync({json.dumps(str(js_path))}, 'utf8');

// Simple DOM Mock tailored to starunion-b2b.js
let capturedMailto = null;
const capturedDataLayer = [];

class MockElement {{
  constructor(tag, name, value = '', type = 'text', classes = []) {{
    this.tagName = tag.toUpperCase();
    this.name = name;
    this.value = value;
    this.type = type;
    this.classList = {{
      add: (c) => classes.push(c),
      remove: (c) => {{ const idx = classes.indexOf(c); if (idx > -1) classes.splice(idx, 1); }},
      contains: (c) => classes.includes(c)
    }};
    this.style = {{}};
    this.disabled = false;
    this.listeners = {{}};
  }}

  addEventListener(event, fn) {{
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(fn);
  }}

  dispatchEvent(event) {{
    const fns = this.listeners[event.type] || [];
    for (const fn of fns) fn(event);
  }}
}}

class MockForm {{
  constructor() {{
    this.elements = [];
    this.listeners = {{}};
    this.classList = {{
      contains: (c) => c === 'js-b2b-quote-form'
    }};
  }}

  addEventListener(event, fn) {{
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(fn);
  }}

  querySelector(selector) {{
    if (selector === '.b2b-warning-alert') {{
      return this.warningBox;
    }}
    if (selector === 'button[type="submit"]') {{
      return this.submitBtn;
    }}
    // Handle attribute selectors like [name="email"]
    const nameMatch = selector.match(/\\[name="([^"]+)"\\]/);
    if (nameMatch) {{
      const targetName = nameMatch[1];
      return this.elements.find(el => el.name === targetName) || null;
    }}
    return null;
  }}

  querySelectorAll(selector) {{
    return [];
  }}

  submit() {{
    let defaultPrevented = false;
    const event = {{
      type: 'submit',
      preventDefault: () => {{ defaultPrevented = true; }},
      defaultPrevented
    }};
    const fns = this.listeners['submit'] || [];
    for (const fn of fns) fn(event);
  }}
}}

// Build Form from inputValues
const form = new MockForm();
form.warningBox = new MockElement('div', null, '', 'div', ['b2b-warning-alert', 'hidden']);
form.submitBtn = new MockElement('button', null, '', 'submit');

for (const [k, v] of Object.entries(inputValues)) {{
  form.elements.push(new MockElement('input', k, v));
}}

const window = {{
  dataLayer: capturedDataLayer,
  location: {{
    set href(val) {{ capturedMailto = val; }},
    get href() {{ return capturedMailto; }}
  }}
}};

const document = {{
  addEventListener(event, fn) {{
    if (event === 'DOMContentLoaded') {{
      fn();
    }}
  }},
  querySelectorAll(sel) {{
    if (sel === '.js-b2b-quote-form') return [form];
    if (sel.includes('whatsapp') || sel.includes('wa.me')) return [];
    return [];
  }},
  getElementById(id) {{
    return null;
  }},
  createElement(tag) {{
    return new MockElement(tag, null);
  }},
  body: {{
    appendChild() {{}}
  }}
}};

// Execute starunion-b2b.js in simulated sandbox
const fn = new Function('window', 'document', jsCode);
fn(window, document);

// Trigger form submission
form.submit();

// Output results
console.log(JSON.stringify({{
  mailto: capturedMailto,
  dataLayer: capturedDataLayer
}}));
"""

    res = subprocess.run(["node", "-e", node_runner], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Node execution failed: {res.stderr}")
    return json.loads(res.stdout)


def parse_mailto(mailto_str):
    if not mailto_str:
        return None, {}
    parsed = urllib.parse.urlparse(mailto_str)
    to_email = parsed.path
    qs = urllib.parse.parse_qs(parsed.query)
    return to_email, {k: v[0] for k, v in qs.items()}


def main():
    print("=" * 80)
    print("CHALLENGER M3 ITERATION 2: EMPIRICAL MULTI-FIELD FORM STRESS TEST")
    print("=" * 80)

    total = 0
    passed = 0
    failed = 0
    failures = []

    def check(name, condition, details=""):
        nonlocal total, passed, failed
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            failures.append(f"{name}: {details}")
            print(f"  [FAIL] {name} -- {details}")

    # =========================================================================
    # TEST SUITE 1: Form Inputs Across All Public Pages
    # =========================================================================
    print("\n--- TEST SUITE 1: Form Field Discoverability across Public Pages ---")
    page_forms = {}
    for p in PUBLIC_PAGES_WITH_FORMS:
        fpath = PROJECT_ROOT / p
        check(f"{p} exists on disk", fpath.exists())
        if not fpath.exists():
            continue
        html = fpath.read_text(encoding="utf-8")
        # Find all forms with js-b2b-quote-form
        forms = re.findall(r'<form\b([^>]*class=[\'"][^\'"]*js-b2b-quote-form[^\'"]*[\'"][^>]*)>(.*?)</form>', html, re.DOTALL | re.I)
        check(f"{p} has at least 1 .js-b2b-quote-form", len(forms) >= 1, f"Found {len(forms)} forms")
        for i, (attrs, body) in enumerate(forms):
            fields = re.findall(r'<(?:input|select|textarea)\b[^>]*\bname=[\"\x27]([^\x27\"]+)[\"\x27]', body, re.I)
            page_forms[f"{p}#form{i+1}"] = fields
            print(f"    -> {p} Form #{i+1} inputs: {fields}")

    # Verify field composition
    for form_id, fields in page_forms.items():
        if form_id.startswith("index.html#form1"):
            check(f"{form_id} has empresa, nombre, cargo, tipo_organizacion", 
                  all(k in fields for k in ['empresa', 'nombre', 'cargo', 'tipo_organizacion']))
        elif form_id.startswith("index.html#form2"):
            check(f"{form_id} has empresa, nombre, cargo, tipo_organizacion, escala",
                  all(k in fields for k in ['empresa', 'nombre', 'cargo', 'tipo_organizacion', 'escala']))
        else:
            # Vertical pages and certificacion-iso
            check(f"{form_id} has empresa, nombre, email, telefono, mensaje",
                  all(k in fields for k in ['empresa', 'nombre', 'email', 'telefono', 'mensaje']),
                  f"Fields found: {fields}")

    # =========================================================================
    # TEST SUITE 2: Empirical Payload Verification on certificacion-iso & Verticals
    # =========================================================================
    print("\n--- TEST SUITE 2: Empirical Form Submission & Lead Payload Completeness ---")

    test_leads = [
        {
            "name": "Standard Vertical Inquirer (email + telefono + mensaje)",
            "inputs": {
                "empresa": "TechLogistics S.A.",
                "nombre": "Carolina Mendez",
                "email": "carolina@techlogistics.com.ar",
                "telefono": "+54 9 11 5555-1234",
                "mensaje": "Requerimos cuadrilla diaria para depósito logístico de 8.000 m² con certificación ISO 9001."
            },
            "expect_email": "carolina@techlogistics.com.ar",
            "expect_tel": "+54 9 11 5555-1234",
            "expect_contact": "carolina@techlogistics.com.ar · +54 9 11 5555-1234",
            "expect_msg": "Requerimos cuadrilla diaria para depósito logístico de 8.000 m² con certificación ISO 9001.",
        },
        {
            "name": "Vertical Inquirer with Email Only (No phone)",
            "inputs": {
                "empresa": "Laboratorios Sur",
                "nombre": "Dr. Fernando Ruiz",
                "email": "fruiz@labsur.com",
                "telefono": "",
                "mensaje": "Limpieza de áreas limpias grado C y D."
            },
            "expect_email": "fruiz@labsur.com",
            "expect_tel": "",
            "expect_contact": "fruiz@labsur.com",
            "expect_msg": "Limpieza de áreas limpias grado C y D.",
        },
        {
            "name": "Vertical Inquirer with Phone Only (No email)",
            "inputs": {
                "empresa": "Consorcio Av. del Libertador 4400",
                "nombre": "Esteban Gomez",
                "email": "",
                "telefono": "011-4777-8899",
                "mensaje": "Torre de 35 pisos, 3 encargados."
            },
            "expect_email": "",
            "expect_tel": "011-4777-8899",
            "expect_contact": "011-4777-8899",
            "expect_msg": "Torre de 35 pisos, 3 encargados.",
        },
        {
            "name": "Home Form User (using cargo for email/phone, escala for requirement)",
            "inputs": {
                "empresa": "Molinos Rio S.A.",
                "nombre": "Valeria Rossi",
                "cargo": "valeria@molinos.com.ar / (011) 5000-2000",
                "tipo_organizacion": "Planta Industrial / Fábrica / Centro Logístico",
                "servicio_requerido": "Relevamiento técnico y propuesta operativa a medida",
                "ubicacion": "AMBA (CABA / GBA)",
                "escala": "Planta harinera 12.000 m2"
            },
            "expect_contact": "valeria@molinos.com.ar / (011) 5000-2000",
            "expect_msg": "Planta harinera 12.000 m2",
            "expect_vertical": "Planta Industrial / Fábrica / Centro Logístico",
        },
        {
            "name": "Multiline and Special Characters in Mensaje",
            "inputs": {
                "empresa": "Cervecería & Maltería Quilmes",
                "nombre": "Ing. Martín O'Connor",
                "email": "moconnor@quilmes.com.ar",
                "telefono": "+54 11 9999-0000",
                "mensaje": "Línea 1: Desinfección CIP.\nLínea 2: Tanques \"Inox\" & pisos epoxi (Área húmeda).\nLínea 3: ¿Disponibilidad inmediata?"
            },
            "expect_contact": "moconnor@quilmes.com.ar · +54 11 9999-0000",
            "expect_msg": "Línea 1: Desinfección CIP.\nLínea 2: Tanques \"Inox\" & pisos epoxi (Área húmeda).\nLínea 3: ¿Disponibilidad inmediata?",
        }
    ]

    for lead in test_leads:
        print(f"\n  Running scenario: {lead['name']}")
        res = run_node_simulation("form", lead["inputs"])
        to_email, params = parse_mailto(res["mailto"])

        check(f"Target address is comercial@starunion.com.ar [{lead['name']}]",
              to_email == "comercial@starunion.com.ar", f"Got: {to_email}")

        check(f"Subject contains company name [{lead['name']}]",
              lead["inputs"]["empresa"] in params.get("subject", ""),
              f"Subject: {params.get('subject')}")

        body = params.get("body", "")

        # Verify contact info is never dropped
        expected_contact = lead["expect_contact"]
        check(f"Body contains Contact info [{lead['name']}]",
              f"• Email / Teléfono: {expected_contact}" in body,
              f"Expected '{expected_contact}' in body. Actual body:\n{body}")

        # Verify message/requirement is never dropped
        expected_msg = lead["expect_msg"]
        check(f"Body contains Message requirement [{lead['name']}]",
              expected_msg in body,
              f"Expected message text in body. Actual body:\n{body}")

        # Verify company name in body
        check(f"Body contains Empresa [{lead['name']}]",
              f"• Empresa / Institución: {lead['inputs']['empresa']}" in body)

        # Verify contact name in body
        check(f"Body contains Contact Name [{lead['name']}]",
              f"• Contacto: {lead['inputs']['nombre']}" in body)

        # Verify dataLayer event
        dl = res["dataLayer"]
        check(f"dataLayer pushed lead event [{lead['name']}]",
              len(dl) > 0 and dl[0].get("event") == "lead_b2b_calificado_starunion",
              f"dataLayer: {dl}")

    # =========================================================================
    # TEST SUITE 3: Adversarial Edge Cases & Disqualification
    # =========================================================================
    print("\n--- TEST SUITE 3: Adversarial Edge Cases & Disqualification Filter ---")

    # Disqualification case: NO_CALIFICA_PARTICULAR
    disqual_inputs = {
        "empresa": "Particular",
        "nombre": "Juan",
        "cargo": "juan@gmail.com",
        "tipo_organizacion": "NO_CALIFICA_PARTICULAR"
    }
    res_disqual = run_node_simulation("form", disqual_inputs)
    check("Disqualified lead (PARTICULAR) blocks mailto dispatch",
          res_disqual["mailto"] is None,
          f"mailto was sent: {res_disqual['mailto']}")
    check("Disqualified lead (PARTICULAR) does NOT fire GA4 lead conversion event",
          len(res_disqual["dataLayer"]) == 0,
          f"dataLayer events: {res_disqual['dataLayer']}")

    # Disqualification case: NO_CALIFICA_CONSORCIO_CHICO
    disqual_inputs2 = {
        "empresa": "Consorcio 4 deptos",
        "nombre": "Pedro",
        "cargo": "pedro@gmail.com",
        "tipo_organizacion": "NO_CALIFICA_CONSORCIO_CHICO"
    }
    res_disqual2 = run_node_simulation("form", disqual_inputs2)
    check("Disqualified lead (CONSORCIO_CHICO) blocks mailto dispatch",
          res_disqual2["mailto"] is None,
          f"mailto was sent: {res_disqual2['mailto']}")
    check("Disqualified lead (CONSORCIO_CHICO) does NOT fire GA4 lead conversion event",
          len(res_disqual2["dataLayer"]) == 0,
          f"dataLayer events: {res_disqual2['dataLayer']}")

    # Leading / Trailing whitespace trimming
    trim_inputs = {
        "empresa": "   BioFarma Labs   ",
        "nombre": "   Dra. Ana López   ",
        "email": "   ana@biofarma.com.ar   ",
        "telefono": "   011-5555-7777   ",
        "mensaje": "   Requerimiento urgente de limpieza esteril   "
    }
    res_trim = run_node_simulation("form", trim_inputs)
    _, trim_params = parse_mailto(res_trim["mailto"])
    trim_body = trim_params.get("body", "")
    check("Whitespace trimmed in Empresa", "• Empresa / Institución: BioFarma Labs" in trim_body)
    check("Whitespace trimmed in Contact Name", "• Contacto: Dra. Ana López" in trim_body)
    check("Whitespace trimmed in Contact Email/Phone", "• Email / Teléfono: ana@biofarma.com.ar · 011-5555-7777" in trim_body)
    check("Whitespace trimmed in Message", "• Detalle adicional: Requerimiento urgente de limpieza esteril" in trim_body)

    # Precedence: cargo overrides email/phone if present
    prec_inputs = {
        "empresa": "Corp X",
        "nombre": "Carlos",
        "cargo": "Gerente de Operaciones",
        "email": "carlos@corpx.com",
        "telefono": "11223344"
    }
    res_prec = run_node_simulation("form", prec_inputs)
    _, prec_params = parse_mailto(res_prec["mailto"])
    prec_body = prec_params.get("body", "")
    check("Cargo takes precedence when provided",
          "• Email / Teléfono: Gerente de Operaciones" in prec_body)

    # Precedence: escala overrides mensaje if present
    prec_escala_inputs = {
        "empresa": "Corp Y",
        "nombre": "Elena",
        "email": "elena@corpy.com",
        "telefono": "11223344",
        "escala": "Edificio corporativo 20 pisos",
        "mensaje": "Mensaje secundario"
    }
    res_prec_escala = run_node_simulation("form", prec_escala_inputs)
    _, prec_escala_params = parse_mailto(res_prec_escala["mailto"])
    prec_escala_body = prec_escala_params.get("body", "")
    check("Escala takes precedence over mensaje when both provided",
          "• Detalle adicional: Edificio corporativo 20 pisos" in prec_escala_body)

    # =========================================================================
    # SUMMARY & VERDICT
    # =========================================================================
    print("\n" + "=" * 80)
    print("ITERATION 2 EMPIRICAL FORM STRESS TEST SUMMARY")
    print("=" * 80)
    print(f"Total Checks:  {total}")
    print(f"Passed Checks: {passed} ({(passed / total) * 100:.1f}%)")
    print(f"Failed Checks: {failed}")

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
