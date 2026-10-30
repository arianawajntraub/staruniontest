#!/usr/bin/env python3
"""
Sincroniza las 5 tiras de Canva (Opción 2: 30/10 Salud, 02/11 Equipos Listos, 03/11 Edificios Corporativos,
05/11 Respuesta Inmediata, 06/11 Maquinaria Lista) en formato 4:5 (IG/FB/LI/GMB) y 9:16 (Reels/Shorts/TikTok/Story),
permite actualizar en Canva: Volanta, Bajada, Placa 2, Placa 3 y Cierre según Rubro,
y genera los 5 Reels MP4 de 12 segundos (3 seg por placa x 4 placas) con zoom suave de portada (cero deformación IA)
y el audio oficial aprobado `starunion_funk_firma_varon_12s.mp3` (locución masculina 1 sola vez al inicio + música libre de derechos).
"""
import json
import os
import subprocess
import urllib.request
from PIL import Image
import imageio_ffmpeg

ROOT_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"
RS_DIR = os.path.join(ROOT_DIR, "redes-sociales")
SYNC_DIR = os.path.join(RS_DIR, "canva_sync")
PIEZAS_DIR = os.path.join(RS_DIR, "piezas")
AUDIO_12S = os.path.join(ROOT_DIR, "audio", "starunion_funk_firma_varon_12s.mp3")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

os.makedirs(SYNC_DIR, exist_ok=True)
os.makedirs(PIEZAS_DIR, exist_ok=True)

CANVA_SERIES = [
    {
        "id": "01",
        "slug": "3010_salud",
        "date_label": "Hoy Viernes 30/10 · 10:30 hs (Lista para aprobar)",
        "scheduled_at": "2026-10-30T10:30",
        "format_mode": "Canva Dinámico (Opción 2) + Video 12s con Locución",
        "ig_design_id": "DAHYlLXJOQw",
        "tt_design_id": "DAHYlJA4Xrs",
        "fb_design_id": "DAHYlOsMQm8",
        "li_design_id": "DAHYlI0nApU",
        "gmb_design_id": "DAHYlJl2ItI",
        "yt_design_id": "DAHYlHyEScA",
        "volanta": "SALUD",
        "bajada": "CLÍNICAS\nY SANATORIOS",
        "placa2": "Trabajamos con protocolos específicos para cada área de tu clínica y con personal formado en nuestro propio centro de capacitación",
        "placa3": "Organizamos los turnos para que salas de espera, consultorios, pasillos y ascensores estén listos antes de cada atención, con supervisores que controlan cada área",
        "cierre_rubro": "Cotizá hoy para tu clínica o sanatorio",
        "editorial_feed": "piezas/04_feed_salud_laboratorios_1080x1350.jpg",
        "copy_ig_fb": (
            "Limpieza técnica para clínicas, sanatorios, centros médicos y laboratorios en CABA y GBA.\n\n"
            "• Protocolos específicos por sector crítico y áreas de atención.\n"
            "• Personal formado en nuestro propio Centro de Capacitación en Base Guaminí.\n"
            "• Organización por turnos para que salas de espera, consultorios, pasillos y ascensores estén listos antes de cada recepción.\n"
            "• Supervisión operativa y gestión certificada bajo Norma ISO 9001:2015 por TÜV Rheinland (ID 9000041847).\n\n"
            "📲 Cotizá tu servicio hoy por WhatsApp: +54 9 11 2275-9369\n"
            "🌐 https://www.starunion.com.ar\n\n"
            "#StarUnion #EmpresaDeLimpieza #LimpiezaHospitalaria #ClinicasYSanatorios #SaludB2B #ISO9001 #LimpiezaProfesional"
        ),
        "copy_linkedin": (
            "En instituciones de salud, clínicas, sanatorios y laboratorios, la higiene técnica exige trazabilidad por sector y coordinación horaria precisa.\n\n"
            "En Star Union S.R.L. ejecutamos servicios de limpieza institucional para el sector salud con respaldo propio:\n"
            "✔️ Protocolos operativos diferenciados para salas de espera, consultorios, laboratorios, pasillos y circulación vertical.\n"
            "✔️ Equipos entrenados en nuestro Centro de Capacitación propio antes de ingresar al objetivo.\n"
            "✔️ Supervisión en sitio y control biométrico de presentismo.\n"
            "✔️ Sistema de Gestión de Calidad certificado bajo Norma ISO 9001:2015 por TÜV Rheinland (Certipedia ID 9000041847).\n\n"
            "Solicitá un relevamiento técnico para tu institución médica:\n"
            "🌐 https://www.starunion.com.ar | 📲 +54 9 11 2275-9369\n\n"
            "#StarUnion #Salud #GestionHospitalaria #FacilityManagement #ISO9001 #LimpiezaInstitucional"
        ),
        "yt_title": "Limpieza para Clínicas y Sanatorios (ISO 9001) — Star Union #Shorts",
    },
    {
        "id": "02",
        "slug": "0211_equipos_listos",
        "date_label": "Lunes 02/11 · 10:00 hs",
        "scheduled_at": "2026-11-02T10:00",
        "format_mode": "Canva Dinámico (Opción 2) + Video 12s con Locución",
        "ig_design_id": "DAHYlMTU6ko",
        "tt_design_id": "DAHYlOiwq8o",
        "fb_design_id": "DAHYlBxzqDg",
        "li_design_id": "DAHYlAOha2s",
        "gmb_design_id": "DAHYlH-ToGQ",
        "yt_design_id": "DAHYlIufvCY",
        "volanta": "CENTRO DE CAPACITACIÓN",
        "bajada": "EQUIPOS LISTOS",
        "placa2": "Cada operario se forma en nuestro centro de capacitación antes de llegar a tu servicio, así aprende los procesos, los productos y las máquinas con las que va a trabajar",
        "placa3": "Al terminar cada curso entregamos un certificado, y después un supervisor acompaña en el lugar para que lo aprendido se aplique en cada turno",
        "cierre_rubro": "Sumá un equipo capacitado a tu empresa",
        "editorial_feed": "piezas/02_feed_base_operativa_taller_1080x1350.jpg",
        "copy_ig_fb": (
            "Equipos listos y formados en nuestro propio Centro de Capacitación antes de ingresar a tu empresa.\n\n"
            "• En nuestra base operativa de Guaminí 5657 (CABA), cada operario se entrena en procesos, dosificación de insumos y manejo seguro de maquinaria.\n"
            "• Certificamos cada instancia formativa y acompañamos con supervisión en campo para sostener el estándar en cada turno.\n"
            "• Gestión certificada ISO 9001:2015 por TÜV Rheinland.\n\n"
            "📲 Pedí tu cotización por WhatsApp: +54 9 11 2275-9369\n"
            "🌐 https://www.starunion.com.ar\n\n"
            "#StarUnion #EmpresaDeLimpieza #CapacitacionOperativa #LimpiezaCorporativa #ISO9001 #FacilityServices"
        ),
        "copy_linkedin": (
            "La calidad de un servicio de limpieza B2B empieza antes del primer turno en las instalaciones del cliente.\n\n"
            "En Star Union S.R.L. contamos con nuestro propio Centro de Capacitación dentro de la base operativa de Guaminí 5657 (CABA):\n"
            "✔️ Entrenamiento práctico previo en procedimientos, seguridad e higiene y operación de maquinaria.\n"
            "✔️ Certificación interna por curso y seguimiento de supervisores en el objetivo.\n"
            "✔️ Respaldo documental completo y certificación TÜV Rheinland ISO 9001:2015.\n\n"
            "Conocé nuestra infraestructura operativa:\n"
            "🌐 https://www.starunion.com.ar | 📲 +54 9 11 2275-9369\n\n"
            "#StarUnion #Capacitacion #LimpiezaProfesional #RRHH #OperacionesB2B #ISO9001"
        ),
        "yt_title": "Centro de Capacitación Propio y Equipos Listos — Star Union #Shorts",
    },
    {
        "id": "03",
        "slug": "0311_edificios_corporativos",
        "date_label": "Martes 03/11 · 10:00 hs (Intercalado con Placa Editorial)",
        "scheduled_at": "2026-11-03T10:00",
        "format_mode": "Intercalado: Placa Editorial en Feed + Reel Canva 12s",
        "ig_design_id": "DAHYlPsIWAA",
        "tt_design_id": "DAHYlOhqcCM",
        "fb_design_id": "DAHYlItqjNo",
        "li_design_id": "DAHYlAfM8G0",
        "gmb_design_id": "DAHYlIqgzas",
        "yt_design_id": "DAHYlADnG0c",
        "volanta": "EDIFICIOS CORPORATIVOS",
        "bajada": "UN SOLO PROVEEDOR",
        "placa2": "Halls, ascensores, cocheras y pisos de oficina se integran en un solo abono con rutinas por horario, así el edificio está listo antes de que llegue la gente",
        "placa3": "Unificar la limpieza en un solo proveedor te ahorra coordinación, tiempo y costos, y te deja un único responsable para todo, incluidos los vidrios en altura",
        "cierre_rubro": "Cotizá hoy el abono integral de tu edificio",
        "editorial_feed": "piezas/05_feed_universidades_clubes_1080x1350.jpg",
        "copy_ig_fb": (
            "Un solo proveedor integral para edificios corporativos, torres de oficinas y consorcios en CABA y GBA.\n\n"
            "• Integramos halls, ascensores, cocheras, pisos de oficinas y limpieza de vidrios en altura en un único abono coordinado por franja horaria.\n"
            "• Ahorrá tiempos de gestión y costos operativos con un único equipo responsable y supervisión permanente.\n"
            "• Calidad certificada ISO 9001:2015 por TÜV Rheinland.\n\n"
            "📲 Cotizá el abono de tu edificio por WhatsApp: +54 9 11 2275-9369\n"
            "🌐 https://www.starunion.com.ar\n\n"
            "#StarUnion #EdificiosCorporativos #LimpiezaDeOficinas #LimpiezaEnAltura #FacilityManagement #Consorcios"
        ),
        "copy_linkedin": (
            "Unificar la higiene de un edificio corporativo en un solo proveedor certificado reduce costos de coordinación y garantiza trazabilidad.\n\n"
            "En Star Union S.R.L. integramos bajo un mismo abono:\n"
            "✔️ Puesta a punto de halls de acceso, ascensores, cocheras y pisos de oficinas antes del ingreso del personal.\n"
            "✔️ Cuadrillas propias para limpieza de vidrios y fachadas en altura.\n"
            "✔️ Un único interlocutor operativo con certificación ISO 9001:2015 (TÜV Rheinland).\n\n"
            "Solicitá una propuesta integral para tu edificio o torre corporativa:\n"
            "🌐 https://www.starunion.com.ar | 📲 +54 9 11 2275-9369\n\n"
            "#StarUnion #RealEstateCorporativo #EdificiosDeOficinas #FacilityManagement #LimpiezaEnAltura #ISO9001"
        ),
        "yt_title": "Limpieza Integral para Edificios Corporativos — Star Union #Shorts",
    },
    {
        "id": "04",
        "slug": "0511_respuesta_inmediata",
        "date_label": "Jueves 05/11 · 10:00 hs",
        "scheduled_at": "2026-11-05T10:00",
        "format_mode": "Canva Dinámico (Opción 2) + Video 12s con Locución",
        "ig_design_id": "DAHYlKE5KiY",
        "tt_design_id": "DAHYlLcWsJU",
        "fb_design_id": "DAHYlFux4cI",
        "li_design_id": "DAHYlMjSyzE",
        "gmb_design_id": "DAHYlFVopSQ",
        "yt_design_id": "DAHYlLVF4CQ",
        "volanta": "RESPUESTA INMEDIATA",
        "bajada": "PRESENTISMO EN TIEMPO REAL",
        "placa2": "Controlamos el presentismo en tiempo real, y si alguien falta organizamos el reemplazo en el momento para que tu servicio no quede descubierto",
        "placa3": "Cada servicio tiene un supervisor asignado que conoce tu espacio y responde rápido cuando surge una necesidad nueva o un cambio de último momento",
        "cierre_rubro": "Asegurá la continuidad diaria de tu servicio",
        "editorial_feed": "piezas/03_feed_presentismo_biometrico_1080x1350.jpg",
        "copy_ig_fb": (
            "Presentismo en tiempo real y respuesta inmediata para que tu operación esté cubierta todos los días.\n\n"
            "• Monitoreamos el ingreso en cada turno y activamos reemplazos inmediatos con guardia móvil propia.\n"
            "• Cada cuenta tiene un supervisor asignado que conoce tus instalaciones y resuelve necesidades operativas en el día.\n"
            "• Gestión certificada ISO 9001:2015 por TÜV Rheinland.\n\n"
            "📲 Hablá hoy con nuestro equipo comercial: +54 9 11 2275-9369\n"
            "🌐 https://www.starunion.com.ar\n\n"
            "#StarUnion #PresentismoEnTiempoReal #ContinuidadOperativa #EmpresaDeLimpieza #SupervisionActiva #ISO9001"
        ),
        "copy_linkedin": (
            "El principal punto crítico en la contratación de servicios de limpieza B2B es el ausentismo imprevisto.\n\n"
            "En Star Union S.R.L. resolvemos la continuidad diaria mediante:\n"
            "✔️ Control de presentismo en tiempo real desde el inicio de cada turno.\n"
            "✔️ Guardia operativa móvil con flota propia para cubrir ausencias en el acto.\n"
            "✔️ Supervisor asignado a cada cuenta con capacidad de respuesta inmediata ante cambios de agenda o eventos.\n\n"
            "Evaluá nuestro sistema operativo certificado bajo ISO 9001:2015:\n"
            "🌐 https://www.starunion.com.ar | 📲 +54 9 11 2275-9369\n\n"
            "#StarUnion #OperacionesB2B #ContinuidadOperativa #FacilityServices #CalidadCertificada #ISO9001"
        ),
        "yt_title": "Presentismo en Tiempo Real y Respuesta Inmediata — Star Union #Shorts",
    },
    {
        "id": "05",
        "slug": "0611_maquinaria_lista",
        "date_label": "Viernes 06/11 · 10:00 hs (Intercalado con Placa Editorial)",
        "scheduled_at": "2026-11-06T10:00",
        "format_mode": "Intercalado: Placa Editorial en Feed + Reel Canva 12s",
        "ig_design_id": "DAHYlG2Qedg",
        "tt_design_id": "DAHYlGci9ds",
        "fb_design_id": "DAHYlOkCF7A",
        "li_design_id": "DAHYlP0sJss",
        "gmb_design_id": "DAHYlA7E-RM",
        "yt_design_id": "DAHYlHX6ynk",
        "volanta": "MANTENIMIENTO PREVENTIVO",
        "bajada": "MAQUINARIA LISTA",
        "placa2": "Si una máquina falla, la retiramos, la reemplazamos y la reparamos en nuestro taller propio, porque la limpieza de tu planta no puede frenarse por un equipo",
        "placa3": "Tenemos stock permanente de insumos en nuestra base operativa y lo llevamos con flota propia, así cada servicio cuenta con lo que necesita antes de que se termine",
        "cierre_rubro": "Cotizá hoy la limpieza de tu planta o centro logístico",
        "editorial_feed": "piezas/01_feed_logistica_industria_1080x1350.jpg",
        "copy_ig_fb": (
            "Maquinaria lista, taller electromecánico propio y stock permanente de insumos para plantas industriales y centros logísticos.\n\n"
            "• Si un equipo requiere servicio técnico, lo retiramos, lo reemplazamos en el día con flota propia y lo reparamos en nuestro taller de Base Guaminí.\n"
            "• Abastecimiento programado de insumos desde nuestro depósito central antes de que se agote el stock en sitio.\n"
            "• Gestión certificada ISO 9001:2015 por TÜV Rheinland.\n\n"
            "📲 Cotizá el servicio para tu planta: +54 9 11 2275-9369\n"
            "🌐 https://www.starunion.com.ar\n\n"
            "#StarUnion #LimpiezaIndustrial #MaquinariaDeLimpieza #LogisticaB2B #TallerPropio #ISO9001"
        ),
        "copy_linkedin": (
            "La limpieza de una planta industrial o centro logístico depende directamente de la disponibilidad mecánica del equipamiento.\n\n"
            "En Star Union S.R.L. garantizamos continuidad operativa desde nuestra base propia de 800 m² en CABA:\n"
            "✔️ Taller electromecánico in-house para mantenimiento preventivo y reemplazo inmediato de fregadoras, barredoras e hidrolavadoras.\n"
            "✔️ Stock permanente de insumos habilitados y distribución con flota utilitaria propia.\n"
            "✔️ Gestión auditada bajo Norma ISO 9001:2015 por TÜV Rheinland.\n\n"
            "Solicitá una visita técnica en tu planta o depósito:\n"
            "🌐 https://www.starunion.com.ar | 📲 +54 9 11 2275-9369\n\n"
            "#StarUnion #LimpiezaIndustrial #SupplyChain #Logistica #MantenimientoPreventivo #ISO9001"
        ),
        "yt_title": "Maquinaria Lista, Taller Propio y Flota — Star Union #Shorts",
    },
]


def load_canva_token():
    cfg = json.load(open("/Users/arianawajntraub/.gemini/config/canva_oauth.json"))
    return cfg["access_token"]


def mcp_req(method, params):
    tok = load_canva_token()
    req = urllib.request.Request(
        "https://mcp.canva.com/mcp",
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def update_canva_design_texts(design_id, volanta=None, bajada=None, placa2=None, placa3=None, cierre_rubro=None):
    """
    Edita en vivo en Canva la Volanta (Placa 1), Bajada (Placa 1), Cartel Placa 2, Cartel Placa 3 y el Cierre según rubro (Placa 4).
    """
    tx = mcp_req("tools/call", {
        "name": "start-editing-transaction",
        "arguments": {"design_id": design_id, "user_intent": "Update slide headlines and closing CTA by industry"}
    })
    data = json.loads(tx["result"]["content"][0]["text"])
    tid = data["transaction"]["transaction_id"]
    richtexts = data.get("richtexts", [])

    # Group elements by page_index
    by_page = {}
    for rt in richtexts:
        p = rt["page_index"]
        by_page.setdefault(p, []).append(rt)

    pages_set = sorted(list({rt["page_index"] for rt in richtexts}))
    ops_by_page = {}

    # Page 1: smaller height is volanta, larger height is bajada
    p1_items = by_page.get(1, [])
    if len(p1_items) >= 2:
        p1_sorted = sorted(p1_items, key=lambda x: x.get("containerElement", {}).get("dimension", {}).get("height", 0))
        el_volanta = p1_sorted[0]["element_id"]
        el_bajada = p1_sorted[-1]["element_id"]
        if volanta:
            ops_by_page.setdefault(1, []).append({"type": "replace_text", "element_id": el_volanta, "text": volanta})
        if bajada:
            ops_by_page.setdefault(1, []).append({"type": "replace_text", "element_id": el_bajada, "text": bajada})

    # Page 2
    p2_items = [x for x in by_page.get(2, []) if "".join(r.get("text", "") for r in x.get("regions", "")).strip()]
    if p2_items and placa2:
        ops_by_page.setdefault(2, []).append({"type": "replace_text", "element_id": p2_items[0]["element_id"], "text": placa2})

    # Page 3
    p3_items = [x for x in by_page.get(3, []) if "".join(r.get("text", "") for r in x.get("regions", "")).strip()]
    if p3_items and placa3:
        ops_by_page.setdefault(3, []).append({"type": "replace_text", "element_id": p3_items[0]["element_id"], "text": placa3})

    # Page 4: find the CTA element ("Cotizá..." or similar)
    p4_items = by_page.get(4, [])
    if p4_items and cierre_rubro:
        target_el = None
        for x in p4_items:
            t_str = "".join(r.get("text", "") for r in x.get("regions", "")).strip()
            if "Cotiz" in t_str or "Sumá" in t_str or "Asegurá" in t_str or ("Star Union" not in t_str and "ISO" not in t_str and t_str):
                target_el = x["element_id"]
                break
        if target_el:
            ops_by_page.setdefault(4, []).append({"type": "replace_text", "element_id": target_el, "text": cierre_rubro})

    try:
        all_ops = []
        first_p = 1
        for p_idx in sorted(ops_by_page.keys()):
            if ops_by_page[p_idx]:
                if not all_ops:
                    first_p = p_idx
                all_ops.extend(ops_by_page[p_idx])
        if all_ops:
            mcp_req("tools/call", {
                "name": "perform-editing-operations",
                "arguments": {
                    "transaction_id": tid,
                    "page_index": first_p,
                    "operations": all_ops,
                    "user_intent": "Apply text updates across slides 1 to 4"
                }
            })
        mcp_req("tools/call", {
            "name": "commit-editing-transaction",
            "arguments": {"transaction_id": tid, "user_intent": "Commit updated texts to Canva design"}
        })
        return True
    except Exception as e:
        try:
            mcp_req("tools/call", {"name": "cancel-editing-transaction", "arguments": {"transaction_id": tid, "user_intent": "Cancel on error"}})
        except Exception:
            pass
        print("Warn edit:", e)
        return False


def export_canva_pages_jpg(design_id, prefix, target_w, target_h):
    res = mcp_req("tools/call", {
        "name": "export-design",
        "arguments": {
            "design_id": design_id,
            "format": {"type": "png"},
            "user_intent": f"Export {prefix} slides from Canva"
        }
    })
    data = json.loads(res["result"]["content"][0]["text"])
    urls = data.get("job", {}).get("urls", []) or data.get("urls", [])
    saved_jpgs = []
    for idx, u in enumerate(urls, 1):
        png_path = os.path.join(SYNC_DIR, f"{prefix}_p{idx}.png")
        jpg_path = os.path.join(PIEZAS_DIR, f"{prefix}_p{idx}.jpg")
        req_dl = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_dl, timeout=30) as r, open(png_path, "wb") as f:
            f.write(r.read())
        im = Image.open(png_path).convert("RGB")
        if im.size != (target_w, target_h):
            im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        im.save(jpg_path, "JPEG", quality=95)
        saved_jpgs.append(jpg_path)
    return saved_jpgs


def build_12s_reel_from_4_slides(slide_jpgs, out_mp4):
    """
    Arma un Reel/Short/TikTok de 12 segundos exactos (3 segundos por lámina x 4 láminas):
    - Placa 1 (Portada): 3 segundos con leve zoom óptico limpio (sin deformar manos ni caras con IA).
    - Placas 2, 3 y 4: 3 segundos cada una.
    - Audio: `starunion_funk_firma_varon_12s.mp3` (locución masculina 1 sola vez al inicio bien ecualizada + Funk Groove libre de derechos).
    """
    seg_paths = []
    for idx, img_path in enumerate(slide_jpgs[:4], 1):
        seg_mp4 = os.path.join(SYNC_DIR, f"_tmp_seg_{os.path.basename(out_mp4)}_{idx}.mp4")
        if idx == 1:
            # Portada de 3 segundos con movimiento de cámara suave (zoom 1.0 -> 1.06 en 90 frames a 30fps)
            vf = "scale=1080:1920,zoompan=z='min(zoom+0.0007,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1080x1920:fps=30,format=yuv420p"
        else:
            vf = "scale=1080:1920,zoompan=z='1.0':d=90:s=1080x1920:fps=30,format=yuv420p"
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", img_path,
            "-vf", vf,
            "-t", "3",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            seg_mp4
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        seg_paths.append(seg_mp4)

    concat_txt = os.path.join(SYNC_DIR, f"_concat_{os.path.basename(out_mp4)}.txt")
    with open(concat_txt, "w", encoding="utf-8") as cf:
        for sp in seg_paths:
            cf.write(f"file '{sp}'\n")

    cmd_final = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", AUDIO_12S,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        out_mp4
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mp4


def sync_all():
    sched_path = os.path.join(RS_DIR, "calendario_programado.json")
    sched = {}
    if os.path.exists(sched_path):
        try:
            sched = json.load(open(sched_path, "r", encoding="utf-8"))
        except Exception:
            sched = {}

    for item in CANVA_SERIES:
        pid = item["id"]
        slug = item["slug"]
        print(f"==> Procesando #{pid} ({slug}) en Canva...")
        # Actualizamos el cierre según rubro en Canva tanto en IG como en TikTok/Reel
        update_canva_design_texts(
            item["ig_design_id"],
            volanta=item["volanta"],
            bajada=item["bajada"],
            placa2=item["placa2"],
            placa3=item["placa3"],
            cierre_rubro=item["cierre_rubro"],
        )
        update_canva_design_texts(
            item["tt_design_id"],
            volanta=item["volanta"],
            bajada=item["bajada"],
            placa2=item["placa2"],
            placa3=item["placa3"],
            cierre_rubro=item["cierre_rubro"],
        )

        ig_slides = export_canva_pages_jpg(item["ig_design_id"], f"canva_{pid}_{slug}_feed", 1080, 1350)
        tt_slides = export_canva_pages_jpg(item["tt_design_id"], f"canva_{pid}_{slug}_9x16", 1080, 1920)

        reel_out = os.path.join(PIEZAS_DIR, f"canva_{pid}_{slug}_reel_12s_locucion.mp4")
        build_12s_reel_from_4_slides(tt_slides, reel_out)
        print(f"  ✅ Exportado 4 placas Feed + 4 placas 9:16 + Reel 12s con locución: {reel_out}")

        rel_slides_feed = [f"piezas/{os.path.basename(p)}" for p in ig_slides]
        rel_slides_9x16 = [f"piezas/{os.path.basename(p)}" for p in tt_slides]
        rel_reel = f"piezas/{os.path.basename(reel_out)}"

        # Si es intercalado (03 o 05), dejamos opción de Placa Editorial o Carrusel Canva
        sched[pid] = {
            "id": pid,
            "slug": slug,
            "date_label": item["date_label"],
            "scheduled_at": item["scheduled_at"],
            "status": "pausado_en_revision",
            "format_mode": item["format_mode"],
            "ig_design_id": item["ig_design_id"],
            "tt_design_id": item["tt_design_id"],
            "fb_design_id": item["fb_design_id"],
            "li_design_id": item["li_design_id"],
            "gmb_design_id": item["gmb_design_id"],
            "yt_design_id": item["yt_design_id"],
            "volanta": item["volanta"],
            "bajada": item["bajada"],
            "placa2": item["placa2"],
            "placa3": item["placa3"],
            "cierre_rubro": item["cierre_rubro"],
            "tag": item["volanta"],
            "title": item["bajada"].replace("\n", " "),
            "subtitle": item["placa2"],
            "feed_file": rel_slides_feed[0],
            "carousel_files": rel_slides_feed,
            "editorial_feed_file": item["editorial_feed"],
            "story_file": rel_slides_9x16[0],
            "story_slides": rel_slides_9x16,
            "reel_file": rel_reel,
            "copy_ig_fb": item["copy_ig_fb"],
            "copy_linkedin": item["copy_linkedin"],
            "yt_title": item["yt_title"],
            "yt_desc": item["copy_ig_fb"],
            "yt_tags": "star union, empresa de limpieza, limpieza industrial, limpieza clinicas, iso 9001",
            "copy_wa": f"*{item['volanta']} — {item['bajada'].replace(chr(10), ' ')}*\n{item['placa2']}\n📲 Cotizá hoy: https://wa.me/5491122759369\n🌐 https://www.starunion.com.ar",
            "channels": ["ig_feed", "ig_story", "ig_reel", "fb_page", "fb_reel", "linkedin", "gmb", "youtube", "tiktok"],
        }

    with open(sched_path, "w", encoding="utf-8") as f:
        json.dump(sched, f, ensure_ascii=False, indent=2)
    print("✅ calendario_programado.json actualizado con las 5 piezas de Canva + Reels 12s.")


if __name__ == "__main__":
    sync_all()
