#!/usr/bin/env python3
"""
Genera los 5 frames de la secuencia de Reel 1080x1920 con margen de seguridad real (250px arriba, 420px abajo, 140px derecha),
usando fotografías operativas reales de Star Union S.R.L., logo oficial, sello TÜV Rheinland ISO 9001:2015 y música institucional.
"""
import os
import subprocess
from PIL import Image
import imageio_ffmpeg

ROOT_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"
BASE_DIR = os.path.join(ROOT_DIR, "redes-sociales")
BASES_DIR = os.path.join(BASE_DIR, "bases-canva-editables")
PIEZAS_DIR = os.path.join(BASE_DIR, "piezas")
TMP_DIR = os.path.join(BASE_DIR, "tmp_render")
DRIVE_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/su para AG/REDES_SOCIALES_Y_SHORTS_2026/00_BASES_MADRE_CANVA_CON_MARGEN_SEGURO"

os.makedirs(BASES_DIR, exist_ok=True)
os.makedirs(PIEZAS_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(DRIVE_DIR, exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
AUDIO_PATH = os.path.join(ROOT_DIR, "audio", "starunion_musica_original_sin_canva_15s.mp3")

SCENES = [
    {
        "step": "ESCENA 1/5 · GANCHO (0-3s)",
        "cat": "LIMPIEZA INDUSTRIAL Y CENTROS LOGÍSTICOS · B2B",
        "title": "¿Tu planta industrial o centro logístico resiste hoy una auditoría operativa y legal?",
        "body": "Operar con proveedores sin respaldo expone a la empresa a contingencias solidarias (Art. 30 LCT) y paradas por maquinaria caída.",
        "cta": "MIRÁ EL PROCESO EN 15 SEGUNDOS →",
        "img": os.path.join(ROOT_DIR, "brochures/img/p1-industria-playa-hd.jpg"),
        "obj_pos": "center 45%"
    },
    {
        "step": "ESCENA 2/5 · CONTINUIDAD EN PLANTA (3-6s)",
        "cat": "MAQUINARIA PROPIA DE ALTO RENDIMIENTO",
        "title": "Fregado y barrido mecanizado en pasillos de racks y naves sin frenar el despacho",
        "body": "Autolavadoras hombre a bordo, barredoras industriales y supervisión técnica permanente en cada turno.",
        "cta": "DIAGNÓSTICO EN CAMPO Y EN BASE PROPIA →",
        "img": os.path.join(ROOT_DIR, "brochures/img/p1-industria-hombre-a-bordo-hd.jpg"),
        "obj_pos": "center 35%"
    },
    {
        "step": "ESCENA 3/5 · INFRAESTRUCTURA PROPIA (6-9s)",
        "cat": "BASE PROPIA 800 M² · GUAMINÍ 5657 CABA",
        "title": "Taller Electromecánico In-House y Flota Propia de Reemplazo Inmediato",
        "body": "Mantenimiento preventivo de fregadoras, barredoras e hidrolavadoras en nuestra base de 3 niveles sin depender de terceros.",
        "cta": "BASE PROPIA GUAMINÍ · RESPUESTA EN EL DÍA →",
        "img": os.path.join(ROOT_DIR, "assets/img/perfit-curadas/perfit-base-maquinas.jpg"),
        "obj_pos": "center 50%"
    },
    {
        "step": "ESCENA 4/5 · TRAZABILIDAD Y NORMA (9-12s)",
        "cat": "CERTIFICACIÓN ISO 9001:2015 TÜV RHEINLAND",
        "title": "Presentismo Biométrico Auditado (Alerta 15 min) + Blindaje Art. 30 LCT",
        "body": "Cobertura de ausencias en menos de 2 horas con guardia móvil y legajo mensual F.931 + ART al día.",
        "cta": "CERTIPEDIA ID 9000041847 · 100% AUDITABLE →",
        "img": os.path.join(ROOT_DIR, "assets/img/base-guamini-biometrico.jpg"),
        "obj_pos": "center 30%"
    },
    {
        "step": "ESCENA 5/5 · CONTACTO DIRECTO (12-15s)",
        "cat": "STAR UNION · DESDE 2001 EN LIMPIEZA B2B",
        "title": "Solicitá hoy un relevamiento técnico para tu planta, centro logístico o edificio",
        "body": "Propuesta operativa a medida en CABA y GBA con certificación internacional TÜV Rheinland ISO 9001:2015.",
        "cta": "📲 WHATSAPP +54 9 11 2275-9369 · STARUNION.COM.AR",
        "img": os.path.join(ROOT_DIR, "brochures/img/p2-guamini-utilitario-transit-hd.jpg"),
        "obj_pos": "center 50%"
    }
]

logo_path = os.path.join(ROOT_DIR, "assets/img/logo-star-union.png")
tuv_path = os.path.join(ROOT_DIR, "assets/img/tuv-iso-9001-badge.png")

frame_paths = []
for i, sc in enumerate(SCENES):
    if not os.path.exists(sc["img"]):
        raise FileNotFoundError(f"Missing scene photo: {sc['img']}")

    progress_bars = "".join([
        f'<div style="flex:1;height:8px;border-radius:999px;background:{"#03582d" if s_idx <= i else "#e5e7eb"};"></div>'
        for s_idx in range(5)
    ])

    cta_bg = "#03582d" if i == 4 else "#111827"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1920px;
    overflow: hidden;
    background: #ffffff;
    font-family: 'Open Sans', sans-serif;
    color: #111827;
    padding: 250px 140px 420px 76px; /* Safe Zone Reel: 250 arriba, 420 abajo, 140 derecha, 76 izquierda */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
</style>
</head>
<body>
  <!-- TOP HEADER & SCENE PROGRESS BAR -->
  <div>
    <div style="display:flex;gap:8px;margin-bottom:18px;">
      {progress_bars}
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;">
      <img src="file://{logo_path}" style="height:56px;width:auto;object-fit:contain;" alt="Star Union">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="background:#e6efea;border:1.5px solid #03582d;color:#03582d;font-weight:800;font-size:14px;padding:7px 14px;border-radius:999px;">
          {sc["step"]}
        </div>
        <div style="display:flex;align-items:center;gap:8px;background:#f9fafb;border:1px solid #e5e7eb;padding:6px 12px;border-radius:10px;">
          <img src="file://{tuv_path}" style="height:32px;width:auto;object-fit:contain;" alt="ISO 9001">
          <div>
            <div style="font-size:11px;font-weight:800;color:#03582d;">ISO 9001:2015</div>
            <div style="font-size:10px;color:#4b5563;font-weight:700;">TÜV Rheinland</div>
          </div>
        </div>
      </div>
    </div>

    <!-- REAL OPERATIONAL PHOTO INSIDE SAFE ZONE -->
    <div style="width:100%;height:500px;border-radius:24px;overflow:hidden;border:3px solid #03582d;box-shadow:0 16px 34px rgba(3,88,45,0.12);margin-bottom:22px;background:#f3f4f6;">
      <img src="file://{sc['img']}" style="width:100%;height:100%;object-fit:cover;object-position:{sc['obj_pos']};" alt="">
    </div>

    <div style="display:inline-block;background:rgba(3,88,45,0.10);color:#03582d;font-weight:800;font-size:15px;letter-spacing:0.06em;padding:6px 14px;border-radius:999px;margin-bottom:12px;">
      {sc["cat"]}
    </div>

    <h1 style="font-size:36px;line-height:1.16;font-weight:800;color:#111827;letter-spacing:-0.015em;margin-bottom:12px;">
      {sc["title"]}
    </h1>

    <p style="font-size:21px;line-height:1.38;color:#374151;font-weight:600;">
      {sc["body"]}
    </p>
  </div>

  <!-- BOTTOM CTA BAR INSIDE SAFE ZONE -->
  <div style="background:{cta_bg};color:#ffffff;padding:18px 26px;border-radius:18px;display:flex;align-items:center;justify-content:space-between;border-bottom:4px solid #ffcc29;">
    <div style="font-size:19px;font-weight:800;letter-spacing:0.02em;">{sc["cta"]}</div>
    <div style="background:#ffffff;color:#03582d;font-size:14px;font-weight:800;padding:7px 14px;border-radius:999px;">0810-333-8646</div>
  </div>
</body>
</html>"""

    html_path = os.path.join(TMP_DIR, f"escena_reel_{i+1}.html")
    png_path = os.path.join(TMP_DIR, f"escena_reel_{i+1}.png")
    fp = os.path.join(BASES_DIR, f"ESCENA_{i+1}_REEL_1080x1920.jpg")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--window-size=1080,1920", f"--screenshot={png_path}", f"file://{html_path}"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    Image.open(png_path).convert("RGB").save(fp, "JPEG", quality=95)
    subprocess.run(["cp", fp, os.path.join(DRIVE_DIR, f"ESCENA_{i+1}_REEL_1080x1920.jpg")], check=True)
    frame_paths.append(fp)

# Stitch the 5 scenes into a real 15-second multi-scene MP4 WITH institutional audio
mp4_out = os.path.join(BASES_DIR, "REEL_5_ESCENAS_DINAMICO_15SEG.mp4")
mp4_piezas = os.path.join(PIEZAS_DIR, "REEL_5_ESCENAS_DINAMICO_15SEG.mp4")

cmd = [
    FFMPEG, "-y",
    "-loop", "1", "-t", "3", "-i", frame_paths[0],
    "-loop", "1", "-t", "3", "-i", frame_paths[1],
    "-loop", "1", "-t", "3", "-i", frame_paths[2],
    "-loop", "1", "-t", "3", "-i", frame_paths[3],
    "-loop", "1", "-t", "3", "-i", frame_paths[4],
    "-i", AUDIO_PATH,
    "-filter_complex",
    "[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0,format=yuv420p[v]",
    "-map", "[v]",
    "-map", "5:a",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-r", "30",
    "-movflags", "+faststart",
    mp4_out
]
subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["cp", mp4_out, mp4_piezas], check=True)
subprocess.run(["cp", mp4_out, os.path.join(DRIVE_DIR, "REEL_5_ESCENAS_DINAMICO_15SEG.mp4")], check=True)
print("Generated multi-scene MP4 with real photos & audio:", mp4_out)
