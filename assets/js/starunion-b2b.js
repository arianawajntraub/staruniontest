/**
 * STAR UNION S.R.L. — MOTOR DE CONVERSIÓN B2B, FILTRO ANTI-CHICOS Y TRACKING GA4/ADS
 * Exclusivo Empresas, Industrias, Edificios Corporativos, Salud e Instituciones.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. FILTRO DEL CATÁLOGO DE CASOS DE ÉXITO POR VERTICAL
  const filterTabs = document.querySelectorAll('[data-case-filter]');
  const caseCards = document.querySelectorAll('[data-case-category]');

  if (filterTabs.length > 0 && caseCards.length > 0) {
    filterTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const target = tab.getAttribute('data-case-filter');
        filterTabs.forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');

        caseCards.forEach((card) => {
          const cats = card.getAttribute('data-case-category') || '';
          if (target === 'all' || cats.includes(target)) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 2. FORMULARIO DE COTIZACIÓN B2B CON BLOQUEO DE CUENTAS CHICAS / PARTICULARES
  const b2bForms = document.querySelectorAll('.js-b2b-quote-form');

  b2bForms.forEach((form) => {
    const tipoSelect = form.querySelector('[name="tipo_organizacion"]');
    const warningBox = form.querySelector('.b2b-warning-alert');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (tipoSelect && warningBox) {
      tipoSelect.addEventListener('change', () => {
        const val = tipoSelect.value;
        if (val === 'NO_CALIFICA_PARTICULAR' || val === 'NO_CALIFICA_CONSORCIO_CHICO') {
          warningBox.style.display = 'block';
          if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.45';
            submitBtn.style.cursor = 'not-allowed';
          }
        } else {
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
      const servicio = form.querySelector('[name="servicio_requerido"]')?.value || '';
      const ubicacion = form.querySelector('[name="ubicacion"]')?.value || '';
      const escala = form.querySelector('[name="escala"]')?.value || '';

      if (tipo === 'NO_CALIFICA_PARTICULAR' || tipo === 'NO_CALIFICA_CONSORCIO_CHICO') {
        if (warningBox) warningBox.style.display = 'block';
        return;
      }

      // Disparo de evento de conversión limpia (Solo B2B Calificado) para GA4 / Google Ads
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'lead_b2b_calificado_starunion',
        b2b_vertical: tipo,
        b2b_service: servicio,
        b2b_location: ubicacion,
        b2b_scale: escala
      });

      const textoWA = [
        `Hola equipo comercial de *Star Union S.R.L.*, solicito cotización B2B / Relevamiento Técnico:`,
        `• *Empresa / Institución:* ${empresa}`,
        `• *Contacto:* ${nombre}${cargo ? ' (' + cargo + ')' : ''}`,
        `• *Vertical:* ${tipo}`,
        `• *Servicio requerido:* ${servicio}`,
        `• *Ubicación / Sede:* ${ubicacion}`,
        `• *Escala / Frecuencia:* ${escala}`
      ].join('\n');

      const waUrl = `https://wa.me/5491122759369?text=${encodeURIComponent(textoWA)}`;
      window.open(waUrl, '_blank', 'noopener,noreferrer');
    });
  });
});
