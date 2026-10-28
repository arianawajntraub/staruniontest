import re

pages = [
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
    "dossier/index.html"
]

print("=== 5. IMAGE & ASSET AUDIT ===")
for p in pages:
    with open(p, "r", encoding="utf-8") as f:
        html = f.read()
    
    imgs = re.findall(r"<img[^>]*src=[\"\x27]([^\"]*)[\"\x27][^>]*alt=[\"\x27]([^\"]*)[\"\x27]", html, re.I)
    footer_logo = re.findall(r"logo-footer[^\"]*", html)
    cleany_mentions = re.findall(r"cleany[^\"]*", html, re.I)
    print(f"\n--- {p} ({len(imgs)} images) ---")
    print(f"Footer logo ref: {set(footer_logo)}")
    print(f"Cleany refs: {set(cleany_mentions)}")
    for src, alt in imgs[:4]:
        print(f"   [{alt[:30]}]: {src}")
