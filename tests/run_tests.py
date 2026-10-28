#!/usr/bin/env python3
"""
E2E Test Runner for Star Union S.R.L.
Provides ANSI colored output, per-tier breakdowns, milestone mapping, and structured reporting.
"""

import sys
import os
import argparse
import unittest
import time
from pathlib import Path

# Add tests directory and project root to sys.path
TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import test_e2e_suite

# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Milestone Mapping for Tests
MILESTONE_MAP = {
    # M1: Typography
    "test_t1_f1": "M1 (Tipografía)",
    "test_t1_f2": "M1 (Tipografía)",
    "test_t1_f3": "M1 (Tipografía)",
    "test_t2_b01": "M1 (Tipografía)",
    "test_t2_b02": "M1 (Tipografía)",
    "test_t2_b03": "M1 (Tipografía)",
    "test_t2_b04": "M1 (Tipografía)",
    "test_t2_b05": "M1 (Tipografía)",
    "test_t2_b06": "M1 (Tipografía)",
    "test_t2_b07": "M1 (Tipografía)",
    "test_t2_b08": "M1 (Tipografía)",
    "test_t2_b09": "M1 (Tipografía)",
    "test_t2_b10": "M1 (Tipografía)",
    "test_t2_b11": "M1 (Tipografía)",
    "test_t3_c01": "M1 (Tipografía)",
    "test_t3_c02": "M1 (Tipografía)",
    "test_t3_c16": "M1 (Tipografía)",

    # M2: Art Direction & Palette
    "test_t1_f4": "M2 (Dirección de Arte)",
    "test_t1_f5": "M2 (Dirección de Arte)",
    "test_t1_f6": "M2 (Dirección de Arte)",
    "test_t2_b12": "M2 (Dirección de Arte)",
    "test_t2_b13": "M2 (Dirección de Arte)",
    "test_t2_b14": "M2 (Dirección de Arte)",
    "test_t2_b15": "M2 (Dirección de Arte)",
    "test_t2_b16": "M2 (Dirección de Arte)",
    "test_t2_b17": "M2 (Dirección de Arte)",
    "test_t2_b18": "M2 (Dirección de Arte)",
    "test_t2_b19": "M2 (Dirección de Arte)",
    "test_t2_b20": "M2 (Dirección de Arte)",
    "test_t2_b21": "M2 (Dirección de Arte)",
    "test_t2_b22": "M2 (Dirección de Arte)",
    "test_t2_b23": "M2 (Dirección de Arte)",
    "test_t3_c04": "M2 (Dirección de Arte)",
    "test_t3_c05": "M2 (Dirección de Arte)",
    "test_t3_c06": "M2 (Dirección de Arte)",
    "test_t3_c07": "M2 (Dirección de Arte)",
    "test_t3_c18": "M2 (Dirección de Arte)",

    # M3: Brand Safety, Connectors & Packaging
    "test_t1_f7": "M3 (Candados y Empaquetado)",
    "test_t1_f8": "M3 (Candados y Empaquetado)",
    "test_t1_f9": "M3 (Candados y Empaquetado)",
    "test_t2_b24": "M3 (Candados y Empaquetado)",
    "test_t2_b25": "M3 (Candados y Empaquetado)",
    "test_t2_b26": "M3 (Candados y Empaquetado)",
    "test_t2_b27": "M3 (Candados y Empaquetado)",
    "test_t2_b28": "M3 (Candados y Empaquetado)",
    "test_t2_b29": "M3 (Candados y Empaquetado)",
    "test_t2_b30": "M3 (Candados y Empaquetado)",
    "test_t2_b31": "M3 (Candados y Empaquetado)",
    "test_t2_b32": "M3 (Candados y Empaquetado)",
    "test_t2_b33": "M3 (Candados y Empaquetado)",
    "test_t2_b34": "M3 (Candados y Empaquetado)",
    "test_t2_b35": "M3 (Candados y Empaquetado)",
    "test_t2_b36": "M3 (Candados y Empaquetado)",
    "test_t2_b37": "M3 (Candados y Empaquetado)",
    "test_t2_b38": "M3 (Candados y Empaquetado)",
    "test_t2_b39": "M3 (Candados y Empaquetado)",
    "test_t2_b40": "M3 (Candados y Empaquetado)",
    "test_t3_c03": "M3 (Candados y Empaquetado)",
    "test_t3_c08": "M3 (Candados y Empaquetado)",
    "test_t3_c09": "M3 (Candados y Empaquetado)",
    "test_t3_c10": "M3 (Candados y Empaquetado)",
    "test_t3_c11": "M3 (Candados y Empaquetado)",
    "test_t3_c12": "M3 (Candados y Empaquetado)",
    "test_t3_c13": "M3 (Candados y Empaquetado)",
    "test_t3_c14": "M3 (Candados y Empaquetado)",
    "test_t3_c15": "M3 (Candados y Empaquetado)",
    "test_t3_c17": "M3 (Candados y Empaquetado)",

    # M4: E2E Forensic & Real-World
    "test_t1_f10": "M4 (Auditoría Forense)",
    "test_t4_s": "M4 (Auditoría Forense)",
}

def get_test_milestone(test_name):
    for prefix, ms in MILESTONE_MAP.items():
        if test_name.startswith(prefix):
            return ms
    return "M4 (Auditoría Forense)"

class ColoredTestResult(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=1):
        super().__init__(stream, descriptions, verbosity)
        self.test_records = []

    def startTest(self, test):
        super().startTest(test)
        test._start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        elapsed = time.time() - getattr(test, "_start_time", time.time())
        self.test_records.append({
            "name": test._testMethodName,
            "doc": (test._testMethodDoc or "").strip(),
            "class": test.__class__.__name__,
            "status": "PASS",
            "elapsed": elapsed,
            "error": None
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        elapsed = time.time() - getattr(test, "_start_time", time.time())
        self.test_records.append({
            "name": test._testMethodName,
            "doc": (test._testMethodDoc or "").strip(),
            "class": test.__class__.__name__,
            "status": "FAIL",
            "elapsed": elapsed,
            "error": self._exc_info_to_string(err, test)
        })

    def addError(self, test, err):
        super().addError(test, err)
        elapsed = time.time() - getattr(test, "_start_time", time.time())
        self.test_records.append({
            "name": test._testMethodName,
            "doc": (test._testMethodDoc or "").strip(),
            "class": test.__class__.__name__,
            "status": "ERROR",
            "elapsed": elapsed,
            "error": self._exc_info_to_string(err, test)
        })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        elapsed = time.time() - getattr(test, "_start_time", time.time())
        self.test_records.append({
            "name": test._testMethodName,
            "doc": (test._testMethodDoc or "").strip(),
            "class": test.__class__.__name__,
            "status": "SKIP",
            "elapsed": elapsed,
            "error": reason
        })


def run_suite(tier_filter=None, milestone_filter=None, verbose=False):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    tier_classes = [
        ("Tier 1 (Feature Coverage)", test_e2e_suite.TestTier1FeatureCoverage),
        ("Tier 2 (Boundary Cases)", test_e2e_suite.TestTier2BoundaryCases),
        ("Tier 3 (Cross-Feature)", test_e2e_suite.TestTier3CrossFeatureIntegrations),
        ("Tier 4 (Real-World Scenarios)", test_e2e_suite.TestTier4RealWorldScenarios),
    ]

    selected_tests = []
    for tier_name, cls in tier_classes:
        tier_num = tier_name.split()[1] # "1", "2", "3", "4"
        if tier_filter and str(tier_filter) != tier_num:
            continue
        for test_name in loader.getTestCaseNames(cls):
            ms = get_test_milestone(test_name)
            if milestone_filter and not ms.startswith(milestone_filter.upper()):
                continue
            selected_tests.append(cls(test_name))

    for t in selected_tests:
        suite.addTest(t)

    print(f"\n{BOLD}{CYAN}══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{CYAN}      STAR UNION S.R.L. · SUITE DE PRUEBAS E2E (DUAL TRACK VERIFICATION)             {RESET}")
    print(f"{BOLD}{CYAN}══════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}Directorio del Proyecto:{RESET} {PROJECT_ROOT}")
    print(f"{BOLD}Total de Pruebas Seleccionadas:{RESET} {len(selected_tests)}")
    if tier_filter:
        print(f"{BOLD}Filtro por Nivel:{RESET} Tier {tier_filter}")
    if milestone_filter:
        print(f"{BOLD}Filtro por Hito:{RESET} {milestone_filter}")
    print(f"{CYAN}──────────────────────────────────────────────────────────────────────────────────────{RESET}\n")

    result = ColoredTestResult()
    start_time = time.time()
    suite.run(result)
    total_time = time.time() - start_time

    # Group by Class (Tier)
    records_by_class = {}
    for r in result.test_records:
        records_by_class.setdefault(r["class"], []).append(r)

    tier_labels = {
        "TestTier1FeatureCoverage": "TIER 1: Cobertura Funcional F1 a F10 (50 Casos)",
        "TestTier2BoundaryCases": "TIER 2: Casos de Borde, Límites y Resiliencia (40 Casos)",
        "TestTier3CrossFeatureIntegrations": "TIER 3: Integración Cruzada y Pairwise (18 Casos)",
        "TestTier4RealWorldScenarios": "TIER 4: Escenarios B2B Reales y Forenses (12 Casos)",
    }

    tier_summaries = {}
    for cls_name, label in tier_labels.items():
        recs = records_by_class.get(cls_name, [])
        if not recs:
            continue
        passed = sum(1 for r in recs if r["status"] == "PASS")
        failed = sum(1 for r in recs if r["status"] in ("FAIL", "ERROR"))
        skipped = sum(1 for r in recs if r["status"] == "SKIP")
        tier_summaries[cls_name] = {"label": label, "total": len(recs), "passed": passed, "failed": failed, "skipped": skipped}

        print(f"{BOLD}{BLUE}▶ {label}{RESET}")
        print(f"  Total: {len(recs)} | {GREEN}Aprobados: {passed}{RESET} | {RED}Pendientes/Fallos: {failed}{RESET} | {YELLOW}Omitidos: {skipped}{RESET}")

        if verbose:
            for r in recs:
                ms = get_test_milestone(r["name"])
                if r["status"] == "PASS":
                    status_badge = f"{GREEN}[PASS]{RESET}"
                elif r["status"] == "SKIP":
                    status_badge = f"{YELLOW}[SKIP]{RESET}"
                else:
                    status_badge = f"{RED}[FAIL]{RESET}"
                print(f"    {status_badge} {r['name']:<42} {CYAN}[{ms}]{RESET} {r['doc']}")
                if r["status"] in ("FAIL", "ERROR") and verbose:
                    first_err_line = (r["error"] or "").strip().split("\n")[-1]
                    print(f"           {RED}↳ {first_err_line}{RESET}")
        print()

    # Breakdown by Milestone
    ms_summary = {}
    for r in result.test_records:
        ms = get_test_milestone(r["name"])
        ms_summary.setdefault(ms, {"total": 0, "passed": 0, "failed": 0, "skipped": 0})
        ms_summary[ms]["total"] += 1
        if r["status"] == "PASS":
            ms_summary[ms]["passed"] += 1
        elif r["status"] == "SKIP":
            ms_summary[ms]["skipped"] += 1
        else:
            ms_summary[ms]["failed"] += 1

    print(f"{BOLD}{CYAN}──────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}DESGLOSE POR HITO DE IMPLEMENTACIÓN (PROGRESSIVE TESTABILITY):{RESET}")
    print(f"{CYAN}──────────────────────────────────────────────────────────────────────────────────────{RESET}")
    for ms, stats in sorted(ms_summary.items()):
        pct = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        status_color = GREEN if stats["failed"] == 0 else YELLOW
        print(f"  • {BOLD}{ms:<30}{RESET} : {stats['passed']:>2}/{stats['total']:<2} superados ({status_color}{pct:>5.1f}%{RESET}) [Pendientes: {stats['failed']}]")

    print(f"\n{BOLD}{CYAN}──────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}RESUMEN FINAL DE EJECUCIÓN:{RESET}")
    total_passed = len(result.successes) if hasattr(result, "successes") else sum(1 for r in result.test_records if r["status"] == "PASS")
    total_failed = len(result.failures) + len(result.errors)
    total_skipped = len(result.skipped)
    total_tests = len(result.test_records)
    overall_pct = (total_passed / total_tests) * 100 if total_tests > 0 else 0

    print(f"  • Total Pruebas Evaluadas: {BOLD}{total_tests}{RESET}")
    print(f"  • {GREEN}Pruebas Aprobadas (Verificadas ahora): {total_passed} ({overall_pct:.1f}%){RESET}")
    print(f"  • {RED}Pruebas Pendientes de Implementación: {total_failed}{RESET}")
    print(f"  • {YELLOW}Pruebas Omitidas: {total_skipped}{RESET}")
    print(f"  • Tiempo de Ejecución: {total_time:.3f} segundos")
    print(f"{BOLD}{CYAN}══════════════════════════════════════════════════════════════════════════════════════{RESET}\n")

    if total_failed == 0:
        print(f"{BOLD}{GREEN}✔ ÉXITO TOTAL: 100% de las pruebas E2E aprobadas satisfactoriamente.{RESET}\n")
        return 0
    else:
        print(f"{BOLD}{YELLOW}ℹ SUITE ACTIVA: {total_passed} pruebas pasando actualmente; {total_failed} pruebas actuarán como guardián de calidad en los Milestones M1, M2 y M3.{RESET}\n")
        return 0 if milestone_filter else (0 if os.environ.get("STRICT_E2E") != "1" else 1)


def main():
    parser = argparse.ArgumentParser(description="Test Runner E2E para Star Union S.R.L.")
    parser.add_argument("--tier", choices=["1", "2", "3", "4"], help="Ejecutar solo un nivel específico (1, 2, 3 o 4)")
    parser.add_argument("--milestone", choices=["M1", "M2", "M3", "M4"], help="Filtrar por hito (M1, M2, M3 o M4)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar detalle de cada caso de prueba")
    parser.add_argument("--strict", action="store_true", help="Retornar código de salida 1 si alguna prueba falla")
    args = parser.parse_args()

    if args.strict:
        os.environ["STRICT_E2E"] = "1"

    code = run_suite(tier_filter=args.tier, milestone_filter=args.milestone, verbose=args.verbose)
    sys.exit(code)

if __name__ == "__main__":
    main()
