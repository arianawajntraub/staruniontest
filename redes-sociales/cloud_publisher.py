#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Publicación 100% en la Nube (GitHub Actions Cloud Runner) para Star Union.
Corre en los servidores de GitHub (Ubuntu Cloud) con hora Argentina (UTC-3),
sin depender en absoluto de que la Mac de Ariana esté prendida o conectada a Wi-Fi.
"""
import datetime
import json
import os
import sys

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


def main():
    sched_path = os.path.join(ROOT_DIR, "redes-sociales", "calendario_programado.json")
    if not os.path.exists(sched_path):
        print("No existe calendario_programado.json")
        return

    with open(sched_path, "r", encoding="utf-8") as f:
        sched = json.load(f)

    # Hora actual en Argentina (UTC-3)
    ar_tz = datetime.timezone(datetime.timedelta(hours=-3))
    now_ar = datetime.datetime.now(ar_tz).strftime("%Y-%m-%dT%H:%M")
    print(f"[CLOUD-PUBLISHER] Hora Argentina actual: {now_ar}")

    keys = srv.load_keys()
    changed = False

    for pid in sorted(sched.keys()):
        p = sched[pid]
        st = p.get("status", "")
        sched_at = p.get("scheduled_at", "")
        if st in ("aprobado", "programado") and sched_at and sched_at <= now_ar:
            print(f"[CLOUD-PUBLISHER] Disparando pieza #{pid} programada para {sched_at}...")
            chs = [c for c in (p.get("channels") or ["ig_feed", "ig_story", "ig_reel", "fb_page", "fb_story", "fb_reel", "linkedin", "gmb", "youtube"]) if c != "tiktok"]
            feed_f = (p.get("carousel_files") or [p.get("feed_file", "")])[0]
            story_f = p.get("story_video_file") or p.get("story_file", "")
            reel_f = p.get("reel_file", "")
            cap_ig = p.get("copy_ig_fb", "")
            cap_li = p.get("copy_linkedin", "")
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

            any_ok = any(isinstance(v, dict) and v.get("ok") for v in res.values())
            if any_ok:
                p["status"] = "publicado"
                p["published_at"] = now_ar
                p["last_results"] = res
                changed = True
                print(f"[CLOUD-PUBLISHER] Pieza #{pid} publicada con éxito en la nube.")
            else:
                print(f"[CLOUD-PUBLISHER] Advertencia en #{pid}: {res}")
        else:
            print(f"[CLOUD-PUBLISHER] Pieza #{pid}: estado={st} | salida={sched_at}")

    if changed:
        with open(sched_path, "w", encoding="utf-8") as f:
            json.dump(sched, f, ensure_ascii=False, indent=2)
        print("[CLOUD-PUBLISHER] calendario_programado.json actualizado.")


if __name__ == "__main__":
    main()
