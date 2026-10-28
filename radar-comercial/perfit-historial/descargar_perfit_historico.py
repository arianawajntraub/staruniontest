#!/usr/bin/env python3
"""
Descargador Automático de Historial Perfit — Star Union S.R.L.
Lee todos los links compartidos de /Users/arianawajntraub/Documents/antigravity/star-union/PERFIT_LINKS_HISTORICOS.md,
consulta la API pública de shares de Perfit y guarda en radar-comercial/perfit-historial/:
- Métricas de cada campaña (enviados, aperturas, clics, rebotes)
- Ranking de botones/links clickeados
- HTML completo de la pieza y textos por vertical
- Todas las imágenes ya recortadas del CDN de Perfit
- Un resumen maestro unificado (RESUMEN_HISTORICO_PERFIT.md) para que el chat lo lea al instante.
"""
import os
import re
import json
import urllib.request

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"
MD_FILE = os.path.join(BASE_DIR, "PERFIT_LINKS_HISTORICOS.md")
OUT_DIR = os.path.join(BASE_DIR, "radar-comercial/perfit-historial")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(MD_FILE):
        print("No se encontró PERFIT_LINKS_HISTORICOS.md")
        return

    text = open(MD_FILE, encoding="utf-8").read()
    matches = re.findall(r"https://app\.myperfit\.com/shares/([^/\s]+)/campaigns/([a-f0-9]+)/(\d+)", text)
    if not matches:
        print("No se encontraron links de Perfit en PERFIT_LINKS_HISTORICOS.md")
        return

    summary_lines = [
        "# 📊 Resumen Histórico Unificado de Mailings Perfit — Star Union S.R.L.\n",
        "| ID | Campaña | Fecha Envío | Asunto | Entregados | Aperturas | Clics Únicos | Pieza Online |",
        "| :-: | :--- | :--- | :--- | :-: | :-: | :-: | :--- |"
    ]
    details_lines = ["\n---\n## 🔍 Detalle de Clics, Textos y Fotos Recortadas por Campaña\n"]

    seen = set()
    for account, token, cid in matches:
        if cid in seen:
            continue
        seen.add(cid)
        api_c = f"https://api.myperfit.com/v2/shares/{account}/campaigns/{token}/{cid}"
        api_l = f"https://api.myperfit.com/v2/shares/{account}/campaigns/{token}/{cid}/links/metrics"

        try:
            c_data = json.loads(urllib.request.urlopen(api_c, timeout=10).read().decode("utf-8"))["data"]
            l_data = json.loads(urllib.request.urlopen(api_l, timeout=10).read().decode("utf-8")).get("data", [])
        except Exception as e:
            print(f"Error descargando campaña {cid}: {e}")
            continue

        json.dump(c_data, open(os.path.join(OUT_DIR, f"campana_{cid}_metricas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(l_data, open(os.path.join(OUT_DIR, f"campana_{cid}_links.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

        name = c_data.get("name", "")
        subj = c_data.get("description", "")
        date = (c_data.get("launchDate") or "")[:10]
        m = c_data.get("metrics", {})
        online_url = c_data.get("options", {}).get("LINK_VIEW_ONLINE", "")
        thumb = c_data.get("thumbnail", "")

        summary_lines.append(
            f"| **#{cid}** | {name} | {date} | {subj} | {m.get('sent',0)} ({m.get('sentP',0)}%) | {m.get('opened',0)} ({m.get('openedP',0)}%) | {m.get('clicked',0)} ({m.get('clickedP',0)}%) | [Ver Pieza]({online_url}) |"
        )

        details_lines.append(f"### 📧 Campaña #{cid}: {name} ({date})")
        details_lines.append(f"- **Asunto:** `{subj}`")
        details_lines.append(f"- **Miniatura completa:** {thumb}")
        details_lines.append(f"- **Versión online HTML:** {online_url}")
        details_lines.append("- **Botones más clickeados:**")
        for lk in l_data:
            details_lines.append(f"  - `{lk.get('clicks',0)} clics` → **{lk.get('name','')}** ({lk.get('url','')})")

        if online_url:
            try:
                html_body = urllib.request.urlopen(online_url, timeout=10).read().decode("utf-8", errors="ignore")
                open(os.path.join(OUT_DIR, f"campana_{cid}_pieza.html"), "w", encoding="utf-8").write(html_body)
                imgs = [i for i in re.findall(r'src="([^"]+)"', html_body) if "cdn.myperfit.net" in i]
                if imgs:
                    details_lines.append("- **Fotos ya recortadas y curadas en CDN de Perfit:**")
                    for im in imgs:
                        details_lines.append(f"  - {im}")
            except Exception:
                pass
        details_lines.append("")

    report_path = os.path.join(OUT_DIR, "RESUMEN_HISTORICO_PERFIT.md")
    open(report_path, "w", encoding="utf-8").write("\n".join(summary_lines + details_lines))
    print(f"✅ Descargadas {len(seen)} campañas en {report_path}")

if __name__ == "__main__":
    main()
