#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de:
1) Circuito Comercial y Funnel de Captación y Ventas B2B 2027 (Con CRM Simulado para Star Union usando las herramientas reales disponibles: Perfit API + Landings con CTA de 1 clic + Planilla Viva de Seguimiento Comercial + WhatsApp B2B).
2) Plantillas HTML Opción A y Opción B con las 7 correcciones exactas de Ariana:
   - Zonas Operativas visibles arriba, en barra central y en el footer (CABA · GBA Norte, Oeste y Sur · La Plata · Bahía Blanca · Neuquén · Trelew) separadas de los "+25 años de trayectoria".
   - Sello TÜV Rheinland ISO 9001:2015 (ID 9000041847) fijo y jerarquizado arriba en A y B.
   - 2 Asuntos por cada plantilla (Asunto 1 de Envío Inicial + Asunto 2 de Reenvío a No-Abridores a los +5 días), basados en el ranking real de las 93 campañas de Perfit (#110 72% open, #102 65% open, #114/#117 +21,8% extra).
   - Footer con peso visual real (borde superior doble #03582D + #FFCC29, franja verde oscura institucional #133522 para la firma, sombra y pastillas enmarcadas, cero aspecto lavado y cero azul marino).
   - Botones de cada sector en Opción A y Opción B bien centrados, sin texto cortado ni "propuesta a medida imposible": llevan a la Landing / Ficha de ese rubro con CTA directo de 1 clic + botón directo a WhatsApp.
"""
import os
import html as html_mod

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"
OUT_DIR = os.path.join(BASE_DIR, "redes-sociales")

LOGO_URL = "https://cdn.myperfit.net/1726860404581-logo-horizontal-1200x300.png"
TUV_URL = "https://cdn.myperfit.net/1775508730335-TR-Testmark_9000041847_EN_CMYK_with-QR-Code.png"
CLEANY_URL = "https://wajntraub.ar/staruniontest/assets/img/cleany-hd.png"
IMG_LOGISTICA = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-logistica-pallets.jpg"
IMG_TALLER = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-base-maquinas.jpg"
IMG_BIOMETRICO = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-uniforme-oficial.jpg"
IMG_SALUD = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-salud-laboratorio.jpg"
IMG_CLUBES = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-clubes-parquet.jpg"

# Landings específicas de cada rubro con UTM de autosegmentación para Perfit (detecta nombre, apellido y empresa del clic)
LANDING_LOGISTICA = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=fabricas&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=logistica_industria"
LANDING_OFICINAS = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=oficinas&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=oficinas_corporativas"
LANDING_CONSORCIOS = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=consorcios&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=consorcios_edificios"
LANDING_SALUD = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=clinicas&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=salud_laboratorios"
LANDING_EDUCACION = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=universidades&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=educacion_clubes"

# Links Directos a WhatsApp Comercial B2B (+54 9 11 2275-9369)
WA_GENERAL = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20vi%20su%20comunicaci%C3%B3n%20y%20quiero%20coordinar%20un%20relevamiento%20t%C3%A9cnico%20para%20cotizar%20nuestras%20instalaciones."
WA_LOGISTICA = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20cotizar%20el%20servicio%20de%20limpieza%20para%20nuestra%20planta%20o%20centro%20log%C3%ADstico."
WA_OFICINAS = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20cotizar%20el%20servicio%20de%20limpieza%20para%20nuestras%20oficinas%20o%20edificio%20corporativo."
WA_CONSORCIOS = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20cotizar%20el%20servicio%20de%20limpieza%20para%20nuestro%20consorcio%20o%20barrio%20cerrado."
WA_SALUD = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20cotizar%20el%20servicio%20de%20higiene%20t%C3%A9cnica%20para%20nuestra%20cl%C3%ADnica%20o%20laboratorio."
WA_EDUCACION = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20cotizar%20el%20mantenimiento%20integral%20para%20nuestra%20universidad%2C%20colegio%20o%20club."


def build_shared_top_header(utm_tag):
    """
    Cabezal Fijo idéntico en Opción A y Opción B:
    1. Barra Superior con Antigüedad (+25 años de trayectoria) separada de la franja de Zonas Operativas reales.
    2. Cabezal con Logo Star Union + Sello TÜV Rheinland ISO 9001:2015 (ID 9000041847) grande y enmarcado.
    """
    return f"""
          <!-- BARRA SUPERIOR 1: TRAYECTORIA REAL -->
          <tr>
            <td style="background-color:#03582D;padding:9px 20px;text-align:center;color:#FFFFFF;border-bottom:2px solid #FFCC29;">
              <div style="font-size:11px;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;">
                ⭐ +25 AÑOS DE TRAYECTORIA EN LIMPIEZA PROFESIONAL, INDUSTRIAL E INSTITUCIONAL
              </div>
            </td>
          </tr>

          <!-- BARRA SUPERIOR 2: ZONAS OPERATIVAS REALES (DESTACADAS Y SEPARADAS DE LA FECHA DE FUNDACIÓN) -->
          <tr>
            <td style="background-color:#E6EFEA;padding:8px 18px;text-align:center;border-bottom:1px solid #C6DDD0;">
              <div style="font-size:11px;font-weight:800;color:#133522;line-height:1.4;">
                📍 ZONAS OPERATIVAS ACTIVAS: <span style="color:#03582D;">CABA · GBA (Norte, Oeste y Sur) · La Plata · Bahía Blanca · Neuquén · Trelew</span>
              </div>
            </td>
          </tr>

          <!-- ENCABEZADO FIJO: LOGO STAR UNION + SELLO TÜV RHEINLAND ISO 9001 JERARQUIZADO -->
          <tr>
            <td style="padding:20px 26px 18px 26px;border-bottom:3px solid #03582D;background-color:#FFFFFF;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" width="46%">
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign={utm_tag}" target="_blank">
                      <img src="{LOGO_URL}" alt="Star Union" width="185" style="display:block;max-width:185px;height:auto;border:0;">
                    </a>
                  </td>
                  <td align="right" valign="middle" width="54%">
                    <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="text-decoration:none;display:inline-block;">
                      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:2px solid #03582D;border-radius:12px;padding:8px 12px;box-shadow:0 2px 6px rgba(3,88,45,0.10);">
                        <tr>
                          <td valign="middle" style="padding-right:10px;">
                            <img src="{TUV_URL}" alt="TÜV Rheinland ISO 9001:2015" width="46" style="display:block;border:0;">
                          </td>
                          <td align="left" valign="middle" style="font-size:11px;line-height:1.32;color:#133522;">
                            <strong style="color:#03582D;font-size:12px;display:block;letter-spacing:0.02em;">CERTIFICACIÓN ISO 9001:2015</strong>
                            <span style="color:#374151;font-weight:700;display:block;">TÜV Rheinland · ID 9000041847</span>
                            <span style="color:#03582D;font-size:10px;font-weight:800;text-decoration:underline;">Verificar certificado oficial ↗</span>
                          </td>
                        </tr>
                      </table>
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
    """


def build_shared_footer(utm_tag):
    """
    Footer con cuerpo, estructura visual, filete amarillo #FFCC29, cabecera de cierre en Verde Institucional (#03582D / #133522)
    y bloque inferior enmarcado con sombra y pastillas (cero aspecto lavado y cero azul marino).
    """
    return f"""
          <!-- PIE INSTITUCIONAL CON PESO VISUAL Y SEPARACIÓN CLARA (VERDE STAR UNION + FILETE AMARILLO + CAJA ENMARCADA) -->
          <tr>
            <td style="background-color:#03582D;border-top:4px solid #FFCC29;padding:18px 26px;text-align:center;color:#FFFFFF;">
              <div style="font-size:16px;font-weight:800;letter-spacing:0.02em;margin-bottom:4px;">
                Star Union · Sabemos de Limpieza
              </div>
              <div style="font-size:12px;color:#E6EFEA;font-weight:600;">
                Base Operativa Central Propia (800 m²): Guaminí 5657, CABA · Atención Comercial: <strong>0810-333-8646</strong> · WhatsApp B2B: <strong>+54 9 11 2275-9369</strong>
              </div>
            </td>
          </tr>
          <tr>
            <td style="background-color:#E6EFEA;border-top:1px solid #C6DDD0;border-bottom:2px solid #03582D;padding:18px 26px;text-align:center;">
              <div style="background-color:#FFFFFF;border:1.5px solid #03582D;border-radius:12px;padding:12px 14px;margin-bottom:14px;box-shadow:0 3px 8px rgba(3,88,45,0.08);">
                <div style="font-size:11px;font-weight:800;color:#03582D;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">
                  📍 Cobertura Regional con Supervisión Propia
                </div>
                <div style="font-size:12px;font-weight:700;color:#133522;">
                  CABA &nbsp;·&nbsp; GBA Norte, Oeste y Sur &nbsp;·&nbsp; La Plata &nbsp;·&nbsp; Bahía Blanca &nbsp;·&nbsp; Neuquén &nbsp;·&nbsp; Trelew
                </div>
              </div>

              <div style="margin-bottom:14px;">
                <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign={utm_tag}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:7px 14px;border-radius:999px;margin:3px;">🌐 Sitio Web Oficial</a>
                <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="display:inline-block;background-color:#FFFFFF;border:1px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:6px 13px;border-radius:999px;margin:3px;">🏅 Certificado TÜV ISO 9001</a>
                <a href="https://www.instagram.com/starunionservicios/" target="_blank" style="display:inline-block;background-color:#FFFFFF;border:1px solid #03582D;color:#133522;font-size:11px;font-weight:700;text-decoration:none;padding:6px 13px;border-radius:999px;margin:3px;">Instagram</a>
                <a href="https://www.linkedin.com/company/star-union-srl/" target="_blank" style="display:inline-block;background-color:#FFFFFF;border:1px solid #03582D;color:#133522;font-size:11px;font-weight:700;text-decoration:none;padding:6px 13px;border-radius:999px;margin:3px;">LinkedIn</a>
              </div>

              <div style="font-size:11px;color:#374151;line-height:1.45;border-top:1px solid #C6DDD0;padding-top:10px;">
                Recibís esta comunicación institucional por formar parte de nuestra red de contactos corporativos.<br>
                Si deseás dejar de recibir novedades, podés <a href="{{{{unsubscribe_link}}}}" style="color:#03582D;font-weight:800;text-decoration:underline;">desuscribirte en 1 clic aquí</a>.
              </div>
            </td>
          </tr>
    """


def build_template_a():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Continuidad Operativa e Infraestructura Propia | Star Union</title>
</head>
<body style="margin:0;padding:0;background-color:#F3F4F6;font-family:'Open Sans',Arial,Helvetica,sans-serif;color:#133522;-webkit-font-smoothing:antialiased;">
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    +25 años de trayectoria · Base Propia de 800 m² en CABA, Taller In-House, presentismo biométrico (&lt; 2 hs) y cobertura en CABA, GBA, La Plata, Bahía Blanca, Neuquén y Trelew.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F3F4F6;padding:24px 10px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:16px;overflow:hidden;border:2px solid #03582D;box-shadow:0 8px 24px rgba(3,88,45,0.08);">
          
          {build_shared_top_header("funnel1_apertura_A")}

          <!-- BLOQUE HERO GENERAL (APERTURA DE EMBUDO 1) -->
          <tr>
            <td style="padding:26px 28px 16px 28px;background-color:#FFFFFF;">
              <div style="display:inline-block;background-color:#E6EFEA;color:#03582D;font-size:11px;font-weight:800;padding:5px 12px;border-radius:999px;letter-spacing:0.05em;margin-bottom:12px;">
                INFRAESTRUCTURA PROPIA Y TRAZABILIDAD OPERATIVA B2B
              </div>
              <h1 style="margin:0 0 12px 0;font-size:24px;line-height:1.22;font-weight:800;color:#133522;">
                Continuidad operativa respaldada por estructura propia de 800 m², taller in-house y control biométrico en tiempo real.
              </h1>
              <p style="margin:0 0 18px 0;font-size:15px;line-height:1.55;color:#374151;">
                En <strong>Star Union</strong> estructuramos cada servicio para que la higiene técnica de tu planta, edificio, clínica o institución funcione con precisión auditable todos los días del año:
              </p>

              <!-- 3 PILARES VERIFICABLES -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:18px;">
                <tr>
                  <td width="32%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#03582D;">800 m²</div>
                    <div style="font-size:11px;color:#374151;font-weight:700;margin-top:3px;">Base Propia en Guaminí 5657 (CABA)</div>
                  </td>
                  <td width="2%"></td>
                  <td width="32%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#03582D;">&lt; 2 Horas</div>
                    <div style="font-size:11px;color:#374151;font-weight:700;margin-top:3px;">Cobertura Biométrica con Guardia Móvil</div>
                  </td>
                  <td width="2%"></td>
                  <td width="32%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#03582D;">In-House</div>
                    <div style="font-size:11px;color:#374151;font-weight:700;margin-top:3px;">Taller Propio y Reemplazo en el Día</div>
                  </td>
                </tr>
              </table>

              <!-- BOTÓN PRINCIPAL WHATSAPP COMERCIAL -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center" style="padding:4px 0 8px 0;">
                    <a href="{WA_GENERAL}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:14px;font-weight:800;text-decoration:none;padding:14px 26px;border-radius:999px;border-bottom:3px solid #FFCC29;">
                      📲 Coordinar Relevamiento Técnico por WhatsApp
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SEPARADOR SECCIÓN AUTO-SEGMENTADORA POR VERTICAL -->
          <tr>
            <td style="padding:10px 28px 6px 28px;background-color:#FFFFFF;">
              <div style="border-top:2px solid #E5E7EB;padding-top:18px;">
                <div style="font-size:12px;font-weight:800;color:#03582D;text-transform:uppercase;letter-spacing:0.05em;">
                  ELEGÍ TU RUBRO PARA VER LA LANDING ESPECÍFICA O COTIZAR DIRECTO
                </div>
                <h2 style="margin:4px 0 12px 0;font-size:18px;font-weight:800;color:#133522;">
                  Equipamiento y protocolos diseñados para cada operación:
                </h2>
              </div>
            </td>
          </tr>

          <!-- VERTICAL 1: LOGÍSTICA E INDUSTRIA -->
          <tr>
            <td style="padding:8px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:14px;overflow:hidden;">
                <tr>
                  <td style="padding:0;">
                    <a href="{LANDING_LOGISTICA}" target="_blank">
                      <img src="{IMG_LOGISTICA}" alt="Logística e Industria" width="544" style="display:block;width:100%;max-width:544px;height:210px;object-fit:cover;border:0;">
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 20px;">
                    <div style="font-size:11px;font-weight:800;color:#03582D;letter-spacing:0.05em;">1. CENTROS LOGÍSTICOS, DEPÓSITOS Y PLANTAS INDUSTRIALES</div>
                    <h3 style="margin:4px 0 8px 0;font-size:17px;font-weight:800;color:#133522;">Fregado y barrido mecanizado sin detener el despacho</h3>
                    <p style="margin:0 0 14px 0;font-size:13px;line-height:1.5;color:#374151;">
                      Autolavadoras hombre a bordo, barredoras industriales y respaldo de nuestro Taller Electromecánico Propio en Guaminí 5657 para reemplazo de equipos en el día.
                    </p>
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td width="56%" style="padding-right:6px;">
                          <a href="{LANDING_LOGISTICA}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:12px;font-weight:800;text-decoration:none;padding:10px 12px;border-radius:8px;">
                            📄 Ver Landing y Ficha Industrial →
                          </a>
                        </td>
                        <td width="44%" style="padding-left:6px;">
                          <a href="{WA_LOGISTICA}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:12px;font-weight:800;text-decoration:none;padding:9px 12px;border-radius:8px;">
                            📲 Cotizar por WhatsApp
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- VERTICAL 2 Y 3 EN DOBLE COLUMNA: OFICINAS + CONSORCIOS -->
          <tr>
            <td style="padding:8px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <!-- OFICINAS -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:14px;overflow:hidden;">
                    <a href="{LANDING_OFICINAS}" target="_blank">
                      <img src="{IMG_BIOMETRICO}" alt="Oficinas y Edificios Corporativos" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">2. OFICINAS Y CORPORATIVOS</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Edificios corporativos, bancos y sedes</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Presentismo validado por reloj biométrico, personal registrado (indemnidad Art. 30 LCT) y supervisión constante.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{LANDING_OFICINAS}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:9px 10px;border-radius:8px;">
                          📄 Ver Landing Oficinas →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_OFICINAS}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
                          📲 Cotizar por WhatsApp
                        </a>
                      </div>
                    </div>
                  </td>
                  <td width="4%"></td>
                  <!-- CONSORCIOS -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:14px;overflow:hidden;">
                    <a href="{LANDING_CONSORCIOS}" target="_blank">
                      <img src="{IMG_TALLER}" alt="Consorcios y Barrios Cerrados" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">3. CONSORCIOS Y TORRES</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Grandes consorcios y barrios cerrados</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Cobertura de ausencias en menos de 2 horas con guardia móvil propia para que ningún turno quede sin cubrir.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{LANDING_CONSORCIOS}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:9px 10px;border-radius:8px;">
                          📄 Ver Landing Consorcios →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_CONSORCIOS}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
                          📲 Cotizar por WhatsApp
                        </a>
                      </div>
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- VERTICAL 4 Y 5 EN DOBLE COLUMNA: SALUD ANMAT + UNIVERSIDADES/CLUBES -->
          <tr>
            <td style="padding:8px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <!-- SALUD -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:14px;overflow:hidden;">
                    <a href="{LANDING_SALUD}" target="_blank">
                      <img src="{IMG_SALUD}" alt="Clínicas y Laboratorios" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">4. SALUD Y LABORATORIOS</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Clínicas, sanatorios y laboratorios</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Zonificación contra contaminación cruzada e insumos aprobados por ANMAT con hojas de seguridad (MSDS) en planta.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{LANDING_SALUD}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:9px 10px;border-radius:8px;">
                          📄 Ver Landing Salud / ANMAT →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_SALUD}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
                          📲 Cotizar por WhatsApp
                        </a>
                      </div>
                    </div>
                  </td>
                  <td width="4%"></td>
                  <!-- EDUCACIÓN Y CLUBES -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:14px;overflow:hidden;">
                    <a href="{LANDING_EDUCACION}" target="_blank">
                      <img src="{IMG_CLUBES}" alt="Universidades, Colegios y Clubes" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">5. EDUCACIÓN Y DEPORTE</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Universidades, colegios y clubes</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Operativos en contraturno, cuidado de pisos deportivos de parquet y preparación para receso y temporada de verano.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{LANDING_EDUCACION}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:9px 10px;border-radius:8px;">
                          📄 Ver Landing Educación/Clubes →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_EDUCACION}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
                          📲 Cotizar por WhatsApp
                        </a>
                      </div>
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- EL DATO TÉCNICO DE CLEANY (SELLO DE AUTORIDAD TÉCNICA) -->
          <tr>
            <td style="padding:16px 28px 22px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:2px solid #03582D;border-radius:14px;padding:16px;">
                <tr>
                  <td width="64" valign="middle" style="padding-right:14px;">
                    <img src="{CLEANY_URL}" alt="Cleany" width="56" style="display:block;border:0;">
                  </td>
                  <td valign="middle" style="font-size:13px;line-height:1.48;color:#133522;">
                    <strong style="color:#03582D;display:block;font-size:12px;letter-spacing:0.04em;">EL DATO TÉCNICO DE CLEANY · TRAZABILIDAD BIOMÉTRICA</strong>
                    Nuestro sistema de reloj biométrico reporta en vivo a la central de calle Guaminí: ante cualquier demora a los <strong>15 minutos</strong> del inicio de turno, se despacha personal de guardia registrado para cubrir el puesto en <strong>menos de 2 horas</strong>.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          {build_shared_footer("funnel1_apertura_A")}

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_template_b():
    """
    OPCIÓN B: Ejecutiva de Auditoría, Continuidad y Recambio de Proveedor.
    Cada uno de los 5 rubros tiene sus botones 100% centrados, anchos y legibles, llevando a:
    1) La Landing específica del rubro (con CTA directo de 1 clic adentro y registro del clic en Perfit).
    2) El WhatsApp Comercial B2B directo.
    """
    rows_data = [
        ("🏭 1. Centros Logísticos, Depósitos y Plantas Industriales", "Autolavadoras hombre a bordo, barredoras y taller propio en CABA.", LANDING_LOGISTICA, WA_LOGISTICA),
        ("🏢 2. Oficinas Corporativas, Bancos y Centros Comerciales", "Control biométrico en tiempo real e indemnidad laboral Art. 30 LCT.", LANDING_OFICINAS, WA_OFICINAS),
        ("🏙️ 3. Grandes Consorcios, Torres y Barrios Cerrados", "Cobertura de ausencias en menos de 2 horas con guardia móvil propia.", LANDING_CONSORCIOS, WA_CONSORCIOS),
        ("🏥 4. Clínicas, Sanatorios y Laboratorios (Protocolo ANMAT)", "Prevención de contaminación cruzada e insumos ANMAT con hojas MSDS.", LANDING_SALUD, WA_SALUD),
        ("🎓 5. Universidades, Colegios Bilingües y Clubes Deportivos", "Operación sincronizada en contraturno y cuidado de pisos deportivos.", LANDING_EDUCACION, WA_EDUCACION),
    ]

    sector_rows_html = ""
    for title, desc, landing_url, wa_url in rows_data:
        sector_rows_html += f"""
                <tr>
                  <td style="padding:6px 0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-left:5px solid #03582D;border-radius:12px;padding:14px 16px;">
                      <tr>
                        <td colspan="2" style="padding-bottom:10px;">
                          <div style="font-size:14px;font-weight:800;color:#133522;line-height:1.25;">{title}</div>
                          <div style="font-size:12px;color:#374151;margin-top:3px;line-height:1.4;">{desc}</div>
                        </td>
                      </tr>
                      <tr>
                        <td width="54%" align="center" style="padding-right:6px;">
                          <a href="{landing_url}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:12px;font-weight:800;text-decoration:none;padding:9px 10px;border-radius:8px;">
                            📄 Ver Landing del Sector →
                          </a>
                        </td>
                        <td width="46%" align="center" style="padding-left:6px;">
                          <a href="{wa_url}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:12px;font-weight:800;text-decoration:none;padding:8px 10px;border-radius:8px;">
                            📲 Cotizar por WhatsApp
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auditoría Operativa y Continuidad del Servicio de Limpieza | Star Union</title>
</head>
<body style="margin:0;padding:0;background-color:#F3F4F6;font-family:'Open Sans',Arial,Helvetica,sans-serif;color:#133522;-webkit-font-smoothing:antialiased;">
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    +25 años de trayectoria · Cómo eliminar puestos vacíos, paradas por maquinaria caída y riesgos laborales solidarios (Art. 30 LCT) con certificación ISO 9001:2015.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F3F4F6;padding:24px 10px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:16px;overflow:hidden;border:2px solid #03582D;box-shadow:0 8px 24px rgba(3,88,45,0.08);">

          {build_shared_top_header("funnel1_apertura_B")}

          <!-- APERTURA EJECUTIVA DE DIAGNÓSTICO B2B -->
          <tr>
            <td style="padding:26px 28px 14px 28px;background-color:#FFFFFF;">
              <div style="display:inline-block;background-color:#E6EFEA;color:#03582D;font-size:11px;font-weight:800;padding:5px 12px;border-radius:999px;letter-spacing:0.05em;margin-bottom:12px;">
                DIAGNÓSTICO DE PROVEEDORES Y PREVISIBILIDAD OPERATIVA
              </div>
              <h1 style="margin:0 0 12px 0;font-size:23px;line-height:1.24;font-weight:800;color:#133522;">
                ¿Tu operación está protegida hoy frente a los 4 riesgos más frecuentes en servicios de limpieza?
              </h1>
              <p style="margin:0 0 16px 0;font-size:15px;line-height:1.55;color:#374151;">
                Al evaluar o renovar el servicio de higiene en una planta industrial, edificio corporativo, consorcio, clínica o institución educativa, la diferencia real está en el respaldo físico detrás de cada turno:
              </p>
            </td>
          </tr>

          <!-- MATRIZ DE LOS 4 RIESGOS RESUELTOS POR STAR UNION -->
          <tr>
            <td style="padding:0 28px 16px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1.5px solid #03582D;border-radius:12px;overflow:hidden;">
                <tr style="background-color:#03582D;color:#FFFFFF;font-size:12px;font-weight:800;">
                  <td width="42%" style="padding:10px 14px;">Riesgo Operativo Habitual</td>
                  <td width="58%" style="padding:10px 14px;">Protocolo Auditado Star Union</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;background-color:#FFFFFF;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#133522;">1. Puestos vacíos por ausencias imprevistas</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Reloj biométrico en tiempo real:</strong> alerta a los 15 min y cobertura en <strong>menos de 2 horas</strong> con guardia móvil propia.</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;background-color:#F9FAFB;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#133522;">2. Servicio frenado por máquinas averiadas</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Taller Electromecánico Propio (800 m² CABA):</strong> mantenimiento preventivo y reemplazo de equipos en el día.</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;background-color:#FFFFFF;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#133522;">3. Contingencia laboral solidaria (Art. 30 LCT)</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Indemnidad documental:</strong> 100% del personal en relación de dependencia con entrega mensual de F.931, ART y seguros.</td>
                </tr>
                <tr style="background-color:#F9FAFB;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#133522;">4. Desvíos en auditorías de calidad o salud</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Norma ISO 9001:2015 (TÜV Rheinland)</strong> + insumos aprobados por ANMAT con hojas de seguridad (MSDS).</td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- FOTO REAL DE RESPALDO: BASE GUAMINÍ Y TALLER PROPIO -->
          <tr>
            <td style="padding:4px 28px 18px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1.5px solid #C6DDD0;border-radius:14px;overflow:hidden;">
                <tr>
                  <td>
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_B&vertical=infraestructura_guamini" target="_blank">
                      <img src="{IMG_TALLER}" alt="Base Operativa Propia de 800 m² en Guaminí 5657, CABA" width="544" style="display:block;width:100%;max-width:544px;height:200px;object-fit:cover;border:0;">
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:14px 18px;font-size:13px;line-height:1.48;color:#374151;">
                    <strong style="color:#133522;">Respaldo físico verificable en CABA y presencia regional:</strong> Operamos desde nuestra Base Central Propia de 800 m² (3 niveles) en Guaminí 5657 con stock permanente de insumos, aula de capacitación y supervisión activa en CABA, GBA, La Plata, Bahía Blanca, Neuquén y Trelew.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SELECTOR AUTO-SEGMENTADOR CON BOTONES BIEN CENTRADOS (LANDING DEL RUBRO + WHATSAPP) -->
          <tr>
            <td style="padding:4px 28px 22px 28px;">
              <div style="font-size:12px;font-weight:800;color:#03582D;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px;">
                SELECCIONÁ TU SECTOR (VER LANDING ESPECÍFICA O COTIZAR POR WHATSAPP):
              </div>
              <p style="margin:0 0 10px 0;font-size:12px;color:#4B5563;">
                Tocá tu sector para ver el protocolo operativo y equipamiento de ese rubro o iniciá conversación directa por WhatsApp:
              </p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                {sector_rows_html}
              </table>

              <div style="text-align:center;margin-top:18px;">
                <a href="{WA_GENERAL}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:14px;font-weight:800;text-decoration:none;padding:14px 28px;border-radius:999px;border-bottom:3px solid #FFCC29;">
                  📲 Coordinar Visita de Relevamiento Técnico sin Cargo
                </a>
              </div>
            </td>
          </tr>

          {build_shared_footer("funnel1_apertura_B")}

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_showcase_html(html_a, html_b):
    esc_a = html_mod.escape(html_a)
    esc_b = html_mod.escape(html_b)

    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Circuito Comercial B2B y CRM Simulado + Plantillas Mailing A y B | Star Union</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Open Sans', sans-serif; background: #f9fafb; color: #133522; }}
  </style>
</head>
<body class="py-8 px-4 sm:px-6">
  <div class="max-w-7xl mx-auto space-y-8">

    <!-- HEADER -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border-2 border-[#03582d] shadow-sm flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <img src="../assets/img/logo-star-union.png" alt="Star Union" class="h-12 w-auto object-contain">
        <div>
          <span class="inline-block bg-[#03582d] text-white text-[11px] font-extrabold uppercase tracking-wider px-3 py-0.5 rounded-full mb-1">
            🌳 CIRCUITO COMERCIAL B2B + CRM SIMULADO (PERFIT API + LANDINGS + PLANILLA VIVA + WHATSAPP)
          </span>
          <h1 class="text-xl sm:text-2xl font-extrabold text-[#133522]">Cómo se Captan, Quién los Ve y Cómo se Siguen los Contactos + Plantillas HTML A y B</h1>
          <p class="text-xs text-gray-600 mt-0.5">Diseñado asumiendo que Star Union no usa CRM complejo: armamos el circuito completo con las herramientas reales disponibles para entregar datos listos para tomar decisiones comerciales.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2">
        <a href="index.html" class="bg-[#133522] hover:bg-black text-white text-xs font-extrabold px-4 py-2.5 rounded-xl transition">
          ← Volver a la Cabina de Redes y Calendario
        </a>
        <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2.5 rounded-xl transition">
          📊 Ver Historial Perfit (93 Campañas)
        </a>
      </div>
    </div>

    <!-- 1. RESPUESTA DIRECTA A TUS 3 PREGUNTAS DE SISTEMA (PERFIT REENVÍO, LANDINGS CON CTA Y CRM SIMULADO) -->
    <div class="bg-emerald-50/80 rounded-2xl p-6 border-2 border-[#03582d] space-y-4">
      <div class="text-xs font-extrabold uppercase text-[#03582d]">⚡ 1. VERDAD TÉCNICA DE LAS 3 PIEZAS DEL SISTEMA (SIN INVENTAR NADA)</div>
      <div class="grid md:grid-cols-3 gap-4 text-xs">
        <div class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
          <div class="font-extrabold text-sm text-[#03582d]">A. ¿Se puede cambiar el Asunto en el Reenvío +5 días de Perfit?</div>
          <p class="text-gray-700 leading-relaxed">
            <strong>Sí, 100%, pero ojo cómo se hace:</strong> En las campañas anteriores (#112, #115, #117, #119) tocaban el botón rápido <em>"Reenviar a no abridores"</em> de Perfit, que por defecto repite el mismo asunto y solo le agrega <code>(reenvío)</code> al nombre interno.<br>
            <strong>Cómo lo hacemos nosotros por API (en 1 clic desde acá):</strong> El servidor crea una campaña duplicada filtrada al segmento <code>No abrieron Envío #1</code> con el <strong>Asunto #2 nuevo ya cambiado</strong>.
          </p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
          <div class="font-extrabold text-sm text-[#03582d]">B. ¿A dónde van los botones de cada sector para evitar mil clics?</div>
          <p class="text-gray-700 leading-relaxed">
            Cada sector tiene <strong>2 botones bien centrados</strong>:<br>
            1. <strong>"📄 Ver Landing del Sector →"</strong>: Lleva a la Landing / Dossier interactivo abierto en ese rubro exacto, que arriba del todo tiene el <strong>botón flotante de WhatsApp de 1 clic</strong> y el teléfono <code>0810-333-8646</code> sin tener que navegar.<br>
            2. <strong>"📲 Cotizar por WhatsApp"</strong>: Abre directo el chat de WhatsApp Comercial (<code>+54 9 11 2275-9369</code>) con el rubro ya escrito.
          </p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
          <div class="font-extrabold text-sm text-[#03582d]">C. ¿Cómo simulamos un CRM sin tener CRM?</div>
          <p class="text-gray-700 leading-relaxed">
            La API de Perfit nos devuelve con <strong>nombre, apellido y correo corporativo</strong> quién hizo clic en cada botón del mail. Nuestro script cruza esa lista contra la base de clientes actuales de Mauro y genera la <strong>Planilla Viva de Seguimiento Comercial (abajo)</strong> para que Mauro o Ventas vean a quién llamar cada semana.
          </p>
        </div>
      </div>
    </div>

    <!-- 2. EL ÁRBOL LÓGICO COMPLETO DEL EMBUDO + QUIÉN LO VE Y CÓMO SE SIGUE -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-6">
      <div>
        <span class="text-xs font-extrabold uppercase text-[#03582d]">2. Árbol Lógico del Embudo B2B (Para Visualizar con Mauro: "Se manda esto a todos → Qué pasa en cada rama")</span>
        <h2 class="text-lg sm:text-xl font-extrabold text-[#133522] mt-0.5">Qué pasa cuando alguien toca, quién lo recibe, dónde queda registrado y qué se hace con quien no toca nada</h2>
      </div>

      <div class="bg-[#03582d] text-white rounded-2xl p-5 text-center space-y-1.5 shadow">
        <div class="text-[11px] font-extrabold uppercase tracking-wider text-[#ffcc29]">DISPARO INICIAL · DÍA 1 (JUEVES 10:00 HS)</div>
        <div class="text-base sm:text-lg font-extrabold">SE MANDA EL MAILING #1 DE APERTURA (GENÉRICO MULTI-RUBRO) A TODA LA BASE ACTIVA DE PERFIT</div>
        <div class="text-xs text-emerald-100">Muestra +25 años de trayectoria, Zonas Operativas (CABA, GBA Norte/Oeste/Sur, La Plata, Bahía Blanca, Neuquén y Trelew), Base 800 m², Taller Propio, Biométrico &lt;2 hs, Sello TÜV ISO 9001 + los 5 Sectores.</div>
      </div>

      <div class="grid lg:grid-cols-4 gap-4 text-xs">
        <!-- RAMA 1 -->
        <div class="bg-emerald-50 border-2 border-[#03582d] rounded-2xl p-4 space-y-2.5 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-[#03582d] text-white font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">🔥 RAMA 1 · TOCA WHATSAPP O RESPONDE</span>
            <h3 class="font-extrabold text-sm text-[#133522]">Quiere cotizar hoy (Urgencia inmediata)</h3>
            <ul class="bg-white p-3 rounded-xl border border-emerald-200 space-y-1.5 text-gray-800">
              <li><strong>¿Dónde cae?:</strong> Directo en el WhatsApp Comercial B2B (<code>+54 9 11 2275-9369</code>) o en <code>info@starunion.com.ar</code> con el rubro ya escrito.</li>
              <li><strong>¿Quién lo ve?:</strong> Recepción Comercial / Mauro en el momento.</li>
              <li><strong>¿Cómo se sigue?:</strong> Se agenda <strong>Visita de Relevamiento Técnico en Planta/Edificio</strong> en 24–48 hs y se lo marca como <code>EN COTIZACIÓN</code> en la Planilla CRM Simulado para excluirlo del reenvío del martes.</li>
            </ul>
          </div>
          <div class="bg-[#03582d] text-white p-2 rounded-xl text-center font-extrabold text-[11px]">
            Pasa directo a Visita Técnica y Presupuesto
          </div>
        </div>

        <!-- RAMA 2 -->
        <div class="bg-amber-50 border-2 border-amber-400 rounded-2xl p-4 space-y-2.5 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-amber-500 text-gray-950 font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">🎯 RAMA 2 · TOCA "VER LANDING DEL SECTOR"</span>
            <h3 class="font-extrabold text-sm text-[#133522]">Miró la Landing de su rubro pero NO mandó WhatsApp</h3>
            <ul class="bg-white p-3 rounded-xl border border-amber-300 space-y-1.5 text-gray-800">
              <li><strong>¿Dónde cae?:</strong> La API de Perfit registra con <strong>nombre, email y empresa</strong> que ese contacto hizo clic en ese rubro exacto (ej. <em>Logística</em> o <em>Salud</em>).</li>
              <li><strong>¿Quién lo ve?:</strong> Todos los viernes/lunes nuestro script actualiza la <strong>Tabla Nominal de Contactos Tibios (abajo)</strong> separando quién ya es cliente y quién es <strong>Prospecto Nuevo</strong>.</li>
              <li><strong>¿Cómo se sigue?:</strong><br>1) Al Día +7 recibe un <strong>Email #2 corto específico de ese rubro</strong>.<br>2) Comercial lo contacta sabiendo de antemano qué rubro estuvo mirando.</li>
            </ul>
          </div>
          <div class="bg-amber-500 text-gray-950 p-2 rounded-xl text-center font-extrabold text-[11px]">
            Lista Nominal de Prospectos Tibios por Rubro
          </div>
        </div>

        <!-- RAMA 3 -->
        <div class="bg-gray-50 border-2 border-gray-300 rounded-2xl p-4 space-y-2.5 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-[#133522] text-white font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">👀 RAMA 3 · ABRIÓ PERO NO TOCÓ NADA</span>
            <h3 class="font-extrabold text-sm text-[#133522]">Leyó el mail pero hoy no está licitando</h3>
            <ul class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-gray-800">
              <li><strong>¿Dónde cae?:</strong> Queda registrado en Perfit como <code>Abridor Activo (Open = Sí, Click = 0)</code>.</li>
              <li><strong>¿Qué pasa con él?:</strong> Como ya abrió el correo del jueves, <strong>NO recibe el reenvío del martes (+5 días)</strong> para no saturarlo.</li>
              <li><strong>¿Cómo se sigue?:</strong> Queda en la <strong>Lista Fidelizada</strong> y en el envío del mes siguiente recibe la otra plantilla (si en el mes 1 vio la A de Infraestructura, en el mes 2 ve la B de los 4 Riesgos Operativos Resueltos).</li>
            </ul>
          </div>
          <div class="bg-gray-200 text-[#133522] p-2 rounded-xl text-center font-extrabold text-[11px]">
            Maduración mensual sin quemar la base
          </div>
        </div>

        <!-- RAMA 4 -->
        <div class="bg-gray-50 border-2 border-gray-300 rounded-2xl p-4 space-y-2.5 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-gray-700 text-white font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">🔁 RAMA 4 · NO ABRIÓ EL MAIL EL JUEVES</span>
            <h3 class="font-extrabold text-sm text-[#133522]">No vio el correo en su bandeja de entrada</h3>
            <ul class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-gray-800">
              <li><strong>¿Qué pasa al Día +5 (Martes 10:00 hs)?:</strong> Por API creamos el 2° envío dirigido <strong>solo a quienes no abrieron el jueves</strong>, aplicándole el <strong>Asunto #2 de Reenvío</strong>.</li>
              <li><strong>Efecto medido en Star Union (#117):</strong> Recupera <strong>+21,8% de aperturas reales adicionales</strong> que el jueves se habían perdido.</li>
              <li><strong>Si tampoco abre en 4 campañas seguidas (90 días):</strong> Se separa en lista de baja frecuencia para proteger la reputación del dominio <code>starunion.com.ar</code>.</li>
            </ul>
          </div>
          <div class="bg-gray-200 text-[#133522] p-2 rounded-xl text-center font-extrabold text-[11px]">
            2° Oportunidad con Asunto #2 (+21,8% Aperturas)
          </div>
        </div>
      </div>
    </div>

    <!-- 3. CÓMO SE VE EL "CRM SIMULADO" QUE ENTREGA DATOS PARA TOMAR DECISIONES COMERCIALES -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border-2 border-[#03582d] shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <span class="text-xs font-extrabold uppercase text-[#03582d]">3. El "CRM Simulado" de Star Union (Dónde se ven y cómo se siguen los contactos después de cada envío)</span>
          <h2 class="text-lg sm:text-xl font-extrabold text-[#133522] mt-0.5">Modelo de Planilla Viva de Seguimiento Comercial que alimenta la API de Perfit + WhatsApp</h2>
          <p class="text-xs text-gray-600 mt-0.5">Sin pagar ni aprender un CRM complejo: cada vez que sale un mailing, el sistema extrae por API quién hizo clic en qué botón y arma esta tabla operativa para Dirección y Ventas:</p>
        </div>
        <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#03582d] text-white text-xs font-extrabold px-4 py-2.5 rounded-xl">
          📊 Ver Datos Reales de Perfit →
        </a>
      </div>

      <div class="overflow-x-auto border border-gray-200 rounded-xl">
        <table class="w-full text-left text-xs">
          <thead class="bg-[#133522] text-white uppercase font-extrabold">
            <tr>
              <th class="p-3">Contacto / Empresa Detectada</th>
              <th class="p-3">Botón que Clickeó en el Mail</th>
              <th class="p-3">Temperatura</th>
              <th class="p-3">Cruce Lista Mauro</th>
              <th class="p-3">Quién lo Sigue y Acción Concreta</th>
              <th class="p-3">Estado CRM Simulado</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr class="bg-emerald-50/60">
              <td class="p-3 font-bold text-[#133522]">Gerencia de Planta / Operaciones<br><span class="text-[11px] text-gray-600">contacto@empresa-logistica.com.ar</span></td>
              <td class="p-3 font-extrabold text-[#03582d]">📲 Cotizar por WhatsApp (Logística)</td>
              <td class="p-3"><span class="bg-[#03582d] text-white font-extrabold px-2 py-0.5 rounded-full text-[10px]">🔥 CALIENTE (Rama 1)</span></td>
              <td class="p-3 font-bold text-amber-800"> Prospecto Nuevo</td>
              <td class="p-3 text-gray-800"><strong>Mauro / Comercial:</strong> Responder WhatsApp y agendar visita a nave en 24-48 hs. Excluir de reenvío martes.</td>
              <td class="p-3 font-extrabold text-[#03582d]">📅 Visita Técnica Agendada</td>
            </tr>
            <tr class="bg-amber-50/50">
              <td class="p-3 font-bold text-[#133522]">Administración de Consorcios<br><span class="text-[11px] text-gray-600">info@administracion-caba.com.ar</span></td>
              <td class="p-3 font-extrabold text-[#133522]">📄 Ver Landing Consorcios (2 clics)</td>
              <td class="p-3"><span class="bg-amber-500 text-gray-950 font-extrabold px-2 py-0.5 rounded-full text-[10px]">🎯 TIBIO CON INTENCIÓN (Rama 2)</span></td>
              <td class="p-3 font-bold text-amber-800">Prospecto Nuevo</td>
              <td class="p-3 text-gray-800"><strong>Sistema + Comercial:</strong> Recibe Email #2 de Consorcios (Biométrico &lt;2 hs) al Día +7 y entra en lista de llamado comercial de la semana.</td>
              <td class="p-3 font-extrabold text-amber-900">📞 Llamar / Enviar Dossier Consorcios</td>
            </tr>
            <tr>
              <td class="p-3 font-bold text-[#133522]">Dirección Médica / Compras<br><span class="text-[11px] text-gray-600">compras@clinica-salud.com.ar</span></td>
              <td class="p-3 font-extrabold text-[#133522]">🏅 Certificado TÜV ISO 9001 + Landing Salud</td>
              <td class="p-3"><span class="bg-amber-500 text-gray-950 font-extrabold px-2 py-0.5 rounded-full text-[10px]">🎯 TIBIO AUDITORÍA (Rama 2)</span></td>
              <td class="p-3 font-bold text-emerald-800">✅ Cliente Actual (Fidelización)</td>
              <td class="p-3 text-gray-800"><strong>Ejecutivo de Cuenta:</strong> Enviar actualización de certificado TÜV Rheinland y consultar si suma nuevos consultorios/sedes.</td>
              <td class="p-3 font-extrabold text-gray-700">🤝 Seguimiento de Cuenta Activa</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- AVISO DE SEPARACIÓN ENTRE EL PANEL INTERNO Y LO QUE VE EL CLIENTE -->
    <div class="bg-[#133522] text-white rounded-2xl p-4 text-center text-xs font-extrabold tracking-wide shadow">
      👇 ABAJO ESTÁN LAS 2 OPCIONES DE PLANTILLA HTML (A Y B): Los cuadros de Asuntos y botones de arriba de cada columna son SOLO tu panel interno de control; lo que ve la gente en su correo es SOLO lo que está adentro del visor del mail 👇
    </div>

    <!-- 4. COMPARADOR LADO A LADO DE LAS 2 PLANTILLAS HTML CORREGIDAS (OPCIÓN A vs. OPCIÓN B) -->
    <div class="grid lg:grid-cols-2 gap-6 items-start">

      <!-- COLUMNA OPCIÓN A -->
      <div class="bg-white rounded-2xl border-2 border-[#03582d] shadow-sm overflow-hidden flex flex-col">
        <div class="bg-emerald-50/80 p-5 border-b border-gray-200 space-y-3">
          <div class="flex items-center justify-between gap-2">
            <span class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase">🛠️ PANEL INTERNO · OPCIÓN A (NO LO VE EL CLIENTE)</span>
            <a href="mailing-apertura-funnel1-opcion-A.html?v=20261030_v4" target="_blank" class="text-xs font-extrabold text-[#03582d] underline">Abrir mail A limpio en pestaña ↗</a>
          </div>
          <h2 class="text-lg font-extrabold text-[#133522]">Opción A: Editorial Visual + Zonas Operativas + Sello TÜV + 5 Rubros con Doble Botón + Cleany</h2>

          <!-- LOS 2 ASUNTOS BASADOS EN DATOS REALES DE LAS 93 CAMPAÑAS -->
          <div class="bg-white p-3.5 rounded-xl border border-gray-200 space-y-2.5 text-xs">
            <div>
              <label class="block font-extrabold text-[#03582d] mb-1">1° Asunto (Envío Inicial Jueves 10:00 hs · Basado en el récord de 72% apertura de campaña #110):</label>
              <input id="subj_A" type="text" value="Mantenimiento técnico y continuidad operativa para infraestructuras exigentes º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-gray-300 font-bold text-[#133522]">
            </div>
            <div>
              <label class="block font-extrabold text-amber-900 mb-1">2° Asunto (Reenvío Martes +5 días SOLO a No-Abridores · Basado en +21,8% de campaña #117):</label>
              <input id="subj_A_resend" type="text" value="Cobertura de ausencias en menos de 2 hs y taller propio en CABA ⚙️ º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-amber-300 bg-amber-50/40 font-bold text-[#133522]">
            </div>
          </div>

          <div class="grid sm:grid-cols-3 gap-2 pt-1">
            <button type="button" onclick="copyHtml('code_A', this)" class="bg-[#133522] hover:bg-black text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              📋 Copiar HTML Opción A
            </button>
            <a href="mailing-apertura-funnel1-opcion-A.html?v=20261030_v4" download="STAR_UNION_MAILING_FUNNEL1_OPCION_A.html" class="bg-white border-2 border-[#133522] text-[#133522] hover:bg-gray-100 text-center text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              ⬇ Descargar .HTML (A)
            </a>
            <button type="button" onclick="pushDraftToPerfit('A', this)" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition shadow-sm">
              🚀 Crear Borrador en Perfit (API)
            </button>
          </div>
          <div id="perfit_res_A" class="hidden text-xs font-bold p-2.5 rounded-lg bg-white border border-gray-200"></div>
        </div>

        <div class="bg-[#03582d] text-white text-[11px] font-extrabold text-center py-1.5 uppercase tracking-wider">
          👁️ Lo que ve el destinatario en su correo (Opción A):
        </div>
        <div class="p-4 bg-gray-100">
          <iframe src="mailing-apertura-funnel1-opcion-A.html?v=20261030_v4" class="w-full h-[1120px] bg-white rounded-xl border border-gray-300 shadow-inner"></iframe>
        </div>
        <textarea id="code_A" class="hidden">{esc_a}</textarea>
      </div>

      <!-- COLUMNA OPCIÓN B -->
      <div class="bg-white rounded-2xl border-2 border-[#133522] shadow-sm overflow-hidden flex flex-col">
        <div class="bg-gray-50 p-5 border-b border-gray-200 space-y-3">
          <div class="flex items-center justify-between gap-2">
            <span class="bg-[#133522] text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase">🛠️ PANEL INTERNO · OPCIÓN B (NO LO VE EL CLIENTE)</span>
            <a href="mailing-apertura-funnel1-opcion-B.html?v=20261030_v4" target="_blank" class="text-xs font-extrabold text-[#03582d] underline">Abrir mail B limpio en pestaña ↗</a>
          </div>
          <h2 class="text-lg font-extrabold text-[#133522]">Opción B: Ejecutiva de Auditoría + Tabla de 4 Riesgos + Grilla de 5 Sectores con Botones Centrados</h2>

          <!-- LOS 2 ASUNTOS BASADOS EN DATOS REALES DE LAS 93 CAMPAÑAS -->
          <div class="bg-white p-3.5 rounded-xl border border-gray-200 space-y-2.5 text-xs">
            <div>
              <label class="block font-extrabold text-[#03582d] mb-1">1° Asunto (Envío Inicial Jueves 10:00 hs · Basado en 64% apertura y 203 clics de campaña #92):</label>
              <input id="subj_B" type="text" value="El servicio con respaldo propio que protege tu operación crítica º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-gray-300 font-bold text-[#133522]">
            </div>
            <div>
              <label class="block font-extrabold text-amber-900 mb-1">2° Asunto (Reenvío Martes +5 días SOLO a No-Abridores · Enfoque Auditoría y Continuidad):</label>
              <input id="subj_B_resend" type="text" value="¿Tu operación está cubierta hoy ante ausencias, fallas de máquinas o auditorías? º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-amber-300 bg-amber-50/40 font-bold text-[#133522]">
            </div>
          </div>

          <div class="grid sm:grid-cols-3 gap-2 pt-1">
            <button type="button" onclick="copyHtml('code_B', this)" class="bg-[#133522] hover:bg-black text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              📋 Copiar HTML Opción B
            </button>
            <a href="mailing-apertura-funnel1-opcion-B.html?v=20261030_v4" download="STAR_UNION_MAILING_FUNNEL1_OPCION_B.html" class="bg-white border-2 border-[#133522] text-[#133522] hover:bg-gray-100 text-center text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              ⬇ Descargar .HTML (B)
            </a>
            <button type="button" onclick="pushDraftToPerfit('B', this)" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition shadow-sm">
              🚀 Crear Borrador en Perfit (API)
            </button>
          </div>
          <div id="perfit_res_B" class="hidden text-xs font-bold p-2.5 rounded-lg bg-white border border-gray-200"></div>
        </div>

        <div class="bg-[#133522] text-white text-[11px] font-extrabold text-center py-1.5 uppercase tracking-wider">
          👁️ Lo que ve el destinatario en su correo (Opción B):
        </div>
        <div class="p-4 bg-gray-100">
          <iframe src="mailing-apertura-funnel1-opcion-B.html?v=20261030_v4" class="w-full h-[1120px] bg-white rounded-xl border border-gray-300 shadow-inner"></iframe>
        </div>
        <textarea id="code_B" class="hidden">{esc_b}</textarea>
      </div>

    </div>

  </div>

  <script>
    const API_BASE = (location.hostname === '127.0.0.1' || location.hostname === 'localhost') ? '' : 'http://127.0.0.1:8894';

    function copyHtml(id, btn) {{
      const el = document.getElementById(id);
      navigator.clipboard.writeText(el.value);
      const old = btn.innerHTML;
      btn.innerHTML = '✅ ¡HTML Copiado!';
      setTimeout(() => btn.innerHTML = old, 2000);
    }}

    async function pushDraftToPerfit(opt, btn) {{
      const resBox = document.getElementById('perfit_res_' + opt);
      resBox.classList.remove('hidden');
      const old = btn.innerHTML;
      btn.innerHTML = '⏳ Creando borrador en Perfit...';
      resBox.innerHTML = '⏳ Subiendo plantilla HTML ' + opt + ' como borrador a la cuenta oficial de Perfit (starunionsrl)...';
      const subject = document.getElementById('subj_' + opt).value;
      try {{
        const r = await fetch(API_BASE + '/api/perfit/create-draft', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ option: opt, subject: subject }})
        }});
        const data = await r.json();
        if (data.ok) {{
          resBox.innerHTML = `✅ <strong>Borrador creado en Perfit con éxito:</strong> Campaña ID <strong>#${{data.campaign_id || 'Listo'}}</strong> (${{data.name || 'Funnel 1 Apertura'}}). Ya podés verlo en tu panel de Perfit o programarlo desde acá.`;
          btn.innerHTML = '✅ ¡Borrador en Perfit!';
        }} else {{
          resBox.innerHTML = '⚠️ Respuesta de Perfit: ' + (data.error || JSON.stringify(data));
          btn.innerHTML = old;
        }}
      }} catch (e) {{
        resBox.innerHTML = '❌ Error conectando con el servidor local (http://127.0.0.1:8894): ' + e.message;
        btn.innerHTML = old;
      }}
    }}
  </script>
</body>
</html>"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    html_a = build_template_a()
    html_b = build_template_b()
    path_a = os.path.join(OUT_DIR, "mailing-apertura-funnel1-opcion-A.html")
    path_b = os.path.join(OUT_DIR, "mailing-apertura-funnel1-opcion-B.html")
    path_show = os.path.join(OUT_DIR, "embudo-y-comparador-mailing-ab.html")

    with open(path_a, "w", encoding="utf-8") as f:
        f.write(html_a)
    with open(path_b, "w", encoding="utf-8") as f:
        f.write(html_b)
    with open(path_show, "w", encoding="utf-8") as f:
        f.write(build_showcase_html(html_a, html_b))

    print("Generados con exito:")
    print(" -", path_a)
    print(" -", path_b)
    print(" -", path_show)


if __name__ == "__main__":
    main()
