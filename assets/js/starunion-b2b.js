/**
 * STAR UNION S.R.L. — MOTOR CORPORATIVO DE COTIZACIÓN PASO A PASO Y DERIVACIÓN DE LAS 3 PUERTAS
 * 1) Cotizador conversacional paso a paso (Paso 1 → 2 → 3) con fondo traslúcido (backdrop-blur) para celular y escritorio.
 * 2) Envío directo a Comercial (api/cotizar.php) con Reply-To real del cliente + evento limpio GA4/Ads.
 * 3) Derivación de 3 puertas en WhatsApp: Empresas -> WhatsApp contextual | RRHH -> Formulario online en pestaña nueva | Proveedores -> vista aislada compras@.
 */

(function () {
  var RRHH_GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/1DNqTP8ulFgupMDxXNAVVS9XWzghCX99wbGdbEYLCEVk/viewform';
  var EMAIL_COMPRAS = 'compras@starunion.com.ar';
  var WA_PHONE = '5491122759369';

  function resolveBaseRoot() {
    var scripts = document.querySelectorAll('script[src*="starunion-b2b.js"]');
    if (scripts.length) {
      var src = scripts[0].getAttribute('src') || '';
      return src.split('assets/js/starunion-b2b.js')[0];
    }
    return '/';
  }

  function resolveApiUrl() {
    return resolveBaseRoot() + 'api/cotizar.php';
  }

  function copyPlainText(text, btn, feedbackText) {
    if (!navigator.clipboard) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (err) {}
      document.body.removeChild(ta);
    } else {
      navigator.clipboard.writeText(text).catch(function () {});
    }
    if (btn) {
      var orig = btn.getAttribute('data-orig-label') || btn.textContent;
      btn.setAttribute('data-orig-label', orig);
      btn.textContent = feedbackText || '✓ Copiado';
      setTimeout(function () {
        btn.textContent = orig;
      }, 2200);
    }
  }

  function detectPageDefaults() {
    var p = (window.location.pathname || '').toLowerCase();
    var res = { rubro: '', especialidad: '', otroDetalle: '', localidad: '' };
    if (p.indexOf('/limpieza-industrial') !== -1) {
      res.rubro = 'Plantas industriales, fábricas y centros logísticos';
    } else if (p.indexOf('/oficinas-corporativas') !== -1) {
      res.rubro = 'Edificios corporativos de oficinas, bancos y sedes';
    } else if (p.indexOf('/universidades-y-clubes') !== -1) {
      res.rubro = 'Universidades, colegios y clubes deportivos';
    } else if (p.indexOf('/consorcios') !== -1) {
      res.rubro = 'Consorcios de vivienda y grandes torres';
    } else if (p.indexOf('/clinicas-y-hospitales') !== -1) {
      res.rubro = 'Clínicas, sanatorios, hospitales y laboratorios';
    } else if (p.indexOf('/limpieza-en-altura') !== -1) {
      res.rubro = 'Servicios especiales (altura, final de obra, predios y MIP)';
      res.especialidad = '1. Lavado de naves, vidrios o cartelería en altura (norma ARAA)';
    } else if (p.indexOf('/servicios-especiales') !== -1) {
      res.rubro = 'Servicios especiales (altura, final de obra, predios y MIP)';
    } else if (p.indexOf('/grandes-superficies') !== -1) {
      res.rubro = 'Otro rubro o establecimiento (especificar)';
      res.otroDetalle = 'Grandes superficies / centro comercial / red de sucursales';
    }

    if (p.indexOf('/bahia-blanca') !== -1) {
      res.localidad = 'Bahía Blanca';
    } else if (p.indexOf('/neuquen-vaca-muerta') !== -1) {
      res.localidad = 'Neuquén / Vaca Muerta';
    } else if (p.indexOf('/trelew') !== -1) {
      res.localidad = 'Trelew, Chubut';
    } else if (p.indexOf('/puerto-madryn') !== -1) {
      res.localidad = 'Puerto Madryn, Chubut';
    }
    return res;
  }

  function buildContextualWaMessage(pathname, rawHref) {
    if (rawHref) {
      try {
        var qIndex = rawHref.indexOf('text=');
        if (qIndex !== -1) {
          var rawText = decodeURIComponent(rawHref.slice(qIndex + 5).split('&')[0].replace(/\+/g, ' '));
          var lowerRaw = rawText.toLowerCase();
          if (lowerRaw.indexOf('brochure interactivo') !== -1) {
            return rawText
              .replace(/\s+sin\s+cargo/gi, '')
              .replace(/\s+B2B/gi, '')
              .trim();
          }
          if (lowerRaw.indexOf('final de obra') !== -1) {
            return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza de final de obra para nuestra empresa o predio. Les comparto localidad y superficie aproximada: ';
          }
          if (lowerRaw.indexOf('espacios verdes') !== -1) {
            return 'Hola Star Union, nos interesa evaluar una propuesta de corte mecanizado y mantenimiento de grandes predios. Les comparto empresa, localidad y superficie aproximada: ';
          }
          if (lowerRaw.indexOf('control de plagas') !== -1) {
            return 'Hola Star Union, nos interesa evaluar una propuesta de fumigación certificada y manejo integrado de plagas (MIP) para nuestra empresa. Les comparto localidad y rubro: ';
          }
        }
      } catch (err) {}
    }

    var p = (pathname || '').toLowerCase();
    if (p.indexOf('/limpieza-industrial') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza industrial a medida para nuestra planta o centro logístico. Les comparto empresa, localidad y esquema que buscamos cubrir: ';
    }
    if (p.indexOf('/oficinas-corporativas') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestras oficinas o edificio corporativo. Les comparto empresa, localidad y esquema horario: ';
    }
    if (p.indexOf('/universidades-y-clubes') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestra institución educativa o club. Les comparto institución, localidad y esquema a cubrir: ';
    }
    if (p.indexOf('/consorcios') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional para nuestro consorcio o edificio. Les comparto dirección o barrio y carga horaria buscada: ';
    }
    if (p.indexOf('/clinicas-y-hospitales') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de higiene institucional para nuestra clínica, sanatorio o laboratorio. Les comparto institución, localidad y áreas a cubrir: ';
    }
    if (p.indexOf('/limpieza-en-altura') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza de vidrios o trabajos en altura con cuadrillas propias ARAA. Les comparto edificio o planta, localidad y alcance estimado: ';
    }
    if (p.indexOf('/servicios-especiales') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de servicios especiales (altura, final de obra, predios o MIP) para nuestra empresa. Les comparto localidad y superficie aproximada: ';
    }
    if (p.indexOf('/grandes-superficies') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional para grandes superficies o red de sucursales. Les comparto empresa, localidades y esquema buscado: ';
    }
    if (p.indexOf('/cobertura-y-operaciones-multi-sede') !== -1 || p.indexOf('/cobertura-regional-unificada') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza multi-sede para nuestra organización. Les comparto empresa y localidades donde operamos: ';
    }
    if (p.indexOf('/bahia-blanca') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestras instalaciones en Bahía Blanca. Les comparto empresa, rubro y carga horaria buscada: ';
    }
    if (p.indexOf('/neuquen-vaca-muerta') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestras instalaciones en Neuquén / Vaca Muerta. Les comparto empresa, rubro y esquema buscado: ';
    }
    if (p.indexOf('/trelew') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestras instalaciones en Trelew. Les comparto empresa, rubro y carga horaria buscada: ';
    }
    if (p.indexOf('/puerto-madryn') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestras instalaciones en Puerto Madryn. Les comparto empresa, rubro y carga horaria buscada: ';
    }
    if (p.indexOf('/la-empresa') !== -1) {
      return 'Hola Star Union, nos interesa coordinar un relevamiento técnico y evaluar una propuesta a medida para nuestra organización. Les comparto empresa, localidad y rubro: ';
    }
    if (p.indexOf('/certificacion-iso') !== -1) {
      return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional bajo Sistema de Gestión certificado ISO 9001:2015. Les comparto empresa, localidad y alcance buscado: ';
    }
    if (p.indexOf('/licitaciones-y-pliegos') !== -1) {
      return 'Hola Star Union, les escribo desde Compras para invitarlos a participar en una licitación o coordinar visita técnica. Les comparto empresa y localidad: ';
    }
    return 'Hola Star Union, nos interesa evaluar una propuesta de limpieza profesional a medida para nuestra organización. Les comparto empresa, localidad y esquema que buscamos cubrir: ';
  }

  function buildWaEndpoint(msg) {
    return 'https://api.whatsapp.com/send?phone=' + WA_PHONE + '&text=' + encodeURIComponent(msg);
  }

  function injectGlobalUxStyles() {
    if (document.getElementById('su-b2b-ux-styles')) return;
    var st = document.createElement('style');
    st.id = 'su-b2b-ux-styles';
    st.textContent = [
      'body.su-overlay-active { overflow: hidden !important; }',
      'body.su-overlay-active .su-wa-floating-btn, body.su-input-focused .su-wa-floating-btn { opacity: 0 !important; pointer-events: none !important; transform: translateY(10px) !important; }',
      '@media (max-width: 639px) {',
      '  .su-wa-floating-btn { padding: 12px !important; width: 48px !important; height: 48px !important; justify-content: center !important; bottom: 14px !important; right: 14px !important; box-shadow: 0 10px 24px rgba(3,88,45,0.28) !important; }',
      '  .su-wa-floating-btn span { display: none !important; }',
      '}',
      '#su-wizard-backdrop {',
      '  display: none; position: fixed; inset: 0; z-index: 9990;',
      '  background: rgba(15, 23, 42, 0.46);',
      '  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);',
      '  align-items: center; justify-content: center; padding: 12px;',
      '}',
      '#su-wizard-backdrop.is-open { display: flex; animation: suFadeBackdrop 0.18s ease-out; }',
      '@keyframes suFadeBackdrop { from { opacity: 0; } to { opacity: 1; } }',
      '#su-wizard-card {',
      '  background: rgba(255, 255, 255, 0.98); width: 100%; max-width: 540px; max-height: 90vh;',
      '  border-radius: 20px; box-shadow: 0 28px 60px -12px rgba(0,0,0,0.32);',
      '  border: 1px solid rgba(229,231,235,0.95); border-top: 4px solid #03582d;',
      '  display: flex; flex-direction: column; overflow: hidden; font-family: "Open Sans", sans-serif;',
      '}',
      '.su-wiz-body { padding: 20px 22px 22px; overflow-y: auto; -webkit-overflow-scrolling: touch; }',
      '@media (max-width: 639px) {',
      '  #su-wizard-backdrop { padding: 8px; align-items: center; }',
      '  #su-wizard-card { max-height: 92vh; border-radius: 18px; }',
      '  .su-wiz-body { padding: 15px 15px 16px; }',
      '  .su-choice-btn { padding: 10px 12px; min-height: 44px; font-size: 13px; }',
      '  .su-pill-opt { padding: 7px 8px; min-height: 38px; font-size: 12px; }',
      '}',
      '.su-choice-btn {',
      '  width: 100%; text-align: left; background: #f9fafb; border: 1.5px solid #e5e7eb;',
      '  border-radius: 12px; padding: 12px 14px; font-size: 13.5px; font-weight: 700; color: #111827;',
      '  display: flex; align-items: center; justify-content: space-between; gap: 10px;',
      '  cursor: pointer; transition: all 0.14s ease; font-family: "Open Sans", sans-serif; min-height: 48px;',
      '}',
      '.su-choice-btn:hover { border-color: #03582d; background: #f4f7f5; color: #03582d; }',
      '.su-choice-btn.is-selected { border-color: #03582d; background: #eef6f1; color: #03582d; box-shadow: 0 0 0 1px #03582d; }',
      '.su-pill-opt {',
      '  text-align: center; background: #ffffff; border: 1.5px solid #d1d5db; border-radius: 10px;',
      '  padding: 9px 10px; font-size: 12.5px; font-weight: 700; color: #1f2937; cursor: pointer;',
      '  transition: all 0.14s ease; font-family: "Open Sans", sans-serif; min-height: 42px; display:flex; align-items:center; justify-content:center;',
      '}',
      '.su-pill-opt:hover { border-color: #03582d; color: #03582d; }',
      '.su-pill-opt.is-selected { background: #03582d; border-color: #03582d; color: #ffffff; }',
      '.su-wiz-input {',
      '  width: 100%; background: #ffffff; border: 1.5px solid #d1d5db; border-radius: 10px;',
      '  padding: 10px 13px; font-size: 16px; color: #111827; outline: none; font-family: "Open Sans", sans-serif;',
      '}',
      '@media (min-width: 640px) { .su-wiz-input { font-size: 14px; } }',
      '.su-wiz-input:focus { border-color: #03582d; box-shadow: 0 0 0 3px rgba(3,88,45,0.1); }'
    ].join('\n');
    document.head.appendChild(st);
  }

  var CLOUD_COTIZADOR_API = 'https://cotizador-api-production-1166303f.up.railway.app/api/cotizar';

  function resolveCotizarLandingUrl(opts) {
    opts = opts || {};
    var defaults = detectPageDefaults();
    var rubro = opts.rubro || defaults.rubro || '';
    var loc = opts.localidad || defaults.localidad || '';
    var qp = [];
    if (rubro) qp.push('rubro=' + encodeURIComponent(rubro));
    if (loc) qp.push('localidad=' + encodeURIComponent(loc));
    qp.push('origen=' + encodeURIComponent(window.location.pathname || '/'));
    return resolveBaseRoot() + 'cotizar/index.html' + (qp.length ? '?' + qp.join('&') : '');
  }

  function submitPayloadToApi(payload, onSuccess, onError) {
    window.dataLayer = window.dataLayer || [];
    var isStagingHost = window.location.hostname.indexOf('wajntraub.ar') !== -1 ||
                        window.location.hostname === 'localhost' ||
                        window.location.hostname === '127.0.0.1';

    var cloudBody = {
      tipo_solicitud: 'cotizacion',
      entorno: isStagingHost ? 'staging' : 'produccion',
      empresa: payload.empresa || '',
      nombre: payload.nombre || '',
      email: payload.email || '',
      telefono: payload.telefono || '',
      rubro: payload.otro_rubro_detalle ? ('Otro: ' + payload.otro_rubro_detalle) : (payload.tipo_organizacion || ''),
      alcance: payload.especialidad_requerida || payload.cantidad_personas || '',
      horas_dia: payload.escala_especial || payload.cantidad_horas || '',
      dias_semana: payload.dias_servicio || '',
      localidad: payload.ubicacion || '',
      sedes_adicionales: payload.sedes_adicionales || '',
      comentarios: payload.escala || '',
      origen_pagina: payload.pagina_origen || window.location.pathname,
      canal_origen: 'Sitio web Star Union',
      website_url: payload.website_hp || ''
    };

    if (!isStagingHost) {
      fetch(resolveApiUrl(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(function () {});
    }

    fetch(CLOUD_COTIZADOR_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cloudBody)
    })
      .then(function (res) { return res.json(); })
      .then(function (j) {
        if (j && j.ok) {
          onSuccess(j);
        } else {
          throw new Error((j && j.error) || 'Error de validación');
        }
      })
      .catch(function () {
        onError();
      });
  }

  function fireQualifiedLeadEvents(payload, isMultiSede) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'lead_b2b_calificado_starunion',
      b2b_vertical: payload.tipo_organizacion,
      b2b_specialty: payload.especialidad_requerida || 'abono_regular',
      b2b_headcount: payload.cantidad_personas || 'especial',
      b2b_hours: payload.cantidad_horas || payload.escala_especial,
      b2b_location: payload.ubicacion,
      b2b_multisede: isMultiSede ? 'si' : 'no'
    });
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'lead_b2b_calificado_starunion', {
        event_category: 'B2B_Form',
        b2b_vertical: payload.tipo_organizacion
      });
    }
  }

  // =========================================================================
  // COTIZADOR CONVERSACIONAL PASO A PASO (ESTILO FORMSPREE / TYPEFORM / NEIL PATEL)
  // =========================================================================
  function initStepWizard() {
    if (document.getElementById('su-wizard-backdrop')) return;

    var state = {
      step: 1,
      rubro: '',
      otroDetalle: '',
      personas: 'A definir en relevamiento técnico',
      horas: 'Jornada completa (8 hs diarias)',
      dias: 'Lunes a viernes',
      especialidad: '1. Lavado de naves, vidrios o cartelería en altura (norma ARAA)',
      escalaEspecial: '',
      ubicacion: '',
      sedesExtras: [],
      empresa: '',
      nombre: '',
      email: '',
      telefono: '',
      observaciones: '',
      subview: '' // 'particular' | 'compras' | 'done'
    };

    var backdrop = document.createElement('div');
    backdrop.id = 'su-wizard-backdrop';
    backdrop.innerHTML = [
      '<div id="su-wizard-card" role="dialog" aria-modal="true" aria-labelledby="su-wiz-title">',
      '  <div style="padding:14px 20px 12px;border-bottom:1px solid #f3f4f6;background:#ffffff;">',
      '    <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px;">',
      '      <div style="display:flex;align-items:center;gap:8px;">',
      '        <button type="button" id="su-wiz-back" style="display:none;white-space:nowrap;flex-shrink:0;background:#f3f4f6;border:none;border-radius:8px;padding:5px 10px;font-size:12px;font-weight:700;color:#111827;cursor:pointer;font-family:\'Open Sans\',sans-serif;">← Anterior</button>',
      '        <span id="su-wiz-step-label" style="font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:0.06em;color:#03582d;">Paso 1 de 3 · Cotización corporativa</span>',
      '      </div>',
      '      <button type="button" id="su-wiz-close" aria-label="Cerrar cotizador" style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;width:34px;height:34px;font-size:16px;font-weight:700;color:#4b5563;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;">✕</button>',
      '    </div>',
      '    <div style="height:4px;width:100%;background:#e5e7eb;border-radius:999px;overflow:hidden;">',
      '      <div id="su-wiz-bar" style="height:100%;width:33%;background:#03582d;border-radius:999px;transition:width 0.25s ease;"></div>',
      '    </div>',
      '  </div>',
      '  <div class="su-wiz-body" id="su-wiz-body"></div>',
      '</div>'
    ].join('');
    document.body.appendChild(backdrop);

    var bodyEl = document.getElementById('su-wiz-body');
    var backBtn = document.getElementById('su-wiz-back');
    var closeBtn = document.getElementById('su-wiz-close');
    var stepLabel = document.getElementById('su-wiz-step-label');
    var barEl = document.getElementById('su-wiz-bar');

    function closeWizard() {
      backdrop.classList.remove('is-open');
      document.body.classList.remove('su-overlay-active');
    }

    function openWizard(opts) {
      opts = opts || {};
      var defaults = detectPageDefaults();
      state.subview = '';
      if (opts.localidad || defaults.localidad) {
        state.ubicacion = opts.localidad || state.ubicacion || defaults.localidad;
      }
      var chosenRubro = opts.rubro || defaults.rubro || '';
      if (defaults.especialidad && !opts.rubro) {
        state.especialidad = defaults.especialidad;
      }
      if (defaults.otroDetalle && !opts.rubro) {
        state.otroDetalle = defaults.otroDetalle;
      }
      if (chosenRubro) {
        state.rubro = chosenRubro;
        state.step = 2;
      } else {
        state.step = 1;
      }
      var mobileDrawer = document.getElementById('mobile-nav-drawer');
      if (mobileDrawer && !mobileDrawer.classList.contains('hidden')) {
        mobileDrawer.classList.add('hidden');
      }
      document.body.classList.add('su-overlay-active');
      backdrop.classList.add('is-open');
      renderWizard();
    }

    window.openStarUnionCotizador = openWizard;

    closeBtn.addEventListener('click', closeWizard);
    backdrop.addEventListener('click', function (e) {
      if (e.target === backdrop) closeWizard();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && backdrop.classList.contains('is-open')) closeWizard();
    });

    backBtn.addEventListener('click', function () {
      if (state.subview) {
        state.subview = '';
        renderWizard();
        return;
      }
      if (state.step > 1) {
        state.step -= 1;
        renderWizard();
      }
    });

    var RUBROS = [
      { val: 'Plantas industriales, fábricas y centros logísticos', label: '1. Plantas industriales, fábricas y logística' },
      { val: 'Edificios corporativos de oficinas, bancos y sedes', label: '2. Edificios de oficinas, bancos y sedes' },
      { val: 'Universidades, colegios y clubes deportivos', label: '3. Universidades, colegios y clubes' },
      { val: 'Consorcios de vivienda y grandes torres', label: '4. Consorcios de vivienda y grandes torres' },
      { val: 'Clínicas, sanatorios, hospitales y laboratorios', label: '5. Clínicas, sanatorios y laboratorios' },
      { val: 'Servicios especiales (altura, final de obra, predios y MIP)', label: '6. Servicios especiales (altura, final de obra, predios)' },
      { val: 'Otro rubro o establecimiento (especificar)', label: 'Otro establecimiento corporativo o comercial' }
    ];

    function escHtml(str) {
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    function renderWizard() {
      if (state.subview === 'compras') {
        backBtn.style.display = 'inline-flex';
        stepLabel.textContent = 'Proveedores e insumos';
        barEl.style.width = '100%';
        bodyEl.innerHTML = [
          '<h3 id="su-wiz-title" style="font-size:19px;font-weight:800;color:#000;margin:0 0 8px;line-height:1.25;">Recepción de propuestas de proveedores</h3>',
          '<p style="font-size:13.5px;color:#4b5563;margin:0 0 16px;line-height:1.5;">El cotizador web es exclusivo para empresas que contratan servicios de limpieza. Copiá la casilla de Compras para enviarnos tu catálogo o presentación:</p>',
          '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;background:#f9fafb;border:1.5px solid #d1d5db;border-radius:12px;padding:12px 14px;">',
          '  <span style="font-weight:800;color:#000;font-size:14px;user-select:all;">' + EMAIL_COMPRAS + '</span>',
          '  <button type="button" id="su-wiz-copy-compras" style="background:#03582d;color:#fff;border:none;border-radius:8px;padding:8px 14px;font-size:12.5px;font-weight:700;cursor:pointer;white-space:nowrap;">Copiar correo</button>',
          '</div>'
        ].join('');
        document.getElementById('su-wiz-copy-compras').addEventListener('click', function () {
          copyPlainText(EMAIL_COMPRAS, this, '✓ Copiado');
        });
        return;
      }

      if (state.subview === 'particular') {
        backBtn.style.display = 'inline-flex';
        stepLabel.textContent = 'Alcance corporativo';
        barEl.style.width = '100%';
        bodyEl.innerHTML = [
          '<div style="background:#f9fafb;border:1.5px solid #d1d5db;border-radius:14px;padding:18px;">',
          '  <h3 id="su-wiz-title" style="font-size:18px;font-weight:800;color:#111827;margin:0 0 8px;">Atención exclusiva para empresas, consorcios e instituciones</h3>',
          '  <p style="font-size:13.5px;color:#4b5563;margin:0;line-height:1.55;">Star Union S.R.L. presta servicios exclusivos para plantas industriales, edificios corporativos, instituciones educativas, clínicas, grandes superficies y consorcios (esquemas desde 4 hs diarias corridas).</p>',
          '</div>'
        ].join('');
        return;
      }

      if (state.subview === 'done') {
        backBtn.style.display = 'none';
        stepLabel.textContent = 'Solicitud enviada';
        barEl.style.width = '100%';
        var cNom = state.nombre.replace(/[,\s]+$/, '').trim();
        var cEmp = state.empresa.replace(/[,\s]+$/, '').trim();
        var doneHeading = (cEmp && cEmp.toLowerCase() !== cNom.toLowerCase())
          ? ('Gracias, ' + escHtml(cNom) + '. Registramos la solicitud de ' + escHtml(cEmp) + '.')
          : ('Gracias, ' + escHtml(cNom) + '. Registramos tu solicitud comercial.');
        bodyEl.innerHTML = [
          '<div style="padding:4px 0;">',
          '  <div style="display:inline-block;background:#eef6f1;color:#03582d;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;padding:4px 10px;border-radius:999px;margin-bottom:10px;">✓ Solicitud recibida</div>',
          '  <h3 id="su-wiz-title" style="font-size:19px;font-weight:800;color:#000;margin:0 0 8px;line-height:1.3;">' + doneHeading + '</h3>',
          '  <p style="font-size:13.5px;color:#374151;margin:0 0 14px;line-height:1.55;">Dirección Comercial evaluará el esquema solicitado y responderá en forma directa a <strong>' + escHtml(state.email) + '</strong> o al <strong>' + escHtml(state.telefono) + '</strong>.</p>',
          '  <div style="padding-top:12px;border-top:1px solid #e5e7eb;display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;font-size:12px;color:#4b5563;">',
          '    <span>Línea directa: <strong style="color:#03582d;">0810-333-UNION (8646)</strong></span>',
          '    <span>Base Central CABA (800 m²) · ISO 9001:2015</span>',
          '  </div>',
          '  <button type="button" id="su-wiz-done-close" style="margin-top:16px;width:100%;background:#03582d;color:#fff;border:none;border-radius:10px;padding:12px;font-size:13.5px;font-weight:800;cursor:pointer;">Volver al sitio</button>',
          '</div>'
        ].join('');
        document.getElementById('su-wiz-done-close').addEventListener('click', closeWizard);
        return;
      }

      // PASO 1
      if (state.step === 1) {
        backBtn.style.display = 'none';
        stepLabel.textContent = 'Paso 1 de 3 · Tipo de establecimiento';
        barEl.style.width = '33%';

        var btnsHtml = RUBROS.map(function (r) {
          var sel = state.rubro === r.val ? ' is-selected' : '';
          return '<button type="button" class="su-choice-btn js-wiz-rubro' + sel + '" data-val="' + escHtml(r.val) + '">' +
            '<span>' + escHtml(r.label) + '</span>' +
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>' +
          '</button>';
        }).join('');

        bodyEl.innerHTML = [
          '<h3 id="su-wiz-title" style="font-size:19px;font-weight:800;color:#000;margin:0 0 4px;line-height:1.25;">¿Para qué tipo de establecimiento buscás cotizar?</h3>',
          '<p style="font-size:13px;color:#676b67;margin:0 0 14px;line-height:1.45;">Tocá una opción para configurar tu esquema en menos de un minuto:</p>',
          '<div style="display:flex;flex-direction:column;gap:8px;">' + btnsHtml + '</div>',
          '<div style="margin-top:12px;padding-top:10px;border-top:1px solid #f3f4f6;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 10px;font-size:11.5px;color:#6b7280;">',
          '  <a href="' + RRHH_GOOGLE_FORM_URL + '" target="_blank" rel="noopener noreferrer" id="su-wiz-rrhh-link" style="color:#03582d;font-weight:700;text-decoration:underline;">Busco empleo (RRHH) ↗</a>',
          '  <button type="button" id="su-wiz-compras-link" style="background:none;border:none;padding:0;color:#374151;font-weight:700;text-decoration:underline;cursor:pointer;font-family:\'Open Sans\',sans-serif;font-size:11.5px;">Soy proveedor</button>',
          '  <button type="button" id="su-wiz-particular-link" style="background:none;border:none;padding:0;color:#6b7280;text-decoration:underline;cursor:pointer;font-family:\'Open Sans\',sans-serif;font-size:11.5px;">Casa particular</button>',
          '</div>'
        ].join('');

        bodyEl.querySelectorAll('.js-wiz-rubro').forEach(function (b) {
          b.addEventListener('click', function () {
            state.rubro = b.getAttribute('data-val');
            state.step = 2;
            renderWizard();
          });
        });
        document.getElementById('su-wiz-rrhh-link').addEventListener('click', function () {
          if (typeof window.gtag === 'function') {
            window.gtag('event', 'salida_rrhh_form', { ubicacion: 'cotizador_paso1' });
          }
          closeWizard();
        });
        document.getElementById('su-wiz-compras-link').addEventListener('click', function () {
          state.subview = 'compras';
          renderWizard();
        });
        document.getElementById('su-wiz-particular-link').addEventListener('click', function () {
          state.subview = 'particular';
          renderWizard();
        });
        return;
      }

      // PASO 2
      if (state.step === 2) {
        backBtn.style.display = 'inline-flex';
        stepLabel.textContent = 'Paso 2 de 3 · Esquema y ubicación';
        barEl.style.width = '66%';

        var isEspecial = state.rubro.indexOf('Servicios especiales') !== -1;
        var isOtro = state.rubro.indexOf('Otro rubro') === 0;

        var otroHtml = isOtro ? (
          '<div style="margin-bottom:12px;">' +
            '<label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:5px;">Especificá tu rubro o tipo de establecimiento *</label>' +
            '<input type="text" id="su-wiz-otro" class="su-wiz-input" value="' + escHtml(state.otroDetalle) + '" placeholder="Ej.: centro comercial, puerto, concesionario, red de sucursales...">' +
          '</div>'
        ) : '';

        function buildWizardWaMessage() {
          var parts = ['Hola Star Union, nos interesa evaluar una propuesta para nuestra organización.'];
          if (state.empresa && state.empresa.trim()) parts.push('Empresa: ' + state.empresa.trim() + '.');
          if (state.rubro) {
            var rLabel = isOtro && state.otroDetalle.trim() ? state.otroDetalle.trim() : state.rubro;
            parts.push('Sector: ' + rLabel + '.');
          }
          if (isEspecial) {
            if (state.especialidad) parts.push('Intervención: ' + state.especialidad + '.');
            if (state.escalaEspecial && state.escalaEspecial.trim()) parts.push('Alcance: ' + state.escalaEspecial.trim() + '.');
          } else {
            var sch = [];
            if (state.personas) sch.push(state.personas);
            if (state.horas) sch.push(state.horas);
            if (state.dias) sch.push(state.dias);
            if (sch.length) parts.push('Esquema: ' + sch.join(' · ') + '.');
          }
          if (state.ubicacion && state.ubicacion.trim()) {
            parts.push('Localidad: ' + state.ubicacion.trim() + '.');
          }
          return parts.join(' ');
        }

        var middleHtml = '';
        if (isEspecial) {
          var espOpts = [
            '1. Lavado de naves, vidrios o cartelería en altura (norma ARAA)',
            '2. Final de obra industrial, corporativo o comercial de escala',
            '3. Corte mecanizado con tractores en grandes predios',
            '4. Fumigación certificada y manejo integrado de plagas (MIP)'
          ];
          middleHtml = [
            '<div style="margin-bottom:12px;">',
            '  <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Intervención en planta, edificio o predio *</label>',
            '  <div style="display:flex;flex-direction:column;gap:6px;">',
            espOpts.map(function (op) {
              var sel = state.especialidad === op ? ' is-selected' : '';
              return '<button type="button" class="su-choice-btn js-wiz-esp' + sel + '" data-val="' + escHtml(op) + '" style="padding:10px 12px;min-height:42px;font-size:12.5px;"><span>' + escHtml(op) + '</span></button>';
            }).join(''),
            '  </div>',
            '</div>',
            '<div style="margin-bottom:12px;">',
            '  <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:5px;">Superficie aproximada (m² / hectáreas) *</label>',
            '  <input type="text" id="su-wiz-escala-esp" class="su-wiz-input" value="' + escHtml(state.escalaEspecial) + '" placeholder="Ej.: 1.800 m² de nave, 4 ha de predio o fachada vidriada">',
            '</div>'
          ].join('');
        } else {
          var pOpts = [
            { v: 'A definir en relevamiento técnico', l: 'A definir en relevamiento' },
            { v: '1 a 2 personas (jornada mínima 4 hs corridas)', l: '1 a 2 personas' },
            { v: '3 a 5 personas en servicio', l: '3 a 5 personas' },
            { v: '6 a 12 personas en servicio', l: '6 a 12 personas' },
            { v: 'Más de 12 personas / turnos rotativos', l: '+12 personas' }
          ];
          var hOpts = [
            { v: 'Media jornada (4 hs diarias corridas)', l: '4 hs corridas (mín.)' },
            { v: 'Jornada de 6 hs diarias corridas', l: '6 hs diarias' },
            { v: 'Jornada completa (8 hs diarias)', l: '8 hs diarias' },
            { v: 'Cobertura multi-turno o 24/7', l: 'Turnos / 24 hs' }
          ];
          var dOpts = ['Lunes a viernes', 'Lunes a sábado', 'Lunes a lunes (cobertura continua)'];

          middleHtml = [
            '<div style="margin-bottom:12px;">',
            '  <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Dotación estimada de personas *</label>',
            '  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;">',
            pOpts.map(function (o, idx) {
              var span2 = idx === 0 ? 'grid-column:span 2;' : '';
              var sel = state.personas === o.v ? ' is-selected' : '';
              return '<button type="button" class="su-pill-opt js-wiz-personas' + sel + '" data-val="' + escHtml(o.v) + '" style="' + span2 + '">' + escHtml(o.l) + '</button>';
            }).join(''),
            '  </div>',
            '</div>',
            '<div style="margin-bottom:12px;">',
            '  <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Carga horaria diaria (mínimo 4 hs corridas) *</label>',
            '  <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;">',
            hOpts.map(function (o) {
              var sel = state.horas === o.v ? ' is-selected' : '';
              return '<button type="button" class="su-pill-opt js-wiz-horas' + sel + '" data-val="' + escHtml(o.v) + '">' + escHtml(o.l) + '</button>';
            }).join(''),
            '  </div>',
            '</div>',
            '<div style="margin-bottom:12px;">',
            '  <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:6px;">Frecuencia semanal *</label>',
            '  <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;">',
            dOpts.map(function (d) {
              var shortD = d.indexOf('Lunes a lunes') === 0 ? 'Lun a lun' : (d === 'Lunes a sábado' ? 'Lun a sáb' : 'Lun a vie');
              var sel = state.dias === d ? ' is-selected' : '';
              return '<button type="button" class="su-pill-opt js-wiz-dias' + sel + '" data-val="' + escHtml(d) + '">' + escHtml(shortD) + '</button>';
            }).join(''),
            '  </div>',
            '</div>'
          ].join('');
        }

        var extraSedesHtml = state.sedesExtras.map(function (s, idx) {
          return '<div style="display:flex;gap:6px;margin-top:6px;">' +
            '<input type="text" class="su-wiz-input js-wiz-sede-loc" data-idx="' + idx + '" value="' + escHtml(s.loc) + '" placeholder="Otra sede (localidad / dirección)" style="flex:1;padding:8px 10px;font-size:13px;">' +
            '<input type="text" class="su-wiz-input js-wiz-sede-dot" data-idx="' + idx + '" value="' + escHtml(s.dot) + '" placeholder="Dotación u horario" style="flex:1;padding:8px 10px;font-size:13px;">' +
            '<button type="button" class="js-wiz-del-sede" data-idx="' + idx + '" style="background:#f3f4f6;border:none;border-radius:8px;padding:0 10px;cursor:pointer;font-weight:700;color:#4b5563;">✕</button>' +
          '</div>';
        }).join('');

        bodyEl.innerHTML = [
          '<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;background:#f4f7f5;border:1px solid #d1e7da;border-radius:10px;padding:7px 11px;margin-bottom:12px;font-size:12px;">',
          '  <span style="color:#133522;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">Sector: ' + escHtml(state.rubro) + '</span>',
          '  <button type="button" id="su-wiz-change-rubro" style="background:none;border:none;color:#03582d;font-weight:800;text-decoration:underline;cursor:pointer;white-space:nowrap;font-size:11.5px;">Cambiar</button>',
          '</div>',
          otroHtml,
          middleHtml,
          '<div id="su-wiz-step2-warn" style="display:none;background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:10px 12px;font-size:12.5px;font-weight:600;color:#991b1b;margin-bottom:12px;line-height:1.45;"></div>',
          '<div style="margin-bottom:14px;">',
          '  <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:5px;">',
          '    <label style="font-size:12.5px;font-weight:700;color:#111827;">Localidad del servicio *</label>',
          '    <button type="button" id="su-wiz-add-sede" style="background:none;border:none;padding:0;color:#03582d;font-size:12px;font-weight:800;cursor:pointer;text-decoration:underline;white-space:nowrap;">+ Sumar otra sede</button>',
          '  </div>',
          '  <input type="text" id="su-wiz-ubicacion" class="su-wiz-input" value="' + escHtml(state.ubicacion) + '" placeholder="Ej.: CABA, GBA, Bahía Blanca, Neuquén, Trelew, Puerto Madryn...">',
          '  <div id="su-wiz-sedes-wrap">' + extraSedesHtml + '</div>',
          '</div>',
          '<button type="button" id="su-wiz-to-step3" style="width:100%;background:#03582d;color:#ffffff;border:none;border-radius:12px;padding:13px 16px;font-size:14px;font-weight:800;cursor:pointer;min-height:48px;font-family:\'Open Sans\',sans-serif;">Continuar al último paso →</button>',
          '<div style="margin-top:10px;text-align:center;">',
          '  <a href="#" id="su-wiz-wa-step2" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:700;color:#03582d;text-decoration:underline;">O enviar estos datos por WhatsApp Comercial ↗</a>',
          '</div>'
        ].join('');

        function syncStep2Inputs() {
          var u = document.getElementById('su-wiz-ubicacion');
          if (u) state.ubicacion = u.value;
          var ot = document.getElementById('su-wiz-otro');
          if (ot) state.otroDetalle = ot.value;
          var ee = document.getElementById('su-wiz-escala-esp');
          if (ee) state.escalaEspecial = ee.value;
          bodyEl.querySelectorAll('.js-wiz-sede-loc').forEach(function (inp) {
            var idx = parseInt(inp.getAttribute('data-idx'), 10);
            if (state.sedesExtras[idx]) state.sedesExtras[idx].loc = inp.value;
          });
          bodyEl.querySelectorAll('.js-wiz-sede-dot').forEach(function (inp) {
            var idx = parseInt(inp.getAttribute('data-idx'), 10);
            if (state.sedesExtras[idx]) state.sedesExtras[idx].dot = inp.value;
          });
        }

        var waStep2El = document.getElementById('su-wiz-wa-step2');
        if (waStep2El) {
          waStep2El.addEventListener('click', function () {
            syncStep2Inputs();
            waStep2El.setAttribute('href', buildWaEndpoint(buildWizardWaMessage()));
            if (typeof window.gtag === 'function') {
              window.gtag('event', 'cotizador_derivacion_wa_b2b', { step: 2, rubro: state.rubro });
            }
            setTimeout(closeWizard, 120);
          });
        }

        document.getElementById('su-wiz-change-rubro').addEventListener('click', function () {
          syncStep2Inputs();
          state.step = 1;
          renderWizard();
        });

        bodyEl.querySelectorAll('.js-wiz-personas').forEach(function (b) {
          b.addEventListener('click', function () {
            syncStep2Inputs();
            state.personas = b.getAttribute('data-val');
            renderWizard();
          });
        });
        bodyEl.querySelectorAll('.js-wiz-horas').forEach(function (b) {
          b.addEventListener('click', function () {
            syncStep2Inputs();
            state.horas = b.getAttribute('data-val');
            renderWizard();
          });
        });
        bodyEl.querySelectorAll('.js-wiz-dias').forEach(function (b) {
          b.addEventListener('click', function () {
            syncStep2Inputs();
            state.dias = b.getAttribute('data-val');
            renderWizard();
          });
        });
        bodyEl.querySelectorAll('.js-wiz-esp').forEach(function (b) {
          b.addEventListener('click', function () {
            syncStep2Inputs();
            state.especialidad = b.getAttribute('data-val');
            renderWizard();
          });
        });

        document.getElementById('su-wiz-add-sede').addEventListener('click', function () {
          syncStep2Inputs();
          if (state.sedesExtras.length < 6) {
            state.sedesExtras.push({ loc: '', dot: '' });
            renderWizard();
          }
        });
        bodyEl.querySelectorAll('.js-wiz-del-sede').forEach(function (b) {
          b.addEventListener('click', function () {
            syncStep2Inputs();
            var idx = parseInt(b.getAttribute('data-idx'), 10);
            state.sedesExtras.splice(idx, 1);
            renderWizard();
          });
        });

        document.getElementById('su-wiz-to-step3').addEventListener('click', function () {
          syncStep2Inputs();
          var warn = document.getElementById('su-wiz-step2-warn');
          if (isOtro && !state.otroDetalle.trim()) {
            warn.textContent = 'Especificá en pocas palabras tu rubro o tipo de establecimiento.';
            warn.style.display = 'block';
            document.getElementById('su-wiz-otro').focus();
            return;
          }
          if (isEspecial && !state.escalaEspecial.trim()) {
            warn.textContent = 'Indicá una superficie aproximada o alcance del trabajo.';
            warn.style.display = 'block';
            document.getElementById('su-wiz-escala-esp').focus();
            return;
          }
          if (!state.ubicacion.trim()) {
            warn.textContent = 'Indicá la localidad o dirección donde se prestará el servicio.';
            warn.style.display = 'block';
            document.getElementById('su-wiz-ubicacion').focus();
            return;
          }
          state.step = 3;
          renderWizard();
        });
        return;
      }

      // PASO 3
      if (state.step === 3) {
        backBtn.style.display = 'inline-flex';
        stepLabel.textContent = 'Paso 3 de 3 · Datos de contacto';
        barEl.style.width = '100%';
        var rfpUrl = resolveBaseRoot() + 'licitaciones-y-pliegos/index.html';

        bodyEl.innerHTML = [
          '<h3 id="su-wiz-title" style="font-size:18.5px;font-weight:800;color:#000;margin:0 0 4px;line-height:1.25;">¿A quién enviamos la propuesta técnica y económica?</h3>',
          '<p style="font-size:12.5px;color:#676b67;margin:0 0 14px;">Dirección Comercial responderá directo a tu correo o teléfono corporativo.</p>',
          '<form id="su-wiz-final-form" style="display:flex;flex-direction:column;gap:10px;">',
          '  <input type="text" name="website_hp" value="" tabindex="-1" autocomplete="off" style="display:none;" aria-hidden="true">',
          '  <div>',
          '    <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:4px;">Empresa, institución o consorcio *</label>',
          '    <input type="text" id="su-wiz-empresa" required class="su-wiz-input" value="' + escHtml(state.empresa) + '" placeholder="Nombre de tu organización">',
          '  </div>',
          '  <div>',
          '    <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:4px;">Nombre, apellido y área *</label>',
          '    <input type="text" id="su-wiz-nombre" required class="su-wiz-input" value="' + escHtml(state.nombre) + '" placeholder="Ej.: Martín Gómez · Compras / Administración">',
          '  </div>',
          '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">',
          '    <div>',
          '      <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:4px;">Correo corporativo *</label>',
          '      <input type="email" id="su-wiz-email" required class="su-wiz-input" value="' + escHtml(state.email) + '" placeholder="nombre@tuempresa.com.ar">',
          '    </div>',
          '    <div>',
          '      <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:4px;">Teléfono o WhatsApp *</label>',
          '      <input type="tel" id="su-wiz-tel" required class="su-wiz-input" value="' + escHtml(state.telefono) + '" placeholder="Ej.: 011 4000-0000">',
          '    </div>',
          '  </div>',
          '  <div>',
          '    <label style="display:block;font-size:12.5px;font-weight:700;color:#111827;margin-bottom:4px;">Comentarios o horarios (opcional)</label>',
          '    <textarea id="su-wiz-obs" rows="2" class="su-wiz-input" style="resize:none;" placeholder="Ej.: visita de relevamiento o requisito puntual">' + escHtml(state.observaciones) + '</textarea>',
          '    <div style="font-size:11.5px;color:#676b67;margin-top:5px;">¿Invitación a licitar o pliego en PDF? <a href="' + escHtml(rfpUrl) + '" target="_blank" rel="noopener noreferrer" style="color:#03582d;font-weight:700;text-decoration:underline;">Subir pliego / RFP acá ↗</a></div>',
          '  </div>',
          '  <div id="su-wiz-step3-err" style="display:none;background:#f3f4f6;border:1px solid #d1d5db;color:#111827;border-radius:10px;padding:10px 12px;font-size:12.5px;font-weight:600;"></div>',
          '  <button type="submit" id="su-wiz-submit" style="margin-top:4px;width:100%;background:#03582d;color:#ffffff;border:none;border-radius:12px;padding:14px 16px;font-size:14.5px;font-weight:800;cursor:pointer;min-height:50px;font-family:\'Open Sans\',sans-serif;">Enviar solicitud a Comercial</button>',
          '  <div style="margin-top:4px;text-align:center;">',
          '    <a href="#" id="su-wiz-wa-step3" target="_blank" rel="noopener noreferrer" style="display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:700;color:#03582d;text-decoration:underline;">O enviar estos datos por WhatsApp Comercial ↗</a>',
          '  </div>',
          '</form>'
        ].join('');

        var waStep3El = document.getElementById('su-wiz-wa-step3');
        if (waStep3El) {
          waStep3El.addEventListener('click', function () {
            var empVal = (document.getElementById('su-wiz-empresa')?.value || '').trim();
            var isEsp3 = state.rubro.indexOf('Servicios especiales') !== -1;
            var msgParts = ['Hola Star Union, nos interesa evaluar una propuesta para nuestra organización.'];
            if (empVal) msgParts.push('Empresa: ' + empVal + '.');
            if (state.rubro) msgParts.push('Sector: ' + state.rubro + '.');
            if (!isEsp3 && state.horas) msgParts.push('Esquema: ' + state.personas + ' · ' + state.horas + ' · ' + state.dias + '.');
            if (isEsp3 && state.especialidad) msgParts.push('Intervención: ' + state.especialidad + '.');
            if (state.ubicacion) msgParts.push('Localidad: ' + state.ubicacion + '.');
            waStep3El.setAttribute('href', buildWaEndpoint(msgParts.join(' ')));
            if (typeof window.gtag === 'function') {
              window.gtag('event', 'cotizador_derivacion_wa_b2b', { step: 3, rubro: state.rubro });
            }
            setTimeout(closeWizard, 120);
          });
        }

        var finalForm = document.getElementById('su-wiz-final-form');
        finalForm.addEventListener('submit', function (e) {
          e.preventDefault();
          state.empresa = document.getElementById('su-wiz-empresa').value.trim();
          state.nombre = document.getElementById('su-wiz-nombre').value.trim();
          state.email = document.getElementById('su-wiz-email').value.trim();
          state.telefono = document.getElementById('su-wiz-tel').value.trim();
          state.observaciones = document.getElementById('su-wiz-obs').value.trim();
          var hp = (finalForm.querySelector('[name="website_hp"]')?.value || '').trim();

          var isEsp = state.rubro.indexOf('Servicios especiales') !== -1;
          var sedesClean = state.sedesExtras
            .filter(function (s) { return (s.loc && s.loc.trim()) || (s.dot && s.dot.trim()); })
            .map(function (s) { return s.loc.trim() + (s.dot.trim() ? ' (' + s.dot.trim() + ')' : ''); });

          var payload = {
            empresa: state.empresa,
            nombre: state.nombre,
            email: state.email,
            telefono: state.telefono,
            tipo_organizacion: state.rubro,
            otro_rubro_detalle: state.otroDetalle,
            especialidad_requerida: isEsp ? state.especialidad : '',
            escala_especial: isEsp ? state.escalaEspecial : '',
            cantidad_personas: isEsp ? '' : state.personas,
            cantidad_horas: isEsp ? '' : state.horas,
            dias_servicio: isEsp ? '' : state.dias,
            ubicacion: state.ubicacion,
            sedes_adicionales: sedesClean.join(' | '),
            escala: state.observaciones,
            pagina_origen: window.location.pathname,
            website_hp: hp
          };

          var subBtn = document.getElementById('su-wiz-submit');
          var errBox = document.getElementById('su-wiz-step3-err');
          subBtn.disabled = true;
          subBtn.textContent = 'Enviando solicitud...';
          errBox.style.display = 'none';

          submitPayloadToApi(
            payload,
            function () {
              fireQualifiedLeadEvents(payload, sedesClean.length > 0);
              state.subview = 'done';
              renderWizard();
            },
            function () {
              subBtn.disabled = false;
              subBtn.textContent = 'Enviar solicitud a Comercial';
              errBox.textContent = 'No pudimos registrar el envío en este instante. Por favor intentá otra vez o escribinos a comercial@starunion.com.ar.';
              errBox.style.display = 'block';
            }
          );
        });
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    injectGlobalUxStyles();
    initStepWizard();

    // Marcar botón flotante de WhatsApp para compactarlo en celular y ocultarlo cuando el cotizador o inputs están activos
    document.querySelectorAll('a.fixed[href*="whatsapp"], a.fixed[href*="wa.me"], a.fixed[href="#atencion-whatsapp"]').forEach(function (el) {
      el.classList.add('su-wa-floating-btn');
    });

    document.addEventListener('focusin', function (e) {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA')) {
        document.body.classList.add('su-input-focused');
      }
    });
    document.addEventListener('focusout', function () {
      setTimeout(function () {
        var ae = document.activeElement;
        if (!ae || (ae.tagName !== 'INPUT' && ae.tagName !== 'SELECT' && ae.tagName !== 'TEXTAREA')) {
          document.body.classList.remove('su-input-focused');
        }
      }, 150);
    });

    // Disparadores del Cotizador Guiado Paso a Paso (/cotizar/) con contexto de rubro y página de origen
    document.querySelectorAll('[data-open-cotizador], a[href="#cotizar-form"], a[href="#formulario-cotizacion"]').forEach(function (trigger) {
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        var rubroAttr = trigger.getAttribute('data-rubro') || '';
        var locAttr = trigger.getAttribute('data-localidad') || '';
        window.location.href = resolveCotizarLandingUrl({ rubro: rubroAttr, localidad: locAttr });
      });
    });

    if (window.location.search && window.location.search.indexOf('cotizar=1') !== -1) {
      window.location.href = resolveCotizarLandingUrl();
    }

    // Anclas a #contacto (deslizar suave a la sección de datos y formulario inferior)
    document.querySelectorAll('a[href="#contacto"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var targetEl = document.getElementById('contacto');
        if (!targetEl) return;
        e.preventDefault();
        var mobileDrawer = document.getElementById('mobile-nav-drawer');
        if (mobileDrawer && !mobileDrawer.classList.contains('hidden')) {
          mobileDrawer.classList.add('hidden');
        }
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    // Formularios completos embebidos al pie (#contacto)
    var b2bForms = document.querySelectorAll('.js-b2b-quote-form');

    b2bForms.forEach(function (form) {
      var tipoSelect = form.querySelector('[name="tipo_organizacion"]');
      var otroWrap = form.querySelector('.js-otro-rubro-wrap');
      var otroInput = form.querySelector('[name="otro_rubro_detalle"]');
      var regularWrap = form.querySelector('.js-regular-dotacion-wrap');
      var especialWrap = form.querySelector('.js-especial-servicio-wrap');
      var especialidadSelect = form.querySelector('[name="especialidad_requerida"]');
      var escalaEspecialInput = form.querySelector('[name="escala_especial"]');
      var personasSelect = form.querySelector('[name="cantidad_personas"]');
      var horasSelect = form.querySelector('[name="cantidad_horas"]');
      var diasSelect = form.querySelector('[name="dias_servicio"]');
      var warningBox = form.querySelector('.b2b-warning-alert');
      var submitBtn = form.querySelector('button[type="submit"]');

      var addSedeBtn = form.querySelector('.js-add-sede-btn');
      var sedesList = form.querySelector('.js-multi-sede-list');

      if (addSedeBtn && sedesList) {
        addSedeBtn.addEventListener('click', function () {
          var count = sedesList.querySelectorAll('.js-sede-extra-row').length;
          if (count >= 6) return;
          var row = document.createElement('div');
          row.className = 'js-sede-extra-row grid grid-cols-1 sm:grid-cols-12 gap-2 pt-2 items-center';
          row.innerHTML = [
            '<input type="text" placeholder="Sede adicional (localidad / dirección)" class="js-sede-loc sm:col-span-6 w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-xs focus:border-brand outline-none">',
            '<input type="text" placeholder="Dotación u horario estimado en esa sede" class="js-sede-dot sm:col-span-5 w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-xs focus:border-brand outline-none">',
            '<button type="button" title="Quitar sede" class="js-remove-sede sm:col-span-1 text-gray-400 hover:text-gray-800 font-bold text-sm py-1 cursor-pointer">✕</button>'
          ].join('');
          row.querySelector('.js-remove-sede').addEventListener('click', function () {
            row.remove();
          });
          sedesList.appendChild(row);
        });
      }

      function evaluateFormState() {
        var val = tipoSelect ? tipoSelect.value : '';
        var horasVal = horasSelect ? horasSelect.value : '';
        var espVal = especialidadSelect ? especialidadSelect.value : '';
        var isEspecial = val.indexOf('Servicios especiales') !== -1;

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

        if (regularWrap && especialWrap) {
          if (isEspecial) {
            regularWrap.classList.add('hidden');
            especialWrap.classList.remove('hidden');
            if (personasSelect) personasSelect.required = false;
            if (horasSelect) horasSelect.required = false;
            if (diasSelect) diasSelect.required = false;
            if (especialidadSelect) especialidadSelect.required = true;
            if (escalaEspecialInput) escalaEspecialInput.required = true;
          } else {
            regularWrap.classList.remove('hidden');
            especialWrap.classList.add('hidden');
            if (personasSelect) personasSelect.required = true;
            if (horasSelect) horasSelect.required = true;
            if (diasSelect) diasSelect.required = true;
            if (especialidadSelect) {
              especialidadSelect.required = false;
              especialidadSelect.value = '';
            }
            if (escalaEspecialInput) {
              escalaEspecialInput.required = false;
              escalaEspecialInput.value = '';
            }
          }
        }

        var blockedMsg = '';
        if (val.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Star Union S.R.L. presta servicios exclusivos para empresas, industrias, edificios corporativos, consorcios e instituciones (esquemas desde 4 hs diarias corridas).';
        } else if (!isEspecial && horasVal.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Para sostener supervisión activa, control biométrico y cobertura de ausencias bajo ISO 9001:2015, nuestros esquemas operativos parten de jornadas mínimas de 4 horas diarias corridas.';
        } else if (isEspecial && espVal.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Nuestra división de Servicios Especiales opera en forma exclusiva para plantas industriales, edificios corporativos, grandes predios y centros comerciales.';
        }

        if (warningBox) {
          if (blockedMsg) {
            warningBox.textContent = blockedMsg;
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
      }

      if (tipoSelect) tipoSelect.addEventListener('change', evaluateFormState);
      if (horasSelect) horasSelect.addEventListener('change', evaluateFormState);
      if (especialidadSelect) especialidadSelect.addEventListener('change', evaluateFormState);
      evaluateFormState();

      form.addEventListener('submit', function (e) {
        e.preventDefault();

        var empresa = (form.querySelector('[name="empresa"]')?.value || '').trim();
        var nombre = (form.querySelector('[name="nombre"]')?.value || '').trim();
        var emailInput = form.querySelector('[name="email"]');
        var telInput = form.querySelector('[name="telefono"]');
        var legacyCargo = form.querySelector('[name="cargo"]');

        var email = (emailInput ? emailInput.value : (legacyCargo ? legacyCargo.value : '')).trim();
        var telefono = (telInput ? telInput.value : '').trim();

        var tipoBase = form.querySelector('[name="tipo_organizacion"]')?.value || '';
        var otroDetalle = (form.querySelector('[name="otro_rubro_detalle"]')?.value || '').trim();
        var especialidad = (form.querySelector('[name="especialidad_requerida"]')?.value || '').trim();
        var escalaEspecial = (form.querySelector('[name="escala_especial"]')?.value || '').trim();
        var cantidadPersonas = (form.querySelector('[name="cantidad_personas"]')?.value || '').trim();
        var cantidadHoras = (form.querySelector('[name="cantidad_horas"]')?.value || '').trim();
        var diasServicio = (form.querySelector('[name="dias_servicio"]')?.value || '').trim();
        var ubicacion = (form.querySelector('[name="ubicacion"]')?.value || '').trim();
        var observaciones = (form.querySelector('[name="escala"]')?.value || form.querySelector('[name="mensaje"]')?.value || '').trim();
        var hp = (form.querySelector('[name="website_hp"]')?.value || '').trim();

        if (
          !tipoBase ||
          tipoBase.indexOf('NO_CALIFICA') === 0 ||
          cantidadHoras.indexOf('NO_CALIFICA') === 0 ||
          especialidad.indexOf('NO_CALIFICA') === 0
        ) {
          evaluateFormState();
          return;
        }

        var sedesExtras = [];
        if (sedesList) {
          sedesList.querySelectorAll('.js-sede-extra-row').forEach(function (r) {
            var loc = (r.querySelector('.js-sede-loc')?.value || '').trim();
            var dot = (r.querySelector('.js-sede-dot')?.value || '').trim();
            if (loc || dot) {
              sedesExtras.push(loc + (dot ? ' (' + dot + ')' : ''));
            }
          });
        }

        var payload = {
          empresa: empresa,
          nombre: nombre,
          email: email,
          telefono: telefono,
          tipo_organizacion: tipoBase,
          otro_rubro_detalle: otroDetalle,
          especialidad_requerida: especialidad,
          escala_especial: escalaEspecial,
          cantidad_personas: cantidadPersonas,
          cantidad_horas: cantidadHoras,
          dias_servicio: diasServicio,
          ubicacion: ubicacion,
          sedes_adicionales: sedesExtras.join(' | '),
          escala: observaciones,
          pagina_origen: window.location.pathname,
          website_hp: hp
        };

        var origBtnText = submitBtn ? submitBtn.textContent : '';
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Enviando solicitud a Comercial...';
        }

        submitPayloadToApi(
          payload,
          function (resData) {
            fireQualifiedLeadEvents(payload, sedesExtras.length > 0);
            var cNom2 = nombre.replace(/[,\s]+$/, '').trim().replace(/</g, '&lt;');
            var cEmp2 = empresa.replace(/[,\s]+$/, '').trim().replace(/</g, '&lt;');
            var h4Txt = (cEmp2 && cEmp2.toLowerCase() !== cNom2.toLowerCase())
              ? ('Gracias, ' + cNom2 + '. Registramos la solicitud de ' + cEmp2 + '.')
              : ('Gracias, ' + cNom2 + '. Registramos tu solicitud comercial.');
            var previewBtn = (resData && resData.preview_url)
              ? '<div class="pt-1"><a href="' + resData.preview_url + '" target="_blank" rel="noopener noreferrer" class="text-xs font-extrabold text-brand underline">Ver comprobante estructurado de la solicitud ↗</a></div>'
              : '';
            var confirmBox = document.createElement('div');
            confirmBox.className = 'bg-white border border-gray-200 border-t-4 border-t-brand rounded-2xl p-6 text-left space-y-3 shadow-sm';
            confirmBox.innerHTML = [
              '<div class="inline-flex items-center gap-2 bg-[#eef6f1] text-brand text-xs font-extrabold uppercase tracking-wider px-3 py-1 rounded-full">',
                '✓ Solicitud recibida',
              '</div>',
              '<h4 class="text-lg font-extrabold text-[#000000]">' + h4Txt + '</h4>',
              '<p class="text-sm text-[#676b67] leading-relaxed">',
                'Dirección Comercial analizará el requerimiento y responderá en forma directa a <strong class="text-[#000000]">' + email.replace(/</g, '&lt;') + '</strong> o al <strong class="text-[#000000]">' + telefono.replace(/</g, '&lt;') + '</strong>.',
              '</p>',
              previewBtn,
              '<div class="pt-2 border-t border-gray-200 text-xs text-[#676b67] flex flex-wrap items-center justify-between gap-2">',
                '<span>Atención telefónica directa: <strong class="text-brand">0810-333-UNION (8646)</strong></span>',
                '<span>Base Central Guaminí 5657, CABA · ISO 9001:2015</span>',
              '</div>'
            ].join('');
            form.replaceWith(confirmBox);
          },
          function () {
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = origBtnText;
            }
            if (warningBox) {
              warningBox.textContent = 'No pudimos registrar el envío en este instante. Por favor intentá otra vez o comunicate directo al 0810-333-UNION (8646) o a comercial@starunion.com.ar.';
              warningBox.classList.remove('hidden');
              warningBox.style.display = 'block';
            }
          }
        );
      });
    });
  });

  // Modal de derivación de las 3 puertas en WhatsApp
  document.addEventListener('DOMContentLoaded', function () {
    var waLinks = document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"], a[data-wa-trigger="1"]');
    if (!waLinks.length) return;

    var modal = document.getElementById('su-wa-filter-modal');
    function resetModalToMain() {
      var mainView = document.getElementById('su-wa-main-view');
      var comprasView = document.getElementById('su-wa-compras-view');
      if (mainView) mainView.style.display = 'block';
      if (comprasView) comprasView.style.display = 'none';
    }
    function closeModal() {
      if (modal) modal.style.display = 'none';
      document.body.classList.remove('su-overlay-active');
      resetModalToMain();
    }

    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'su-wa-filter-modal';
      modal.style.cssText = 'display:none;position:fixed;inset:0;z-index:9999;background:rgba(15,23,42,0.48);backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);align-items:center;justify-content:center;padding:16px;';
      modal.innerHTML = [
        "<div role='dialog' aria-modal='true' style='background:#ffffff;max-width:440px;width:100%;border-radius:18px;padding:24px;box-shadow:0 24px 48px rgba(0,0,0,0.24);border-top:4px solid #03582d;font-family:\"Open Sans\",sans-serif;'>",
          "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>",
            "<span style='font-size:11px;font-weight:800;text-transform:uppercase;color:#03582d;letter-spacing:0.06em;'>Atención directa · Star Union S.R.L.</span>",
            "<button type='button' id='su-wa-close' aria-label='Cerrar ventana' style='background:none;border:none;font-size:18px;line-height:1;cursor:pointer;color:#6b7280;padding:4px;'>✕</button>",
          "</div>",

          "<div id='su-wa-main-view'>",
            "<h3 style='font-size:18px;font-weight:800;color:#000000;margin:0 0 6px 0;line-height:1.25;'>¿Con qué área necesitás comunicarte?</h3>",
            "<p style='font-size:13px;color:#4b5563;margin:0 0 16px 0;line-height:1.45;'>Seleccioná una opción para derivarte con el canal correspondiente en una pestaña nueva:</p>",
            "<div style='display:flex;flex-direction:column;gap:10px;'>",
              "<a id='su-wa-go-b2b' href='#' target='_blank' rel='noopener noreferrer' style='display:block;background:#03582d;color:#ffffff;padding:14px 16px;border-radius:10px;text-decoration:none;border:1px solid #03582d;transition:background 0.15s;'>",
                "<span style='display:flex;align-items:center;justify-content:space-between;font-weight:800;font-size:13.5px;'>",
                  "<span>Solicitar cotización para mi empresa o institución</span>",
                  "<svg width='15' height='15' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M9 5l7 7-7 7'/></svg>",
                "</span>",
                "<span style='display:block;font-size:11.5px;font-weight:400;color:rgba(255,255,255,0.88);margin-top:3px;'>Exclusivo empresas, industrias, instituciones y consorcios (sin viviendas particulares).</span>",
              "</a>",

              "<a id='su-wa-go-rrhh' href='" + RRHH_GOOGLE_FORM_URL + "' target='_blank' rel='noopener noreferrer' style='display:flex;align-items:center;justify-content:space-between;background:#f9fafb;color:#111827;font-weight:700;font-size:13px;padding:12px 16px;border-radius:10px;border:1px solid #d1d5db;text-decoration:none;'>",
                "<span>Busco trabajo / Cargar CV en Recursos Humanos</span>",
                "<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#03582d' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg>",
              "</a>",

              "<button type='button' id='su-wa-open-compras' style='display:flex;align-items:center;justify-content:space-between;width:100%;text-align:left;background:#ffffff;color:#374151;font-weight:700;font-size:13px;padding:12px 16px;border-radius:10px;border:1px solid #e5e7eb;cursor:pointer;font-family:\"Open Sans\",sans-serif;'>",
                "<span>Soy proveedor de insumos o servicios</span>",
                "<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#6b7280' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M9 5l7 7-7 7'/></svg>",
              "</button>",
            "</div>",
          "</div>",

          "<div id='su-wa-compras-view' style='display:none;'>",
            "<button type='button' id='su-wa-back-main' style='display:inline-flex;align-items:center;gap:5px;background:none;border:none;padding:0;margin:0 0 12px 0;font-size:12px;font-weight:700;color:#03582d;cursor:pointer;font-family:\"Open Sans\",sans-serif;'><svg width='13' height='13' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'><path d='M15 19l-7-7 7-7'/></svg><span>Volver</span></button>",
            "<h3 style='font-size:17px;font-weight:800;color:#000000;margin:0 0 8px 0;line-height:1.3;'>Recepción de propuestas de proveedores</h3>",
            "<p style='font-size:13px;color:#374151;margin:0 0 14px 0;line-height:1.5;'>Copiá la casilla de Compras y envianos tu presentación o catálogo por correo:</p>",
            "<div style='display:flex;align-items:center;justify-content:space-between;gap:10px;background:#f9fafb;border:1px solid #d1d5db;border-radius:10px;padding:11px 14px;'>",
              "<span style='font-weight:800;color:#000000;font-size:13.5px;user-select:all;'>" + EMAIL_COMPRAS + "</span>",
              "<button type='button' id='su-copy-compras-btn' style='background:#03582d;border:none;border-radius:8px;padding:7px 12px;font-size:12px;font-weight:700;cursor:pointer;color:#ffffff;font-family:\"Open Sans\",sans-serif;white-space:nowrap;'>Copiar correo</button>",
            "</div>",
          "</div>",
        "</div>"
      ].join('');
      document.body.appendChild(modal);

      document.getElementById('su-wa-close').addEventListener('click', closeModal);
      modal.addEventListener('click', function (e) {
        if (e.target === modal) closeModal();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') closeModal();
      });

      document.getElementById('su-wa-go-b2b').addEventListener('click', function () {
        if (typeof window.gtag === 'function') {
          window.gtag('event', 'contacto_wa_empresa_b2b', {
            event_category: 'B2B_Lead',
            source_page: window.location.pathname
          });
        }
        closeModal();
      });

      document.getElementById('su-wa-go-rrhh').addEventListener('click', function () {
        if (typeof window.gtag === 'function') {
          window.gtag('event', 'salida_rrhh_form', { ubicacion: 'modal_whatsapp' });
        }
        closeModal();
      });

      document.getElementById('su-wa-open-compras').addEventListener('click', function () {
        document.getElementById('su-wa-main-view').style.display = 'none';
        document.getElementById('su-wa-compras-view').style.display = 'block';
      });

      document.getElementById('su-wa-back-main').addEventListener('click', function () {
        resetModalToMain();
      });

      document.getElementById('su-copy-compras-btn').addEventListener('click', function () {
        copyPlainText(EMAIL_COMPRAS, this, '✓ Copiado');
      });
    }

    waLinks.forEach(function (link) {
      if (link.id === 'su-wa-go-b2b') return;
      var origHref = link.getAttribute('href') || '';
      if (origHref && origHref !== '#atencion-whatsapp') {
        link.setAttribute('data-wa-orig-href', origHref);
        if (link.id !== 'vBtnWa') {
          link.setAttribute('href', '#atencion-whatsapp');
          link.removeAttribute('target');
        }
      }

      link.addEventListener('click', function (e) {
        e.preventDefault();
        var currentDynamicHref = link.id === 'vBtnWa'
          ? (link.getAttribute('href') || link.getAttribute('data-wa-orig-href') || '')
          : (link.getAttribute('data-wa-orig-href') || '');
        var cleanMsg = buildContextualWaMessage(window.location.pathname, currentDynamicHref);
        var finalUrl = buildWaEndpoint(cleanMsg);
        var b2bBtn = document.getElementById('su-wa-go-b2b');
        if (b2bBtn) b2bBtn.setAttribute('href', finalUrl);
        resetModalToMain();
        document.body.classList.add('su-overlay-active');
        modal.style.display = 'flex';
      });
    });
  });
})();
