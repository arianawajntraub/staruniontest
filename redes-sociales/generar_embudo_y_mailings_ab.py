#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la Propuesta de Embudo B2B (Funnel 1) + Plantillas HTML Email-Safe Opción A y Opción B
para Star Union (Perfit Email Marketing + WhatsApp Comercial + Retroalimentación con Redes).
Cumple 100% de reglas Star Union:
- 85% Blanco dominante (#FFFFFF), 12% Verde (#03582D / #133522), 3% Amarillo (#FFCC29), cero azul.
- Cero "S.R.L.", cero "Ford Transit", cero adverbios en -mente, cero links a LinkedIn que piden login.
- Todos los botones llevan a www.starunion.com.ar (con UTM de autosegmentación por vertical) o a WhatsApp Comercial B2B (+54 9 11 2275-9369).
"""
import os

BASE_DIR = "/Users/arianawajntraub/Documents/antigravity/star-union"
OUT_DIR = os.path.join(BASE_DIR, "redes-sociales")

# Imágenes públicas alojadas en CDN oficial de Perfit de Star Union + Espejo HTTPS activo
LOGO_URL = "https://cdn.myperfit.net/1726860404581-logo-horizontal-1200x300.png"
TUV_URL = "https://cdn.myperfit.net/1775508730335-TR-Testmark_9000041847_EN_CMYK_with-QR-Code.png"
CLEANY_URL = "https://wajntraub.ar/staruniontest/assets/img/cleany-hd.png"
IMG_LOGISTICA = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-logistica-pallets.jpg"
IMG_TALLER = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-base-maquinas.jpg"
IMG_BIOMETRICO = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-uniforme-oficial.jpg"
IMG_SALUD = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-salud-laboratorio.jpg"
IMG_CLUBES = "https://wajntraub.ar/staruniontest/assets/img/perfit-curadas/perfit-clubes-parquet.jpg"

WA_GENERAL = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20vi%20su%20comunicaci%C3%B3n%20y%20quiero%20solicitar%20una%20propuesta%20t%C3%A9cnica%20de%20limpieza%20para%20nuestra%20organizaci%C3%B3n."
WA_LOGISTICA = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20limpieza%20industrial%20y%20centros%20log%C3%ADsticos."
WA_OFICINAS = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20limpieza%20para%20oficinas%20y%20edificios%20corporativos."
WA_CONSORCIOS = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20limpieza%20para%20consorcios%20y%20edificios."
WA_SALUD = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20servicio%20de%20higiene%20t%C3%A9cnica%20para%20cl%C3%ADnicas%20y%20laboratorios."
WA_EDUCACION = "https://api.whatsapp.com/send?phone=5491122759369&text=Hola%20Star%20Union%2C%20quiero%20consultar%20por%20el%20mantenimiento%20integral%20de%20universidades%2C%20colegios%20y%20clubes."


def build_template_a():
    """
    OPCIÓN A: Editorial Visual Multi-Vertical con Infraestructura 800 m²,
    Tarjetas Fotográficas Autosegmentadoras por Rubro y El Dato Técnico de Cleany.
    """
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Continuidad Operativa e Infraestructura Propia | Star Union</title>
</head>
<body style="margin:0;padding:0;background-color:#F3F4F6;font-family:'Open Sans',Arial,Helvetica,sans-serif;color:#111827;-webkit-font-smoothing:antialiased;">
  <!-- Preheader oculto -->
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    Base Operativa Propia de 800 m² en CABA, Taller Electromecánico In-House, presentismo biométrico (&lt; 2 hs) y procesos certificados ISO 9001:2015 por TÜV Rheinland.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F3F4F6;padding:24px 10px;">
    <tr>
      <td align="center">
        <!-- CONTENEDOR 600PX BLANCO DOMINANTE -->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:16px;overflow:hidden;border:1px solid #E5E7EB;">
          
          <!-- FRANJA SUPERIOR VERDE STAR UNION -->
          <tr>
            <td style="background-color:#03582D;padding:10px 24px;text-align:center;color:#FFFFFF;font-size:12px;font-weight:700;letter-spacing:0.04em;">
              EMPRESA DE LIMPIEZA PROFESIONAL E INDUSTRIAL · DESDE 2001 EN CABA Y GBA
            </td>
          </tr>

          <!-- ENCABEZADO: LOGO + SELLO TÜV RHEINLAND ISO 9001 -->
          <tr>
            <td style="padding:22px 28px 18px 28px;border-bottom:3px solid #03582D;background-color:#FFFFFF;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" width="55%">
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A" target="_blank">
                      <img src="{LOGO_URL}" alt="Star Union" width="190" style="display:block;max-width:190px;height:auto;border:0;">
                    </a>
                  </td>
                  <td align="right" valign="middle" width="45%">
                    <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="text-decoration:none;">
                      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;padding:6px 10px;">
                        <tr>
                          <td valign="middle" style="padding-right:8px;">
                            <img src="{TUV_URL}" alt="TÜV Rheinland ISO 9001" width="38" style="display:block;border:0;">
                          </td>
                          <td align="left" valign="middle" style="font-size:11px;line-height:1.3;color:#111827;">
                            <strong style="color:#03582D;display:block;">ISO 9001:2015</strong>
                            <span style="color:#4B5563;">ID 9000041847</span>
                          </td>
                        </tr>
                      </table>
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- BLOQUE HERO GENERAL (APERTURA DE EMBUDO 1) -->
          <tr>
            <td style="padding:28px 28px 16px 28px;background-color:#FFFFFF;">
              <div style="display:inline-block;background-color:#E6EFEA;color:#03582D;font-size:11px;font-weight:800;padding:5px 12px;border-radius:999px;letter-spacing:0.05em;margin-bottom:12px;">
                INFRAESTRUCTURA PROPIA Y TRAZABILIDAD OPERATIVA B2B
              </div>
              <h1 style="margin:0 0 12px 0;font-size:25px;line-height:1.22;font-weight:800;color:#111827;">
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
                      📲 Solicitar Relevamiento Técnico por WhatsApp
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
                  SELECCIONÁ TU SECTOR PARA RECIBIR EL PROTOCOLO ESPECÍFICO
                </div>
                <h2 style="margin:4px 0 12px 0;font-size:18px;font-weight:800;color:#111827;">
                  Soluciones diseñadas según la exigencia de cada operación:
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
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A&vertical=logistica_industria" target="_blank">
                      <img src="{IMG_LOGISTICA}" alt="Logística e Industria" width="544" style="display:block;width:100%;max-width:544px;height:210px;object-fit:cover;border:0;">
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 20px;">
                    <div style="font-size:11px;font-weight:800;color:#03582D;letter-spacing:0.05em;">1. CENTROS LOGÍSTICOS, DEPÓSITOS Y PLANTAS INDUSTRIALES</div>
                    <h3 style="margin:4px 0 8px 0;font-size:17px;font-weight:800;color:#111827;">Fregado y barrido mecanizado sin detener el despacho</h3>
                    <p style="margin:0 0 12px 0;font-size:13px;line-height:1.5;color:#374151;">
                      Autolavadoras hombre a bordo, barredoras industriales y respaldo de nuestro Taller Electromecánico Propio en Guaminí 5657 para reemplazo de equipos en el día.
                    </p>
                    <a href="{WA_LOGISTICA}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:12px;font-weight:800;text-decoration:none;padding:9px 18px;border-radius:8px;margin-right:8px;">
                      📲 Cotizar Planta / Logística
                    </a>
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A&vertical=logistica_industria" target="_blank" style="display:inline-block;color:#03582D;font-size:12px;font-weight:800;text-decoration:underline;">
                      Ver protocolo industrial →
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
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A&vertical=oficinas_corporativas" target="_blank">
                      <img src="{IMG_BIOMETRICO}" alt="Oficinas y Edificios Corporativos" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">2. OFICINAS Y CORPORATIVOS</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#111827;">Edificios corporativos, bancos y sedes</h3>
                      <p style="margin:0 0 10px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Presentismo validado por reloj biométrico, personal registrado (indemnidad Art. 30 LCT) y supervisión constante.
                      </p>
                      <a href="{WA_OFICINAS}" target="_blank" style="display:inline-block;background-color:#111827;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 14px;border-radius:8px;">
                        📲 Consultar Oficinas →
                      </a>
                    </div>
                  </td>
                  <td width="4%"></td>
                  <!-- CONSORCIOS -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A&vertical=consorcios_edificios" target="_blank">
                      <img src="{IMG_TALLER}" alt="Consorcios y Barrios Cerrados" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">3. CONSORCIOS Y TORRES</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#111827;">Grandes consorcios y barrios cerrados</h3>
                      <p style="margin:0 0 10px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Cobertura de ausencias en menos de 2 horas con guardia móvil propia en CABA y GBA para que ningún turno quede vacío.
                      </p>
                      <a href="{WA_CONSORCIOS}" target="_blank" style="display:inline-block;background-color:#111827;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 14px;border-radius:8px;">
                        📲 Consultar Consorcios →
                      </a>
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
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A&vertical=salud_laboratorios" target="_blank">
                      <img src="{IMG_SALUD}" alt="Clínicas y Laboratorios" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">4. SALUD Y LABORATORIOS</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#111827;">Clínicas, sanatorios y laboratorios</h3>
                      <p style="margin:0 0 10px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Zonificación contra contaminación cruzada e insumos aprobados por ANMAT con hojas de seguridad (MSDS) en planta.
                      </p>
                      <a href="{WA_SALUD}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 14px;border-radius:8px;">
                        📲 Consultar Salud →
                      </a>
                    </div>
                  </td>
                  <td width="4%"></td>
                  <!-- EDUCACIÓN Y CLUBES -->
                  <td width="48%" valign="top" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;">
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A&vertical=educacion_clubes" target="_blank">
                      <img src="{IMG_CLUBES}" alt="Universidades, Colegios y Clubes" width="260" style="display:block;width:100%;height:150px;object-fit:cover;border:0;">
                    </a>
                    <div style="padding:14px;">
                      <div style="font-size:10px;font-weight:800;color:#03582D;">5. EDUCACIÓN Y DEPORTE</div>
                      <h3 style="margin:4px 0 6px 0;font-size:15px;font-weight:800;color:#111827;">Universidades, colegios y clubes</h3>
                      <p style="margin:0 0 10px 0;font-size:12px;line-height:1.45;color:#374151;">
                        Operativos en contraturno, cuidado de pisos deportivos de parquet y preparación para receso y temporada de verano.
                      </p>
                      <a href="{WA_EDUCACION}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:11px;font-weight:800;text-decoration:none;padding:8px 14px;border-radius:8px;">
                        📲 Consultar Predios →
                      </a>
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
                  <td valign="middle" style="font-size:13px;line-height:1.48;color:#111827;">
                    <strong style="color:#03582D;display:block;font-size:12px;letter-spacing:0.04em;">EL DATO TÉCNICO DE CLEANY · TRAZABILIDAD BIOMÉTRICA</strong>
                    Nuestro sistema de reloj biométrico reporta en vivo a la central de calle Guaminí: ante cualquier demora a los <strong>15 minutos</strong> del inicio de turno, se despacha personal de guardia registrado para cubrir el puesto en <strong>menos de 2 horas</strong>.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- PIE INSTITUCIONAL Y CUMPLIMIENTO PERFIT -->
          <tr>
            <td style="background-color:#111827;color:#FFFFFF;padding:24px 28px;text-align:center;">
              <div style="font-size:15px;font-weight:800;margin-bottom:4px;">Star Union · Sabemos de Limpieza</div>
              <div style="font-size:12px;color:#D1D5DB;margin-bottom:12px;">
                Base Operativa Propia (800 m²): Guaminí 5657, CABA · Tel: 0810-333-8646 · WhatsApp B2B: +54 9 11 2275-9369
              </div>
              <div style="margin-bottom:14px;">
                <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_A" target="_blank" style="color:#FFCC29;font-size:12px;font-weight:700;text-decoration:none;margin:0 8px;">Sitio Web Oficial</a> |
                <a href="https://www.instagram.com/starunionservicios/" target="_blank" style="color:#FFFFFF;font-size:12px;text-decoration:none;margin:0 8px;">Instagram</a> |
                <a href="https://www.linkedin.com/company/star-union-srl/" target="_blank" style="color:#FFFFFF;font-size:12px;text-decoration:none;margin:0 8px;">LinkedIn</a> |
                <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="color:#FFFFFF;font-size:12px;text-decoration:none;margin:0 8px;">Certificado TÜV ISO 9001</a>
              </div>
              <div style="font-size:11px;color:#9CA3AF;line-height:1.4;">
                Recibís esta comunicación institucional por formar parte de nuestra red de contactos corporativos.<br>
                Si deseás dejar de recibir novedades, podés <a href="{{{{unsubscribe_link}}}}" style="color:#D1D5DB;text-decoration:underline;">desuscribirte en 1 clic aquí</a>.
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_template_b():
    """
    OPCIÓN B: Ejecutiva de Auditoría, Continuidad y Recambio de Proveedor.
    Entra por los 4 Dolores Críticos B2B (Ausentismo, Parada de Máquinas, Art. 30 LCT, Auditorías ISO/ANMAT)
    + Tabla Comparativa + Selector Rápido de Rubro en 1 Clic.
    """
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auditoría Operativa y Continuidad del Servicio de Limpieza | Star Union</title>
</head>
<body style="margin:0;padding:0;background-color:#F3F4F6;font-family:'Open Sans',Arial,Helvetica,sans-serif;color:#111827;-webkit-font-smoothing:antialiased;">
  <!-- Preheader oculto -->
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    Cómo eliminar puestos vacíos, paradas por maquinaria caída y riesgos laborales solidarios (Art. 30 LCT) con certificación ISO 9001:2015 (TÜV Rheinland).
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F3F4F6;padding:24px 10px;">
    <tr>
      <td align="center">
        <!-- CONTENEDOR 600PX BLANCO DOMINANTE -->
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:16px;overflow:hidden;border:1px solid #E5E7EB;">

          <!-- CABECERA EJECUTIVA -->
          <tr>
            <td style="padding:22px 28px 18px 28px;border-bottom:4px solid #03582D;background-color:#FFFFFF;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" width="55%">
                    <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_B" target="_blank">
                      <img src="{LOGO_URL}" alt="Star Union" width="190" style="display:block;max-width:190px;height:auto;border:0;">
                    </a>
                  </td>
                  <td align="right" valign="middle" width="45%">
                    <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="text-decoration:none;">
                      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="background-color:#F9FAFB;border:1px solid #E5E7EB;border-radius:10px;padding:6px 10px;">
                        <tr>
                          <td valign="middle" style="padding-right:8px;">
                            <img src="{TUV_URL}" alt="TÜV Rheinland ISO 9001" width="38" style="display:block;border:0;">
                          </td>
                          <td align="left" valign="middle" style="font-size:11px;line-height:1.3;color:#111827;">
                            <strong style="color:#03582D;display:block;">ISO 9001:2015</strong>
                            <span style="color:#4B5563;">TÜV ID 9000041847</span>
                          </td>
                        </tr>
                      </table>
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- APERTURA EJECUTIVA DE DIAGNÓSTICO B2B -->
          <tr>
            <td style="padding:28px 28px 14px 28px;background-color:#FFFFFF;">
              <div style="display:inline-block;background-color:#E6EFEA;color:#03582D;font-size:11px;font-weight:800;padding:5px 12px;border-radius:999px;letter-spacing:0.05em;margin-bottom:12px;">
                DIAGNÓSTICO DE PROVEEDORES Y PREVISIBILIDAD OPERATIVA
              </div>
              <h1 style="margin:0 0 12px 0;font-size:24px;line-height:1.24;font-weight:800;color:#111827;">
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
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#111827;">1. Puestos vacíos por ausencias imprevistas</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Reloj biométrico en tiempo real:</strong> alerta a los 15 min y cobertura en <strong>menos de 2 horas</strong> con guardia móvil propia.</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;background-color:#F9FAFB;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#111827;">2. Servicio frenado por máquinas averiadas</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Taller Electromecánico Propio (800 m² CABA):</strong> mantenimiento preventivo y reemplazo de equipos en el día.</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;background-color:#FFFFFF;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#111827;">3. Contingencia laboral solidaria (Art. 30 LCT)</td>
                  <td style="padding:12px 14px;font-size:12px;color:#374151;"><strong style="color:#03582D;">Indemnidad documental:</strong> 100% del personal en relación de dependencia con entrega mensual de F.931, ART y seguros.</td>
                </tr>
                <tr style="background-color:#F9FAFB;">
                  <td style="padding:12px 14px;font-size:12px;font-weight:700;color:#111827;">4. Desvíos en auditorías de calidad o salud</td>
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
                    <strong style="color:#111827;">Respaldo físico verificable en CABA:</strong> Operamos desde nuestra Base Central Propia de 800 m² (3 niveles) en Guaminí 5657 con stock permanente de insumos, aula de capacitación y flota propia de asistencia técnica.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- SELECTOR AUTO-SEGMENTADOR EN 1 CLIC (DISPARA ETAPA 2 DEL FUNNEL) -->
          <tr>
            <td style="padding:4px 28px 20px 28px;">
              <div style="font-size:12px;font-weight:800;color:#03582D;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">
                INDICÁ TU RUBRO EN 1 CLIC PARA RECIBIR UNA PROPUESTA A MEDIDA:
              </div>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="padding:5px 0;">
                    <a href="{WA_LOGISTICA}" target="_blank" style="display:block;background-color:#F9FAFB;border:1.5px solid #03582D;border-radius:10px;padding:11px 16px;text-decoration:none;color:#111827;font-size:13px;font-weight:800;">
                      🏭 1. Centros Logísticos, Depósitos y Plantas Industriales <span style="float:right;color:#03582D;">Solicitar relevamiento →</span>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:5px 0;">
                    <a href="{WA_OFICINAS}" target="_blank" style="display:block;background-color:#F9FAFB;border:1.5px solid #03582D;border-radius:10px;padding:11px 16px;text-decoration:none;color:#111827;font-size:13px;font-weight:800;">
                      🏢 2. Oficinas Corporativas, Bancos y Centros Comerciales <span style="float:right;color:#03582D;">Solicitar relevamiento →</span>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:5px 0;">
                    <a href="{WA_CONSORCIOS}" target="_blank" style="display:block;background-color:#F9FAFB;border:1.5px solid #03582D;border-radius:10px;padding:11px 16px;text-decoration:none;color:#111827;font-size:13px;font-weight:800;">
                      🏙️ 3. Grandes Consorcios, Edificios y Barrios Cerrados <span style="float:right;color:#03582D;">Solicitar relevamiento →</span>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:5px 0;">
                    <a href="{WA_SALUD}" target="_blank" style="display:block;background-color:#F9FAFB;border:1.5px solid #03582D;border-radius:10px;padding:11px 16px;text-decoration:none;color:#111827;font-size:13px;font-weight:800;">
                      🏥 4. Clínicas, Sanatorios y Laboratorios (Protocolo ANMAT) <span style="float:right;color:#03582D;">Solicitar relevamiento →</span>
                    </a>
                  </td>
                </tr>
                <tr>
                  <td style="padding:5px 0;">
                    <a href="{WA_EDUCACION}" target="_blank" style="display:block;background-color:#F9FAFB;border:1.5px solid #03582D;border-radius:10px;padding:11px 16px;text-decoration:none;color:#111827;font-size:13px;font-weight:800;">
                      🎓 5. Universidades, Colegios Bilingües y Clubes Deportivos <span style="float:right;color:#03582D;">Solicitar relevamiento →</span>
                    </a>
                  </td>
                </tr>
              </table>

              <div style="text-align:center;margin-top:18px;">
                <a href="{WA_GENERAL}" target="_blank" style="display:inline-block;background-color:#03582D;color:#FFFFFF;font-size:14px;font-weight:800;text-decoration:none;padding:14px 28px;border-radius:999px;border-bottom:3px solid #FFCC29;">
                  📲 Hablar Ahora con Dirección Comercial por WhatsApp
                </a>
              </div>
            </td>
          </tr>

          <!-- PIE INSTITUCIONAL Y CUMPLIMIENTO PERFIT -->
          <tr>
            <td style="background-color:#111827;color:#FFFFFF;padding:24px 28px;text-align:center;">
              <div style="font-size:15px;font-weight:800;margin-bottom:4px;">Star Union · Sabemos de Limpieza</div>
              <div style="font-size:12px;color:#D1D5DB;margin-bottom:12px;">
                Base Operativa Propia (800 m²): Guaminí 5657, CABA · Tel: 0810-333-8646 · WhatsApp B2B: +54 9 11 2275-9369
              </div>
              <div style="margin-bottom:14px;">
                <a href="https://www.starunion.com.ar/?utm_source=perfit&utm_medium=email&utm_campaign=funnel1_apertura_B" target="_blank" style="color:#FFCC29;font-size:12px;font-weight:700;text-decoration:none;margin:0 8px;">Sitio Web Oficial</a> |
                <a href="https://www.instagram.com/starunionservicios/" target="_blank" style="color:#FFFFFF;font-size:12px;text-decoration:none;margin:0 8px;">Instagram</a> |
                <a href="https://www.linkedin.com/company/star-union-srl/" target="_blank" style="color:#FFFFFF;font-size:12px;text-decoration:none;margin:0 8px;">LinkedIn</a> |
                <a href="https://www.certipedia.com/quality_marks/9000041847" target="_blank" style="color:#FFFFFF;font-size:12px;text-decoration:none;margin:0 8px;">Certificado TÜV ISO 9001</a>
              </div>
              <div style="font-size:11px;color:#9CA3AF;line-height:1.4;">
                Recibís esta comunicación institucional por formar parte de nuestra red de contactos corporativos.<br>
                Si deseás dejar de recibir novedades, podés <a href="{{{{unsubscribe_link}}}}" style="color:#D1D5DB;text-decoration:underline;">desuscribirte en 1 clic aquí</a>.
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_showcase_html(html_a, html_b):
    import html as html_mod
    esc_a = html_mod.escape(html_a)
    esc_b = html_mod.escape(html_b)

    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Propuesta de Embudo B2B + Plantillas HTML Mailing A y B | Star Union</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Open Sans', sans-serif; background: #f9fafb; color: #111827; }}
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
            📧 MAILING + EMBUDO B2B INTEGRADO A LAS 5 REDES · CONECTADO A PERFIT API
          </span>
          <h1 class="text-xl sm:text-2xl font-extrabold text-gray-900">Propuesta de Embudo (Funnel 1) + Comparador en Vivo de Plantillas HTML A y B</h1>
          <p class="text-xs text-gray-600 mt-0.5">Diseñado con todo el aprendizaje de las 93 campañas históricas de Star Union: 85% Blanco Dominante, cero links que reboten en login de LinkedIn, cero "S.R.L.", cero "Ford Transit" y autosegmentación en 1 clic hacia WhatsApp Comercial.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2">
        <a href="index.html" class="bg-gray-900 hover:bg-black text-white text-xs font-extrabold px-4 py-2.5 rounded-xl transition">
          ← Volver a la Cabina de Redes y Calendario
        </a>
        <a href="../radar-comercial/perfit-historial/index.html" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold px-4 py-2.5 rounded-xl transition">
          📊 Ver Historial Perfit (93 Campañas)
        </a>
      </div>
    </div>

    <!-- 1. ARQUITECTURA DEL EMBUDO B2B (POR QUÉ EL EMAIL 1 ES GENÉRICO PARAGUAS Y CÓMO CONVIERTE) -->
    <div class="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-5">
      <div>
        <span class="text-xs font-extrabold uppercase text-[#03582d]">1. Arquitectura del Embudo Comercial B2B (Perfit + Redes + WhatsApp)</span>
        <h2 class="text-lg sm:text-xl font-extrabold text-gray-900 mt-0.5">Cómo funciona el Funnel 1 desde el Mailing Inicial Genérico hasta la Visita Técnica</h2>
        <p class="text-xs text-gray-600 mt-1">
          <strong>¿Qué corregimos respecto a los mailings anteriores (#116/#119)?</strong> En los envíos viejos, los botones de las fotos llevaban a posteos de LinkedIn (donde el usuario sin sesión rebota) en vez de capturar el interés por rubro. Ahora el <strong>Email #1 Inicial Genérico</strong> actúa como un <strong>Filtro Autosegmentador</strong> que lleva directo a WhatsApp con mensaje pre-armado por vertical o al sitio oficial con UTM de seguimiento.
        </p>
      </div>

      <div class="grid md:grid-cols-4 gap-4 text-xs">
        <div class="bg-emerald-50/70 p-4 rounded-xl border-2 border-[#03582d] space-y-2">
          <span class="inline-block bg-[#03582d] text-white font-extrabold px-2.5 py-0.5 rounded-full text-[10px]">ETAPA 1 · JUEVES 10:00 HS</span>
          <h3 class="font-extrabold text-sm text-gray-900">Mailing Inicial de Apertura de Funnel 1 (Genérico Multi-Vertical)</h3>
          <p class="text-gray-700 leading-relaxed">
            Sale a la <strong>Lista Fidelizada (63%-72% apertura)</strong> y a la <strong>Lista General Depurada</strong>. Presenta el respaldo común (Base 800 m² Guaminí + Taller Propio + Biométrico &lt;2 hs + ISO 9001 TÜV) y ofrece los <strong>5 botones de rubro</strong> para que el lector se autosegmente con 1 clic.
          </p>
        </div>

        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2">
          <span class="inline-block bg-gray-900 text-white font-extrabold px-2.5 py-0.5 rounded-full text-[10px]">ETAPA 2 · MARTES (+5 DÍAS)</span>
          <h3 class="font-extrabold text-sm text-gray-900">2° Pasada Automática solo a No-Abridores (+21,8% Aperturas)</h3>
          <p class="text-gray-700 leading-relaxed">
            A los 5 días, quienes no abrieron la Etapa 1 reciben el envío con <strong>Asunto cambiado</strong> (enfocado en <em>Control de Presentismo Biométrico y Blindaje Art. 30 LCT</em>). Si usaste la Plantilla A en el envío 1, podés usar la Plantilla B en el reenvío.
          </p>
        </div>

        <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-2">
          <span class="inline-block bg-[#03582d] text-white font-extrabold px-2.5 py-0.5 rounded-full text-[10px]">ETAPA 3 · AUTOMÁTICA POR CLIC</span>
          <h3 class="font-extrabold text-sm text-gray-900">Etiquetado por Rubro en Perfit + Derivación a WhatsApp B2B</h3>
          <p class="text-gray-700 leading-relaxed">
            Cada clic en Logística, Oficinas, Consorcios, Salud o Educación abre un <strong>WhatsApp pre-redactado de ese sector</strong> (+54 9 11 2275-9369) y deja marcado el interés del contacto en Perfit para enviarle el brochure técnico de su vertical.
          </p>
        </div>

        <div class="bg-amber-50/80 p-4 rounded-xl border border-amber-300 space-y-2">
          <span class="inline-block bg-amber-500 text-gray-950 font-extrabold px-2.5 py-0.5 rounded-full text-[10px]">ETAPA 4 · RETROALIMENTACIÓN</span>
          <h3 class="font-extrabold text-sm text-gray-900">Alimentación Directa del Calendario de las 5 Redes</h3>
          <p class="text-gray-700 leading-relaxed">
            El rubro con más clics del mailing pasa a encabezar la tanda de publicaciones en <strong>IG, FB, Google Maps, YouTube Shorts y TikTok</strong> de la quincena siguiente, cerrando el círculo comercial.
          </p>
        </div>
      </div>
    </div>

    <!-- 2. COMPARADOR LADO A LADO DE LAS 2 PLANTILLAS HTML (OPCIÓN A vs. OPCIÓN B) -->
    <div class="grid lg:grid-cols-2 gap-6 items-start">

      <!-- COLUMNA OPCIÓN A -->
      <div class="bg-white rounded-2xl border-2 border-[#03582d] shadow-sm overflow-hidden flex flex-col">
        <div class="bg-emerald-50/80 p-5 border-b border-gray-200 space-y-3">
          <div class="flex items-center justify-between gap-2">
            <span class="bg-[#03582d] text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase">OPCIÓN A · Editorial Visual + 5 Verticales + Cleany</span>
            <a href="mailing-apertura-funnel1-opcion-A.html" target="_blank" class="text-xs font-extrabold text-[#03582d] underline">Abrir sola en pestaña ↗</a>
          </div>
          <h2 class="text-lg font-extrabold text-gray-900">Plantilla A: Infraestructura 800 m² + Tarjetas Fotográficas por Sector + Dato Técnico de Cleany</h2>
          <p class="text-xs text-gray-700">
            <strong>Por qué elegir la A:</strong> Mantiene el formato visual de tarjetas con fotografía operativa real que la base de Star Union ya reconoce, pero reemplaza todos los links viejos por botones directos de conversión por rubro y suma los 3 KPIs físicos arriba.
          </p>
          <div class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-xs">
            <div><strong class="text-gray-600">Asunto Editable A:</strong></div>
            <input id="subj_A" type="text" value="Infraestructura propia de 800 m² y continuidad operativa ISO 9001 º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-gray-300 font-bold text-gray-900">
          </div>
          <div class="grid sm:grid-cols-3 gap-2 pt-1">
            <button type="button" onclick="copyHtml('code_A', this)" class="bg-gray-900 hover:bg-black text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              📋 Copiar HTML Opción A
            </button>
            <a href="mailing-apertura-funnel1-opcion-A.html" download="STAR_UNION_MAILING_FUNNEL1_OPCION_A.html" class="bg-white border-2 border-gray-800 text-gray-900 hover:bg-gray-100 text-center text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              ⬇ Descargar .HTML (A)
            </a>
            <button type="button" onclick="pushDraftToPerfit('A', this)" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition shadow-sm">
              🚀 Crear Borrador en Perfit (API)
            </button>
          </div>
          <div id="perfit_res_A" class="hidden text-xs font-bold p-2.5 rounded-lg bg-white border border-gray-200"></div>
        </div>

        <div class="p-4 bg-gray-100">
          <iframe src="mailing-apertura-funnel1-opcion-A.html" class="w-full h-[980px] bg-white rounded-xl border border-gray-300 shadow-inner"></iframe>
        </div>
        <textarea id="code_A" class="hidden">{esc_a}</textarea>
      </div>

      <!-- COLUMNA OPCIÓN B -->
      <div class="bg-white rounded-2xl border-2 border-gray-800 shadow-sm overflow-hidden flex flex-col">
        <div class="bg-gray-50 p-5 border-b border-gray-200 space-y-3">
          <div class="flex items-center justify-between gap-2">
            <span class="bg-gray-900 text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase">OPCIÓN B · Ejecutiva de Auditoría + Los 4 Dolores Resueltos</span>
            <a href="mailing-apertura-funnel1-opcion-B.html" target="_blank" class="text-xs font-extrabold text-[#03582d] underline">Abrir sola en pestaña ↗</a>
          </div>
          <h2 class="text-lg font-extrabold text-gray-900">Plantilla B: Matriz de los 4 Riesgos Operativos Resueltos + Selector Rápido de Rubro en 1 Clic</h2>
          <p class="text-xs text-gray-700">
            <strong>Por qué elegir la B (o usarla en el Reenvío +5 días):</strong> Va directo al hueso del decisor de Compras, Operaciones o Administración: muestra en una tabla limpia cómo Star Union resuelve el ausentismo (&lt;2 hs), las máquinas paradas (Taller propio), el riesgo Art. 30 LCT y las auditorías ISO/ANMAT.
          </p>
          <div class="bg-white p-3 rounded-xl border border-gray-200 space-y-1.5 text-xs">
            <div><strong class="text-gray-600">Asunto Editable B:</strong></div>
            <input id="subj_B" type="text" value="¿Tu operación está cubierta hoy ante ausencias, fallas de máquinas o auditorías? º Star ⭐ Union" class="w-full px-2.5 py-1.5 rounded border border-gray-300 font-bold text-gray-900">
          </div>
          <div class="grid sm:grid-cols-3 gap-2 pt-1">
            <button type="button" onclick="copyHtml('code_B', this)" class="bg-gray-900 hover:bg-black text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              📋 Copiar HTML Opción B
            </button>
            <a href="mailing-apertura-funnel1-opcion-B.html" download="STAR_UNION_MAILING_FUNNEL1_OPCION_B.html" class="bg-white border-2 border-gray-800 text-gray-900 hover:bg-gray-100 text-center text-xs font-extrabold py-2.5 px-3 rounded-xl transition">
              ⬇ Descargar .HTML (B)
            </a>
            <button type="button" onclick="pushDraftToPerfit('B', this)" class="bg-[#03582d] hover:bg-[#133522] text-white text-xs font-extrabold py-2.5 px-3 rounded-xl transition shadow-sm">
              🚀 Crear Borrador en Perfit (API)
            </button>
          </div>
          <div id="perfit_res_B" class="hidden text-xs font-bold p-2.5 rounded-lg bg-white border border-gray-200"></div>
        </div>

        <div class="p-4 bg-gray-100">
          <iframe src="mailing-apertura-funnel1-opcion-B.html" class="w-full h-[980px] bg-white rounded-xl border border-gray-300 shadow-inner"></iframe>
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
