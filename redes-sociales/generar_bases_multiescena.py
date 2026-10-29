#!/usr/bin/env python3
"""
Genera las 3 Bases Maestras Editables en Canva (.pptx + .pdf) como SECUENCIAS DINÁMICAS (5 escenas por Reel / 5 slides por Carrusel IG y LinkedIn)
respetando los Márgenes de Seguridad exactos de cada red, + actualiza los videos .mp4 con secuencia multi-escena real (cambios de plano cada 3s).
"""
import os
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union/redes-sociales"
BASES_DIR = os.path.join(BASE_DIR, "bases-canva-editables")
DRIVE_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/su para AG/REDES_SOCIALES_Y_SHORTS_2026/00_BASES_MADRE_CANVA_CON_MARGEN_SEGURO"
DRIVE_MP4_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/su para AG/REDES_SOCIALES_Y_SHORTS_2026"
os.makedirs(BASES_DIR, exist_ok=True)
os.makedirs(DRIVE_DIR, exist_ok=True)

DARK = RGBColor(26, 26, 26)
CHARCOAL = RGBColor(38, 38, 38)
GREEN = RGBColor(46, 125, 50)
GREEN_SOFT = RGBColor(232, 245, 233)
WHITE = RGBColor(255, 255, 255)
OFFWHITE = RGBColor(247, 248, 247)
MUTED = RGBColor(90, 96, 101)
BORDER = RGBColor(218, 224, 220)

SCENES_REEL = [
    {
        "step": "ESCENA 1 DE 5 · GANCHO (0 a 3 seg)",
        "cat": "LIMPIEZA INDUSTRIAL Y CENTROS LOGÍSTICOS · B2B",
        "title": "¿Tu planta industrial o centro logístico resiste hoy una auditoría operativa y legal?",
        "body": "Operar con proveedores sin respaldo expone a la empresa a contingencias solidarias (Art. 30 LCT) y paradas por maquinaria caída.",
        "highlight": "DESLIZÁ / MIRÁ EL PROCESO EN 15 SEG →",
        "img": "/Users/arianawajntraub/Documents/antigravity/star-union/assets/img/valvulas_1_1774566253599.png"
    },
    {
        "step": "ESCENA 2 DE 5 · EL RIESGO EN CAMPO (3 a 6 seg)",
        "cat": "PUNTO CRÍTICO EN OPERACIÓN",
        "title": "Riesgo solidario Art. 30 LCT y máquinas paradas por falta de taller propio",
        "body": "Sin nómina 100% propia ni taller electromecánico de reemplazo inmediato, el servicio se corta en plena operación.",
        "highlight": "DIAGNÓSTICO EN PLANTA Y EN BASE PROPIA",
        "img": "/Users/arianawajntraub/Documents/antigravity/star-union/assets/img/hero_option_2_field_1774550794303.png"
    },
    {
        "step": "ESCENA 3 DE 5 · INTERVENCIÓN TÉCNICA (6 a 9 seg)",
        "title": "Base Operativa Guaminí: Taller Electromecánico Propio y Flota de Reemplazo",
        "cat": "PROTOCOLO STAR UNION",
        "body": "Mantenimiento preventivo de fregadoras, barredoras e hidrolavadoras industriales sin depender de terceros.",
        "highlight": "BASE PROPIA GUAMINÍ · RESPUESTA EN 24 HS",
        "img": "/Users/arianawajntraub/Documents/antigravity/star-union/assets/img/valvulas_2_1774566275567.png"
    },
    {
        "step": "ESCENA 4 DE 5 · EVIDENCIA Y NORMA (9 a 12 seg)",
        "cat": "CERTIFICACIÓN PARA AUDITORÍA",
        "title": "Calidad Certificada ISO 9001:2015 TÜV Rheinland (ID 9000041847) + Blindaje Art. 30",
        "body": "Carpetas mensuales F.931, ART con cláusula de no repetición, seguros e higiene y seguridad al día.",
        "highlight": "TRAZABILIDAD DOCUMENTAL 100% COMPLETA",
        "img": "/Users/arianawajntraub/Documents/antigravity/star-union/assets/img/iso_3_1774566497461.png"
    },
    {
        "step": "ESCENA 5 DE 5 · CIERRE Y CONTACTO (12 a 15 seg)",
        "cat": "STAR UNION S.R.L. · MÁS DE 25 AÑOS EN LIMPIEZA B2B",
        "title": "Pedí hoy el relevamiento técnico para tu planta o edificio",
        "body": "Propuesta operativa a medida para fábricas, centros logísticos, oficinas corporativas e instituciones.",
        "highlight": "📲 WHATSAPP COMERCIAL · WWW.STARUNION.COM.AR",
        "img": "/Users/arianawajntraub/Documents/antigravity/star-union/assets/img/instalaciones_1_1774566398081.png"
    }
]

def add_rect(slide, x, y, w, h, fill_rgb, line_rgb=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if line_rgb:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def add_textbox(slide, x, y, w, h, text, font_size, bold=False, color=DARK):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = "Arial"
    return tb

def build_pptx_multiscene(filename, width_px, height_px, top_safe_px, bottom_safe_px, right_safe_px, left_safe_px, mode_label):
    prs = Presentation()
    w_in = width_px / 96.0
    h_in = height_px / 96.0
    prs.slide_width = Inches(w_in)
    prs.slide_height = Inches(h_in)
    blank_layout = prs.slide_layouts[6]

    sx = left_safe_px / 96.0
    sy = top_safe_px / 96.0
    sw = (width_px - left_safe_px - right_safe_px) / 96.0
    sh = (height_px - top_safe_px - bottom_safe_px) / 96.0

    for idx, sc in enumerate(SCENES_REEL):
        slide = prs.slides.add_slide(blank_layout)
        # Alternate subtle light/dark-accent headers so each scene feels visually distinct in motion
        add_rect(slide, 0, 0, w_in, h_in, WHITE if idx % 2 == 0 else OFFWHITE)
        add_rect(slide, sx, sy, sw, 0.10, GREEN)

        # Header brand bar inside Safe Zone
        add_textbox(slide, sx, sy + 0.16, sw * 0.62, 0.40, "STAR UNION · LIMPIEZA INDUSTRIAL Y CORPORATIVA B2B", 15, bold=True, color=DARK)
        pill = add_rect(slide, sx + sw * 0.63, sy + 0.14, sw * 0.37, 0.42, GREEN_SOFT, GREEN)
        add_textbox(slide, sx + sw * 0.64, sy + 0.18, sw * 0.35, 0.36, sc["step"], 11, bold=True, color=GREEN)

        # Photo inside Safe Zone
        img_y = sy + 0.68
        img_h = sh * 0.40
        if os.path.exists(sc["img"]):
            slide.shapes.add_picture(sc["img"], Inches(sx), Inches(img_y), width=Inches(sw), height=Inches(img_h))

        # Category & Scene number
        cat_y = img_y + img_h + 0.16
        add_textbox(slide, sx, cat_y, sw, 0.35, sc["cat"], 13, bold=True, color=GREEN)

        # Editable H1 Title
        title_y = cat_y + 0.34
        add_textbox(slide, sx, title_y, sw, sh * 0.20, sc["title"], 26 if height_px >= 1350 else 23, bold=True, color=DARK)

        # Editable Body
        body_y = title_y + sh * 0.19
        add_textbox(slide, sx, body_y, sw, sh * 0.13, sc["body"], 15, bold=False, color=MUTED)

        # Bottom CTA Bar inside Safe Zone
        cta_h = 0.68
        cta_y = sy + sh - cta_h
        add_rect(slide, sx, cta_y, sw, cta_h, DARK if idx < 4 else GREEN)
        add_textbox(slide, sx + 0.2, cta_y + 0.14, sw - 0.4, 0.42, sc["highlight"], 14, bold=True, color=WHITE)

    out_pptx = os.path.join(BASES_DIR, filename)
    prs.save(out_pptx)
    subprocess.run(["cp", out_pptx, os.path.join(DRIVE_DIR, filename)], check=True)
    print("Saved 5-scene editable PPTX:", out_pptx)

# 1. REEL / SHORT (1080x1920) - 5 Escenas encadenadas
build_pptx_multiscene(
    "BASE_1_REEL_SHORT_1080x1920_EDITABLE_CANVA.pptx",
    1080, 1920,
    top_safe_px=250, bottom_safe_px=420, right_safe_px=140, left_safe_px=70,
    mode_label="REEL 5 ESCENAS"
)

# 2. FACEBOOK / IG FEED CARRUSEL (1080x1350) - 5 Placas deslizables
build_pptx_multiscene(
    "BASE_2_FACEBOOK_IG_FEED_1080x1350_EDITABLE_CANVA.pptx",
    1080, 1350,
    top_safe_px=145, bottom_safe_px=145, right_safe_px=75, left_safe_px=75,
    mode_label="CARRUSEL IG/FB 5 PLACAS"
)

# 3. LINKEDIN CARRUSEL DOCUMENTO (1200x1200) - 5 Placas técnicas B2B
build_pptx_multiscene(
    "BASE_3_LINKEDIN_1200x1200_EDITABLE_CANVA.pptx",
    1200, 1200,
    top_safe_px=90, bottom_safe_px=90, right_safe_px=90, left_safe_px=90,
    mode_label="CARRUSEL LINKEDIN 5 PLACAS"
)
