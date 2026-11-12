#!/usr/bin/env python3
"""
Script de conmutación canónica en 1 clic entre Staging (wajntraub.ar/staruniontest)
y Producción en Hostgator (www.starunion.com.ar).

Uso:
  python3 scripts/preparar_hostgator.py --modo produccion
  python3 scripts/preparar_hostgator.py --modo staging
"""
import argparse
import glob
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING_BASE = "https://wajntraub.ar/staruniontest/"
PROD_BASE = "https://www.starunion.com.ar/"

TARGETS = [
    "index.html",
    "llms.txt",
    "sitemap.xml",
    "limpieza-industrial/index.html",
    "oficinas-corporativas/index.html",
    "universidades-y-clubes/index.html",
    "consorcios/index.html",
    "clinicas-y-hospitales/index.html",
    "limpieza-en-altura/index.html",
    "servicios-especiales/index.html",
    "grandes-superficies/index.html",
    "cobertura-y-operaciones-multi-sede/index.html",
    "cobertura-regional-unificada/index.html",
    "buenos-aires-amba/index.html",
    "bahia-blanca/index.html",
    "neuquen-vaca-muerta/index.html",
    "trelew/index.html",
    "puerto-madryn/index.html",
    "la-empresa/index.html",
    "certificacion-iso/index.html",
    "licitaciones-y-pliegos/index.html",
    "cotizar/index.html",
    "postulaciones/index.html",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["produccion", "staging"], required=True)
    args = parser.parse_args()

    src = STAGING_BASE if args.modo == "produccion" else PROD_BASE
    dst = PROD_BASE if args.modo == "produccion" else STAGING_BASE

    changed = 0
    for rel in TARGETS:
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            txt = f.read()
        new_txt = txt.replace(src, dst)
        if new_txt != txt:
            with open(p, "w", encoding="utf-8") as f:
                f.write(new_txt)
            changed += 1
    print(f"OK: {changed} archivos actualizados a {dst}")

if __name__ == "__main__":
    main()
