#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
import base64
from generar_pack_redes import POSTS, OUT_DIR, PIEZAS_DIR, BASE_DIR

# Add chronological dates & rationale to each post
CALENDAR_META = [
    {
        "date": "Jueves 29 Oct 2026",
        "channels": "IG Feed + FB + LinkedIn + Estado WA + Short #1",
        "reason": "Acompaña en caliente los 179 clics a WhatsApp del Mailing de Octubre (#116/#119) donde el bloque #1 más clickeado (197 clics) fue Centros Logísticos y Plantas Industriales."
    },
    {
        "date": "Lunes 02 Nov 2026",
        "channels": "LinkedIn + IG Feed + FB + Story",
        "reason": "Abre noviembre mostrando el diferenciador físico duro (Base Propia de 800 m² en Guaminí 5657 y Taller Electromecánico In-House) para decisores técnicos que están evaluando recambio de proveedor."
    },
    {
        "date": "Miércoles 04 Nov 2026",
        "channels": "IG Feed + FB + LinkedIn + Estado WA",
        "reason": "Mitad de semana: ataca el dolor #1 de Administraciones y Gerencias (el ausentismo) con 'El Dato Técnico de Cleany' (Reloj Biométrico con alerta a los 15 min y cobertura < 2 hs)."
    },
    {
        "date": "Viernes 06 Nov 2026",
        "channels": "LinkedIn + IG Feed + FB + Short #2",
        "reason": "Cierre de semana enfocado en el vertical regulado (Clínicas, Sanatorios y Laboratorios con insumos ANMAT + ISO 9001:2015 TÜV Rheinland), preparando el terreno antes del 1° Envío Perfit de Noviembre."
    },
    {
        "date": "Martes 10 Nov 2026",
        "channels": "IG Feed + FB + LinkedIn + Estado WA",
        "reason": "Pre-temporada de licitaciones educativas y deportivas (Universidades, Colegios y Clubes para receso de verano y colonia), conectando con el 1° Envío de Perfit de Noviembre (Jueves 19/11)."
    }
]

def img_to_data_uri(rel_path):
    abs_path = os.path.normpath(os.path.join(PIEZAS_DIR, rel_path))
    if not os.path.exists(abs_path):
        return ""
    ext = os.path.splitext(abs_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    with open(abs_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/{ext};base64,{b64}"

def wrap_lines(text, max_chars):
    words = text.split()
    lines, cur = [], []
    for w in words:
        if sum(len(x) for x in cur) + len(cur) + len(w) <= max_chars:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines

def create_editable_svg(post, width, height, out_svg):
    logo_uri = img_to_data_uri("../../assets/img/logo-star-union.png")
    tuv_uri = img_to_data_uri("../../assets/img/tuv-iso-9001-badge.png")
    photo_uri = img_to_data_uri(post["photo"])

    is_story = (height == 1920)
    left_x = 76 if is_story else 72
    right_margin = 140 if is_story else 72
    content_w = width - left_x - right_margin
    top_y = 250 if is_story else 145
    bottom_margin = 420 if is_story else 145

    title_lines = wrap_lines(post["title"], 32 if is_story else 34)
    sub_lines = wrap_lines(post["subtitle"], 52 if is_story else 56)

    title_tspans = "".join([
        f'<tspan x="{left_x}" dy="{0 if i==0 else 44}">{line}</tspan>'
        for i, line in enumerate(title_lines)
    ])
    sub_tspans = "".join([
        f'<tspan x="{left_x}" dy="{0 if i==0 else 28}">{line}</tspan>'
        for i, line in enumerate(sub_lines)
    ])

    photo_y = top_y + 390
    photo_h = 460 if is_story else 450
    footer_y = height - bottom_margin - 55

    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <!-- FONDO BLANCO EDITABLE -->
  <rect id="Fondo_Blanco" x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>

  <!-- LOGO Y SELLO ISO (DENTRO DE ZONA SEGURA) -->
  <image id="Logo_Star_Union" x="{left_x}" y="{top_y}" width="210" height="62" preserveAspectRatio="xMinYMid meet" href="{logo_uri}"/>
  <g id="Sello_ISO_9001">
    <rect x="{left_x + content_w - 300}" y="{top_y}" width="300" height="66" rx="12" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="2"/>
    <image x="{left_x + content_w - 286}" y="{top_y + 11}" width="52" height="44" preserveAspectRatio="xMidYMid meet" href="{tuv_uri}"/>
    <text x="{left_x + content_w - 222}" y="{top_y + 29}" font-family="Open Sans, Arial, sans-serif" font-size="14" font-weight="800" fill="#03582D">ISO 9001:2015</text>
    <text x="{left_x + content_w - 222}" y="{top_y + 47}" font-family="Open Sans, Arial, sans-serif" font-size="12" font-weight="600" fill="#4B5563">TÜV Rheinland · ID 9000041847</text>
  </g>
  <line x1="{left_x}" y1="{top_y + 78}" x2="{left_x + content_w}" y2="{top_y + 78}" stroke="#03582D" stroke-width="4"/>

  <!-- ETIQUETA SUPERIOR EDITABLE -->
  <g id="Etiqueta_Rubro">
    <rect x="{left_x}" y="{top_y + 96}" width="440" height="36" rx="18" fill="#E6EFEA"/>
    <text x="{left_x + 18}" y="{top_y + 120}" font-family="Open Sans, Arial, sans-serif" font-size="14" font-weight="800" fill="#03582D">{post["tag"]}</text>
  </g>

  <!-- TITULAR PRINCIPAL EDITABLE -->
  <text id="Titular_Editable" x="{left_x}" y="{top_y + 178}" font-family="Open Sans, Arial, sans-serif" font-size="38" font-weight="800" fill="#111827">
    {title_tspans}
  </text>

  <!-- BAJADA EDITABLE -->
  <text id="Bajada_Editable" x="{left_x}" y="{top_y + 305}" font-family="Open Sans, Arial, sans-serif" font-size="20" font-weight="600" fill="#374151">
    {sub_tspans}
  </text>

  <!-- FOTOGRAFÍA REAL ENMARCADA DENTRO DE ZONA SEGURA -->
  <clipPath id="clip_foto_{post['id']}_{height}">
    <rect x="{left_x}" y="{photo_y}" width="{content_w}" height="{photo_h}" rx="22"/>
  </clipPath>
  <image id="Fotografia_Operativa" x="{left_x}" y="{photo_y}" width="{content_w}" height="{photo_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip_foto_{post['id']}_{height})" href="{photo_uri}"/>
  <rect x="{left_x}" y="{photo_y}" width="{content_w}" height="{photo_h}" rx="22" fill="none" stroke="#03582D" stroke-width="3"/>

  <!-- PIE DE CONTACTO Y BOTÓN CTA EDITABLE DENTRO DE ZONA SEGURA -->
  <g id="Pie_Institucional">
    <line x1="{left_x}" y1="{footer_y - 16}" x2="{left_x + content_w}" y2="{footer_y - 16}" stroke="#E5E7EB" stroke-width="2"/>
    <text x="{left_x}" y="{footer_y + 14}" font-family="Open Sans, Arial, sans-serif" font-size="16" font-weight="800" fill="#111827">Star Union S.R.L. · Base Operativa Guaminí 5657, CABA</text>
    <text x="{left_x}" y="{footer_y + 36}" font-family="Open Sans, Arial, sans-serif" font-size="14" font-weight="600" fill="#4B5563">WhatsApp Comercial B2B: +54 9 11 2275-9369 · 0810-333-8646</text>
    <rect x="{left_x + content_w - 280}" y="{footer_y - 4}" width="280" height="46" rx="23" fill="#03582D"/>
    <text x="{left_x + content_w - 140}" y="{footer_y + 25}" text-anchor="middle" font-family="Open Sans, Arial, sans-serif" font-size="15" font-weight="800" fill="#FFFFFF">{post["cta_pill"]}</text>
  </g>
</svg>"""
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_content)

def main():
    # 1. Generate Editable SVGs + Bulk CSV for Canva / Adobe Express / Illustrator
    csv_path = os.path.join(PIEZAS_DIR, "STAR_UNION_CANVA_ADOBE_BULK.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as cf:
        writer = csv.writer(cf)
        writer.writerow([
            "Orden", "Fecha_Programada", "Canales", "Etiqueta_Superior", "Titular_Editable",
            "Bajada_Editable", "KPI_1", "KPI_2", "KPI_3", "URL_CTA",
            "Copy_IG_FB", "Copy_LinkedIn", "YouTube_Short_Titulo", "YouTube_Short_Descripcion", "YouTube_Short_Tags", "Copy_Estado_WhatsApp"
        ])
        for i, p in enumerate(POSTS):
            meta = CALENDAR_META[i]
            p["date"] = meta["date"]
            p["channels"] = meta["channels"]
            p["reason"] = meta["reason"]

            svg_feed = os.path.join(PIEZAS_DIR, f"{p['id']}_feed_{p['slug']}_EDITABLE.svg")
            svg_story = os.path.join(PIEZAS_DIR, f"{p['id']}_story_{p['slug']}_EDITABLE.svg")
            create_editable_svg(p, 1080, 1350, svg_feed)
            create_editable_svg(p, 1080, 1920, svg_story)
            p["svg_feed_file"] = f"piezas/{p['id']}_feed_{p['slug']}_EDITABLE.svg"
            p["svg_story_file"] = f"piezas/{p['id']}_story_{p['slug']}_EDITABLE.svg"
            p["feed_file"] = f"piezas/{p['id']}_feed_{p['slug']}_1080x1350.jpg"
            p["story_file"] = f"piezas/{p['id']}_story_{p['slug']}_1080x1920.jpg"

            writer.writerow([
                p["id"], p["date"], p["channels"], p["tag"], p["title"],
                p["subtitle"], p["kpis"][0], p["kpis"][1], p["kpis"][2], p["cta_pill"],
                p["copy_ig_fb"], p["copy_linkedin"], p["yt_title"], p["yt_desc"], p["yt_tags"], p["copy_wa"]
            ])

    # 2. Build Calendar rows
    cal_rows = ""
    for p in POSTS:
        cal_rows += f"""
        <tr class="hover:bg-gray-50">
          <td class="p-3 font-extrabold text-[#03582d] whitespace-nowrap">{p['date']}</td>
          <td class="p-3 font-bold text-gray-900">#{p['id']} · {p['title']}</td>
          <td class="p-3 text-gray-700 font-semibold">{p['channels']}</td>
          <td class="p-3 text-gray-600">{p['reason']}</td>
          <td class="p-3 text-center whitespace-nowrap">
            <a href="#post-{p['id']}" class="bg-[#03582d] text-white text-[11px] font-extrabold px-3 py-1.5 rounded-lg">Ir a Pieza #{p['id']} ↓</a>
          </td>
        </tr>
        """

    # Add the Perfit November Milestones to the same chronological calendar so she sees the full picture
    cal_rows += """
        <tr class="bg-[#03582d]/5 border-t-2 border-[#03582d]/20">
          <td class="p-3 font-extrabold text-[#03582d] whitespace-nowrap">Jueves 19 Nov 2026</td>
          <td class="p-3 font-extrabold text-gray-900">📧 PERFIT NOVIEMBRE (1° Envío Mensual · 10:00 hs)</td>
          <td class="p-3 text-gray-700 font-bold">Mailing Perfit (Lista Fidelizada + Lista Depurada)</td>
          <td class="p-3 text-gray-700">Cierra el ciclo iniciado en redes: Bloque #1 Logística/Industria + Bloque #2 Inicio Licitaciones Verano (Clubes/Universidades) + Dato Técnico de Cleany aterrizando en las nuevas landings web.</td>
          <td class="p-3 text-center whitespace-nowrap">
            <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#111827] text-white text-[11px] font-extrabold px-3 py-1.5 rounded-lg">Ver Plan Perfit →</a>
          </td>
        </tr>
        <tr class="bg-[#03582d]/5">
          <td class="p-3 font-extrabold text-[#03582d] whitespace-nowrap">Martes 24 Nov 2026</td>
          <td class="p-3 font-extrabold text-gray-900">📧 PERFIT NOVIEMBRE (2° Envío +5 días a No-Abridores con Asunto Nuevo)</td>
          <td class="p-3 text-gray-700 font-bold">Mailing Perfit (Segmento Activos No-Abridores)</td>
          <td class="p-3 text-gray-700">Aplica la regla comprobada de Septiembre (#117): cambio de asunto obligatorio para sumar +21,8% de aperturas extra y duplicar los clics hacia WhatsApp Comercial.</td>
          <td class="p-3 text-center whitespace-nowrap">
            <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#111827] text-white text-[11px] font-extrabold px-3 py-1.5 rounded-lg">Ver Plan Perfit →</a>
          </td>
        </tr>
    """

    cards_html = ""
    for p in POSTS:
        cards_html += f"""
        <div id="post-{p['id']}" class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex flex-wrap items-center justify-between gap-3">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-0.5 rounded-full">📅 {p['date']}</span>
                <span class="text-xs font-extrabold uppercase tracking-wider text-[#03582d]">{p['day_label']}</span>
              </div>
              <h2 class="text-lg font-extrabold text-gray-900 mt-1">{p['title']}</h2>
              <p class="text-xs text-gray-600 mt-0.5"><strong>Sentido cronológico:</strong> {p['reason']}</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <a href="{p['feed_file']}" download class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-3.5 py-2 rounded-lg transition">
                ⬇ JPG Feed (1080×1350)
              </a>
              <a href="{p['story_file']}" download class="bg-[#111827] hover:bg-black text-white text-xs font-extrabold px-3.5 py-2 rounded-lg transition">
                ⬇ JPG Story/WA (1080×1920)
              </a>
              <a href="{p['svg_feed_file']}" download class="bg-white border-2 border-[#03582d] text-[#03582d] hover:bg-[#03582d]/5 text-xs font-extrabold px-3.5 py-2 rounded-lg transition">
                ✏️ SVG Editable Feed (Canva / Illustrator / Adobe)
              </a>
              <a href="{p['svg_story_file']}" download class="bg-white border-2 border-gray-800 text-gray-900 hover:bg-gray-100 text-xs font-extrabold px-3.5 py-2 rounded-lg transition">
                ✏️ SVG Editable Story (Canva / Illustrator / Adobe)
              </a>
            </div>
          </div>

          <div class="p-6 grid lg:grid-cols-12 gap-6 items-start">
            <div class="lg:col-span-5 grid grid-cols-2 gap-4">
              <div>
                <div class="text-xs font-bold text-gray-500 mb-2">Feed IG / FB / LinkedIn (1080×1350)</div>
                <a href="{p['feed_file']}" target="_blank">
                  <img src="{p['feed_file']}" class="w-full rounded-xl border border-gray-200 shadow-sm hover:opacity-95 transition" alt="Feed">
                </a>
              </div>
              <div>
                <div class="text-xs font-bold text-gray-500 mb-2">Story IG/FB + Estado WhatsApp (1080×1920)</div>
                <a href="{p['story_file']}" target="_blank">
                  <img src="{p['story_file']}" class="w-full rounded-xl border border-gray-200 shadow-sm hover:opacity-95 transition" alt="Story">
                </a>
              </div>
            </div>

            <div class="lg:col-span-7 space-y-4">
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-extrabold uppercase text-[#03582d]">📸 Copy Instagram y Facebook</span>
                  <button onclick="copyText('ig_{p['id']}', this)" class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1.5 rounded-lg">📋 Copiar Copy IG/FB</button>
                </div>
                <pre id="ig_{p['id']}" class="text-xs text-gray-800 whitespace-pre-wrap font-sans leading-relaxed">{p['copy_ig_fb']}</pre>
              </div>

              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-extrabold uppercase text-gray-900">💼 Copy LinkedIn B2B</span>
                  <button onclick="copyText('li_{p['id']}', this)" class="bg-[#111827] text-white text-xs font-extrabold px-3 py-1.5 rounded-lg">📋 Copiar Copy LinkedIn</button>
                </div>
                <pre id="li_{p['id']}" class="text-xs text-gray-800 whitespace-pre-wrap font-sans leading-relaxed">{p['copy_linkedin']}</pre>
              </div>

              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200 space-y-2">
                <div class="text-xs font-extrabold uppercase text-[#03582d]">▶️ Pack YouTube Shorts (Título + Descripción + Etiquetas)</div>
                <div class="flex items-center justify-between gap-2 bg-white p-2.5 rounded-lg border border-gray-200">
                  <div class="text-xs"><strong class="text-gray-600">Título:</strong> <span id="ytt_{p['id']}" class="font-bold text-gray-900">{p['yt_title']}</span></div>
                  <button onclick="copyText('ytt_{p['id']}', this)" class="bg-gray-200 hover:bg-gray-300 text-gray-900 text-[11px] font-bold px-2.5 py-1 rounded">📋 Copiar Título</button>
                </div>
                <div class="bg-white p-2.5 rounded-lg border border-gray-200">
                  <div class="flex items-center justify-between mb-1">
                    <strong class="text-xs text-gray-600">Descripción:</strong>
                    <button onclick="copyText('ytd_{p['id']}', this)" class="bg-gray-200 hover:bg-gray-300 text-gray-900 text-[11px] font-bold px-2.5 py-1 rounded">📋 Copiar Descripción</button>
                  </div>
                  <pre id="ytd_{p['id']}" class="text-xs text-gray-800 whitespace-pre-wrap font-sans">{p['yt_desc']}</pre>
                </div>
                <div class="flex items-center justify-between gap-2 bg-white p-2.5 rounded-lg border border-gray-200">
                  <div class="text-xs"><strong class="text-gray-600">Tags:</strong> <span id="yttags_{p['id']}" class="text-gray-800">{p['yt_tags']}</span></div>
                  <button onclick="copyText('yttags_{p['id']}', this)" class="bg-gray-200 hover:bg-gray-300 text-gray-900 text-[11px] font-bold px-2.5 py-1 rounded shrink-0">📋 Copiar Tags</button>
                </div>
              </div>

              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200 flex items-center justify-between gap-3">
                <div class="text-xs text-gray-800"><strong class="text-[#03582d] uppercase block mb-0.5">📲 Pie para Estado de WhatsApp:</strong><span id="wa_{p['id']}">{p['copy_wa']}</span></div>
                <button onclick="copyText('wa_{p['id']}', this)" class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1.5 rounded-lg shrink-0">📋 Copiar Texto WA</button>
              </div>

              <!-- BARRA DE APROBACIÓN HUMANA Y DISPARO DIRECTO POR API -->
              <div class="bg-emerald-50/90 border-2 border-[#03582d] rounded-xl p-4 space-y-3">
                <div class="text-xs font-extrabold uppercase text-[#03582d]">🚀 Aprobación Humana y Disparo Directo por API (Marcá en qué redes publicar esta pieza):</div>
                <div class="flex flex-wrap gap-3 text-xs font-bold text-gray-900">
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_ig_feed_{p['id']}" checked> 📸 IG Feed (4:5)</label>
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_ig_story_{p['id']}" checked> 📱 IG Story (9:16)</label>
                  <label class="flex items-center gap-1.5 bg-amber-50 px-2.5 py-1.5 rounded-lg border border-amber-400"><input type="checkbox" id="chk_ig_reel_{p['id']}" checked> 🎬 IG Reel MP4 (Voz Varón + Funk)</label>
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_fb_{p['id']}" checked> 👍 Facebook Page</label>
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_li_{p['id']}" checked> 💼 LinkedIn Empresa</label>
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_gmb_{p['id']}" checked> 📍 Google My Business</label>
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_yt_{p['id']}" checked> ▶️ YouTube Shorts</label>
                  <label class="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded-lg border border-gray-300"><input type="checkbox" id="chk_tt_{p['id']}"> 🎵 TikTok</label>
                </div>
                <button type="button" onclick="publishPostViaApi('{p['id']}', '{p['feed_file']}', '{p['story_file']}', 'piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4', this)" class="w-full bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-3 px-4 rounded-xl transition shadow-sm">
                  🚀 APROBAR Y PUBLICAR AHORA POR API EN LAS REDES MARCADAS (PIEZA #{p['id']})
                </button>
                <div id="api_res_{p['id']}" class="text-xs font-semibold text-gray-800 hidden bg-white p-3 rounded-lg border border-gray-200"></div>
              </div>
            </div>
          </div>
        </div>
        """

    hub_html = f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Calendario + Pack Editable de Redes Sociales y Shorts | Star Union S.R.L.</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Open Sans', sans-serif; background: #f9fafb; color: #111827; }}
  </style>
</head>
<body class="py-8 px-4 sm:px-6">
  <div class="max-w-7xl mx-auto space-y-8">
    <!-- HEADER -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 border-t-4 border-t-[#03582d] shadow-sm flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <img src="../assets/img/logo-star-union.png" alt="Star Union" class="h-12 w-auto object-contain">
        <div>
          <span class="inline-block bg-[#03582d]/10 text-[#03582d] text-[11px] font-extrabold uppercase tracking-wider px-3 py-0.5 rounded-full mb-1">
            Calendario Cronológico + 10 JPG + 10 SVG Editables (Canva / Illustrator / Adobe) + CSV Lote + 2 MP4
          </span>
          <h1 class="text-xl sm:text-2xl font-extrabold text-gray-900">Planilla Cronológica y Pack Editable de Redes — Star Union S.R.L.</h1>
          <p class="text-xs text-gray-600 mt-0.5">Todo queda guardado en tu disco y con archivos .SVG por capas + .CSV para abrir y editar textos/fotos en Canva, Adobe Express o Illustrator cuando quieras.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2">
        <button type="button" onclick="toggleApiBox()" class="bg-amber-500 hover:bg-amber-600 text-gray-950 text-xs font-extrabold px-4 py-2.5 rounded-lg transition shadow-sm">
          🔌 Conectar / Ver Estado de las 6 Redes (API Directa)
        </button>
        <a href="piezas/STAR_UNION_CANVA_ADOBE_BULK.csv" download class="bg-[#111827] hover:bg-black text-white text-xs font-extrabold px-4 py-2.5 rounded-lg transition">
          📥 Descargar Planilla .CSV (Canva Bulk / Excel)
        </a>
        <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2.5 rounded-lg transition">
          📊 Ver Informe Perfit (El mismo del Chat SU)
        </a>
      </div>
    </div>

    <!-- CABINA DE CONEXIÓN DIRECTA DE LAS 6 REDES DE STAR UNION ($0 · CERO MAKE · CERO ZAPIER) -->
    <div class="bg-[#111827] text-white rounded-2xl p-6 sm:p-8 border-2 border-[#03582d] shadow-md space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <span class="inline-block bg-[#03582d] text-white text-[11px] font-extrabold uppercase px-3 py-0.5 rounded-full mb-1">
            🔌 CONEXIÓN DIRECTA POR API OFICIAL · BÓVEDA AISLADA STAR UNION (.agents/vault/social_keys.json)
          </span>
          <h2 class="text-lg sm:text-xl font-extrabold text-white">Conectá las 6 Redes de Star Union una sola vez y publicá en 1 clic</h2>
          <div id="api-status-line" class="text-xs text-gray-300 mt-1">Verificando estado de conexión con el servidor API local (`127.0.0.1:8894`)...</div>
        </div>
        <button type="button" onclick="toggleApiBox()" class="bg-white/10 hover:bg-white/20 text-white text-xs font-extrabold px-4 py-2 rounded-lg border border-white/20 transition">
          ⚙️ Mostrar / Ocultar Llaves de API
        </button>
      </div>

      <div id="api-config-box" class="grid md:grid-cols-2 lg:grid-cols-3 gap-4 pt-4 border-t border-white/15 text-xs">
        <!-- 1. META: FACEBOOK + INSTAGRAM -->
        <div class="bg-white/5 border border-white/15 rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div class="space-y-1.5">
            <div class="font-extrabold text-amber-400 text-sm">1. Facebook Page + Instagram (@starunionservicios)</div>
            <p class="text-gray-300 leading-relaxed">
              1) Abrí <a href="https://developers.facebook.com/tools/explorer/" target="_blank" class="text-amber-300 underline font-bold">Meta Graph API Explorer ↗</a><br>
              2) Elegí tu App y marcá permisos: <code>pages_show_list</code>, <code>pages_read_engagement</code>, <code>pages_manage_posts</code>, <code>instagram_basic</code>, <code>instagram_content_publish</code>.<br>
              3) Tocá <strong>Generate Access Token</strong>, seleccioná la Fan Page de <strong>Star Union</strong> y pegalo acá (detecta FB + IG juntos):
            </p>
          </div>
          <div class="space-y-2 pt-2">
            <div id="status-box-meta" class="bg-emerald-900/80 border border-emerald-400 text-emerald-200 font-extrabold p-2.5 rounded-lg text-xs">
              ✅ CONECTADO: FB "Star Union Servicios" + IG @starunionservicios
            </div>
            <input id="inp-meta-token" type="password" placeholder="Pegar nuevo Access Token si querés renovar (EAA...)" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <button id="btn-connect-meta" type="button" onclick="saveApiTokens(this)" class="w-full bg-[#03582d] hover:bg-[#133522] text-white font-extrabold py-2 px-3 rounded-lg transition">✅ Facebook + Instagram Conectados (Tocar para actualizar)</button>
          </div>
        </div>

        <!-- 2. LINKEDIN PÁGINA DE EMPRESA -->
        <div class="bg-white/5 border border-white/15 rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div class="space-y-1.5">
            <div class="font-extrabold text-amber-400 text-sm">2. LinkedIn Página Empresa (Candado Anti-Perfil Personal)</div>
            <p class="text-gray-300 leading-relaxed">
              1) Abrí <a href="https://www.linkedin.com/developers/tools/oauth/token-generator" target="_blank" class="text-amber-300 underline font-bold">LinkedIn OAuth Token Generator ↗</a><br>
              2) Marcá permisos de organización: <code>w_organization_social</code> y <code>r_organization_social</code>.<br>
              3) Pegá el Token y el ID numérico de la Página de Empresa Star Union (el sistema bloquea por seguridad cualquier intento de publicar en tu perfil personal):
            </p>
          </div>
          <div class="space-y-2 pt-2">
            <input id="inp-li-token" type="password" placeholder="Access Token de LinkedIn (AQV...)" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <input id="inp-li-urn" type="text" placeholder="ID o URN Página Empresa (ej. urn:li:organization:123456)" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <button type="button" onclick="saveApiTokens(this)" class="w-full bg-[#03582d] hover:bg-[#133522] text-white font-extrabold py-2 px-3 rounded-lg transition">🔌 Conectar LinkedIn Empresa</button>
          </div>
        </div>

        <!-- 3. GOOGLE MY BUSINESS (GOOGLE MAPS GUAMINÍ 5657) -->
        <div class="bg-white/5 border border-white/15 rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div class="space-y-1.5">
            <div class="font-extrabold text-amber-400 text-sm">3. Google My Business (Ficha Maps Guaminí 5657)</div>
            <p class="text-gray-300 leading-relaxed">
              1) Abrí <a href="https://developers.google.com/oauthplayground/" target="_blank" class="text-amber-300 underline font-bold">Google OAuth Playground ↗</a><br>
              2) En Step 1 pegá el permiso: <code>https://www.googleapis.com/auth/business.manage</code> y tocá <strong>Authorize APIs</strong>.<br>
              3) En Step 2 tocá <strong>Exchange authorization code</strong> y pegá acá <strong>SOLO el Token</strong> (el sistema ya detectó solo el ID de ubicación):
            </p>
          </div>
          <div class="space-y-2 pt-2">
            <div id="status-box-gmb" class="bg-emerald-900/80 border border-emerald-400 text-emerald-200 font-extrabold p-2.5 rounded-lg text-xs">
              ✅ CONECTADO: Empresa de Limpieza - Star Union (locations/8938663810475756647)
            </div>
            <input id="inp-gmb-token" type="password" placeholder="Pegar nuevo Token Google Business si querés renovar (ya29...)" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <button type="button" onclick="saveApiTokens(this)" class="w-full bg-[#03582d] hover:bg-[#133522] text-white font-extrabold py-2 px-3 rounded-lg transition">✅ Google Maps Conectado (Tocar para actualizar)</button>
          </div>
        </div>

        <!-- 4. YOUTUBE SHORTS (@starunionservicios) -->
        <div class="bg-white/5 border border-white/15 rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div class="space-y-1.5">
            <div class="font-extrabold text-amber-400 text-sm">4. YouTube Shorts (@starunionservicios · API v3)</div>
            <p class="text-gray-300 leading-relaxed">
              1) Abrí <a href="https://developers.google.com/oauthplayground/" target="_blank" class="text-amber-300 underline font-bold">Google OAuth Playground ↗</a><br>
              2) En Step 1 elegí <strong>YouTube Data API v3</strong> → marcá <code>https://www.googleapis.com/auth/youtube.upload</code> y <code>https://www.googleapis.com/auth/youtube.readonly</code>.<br>
              3) Elegí el canal <strong>@starunionservicios</strong>, tocá <strong>Exchange authorization code</strong> y pegá el <code>Access token</code>:
            </p>
          </div>
          <div class="space-y-2 pt-2">
            <div id="status-box-yt" class="bg-emerald-900/80 border border-emerald-400 text-emerald-200 font-extrabold p-2.5 rounded-lg text-xs">
              ✅ CONECTADO: Star Union | Limpieza Profesional e Industrial (@starunionservicios)
            </div>
            <input id="inp-yt-token" type="password" placeholder="Pegar nuevo Token YouTube si querés renovar (ya29...)" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <button type="button" onclick="saveApiTokens(this)" class="w-full bg-[#03582d] hover:bg-[#133522] text-white font-extrabold py-2 px-3 rounded-lg transition">✅ YouTube Shorts Conectado (Tocar para actualizar)</button>
          </div>
        </div>

        <!-- 5. TIKTOK BUSINESS -->
        <div class="bg-white/5 border border-white/15 rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div class="space-y-1.5">
            <div class="font-extrabold text-amber-400 text-sm">5. TikTok Business (Content Posting API v2)</div>
            <p class="text-gray-300 leading-relaxed">
              1) En <a href="https://developers.tiktok.com/" target="_blank" class="text-amber-300 underline font-bold">TikTok for Developers ↗</a> (modo <strong>Sandbox</strong> o <strong>Production</strong>), copiá arriba el <code>Client Key</code> y <code>Client Secret</code>.<br>
              2) En <strong>Login Kit → Redirect URI</strong> poné: <code>https://wajntraub.ar/staruniontest/redes-sociales/tiktok-callback.html</code><br>
              3) <a href="assets/starunion_tiktok_icon_1024.png" download class="text-emerald-300 underline font-bold">⬇ Bajar Ícono 1024×1024 PNG de Star Union</a> (para subir en App Icon):
            </p>
          </div>
          <div class="space-y-2 pt-2">
            <input id="inp-tt-ck" type="text" placeholder="Pegar Client key de TikTok" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <input id="inp-tt-cs" type="password" placeholder="Pegar Client secret de TikTok" class="w-full px-3 py-2 rounded-lg bg-gray-950 border border-gray-700 text-white text-xs">
            <button type="button" onclick="connectTikTokOAuth()" class="w-full bg-amber-500 hover:bg-amber-600 text-gray-950 font-extrabold py-2 px-3 rounded-lg transition">🔗 1 Clic: Conectar TikTok con Client Key y Secret</button>
          </div>
        </div>

        <!-- 6. ESTADO Y AUTO-DETECCIÓN -->
        <div class="bg-emerald-950/60 border border-[#03582d] rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div class="space-y-1.5">
            <div class="font-extrabold text-emerald-300 text-sm">🔒 Seguridad y Aislamiento Zero-Trust</div>
            <p class="text-gray-300 leading-relaxed">
              • Todas las llaves quedan guardadas solo en tu Mac dentro de <code>star-union/.agents/vault/social_keys.json</code> (jamás se suben a GitHub).<br>
              • Perfit ya está conectado y activo en esa misma bóveda.<br>
              • Podés conectar primero Meta (FB + IG) y YouTube, y sumar las demás cuando quieras.
            </p>
          </div>
          <div id="api-connect-log" class="text-xs font-bold text-amber-300 bg-black/40 p-2.5 rounded-lg min-h-[42px] flex items-center">
            Esperando pegado de tokens...
          </div>
        </div>
      </div>
    </div>

    <!-- 0. 3 BASES MAESTRAS EDITABLES EN CANVA (CON MÁRGENES DE SEGURIDAD REALES + 5 PÁGINAS CON FOTO REAL POR ARCHIVO) -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border-2 border-[#03582d] shadow-sm space-y-4">
      <div>
        <span class="text-xs font-extrabold uppercase text-[#03582d]">★ 3 BASES MAESTRAS EDITABLES EN CANVA (CON FOTOS REALES INCLUIDAS + MÁRGENES DE SEGURIDAD + 5 PÁGINAS POR ARCHIVO)</span>
        <h2 class="text-lg sm:text-xl font-extrabold text-gray-900 mt-1">Subí estas 3 bases a Canva una sola vez, sumales la música de la marca y duplicalas siempre</h2>
        <p class="text-xs text-gray-600 mt-1">Cada archivo <strong>.PPTX</strong> o <strong>.PDF</strong> contiene las 5 publicaciones adentro con sus <strong>fotografías reales de Star Union ya colocadas</strong>, textos 100% editables en Canva (fuente Open Sans) y márgenes de seguridad reales (grilla 1:1 de perfil y botonera derecha de Reels/Shorts despejadas).</p>
      </div>
      <div class="grid md:grid-cols-3 gap-4">
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-3">
          <div class="text-xs font-extrabold text-[#03582d] uppercase">1. Base Reel / Short / Story (1080×1920)</div>
          <p class="text-[11px] text-gray-600">Margen seguro: <strong>250px arriba</strong>, <strong>420px abajo</strong> (copy y música) y <strong>140px a la derecha</strong> (botonera ❤️💬✈️ de Reels).</p>
          <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_1_REEL_SHORT_1080x1920.jpg" target="_blank">
            <img src="piezas/3_BASES_MAESTRAS_CANVA/BASE_1_REEL_SHORT_1080x1920.jpg" class="w-full h-56 object-contain bg-white rounded-lg border border-gray-200" alt="Base 1">
          </a>
          <div class="flex flex-col gap-2">
            <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_1_REEL_SHORT_1080x1920_EDITABLE_CANVA.pptx" download class="bg-[#03582d] text-white text-center text-xs font-extrabold py-2 px-3 rounded-lg">✏️ Bajar Base 1 Editable (.PPTX con Fotos para Canva)</a>
            <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_1_REEL_SHORT_1080x1920_EDITABLE_CANVA.pdf" download class="bg-gray-900 text-white text-center text-xs font-extrabold py-2 px-3 rounded-lg">📄 Bajar Base 1 Editable (.PDF para Canva/Illustrator)</a>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-3">
          <div class="text-xs font-extrabold text-[#03582d] uppercase">2. Base Facebook / IG Feed (1080×1350)</div>
          <p class="text-[11px] text-gray-600">Margen seguro aplicado: <strong>145px arriba y 145px abajo</strong> para que la <strong>grilla cuadrada 1:1 del perfil de IG</strong> jamás corte el logo ni el pie.</p>
          <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_2_FACEBOOK_IG_FEED_1080x1350.jpg" target="_blank">
            <img src="piezas/3_BASES_MAESTRAS_CANVA/BASE_2_FACEBOOK_IG_FEED_1080x1350.jpg" class="w-full h-56 object-contain bg-white rounded-lg border border-gray-200" alt="Base 2">
          </a>
          <div class="flex flex-col gap-2">
            <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_2_FACEBOOK_IG_FEED_1080x1350_EDITABLE_CANVA.pptx" download class="bg-[#03582d] text-white text-center text-xs font-extrabold py-2 px-3 rounded-lg">✏️ Bajar Base 2 Editable (.PPTX con Fotos para Canva)</a>
            <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_2_FACEBOOK_IG_FEED_1080x1350_EDITABLE_CANVA.pdf" download class="bg-gray-900 text-white text-center text-xs font-extrabold py-2 px-3 rounded-lg">📄 Bajar Base 2 Editable (.PDF para Canva/Illustrator)</a>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-3">
          <div class="text-xs font-extrabold text-[#03582d] uppercase">3. Base LinkedIn Corporativo (1200×1200)</div>
          <p class="text-[11px] text-gray-600">Margen seguro aplicado: <strong>90px libres en los 4 lados</strong> para feed de escritorio y móvil de LinkedIn sin recortes laterales.</p>
          <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_3_LINKEDIN_1200x1200.jpg" target="_blank">
            <img src="piezas/3_BASES_MAESTRAS_CANVA/BASE_3_LINKEDIN_1200x1200.jpg" class="w-full h-56 object-contain bg-white rounded-lg border border-gray-200" alt="Base 3">
          </a>
          <div class="flex flex-col gap-2">
            <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_3_LINKEDIN_1200x1200_EDITABLE_CANVA.pptx" download class="bg-[#03582d] text-white text-center text-xs font-extrabold py-2 px-3 rounded-lg">✏️ Bajar Base 3 Editable (.PPTX con Fotos para Canva)</a>
            <a href="piezas/3_BASES_MAESTRAS_CANVA/BASE_3_LINKEDIN_1200x1200_EDITABLE_CANVA.pdf" download class="bg-gray-900 text-white text-center text-xs font-extrabold py-2 px-3 rounded-lg">📄 Bajar Base 3 Editable (.PDF para Canva/Illustrator)</a>
          </div>
        </div>
      </div>
    </div>

    <!-- 1. CALENDARIO CRONOLÓGICO VISIBLE (SENTIDO COMERCIAL CONECTADO CON PERFIT) -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <span class="text-xs font-extrabold uppercase text-[#03582d]">1. Cronograma con Sentido Comercial (Octubre → Noviembre 2026)</span>
          <h2 class="text-lg sm:text-xl font-extrabold text-gray-900">Calendario de Publicaciones Conectado al Embudo de Mailings Perfit</h2>
        </div>
        <span class="text-xs bg-gray-100 text-gray-800 font-bold px-3 py-1.5 rounded-lg">
          💡 Para editar en Canva / Illustrator / Adobe Express: descargá el botón <strong>✏️ SVG Editable</strong> de cualquier pieza y arrastralo a Canva o Illustrator.
        </span>
      </div>

      <div class="overflow-x-auto border border-gray-200 rounded-xl">
        <table class="w-full text-left text-xs">
          <thead class="bg-gray-100 text-gray-700 uppercase font-extrabold border-b border-gray-200">
            <tr>
              <th class="p-3">Fecha Programada</th>
              <th class="p-3">Pieza / Hito</th>
              <th class="p-3">Canales</th>
              <th class="p-3">Por qué va este día (Lógica de Embudo y Temporada)</th>
              <th class="p-3 text-center">Acción</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            {cal_rows}
          </tbody>
        </table>
      </div>
    </div>

    <!-- 2. VIDEOS MP4 SHORTS / REELS CON FOTOS OPERATIVAS REALES + SELECTOR DE 4 OPCIONES DE MÚSICA ARRIBA -->
    <div class="bg-white rounded-2xl p-6 border-2 border-[#03582d] shadow-sm space-y-6">
      <div class="flex flex-wrap items-start justify-between gap-4 border-b border-gray-200 pb-4">
        <div>
          <span class="inline-block bg-[#03582d] text-white text-[11px] font-extrabold uppercase px-3 py-0.5 rounded-full mb-1">
            🎵 NUEVO · 4 OPCIONES CON RITMO ARRIBA, MOVIMIENTO DE CÁMARA Y FIRMA HABLADA (CERO SINTETIZADOR LENTO)
          </span>
          <h2 class="text-lg sm:text-xl font-extrabold text-gray-900 mt-0.5">Probador en Vivo de Música y Locución + Videos .MP4 Listos</h2>
          <p class="text-xs text-gray-600 mt-1">Reemplazamos la base lenta anterior por <strong>4 opciones reales con instrumentos de estudio, groove arriba, zoom dinámico en cada foto y opción de firma hablada al cierre</strong>.</p>
        </div>
      </div>

      <!-- COMPARADOR DE LAS 4 OPCIONES SOBRE EL REEL DE 5 ESCENAS -->
      <div class="bg-emerald-50/70 rounded-2xl p-5 border-2 border-[#03582d] space-y-4">
        <div class="text-xs font-extrabold uppercase text-[#03582d]">🔊 Elegí cuál de las 4 opciones de audio te gusta más (tocá Play en cualquiera o descargala en 1 clic):</div>
        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- OPCION C (GROOVE + FIRMA FINAL CON VOZ DE VARÓN) -->
          <div class="bg-white p-3.5 rounded-xl border-2 border-[#03582d] shadow-sm flex flex-col justify-between space-y-3">
            <div>
              <span class="inline-block bg-[#03582d] text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full uppercase mb-1">✅ Opción 1 Aprobada · Voz de Varón al Inicio (0 dB)</span>
              <h3 class="font-extrabold text-xs text-gray-900">Firma Hablada con Voz de Varón al Inicio ("Star Union. Sabemos de limpieza") + Funk Groove Arriba</h3>
              <p class="text-[11px] text-gray-600 mt-1">15 seg exactos: la voz de varón entra una sola vez al inicio con ecualización 0 dB y luego corre el Funk Groove a pleno hasta el final.</p>
            </div>
            <video id="vid_hub_op1" src="piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4?v=varon_inicio_15s" poster="bases-canva-editables/ESCENA_1_REEL_1080x1920.jpg" preload="auto" controls class="w-full rounded-lg border border-gray-300 bg-white"></video>
            <button onclick="const v=document.getElementById('vid_hub_op1'); v.muted=false; v.volume=1.0; v.currentTime=0; v.play();" class="w-full block text-center bg-amber-500 hover:bg-amber-600 text-gray-950 text-[11px] font-extrabold py-2 px-3 rounded-lg transition shadow-sm">
              🔊 Tocar Play con Sonido al 100%
            </button>
            <a href="piezas/REEL_OPCION_C_GROOVE_CON_FIRMA_FINAL.mp4?v=varon_inicio_15s" download="REEL_STAR_UNION_FUNK_VOZ_VARON.mp4" class="block text-center bg-[#03582d] hover:bg-[#133522] text-white text-[11px] font-extrabold py-2 px-3 rounded-lg transition">
              ⬇ Bajar MP4 Oficial (Voz Varón al Inicio)
            </a>
          </div>

          <!-- OPCION A (SOLO FUNK GROOVE ARRIBA) -->
          <div class="bg-white p-3.5 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between space-y-3">
            <div>
              <span class="inline-block bg-gray-900 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full uppercase mb-1">Opción 2 · Solo Música Funk</span>
              <h3 class="font-extrabold text-xs text-gray-900">Funk & Sax Groove 100% Instrumental Bien Arriba (Estudio Real)</h3>
              <p class="text-[11px] text-gray-600 mt-1">Bajo funk, batería marcada y vientos con ritmo rápido para levantar las fotos operativas.</p>
            </div>
            <video src="piezas/REEL_OPCION_A_FUNK_GROOVE.mp4" poster="bases-canva-editables/ESCENA_1_REEL_1080x1920.jpg" preload="metadata" controls class="w-full rounded-lg border border-gray-300 bg-white"></video>
            <a href="piezas/REEL_OPCION_A_FUNK_GROOVE.mp4" download class="block text-center bg-gray-900 hover:bg-black text-white text-[11px] font-extrabold py-2 px-3 rounded-lg transition">
              ⬇ Bajar MP4 Opción 2
            </a>
          </div>

          <!-- OPCION B (POP-ROCK PUBLICITARIO LUMINOSO) -->
          <div class="bg-white p-3.5 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between space-y-3">
            <div>
              <span class="inline-block bg-gray-900 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full uppercase mb-1">Opción 3 · Pop-Rock Luminoso</span>
              <h3 class="font-extrabold text-xs text-gray-900">Upbeat Publicitario Luminoso (Guitarras y Batería Optimista)</h3>
              <p class="text-[11px] text-gray-600 mt-1">Estética de comercial televisivo luminoso, limpio y positivo (cero tono solemne).</p>
            </div>
            <video src="piezas/REEL_OPCION_B_UPBEAT_LUMINOSO.mp4" poster="bases-canva-editables/ESCENA_1_REEL_1080x1920.jpg" preload="metadata" controls class="w-full rounded-lg border border-gray-300 bg-white"></video>
            <a href="piezas/REEL_OPCION_B_UPBEAT_LUMINOSO.mp4" download class="block text-center bg-gray-900 hover:bg-black text-white text-[11px] font-extrabold py-2 px-3 rounded-lg transition">
              ⬇ Bajar MP4 Opción 3
            </a>
          </div>

          <!-- OPCION D (LOCUCIÓN B2B COMPLETA + MÚSICA ARRIBA) -->
          <div class="bg-white p-3.5 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between space-y-3">
            <div>
              <span class="inline-block bg-[#03582d] text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full uppercase mb-1">Opción 4 · Locución Completa</span>
              <h3 class="font-extrabold text-xs text-gray-900">Voz Rioplatense B2B Completa + Base Upbeat Luminosa</h3>
              <p class="text-[11px] text-gray-600 mt-1">Locución comercial firme durante los 15 seg contando los 800 m², taller propio e ISO 9001.</p>
            </div>
            <video src="piezas/REEL_OPCION_D_LOCUCION_COMPLETA_B2B.mp4?v=varon_fuerte_15s" poster="bases-canva-editables/ESCENA_1_REEL_1080x1920.jpg" preload="metadata" controls class="w-full rounded-lg border border-gray-300 bg-white"></video>
            <a href="piezas/REEL_OPCION_D_LOCUCION_COMPLETA_B2B.mp4?v=varon_fuerte_15s" download class="block text-center bg-[#03582d] hover:bg-[#133522] text-white text-[11px] font-extrabold py-2 px-3 rounded-lg transition">
              ⬇ Bajar MP4 Opción 4
            </a>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-2 gap-6">
        <!-- SHORT #1 -->
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 flex flex-col sm:flex-row items-center gap-4">
          <video src="piezas/short_01_infraestructura_y_presentismo_1080x1920.mp4?v=varon_inicio_15s" poster="piezas/01_story_logistica_industria_1080x1920.jpg" preload="metadata" controls class="w-36 rounded-lg border border-gray-300 shadow-sm shrink-0 bg-white"></video>
          <div class="space-y-2">
            <span class="text-[11px] font-extrabold text-[#03582d] uppercase">📅 Jueves 29 Oct 2026 · Voz Varón al Inicio (0 dB) + Funk Groove</span>
            <h3 class="font-extrabold text-sm text-gray-900">Short #1: Infraestructura 800 m² Guaminí + Taller Propio + Presentismo Biométrico</h3>
            <a href="piezas/short_01_infraestructura_y_presentismo_1080x1920.mp4?v=varon_inicio_15s" download class="inline-block bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2 rounded-lg transition">
              ⬇ Descargar Video Short #1 (.MP4)
            </a>
          </div>
        </div>

        <!-- SHORT #2 -->
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 flex flex-col sm:flex-row items-center gap-4">
          <video src="piezas/short_02_verticales_iso9001_1080x1920.mp4?v=varon_inicio_15s" poster="piezas/04_story_salud_laboratorios_1080x1920.jpg" preload="metadata" controls class="w-36 rounded-lg border border-gray-300 shadow-sm shrink-0 bg-white"></video>
          <div class="space-y-2">
            <span class="text-[11px] font-extrabold text-[#03582d] uppercase">📅 Viernes 06 Nov 2026 · Voz Varón al Inicio (0 dB) + Funk Groove</span>
            <h3 class="font-extrabold text-sm text-gray-900">Short #2: Verticales de Alta Exigencia (Logística, Salud ANMAT y Educación) · ISO 9001</h3>
            <a href="piezas/short_02_verticales_iso9001_1080x1920.mp4?v=varon_inicio_15s" download class="inline-block bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2 rounded-lg transition">
              ⬇ Descargar Video Short #2 (.MP4)
            </a>
          </div>
        </div>
      </div>

      <!-- DESGLOSE VISUAL DE LAS 5 ESCENAS CON FOTO REAL DEL REEL DINÁMICO -->
      <div class="pt-4 border-t border-gray-200">
        <div class="text-xs font-extrabold uppercase text-[#03582d] mb-3">Vista Previa de las 5 Escenas del Reel Dinámico (Todas con fotografía operativa real + margen seguro 1080×1920):</div>
        <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <a href="bases-canva-editables/ESCENA_1_REEL_1080x1920.jpg" target="_blank" class="block bg-gray-50 p-2 rounded-xl border border-gray-200 hover:border-[#03582d] transition">
            <img src="bases-canva-editables/ESCENA_1_REEL_1080x1920.jpg" class="w-full rounded-lg border border-gray-200" alt="Escena 1">
            <div class="text-[11px] font-bold text-center text-gray-800 mt-1.5">Escena 1 (0–3s) · Gancho</div>
          </a>
          <a href="bases-canva-editables/ESCENA_2_REEL_1080x1920.jpg" target="_blank" class="block bg-gray-50 p-2 rounded-xl border border-gray-200 hover:border-[#03582d] transition">
            <img src="bases-canva-editables/ESCENA_2_REEL_1080x1920.jpg" class="w-full rounded-lg border border-gray-200" alt="Escena 2">
            <div class="text-[11px] font-bold text-center text-gray-800 mt-1.5">Escena 2 (3–6s) · Naves</div>
          </a>
          <a href="bases-canva-editables/ESCENA_3_REEL_1080x1920.jpg" target="_blank" class="block bg-gray-50 p-2 rounded-xl border border-gray-200 hover:border-[#03582d] transition">
            <img src="bases-canva-editables/ESCENA_3_REEL_1080x1920.jpg" class="w-full rounded-lg border border-gray-200" alt="Escena 3">
            <div class="text-[11px] font-bold text-center text-gray-800 mt-1.5">Escena 3 (6–9s) · Taller</div>
          </a>
          <a href="bases-canva-editables/ESCENA_4_REEL_1080x1920.jpg" target="_blank" class="block bg-gray-50 p-2 rounded-xl border border-gray-200 hover:border-[#03582d] transition">
            <img src="bases-canva-editables/ESCENA_4_REEL_1080x1920.jpg" class="w-full rounded-lg border border-gray-200" alt="Escena 4">
            <div class="text-[11px] font-bold text-center text-gray-800 mt-1.5">Escena 4 (9–12s) · ISO/Reloj</div>
          </a>
          <a href="bases-canva-editables/ESCENA_5_REEL_1080x1920.jpg" target="_blank" class="block bg-gray-50 p-2 rounded-xl border border-gray-200 hover:border-[#03582d] transition">
            <img src="bases-canva-editables/ESCENA_5_REEL_1080x1920.jpg" class="w-full rounded-lg border border-gray-200" alt="Escena 5">
            <div class="text-[11px] font-bold text-center text-gray-800 mt-1.5">Escena 5 (12–15s) · Flota</div>
          </a>
        </div>
      </div>
    </div>

    <!-- 3. LAS 5 PUBLICACIONES CON JPG + SVG EDITABLE + COPIES -->
    <div class="space-y-6">
      {cards_html}
    </div>
  </div>

  <script>
    const API_BASE = (location.hostname === '127.0.0.1' || location.hostname === 'localhost') ? '' : 'http://127.0.0.1:8894';

    function copyText(id, btn) {{
      const el = document.getElementById(id);
      navigator.clipboard.writeText(el.innerText);
      const old = btn.innerText;
      btn.innerText = '✅ ¡Copiado!';
      setTimeout(() => btn.innerText = old, 1800);
    }}

    function toggleApiBox() {{
      const b = document.getElementById('api-config-box');
      b.classList.toggle('hidden');
    }}

    async function loadApiStatus() {{
      const line = document.getElementById('api-status-line');
      try {{
        const r = await fetch(API_BASE + '/api/status');
        const st = await r.json();
        const parts = [];
        parts.push(st.meta_connected ? `🟢 Meta ACTIVO (${{st.fb_page_name || 'FB'}} + @${{st.ig_username || 'IG'}})` : `🔴 Meta (FB/IG) pendiente`);
        parts.push(st.linkedin_connected ? `🟢 LinkedIn (${{st.linkedin_name}})` : `⚪ LinkedIn pendiente`);
        parts.push(st.gmb_connected ? `🟢 Google Maps conectado` : `⚪ Google Maps pendiente`);
        parts.push(st.youtube_connected ? `🟢 YouTube (${{st.youtube_channel_name || 'Conectado'}})` : `⚪ YouTube pendiente`);
        parts.push(st.tiktok_connected ? `🟢 TikTok conectado` : `⚪ TikTok pendiente`);
        line.innerHTML = parts.join(' &nbsp;·&nbsp; ');
        const metaBox = document.getElementById('status-box-meta');
        if (metaBox && st.meta_connected) {{
          metaBox.innerHTML = `✅ CONECTADO Y ACTIVO:<br>• Facebook: <strong>${{st.fb_page_name}}</strong> (${{st.fb_page_id}})<br>• Instagram: <strong>@${{st.ig_username}}</strong> (${{st.ig_user_id}})`;
        }}
        const ytBox = document.getElementById('status-box-yt');
        if (ytBox && st.youtube_connected) {{
          ytBox.innerHTML = `✅ CONECTADO Y ACTIVO: <strong>${{st.youtube_channel_name || 'Star Union | Limpieza Profesional e Industrial'}} (@starunionservicios)</strong>`;
        }}
        const gmbBox = document.getElementById('status-box-gmb');
        if (gmbBox && st.gmb_connected) {{
          gmbBox.style.background = '#d1fae5';
          gmbBox.style.borderColor = '#10b981';
          gmbBox.style.color = '#065f46';
          gmbBox.innerHTML = `✅ CONECTADO Y ACTIVO: <strong>${{st.gmb_location_title || 'Star Union (Google Maps)'}}</strong> (${{st.gmb_location_name || 'Auto-detectado'}})`;
        }}
      }} catch (e) {{
        line.innerHTML = '⚠️ Servidor API local corriendo en http://127.0.0.1:8894';
      }}
    }}

    function connectTikTokOAuth() {{
      const ck = document.getElementById('inp-tt-ck').value.trim();
      const cs = document.getElementById('inp-tt-cs').value.trim();
      if (!ck || !cs) {{
        alert('Pegá primero el Client Key y el Client Secret que figuran arriba en la página de tu App de TikTok.');
        return;
      }}
      window.location.href = API_BASE + '/api/tiktok/login?client_key=' + encodeURIComponent(ck) + '&client_secret=' + encodeURIComponent(cs);
    }}

    async function saveApiTokens(btnEl) {{
      const logEl = document.getElementById('api-connect-log');
      const oldBtn = btnEl ? btnEl.innerHTML : '';
      if (btnEl) btnEl.innerHTML = '⏳ Conectando...';
      logEl.innerHTML = '⏳ Conectando y auto-detectando cuentas de Star Union...';
      const payload = {{
        meta_token: document.getElementById('inp-meta-token').value,
        linkedin_token: document.getElementById('inp-li-token').value,
        linkedin_urn: document.getElementById('inp-li-urn').value,
        gmb_token: document.getElementById('inp-gmb-token').value,
        youtube_token: document.getElementById('inp-yt-token').value,
        tiktok_client_key: document.getElementById('inp-tt-ck') ? document.getElementById('inp-tt-ck').value : '',
        tiktok_client_secret: document.getElementById('inp-tt-cs') ? document.getElementById('inp-tt-cs').value : ''
      }};
      try {{
        const r = await fetch(API_BASE + '/api/connect', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload)
        }});
        const data = await r.json();
        const msg = (data.messages || []).join('<br>') || '✅ Guardado en bóveda de Star Union.';
        logEl.innerHTML = msg;
        if (btnEl) btnEl.innerHTML = '✅ ¡CONECTADO CON ÉXITO!';
        const metaBox = document.getElementById('status-box-meta');
        if (metaBox && data.status && data.status.meta_connected) {{
          metaBox.innerHTML = `✅ CONECTADO Y ACTIVO: FB <strong>${{data.status.fb_page_name}}</strong> + IG <strong>@${{data.status.ig_username}}</strong>`;
        }}
        loadApiStatus();
      }} catch (e) {{
        logEl.innerHTML = '❌ Error conectando al servidor local (http://127.0.0.1:8894): ' + e.message;
        if (btnEl) btnEl.innerHTML = oldBtn;
      }}
    }}

    async function publishPostViaApi(id, feedFile, storyFile, reelFile, btn) {{
      const resBox = document.getElementById('api_res_' + id);
      resBox.classList.remove('hidden');
      resBox.innerHTML = '⏳ Publicando por API oficial en los canales seleccionados...';
      const channels = [];
      if (document.getElementById('chk_ig_feed_' + id).checked) channels.push('ig_feed');
      if (document.getElementById('chk_ig_story_' + id).checked) channels.push('ig_story');
      if (document.getElementById('chk_ig_reel_' + id).checked) channels.push('ig_reel');
      if (document.getElementById('chk_fb_' + id).checked) channels.push('fb_page');
      if (document.getElementById('chk_li_' + id).checked) channels.push('linkedin');
      if (document.getElementById('chk_gmb_' + id).checked) channels.push('gmb');
      if (document.getElementById('chk_yt_' + id).checked) channels.push('youtube');
      if (document.getElementById('chk_tt_' + id).checked) channels.push('tiktok');

      const payload = {{
        channels: channels,
        feed_file: feedFile,
        story_file: storyFile,
        reel_file: reelFile,
        caption_ig: document.getElementById('ig_' + id).innerText,
        caption_li: document.getElementById('li_' + id).innerText,
        yt_title: document.getElementById('ytt_' + id).innerText,
        yt_desc: document.getElementById('ytd_' + id).innerText,
        yt_tags: document.getElementById('yttags_' + id).innerText,
        public_url: 'https://www.starunion.com.ar',
        title: document.getElementById('ytt_' + id).innerText
      }};
      try {{
        const r = await fetch(API_BASE + '/api/publish', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload)
        }});
        const data = await r.json();
        const lines = [];
        for (const [k, v] of Object.entries(data.results || {{}})) {{
          lines.push(v.ok ? `✅ <strong>${{k}}:</strong> Publicado (ID: ${{v.id}})` : `❌ <strong>${{k}}:</strong> ${{v.error}}`);
        }}
        resBox.innerHTML = lines.join('<br>') || '⚠️ Seleccioná al menos un canal.';
      }} catch (e) {{
        resBox.innerHTML = '❌ Error conectando con http://127.0.0.1:8894: ' + e.message;
      }}
    }}

    window.addEventListener('DOMContentLoaded', loadApiStatus);
  </script>
</body>
</html>"""

    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)
    print("Editable SVGs, Bulk CSV, and Chronological Calendar generated successfully.")

if __name__ == "__main__":
    main()
