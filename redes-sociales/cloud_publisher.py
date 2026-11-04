#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Publicación 100% en la Nube (GitHub Actions Cloud Runner) conectado en vivo a APROBALO.
- Fuente de verdad centralizada: Aprobalo (https://aprobala-app.943ari.workers.dev).
- Corre en los servidores de GitHub (Ubuntu Cloud) con hora Argentina (UTC-3),
  sin depender de ninguna computadora prendida.
- Cuando una pieza aprobada llega a su fecha/hora de salida, la publica en:
  Instagram (Carrusel + Story Video + Reel 12s), Facebook (Page + Reel),
  LinkedIn (Página Empresa), YouTube Shorts y TikTok (con Copy Completo),
  y la marca automáticamente como PUBLICADA dentro de Aprobalo.
"""
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Si corre en GitHub Actions, hidrata .agents/vault/social_keys.json desde el Secret encriptado
secret_json = os.environ.get("STARUNION_SOCIAL_KEYS_JSON", "").strip()
vault_dir = os.path.join(ROOT_DIR, ".agents", "vault")
vault_path = os.path.join(vault_dir, "social_keys.json")
if secret_json:
    os.makedirs(vault_dir, exist_ok=True)
    with open(vault_path, "w", encoding="utf-8") as vf:
        vf.write(secret_json)

import starunion_api_server as srv

APROBALA_URL = "https://aprobala-app.943ari.workers.dev"
APROBALA_CUENTA_SU = "6e090d5e-8342-42b6-a355-8769bfaa85f3"


def fetch_aprobala_piece(cm_token, aprobala_id):
    if not cm_token or not aprobala_id:
        return None
    req = urllib.request.Request(
        f"{APROBALA_URL}/api/v1/piezas/{aprobala_id}",
        headers={
            "Authorization": f"Bearer {cm_token}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"[APROBALO-SYNC] Aviso leyendo {aprobala_id}: {e}")
        return None


def mark_aprobala_published(prod_token, aprobala_id, live_url):
    if not prod_token or not aprobala_id:
        return
    try:
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        # 1. Obtener cookie de sesión de Productora
        req_login = urllib.request.Request(
            f"{APROBALA_URL}/p/{prod_token}",
            headers={"User-Agent": ua},
            method="GET",
        )
        try:
            resp = urllib.request.urlopen(req_login, timeout=15)
            cookie = resp.headers.get("Set-Cookie", "").split(";")[0]
        except urllib.error.HTTPError as he:
            cookie = he.headers.get("Set-Cookie", "").split(";")[0]
        if not cookie:
            return
        # 2. Marcar publicada en Aprobalo
        body = urllib.parse.urlencode({"url_publicada": live_url or "https://www.instagram.com/starunion.ar/"}).encode("utf-8")
        req_pub = urllib.request.Request(
            f"{APROBALA_URL}/piezas/{aprobala_id}/publicada",
            data=body,
            headers={
                "Cookie": cookie,
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": ua,
            },
            method="POST",
        )
        urllib.request.urlopen(req_pub, timeout=15)
        print(f"[APROBALO-SYNC] Pieza {aprobala_id} marcada como PUBLICADA en Aprobalo ({live_url}).")
    except Exception as e:
        print(f"[APROBALO-SYNC] Aviso marcando publicada en Aprobalo: {e}")


def main():
    sched_path = os.path.join(ROOT_DIR, "redes-sociales", "calendario_programado.json")
    if not os.path.exists(sched_path):
        print("No existe calendario_programado.json")
        return

    with open(sched_path, "r", encoding="utf-8") as f:
        sched = json.load(f)

    ar_tz = datetime.timezone(datetime.timedelta(hours=-3))
    now_ar = datetime.datetime.now(ar_tz).strftime("%Y-%m-%dT%H:%M")
    print(f"[CLOUD-PUBLISHER] Hora Argentina actual: {now_ar}")

    keys = srv.load_keys()
    cm_tok = keys.get("aprobala_cm_token", "")
    prod_tok = keys.get("aprobala_prod_token", "")
    changed = False

    for pid in sorted(sched.keys()):
        p = sched[pid]
        ap_id = p.get("aprobala_id", "")

        # 1. Sincronizar estado, fecha y copies en vivo desde Aprobalo (Fuente Única de Verdad)
        ap_piece = fetch_aprobala_piece(cm_tok, ap_id)
        if ap_piece:
            ap_estado = ap_piece.get("estado", "")
            ap_fecha = ap_piece.get("fecha", "")
            ap_datos = ap_piece.get("datos", {}) or {}
            ap_copies = ap_datos.get("copies", {}) or {}
            ap_yt = (ap_datos.get("yt", {}) or {}).get("Español", {}) or {}

            if ap_estado == "publicada" and p.get("status") != "publicado":
                p["status"] = "publicado"
                changed = True
            elif ap_estado == "aprobada" and p.get("status") not in ("publicado", "aprobado"):
                p["status"] = "aprobado"
                changed = True

            if ap_fecha and len(ap_fecha) == 10:
                hora_previa = (p.get("scheduled_at") or "T10:00").split("T")[-1]
                nuevo_sched = f"{ap_fecha}T{hora_previa}"
                if nuevo_sched != p.get("scheduled_at"):
                    p["scheduled_at"] = nuevo_sched
                    changed = True

            cp_ig = (ap_copies.get("Instagram", {}) or {}).get("Español") or (ap_copies.get("madre", {}) or {}).get("Español")
            cp_li = (ap_copies.get("LinkedIn", {}) or {}).get("Español")
            cp_tt = (ap_copies.get("TikTok", {}) or {}).get("Español") or cp_ig
            if cp_ig:
                p["copy_ig_fb"] = cp_ig
            if cp_li:
                p["copy_linkedin"] = cp_li
            if cp_tt:
                p["copy_tiktok"] = cp_tt
            if ap_yt.get("titulo"):
                p["yt_title"] = ap_yt["titulo"]
            if ap_yt.get("desc"):
                p["yt_desc"] = ap_yt["desc"]
            if ap_yt.get("tags"):
                p["yt_tags"] = ap_yt["tags"]

        st = p.get("status", "")
        sched_at = p.get("scheduled_at", "")
        ap_estado_actual = (ap_piece or {}).get("estado", "")
        today_ar = now_ar[:10]
        # REGLA DE HIERRO: Solo publicar si en Aprobalo está explícitamente "aprobada" (jamás "programado" ni "borrador") y su fecha es hoy
        if ap_estado_actual == "aprobada" and st == "aprobado" and sched_at and sched_at[:10] == today_ar and sched_at <= now_ar:
            print(f"[CLOUD-PUBLISHER] Disparando pieza #{pid} (Aprobalo ID: {ap_id}) programada para {sched_at}...")
            chs = p.get("channels") or ["ig_feed", "ig_story", "ig_reel", "fb_page", "fb_story", "fb_reel", "linkedin", "gmb", "youtube", "tiktok"]
            feed_f = (p.get("carousel_files") or [p.get("feed_file", "")])[0]
            story_f = p.get("story_video_file") or p.get("story_file", "")
            reel_f = p.get("reel_file", "")
            cap_ig = p.get("copy_ig_fb", "")
            cap_li = p.get("copy_linkedin", "")
            cap_tt = p.get("copy_tiktok") or cap_ig
            yt_t = p.get("yt_title", "")
            yt_d = p.get("yt_desc", cap_ig)
            yt_tags = p.get("yt_tags", "")
            title = f"{p.get('volanta', 'Star Union')} — {p.get('bajada', '').replace(chr(10), ' ')}"

            res = {}
            if "ig_feed" in chs:
                res["Instagram Feed (4:5)"] = srv.publish_ig_feed(keys, feed_f, cap_ig)
            if "ig_story" in chs:
                res["Instagram Story Video c/Música (9:16)"] = srv.publish_ig_story(keys, story_f, reel_f)
            if "ig_reel" in chs:
                res["Instagram Reel 12s c/Locución"] = srv.publish_ig_reel(keys, reel_f, cap_ig)
            if "fb_page" in chs:
                res["Facebook Page"] = srv.publish_fb_page(keys, p.get("fb_feed_file") or feed_f, cap_ig, "https://www.starunion.com.ar")
            if "fb_reel" in chs:
                res["Facebook Reel MP4"] = srv.publish_fb_reel(keys, reel_f, cap_ig, "https://www.starunion.com.ar")
            if "linkedin" in chs:
                res["LinkedIn Página Empresa"] = srv.publish_linkedin(keys, p.get("li_feed_file") or feed_f, cap_li, "https://www.starunion.com.ar", title)
            if "gmb" in chs:
                res["Google My Business (Maps)"] = srv.publish_gmb(keys, p.get("gmb_feed_file") or feed_f, cap_ig, "https://www.starunion.com.ar")
            if "youtube" in chs:
                res["YouTube Shorts (@starunionservicios)"] = srv.publish_youtube_short(keys, reel_f, yt_t, yt_d, yt_tags)
            if "tiktok" in chs:
                res["TikTok Video (Copy Completo)"] = srv.publish_tiktok(keys, reel_f, cap_tt)

            any_ok = any(isinstance(v, dict) and v.get("ok") for v in res.values())
            if any_ok:
                p["status"] = "publicado"
                p["published_at"] = now_ar
                p["last_results"] = res
                changed = True
                live_url = (res.get("YouTube Shorts (@starunionservicios)", {}) or {}).get("id") or "https://www.instagram.com/starunion.ar/"
                mark_aprobala_published(prod_tok, ap_id, live_url)
                print(f"[CLOUD-PUBLISHER] Pieza #{pid} publicada con éxito en la nube y marcada en Aprobalo.")
            else:
                print(f"[CLOUD-PUBLISHER] Advertencia en #{pid}: {res}")
        else:
            print(f"[CLOUD-PUBLISHER] Pieza #{pid}: estado={st} | salida={sched_at}")

    if changed:
        with open(sched_path, "w", encoding="utf-8") as f:
            json.dump(sched, f, ensure_ascii=False, indent=2)
        print("[CLOUD-PUBLISHER] calendario_programado.json sincronizado con Aprobalo.")


if __name__ == "__main__":
    main()
