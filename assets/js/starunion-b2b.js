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
