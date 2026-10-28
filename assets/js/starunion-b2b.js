/**
 * STAR UNION S.R.L. — MOTOR DE CONVERSIÓN B2B, FILTRO ANTI-CHICOS Y ENVÍO A COMERCIAL@STARUNION.COM.AR
 */

document.addEventListener('DOMContentLoaded', () => {
  const b2bForms = document.querySelectorAll('.js-b2b-quote-form');

  b2bForms.forEach((form) => {
    const tipoSelect = form.querySelector('[name="tipo_organizacion"]');
    const warningBox = form.querySelector('.b2b-warning-alert');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (tipoSelect && warningBox) {
      tipoSelect.addEventListener('change', () => {
        const val = tipoSelect.value;
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
      });
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const empresa = (form.querySelector('[name="empresa"]')?.value || '').trim();
      const nombre = (form.querySelector('[name="nombre"]')?.value || '').trim();
      const cargo = (form.querySelector('[name="cargo"]')?.value || '').trim();
      const tipo = form.querySelector('[name="tipo_organizacion"]')?.value || '';
      const servicio = form.querySelector('[name="servicio_requerido"]')?.value || 'Relevamiento Técnico B2B';
      const ubicacion = form.querySelector('[name="ubicacion"]')?.value || 'AMBA';
      const escala = form.querySelector('[name="escala"]')?.value || '';

      if (tipo === 'NO_CALIFICA_PARTICULAR' || tipo === 'NO_CALIFICA_CONSORCIO_CHICO') {
        if (warningBox) {
          warningBox.classList.remove('hidden');
          warningBox.style.display = 'block';
        }
        return;
      }

      // Evento de conversión limpia para GA4 / Google Ads (Solo B2B Calificado)
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'lead_b2b_calificado_starunion',
        b2b_vertical: tipo,
        b2b_service: servicio,
        b2b_location: ubicacion
      });

      const asunto = `Solicitud de Presupuesto B2B: ${empresa} (${tipo})`;
      const cuerpo = [
        `Solicitud de Relevamiento Técnico / Presupuesto B2B — Star Union S.R.L.`,
        `----------------------------------------------------------------------`,
        `• Empresa / Institución: ${empresa}`,
        `• Contacto: ${nombre}`,
        `• Email / Teléfono: ${cargo}`,
        `• Vertical: ${tipo}`,
        `• Requerimiento: ${servicio}`,
        `• Ubicación: ${ubicacion}`,
        escala ? `• Detalle adicional: ${escala}` : ''
      ].filter(Boolean).join('\n');

      // Abre correo directo hacia comercial@starunion.com.ar (la casilla activa de la oficina)
      const mailtoLink = `mailto:comercial@starunion.com.ar?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
      window.location.href = mailtoLink;
    });
  });
});


// Micro-Filtro Tecnológico en Botones de WhatsApp (Separa Empresas de Postulantes RRHH sin carteles agresivos)
document.addEventListener("DOMContentLoaded", function () {
  var waLinks = document.querySelectorAll("a[href*="api.whatsapp.com"], a[href*="wa.me"]");
  if (!waLinks.length) return;

  var modal = document.createElement("div");
  modal.id = "su-wa-filter-modal";
  modal.style.cssText = "display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.55);align-items:center;justify-content:center;padding:16px;";
  modal.innerHTML = [
    "<div style="background:#ffffff;max-width:420px;width:100%;border-radius:16px;padding:24px;box-shadow:0 20px 40px rgba(0,0,0,0.25);border-top:5px solid #03582d;font-family:Inter,sans-serif;">",
      "<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">",
        "<span style="font-size:11px;font-weight:800;text-transform:uppercase;color:#03582d;letter-spacing:0.05em;">Atención Directa Star Union</span>",
        "<button type="button" id="su-wa-close" style="background:none;border:none;font-size:18px;cursor:pointer;color:#6b7280;">✕</button>",
      "</div>",
      "<h3 style="font-size:18px;font-weight:800;color:#000000;margin:0 0 6px 0;">¿Con qué área querés comunicarte?</h3>",
      "<p style="font-size:13px;color:#4b5563;margin:0 0 16px 0;line-height:1.45;">Seleccioná una opción para derivarte de inmediato con el equipo correspondiente:</p>",
      "<div style="display:flex;flex-direction:column;gap:10px;">",
        "<a id="su-wa-go-b2b" href="#" target="_blank" style="display:block;text-align:center;background:#03582d;color:#ffffff;font-weight:800;font-size:13.5px;padding:14px 16px;border-radius:10px;text-decoration:none;">🏢 Solicitar Cotización para mi Empresa / Institución →</a>",
        "<a id="su-wa-go-rrhh" href="/index.html#postularse" style="display:block;text-align:center;background:#f3f4f6;color:#111827;font-weight:700;font-size:13px;padding:12px 16px;border-radius:10px;text-decoration:none;border:1px solid #d1d5db;">👷 Busco Trabajo / Enviar CV a Recursos Humanos</a>",
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

  waLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      var targetHref = link.getAttribute("href");
      var b2bBtn = document.getElementById("su-wa-go-b2b");
      b2bBtn.setAttribute("href", targetHref);
      modal.style.display = "flex";
    });
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
});
