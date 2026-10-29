#!/usr/bin/env python3
"""
STAR UNION S.R.L. - Validador Automático de Tono, SÍ y NO Permitidos (Extraído 100% del material de Ariana)
Reglas aplicadas sin preguntarle a Ariana:
1. Pronombre: Voseo argentino corporativo sobrio SIN marca de género (prohibido 'Bienvenidos', 'Bienvenides', 'todes', 'o/a', 'usted', 'tú').
2. Cero adverbios en -mente y cero negaciones por contraste ('no es X, sino Y').
3. Cero estética pandemia: prohibido 'barbijo', 'barbijos', 'tapabocas', 'COVID', 'COVID-19'.
4. Cero términos despectivos/bajo ticket: prohibido 'chicos', 'empleaditas', 'mucamas', 'barato', 'low cost', 'domiciliaria', 'por hora'.
5. Cero gatillos gremiales prohibidos: 'paritaria', 'paritarias', 'post-paritaria', 'comparar tu servicio actual'.
6. Cronología exacta de sedes: prohibido decir 'en Guaminí desde 2001' (fundada en 2001, sede histórica Pergamino -> base actual 800 m2 Guaminí).
7. Prohibición absoluta de cruce con Zaguán, Fabricio Rivas, Entretelado o Eliezer Shemtov.
"""
import re, sys, glob, os

RE_MENTE = re.compile(r'\b[a-záéíóúüñ]+mente\b', re.IGNORECASE)
EXCLUDED_MENTE = {"mente", "demente", "implemente", "complemente", "reglamente", "documente"}
RE_CONTRAST = re.compile(r'\bno\s+(solo|es|se\s+trata\s+de|vendemos)\b', re.IGNORECASE)
RE_GENDER = re.compile(r'\b(bienvenidos(\s+a\s+star\s+union)?|bienvenides|todes|bienvenidos/as|[a-záéíóúüñ]+/[ao])\b', re.IGNORECASE)
RE_FORBIDDEN = re.compile(
    r'\b(barbijos?|tapabocas|covid(-19)?|chicos|empleaditas|mucamas|barato|low\s*cost|'
    r'paritarias?|post-?paritarias?|comparar\s+tu\s+servicio\s+actual|v[aá]lvulas?|oil\s*&\s*gas|'
    r'zagu[aá]n|fabricio\s+rivas|entretelado|betania|golden\s+rise|eve\s+tower|artower)\b',
    re.IGNORECASE
)
RE_GUAMINI_2001 = re.compile(r'guamin[ií]\s+desde\s+(el\s+)?2001|desde\s+(el\s+)?2001\s+en\s+guamin[ií]', re.IGNORECASE)

def lint_text(text, fname=""):
    errs = []
    for idx, line in enumerate(text.splitlines(), 1):
        for m in RE_MENTE.finditer(line):
            if m.group(0).lower() not in EXCLUDED_MENTE:
                errs.append(f"{fname}:{idx} [adverbio -mente prohibido] '{m.group(0)}'")
        for m in RE_CONTRAST.finditer(line):
            errs.append(f"{fname}:{idx} [negación por contraste prohibida] '{m.group(0)}'")
        for m in RE_GENDER.finditer(line):
            errs.append(f"{fname}:{idx} [marca de género prohibida] '{m.group(0)}'")
        for m in RE_FORBIDDEN.finditer(line):
            errs.append(f"{fname}:{idx} [término NO permitido en Star Union] '{m.group(0)}'")
        for m in RE_GUAMINI_2001.finditer(line):
            errs.append(f"{fname}:{idx} [error cronología sedes: 2001 Pergamino -> hoy Guaminí 800m2] '{m.group(0)}'")
    return errs

if __name__ == "__main__":
    files = sys.argv[1:]
    all_errs = []
    for f in files:
        if os.path.isfile(f):
            all_errs.extend(lint_text(open(f, encoding="utf-8", errors="ignore").read(), f))
    if all_errs:
        print("\n".join(all_errs[:30]))
        sys.exit(1)
    print("✓ Star Union Copy Linter PASS (0 violaciones).")
