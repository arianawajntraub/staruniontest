/**
 * STAR UNION S.R.L. — MOTOR DE CONVERSIÓN B2B, FILTRO ANTI-CHICOS Y ENVÍO A COMERCIAL@STARUNION.COM.AR
 */

document.addEventListener('DOMContentLoaded', () => {
  const b2bForms = document.querySelectorAll('.js-b2b-quote-form');

  b2bForms.forEach((form) => {
    const tipoSelect = form.querySelector('[name="tipo_organizacion"]');
    const otroWrap = form.querySelector('.js-otro-rubro-wrap');
    const otroInput = form.querySelector('[name="otro_rubro_detalle"]');
    const warningBox = form.querySelector('.b2b-warning-alert');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (tipoSelect) {
      tipoSelect.addEventListener('change', () => {
        const val = tipoSelect.value;

        if (otroWrap && otroInput) {
          if (val === 'Otro rubro o establecimiento (especificar)') {
            otroWrap.classList.remove('hidden');
            otroInput.required = true;
          } else {
            otroWrap.classList.add('hidden');
            otroInput.required = false;
            otroInput.value = '';
          }
        }

        if (warningBox) {
          if (val === 'NO_CALIFICA_PARTICULAR' || val === 'NO_CALIFICA_CONSORCIO_CHICO') {
            warningBox.classList.remove('hidden');
            warningBox.style.display = 'block';
            if (submitBtn) {
              submitBtn.disabled = true;
              submitBtn.style.opacity = '0.45';
              submitBtn.style.cursor = 'not-allowed';
            }
          } else {
            warningBox.classList.add('hidden');
            warningBox.style.display = 'none';
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.style.opacity = '1';
              submitBtn.style.cursor = 'pointer';
            }
          }
        }
      });
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const empresa = (form.querySelector('[name="empresa"]')?.value || '').trim();
      const nombre = (form.querySelector('[name="nombre"]')?.value || '').trim();
      const cargo = (form.querySelector('[name="cargo"]')?.value || '').trim();
      const email = (form.querySelector('[name="email"]')?.value || '').trim();
      const telefono = (form.querySelector('[name="telefono"]')?.value || '').trim();
      const contacto = cargo || [email, telefono].filter(Boolean).join(' · ');

      const tipoBase = form.querySelector('[name="tipo_organizacion"]')?.value || '';
      const otroDetalle = (form.querySelector('[name="otro_rubro_detalle"]')?.value || '').trim();
      const tipo = (tipoBase === 'Otro rubro o establecimiento (especificar)' && otroDetalle)
        ? `Otro rubro: ${otroDetalle}`
        : tipoBase;

      const cantidadPersonas = (form.querySelector('[name="cantidad_personas"]')?.value || '').trim();
      const cantidadHoras = (form.querySelector('[name="cantidad_horas"]')?.value || '').trim();
      const diasServicio = (form.querySelector('[name="dias_servicio"]')?.value || '').trim();
      const jornada = (form.querySelector('[name="jornada"]')?.value || '').trim();
      const ubicacion = (form.querySelector('[name="ubicacion"]')?.value || '').trim();
      const escala = (form.querySelector('[name="escala"]')?.value || '').trim();
      const mensaje = (form.querySelector('[name="mensaje"]')?.value || '').trim();
      const detalle = escala || mensaje;

      if (tipoBase === 'NO_CALIFICA_PARTICULAR' || tipoBase === 'NO_CALIFICA_CONSORCIO_CHICO') {
        if (warningBox) {
          warningBox.classList.remove('hidden');
          warningBox.style.display = 'block';
        }
        return;
      }

      // Evento de conversión limpia para GA4 / Google Ads (Solo B2B calificado)
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'lead_b2b_calificado_starunion',
        b2b_vertical: tipo,
        b2b_headcount: cantidadPersonas,
        b2b_hours: cantidadHoras,
        b2b_days: diasServicio,
        b2b_shift: jornada,
        b2b_location: ubicacion
      });

      const asunto = `Solicitud de presupuesto B2B: ${empresa}${tipo ? ` (${tipo})` : ''}`;
      const cuerpo = [
        `Solicitud de presupuesto operativo B2B — Star Union S.R.L.`,
        `----------------------------------------------------------------------`,
        `• Empresa o institución: ${empresa}`,
        `• Contacto: ${nombre}`,
        `• Email o teléfono: ${contacto}`,
        `• Tipo de servicio o rubro: ${tipo}`,
        cantidadPersonas ? `• Cantidad de personas (operarios): ${cantidadPersonas}` : '',
        cantidadHoras ? `• Cantidad de horas: ${cantidadHoras}` : '',
        diasServicio ? `• Días de servicio: ${diasServicio}` : '',
        jornada ? `• Jornada: ${jornada}` : '',
        ubicacion ? `• Localidad o ubicación del servicio: ${ubicacion}` : '',
        detalle ? `• Observaciones adicionales: ${detalle}` : ''
      ].filter(Boolean).join('\n');

      // Abre correo directo hacia comercial@starunion.com.ar (la casilla activa de la oficina)
      const mailtoLink = `mailto:comercial@starunion.com.ar?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
      window.location.href = mailtoLink;
    });
  });
});


// Micro-filtro tecnológico en botones de WhatsApp (separa empresas de postulantes RRHH)
document.addEventListener("DOMContentLoaded", function () {
  var waLinks = document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]');
  if (!waLinks.length) return;

  var modal = document.getElementById("su-wa-filter-modal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "su-wa-filter-modal";
    modal.style.cssText = "display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.55);align-items:center;justify-content:center;padding:16px;";
    modal.innerHTML = [
      "<div style='background:#ffffff;max-width:420px;width:100%;border-radius:16px;padding:24px;box-shadow:0 20px 40px rgba(0,0,0,0.25);border-top:5px solid #03582d;font-family:\"Open Sans\",sans-serif;'>",
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>",
          "<span style='font-size:11px;font-weight:800;text-transform:uppercase;color:#03582d;letter-spacing:0.05em;'>Atención directa Star Union</span>",
          "<button type='button' id='su-wa-close' style='background:none;border:none;font-size:18px;cursor:pointer;color:#6b7280;'>✕</button>",
        "</div>",
        "<h3 style='font-size:18px;font-weight:800;color:#000000;margin:0 0 6px 0;'>¿Con qué área querés comunicarte?</h3>",
        "<p style='font-size:13px;color:#4b5563;margin:0 0 16px 0;line-height:1.45;'>Seleccioná una opción para derivarte de inmediato con el equipo correspondiente:</p>",
        "<div style='display:flex;flex-direction:column;gap:10px;'>",
          "<a id='su-wa-go-b2b' href='#' target='_blank' style='display:block;text-align:center;background:#03582d;color:#ffffff;font-weight:800;font-size:13.5px;padding:14px 16px;border-radius:10px;text-decoration:none;'>🏢 Solicitar cotización para mi empresa o institución →</a>",
          "<a id='su-wa-go-rrhh' href='/index.html#postularse' style='display:block;text-align:center;background:#f3f4f6;color:#111827;font-weight:700;font-size:13px;padding:12px 16px;border-radius:10px;text-decoration:none;border:1px solid #d1d5db;'>👷 Busco trabajo / enviar CV a Recursos Humanos</a>",
        "</div>",
      "</div>"
    ].join("");
    document.body.appendChild(modal);

    document.getElementById("su-wa-close").addEventListener("click", function () {
      modal.style.display = "none";
    });
    modal.addEventListener("click", function (e) {
      if (e.target === modal) modal.style.display = "none";
    });

    document.getElementById("su-wa-go-b2b").addEventListener("click", function () {
      if (typeof window.gtag === "function") {
        window.gtag("event", "contacto_wa_empresa_b2b", { event_category: "B2B_Lead" });
      }
      modal.style.display = "none";
    });

    document.getElementById("su-wa-go-rrhh").addEventListener("click", function () {
      modal.style.display = "none";
    });
  }

  waLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      var targetHref = link.getAttribute("href");
      var b2bBtn = document.getElementById("su-wa-go-b2b");
      b2bBtn.setAttribute("href", targetHref);
      modal.style.display = "flex";
    });
  });
});
