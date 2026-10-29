#!/usr/bin/env python3
"""
Servidor Local de Publicación Directa por API — 4 - STAR UNION S.R.L.
Corre en http://127.0.0.1:8894
- Sirve la web y la Central de Redes (/redes-sociales/index.html)
- Guarda las llaves aisladas en /Users/arianawajntraub/Documents/antigravity/star-union/.agents/vault/social_keys.json
- Publica directo por API oficial en las 6 redes:
  1) Instagram Business (Feed 4:5, Story 9:16 y Reel MP4 con voz de varón + Funk Groove)
  2) Facebook Page (Post y Reel MP4)
  3) LinkedIn Página de Empresa (con Candado Duro Anti-Perfil Personal urn:li:organization)
  4) Google Business Profile / My Business (Google Maps)
  5) YouTube Shorts (YouTube Data API v3)
  6) TikTok Business (TikTok Content Posting API v2)
"""
import http.server
import json
import os
import stat
import time
import urllib.parse
import urllib.request
import urllib.error

WEB_ROOT = "/Users/arianawajntraub/Documents/antigravity/star-union"
VAULT_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union/.agents/vault"
KEYS_PATH = os.path.join(VAULT_DIR, "social_keys.json")
PUBLIC_BASE = "https://wajntraub.ar/staruniontest"


def load_keys():
    os.makedirs(VAULT_DIR, exist_ok=True)
    if not os.path.exists(KEYS_PATH):
        return {}
    try:
        with open(KEYS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_keys(data):
    os.makedirs(VAULT_DIR, exist_ok=True)
    current = load_keys()
    current.update(data)
    with open(KEYS_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, ensure_ascii=False)
    try:
        os.chmod(KEYS_PATH, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass
    return current


def http_json(method, url, headers=None, params=None, body_json=None, form_data=None):
    if params:
        qs = urllib.parse.urlencode(params)
        url = f"{url}{'&' if '?' in url else '?'}{qs}"
    req_headers = headers or {}
    data_bytes = None
    if body_json is not None:
        data_bytes = json.dumps(body_json).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    elif form_data is not None:
        data_bytes = urllib.parse.urlencode(form_data).encode("utf-8")
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"error": raw}
    except Exception as e:
        return 500, {"error": str(e)}


def auto_discover_meta(user_or_page_token):
    """
    A partir de 1 solo token de Meta, detecta automáticamente:
    - La Fan Page de Facebook de Star Union (fb_page_id, fb_page_name, fb_page_token)
    - La cuenta de Instagram Business vinculada (ig_user_id, ig_username)
    """
    status, data = http_json(
        "GET",
        "https://graph.facebook.com/v21.0/me/accounts",
        params={
            "fields": "id,name,access_token,instagram_business_account{id,username}",
            "access_token": user_or_page_token,
        },
    )
    if status == 200 and "data" in data and len(data["data"]) > 0:
        chosen = data["data"][0]
        for page in data["data"]:
            pname = (page.get("name") or "").lower()
            if "star union" in pname or "starunion" in pname:
                chosen = page
                break
        ig = chosen.get("instagram_business_account") or {}
        return {
            "ok": True,
            "meta_user_token": user_or_page_token,
            "fb_page_id": chosen.get("id", ""),
            "fb_page_name": chosen.get("name", ""),
            "fb_page_token": chosen.get("access_token", user_or_page_token),
            "ig_user_id": ig.get("id", ""),
            "ig_username": ig.get("username", ""),
        }

    status2, page_data = http_json(
        "GET",
        "https://graph.facebook.com/v21.0/me",
        params={
            "fields": "id,name,instagram_business_account{id,username}",
            "access_token": user_or_page_token,
        },
    )
    if status2 == 200 and page_data.get("id"):
        ig = page_data.get("instagram_business_account") or {}
        return {
            "ok": True,
            "meta_user_token": user_or_page_token,
            "fb_page_id": page_data.get("id", ""),
            "fb_page_name": page_data.get("name", ""),
            "fb_page_token": user_or_page_token,
            "ig_user_id": ig.get("id", ""),
            "ig_username": ig.get("username", ""),
        }
    return {"ok": False, "detail": data}


def auto_discover_linkedin(li_token, custom_urn=""):
    headers = {"Authorization": f"Bearer {li_token}"}
    if custom_urn:
        if custom_urn.isdigit():
            custom_urn = f"urn:li:organization:{custom_urn}"
        return {"ok": True, "linkedin_token": li_token, "linkedin_urn": custom_urn, "linkedin_name": f"Página Empresa ({custom_urn})"}
    st_org, org_data = http_json(
        "GET",
        "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee&role=ADMINISTRATOR&state=APPROVED",
        headers=headers,
    )
    if st_org == 200 and org_data.get("elements"):
        org_urn = org_data["elements"][0].get("organizationalTarget", "")
        if org_urn:
            return {"ok": True, "linkedin_token": li_token, "linkedin_urn": org_urn, "linkedin_name": f"Página Empresa ({org_urn})"}
    status, info = http_json("GET", "https://api.linkedin.com/v2/userinfo", headers=headers)
    if status == 200 and info.get("sub"):
        urn = f"urn:li:person:{info['sub']}"
        return {"ok": True, "linkedin_token": li_token, "linkedin_urn": urn, "linkedin_name": f"🛑 Perfil Personal: {info.get('name', urn)} (Bloqueado: falta urn:li:organization)"}
    return {"ok": False, "detail": info}


def auto_discover_youtube(yt_token):
    headers = {"Authorization": f"Bearer {yt_token}"}
    st, data = http_json(
        "GET",
        "https://www.googleapis.com/youtube/v3/channels",
        headers=headers,
        params={"part": "snippet", "mine": "true"},
    )
    if st == 200 and data.get("items"):
        ch = data["items"][0]
        title = ch.get("snippet", {}).get("title", "Canal YouTube")
        cid = ch.get("id", "")
        return {"ok": True, "youtube_token": yt_token, "youtube_channel_id": cid, "youtube_channel_name": title}
    return {"ok": False, "detail": data}


def publish_ig_feed(keys, img_rel_path, caption):
    ig_id = keys.get("ig_user_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not ig_id or not token:
        return {"ok": False, "error": "Falta conectar el Token de Meta / Instagram de Star Union."}

    img_url = f"{PUBLIC_BASE}/redes-sociales/{img_rel_path.lstrip('/')}"
    st, res = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        form_data={
            "image_url": img_url,
            "caption": caption,
            "access_token": token,
        },
    )
    if st != 200 or not res.get("id"):
        return {"ok": False, "error": f"Error subiendo imagen a IG: {res}"}

    time.sleep(2)
    st_pub, res_pub = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        form_data={
            "creation_id": res["id"],
            "access_token": token,
        },
    )
    if st_pub == 200 and res_pub.get("id"):
        return {"ok": True, "id": res_pub["id"]}
    return {"ok": False, "error": f"Error publicando Feed IG: {res_pub}"}


def publish_ig_story(keys, story_rel_path):
    ig_id = keys.get("ig_user_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not ig_id or not token:
        return {"ok": False, "error": "Falta conectar el Token de Meta / Instagram de Star Union."}

    story_url = f"{PUBLIC_BASE}/redes-sociales/{story_rel_path.lstrip('/')}"
    st, res = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        form_data={
            "image_url": story_url,
            "media_type": "STORIES",
            "access_token": token,
        },
    )
    if st != 200 or not res.get("id"):
        return {"ok": False, "error": f"Error creando Story IG: {res}"}

    time.sleep(2)
    st_pub, res_pub = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        form_data={
            "creation_id": res["id"],
            "access_token": token,
        },
    )
    if st_pub == 200 and res_pub.get("id"):
        return {"ok": True, "id": res_pub["id"]}
    return {"ok": False, "error": f"Error publicando Story IG: {res_pub}"}


def publish_ig_reel(keys, reel_rel_path, caption):
    ig_id = keys.get("ig_user_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not ig_id or not token:
        return {"ok": False, "error": "Falta conectar el Token de Meta / Instagram de Star Union."}

    video_url = f"{PUBLIC_BASE}/redes-sociales/{reel_rel_path.lstrip('/')}"
    st, res = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        form_data={
            "video_url": video_url,
            "media_type": "REELS",
            "caption": caption,
            "access_token": token,
        },
    )
    if st != 200 or not res.get("id"):
        return {"ok": False, "error": f"Error subiendo Reel a IG: {res}"}

    cid = res["id"]
    for _ in range(15):
        time.sleep(3)
        st_c, res_c = http_json(
            "GET",
            f"https://graph.facebook.com/v21.0/{cid}",
            params={"fields": "status_code", "access_token": token},
        )
        if res_c.get("status_code") == "FINISHED":
            break
        if res_c.get("status_code") == "ERROR":
            return {"ok": False, "error": f"Error procesando video Reel en IG: {res_c}"}

    st_pub, res_pub = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        form_data={
            "creation_id": cid,
            "access_token": token,
        },
    )
    if st_pub == 200 and res_pub.get("id"):
        return {"ok": True, "id": res_pub["id"]}
    return {"ok": False, "error": f"Error publicando Reel IG: {res_pub}"}


def publish_fb_page(keys, img_rel_path, caption):
    page_id = keys.get("fb_page_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not page_id or not token:
        return {"ok": False, "error": "Falta conectar el Token de Facebook Page de Star Union."}

    img_url = f"{PUBLIC_BASE}/redes-sociales/{img_rel_path.lstrip('/')}"
    st, res = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{page_id}/photos",
        form_data={
            "url": img_url,
            "message": caption,
            "access_token": token,
        },
    )
    if st == 200 and res.get("id"):
        return {"ok": True, "id": res["id"]}
    return {"ok": False, "error": f"Error publicando en Facebook Page: {res}"}


def publish_linkedin(keys, caption, public_url, title):
    token = keys.get("linkedin_token")
    urn = keys.get("linkedin_urn")
    if not token or not urn:
        return {"ok": False, "error": "Falta conectar el Token de LinkedIn de Star Union."}
    if urn.startswith("urn:li:person:"):
        return {
            "ok": False,
            "error": "🛑 BLOQUEADO POR SEGURIDAD: El token actual apunta a tu perfil personal (Ariana Wajntraub) y NO a la Página de Empresa STAR UNION (urn:li:organization:...). Jamás se publica en perfil personal.",
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    body = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": caption},
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "originalUrl": public_url,
                        "title": {"text": title},
                    }
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    st, res = http_json("POST", "https://api.linkedin.com/v2/ugcPosts", headers=headers, body_json=body)
    if st in (200, 201):
        return {"ok": True, "id": res.get("id", "published")}
    return {"ok": False, "error": f"Error en LinkedIn API: {res}"}


def publish_gmb(keys, img_rel_path, caption, public_url):
    token = keys.get("gmb_token")
    loc = keys.get("gmb_location_name")
    if not token or not loc:
        return {"ok": False, "error": "Falta Token o ID de ubicación de Google My Business (Guaminí 5657)."}

    headers = {"Authorization": f"Bearer {token}"}
    img_url = f"{PUBLIC_BASE}/redes-sociales/{img_rel_path.lstrip('/')}"
    body = {
        "languageCode": "es-419",
        "summary": caption[:1450],
        "callToAction": {
            "actionType": "LEARN_MORE",
            "url": public_url,
        },
        "media": [
            {
                "mediaFormat": "PHOTO",
                "sourceUrl": img_url,
            }
        ],
        "topicType": "STANDARD",
    }
    url = f"https://mybusiness.googleapis.com/v4/{loc.lstrip('/')}/localPosts"
    st, res = http_json("POST", url, headers=headers, body_json=body)
    if st in (200, 201):
        return {"ok": True, "id": res.get("name", "published")}
    return {"ok": False, "error": f"Error en Google Business API: {res}"}


def publish_youtube_short(keys, reel_rel_path, title, description, tags_csv):
    token = keys.get("youtube_token")
    if not token:
        return {"ok": False, "error": "Falta conectar el Token de YouTube Data API v3 (@StarUnionSRL)."}

    local_mp4 = os.path.join(WEB_ROOT, "redes-sociales", reel_rel_path.lstrip("/").split("?")[0])
    if not os.path.exists(local_mp4):
        return {"ok": False, "error": f"Archivo MP4 no encontrado: {local_mp4}"}

    tags_list = [t.strip() for t in (tags_csv or "").split(",") if t.strip()]
    short_title = title if "#Shorts" in title else f"{title[:88]} #Shorts"
    meta = {
        "snippet": {
            "title": short_title,
            "description": description,
            "tags": tags_list,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    init_req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(meta).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(init_req, timeout=30) as resp:
            upload_url = resp.headers.get("Location")
        if not upload_url:
            return {"ok": False, "error": "YouTube no devolvió URL de subida resumable."}
        with open(local_mp4, "rb") as vf:
            video_bytes = vf.read()
        up_req = urllib.request.Request(
            upload_url,
            data=video_bytes,
            headers={"Content-Type": "video/mp4", "Content-Length": str(len(video_bytes))},
            method="PUT",
        )
        with urllib.request.urlopen(up_req, timeout=120) as uresp:
            res_data = json.loads(uresp.read().decode("utf-8"))
            return {"ok": True, "id": res_data.get("id", "uploaded")}
    except Exception as e:
        return {"ok": False, "error": f"Error subiendo YouTube Short: {e}"}


def publish_tiktok(keys, reel_rel_path, caption):
    token = keys.get("tiktok_token")
    if not token:
        return {"ok": False, "error": "Falta conectar el Access Token de TikTok Content Posting API."}

    video_url = f"{PUBLIC_BASE}/redes-sociales/{reel_rel_path.lstrip('/')}"
    st, res = http_json(
        "POST",
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers={"Authorization": f"Bearer {token}"},
        body_json={
            "post_info": {
                "title": caption[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url,
            },
        },
    )
    if st in (200, 201) and not res.get("error", {}).get("code") in ("access_token_invalid", "scope_not_authorized"):
        return {"ok": True, "id": res.get("data", {}).get("publish_id", "published")}
    return {"ok": False, "error": f"Error en TikTok API: {res}"}


class StarUnionAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_ROOT, **kwargs)

    def _send_json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/status"):
            keys = load_keys()
            self._send_json(
                200,
                {
                    "meta_connected": bool(keys.get("fb_page_token") or keys.get("meta_user_token")),
                    "fb_page_name": keys.get("fb_page_name", ""),
                    "fb_page_id": keys.get("fb_page_id", ""),
                    "ig_username": keys.get("ig_username", ""),
                    "ig_user_id": keys.get("ig_user_id", ""),
                    "linkedin_connected": bool(keys.get("linkedin_token") and keys.get("linkedin_urn")),
                    "linkedin_name": keys.get("linkedin_name", ""),
                    "linkedin_urn": keys.get("linkedin_urn", ""),
                    "gmb_connected": bool(keys.get("gmb_token") and keys.get("gmb_location_name")),
                    "gmb_location_name": keys.get("gmb_location_name", ""),
                    "youtube_connected": bool(keys.get("youtube_token")),
                    "youtube_channel_name": keys.get("youtube_channel_name", ""),
                    "tiktok_connected": bool(keys.get("tiktok_token")),
                },
            )
            return
        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(raw)
        except Exception:
            body = {}

        if self.path.startswith("/api/connect"):
            updates = {}
            messages = []

            meta_token = (body.get("meta_token") or "").strip()
            if meta_token:
                disc = auto_discover_meta(meta_token)
                if disc.get("ok"):
                    updates.update(disc)
                    if body.get("fb_page_id"):
                        updates["fb_page_id"] = body["fb_page_id"].strip()
                    if body.get("ig_user_id"):
                        updates["ig_user_id"] = body["ig_user_id"].strip()
                    messages.append(
                        f"✅ Meta conectado: FB Page '{updates.get('fb_page_name')}' ({updates.get('fb_page_id')}) + IG @{updates.get('ig_username')} ({updates.get('ig_user_id')})"
                    )
                else:
                    updates["meta_user_token"] = meta_token
                    updates["fb_page_token"] = meta_token
                    messages.append(f"⚠️ Token de Meta guardado (verificá permisos pages_manage_posts / instagram_content_publish): {disc.get('detail')}")

            li_token = (body.get("linkedin_token") or "").strip()
            li_urn = (body.get("linkedin_urn") or "").strip()
            if li_token:
                disc_li = auto_discover_linkedin(li_token, li_urn)
                if disc_li.get("ok"):
                    updates.update(disc_li)
                    messages.append(f"✅ LinkedIn conectado: {disc_li.get('linkedin_name')}")
                else:
                    updates["linkedin_token"] = li_token
                    if li_urn:
                        updates["linkedin_urn"] = li_urn if li_urn.startswith("urn:") else f"urn:li:organization:{li_urn}"
                    messages.append(f"⚠️ Token de LinkedIn guardado: {disc_li.get('detail')}")

            gmb_token = (body.get("gmb_token") or "").strip()
            gmb_loc = (body.get("gmb_location_name") or "").strip()
            if gmb_token:
                updates["gmb_token"] = gmb_token
                if gmb_loc:
                    updates["gmb_location_name"] = gmb_loc
                messages.append("✅ Google My Business (Google Maps) guardado.")

            yt_token = (body.get("youtube_token") or "").strip()
            if yt_token:
                disc_yt = auto_discover_youtube(yt_token)
                if disc_yt.get("ok"):
                    updates.update(disc_yt)
                    messages.append(f"✅ YouTube Shorts conectado: {disc_yt.get('youtube_channel_name')} ({disc_yt.get('youtube_channel_id')})")
                else:
                    updates["youtube_token"] = yt_token
                    messages.append("✅ Token de YouTube Data API v3 guardado.")

            tt_token = (body.get("tiktok_token") or "").strip()
            if tt_token:
                updates["tiktok_token"] = tt_token
                messages.append("✅ Token de TikTok Content Posting API guardado.")

            saved = save_keys(updates)
            self._send_json(
                200,
                {
                    "ok": True,
                    "messages": messages,
                    "status": {
                        "meta_connected": bool(saved.get("fb_page_token") or saved.get("meta_user_token")),
                        "fb_page_name": saved.get("fb_page_name", ""),
                        "ig_username": saved.get("ig_username", ""),
                        "linkedin_connected": bool(saved.get("linkedin_token") and saved.get("linkedin_urn")),
                        "linkedin_name": saved.get("linkedin_name", ""),
                        "gmb_connected": bool(saved.get("gmb_token") and saved.get("gmb_location_name")),
                        "youtube_connected": bool(saved.get("youtube_token")),
                        "youtube_channel_name": saved.get("youtube_channel_name", ""),
                        "tiktok_connected": bool(saved.get("tiktok_token")),
                    },
                },
            )
            return

        if self.path.startswith("/api/publish"):
            keys = load_keys()
            channels = body.get("channels", [])
            feed_file = body.get("feed_file", "piezas/01_feed_logistica_industria_1080x1350.jpg")
            story_file = body.get("story_file", "piezas/01_story_logistica_industria_1080x1920.jpg")
            reel_file = body.get("reel_file", "piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4")
            caption_ig = body.get("caption_ig", "")
            caption_li = body.get("caption_li", "")
            yt_title = body.get("yt_title", "Star Union S.R.L. · Limpieza Corporativa e Industrial #Shorts")
            yt_desc = body.get("yt_desc", caption_ig)
            yt_tags = body.get("yt_tags", "star union, limpieza industrial, iso 9001")
            public_url = body.get("public_url", "https://www.starunion.com.ar")
            title = body.get("title", "Star Union S.R.L.")

            results = {}
            if "ig_feed" in channels:
                results["Instagram Feed (4:5)"] = publish_ig_feed(keys, feed_file, caption_ig)
            if "ig_story" in channels:
                results["Instagram Story (9:16)"] = publish_ig_story(keys, story_file)
            if "ig_reel" in channels:
                results["Instagram Reel con Voz Varón + Funk (MP4)"] = publish_ig_reel(keys, reel_file, caption_ig)
            if "fb_page" in channels:
                results["Facebook Page"] = publish_fb_page(keys, feed_file, caption_ig)
            if "linkedin" in channels:
                results["LinkedIn Página Empresa"] = publish_linkedin(keys, caption_li, public_url, title)
            if "gmb" in channels:
                results["Google My Business (Maps)"] = publish_gmb(keys, feed_file, caption_ig, public_url)
            if "youtube" in channels:
                results["YouTube Shorts (@StarUnionSRL)"] = publish_youtube_short(keys, reel_file, yt_title, yt_desc, yt_tags)
            if "tiktok" in channels:
                results["TikTok Video"] = publish_tiktok(keys, reel_file, caption_ig)

            self._send_json(200, {"ok": True, "results": results})
            return

        self._send_json(404, {"error": "Endpoint no encontrado"})


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 8894), StarUnionAPIHandler)
    print("STAR UNION API Server corriendo en http://127.0.0.1:8894")
    server.serve_forever()
