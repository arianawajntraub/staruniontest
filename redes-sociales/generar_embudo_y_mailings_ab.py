#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Propuesta Visual de Embudo B2B 2027 (Árbol de Decisión CRM para Ariana y Mauro)
+ Plantillas HTML Email-Safe Opción A y Opción B corregidas con los 4 comentarios de Ariana:
1. Franja superior: +25 años de trayectoria separada de las Zonas Operativas reales (CABA · GBA Norte, Oeste y Sur · La Plata · Bahía Blanca · Neuquén · Trelew).
2. Sello TÜV Rheinland ISO 9001:2015 (ID 9000041847) jerarquizado siempre arriba en el cabezal en ambas versiones A y B.
3. Destino claro de los botones por sector (Best Practice B2B 2027):
   - Botón 1 ("📄 Ver Ficha Técnica del Sector"): Abre el Dossier/Landing de ese rubro y etiqueta en Perfit el interés exacto del contacto aunque todavía no escriba por WhatsApp (captura de Intent Leads).
   - Botón 2 ("📲 WhatsApp B2B"): Abre conversación directa con Comercial (+54 9 11 2275-9369) para el que ya quiere cotizar hoy.
4. Grilla de rubros en Opción B maquetada en tabla de 2 columnas con botones limpios (cero texto pegado ni float roto).
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

# Links de Captura de Intención (Ficha Técnica / Dossier por Vertical con UTM para Perfit)
DOSSIER_LOGISTICA = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=fabricas&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=logistica_industria"
DOSSIER_OFICINAS = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=oficinas&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=oficinas_corporativas"
DOSSIER_CONSORCIOS = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=consorcios&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=consorcios_edificios"
DOSSIER_SALUD = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=clinicas&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=salud_laboratorios"
DOSSIER_EDUCACION = "https://wajntraub.ar/staruniontest/dossier/index.html?vertical=universidades&utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura&rubro=educacion_clubes"

# Links Directos a WhatsApp Comercial B2B (+54 9 11 2275-9369)
WA_GENERAL = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20vi%20su%20comunicaci%C3%B3n%20y%20quiero%20solicitar%20una%20propuesta%20t%C3%A9cnica%20de%20limpieza%20para%20nuestra%20organizaci%C3%B3n."
WA_LOGISTICA = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20limpieza%20industrial%20y%20centros%20log%C3%ADsticos."
WA_OFICINAS = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20limpieza%20para%20oficinas%20y%20edificios%20corporativos."
WA_CONSORCIOS = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20limpieza%20para%20consorcios%20y%20edificios."
WA_SALUD = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20higiene%20t%C3%A9cnica%20para%20cl%C3%ADnicas%20y%20laboratorios."
WA_EDUCACION = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20mantenimiento%20integral%20de%20universidades%2C%20colegios%20y%20clubes."


def build_shared_top_header(utm_tag):
    """
    Cabezal Maestro Obligatorio (Idéntico en jerarquía para Opción A y Opción B):
    1. Franja Verde con Antigüedad Real (+25 años de trayectoria) separada de la Cobertura Geográfica Real.
    2. Cabezal Blanco con Logo Star Union + Sello TÜV Rheinland ISO 9001:2015 (ID 9000041847) grande y clicable.
    """
    return f"""
          <!-- FRANJA SUPERIOR 1: ANTIGÜEDAD + ZONAS OPERATIVAS REALES (SIN MEZCLAR FECHAS CON LOCALIDADES) -->
          <tr>
            <td style="background-color:#03582D;padding:10px 20px;text-align:center;color:#FFFFFF;">
              <div style="font-size:11px;font-weight:800;letter-spacing:0.05em;text-transform:uppercase;">
                +25 AÑOS DE TRAYECTORIA EN LIMPIEZA PROFESIONAL E INDUSTRIAL
              </div>
              <div style="font-size:11px;font-weight:600;color:#E6EFEA;margin-top:3px;">
                📍 Cobertura Operativa: <strong>CABA · GBA (Norte, Oeste y Sur) · La Plata · Bahía Blanca · Neuquén · Trelew</strong>
              </div>
            </td>
          </tr>

          <!-- ENCABEZADO FIJO: LOGO STAR UNION + SELLO TÜV RHEINLAND ISO 9001 JERARQUIZADO -->
          <tr>
            <td style="padding:20px 26px 18px 26px;border-bottom:3px solid #03582D;background-color:#FFFFFF;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" width="48%">
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign={utm_tag}" target="_blank">
                      <img src="{LOGO_URL}" alt="Star Union" width="185" style="display:block;max-width:185px;height:auto;border:0;">
                    </a>
                  </td>
                  <td align="right" valign="middle" width="52%">
                    <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="text-decoration:none;display:inline-block;">
                      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:2px solid #03582D;border-radius:12px;padding:8px 12px;">
                        <tr>
                          <td valign="middle" style="padding-right:10px;">
                            <img src="{TUV_URL}" alt="TÜV Rheinland ISO 9001:2015" width="44" style="display:block;border:0;">
                          </td>
                          <td align="left" valign="middle" style="font-size:11px;line-height:1.32;color:#133522;">
                            <strong style="color:#03582D;font-size:12px;display:block;letter-spacing:0.02em;">CERTIFICACIÓN ISO 9001:2015</strong>
                            <span style="color:#374151;font-weight:700;display:block;">TÜV Rheinland · ID 9000041847</span>
                            <span style="color:#03582D;font-size:10px;font-weight:800;text-decoration:underline;">Verificar certificado en línea ↗</span>
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
    return f"""
          <!-- PIE INSTITUCIONAL Y CUMPLIMIENTO PERFIT (BLANCO / VERDE STAR UNION · CERO AZUL) -->
          <tr>
            <td style="background-color:#F9FAFB;border-top:4px solid #03582D;color:#133522;padding:24px 28px;text-align:center;">
              <div style="font-size:15px;font-weight:800;color:#03582D;margin-bottom:4px;">Star Union · Sabemos de Limpieza</div>
              <div style="font-size:12px;color:#374151;font-weight:700;margin-bottom:4px;">
                Base Operativa Central (800 m²): Guaminí 5657, CABA · Tel: 0810-333-8646 · WhatsApp B2B: +54 9 11 2275-9369
              </div>
              <div style="font-size:11px;color:#4B5563;font-weight:600;margin-bottom:12px;">
                Operación activa en CABA · GBA Norte, Oeste y Sur · La Plata · Bahía Blanca · Neuquén · Trelew
              </div>
              <div style="margin-bottom:14px;">
                <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign={utm_tag}" target="_blank" style="color:#03582D;font-size:12px;font-weight:800;text-decoration:underline;margin:0 8px;">Sitio Web Oficial</a> |
                <a href="https://www.instagram.com/starunionservicios/" target="_blank" style="color:#133522;font-size:12px;font-weight:700;text-decoration:none;margin:0 8px;">Instagram</a> |
                <a href="https://www.linkedin.com/company/star-union-srl/" target="_blank" style="color:#133522;font-size:12px;font-weight:700;text-decoration:none;margin:0 8px;">LinkedIn</a> |
                <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="color:#03582D;font-size:12px;font-weight:700;text-decoration:none;margin:0 8px;">Certificado TÜV ISO 9001</a>
              </div>
              <div style="font-size:11px;color:#4B5563;line-height:1.4;">
                Recibís esta comunicación institucional por formar parte de nuestra red de contactos corporativos.<br>
                Si deseás dejar de recibir novedades, podés <a href="{{{{unsubscribe_link}}}}" style="color:#03582D;font-weight:700;text-decoration:underline;">desuscribirte en 1 clic aquí</a>.
              </div>
            </td>
          </tr>
    """


def build_template_a():
    """
    OPCIÓN A: Editorial Visual Multi-Vertical con Infraestructura 800 m²,
    Tarjetas Fotográficas por Sector (con doble botón: 1. Ver Ficha Técnica / Dossier del Sector para capturar clic en CRM + 2. WhatsApp Directo)
    y El Dato Técnico de Cleany.
    """
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Continuidad Operativa e Infraestructura Propia | Star Union</title>
</head>
<body style="margin:0;padding:0;background-color:#F3F4F6;font-family:'Open Sans',Arial,Helvetica,sans-serif;color:#133522;-webkit-font-smoothing:antialiased;">
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    +25 años de trayectoria · Base Propia de 800 m² en CABA, Taller In-House, presentismo biométrico (&lt; 2 hs) y certificación ISO 9001:2015 (TÜV Rheinland).
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F3F4F6;padding:24px 10px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:16px;overflow:hidden;border:1px solid #E5E7EB;">
          
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
                  <td width="32%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#03582D;">800 m²</div>
                    <div style="font-size:11px;color:#374151;font-weight:600;margin-top:3px;">Base Propia en Guaminí 5657 (CABA)</div>
                  </td>
                  <td width="2%"></td>
                  <td width="32%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#03582D;">&lt; 2 Horas</div>
                    <div style="font-size:11px;color:#374151;font-weight:600;margin-top:3px;">Cobertura Biométrica con Guardia Móvil</div>
                  </td>
                  <td width="2%"></td>
                  <td width="32%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;padding:12px;text-align:center;">
                    <div style="font-size:18px;font-weight:800;color:#03582D;">In-House</div>
                    <div style="font-size:11px;color:#374151;font-weight:600;margin-top:3px;">Taller Propio y Reemplazo en el Día</div>
                  </td>
                </tr>
              </table>

              <!-- BOTÓN PRINCIPAL WHATSAPP COMERCIAL -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center" style="padding:4px 0 8px 0;">
                    <a href="{WA_GENERAL}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:14px;font-weight:800;text-decoration:none;padding:14px 26px;border-radius:999px;border-bottom:3px solid #FFCC29;">
                      📲 Hablar con Dirección Comercial por WhatsApp
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
                  SELECCIONÁ TU SECTOR (VER DOSSIER TÉCNICO O COTIZAR DIRECTO)
                </div>
                <h2 style="margin:4px 0 12px 0;font-size:18px;font-weight:800;color:#133522;">
                  Soluciones específicas según la exigencia de tu operación:
                </h2>
              </div>
            </td>
          </tr>

          <!-- VERTICAL 1: LOGÍSTICA E INDUSTRIA -->
          <tr>
            <td style="padding:8px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                <tr>
                  <td style="padding:0;">
                    <a href="{DOSSIER_LOGISTICA}" target="_blank">
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
                    <a href="{DOSSIER_LOGISTICA}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:12px;font-weight:800;text-decoration:none;padding:10px 16px;border-radius:8px;margin-right:8px;">
                      📄 Ver Dossier Industrial y Alcance →
                    </a>
                    <a href="{WA_LOGISTICA}" target="_blank" style="display:inline-block;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:12px;font-weight:800;text-decoration:none;padding:9px 14px;border-radius:8px;">
                      📲 WhatsApp Directo
                    </a>
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
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                    <a href="{DOSSIER_OFICINAS}" target="_blank">
                      <img src="{IMG_BIOMETRICO}" alt="Oficinas y Edificios Corporativos" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">2. OFICINAS Y CORPORATIVOS</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Edificios corporativos, bancos y sedes</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Presentismo validado por reloj biométrico, personal registrado (indemnidad Art. 30 LCT) y supervisión constante.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{DOSSIER_OFICINAS}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 10px;border-radius:8px;">
                          📄 Ver Ficha Oficinas →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_OFICINAS}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
                          📲 Cotizar por WhatsApp
                        </a>
                      </div>
                    </div>
                  </td>
                  <td width="4%"></td>
                  <!-- CONSORCIOS -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                    <a href="{DOSSIER_CONSORCIOS}" target="_blank">
                      <img src="{IMG_TALLER}" alt="Consorcios y Barrios Cerrados" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">3. CONSORCIOS Y TORRES</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Grandes consorcios y barrios cerrados</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Cobertura de ausencias en menos de 2 horas con guardia móvil propia para que ningún turno quede sin cubrir.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{DOSSIER_CONSORCIOS}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 10px;border-radius:8px;">
                          📄 Ver Ficha Consorcios →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_CONSORCIOS}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
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
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                    <a href="{DOSSIER_SALUD}" target="_blank">
                      <img src="{IMG_SALUD}" alt="Clínicas y Laboratorios" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">4. SALUD Y LABORATORIOS</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Clínicas, sanatorios y laboratorios</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Zonificación contra contaminación cruzada e insumos aprobados por ANMAT con hojas de seguridad (MSDS) en planta.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{DOSSIER_SALUD}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 10px;border-radius:8px;">
                          📄 Ver Ficha Salud / ANMAT →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_SALUD}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
                          📲 Cotizar por WhatsApp
                        </a>
                      </div>
                    </div>
                  </td>
                  <td width="4%"></td>
                  <!-- EDUCACIÓN Y CLUBES -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                    <a href="{DOSSIER_EDUCACION}" target="_blank">
                      <img src="{IMG_CLUBES}" alt="Universidades, Colegios y Clubes" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">5. EDUCACIÓN Y DEPORTE</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#133522;">Universidades, colegios y clubes</h3>
                      <p style="margin:0 0 12px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Operativos en contraturno, cuidado de pisos deportivos de parquet y preparación para receso y temporada de verano.
                      </p>
                      <div style="margin-bottom:6px;">
                        <a href="{DOSSIER_EDUCACION}" target="_blank" style="display:block;text-align:center;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 10px;border-radius:8px;">
                          📄 Ver Ficha Educación/Clubes →
                        </a>
                      </div>
                      <div>
                        <a href="{WA_EDUCACION}" target="_blank" style="display:block;text-align:center;background-color:#FFFFFF;border:1px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:8px;">
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
            <td style="padding:16px 28px;">
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
    Entra por los 4 Dolores Críticos B2B + Tabla Comparativa + Grilla de 5 Sectores en Tabla de 2 Columnas Limpias
    (con Botón "📄 Ver Ficha" para capturar intención en CRM + Botón "📲 WhatsApp").
    """
    rows_data = [
        ("🏭 1. Centros Logísticos, Depósitos y Plantas", "Autolavadoras hombre a bordo, barredoras y taller propio en CABA.", DOSSIER_LOGISTICA, WA_LOGISTICA),
        ("🏢 2. Oficinas Corporativas, Bancos y Sedes", "Control biométrico en tiempo real e indemnidad laboral Art. 30 LCT.", DOSSIER_OFICINAS, WA_OFICINAS),
        ("🏙️ 3. Grandes Consorcios, Torres y Barrios Cerrados", "Cobertura de ausencias en menos de 2 horas con guardia móvil propia.", DOSSIER_CONSORCIOS, WA_CONSORCIOS),
        ("🏥 4. Clínicas, Sanatorios y Laboratorios (ANMAT)", "Prevención de contaminación cruzada e insumos ANMAT con hojas MSDS.", DOSSIER_SALUD, WA_SALUD),
        ("🎓 5. Universidades, Colegios Bilingües y Clubes", "Operación sincronizada en contraturno y cuidado de pisos deportivos.", DOSSIER_EDUCACION, WA_EDUCACION),
    ]

    sector_rows_html = ""
    for title, desc, dossier_url, wa_url in rows_data:
        sector_rows_html += f"""
                <tr>
                  <td style="padding:6px 0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1.5px solid #E5E7EB;border-left:4px solid #03582D;border-radius:10px;padding:12px 14px;">
                      <tr>
                        <td valign="middle" width="60%" style="padding-right:10px;">
                          <div style="font-size:13px;font-weight:800;color:#133522;line-height:1.25;">{title}</div>
                          <div style="font-size:11px;color:#4B5563;margin-top:3px;line-height:1.35;">{desc}</div>
                        </td>
                        <td valign="middle" align="right" width="40%" style="white-space:nowrap;">
                          <a href="{dossier_url}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 11px;border-radius:7px;margin-right:4px;">
                            📄 Ver Ficha
                          </a>
                          <a href="{wa_url}" target="_blank" style="display:inline-block;background-color:#FFFFFF;border:1.5px solid #03582D;color:#03582D;font-size:11px;font-weight:800;text-decoration:none;padding:7px 10px;border-radius:7px;">
                            📲 WhatsApp
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
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:16px;overflow:hidden;border:1px solid #E5E7EB;">

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
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:1px solid #E5E7EB;border-radius:12px;overflow:hidden;">
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
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                <tr>
                  <td>
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_B&vertical=infraestructura_guamini" target="_blank">
                      <img src="{IMG_TALLER}" alt="Base Operativa Propia de 800 m² en Guaminí 5657, CABA" width="544" style="display:block;width:100%;max-width:544px;height:200px;object-fit:cover;border:0;">
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:14px 18px;font-size:13px;line-height:1.48;color:#374151;">
                    <strong style="color:#133522;">Respaldo físico verificable en CABA:</strong> Operamos desde nuestra Base Central Propia de 800 m² (3 niveles) en Guaminí 5657 con stock permanente de insumos, aula de capacitación y flota propia de asistencia técnica.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SELECTOR AUTO-SEGMENTADOR EN TABLA DE 2 COLUMNAS LIMPIA (DOSSIER + WHATSAPP) -->
          <tr>
            <td style="padding:4px 28px 22px 28px;">
              <div style="font-size:12px;font-weight:800;color:#03582D;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px;">
                SELECCIONÁ TU SECTOR (VER FICHA TÉCNICA ONLINE O HABLAR POR WHATSAPP):
              </div>
              <p style="margin:0 0 10px 0;font-size:12px;color:#4B5563;">
                Podés revisar primero el alcance técnico de tu rubro sin compromiso o iniciar conversación directa con nuestra Dirección Comercial:
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
  <title>Árbol Lógico del Embudo B2B 2027 + Plantillas HTML Mailing A y B | Star Union</title>
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
            🌳 ÁRBOL DE DECISIÓN DEL EMBUDO B2B 2027 · PARA VISUALIZAR CON DUEÑO (MAURO)
          </span>
          <h1 class="text-xl sm:text-2xl font-extrabold text-[#133522]">Cómo Funciona el Embudo paso a paso ("Si toca X → pasa Y") + Plantillas HTML A y B</h1>
          <p class="text-xs text-gray-600 mt-0.5">Arquitectura World-Class de Ventas B2B y Prospección CRM: por qué cada sector tiene botón a <strong>Ficha Técnica (captura silenciosa de intención)</strong> + botón a <strong>WhatsApp (urgencia inmediata)</strong>.</p>
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

    <!-- 1. EXPLICACIÓN DE MEJOR PRÁCTICA WORLD-CLASS B2B (RESPUESTA A "¿A DÓNDE VAN LOS BOTONES?") -->
    <div class="bg-emerald-50/70 rounded-2xl p-6 border-2 border-[#03582d] space-y-4">
      <div class="text-xs font-extrabold uppercase text-[#03582d]">💡 LA REGLA DE ORO DE VENTAS B2B 2027: ¿A dónde van los botones de cada sector y por qué hay DOS botones por rubro?</div>
      <div class="grid md:grid-cols-2 gap-4 text-xs">
        <div class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
          <div class="font-extrabold text-sm text-[#03582d]">1. Botón "📄 Ver Ficha Técnica / Dossier del Sector" (El detector de intención del CRM)</div>
          <p class="text-gray-700 leading-relaxed">
            <strong>¿A dónde lleva?:</strong> Al <strong>Brochure Interactivo Online de ese rubro exacto</strong> (ej. <em>Dossier de Fábricas y Logística</em>, <em>Dossier de Clínicas ANMAT</em>, <em>Dossier de Consorcios</em>).<br>
            <strong>¿Por qué es clave en ventas B2B?:</strong> El 85% de los gerentes de compras o planta que abren un mail <strong>quieren ver primero qué máquinas tenés y cómo trabajás antes de hablar con un vendedor en WhatsApp</strong>. Si el único botón abre WhatsApp de prepo, el gerente cierra la ventana y <strong>no te enterás nunca de quién era</strong>. En cambio, cuando toca <em>"📄 Ver Ficha Técnica"</em>, Perfit guarda en el acto su <strong>Nombre, Email, Empresa y qué Rubro tocó</strong>. ¡Ahí ya lo capturaste como Lead Tibio con nombre y apellido!
          </p>
        </div>
        <div class="bg-white p-4 rounded-xl border border-gray-200 space-y-2">
          <div class="font-extrabold text-sm text-[#03582d]">2. Botón "📲 WhatsApp Directo B2B" (El canal rápido para el que tiene urgencia hoy)</div>
          <p class="text-gray-700 leading-relaxed">
            <strong>¿A dónde lleva?:</strong> Abre el WhatsApp Comercial de Star Union (<code>+54 9 11 2275-9369</code>) con el texto ya escrito para ese rubro (ej. <em>"Hola Star Union, quiero consultar por el servicio de limpieza industrial y centros logísticos"</em>).<br>
            <strong>¿Para quién es?:</strong> Para el 15% de la base que justo esa semana tuvo un problema grave con su proveedor actual (ausencias, mala limpieza o auditoría en puerta) y quiere cotizar en el día sin leer más.
          </p>
        </div>
      </div>
    </div>

    <!-- 2. EL ÁRBOL LÓGICO COMPLETO DEL EMBUDO (PARA MOSTRARLE A MAURO EN 1 PANTALLA) -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-6">
      <div>
        <span class="text-xs font-extrabold uppercase text-[#03582d]">2. Árbol de Decisión del Embudo (Paso a Paso: "Se manda esto a todos → ¿Qué pasa según lo que hace cada uno?")</span>
        <h2 class="text-lg sm:text-xl font-extrabold text-[#133522] mt-0.5">Circuito Completo desde el Disparo Inicial (Día 1) hasta el Cierre de Visita Técnica</h2>
      </div>

      <!-- CAJA MADRE: DISPARO DÍA 1 -->
      <div class="bg-[#03582d] text-white rounded-2xl p-5 text-center space-y-1.5 shadow">
        <div class="text-[11px] font-extrabold uppercase tracking-wider text-[#ffcc29]">PASO INICIAL · DÍA 1 (JUEVES 10:00 HS)</div>
        <div class="text-base sm:text-lg font-extrabold">SE ENVÍA EL MAILING #1 DE APERTURA (GENÉRICO MULTI-RUBRO · OPCIÓN A) A TODA LA BASE ACTIVA</div>
        <div class="text-xs text-emerald-100">Presenta la espalda de Star Union (+25 años, Base 800 m² Guaminí, Taller Propio, Biométrico &lt;2 hs, ISO 9001 TÜV, Cobertura CABA/GBA/La Plata/Bahía Blanca/Neuquén/Trelew) + los 5 Sectores.</div>
      </div>

      <div class="text-center text-sm font-extrabold text-[#03582d]">⬇️ A partir de ese envío, la base se divide sola en 4 RAMAS según el comportamiento real de cada contacto ⬇️</div>

      <!-- LAS 4 RAMAS DEL ÁRBOL -->
      <div class="grid lg:grid-cols-4 gap-4 text-xs">

        <!-- RAMA 1: TOCA WHATSAPP O RESPONDE -->
        <div class="bg-emerald-50 border-2 border-[#03582d] rounded-2xl p-4 space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-[#03582d] text-white font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">🔥 RAMA 1 · LEAD CALIENTE (URGENCIA HOY)</span>
            <h3 class="font-extrabold text-sm text-[#133522]">¿Qué hizo?: Tocó "📲 WhatsApp" o respondió el correo</h3>
            <div class="bg-white p-3 rounded-xl border border-emerald-200 space-y-1.5 text-gray-800">
              <div><strong>1. Qué pasa en el acto:</strong> Entra al WhatsApp Comercial (<code>+54 9 11 2275-9369</code>) con su rubro ya identificado en el mensaje.</div>
              <div><strong>2. Qué hace el CRM / Perfit:</strong> Se le pone la etiqueta <code>EN_COTIZACION</code> y <strong>se lo pausa de los reenvíos automáticos</strong> para no mandarle otro mail mientras está hablando con ventas.</div>
              <div><strong>3. Acción de Star Union:</strong> Coordinar <strong>Visita de Relevamiento Técnico en Planta/Edificio</strong> dentro de las 24–48 hs.</div>
            </div>
          </div>
          <div class="bg-[#03582d] text-white p-2.5 rounded-xl text-center font-extrabold text-[11px]">
            🎯 Resultado: Pasa directo a Presupuesto / Visita Técnica
          </div>
        </div>

        <!-- RAMA 2: TOCA "VER FICHA TÉCNICA" DE UN RUBRO PERO NO ESCRIBE A WHATSAPP -->
        <div class="bg-amber-50 border-2 border-amber-400 rounded-2xl p-4 space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-amber-500 text-gray-950 font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">🎯 RAMA 2 · LA MINA DE ORO (CLIC EN RUBRO)</span>
            <h3 class="font-extrabold text-sm text-[#133522]">¿Qué hizo?: Tocó "📄 Ver Ficha" (ej. Logística o Salud), miró el Dossier, pero NO mandó WhatsApp</h3>
            <div class="bg-white p-3 rounded-xl border border-amber-300 space-y-1.5 text-gray-800">
              <div><strong>1. Qué detecta Perfit en silencio:</strong> Guarda nombre, mail y empresa bajo la etiqueta exacta del sector que tocó (ej. <code>INTERES_LOGISTICA</code>, <code>INTERES_CONSORCIOS</code>, <code>INTERES_SALUD</code>).</div>
              <div><strong>2. Cruce con Lista de Mauro:</strong> Si no es cliente actual, sabemos que ese gerente está mirando proveedores de ese rubro hoy.</div>
              <div><strong>3. Qué recibe al Día +7 (Email #2 Específico):</strong> Recibe un correo corto <strong>100% de su rubro</strong> (no genérico) con el PDF descargable de su vertical y propuesta de relevamiento sin cargo.</div>
            </div>
          </div>
          <div class="bg-amber-500 text-gray-950 p-2.5 rounded-xl text-center font-extrabold text-[11px]">
            🎯 Resultado: Lista Nominal de Prospectos Tibios por Rubro para Comercial
          </div>
        </div>

        <!-- RAMA 3: ABRIÓ EL MAIL PERO NO TOCÓ NADA -->
        <div class="bg-gray-50 border-2 border-gray-300 rounded-2xl p-4 space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-[#133522] text-white font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">👀 RAMA 3 · ABRIÓ PERO NO CLICKEÓ</span>
            <h3 class="font-extrabold text-sm text-[#133522]">¿Qué hizo?: Abrió el correo, leyó el titular o vio el sello ISO 9001, pero no tocó botones</h3>
            <div class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-gray-800">
              <div><strong>1. Por qué pasa:</strong> En B2B los contratos de limpieza se renuevan en ventanas específicas; hoy leyó quién sos, pero su licitación abre el mes que viene.</div>
              <div><strong>2. Qué NO hacemos:</strong> No le reenviamos el mismo mail a los 5 días (para no cansarlo si ya lo abrió).</div>
              <div><strong>3. Qué recibe al mes siguiente:</strong> En la campaña siguiente entra con el <strong>Ángulo B (Tabla de los 4 Riesgos Operativos Resueltos: Biométrico &lt;2 hs, Taller Propio, Art. 30 LCT)</strong> + impactos en las 5 redes.</div>
            </div>
          </div>
          <div class="bg-gray-200 text-[#133522] p-2.5 rounded-xl text-center font-extrabold text-[11px]">
            🎯 Resultado: Maduración de Marca (Top of Mind para cuando licite)
          </div>
        </div>

        <!-- RAMA 4: NO ABRIÓ EL MAIL -->
        <div class="bg-gray-50 border-2 border-gray-300 rounded-2xl p-4 space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <span class="inline-block bg-gray-700 text-white font-extrabold px-2.5 py-1 rounded-full text-[10px] uppercase">🔁 RAMA 4 · NO ABRIÓ EL MAIL DÍA 1</span>
            <h3 class="font-extrabold text-sm text-[#133522]">¿Qué hizo?: Estaba en reunión o en planta el jueves y el correo quedó abajo en su bandeja</h3>
            <div class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-gray-800">
              <div><strong>1. Qué pasa al Día +5 (Martes 10:00 hs):</strong> Perfit filtra <strong>solo a los que no abrieron el jueves</strong> y les envía la <strong>Opción B con un Asunto nuevo de pregunta</strong> (<em>"¿Tu operación está cubierta hoy ante ausencias o auditorías?"</em>).</div>
              <div><strong>2. Dato real comprobado en Star Union (#117):</strong> Esta segunda pasada suma <strong>+21,8% de aperturas reales extra</strong> y duplica los clics a WhatsApp.</div>
              <div><strong>3. Regla de higiene CRM:</strong> Si un correo no abre 4 envíos seguidos (90 días), pasa a lista fría para cuidar la entregabilidad del dominio.</div>
            </div>
          </div>
          <div class="bg-gray-200 text-[#133522] p-2.5 rounded-xl text-center font-extrabold text-[11px]">
            🎯 Resultado: Recupera +21,8% de decisores que no habían visto el 1° envío
          </div>
        </div>

      </div>
    </div>

    <!-- 3. COMPARADOR LADO A LADO DE LAS 2 PLANTILLAS HTML CORREGIDAS (OPCIÓN A vs. OPCIÓN B) -->
    <div class="grid lg:grid-cols-2 gap-6 items-start">

      <!-- COLUMNA OPCIÓN A -->
      <div class="bg-white rounded-2xl border-2 border-[#03582d] shadow-sm overflow-hidden flex flex-col">
        <div class="bg-emerald-50/80 p-5 border-b border-gray-200 space-y-3">
          <div class="flex items-center justify-between gap-2">
            <span class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase">OPCIÓN A · Ideal para el 1° Envío (Jueves)</span>
            <a href="mailing-apertura-funnel1-opcion-A.html" target="_blank" class="text-xs font-extrabold text-[#03582d] underline">Abrir sola en pestaña ↗</a>
          </div>
          <h2 class="text-lg font-extrabold text-[#133522]">Plantilla A: Infraestructura 800 m² + 5 Tarjetas con Doble Botón (Ficha Técnica + WhatsApp) + Cleany</h2>
          <p class="text-xs text-gray-700">
            <strong>Cambios aplicados:</strong> Franja superior con <em>+25 años de trayectoria</em> + las <em>7 zonas operativas reales</em> (CABA, GBA Norte/Oeste/Sur, La Plata, Bahía Blanca, Neuquén y Trelew), Sello TÜV ISO 9001 grande en el cabezal y doble botón en cada sector (<strong>📄 Ver Dossier/Ficha</strong> + <strong>📲 WhatsApp</strong>).
          </p>
          <div class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-xs">
            <div><strong class="text-gray-600">Asunto Editable A:</strong></div>
            <input id="subj_A" type="text" value="Infraestructura propia de 800 m² y continuidad operativa ISO 9001 º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-gray-300 font-bold text-[#133522]">
          </div>
          <div class="grid sm:grid-cols-3 gap-2 pt-1">
            <button type="button" onclick="copyHtml('code_A', this)" class="bg-[#133522] hover:bg-black text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              📋 Copiar HTML Opción A
            </button>
            <a href="mailing-apertura-funnel1-opcion-A.html" download="STAR_UNION_MAILING_FUNNEL1_OPCION_A.html" class="bg-white border-2 border-[#133522] text-[#133522] hover:bg-gray-100 text-center text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              ⬇ Descargar .HTML (A)
            </a>
            <button type="button" onclick="pushDraftToPerfit('A', this)" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition shadow-sm">
              🚀 Crear Borrador en Perfit (API)
            </button>
          </div>
          <div id="perfit_res_A" class="hidden text-xs font-bold p-2.5 rounded-lg bg-white border border-gray-200"></div>
        </div>

        <div class="p-4 bg-gray-100">
          <iframe src="mailing-apertura-funnel1-opcion-A.html" class="w-full h-[1060px] bg-white rounded-xl border border-gray-300 shadow-inner"></iframe>
        </div>
        <textarea id="code_A" class="hidden">{esc_a}</textarea>
      </div>

      <!-- COLUMNA OPCIÓN B -->
      <div class="bg-white rounded-2xl border-2 border-[#133522] shadow-sm overflow-hidden flex flex-col">
        <div class="bg-gray-50 p-5 border-b border-gray-200 space-y-3">
          <div class="flex items-center justify-between gap-2">
            <span class="bg-[#133522] text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase">OPCIÓN B · Ideal para el 2° Envío (+5 Días) o Decisores Técnicos</span>
            <a href="mailing-apertura-funnel1-opcion-B.html" target="_blank" class="text-xs font-extrabold text-[#03582d] underline">Abrir sola en pestaña ↗</a>
          </div>
          <h2 class="text-lg font-extrabold text-[#133522]">Plantilla B: Matriz de los 4 Riesgos Operativos Resueltos + Grilla Limpia de 2 Columnas por Sector</h2>
          <p class="text-xs text-gray-700">
            <strong>Cambios aplicados:</strong> Mismo cabezal superior con <em>+25 años + Zonas Operativas</em> y Sello TÜV Rheinland ISO 9001 grande, tabla comparativa de los 4 dolores B2B y <strong>nueva grilla de los 5 rubros en 2 columnas limpias</strong> con los botones <strong>📄 Ver Ficha</strong> y <strong>📲 WhatsApp</strong> alineados.
          </p>
          <div class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-xs">
            <div><strong class="text-gray-600">Asunto Editable B:</strong></div>
            <input id="subj_B" type="text" value="¿Tu operación está cubierta hoy ante ausencias, fallas de máquinas o auditorías? º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-gray-300 font-bold text-[#133522]">
          </div>
          <div class="grid sm:grid-cols-3 gap-2 pt-1">
            <button type="button" onclick="copyHtml('code_B', this)" class="bg-[#133522] hover:bg-black text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              📋 Copiar HTML Opción B
            </button>
            <a href="mailing-apertura-funnel1-opcion-B.html" download="STAR_UNION_MAILING_FUNNEL1_OPCION_B.html" class="bg-white border-2 border-[#133522] text-[#133522] hover:bg-gray-100 text-center text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              ⬇ Descargar .HTML (B)
            </a>
            <button type="button" onclick="pushDraftToPerfit('B', this)" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition shadow-sm">
              🚀 Crear Borrador en Perfit (API)
            </button>
          </div>
          <div id="perfit_res_B" class="hidden text-xs font-bold p-2.5 rounded-lg bg-white border border-gray-200"></div>
        </div>

        <div class="p-4 bg-gray-100">
          <iframe src="mailing-apertura-funnel1-opcion-B.html" class="w-full h-[1060px] bg-white rounded-xl border border-gray-300 shadow-inner"></iframe>
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
