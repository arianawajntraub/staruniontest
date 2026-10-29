#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from PIL import Image
import imageio_ffmpeg

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"
OUT_DIR = os.path.join(BASE_DIR, "redes-sociales")
PIEZAS_DIR = os.path.join(OUT_DIR, "piezas")
TMP_DIR = os.path.join(OUT_DIR, "tmp_render")

os.makedirs(PIEZAS_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

POSTS = [
    {
        "id": "01",
        "slug": "logistica_industria",
        "day_label": "Publicación 1 · Hoy / Mañana (Vertical #1 en Clics B2B)",
        "tag": "LOGÍSTICA E INDUSTRIA · ISO 9001:2015",
        "title": "Operación continua en centros logísticos y plantas industriales.",
        "subtitle": "Autolavadoras hombre a bordo, barredoras industriales y supervisión técnica bajo norma ISO 9001:2015 (TÜV Rheinland) sin detener tu línea ni el despacho.",
        "kpis": ["+800 m² Base Propia CABA", "Taller Propio In-House", "ISO 9001:2015 TÜV"],
        "photo": "../../assets/img/perfit-curadas/perfit-logistica-pallets.jpg",
        "use_cleany": False,
        "cta_pill": "www.starunion.com.ar",
        "copy_ig_fb": """Continuidad operativa real para centros logísticos, depósitos y plantas industriales en CABA y GBA.

En operaciones de alto tránsito de autoelevadores y despacho 24/7, la limpieza técnica no puede improvisarse ni frenar el ritmo de planta:

✔️ Maquinaria propia de alto rendimiento (autolavadoras y barredoras industriales).
✔️ Respaldo de nuestra Base Operativa Propia de 800 m² en calle Guaminí (CABA) con taller electromecánico in-house: si un equipo requiere asistencia, lo reemplazamos en el día.
✔️ Procesos auditados bajo Norma ISO 9001:2015 por TÜV Rheinland (ID Certipedia 9000041847).

Solicitá un relevamiento técnico para tu planta o centro logístico en www.starunion.com.ar o por WhatsApp Comercial al +54 9 11 2275-9369.

#StarUnion #LimpiezaIndustrial #LogisticaArgentina #FacilityManagement #ISO9001 #MantenimientoIndustrial""",
        "copy_linkedin": """En logística e industria manufacturera, el proveedor de limpieza e higiene técnica impacta de forma directa en la seguridad operativa y en las auditorías de calidad.

Por eso en Star Union S.R.L. estructuramos nuestro servicio industrial sobre tres pilares verificables:

1. Infraestructura propia: operamos desde nuestra Base Operativa Central de 800 m² (3 niveles) en Guaminí 5657, CABA, con stock permanente de insumos aprobados por ANMAT y flota propia de soporte (unidades Ford Transit).
2. Cero paradas por maquinaria: contamos con taller electromecánico propio in-house activo desde fines de 2010 para mantenimiento preventivo y reemplazo inmediato de equipos en planta.
3. Calidad certificada: procesos auditados bajo Norma ISO 9001:2015 por TÜV Rheinland (Certipedia ID 9000041847).

👉 Conocé nuestro protocolo para plantas y centros logísticos en: https://www.starunion.com.ar

#FacilityManagement #Logistica #IndustriaArgentina #ISO9001 #HigieneIndustrial #OperacionesB2B #StarUnion""",
        "yt_title": "Limpieza Técnica en Centros Logísticos y Plantas | Star Union ISO 9001",
        "yt_desc": """Cómo garantizamos la continuidad operativa en centros logísticos, depósitos y plantas industriales de CABA y GBA sin detener el despacho.

00:00 Limpieza mecanizada en pasillos de racks y zonas de despacho
00:04 Base Operativa Propia de 800 m² en calle Guaminí (CABA) y Taller Propio
00:08 Certificación ISO 9001:2015 por TÜV Rheinland (ID 9000041847)

Solicitá una visita técnica para tu empresa en: https://www.starunion.com.ar
WhatsApp Comercial B2B: +54 9 11 2275-9369""",
        "yt_tags": "limpieza industrial, centros logisticos, limpieza de depositos, star union, iso 9001 tuv rheinland, facility management argentina, autolavadoras industriales, mantenimiento de plantas",
        "copy_wa": "Operación continua en centros logísticos y plantas industriales con maquinaria propia y certificación ISO 9001:2015 (TÜV Rheinland). Conocé más en https://www.starunion.com.ar"
    },
    {
        "id": "02",
        "slug": "base_operativa_taller",
        "day_label": "Publicación 2 · Infraestructura Propia (Diferenciador #1 B2B)",
        "tag": "INFRAESTRUCTURA PROPIA · GUAMINÍ 5657 CABA",
        "title": "Taller electromecánico propio: tus máquinas en planta nunca se detienen.",
        "subtitle": "En nuestra Base Operativa de 800 m² en CABA reparamos, mantenemos y despachamos equipos de reemplazo con flota propia sin depender de terceros.",
        "kpis": ["Taller Propio desde 2010", "Flota Ford Transit", "Respuesta en el Día"],
        "photo": "../../assets/img/perfit-curadas/perfit-base-maquinas.jpg",
        "use_cleany": False,
        "cta_pill": "www.starunion.com.ar",
        "copy_ig_fb": """¿Qué pasa cuando una máquina lavadora se detiene en medio de tu operación diaria?

En Star Union no dependemos de talleres externos ni de alquileres improvisados. Contamos con Taller Electromecánico Propio dentro de nuestra Base Operativa Central de 800 m² en calle Guaminí (CABA).

✔️ Mantenimiento preventivo in-house de autolavadoras, barredoras, lustradoras y aspiradoras industriales.
✔️ Cabina de arenado, pintura y banco de pruebas propio.
✔️ Flota de unidades móviles Ford Transit para reemplazo inmediato en tu objetivo.

Conocé nuestra infraestructura operativa en www.starunion.com.ar

#StarUnion #InfraestructuraPropia #FacilityServices #LimpiezaProfesional #OperacionesB2B #CABA""",
        "copy_linkedin": """Uno de los mayores costos ocultos al contratar servicios de limpieza B2B es la caída del servicio cuando se avería una máquina crítica en el objetivo.

Fundada en 2001 (con sede histórica inicial en calle Pergamino), Star Union S.R.L. centraliza hoy toda su logística en su Base Operativa Propia de 800 m² (3 niveles) en Guaminí 5657, CABA, donde desde fines de 2010 opera nuestro Taller Electromecánico In-House.

¿Qué significa esto para cada gerente de planta, operaciones o compras?
• Mantenimiento preventivo programado de todo el parque de maquinaria.
• Stock propio de repuestos y equipos de back-up listos para salir con nuestra flota de unidades Ford Transit.
• Trazabilidad completa bajo Norma ISO 9001:2015 (TÜV Rheinland).

👉 Recorré nuestra Base Operativa en: https://www.starunion.com.ar

#InfraestructuraB2B #ComprasCorporativas #FacilityManagement #MantenimientoOperativo #ISO9001 #StarUnion""",
        "yt_title": "Taller Electromecánico Propio y Base de 800 m² | Star Union S.R.L.",
        "yt_desc": """Por qué nuestra Base Operativa Propia de 800 m² en calle Guaminí (CABA) y nuestro Taller Electromecánico In-House garantizan cero interrupciones en tu empresa.

00:00 Parque de maquinaria propio y mantenimiento preventivo in-house
00:04 Stock permanente de insumos ANMAT y repuestos en 800 m²
00:08 Soporte logístico con flota propia Ford Transit en CABA y GBA

Conocé nuestra infraestructura en: https://www.starunion.com.ar""",
        "yt_tags": "star union, base operativa guamini, taller electromecanico limpieza, empresa de limpieza b2b, maquinaria de limpieza industrial, iso 9001 limpieza",
        "copy_wa": "Taller electromecánico propio en nuestra Base Operativa de 800 m² (Guaminí 5657, CABA): respaldo real para que las máquinas en tu empresa nunca se detengan. 👉 https://www.starunion.com.ar"
    },
    {
        "id": "03",
        "slug": "presentismo_biometrico",
        "day_label": "Publicación 3 · El Dato Técnico de Cleany (Presentismo Auditado)",
        "tag": "CONTROL BIOMÉTRICO · COBERTURA < 2 HORAS",
        "title": "Presentismo auditado en tiempo real y cobertura de ausencias en menos de 2 horas.",
        "subtitle": "Reloj biométrico conectado a nuestra central operativa: alerta automática a los 15 minutos y envío inmediato de personal de reemplazo.",
        "kpis": ["Alerta Automática 15 min", "Cobertura < 2 Horas", "Personal Registrado"],
        "photo": "../../assets/img/perfit-curadas/perfit-uniforme-oficial.jpg",
        "obj_pos": "center 65%",
        "use_cleany": True,
        "cleany_tip": "EL DATO TÉCNICO DE CLEANY: El sistema biométrico emite alerta a los 15 min y activa la guardia móvil antes de que afecte tu turno.",
        "cta_pill": "www.starunion.com.ar",
        "copy_ig_fb": """El Dato Técnico de Cleany: ¿Cómo aseguramos el 100% de los puestos cubiertos en cada turno?

En edificios corporativos, grandes consorcios, clínicas e industrias, una ausencia sin cubrir resiente toda la jornada. Por eso implementamos control biométrico conectado en tiempo real con nuestra mesa operativa:

✔️ Fichaje biométrico en el objetivo con alerta automática a los 15 minutos de tolerancia.
✔️ Activación inmediata de nuestra guardia operativa móvil.
✔️ Cobertura efectiva en menos de 2 horas con personal capacitado, uniformado y 100% registrado (ART y cargas sociales al día).

Consultá por nuestros abonos corporativos en www.starunion.com.ar

#StarUnion #ControlDePresentismo #GestionOperativa #ConsorciosCABA #EdificiosCorporativos #ISO9001""",
        "copy_linkedin": """La previsibilidad en el servicio de limpieza corporativa no depende de promesas comerciales, sino de sistemas de control en tiempo real.

En Star Union S.R.L. combinamos tecnología biométrica con capacidad de respuesta física:
• Cada ingreso se valida mediante reloj biométrico conectado a nuestra central en CABA.
• Ante cualquier demora superior a 15 minutos, el sistema dispara una alerta temprana a Supervisión.
• Nuestra flota móvil traslada personal de guardia capacitado y registrado para cubrir la posición en menos de 2 horas, eliminando el riesgo de puestos vacantes y garantizando indemnidad laboral total.

👉 Conocé nuestro sistema de trazabilidad operativa en: https://www.starunion.com.ar/

#RecursosHumanos #Operaciones #FacilityManagement #Consorcios #EdificiosCorporativos #ComplianceLaboral #StarUnion""",
        "yt_title": "Control Biométrico y Cobertura en < 2 Horas | El Dato Técnico de Cleany",
        "yt_desc": """Cómo funciona el sistema de control de presentismo biométrico en tiempo real de Star Union S.R.L. para garantizar puestos 100% cubiertos en cada turno.

00:00 Fichaje biométrico en tiempo real en cada objetivo
00:04 Alerta automática a los 15 minutos en nuestra central operativa
00:08 Cobertura en menos de 2 horas con personal registrado y flota propia

Solicitá una propuesta técnica en: https://www.starunion.com.ar/""",
        "yt_tags": "control biometrico limpieza, presentismo limpieza, empresa de limpieza caba, star union, consorcios caba, edificios corporativos limpieza",
        "copy_wa": "Presentismo auditado por reloj biométrico con alerta a los 15 min y cobertura en menos de 2 horas. Conocé cómo protegemos la continuidad de tu edificio o empresa 👉 https://www.starunion.com.ar/"
    },
    {
        "id": "04",
        "slug": "salud_laboratorios",
        "day_label": "Publicación 4 · Clínicas, Hospitales y Laboratorios",
        "tag": "SALUD Y LABORATORIOS · PROTOCOLOS ANMAT",
        "title": "Higiene técnica para clínicas, sanatorios y laboratorios de alta exigencia.",
        "subtitle": "Protocolos contra contaminación cruzada, insumos aprobados por ANMAT con hojas de seguridad (MSDS) y supervisión auditada bajo ISO 9001:2015.",
        "kpis": ["Insumos ANMAT + MSDS", "Cero Contaminación Cruzada", "ISO 9001:2015 TÜV"],
        "photo": "../../assets/img/perfit-curadas/perfit-salud-laboratorio.jpg",
        "use_cleany": False,
        "cta_pill": "www.starunion.com.ar",
        "copy_ig_fb": """En clínicas, centros de diagnóstico y laboratorios, la limpieza e higiene institucional exige rigor técnico verificable y trazabilidad documental.

✔️ Protocolos estrictos de zonificación por áreas críticas, semicríticas y comunes para evitar contaminación cruzada.
✔️ Insumos desinfectantes de grado profesional aprobados por ANMAT, con fichas técnicas y hojas de seguridad (MSDS) disponibles en el objetivo.
✔️ Procesos auditados bajo Norma ISO 9001:2015 por TÜV Rheinland.

Conocé nuestra división de Salud y Laboratorios en www.starunion.com.ar

#StarUnion #Salud #ClinicasYHospitales #Laboratorios #HigieneHospitalaria #ISO9001 #ANMAT""",
        "copy_linkedin": """La gestión de higiene en instituciones de salud, centros médicos y laboratorios farmacéuticos requiere estándares auditables en cada turno.

Desde nuestra división especializada en Salud y Laboratorios, en Star Union S.R.L. implementamos:
• Codificación estricta de elementos y paños por área para prevenir la contaminación cruzada.
• Utilización exclusiva de productos aprobados por ANMAT con documentación técnica y hojas de seguridad (MSDS) en carpeta de planta.
• Supervisión técnica periódica y auditoría de procesos certificada bajo Norma ISO 9001:2015 por TÜV Rheinland (Certipedia ID 9000041847).

👉 Consultá el protocolo técnico para instituciones médicas en: https://www.starunion.com.ar

#SaludArgentina #GestionHospitalaria #Laboratorios #Bioseguridad #ISO9001 #StarUnion""",
        "yt_title": "Higiene Técnica en Clínicas, Sanatorios y Laboratorios | Star Union",
        "yt_desc": """Protocolos de desinfección e higiene institucional para clínicas, hospitales, centros de diagnóstico y laboratorios bajo Norma ISO 9001:2015.

00:00 Zonificación técnica y prevención de contaminación cruzada
00:04 Insumos aprobados por ANMAT con hojas de seguridad (MSDS)
00:08 Supervisión auditada bajo ISO 9001:2015 (TÜV Rheinland)

Conocé más en: https://www.starunion.com.ar""",
        "yt_tags": "limpieza de clinicas, limpieza hospitalaria, limpieza de laboratorios, insumos anmat, iso 9001 salud, star union",
        "copy_wa": "Higiene técnica certificada ISO 9001:2015 para clínicas, sanatorios y laboratorios con insumos aprobados por ANMAT. 👉 https://www.starunion.com.ar"
    },
    {
        "id": "05",
        "slug": "universidades_clubes",
        "day_label": "Publicación 5 · Universidades, Colegios y Clubes Deportivos",
        "tag": "EDUCACIÓN Y DEPORTE · GRANDES PREDIOS",
        "title": "Mantenimiento integral de campus universitarios, colegios y clubes deportivos.",
        "subtitle": "Equipos sincronizados en contraturno y entre cambios de clase para aulas, auditorios, vestuarios y pisos deportivos de alto tránsito.",
        "kpis": ["Operación en Contraturno", "Cuidado de Parquet y Pisos", "Personal Identificado"],
        "photo": "../../assets/img/perfit-curadas/perfit-clubes-parquet.jpg",
        "use_cleany": False,
        "cta_pill": "www.starunion.com.ar",
        "copy_ig_fb": """Miles de personas circulan cada día por campus universitarios, colegios bilingües y clubes deportivos. Mantener cada espacio impecable sin interferir con las actividades académicas o deportivas requiere planificación milimétrica.

✔️ Operación en contraturno nocturno y guardias activas durante los cambios de turno.
✔️ Tratamiento específico para pisos deportivos de madera/parquet, gimnasios, vestuarios, comedores y aulas.
✔️ Personal capacitado en nuestra aula propia de formación, uniformado e identificado.

Conocé nuestras referencias en educación y deporte en www.starunion.com.ar

#StarUnion #Universidades #Colegios #ClubesDeportivos #InfraestructuraEducativa #LimpiezaProfesional""",
        "copy_linkedin": """¿Cómo se gestiona la higiene diaria de un campus universitario o un club deportivo donde circulan miles de personas por jornada?

En Star Union S.R.L. acompañamos a instituciones educativas y deportivas líderes (como Universidad Torcuato Di Tella, Asociación Escuelas Lincoln y Club de Amigos) con un esquema de doble capa operativa:

1. Guardia diurna de mantenimiento continuo en sanitarios, áreas comunes, comedores y vestuarios durante los picos de circulación.
2. Operativo intensivo en contraturno con maquinaria silenciosa para el tratamiento de pisos deportivos, aulas magnas, laboratorios y gimnasios.

👉 Conocé nuestras soluciones para instituciones educativas y clubes en: https://www.starunion.com.ar

#Educacion #Universidades #GestionDeportiva #FacilityManagement #ISO9001 #StarUnion""",
        "yt_title": "Limpieza Profesional en Universidades, Colegios y Clubes | Star Union",
        "yt_desc": """Gestión de higiene y mantenimiento en contraturno para grandes campus universitarios, colegios e instituciones deportivas en CABA y GBA.

00:00 Cuidado técnico de pisos deportivos de parquet y gimnasios
00:04 Operación sincronizada en aulas, laboratorios y vestuarios
00:08 Personal capacitado y procesos certificados ISO 9001:2015

Conocé más en: https://www.starunion.com.ar""",
        "yt_tags": "limpieza de universidades, limpieza de colegios, limpieza de clubes deportivos, mantenimiento de campus, star union",
        "copy_wa": "Mantenimiento integral en contraturno para universidades, colegios y clubes deportivos con certificación ISO 9001:2015. 👉 https://www.starunion.com.ar"
    }
]


def build_feed_html(post):
    cleany_block = ""
    if post["use_cleany"]:
        cleany_block = f"""
        <div style="margin-top:10px;background:#f9fafb;border:2px solid #03582d;border-radius:16px;padding:10px 16px;display:flex;align-items:center;gap:14px;">
            <img src="../../assets/img/cleany-hd.png" style="width:48px;height:48px;object-fit:contain;flex-shrink:0;" alt="Cleany">
            <div style="font-size:16px;line-height:1.32;color:#111827;font-weight:700;">
                {post["cleany_tip"]}
            </div>
        </div>
        """

    kpis_html = "".join([
        f'<span style="background:#f3f4f6;border:1px solid #e5e7eb;color:#133522;font-weight:800;font-size:16px;padding:8px 15px;border-radius:999px;">✓ {k}</span>'
        for k in post["kpis"]
    ])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    background: #ffffff;
    font-family: 'Open Sans', sans-serif;
    color: #111827;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 145px 72px 145px 72px; /* Safe Zone 4:5 Feed (145px arriba y 145px abajo para que la grilla 1:1 de IG jamás corte logo ni pie) */
  }}
</style>
</head>
<body>
  <!-- TOP HEADER (WHITE DOMINANT, INSIDE 1:1 GRID SAFE ZONE) -->
  <div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;padding-bottom:12px;border-bottom:4px solid #03582d;">
      <img src="../../assets/img/logo-star-union.png" style="height:60px;width:auto;object-fit:contain;" alt="Star Union">
      <div style="display:flex;align-items:center;gap:10px;background:#f9fafb;border:1px solid #e5e7eb;padding:8px 14px;border-radius:12px;">
        <img src="../../assets/img/tuv-iso-9001-badge.png" style="height:36px;width:auto;object-fit:contain;" alt="ISO 9001">
        <div style="text-align:left;">
          <div style="font-size:12px;font-weight:800;color:#03582d;letter-spacing:0.05em;">ISO 9001:2015</div>
          <div style="font-size:11px;color:#4b5563;font-weight:600;">TÜV Rheinland · ID 9000041847</div>
        </div>
      </div>
    </div>

    <div style="display:inline-block;background:rgba(3,88,45,0.09);color:#03582d;font-weight:800;font-size:14px;letter-spacing:0.07em;padding:6px 16px;border-radius:999px;margin-bottom:12px;">
      {post["tag"]}
    </div>

    <h1 style="font-size:38px;line-height:1.15;font-weight:800;color:#111827;letter-spacing:-0.02em;margin-bottom:12px;">
      {post["title"]}
    </h1>

    <p style="font-size:20px;line-height:1.38;color:#374151;font-weight:600;margin-bottom:14px;">
      {post["subtitle"]}
    </p>

    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px;">
      {kpis_html}
    </div>
    {cleany_block}
  </div>

  <!-- PHOTO FRAME (CLEAN, ZERO OVERLAY ON FACES/MACHINES) -->
  <div style="width:100%;height:{'380px' if post['use_cleany'] else '450px'};border-radius:22px;overflow:hidden;border:3px solid #03582d;background:#f9fafb;position:relative;box-shadow:0 12px 28px rgba(3,88,45,0.10);">
    <img src="{post['photo']}" style="width:100%;height:100%;object-fit:cover;object-position:{post.get('obj_pos', 'center 20%')};" alt="">
  </div>

  <!-- FOOTER BAR INSIDE 1:1 GRID SAFE ZONE -->
  <div style="display:flex;align-items:center;justify-content:space-between;padding-top:14px;border-top:2px solid #e5e7eb;">
    <div>
      <div style="font-size:16px;font-weight:800;color:#111827;">Star Union S.R.L. · Base Operativa Guaminí 5657, CABA</div>
      <div style="font-size:14px;font-weight:600;color:#4b5563;">WhatsApp Comercial B2B: +54 9 11 2275-9369 · 0810-333-8646</div>
    </div>
    <div style="background:#03582d;color:#ffffff;font-weight:800;font-size:16px;padding:11px 22px;border-radius:999px;border-bottom:3px solid #ffcc29;">
      {post["cta_pill"]}
    </div>
  </div>
</body>
</html>"""


def build_story_html(post):
    kpis_html = "".join([
        f'<div style="background:#f9fafb;border:1px solid #e5e7eb;color:#133522;font-weight:800;font-size:17px;padding:10px 14px;border-radius:12px;display:flex;align-items:center;gap:8px;"><span style="color:#03582d;font-size:19px;">✓</span> {k}</div>'
        for k in post["kpis"]
    ])

    return f"""<!DOCTYPE html>
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
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 250px 140px 420px 76px; /* Safe Zone Universal Reels/Shorts/Stories: 250px arriba, 420px abajo, 140px derecha, 76px izquierda */
  }}
</style>
</head>
<body>
  <div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding-bottom:12px;border-bottom:4px solid #03582d;">
      <img src="../../assets/img/logo-star-union.png" style="height:60px;width:auto;object-fit:contain;" alt="Star Union">
      <div style="display:flex;align-items:center;gap:10px;background:#f9fafb;border:1px solid #e5e7eb;padding:8px 14px;border-radius:12px;">
        <img src="../../assets/img/tuv-iso-9001-badge.png" style="height:36px;width:auto;object-fit:contain;" alt="ISO 9001">
        <div>
          <div style="font-size:12px;font-weight:800;color:#03582d;">ISO 9001:2015</div>
          <div style="font-size:11px;color:#4b5563;font-weight:700;">TÜV Rheinland</div>
        </div>
      </div>
    </div>

    <div style="display:inline-block;background:rgba(3,88,45,0.1);color:#03582d;font-weight:800;font-size:15px;letter-spacing:0.06em;padding:7px 16px;border-radius:999px;margin-bottom:14px;">
      {post["tag"]}
    </div>

    <h1 style="font-size:38px;line-height:1.15;font-weight:800;color:#111827;letter-spacing:-0.02em;margin-bottom:12px;">
      {post["title"]}
    </h1>

    <p style="font-size:21px;line-height:1.38;color:#374151;font-weight:600;margin-bottom:18px;">
      {post["subtitle"]}
    </p>
  </div>

  <!-- CLEAN PHOTO INSIDE SAFE ZONE -->
  <div style="width:100%;height:460px;border-radius:24px;overflow:hidden;border:3px solid #03582d;background:#f9fafb;box-shadow:0 14px 32px rgba(3,88,45,0.10);">
    <img src="{post['photo']}" style="width:100%;height:100%;object-fit:cover;object-position:{post.get('obj_pos', 'center 20%')};" alt="">
  </div>

  <!-- BOTTOM KPI & CTA INSIDE SAFE ZONE -->
  <div style="margin-top:16px;">
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;">
      {kpis_html}
    </div>
    <div style="background:#03582d;color:#ffffff;padding:18px 24px;border-radius:18px;display:flex;align-items:center;justify-content:space-between;border-bottom:4px solid #ffcc29;">
      <div>
        <div style="font-size:19px;font-weight:800;">Solicitá relevamiento técnico B2B</div>
        <div style="font-size:15px;color:#f3f4f6;font-weight:600;">WhatsApp: +54 9 11 2275-9369 · Guaminí 5657</div>
      </div>
      <div style="background:#ffffff;color:#03582d;font-weight:800;font-size:16px;padding:10px 18px;border-radius:999px;">
        {post["cta_pill"]}
      </div>
    </div>
  </div>
</body>
</html>"""


def render_screenshot(html_path, png_path, width, height):
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        f"file://{html_path}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def make_video_from_slides(slide_jpgs, out_mp4):
    # Create a 12-second 1080x1920 MP4 (4 seconds per slide) at 25fps WITH institutional audio track (male voice at start + Funk Groove)
    audio_path = os.path.join(BASE_DIR, "audio", "starunion_funk_firma_varon_12s.mp3")
    inputs = []
    filter_parts = []
    for i, jpg in enumerate(slide_jpgs):
        inputs.extend(["-loop", "1", "-t", "4", "-i", jpg])
        filter_parts.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=25,format=yuv420p[v{i}];")
    concat_inputs = "".join([f"[v{i}]" for i in range(len(slide_jpgs))])
    filter_complex = "".join(filter_parts) + f"{concat_inputs}concat=n={len(slide_jpgs)}:v=1:a=0[outv]"

    if os.path.exists(audio_path):
        inputs.extend(["-i", audio_path])
        audio_idx = len(slide_jpgs)
        cmd = [
            FFMPEG, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", f"{audio_idx}:a",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out_mp4
        ]
    else:
        cmd = [
            FFMPEG, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out_mp4
        ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    story_jpgs = []
    for post in POSTS:
        # 1. Feed 1080x1350
        feed_html = os.path.join(TMP_DIR, f"feed_{post['id']}.html")
        feed_png = os.path.join(TMP_DIR, f"feed_{post['id']}.png")
        feed_jpg = os.path.join(PIEZAS_DIR, f"{post['id']}_feed_{post['slug']}_1080x1350.jpg")
        with open(feed_html, "w", encoding="utf-8") as f:
            f.write(build_feed_html(post))
        render_screenshot(feed_html, feed_png, 1080, 1350)
        Image.open(feed_png).convert("RGB").save(feed_jpg, "JPEG", quality=94)

        # 2. Story / WhatsApp Status 1080x1920
        story_html = os.path.join(TMP_DIR, f"story_{post['id']}.html")
        story_png = os.path.join(TMP_DIR, f"story_{post['id']}.png")
        story_jpg = os.path.join(PIEZAS_DIR, f"{post['id']}_story_{post['slug']}_1080x1920.jpg")
        with open(story_html, "w", encoding="utf-8") as f:
            f.write(build_story_html(post))
        render_screenshot(story_html, story_png, 1080, 1920)
        Image.open(story_png).convert("RGB").save(story_jpg, "JPEG", quality=94)
        story_jpgs.append(story_jpg)

        post["feed_file"] = f"piezas/{post['id']}_feed_{post['slug']}_1080x1350.jpg"
        post["story_file"] = f"piezas/{post['id']}_story_{post['slug']}_1080x1920.jpg"

    # 3. Generate 2 YouTube Shorts / Reels (.mp4 1080x1920)
    short1_mp4 = os.path.join(PIEZAS_DIR, "short_01_infraestructura_y_presentismo_1080x1920.mp4")
    short2_mp4 = os.path.join(PIEZAS_DIR, "short_02_verticales_iso9001_1080x1920.mp4")
    make_video_from_slides([story_jpgs[0], story_jpgs[1], story_jpgs[2]], short1_mp4)
    make_video_from_slides([story_jpgs[0], story_jpgs[3], story_jpgs[4]], short2_mp4)

    # 4. Build interactive index.html for Ariana (1-click Download + 1-click Copy)
    cards_html = ""
    for p in POSTS:
        cards_html += f"""
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div class="bg-gray-50 px-6 py-4 border-b border-gray-200 flex flex-wrap items-center justify-between gap-3">
            <div>
              <span class="text-xs font-extrabold uppercase tracking-wider text-[#03582d]">{p['day_label']}</span>
              <h2 class="text-lg font-extrabold text-gray-900 mt-0.5">{p['title']}</h2>
            </div>
            <div class="flex flex-wrap gap-2">
              <a href="{p['feed_file']}" download class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2.5 rounded-lg transition">
                ⬇ Descargar Feed 4:5 (1080×1350 JPG)
              </a>
              <a href="{p['story_file']}" download class="bg-[#111827] hover:bg-black text-white text-xs font-extrabold px-4 py-2.5 rounded-lg transition">
                ⬇ Descargar Story / Estado WA (1080×1920 JPG)
              </a>
            </div>
          </div>

          <div class="p-6 grid lg:grid-cols-12 gap-6 items-start">
            <!-- PREVIEWS -->
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

            <!-- COPIES LISTOS CON BOTÓN COPIAR EN 1 CLIC -->
            <div class="lg:col-span-7 space-y-4">
              <!-- IG / FB -->
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-extrabold uppercase text-[#03582d]">📸 Copy Instagram y Facebook (Canva / Adobe / Meta Suite)</span>
                  <button onclick="copyText('ig_{p['id']}', this)" class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1.5 rounded-lg">📋 Copiar Copy IG/FB</button>
                </div>
                <pre id="ig_{p['id']}" class="text-xs text-gray-800 whitespace-pre-wrap font-sans leading-relaxed">{p['copy_ig_fb']}</pre>
              </div>

              <!-- LINKEDIN -->
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-extrabold uppercase text-gray-900">💼 Copy LinkedIn B2B (Formato Corporativo)</span>
                  <button onclick="copyText('li_{p['id']}', this)" class="bg-[#111827] text-white text-xs font-extrabold px-3 py-1.5 rounded-lg">📋 Copiar Copy LinkedIn</button>
                </div>
                <pre id="li_{p['id']}" class="text-xs text-gray-800 whitespace-pre-wrap font-sans leading-relaxed">{p['copy_linkedin']}</pre>
              </div>

              <!-- YOUTUBE SHORTS (TÍTULO + DESCRIPCIÓN + TAGS) -->
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200 space-y-2">
                <div class="text-xs font-extrabold uppercase text-[#03582d]">▶️ Pack YouTube Shorts (Título + Descripción con Timestamps + Etiquetas)</div>
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
                  <div class="text-xs"><strong class="text-gray-600">Tags (pegar en etiquetas):</strong> <span id="yttags_{p['id']}" class="text-gray-800">{p['yt_tags']}</span></div>
                  <button onclick="copyText('yttags_{p['id']}', this)" class="bg-gray-200 hover:bg-gray-300 text-gray-900 text-[11px] font-bold px-2.5 py-1 rounded shrink-0">📋 Copiar Tags</button>
                </div>
              </div>

              <!-- ESTADO WHATSAPP -->
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-200 flex items-center justify-between gap-3">
                <div class="text-xs text-gray-800"><strong class="text-[#03582d] uppercase block mb-0.5">📲 Pie para Estado de WhatsApp:</strong><span id="wa_{p['id']}">{p['copy_wa']}</span></div>
                <button onclick="copyText('wa_{p['id']}', this)" class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1.5 rounded-lg shrink-0">📋 Copiar Texto WA</button>
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
  <title>Pack de Redes Sociales + YouTube Shorts + Embudo Perfit | Star Union S.R.L.</title>
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
            Listo para Publicar · 10 Piezas JPG + 2 Videos MP4 + Copies en 1 Clic
          </span>
          <h1 class="text-xl sm:text-2xl font-extrabold text-gray-900">Central de Redes Sociales, Shorts y Embudo Perfit — Star Union S.R.L.</h1>
          <p class="text-xs text-gray-600 mt-0.5">Diseñado con Blanco Dominante (85%), Verde Star Union (#03582D), fotos reales curadas y cero texto pisando caras o máquinas.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2">
        <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2.5 rounded-lg transition">
          📊 Ver Informe Perfit (21 Campañas + Embudo + Calendario)
        </a>
        <a href="../accesos/index.html" class="bg-gray-100 hover:bg-gray-200 text-gray-900 text-xs font-extrabold px-4 py-2.5 rounded-lg transition">
          ← Linktree Star Union
        </a>
      </div>
    </div>

    <!-- VIDEOS MP4 SHORTS / REELS LISTOS PARA DESCARGAR -->
    <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
        <div>
          <span class="text-xs font-extrabold uppercase text-[#03582d]">Videos Verticales 9:16 (1080×1920 MP4) · YouTube Shorts, IG Reels y Estados</span>
          <h2 class="text-lg font-extrabold text-gray-900">2 Videos .MP4 Ya Renderizados Listos para Subir</h2>
        </div>
      </div>
      <div class="grid md:grid-cols-2 gap-6">
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 flex flex-col sm:flex-row items-center gap-4">
          <video src="piezas/short_01_infraestructura_y_presentismo_1080x1920.mp4" controls class="w-40 rounded-lg border border-gray-300 shadow-sm"></video>
          <div class="space-y-2">
            <h3 class="font-extrabold text-sm text-gray-900">Short #1: Infraestructura 800 m² Guaminí + Taller Propio + Presentismo Biométrico</h3>
            <p class="text-xs text-gray-600">Formato 1080×1920 H.264 MP4 (12 seg). Ideal para YouTube Shorts, Reels de Instagram y LinkedIn Video.</p>
            <a href="piezas/short_01_infraestructura_y_presentismo_1080x1920.mp4" download class="inline-block bg-[#03582d] text-white text-xs font-extrabold px-4 py-2 rounded-lg">
              ⬇ Descargar Video Short #1 (.MP4)
            </a>
          </div>
        </div>
        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 flex flex-col sm:flex-row items-center gap-4">
          <video src="piezas/short_02_verticales_iso9001_1080x1920.mp4" controls class="w-40 rounded-lg border border-gray-300 shadow-sm"></video>
          <div class="space-y-2">
            <h3 class="font-extrabold text-sm text-gray-900">Short #2: Verticales de Alta Exigencia (Logística, Salud ANMAT y Educación) · ISO 9001</h3>
            <p class="text-xs text-gray-600">Formato 1080×1920 H.264 MP4 (12 seg). Ideal para YouTube Shorts, Reels y Estados de WhatsApp.</p>
            <a href="piezas/short_02_verticales_iso9001_1080x1920.mp4" download class="inline-block bg-[#03582d] text-white text-xs font-extrabold px-4 py-2 rounded-lg">
              ⬇ Descargar Video Short #2 (.MP4)
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- LAS 5 PUBLICACIONES COMPLETAS -->
    <div class="space-y-6">
      {cards_html}
    </div>
  </div>

  <script>
    function copyText(id, btn) {{
      const el = document.getElementById(id);
      navigator.clipboard.writeText(el.innerText);
      const old = btn.innerText;
      btn.innerText = '✅ ¡Copiado!';
      setTimeout(() => btn.innerText = old, 1800);
    }}
  </script>
</body>
</html>"""

    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)

    print("Generated all 10 JPGs, 2 MP4 Shorts, and redes-sociales/index.html successfully.")

if __name__ == "__main__":
    main()
