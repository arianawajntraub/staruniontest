#!/usr/bin/env python3
"""
STAR UNION — Servidor Local de Publicación Directa por API ($0 · Sin Make ni Zapier)
Unificado 100% con el Estándar Maestro de Redes:
  - Facebook Page API + Facebook Reels (Graph API v21.0 · Page Token Permanente expires_at=0)
  - Instagram Business API (Graph API v21.0: Feed 4:5 sin URL en copy + Stories en Video MP4 con música + Reels MP4)
  - LinkedIn Company Page API (UGC Posts v2 + registerUpload binario nativo 1080x1350 · Candado duro urn:li:organization:35644861)
  - Google Business Profile API (Google Maps Local Posts v4 + Auto-Refresh con refresh_token 1//04...)
  - YouTube Data API v3 (Subida Resumable de YouTube Shorts MP4 + X-Upload-Content-Length + Auto-Refresh 1//04...)
  - TikTok Content Posting API v2 (Subida Binaria FILE_UPLOAD + Fallback /inbox/video/init/ + Auto-Refresh 365 días)

Bóveda aislada Zero-Trust: /Users/arianawajntraub/Documents/antigravity/star-union/.agents/vault/social_keys.json
Puerto exclusivo: http://127.0.0.1:8894
"""

import base64
import http.server
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

WEB_ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT_PATH = os.path.join(WEB_ROOT, ".agents", "vault", "social_keys.json")
PUBLIC_ASSET_BASE = "https://wajntraub.ar/staruniontest/redes-sociales"
STAR_UNION_LI_ORG_URN = "urn:li:organization:35644861"


def load_keys():
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_keys(new_data):
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    current = load_keys()
    for k, v in new_data.items():
        if v is not None and v != "":
            current[k] = v
    with open(VAULT_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    return current


def http_json(method, url, headers=None, json_body=None, form_data=None, timeout=45):
    hdrs = headers.copy() if headers else {}
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    elif form_data is not None:
        data = urllib.parse.urlencode(form_data).encode("utf-8")
        hdrs["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"error": raw}
    except Exception as e:
        return 500, {"error": str(e)}


# =====================================================================
# 0. AUTO-RENOVACIÓN DE TOKENS (GOOGLE OAUTH PLAYGROUND + TIKTOK + META)
# =====================================================================
def exchange_google_refresh_token(refresh_token):
    """Usa el endpoint oficial de Google OAuth Playground para renovar un ya29... a partir de un 1//04..."""
    if not refresh_token or not refresh_token.startswith("1//"):
        return ""
    try:
        req = urllib.request.Request(
            "https://developers.google.com/oauthplayground/refreshAccessToken",
            data=json.dumps({
                "token_uri": "https://oauth2.googleapis.com/token",
                "refresh_token": refresh_token.strip()
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            outer = json.loads(r.read().decode("utf-8"))
            msg_b64 = outer.get("Response", {}).get("message-body", "")
            if msg_b64:
                inner = json.loads(base64.b64decode(msg_b64).decode("utf-8", "ignore"))
                return inner.get("access_token", "")
            return outer.get("access_token", "")
    except Exception:
        return ""


def ensure_fresh_youtube_token(keys):
    yt_tok = keys.get("youtube_token", "")
    yt_rt = keys.get("youtube_refresh_token", "")
    if yt_tok.startswith("1//"):
        yt_rt = yt_tok
        save_keys({"youtube_refresh_token": yt_rt})
    if yt_tok and not yt_tok.startswith("1//"):
        st, _ = http_json("GET", "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true", headers={"Authorization": f"Bearer {yt_tok}"})
        if st == 200:
            return yt_tok
    if yt_rt:
        new_tok = exchange_google_refresh_token(yt_rt)
        if new_tok:
            save_keys({"youtube_token": new_tok, "youtube_refresh_token": yt_rt})
            keys["youtube_token"] = new_tok
            return new_tok
    return yt_tok


def ensure_fresh_gmb_token(keys):
    gmb_tok = keys.get("gmb_token", "")
    gmb_rt = keys.get("gmb_refresh_token", "")
    if gmb_tok.startswith("1//"):
        gmb_rt = gmb_tok
        save_keys({"gmb_refresh_token": gmb_rt})
    if gmb_tok and not gmb_tok.startswith("1//"):
        st, _ = http_json("GET", "https://mybusinessaccountmanagement.googleapis.com/v1/accounts", headers={"Authorization": f"Bearer {gmb_tok}"})
        if st == 200:
            return gmb_tok
    if gmb_rt:
        new_tok = exchange_google_refresh_token(gmb_rt)
        if new_tok:
            save_keys({"gmb_token": new_tok, "gmb_refresh_token": gmb_rt})
            keys["gmb_token"] = new_tok
            return new_tok
    return gmb_tok


def ensure_fresh_tiktok_token(keys):
    tt_tok = keys.get("tiktok_token", "")
    tt_rt = keys.get("tiktok_refresh_token", "")
    ck = keys.get("tiktok_client_key", "")
    cs = keys.get("tiktok_client_secret", "")
    if tt_tok:
        st, _ = http_json("GET", "https://open.tiktokapis.com/v2/user/info/?fields=open_id,display_name", headers={"Authorization": f"Bearer {tt_tok}"})
        if st == 200:
            return tt_tok
    if tt_rt and ck and cs:
        st, data = http_json(
            "POST",
            "https://open.tiktokapis.com/v2/oauth/token/",
            form_data={
                "client_key": ck,
                "client_secret": cs,
                "grant_type": "refresh_token",
                "refresh_token": tt_rt,
            },
        )
        new_tok = data.get("access_token") or data.get("data", {}).get("access_token", "")
        new_rt = data.get("refresh_token") or data.get("data", {}).get("refresh_token", tt_rt)
        if new_tok:
            save_keys({"tiktok_token": new_tok, "tiktok_refresh_token": new_rt})
            keys["tiktok_token"] = new_tok
            return new_tok
    return tt_tok


# =====================================================================
# 1. AUTO-DISCOVERY DE CUENTAS (CONEXIÓN EN 1 CLIC + TOKEN PERMANENTE)
# =====================================================================
def auto_discover_meta(user_or_page_token, app_secret=""):
    """
    Intercambia el User Token de 1h por un Long-Lived User Token (60 días) y extrae el
    Page Token Permanente (expires_at: 0, no vence nunca) para Star Union Servicios + @starunionservicios.
    Soporta tanto la App 924417103935122 como 912176281861229.
    """
    token_to_use = user_or_page_token.strip()
    saved_keys = load_keys()

    candidate_apps = []
    if app_secret:
        candidate_apps.append(("924417103935122", app_secret.strip()))
        candidate_apps.append(("912176281861229", app_secret.strip()))
    if saved_keys.get("meta_app_secret"):
        candidate_apps.append(("924417103935122", saved_keys["meta_app_secret"]))
        candidate_apps.append(("912176281861229", saved_keys["meta_app_secret"]))
    if saved_keys.get("meta_app_secret_shared"):
        candidate_apps.append(("912176281861229", saved_keys["meta_app_secret_shared"]))

    exchanged_permanent = False
    for app_id, sec in candidate_apps:
        ex_url = (
            "https://graph.facebook.com/v21.0/oauth/access_token?"
            + urllib.parse.urlencode({
                "grant_type": "fb_exchange_token",
                "client_id": app_id,
                "client_secret": sec,
                "fb_exchange_token": token_to_use,
            })
        )
        st_ex, data_ex = http_json("GET", ex_url)
        if st_ex == 200 and data_ex.get("access_token"):
            token_to_use = data_ex["access_token"]
            exchanged_permanent = True
            break

    url = (
        "https://graph.facebook.com/v21.0/me/accounts?"
        + urllib.parse.urlencode(
            {
                "fields": "id,name,access_token,instagram_business_account{id,username}",
                "access_token": token_to_use,
            }
        )
    )
    status, data = http_json("GET", url)
    if status != 200 or "data" not in data:
        me_url = "https://graph.facebook.com/v21.0/me?" + urllib.parse.urlencode(
            {
                "fields": "id,name,instagram_business_account{id,username}",
                "access_token": token_to_use,
            }
        )
        st2, me_data = http_json("GET", me_url)
        if st2 == 200 and "id" in me_data:
            ig = me_data.get("instagram_business_account", {})
            return {
                "ok": True,
                "meta_user_token": token_to_use,
                "fb_page_id": me_data["id"],
                "fb_page_name": me_data.get("name", "Star Union"),
                "fb_page_token": token_to_use,
                "ig_user_id": ig.get("id", ""),
                "ig_username": ig.get("username", ""),
                "permanent": exchanged_permanent,
            }
        return {"ok": False, "detail": data}

    pages = data.get("data", [])
    if not pages:
        return {"ok": False, "detail": "El token no devolvió páginas asociadas. Verificá tildar 'Star Union Servicios' al generar el token."}

    chosen = pages[0]
    for p in pages:
        name_low = p.get("name", "").lower()
        if "star" in name_low or "union" in name_low or p.get("id") == "349413715151593":
            chosen = p
            break

    ig = chosen.get("instagram_business_account", {})
    return {
        "ok": True,
        "meta_user_token": token_to_use,
        "fb_page_id": chosen["id"],
        "fb_page_name": chosen.get("name", ""),
        "fb_page_token": chosen.get("access_token", token_to_use),
        "ig_user_id": ig.get("id", ""),
        "ig_username": ig.get("username", ""),
        "permanent": exchanged_permanent,
    }


def auto_discover_linkedin(li_token, manual_org_urn=""):
    """
    CANDADO ESTRICTO: En Star Union JAMÁS se publica en perfil personal (urn:li:person:).
    Solo se permite urn:li:organization:35644861 (Star Union Servicios).
    """
    urn = (manual_org_urn or STAR_UNION_LI_ORG_URN).strip()
    if not urn.startswith("urn:li:"):
        urn = f"urn:li:organization:{urn}"
    if "urn:li:person:" in urn:
        return {
            "ok": False,
            "detail": "🛑 BLOQUEADO POR SEGURIDAD: Se detectó un URN de perfil personal. Star Union solo permite Página de Empresa (urn:li:organization:35644861).",
        }
    hdrs = {"Authorization": f"Bearer {li_token}", "X-Restli-Protocol-Version": "2.0.0"}
    org_id = urn.split(":")[-1]
    st, data = http_json("GET", f"https://api.linkedin.com/v2/organizations/{org_id}", headers=hdrs)
    if st == 200 and data.get("localizedName"):
        return {
            "ok": True,
            "linkedin_token": li_token,
            "linkedin_urn": urn,
            "linkedin_name": f"{data.get('localizedName')} (Página Empresa ID {org_id})",
        }
    return {
        "ok": True,
        "linkedin_token": li_token,
        "linkedin_urn": urn,
        "linkedin_name": f"Star Union ({urn})",
    }


def auto_discover_youtube(yt_token_or_rt):
    raw = yt_token_or_rt.strip()
    refresh_tok = ""
    access_tok = raw
    if raw.startswith("1//"):
        refresh_tok = raw
        access_tok = exchange_google_refresh_token(refresh_tok)
        if not access_tok:
            return {"ok": False, "detail": "No se pudo canjear el Refresh Token (1//04...) en Google OAuth Playground."}
    hdrs = {"Authorization": f"Bearer {access_tok}"}
    st, data = http_json("GET", "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", headers=hdrs)
    if st == 200 and data.get("items"):
        ch = data["items"][0]
        res = {
            "ok": True,
            "youtube_token": access_tok,
            "youtube_channel_id": ch["id"],
            "youtube_channel_name": ch["snippet"]["title"],
        }
        if refresh_tok:
            res["youtube_refresh_token"] = refresh_tok
        return res
    return {"ok": False, "detail": data}


def auto_discover_gmb(gmb_token_or_rt, manual_loc=""):
    raw = gmb_token_or_rt.strip()
    refresh_tok = ""
    access_tok = raw
    if raw.startswith("1//"):
        refresh_tok = raw
        access_tok = exchange_google_refresh_token(refresh_tok)
        if not access_tok:
            return {"ok": False, "detail": "No se pudo canjear el Refresh Token (1//04...) en Google OAuth Playground."}

    if manual_loc and manual_loc.strip():
        res = {"ok": True, "gmb_token": access_tok, "gmb_location_name": manual_loc.strip()}
        if refresh_tok:
            res["gmb_refresh_token"] = refresh_tok
        return res

    hdrs = {"Authorization": f"Bearer {access_tok}"}
    st, acc_data = http_json("GET", "https://mybusinessaccountmanagement.googleapis.com/v1/accounts", headers=hdrs)
    if st == 200 and "accounts" in acc_data:
        for acc in acc_data["accounts"]:
            acc_name = acc["name"]
            st2, loc_data = http_json(
                "GET",
                f"https://mybusinessbusinessinformation.googleapis.com/v1/{acc_name}/locations?readMask=name,title",
                headers=hdrs,
            )
            if st2 == 200 and "locations" in loc_data:
                for loc in loc_data["locations"]:
                    title = loc.get("title", "")
                    if "star" in title.lower() or "union" in title.lower() or len(loc_data["locations"]) == 1:
                        res = {
                            "ok": True,
                            "gmb_token": access_tok,
                            "gmb_location_name": f"{acc_name}/{loc['name']}" if not loc["name"].startswith("accounts/") else loc["name"],
                            "gmb_title": title,
                        }
                        if refresh_tok:
                            res["gmb_refresh_token"] = refresh_tok
                        return res
    return {
        "ok": False,
        "gmb_token": access_tok,
        "detail": "Token guardado, pero no se encontró ubicación activa de Google Business Profile.",
    }


# =====================================================================
# 2. PUBLICADORES DIRECTOS POR API OFICIAL (ESTÁNDAR MAESTRO UNIFICADO)
# =====================================================================
def clean_ig_caption(caption):
    """
    REGLA INQUEBRANTABLE: En Instagram los links en el copy NO son clicables.
    Elimina cualquier URL cruda (http://, https://, www.starunion.com.ar) y deriva a la bio.
    """
    lines = []
    for line in (caption or "").splitlines():
        s = line.strip()
        if s.startswith("http://") or s.startswith("https://"):
            continue
        line = re.sub(r"https?://\S+", "el link de nuestra bio (@starunionservicios)", line)
        line = re.sub(r"www\.starunion\.com\.ar", "el link de nuestra bio (@starunionservicios)", line, flags=re.IGNORECASE)
        lines.append(line)
    cleaned = "\n".join(lines).strip()
    if "@starunionservicios" not in cleaned:
        cleaned += "\n\n📲 Relevamiento técnico y contacto directo en el link de nuestra bio (@starunionservicios)."
    return cleaned


def publish_ig_feed(keys, feed_rel_path, caption):
    caption = clean_ig_caption(caption)
    ig_id = keys.get("ig_user_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not ig_id or not token:
        return {"ok": False, "error": "Falta conectar o renovar el Token de Meta (Instagram @starunionservicios)."}

    img_url = f"{PUBLIC_ASSET_BASE}/{feed_rel_path.lstrip('/')}"
    st, data = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        form_data={"image_url": img_url, "caption": caption, "access_token": token},
    )
    if st != 200 or "id" not in data:
        return {"ok": False, "error": f"Error creando contenedor IG Feed: {data}"}

    creation_id = data["id"]
    time.sleep(3)
    st3, pub = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        form_data={"creation_id": creation_id, "access_token": token},
    )
    if st3 == 200 and "id" in pub:
        return {"ok": True, "id": pub["id"]}
    return {"ok": False, "error": f"Error publicando IG Feed: {pub}"}


def publish_ig_story(keys, story_rel_path, reel_rel_path="piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4"):
    """
    REGLA INQUEBRANTABLE: Prohibido subir un JPG mudo a Instagram Stories por API.
    Se sube siempre el video vertical 9:16 (.mp4 con música y voz de marca) como media_type=STORIES.
    """
    ig_id = keys.get("ig_user_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not ig_id or not token:
        return {"ok": False, "error": "Falta conectar o renovar el Token de Meta (Instagram @starunionservicios)."}

    rel = reel_rel_path if reel_rel_path and reel_rel_path.endswith(".mp4") else "piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4"
    video_url = f"{PUBLIC_ASSET_BASE}/{rel.lstrip('/')}"
    st, data = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        form_data={
            "media_type": "STORIES",
            "video_url": video_url,
            "access_token": token,
        },
    )
    if st != 200 or "id" not in data:
        return {"ok": False, "error": f"Error creando IG Story en video con música: {data}"}

    cid = data["id"]
    for _ in range(18):
        time.sleep(3)
        st_chk, chk = http_json(
            "GET",
            f"https://graph.facebook.com/v21.0/{cid}?fields=status_code,status&access_token={urllib.parse.quote(token)}",
        )
        code = chk.get("status_code", "")
        if code == "FINISHED":
            break
        if code == "ERROR":
            return {"ok": False, "error": f"Meta rechazó el video de Story: {chk}"}

    st2, pub = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        form_data={"creation_id": cid, "access_token": token},
    )
    if st2 == 200 and "id" in pub:
        return {"ok": True, "id": pub["id"], "note": "Story publicada en video MP4 9:16 con voz de varón y Funk Groove."}
    return {"ok": False, "error": f"Error publicando IG Story: {pub}"}


def publish_ig_reel(keys, reel_rel_path, caption):
    caption = clean_ig_caption(caption)
    ig_id = keys.get("ig_user_id")
    token = keys.get("fb_page_token") or keys.get("meta_user_token")
    if not ig_id or not token:
        return {"ok": False, "error": "Falta conectar o renovar el Token de Meta (Instagram @starunionservicios)."}

    video_url = f"{PUBLIC_ASSET_BASE}/{reel_rel_path.lstrip('/')}"
    st, data = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media",
        form_data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": token,
        },
    )
    if st != 200 or "id" not in data:
        return {"ok": False, "error": f"Error iniciando contenedor de Reel MP4: {data}"}

    cid = data["id"]
    for _ in range(20):
        time.sleep(3)
        st_chk, chk = http_json(
            "GET",
            f"https://graph.facebook.com/v21.0/{cid}?fields=status_code,status&access_token={urllib.parse.quote(token)}",
        )
        code = chk.get("status_code", "")
        if code == "FINISHED":
            break
        if code == "ERROR":
            return {"ok": False, "error": f"Meta rechazó el procesamiento del Reel: {chk}"}

    st2, pub = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{ig_id}/media_publish",
        form_data={"creation_id": cid, "access_token": token},
    )
    if st2 == 200 and "id" in pub:
        return {"ok": True, "id": pub["id"]}
    return {"ok": False, "error": f"Error publicando Reel: {pub}"}


def publish_fb_page(keys, feed_rel_path, caption, public_url="https://www.starunion.com.ar"):
    page_id = keys.get("fb_page_id")
    page_token = keys.get("fb_page_token")
    if not page_id or not page_token:
        return {"ok": False, "error": "Falta conectar o renovar el Token de Facebook Page."}

    fb_caption = (caption or "").strip()
    if public_url and public_url not in fb_caption and "starunion.com.ar" not in fb_caption:
        fb_caption += f"\n\n👉 Conocé más en: {public_url}"

    img_url = f"{PUBLIC_ASSET_BASE}/{feed_rel_path.lstrip('/')}"
    st, data = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{page_id}/photos",
        form_data={"url": img_url, "message": fb_caption, "published": "true", "access_token": page_token},
    )
    if st == 200 and "id" in data:
        return {"ok": True, "id": data["id"]}
    return {"ok": False, "error": f"Error publicando en Facebook Page: {data}"}


def publish_fb_reel(keys, reel_rel_path, caption, public_url="https://www.starunion.com.ar"):
    page_id = keys.get("fb_page_id")
    page_token = keys.get("fb_page_token")
    if not page_id or not page_token:
        return {"ok": False, "error": "Falta conectar o renovar el Token de Facebook Page."}

    fb_caption = (caption or "").strip()
    if public_url and public_url not in fb_caption and "starunion.com.ar" not in fb_caption:
        fb_caption += f"\n\n👉 Relevamiento técnico: {public_url}"

    video_url = f"{PUBLIC_ASSET_BASE}/{reel_rel_path.lstrip('/')}"
    st, data = http_json(
        "POST",
        f"https://graph.facebook.com/v21.0/{page_id}/videos",
        form_data={
            "file_url": video_url,
            "description": fb_caption,
            "published": "true",
            "access_token": page_token,
        },
    )
    if st == 200 and "id" in data:
        return {"ok": True, "id": data["id"]}
    return {"ok": False, "error": f"Error publicando Reel en Facebook Page: {data}"}


def publish_linkedin(keys, feed_rel_path, caption, article_url, title):
    """
    REGLA INQUEBRANTABLE:
    1) Bloqueo duro de cualquier perfil personal (urn:li:person:). Solo permite urn:li:organization:35644861.
    2) Subida binaria de la placa gráfica 1080x1350 (registerUpload + shareMediaCategory: IMAGE)
       para que LinkedIn muestre la imagen completa y no un recuadro gris.
    """
    li_token = keys.get("linkedin_token")
    li_urn = keys.get("linkedin_urn") or STAR_UNION_LI_ORG_URN
    if not li_token or not li_urn:
        return {"ok": False, "error": "Falta conectar LinkedIn Página de Empresa."}
    if "urn:li:person:" in li_urn or li_urn != STAR_UNION_LI_ORG_URN:
        return {
            "ok": False,
            "error": f"🛑 BLOQUEADO POR SEGURIDAD: El URN ({li_urn}) no coincide con la Página de Empresa de Star Union ({STAR_UNION_LI_ORG_URN}).",
        }

    hdrs = {"Authorization": f"Bearer {li_token}", "X-Restli-Protocol-Version": "2.0.0"}
    img_path = os.path.join(WEB_ROOT, "redes-sociales", feed_rel_path.lstrip("/"))
    asset_urn = None

    if os.path.exists(img_path):
        reg_body = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": li_urn,
                "serviceRelationships": [
                    {"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}
                ],
            }
        }
        st_reg, reg_data = http_json(
            "POST",
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=hdrs,
            json_body=reg_body,
        )
        if st_reg in (200, 201):
            val = reg_data.get("value", {})
            upload_url = (
                val.get("uploadMechanism", {})
                .get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {})
                .get("uploadUrl", "")
            )
            asset_urn = val.get("asset", "")
            if upload_url and asset_urn:
                with open(img_path, "rb") as f:
                    img_bytes = f.read()
                req_put = urllib.request.Request(
                    upload_url,
                    data=img_bytes,
                    headers={"Authorization": f"Bearer {li_token}", "Content-Type": "image/jpeg"},
                    method="PUT",
                )
                try:
                    urllib.request.urlopen(req_put, timeout=45).read()
                except Exception as ex:
                    return {"ok": False, "error": f"Error subiendo imagen a LinkedIn: {ex}"}

    clean_title = (title or "STAR UNION").strip().upper()
    full_text = f"{clean_title}\n\n{(caption or '').strip()}"
    if article_url and article_url not in full_text:
        full_text += f"\n\n👉 Protocolo técnico y contacto directo: {article_url}"

    if asset_urn:
        body = {
            "author": li_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": full_text},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn,
                            "title": {"text": title or "Star Union"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
    else:
        body = {
            "author": li_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": full_text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": article_url,
                            "title": {"text": title or "Star Union"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

    st, data = http_json("POST", "https://api.linkedin.com/v2/ugcPosts", headers=hdrs, json_body=body)
    if st in (200, 201) and "id" in data:
        return {"ok": True, "id": data["id"]}
    return {"ok": False, "error": f"Error en LinkedIn API ({st}): {data}"}


def publish_gmb(keys, feed_rel_path, caption, article_url="https://www.starunion.com.ar"):
    gmb_token = ensure_fresh_gmb_token(keys)
    gmb_loc = keys.get("gmb_location_name")
    if not gmb_token or not gmb_loc:
        return {"ok": False, "error": "Falta conectar o renovar Google My Business."}

    img_url = f"{PUBLIC_ASSET_BASE}/{feed_rel_path.lstrip('/')}"
    body = {
        "languageCode": "es-AR",
        "summary": (caption or "")[:1450],
        "callToAction": {"actionType": "LEARN_MORE", "url": article_url},
        "media": [{"mediaFormat": "PHOTO", "sourceUrl": img_url}],
        "topicType": "STANDARD",
    }
    st, data = http_json(
        "POST",
        f"https://mybusiness.googleapis.com/v4/{gmb_loc}/localPosts",
        headers={"Authorization": f"Bearer {gmb_token}"},
        json_body=body,
    )
    if st in (200, 201) and "name" in data:
        return {"ok": True, "id": data["name"]}
    return {"ok": False, "error": f"Error en Google Business Profile API ({st}): {data}"}


def publish_youtube_short(keys, reel_rel_path, title, description, tags_csv=""):
    yt_token = ensure_fresh_youtube_token(keys)
    if not yt_token:
        return {"ok": False, "error": "Falta conectar o renovar el Token de YouTube Shorts."}

    clean_rel = reel_rel_path.split("?")[0].lstrip("/")
    local_mp4 = os.path.join(WEB_ROOT, "redes-sociales", clean_rel)
    if not os.path.exists(local_mp4):
        return {"ok": False, "error": f"No se encontró el archivo MP4 local: {local_mp4}"}

    with open(local_mp4, "rb") as f:
        video_bytes = f.read()

    short_title = (title or "Star Union — Empresa de Limpieza Industrial").strip()
    if "#Shorts" not in short_title and "#shorts" not in short_title:
        short_title = short_title[:88].strip() + " #Shorts"
    else:
        short_title = short_title[:98]

    tags_list = [t.strip() for t in (tags_csv or "").split(",") if t.strip()][:15]
    if "Shorts" not in tags_list:
        tags_list.append("Shorts")

    meta = {
        "snippet": {
            "title": short_title,
            "description": (description or "") + "\n\n#Shorts #EmpresaDeLimpieza #StarUnion",
            "tags": tags_list,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    req = urllib.request.Request(
        init_url,
        data=json.dumps(meta).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {yt_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(len(video_bytes)),
            "X-Upload-Content-Type": "video/mp4",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            upload_url = resp.headers.get("Location")
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"Error iniciando subida a YouTube ({e.code}): {e.read().decode('utf-8', 'replace')}"}
    except Exception as e:
        return {"ok": False, "error": f"Error de red con YouTube: {e}"}

    if not upload_url:
        return {"ok": False, "error": "YouTube no devolvió Location header para subida resumable."}

    put_req = urllib.request.Request(
        upload_url,
        data=video_bytes,
        headers={
            "Authorization": f"Bearer {yt_token}",
            "Content-Type": "video/mp4",
            "Content-Length": str(len(video_bytes)),
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(put_req, timeout=180) as resp2:
            out = json.loads(resp2.read().decode("utf-8"))
            vid_id = out.get("id", "")
            return {"ok": True, "id": f"https://youtube.com/shorts/{vid_id}"}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"Error subiendo bytes a YouTube ({e.code}): {e.read().decode('utf-8', 'replace')}"}
    except Exception as e:
        return {"ok": False, "error": f"Error completando subida a YouTube: {e}"}


def publish_tiktok(keys, reel_rel_path, caption):
    """
    REGLA INQUEBRANTABLE:
    En TikTok jamás usar PULL_FROM_URL (exige verificación de dominio y auditoría).
    Siempre subir el archivo binario local con FILE_UPLOAD y usar fallback automático
    a /v2/post/publish/inbox/video/init/ para apps en modo Sandbox / sin auditar.
    """
    tt_token = ensure_fresh_tiktok_token(keys)
    if not tt_token:
        return {"ok": False, "error": "Falta conectar o renovar TikTok."}

    clean_rel = reel_rel_path.split("?")[0].lstrip("/")
    video_path = os.path.join(WEB_ROOT, "redes-sociales", clean_rel)
    if not os.path.exists(video_path):
        return {"ok": False, "error": f"No existe el archivo MP4 local: {video_path}"}

    with open(video_path, "rb") as f:
        video_bytes = f.read()
    size = len(video_bytes)

    hdrs = {
        "Authorization": f"Bearer {tt_token}",
        "Content-Type": "application/json; charset=UTF-8",
    }

    st_ci, ci_data = http_json("POST", "https://open.tiktokapis.com/v2/post/publish/creator_info/query/", headers=hdrs, json_body={})
    priv_opts = ci_data.get("data", {}).get("privacy_level_options", [])
    privacy = "PUBLIC_TO_EVERYONE" if "PUBLIC_TO_EVERYONE" in priv_opts else ("SELF_ONLY" if "SELF_ONLY" in priv_opts else (priv_opts[0] if priv_opts else "SELF_ONLY"))

    upload_url = ""
    pub_id = ""
    mode_note = "Publicado directo"

    if st_ci == 200:
        body = {
            "post_info": {
                "title": (caption or "")[:2000],
                "privacy_level": privacy,
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": size,
                "chunk_size": size,
                "total_chunk_count": 1,
            },
        }
        st, data = http_json("POST", "https://open.tiktokapis.com/v2/post/publish/video/init/", headers=hdrs, json_body=body)
        if st == 200 and data.get("data", {}).get("upload_url"):
            upload_url = data["data"]["upload_url"]
            pub_id = data["data"].get("publish_id", "")

    if not upload_url:
        inbox_body = {
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": size,
                "chunk_size": size,
                "total_chunk_count": 1,
            }
        }
        st_in, data_in = http_json("POST", "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/", headers=hdrs, json_body=inbox_body)
        if st_in == 200 and data_in.get("data", {}).get("upload_url"):
            upload_url = data_in["data"]["upload_url"]
            pub_id = data_in["data"].get("publish_id", "")
            mode_note = "Enviado a la Bandeja de TikTok (@starunionservicios listos para 1 toque)"
        else:
            return {"ok": False, "error": f"Error iniciando subida en TikTok API: {data_in}"}

    put_req = urllib.request.Request(
        upload_url,
        data=video_bytes,
        headers={
            "Content-Type": "video/mp4",
            "Content-Length": str(size),
            "Content-Range": f"bytes 0-{size - 1}/{size}",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(put_req, timeout=120) as _:
            return {"ok": True, "id": f"{pub_id} ({mode_note})"}
    except Exception as e:
        return {"ok": False, "error": f"Error subiendo bytes del MP4 a TikTok: {e}"}


# =====================================================================
# 3. SERVIDOR HTTP LOCAL + ENDPOINTS /api/status, /api/connect, /api/publish, /api/schedule
# =====================================================================
class StarUnionAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def _send_json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/tiktok/login"):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            keys = load_keys()
            ck = (qs.get("client_key", [""])[0] or keys.get("tiktok_client_key", "")).strip()
            cs = (qs.get("client_secret", [""])[0] or keys.get("tiktok_client_secret", "")).strip()
            if ck or cs:
                save_keys({"tiktok_client_key": ck, "tiktok_client_secret": cs})
            redirect_uri = "https://wajntraub.ar/staruniontest/redes-sociales/tiktok-callback.html"
            auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode(
                {
                    "client_key": ck,
                    "scope": "user.info.basic,video.upload",
                    "response_type": "code",
                    "redirect_uri": redirect_uri,
                    "state": "starunion_tt",
                }
            )
            self.send_response(302)
            self.send_header("Location", auth_url)
            self.end_headers()
            return

        if self.path.startswith("/api/tiktok/callback"):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            code = urllib.parse.unquote(qs.get("code", [""])[0]).strip()
            keys = load_keys()
            ck = keys.get("tiktok_client_key", "")
            cs = keys.get("tiktok_client_secret", "")
            redirect_uri = "https://wajntraub.ar/staruniontest/redes-sociales/tiktok-callback.html"
            st, data = http_json(
                "POST",
                "https://open.tiktokapis.com/v2/oauth/token/",
                form_data={
                    "client_key": ck,
                    "client_secret": cs,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                },
            )
            tok = data.get("access_token") or data.get("data", {}).get("access_token", "")
            open_id = data.get("open_id") or data.get("data", {}).get("open_id", "")
            rt = data.get("refresh_token") or data.get("data", {}).get("refresh_token", "")
            if tok:
                save_keys({"tiktok_token": tok, "tiktok_open_id": open_id, "tiktok_refresh_token": rt})
                html = "<html><head><meta charset='utf-8'></head><body style='font-family:sans-serif;background:#064e3b;color:#fff;padding:40px;text-align:center;'><h2>✅ ¡TikTok de Star Union Conectado con Éxito!</h2><p>Redirigiendo al panel...</p><script>setTimeout(()=>location.href='/redes-sociales/index.html', 1000);</script></body></html>"
            else:
                html = f"<html><head><meta charset='utf-8'></head><body style='font-family:sans-serif;background:#7f1d1d;color:#fff;padding:40px;'><h2>❌ Error obteniendo token de TikTok</h2><pre>{json.dumps(data, indent=2)}</pre><p><a href='/redes-sociales/index.html' style='color:#fde047;'>← Volver al panel</a></p></body></html>"
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path.startswith("/api/status"):
            keys = load_keys()
            tok_meta = keys.get("fb_page_token") or keys.get("meta_user_token")
            meta_ok = False
            meta_expired = False
            if tok_meta:
                st_m, dm = http_json(
                    "GET",
                    f"https://graph.facebook.com/v21.0/me?fields=id,name&access_token={urllib.parse.quote(tok_meta)}",
                )
                if st_m == 200 and dm.get("id"):
                    meta_ok = True
                else:
                    meta_expired = True

            yt_tok = ensure_fresh_youtube_token(keys)
            yt_ok = False
            yt_expired = False
            if yt_tok:
                st_y, _ = http_json("GET", "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true", headers={"Authorization": f"Bearer {yt_tok}"})
                if st_y == 200:
                    yt_ok = True
                else:
                    yt_expired = True

            gmb_tok = ensure_fresh_gmb_token(keys)
            gmb_ok = False
            gmb_expired = False
            if gmb_tok and keys.get("gmb_location_name"):
                st_g, _ = http_json("GET", "https://mybusinessaccountmanagement.googleapis.com/v1/accounts", headers={"Authorization": f"Bearer {gmb_tok}"})
                if st_g == 200:
                    gmb_ok = True
                else:
                    gmb_expired = True

            tt_tok = ensure_fresh_tiktok_token(keys)
            tt_ok = bool(tt_tok)
            li_ok = bool(keys.get("linkedin_token") and keys.get("linkedin_urn") == STAR_UNION_LI_ORG_URN)

            self._send_json(
                200,
                {
                    "ok": True,
                    "meta_connected": meta_ok,
                    "meta_expired": meta_expired,
                    "fb_page_name": keys.get("fb_page_name", ""),
                    "fb_page_id": keys.get("fb_page_id", ""),
                    "ig_username": keys.get("ig_username", ""),
                    "ig_user_id": keys.get("ig_user_id", ""),
                    "linkedin_connected": li_ok,
                    "linkedin_name": keys.get("linkedin_name", ""),
                    "linkedin_urn": keys.get("linkedin_urn", ""),
                    "gmb_connected": gmb_ok,
                    "gmb_expired": gmb_expired,
                    "gmb_has_refresh": bool(keys.get("gmb_refresh_token")),
                    "gmb_location_name": keys.get("gmb_location_name", ""),
                    "gmb_location_title": keys.get("gmb_title", ""),
                    "youtube_connected": yt_ok,
                    "youtube_expired": yt_expired,
                    "youtube_has_refresh": bool(keys.get("youtube_refresh_token")),
                    "youtube_channel_name": keys.get("youtube_channel_name", ""),
                    "tiktok_connected": tt_ok,
                },
            )
            return

        if self.path.startswith("/api/schedule"):
            sched_path = os.path.join(WEB_ROOT, "redes-sociales", "calendario_programado.json")
            data = {}
            if os.path.exists(sched_path):
                try:
                    with open(sched_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            self._send_json(200, {"ok": True, "schedule": data})
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
            meta_secret = (body.get("meta_app_secret") or "").strip()
            if meta_secret:
                updates["meta_app_secret"] = meta_secret
            if meta_token:
                disc = auto_discover_meta(meta_token, meta_secret)
                if disc.get("ok"):
                    updates.update(disc)
                    perm_txt = " (TOKEN PERMANENTE SIN VENCIMIENTO)" if disc.get("permanent") else " (Agregá la Clave Secreta de la App para que no venza en 1h)"
                    messages.append(
                        f"✅ Meta conectado: FB Page '{updates.get('fb_page_name')}' ({updates.get('fb_page_id')}) + IG @{updates.get('ig_username')}{perm_txt}"
                    )
                else:
                    updates["meta_user_token"] = meta_token
                    updates["fb_page_token"] = meta_token
                    messages.append(f"⚠️ Token de Meta guardado (revisar permisos): {disc.get('detail')}")

            li_token = (body.get("linkedin_token") or "").strip()
            li_urn = (body.get("linkedin_urn") or "").strip()
            if li_token:
                disc_li = auto_discover_linkedin(li_token, li_urn)
                if disc_li.get("ok"):
                    updates.update(disc_li)
                    messages.append(f"✅ LinkedIn conectado: {disc_li.get('linkedin_name')}")
                else:
                    messages.append(disc_li.get("detail", "❌ Error en LinkedIn"))

            gmb_token = (body.get("gmb_token") or "").strip()
            gmb_loc = (body.get("gmb_location_name") or "").strip()
            if gmb_token:
                disc_gmb = auto_discover_gmb(gmb_token, gmb_loc)
                updates.update(disc_gmb)
                if disc_gmb.get("ok"):
                    rt_note = " (Refresh Token permanente activo)" if disc_gmb.get("gmb_refresh_token") else ""
                    messages.append(f"✅ Google My Business conectado: {disc_gmb.get('gmb_location_name')}{rt_note}")
                else:
                    messages.append(f"⚠️ {disc_gmb.get('detail')}")

            yt_token = (body.get("youtube_token") or "").strip()
            if yt_token:
                disc_yt = auto_discover_youtube(yt_token)
                if disc_yt.get("ok"):
                    updates.update(disc_yt)
                    rt_note = " (Refresh Token permanente activo)" if disc_yt.get("youtube_refresh_token") else ""
                    messages.append(f"✅ Canal de YouTube conectado: {disc_yt.get('youtube_channel_name')}{rt_note}")
                else:
                    updates["youtube_token"] = yt_token
                    messages.append(f"⚠️ Token de YouTube guardado (verificá scope youtube.upload): {disc_yt.get('detail')}")

            tt_token = (body.get("tiktok_token") or "").strip()
            if tt_token:
                updates["tiktok_token"] = tt_token
                messages.append("✅ Token de TikTok Content Posting API guardado.")

            tt_ck = (body.get("tiktok_client_key") or "").strip()
            tt_cs = (body.get("tiktok_client_secret") or "").strip()
            if tt_ck or tt_cs:
                if tt_ck:
                    updates["tiktok_client_key"] = tt_ck
                if tt_cs:
                    updates["tiktok_client_secret"] = tt_cs
                messages.append("✅ Credenciales Client Key / Secret de TikTok guardadas.")

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
            yt_title = body.get("yt_title", "Star Union · Limpieza Corporativa e Industrial #Shorts")
            yt_desc = body.get("yt_desc", caption_ig)
            yt_tags = body.get("yt_tags", "empresa de limpieza, star union, limpieza industrial, iso 9001")
            public_url = body.get("public_url", "https://www.starunion.com.ar")
            title = body.get("title", "Star Union")

            results = {}
            if "ig_feed" in channels:
                results["Instagram Feed (4:5)"] = publish_ig_feed(keys, feed_file, caption_ig)
            if "ig_story" in channels:
                results["Instagram Story Video c/Música (9:16)"] = publish_ig_story(keys, story_file, reel_file)
            if "ig_reel" in channels:
                results["Instagram Reel con Voz Varón + Funk (MP4)"] = publish_ig_reel(keys, reel_file, caption_ig)
            if "fb_page" in channels:
                results["Facebook Page"] = publish_fb_page(keys, feed_file, caption_ig, public_url)
            if "fb_reel" in channels:
                results["Facebook Reel MP4"] = publish_fb_reel(keys, reel_file, caption_ig, public_url)
            if "linkedin" in channels:
                results["LinkedIn Página Empresa (Imagen Nativa)"] = publish_linkedin(keys, feed_file, caption_li, public_url, title)
            if "gmb" in channels:
                results["Google My Business (Maps)"] = publish_gmb(keys, feed_file, caption_ig, public_url)
            if "youtube" in channels:
                results["YouTube Shorts (@starunionservicios)"] = publish_youtube_short(keys, reel_file, yt_title, yt_desc, yt_tags)
            if "tiktok" in channels:
                results["TikTok Video (FILE_UPLOAD)"] = publish_tiktok(keys, reel_file, caption_ig)

            self._send_json(200, {"ok": True, "results": results})
            return

        if self.path.startswith("/api/schedule"):
            sched_path = os.path.join(WEB_ROOT, "redes-sociales", "calendario_programado.json")
            data = {}
            if os.path.exists(sched_path):
                try:
                    with open(sched_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}

            post_id = str(body.get("id", "01")).zfill(2)
            entry = data.get(post_id, {})
            for k in (
                "scheduled_at",
                "status",
                "tag",
                "title",
                "subtitle",
                "copy_ig_fb",
                "copy_linkedin",
                "yt_title",
                "yt_desc",
                "yt_tags",
                "copy_wa",
                "channels",
                "feed_file",
                "story_file",
                "reel_file",
            ):
                if k in body:
                    entry[k] = body[k]
            data[post_id] = entry

            with open(sched_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            regen_msg = ""
            if body.get("regenerate_image"):
                try:
                    import sys
                    rs_dir = os.path.join(WEB_ROOT, "redes-sociales")
                    if rs_dir not in sys.path:
                        sys.path.insert(0, rs_dir)
                    import generar_pack_redes as gpr
                    import actualizar_editable_y_calendario as aec
                    from PIL import Image
                    for p in gpr.POSTS:
                        if p["id"] == post_id:
                            if entry.get("tag"):
                                p["tag"] = entry["tag"]
                            if entry.get("title"):
                                p["title"] = entry["title"]
                            if entry.get("subtitle"):
                                p["subtitle"] = entry["subtitle"]
                            feed_html = os.path.join(gpr.TMP_DIR, f"feed_{p['id']}.html")
                            feed_png = os.path.join(gpr.TMP_DIR, f"feed_{p['id']}.png")
                            feed_jpg = os.path.join(gpr.PIEZAS_DIR, f"{p['id']}_feed_{p['slug']}_1080x1350.jpg")
                            with open(feed_html, "w", encoding="utf-8") as hf:
                                hf.write(gpr.build_feed_html(p))
                            gpr.render_screenshot(feed_html, feed_png, 1080, 1350)
                            Image.open(feed_png).convert("RGB").save(feed_jpg, "JPEG", quality=95)

                            story_html = os.path.join(gpr.TMP_DIR, f"story_{p['id']}.html")
                            story_png = os.path.join(gpr.TMP_DIR, f"story_{p['id']}.png")
                            story_jpg = os.path.join(gpr.PIEZAS_DIR, f"{p['id']}_story_{p['slug']}_1080x1920.jpg")
                            with open(story_html, "w", encoding="utf-8") as hf:
                                hf.write(gpr.build_story_html(p))
                            gpr.render_screenshot(story_html, story_png, 1080, 1920)
                            Image.open(story_png).convert("RGB").save(story_jpg, "JPEG", quality=95)

                            aec.create_editable_svg(p, 1080, 1350, os.path.join(gpr.PIEZAS_DIR, f"{p['id']}_feed_{p['slug']}_EDITABLE.svg"))
                            aec.create_editable_svg(p, 1080, 1920, os.path.join(gpr.PIEZAS_DIR, f"{p['id']}_story_{p['slug']}_EDITABLE.svg"))
                            regen_msg = " + Placas JPG (1080×1350 y 1080×1920) y SVGs regenerados en vivo."
                            break
                except Exception as ex:
                    regen_msg = f" (Aviso placa: {ex})"

            self._send_json(200, {"ok": True, "entry": entry, "message": f"✅ Guardado Pieza #{post_id} ({entry.get('status', 'guardado')} para {entry.get('scheduled_at', '')}){regen_msg}"})
            return

        if self.path.startswith("/api/perfit/create-draft"):
            try:
                perfit_vault = os.path.join(WEB_ROOT, ".agents", "vault", "perfit.json")
                pf = json.load(open(perfit_vault, "r", encoding="utf-8"))
                account = pf.get("account", "starunionsrl")
                api_key = pf.get("api_key", "")
                opt = str(body.get("option", "A")).upper()
                subj = body.get("subject", "Continuidad operativa e infraestructura propia º Star ⭐ Union")
                fname = "mailing-apertura-funnel1-opcion-A.html" if opt == "A" else "mailing-apertura-funnel1-opcion-B.html"
                html_content = open(os.path.join(WEB_ROOT, "redes-sociales", fname), "r", encoding="utf-8").read()
                payload_pf = {
                    "name": f"Funnel 1 Apertura - Opción {opt} (Star Union)",
                    "subject": subj,
                    "from": {"email": "info@starunion.com.ar", "name": "Star Union"},
                    "replyTo": {"email": "info@starunion.com.ar", "name": "Star Union"},
                    "content": {"html": html_content},
                }
                st_pf, res_pf = http_json(
                    "POST",
                    f"https://api.myperfit.com/v2/{account}/campaigns",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json_body=payload_pf,
                )
                if st_pf in (200, 201) and res_pf.get("data"):
                    cid = res_pf["data"].get("id", "")
                    cname = res_pf["data"].get("name", f"Opción {opt}")
                    self._send_json(200, {"ok": True, "campaign_id": cid, "name": cname})
                else:
                    self._send_json(200, {"ok": False, "error": f"Perfit ({st_pf}): {res_pf}"})
            except Exception as ex:
                self._send_json(200, {"ok": False, "error": str(ex)})
            return

        self._send_json(404, {"error": "Endpoint no encontrado"})


def run_scheduler_loop():
    import datetime
    sched_path = os.path.join(WEB_ROOT, "redes-sociales", "calendario_programado.json")
    while True:
        try:
            if os.path.exists(sched_path):
                with open(sched_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                now_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
                changed = False
                keys = load_keys()
                for pid, entry in data.items():
                    if entry.get("status") == "programado" and entry.get("scheduled_at") and entry["scheduled_at"] <= now_str:
                        channels = entry.get("channels", [])
                        feed_file = entry.get("feed_file", f"piezas/{pid}_feed_logistica_industria_1080x1350.jpg")
                        story_file = entry.get("story_file", f"piezas/{pid}_story_logistica_industria_1080x1920.jpg")
                        reel_file = entry.get("reel_file", "piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4")
                        caption_ig = entry.get("copy_ig_fb", "")
                        caption_li = entry.get("copy_linkedin", "")
                        yt_title = entry.get("yt_title", "Star Union — Empresa de Limpieza #Shorts")
                        yt_desc = entry.get("yt_desc", caption_ig)
                        yt_tags = entry.get("yt_tags", "empresa de limpieza, star union, limpieza industrial")
                        public_url = "https://www.starunion.com.ar"
                        title = entry.get("title", "Star Union")
                        res = {}
                        if "ig_feed" in channels:
                            res["IG Feed"] = publish_ig_feed(keys, feed_file, caption_ig)
                        if "ig_story" in channels:
                            res["IG Story Video"] = publish_ig_story(keys, story_file, reel_file)
                        if "ig_reel" in channels:
                            res["IG Reel"] = publish_ig_reel(keys, reel_file, caption_ig)
                        if "fb_page" in channels:
                            res["FB Page"] = publish_fb_page(keys, feed_file, caption_ig, public_url)
                        if "fb_reel" in channels:
                            res["FB Reel"] = publish_fb_reel(keys, reel_file, caption_ig, public_url)
                        if "linkedin" in channels:
                            res["LinkedIn"] = publish_linkedin(keys, feed_file, caption_li, public_url, title)
                        if "gmb" in channels:
                            res["Google Maps"] = publish_gmb(keys, feed_file, caption_ig, public_url)
                        if "youtube" in channels:
                            res["YouTube"] = publish_youtube_short(keys, reel_file, yt_title, yt_desc, yt_tags)
                        if "tiktok" in channels:
                            res["TikTok"] = publish_tiktok(keys, reel_file, caption_ig)
                        entry["status"] = "publicado"
                        entry["published_at"] = now_str
                        entry["last_results"] = res
                        changed = True
                if changed:
                    with open(sched_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        time.sleep(25)


if __name__ == "__main__":
    import threading
    t2 = threading.Thread(target=run_scheduler_loop, daemon=True)
    t2.start()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 8894), StarUnionAPIHandler)
    print("STAR UNION API Server corriendo en http://127.0.0.1:8894")
    server.serve_forever()
