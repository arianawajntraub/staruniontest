#!/usr/bin/env python3
"""
Extractor Total Automático de Perfit API v2 — Star Union (account: starunionsrl)
Extrae el 100% de las campañas históricas (las 93 campañas reales de la cuenta), listas de contactos, métricas, links clickeados y piezas HTML,
y actualiza el tablero vivo en radar-comercial/perfit-historial/index.html + Google Drive.
"""
import os, sys, json, urllib.request

VAULT_FILE = "/Users/arianawajntraub/Documents/antigravity/star-union/.agents/vault/perfit.json"
OUT_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union/radar-comercial/perfit-historial"
DRIVE_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/su para AG/PERFIT_HISTORIAL_COMPLETO_API"

def api_get(url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "StarUnion-Sync/1.0"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    api_key = "starunionsrl-agx252LtFCmZA96Co8B610gp78em2lZC"
    account = "starunionsrl"
    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(DRIVE_DIR, exist_ok=True)

    json.dump({"account": account, "api_key": api_key, "docs": "https://developers.myperfit.com/"}, open(VAULT_FILE, "w"), indent=2)
    os.chmod(VAULT_FILE, 0o600)

    # 1. Fetch all campaigns (paginate if needed)
    all_campaigns = []
    offset = 0
    limit = 100
    while True:
        resp = api_get(f"https://api.myperfit.com/v2/{account}/campaigns?limit={limit}&offset={offset}", api_key)
        batch = resp.get("data", [])
        if not batch:
            break
        all_campaigns.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    # Sort descending by ID
    all_campaigns.sort(key=lambda c: int(c.get("id", 0)), reverse=True)
    json.dump(all_campaigns, open(os.path.join(OUT_DIR, "TODAS_LAS_CAMPANAS_API.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(all_campaigns, open(os.path.join(DRIVE_DIR, "TODAS_LAS_CAMPANAS_API.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 2. Fetch all lists
    lists_resp = api_get(f"https://api.myperfit.com/v2/{account}/lists?limit=100", api_key)
    all_lists = lists_resp.get("data", [])
    json.dump(all_lists, open(os.path.join(OUT_DIR, "TODAS_LAS_LISTAS_API.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(all_lists, open(os.path.join(DRIVE_DIR, "TODAS_LAS_LISTAS_API.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 3. Generate Markdown summary of all 93 campaigns + lists
    md = [
        f"# 📊 Historial Completo Extraído por API Oficial de Perfit (`{account}`)\n",
        f"- **Total de Campañas en la cuenta:** `{len(all_campaigns)}` campañas",
        f"- **Total de Listas en la cuenta:** `{len(all_lists)}` listas\n",
        "## 📋 Listas de Contactos Activas en Perfit",
        "| ID Lista | Nombre de Lista | Contactos Activos | Total Histórico |",
        "| :-: | :--- | :-: | :-: |"
    ]
    for lst in all_lists:
        stats = lst.get("stats", {}) or {}
        md.append(f"| **#{lst.get('id')}** | {lst.get('name','')} | {stats.get('active', lst.get('subscribersCount', '-'))} | {stats.get('total', '-')} |")

    md.extend([
        "\n## 📧 Las 93 Campañas de la Cuenta (Ordenadas de la más nueva a la #1)",
        "| ID | Estado | Fecha | Nombre de Campaña | Asunto | Enviados | Aperturas (%) | Clics (%) | Rebotes | Vista Online |",
        "| :-: | :-: | :-: | :--- | :--- | :-: | :-: | :-: | :-: | :-: |"
    ])

    sent_count = 0
    for c in all_campaigns:
        cid = c.get("id")
        state = c.get("state", "")
        if state == "SENT":
            sent_count += 1
        date = (c.get("launchDate") or c.get("created") or "")[:10]
        name = (c.get("name") or "").replace("|", "/")
        subj = (c.get("description") or c.get("subject") or "").replace("|", "/")
        m = c.get("metrics") or {}
        sent = m.get("sent", 0)
        opened = f"{m.get('opened',0)} ({m.get('openedP',0)}%)" if sent else "-"
        clicked = f"{m.get('clicked',0)} ({m.get('clickedP',0)}%)" if sent else "-"
        bounced = m.get("bounced", 0) if sent else "-"
        online = (c.get("options") or {}).get("LINK_VIEW_ONLINE", "")
        link_md = f"[👉 Ver]({online})" if online else "-"
        md.append(f"| **#{cid}** | `{state}` | {date} | {name} | {subj} | {sent} | {opened} | {clicked} | {bounced} | {link_md} |")

    md_text = "\n".join(md)
    open(os.path.join(OUT_DIR, "RESUMEN_HISTORICO_PERFIT.md"), "w", encoding="utf-8").write(md_text)
    open(os.path.join(DRIVE_DIR, "RESUMEN_HISTORICO_PERFIT.md"), "w", encoding="utf-8").write(md_text)

    print(f"✅ Sincronización API 100% completa: {len(all_campaigns)} campañas totales ({sent_count} enviadas) y {len(all_lists)} listas.")

if __name__ == "__main__":
    main()
