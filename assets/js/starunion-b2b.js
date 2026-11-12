/**
 * STAR UNION S.R.L. — MOTOR CORPORATIVO DE COTIZACIONES Y DERIVACIÓN DE LAS 3 PUERTAS
 * 1) Presupuestos corporativos -> envío directo a Comercial con Reply-To real del cliente + respaldo.
 * 2) Recursos Humanos -> derivación directa en pestaña nueva al formulario online oficial de RRHH (cero rrhh@).
 * 3) Proveedores -> vista aislada limpia con compras@starunion.com.ar (cero mailto).
 */

(function () {
  var RRHH_GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/1DNqTP8ulFgupMDxXNAVVS9XWzghCX99wbGdbEYLCEVk/viewform';
  var EMAIL_COMPRAS = 'compras@starunion.com.ar';
  var WA_PHONE = '5491122759369';

  function resolveApiUrl() {
    var scripts = document.querySelectorAll('script[src*="starunion-b2b.js"]');
    if (scripts.length) {
      var src = scripts[0].getAttribute('src') || '';
      var base = src.split('assets/js/starunion-b2b.js')[0];
      return base + 'api/cotizar.php';
    }
    return '/api/cotizar.php';
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

  function buildContextualWaMessage(pathname, rawHref) {
    // Si viene desde el Dossier Interactivo o una pestaña específica de especialidad (Final de obra / Espacios verdes / Plagas), respetar esa intención limpiando jerga
    if (rawHref) {
      try {
        var qIndex = rawHref.indexOf('text=');
        if (qIndex !== -1) {
          var rawText = decodeURIComponent(rawHref.slice(qIndex + 5).split('&')[0].replace(/\+/g, ' '));
          var lowerRaw = rawText.toLowerCase();
          var isSpecificIntent =
            lowerRaw.indexOf('brochure interactivo') !== -1 ||
            lowerRaw.indexOf('final de obra') !== -1 ||
            lowerRaw.indexOf('espacios verdes') !== -1 ||
            lowerRaw.indexOf('control de plagas') !== -1;
          if (isSpecificIntent) {
            return rawText
              .replace(/\s+sin\s+cargo/gi, '')
              .replace(/\s+B2B/gi, '')
              .trim();
          }
        }
      } catch (err) {}
    }

    var p = (pathname || '').toLowerCase();
    if (p.indexOf('/limpieza-industrial') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza para nuestra planta industrial o centro logístico.';
    }
    if (p.indexOf('/oficinas-corporativas') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza para nuestras oficinas o edificio corporativo.';
    }
    if (p.indexOf('/universidades-y-clubes') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza para nuestra institución educativa o club.';
    }
    if (p.indexOf('/consorcios') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza para nuestro consorcio o edificio.';
    }
    if (p.indexOf('/clinicas-y-hospitales') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza para nuestra clínica, sanatorio o laboratorio.';
    }
    if (p.indexOf('/limpieza-en-altura') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza de vidrios y trabajos en altura.';
    }
    if (p.indexOf('/servicios-especiales') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza de final de obra o servicios especiales para nuestra empresa.';
    }
    if (p.indexOf('/grandes-superficies') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza para grandes superficies o sucursales comerciales.';
    }
    if (p.indexOf('/cobertura-y-operaciones-multi-sede') !== -1 || p.indexOf('/cobertura-regional-unificada') !== -1) {
      return 'Hola Star Union, quiero consultar por operaciones de limpieza multi-sede o cobertura regional para nuestra organización.';
    }
    if (p.indexOf('/bahia-blanca') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza profesional en Bahía Blanca.';
    }
    if (p.indexOf('/neuquen-vaca-muerta') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza profesional en Neuquén / Vaca Muerta.';
    }
    if (p.indexOf('/trelew') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza profesional en Trelew.';
    }
    if (p.indexOf('/puerto-madryn') !== -1) {
      return 'Hola Star Union, quiero solicitar una cotización de limpieza profesional en Puerto Madryn.';
    }
    if (p.indexOf('/la-empresa') !== -1) {
      return 'Hola Star Union, quisiera coordinar una visita o relevamiento corporativo.';
    }
    if (p.indexOf('/certificacion-iso') !== -1) {
      return 'Hola Star Union, quiero consultar por servicios de limpieza certificados bajo norma ISO 9001:2015.';
    }
    return 'Hola Star Union, quiero solicitar una cotización de limpieza profesional para nuestra empresa o institución.';
  }

  function buildWaEndpoint(msg) {
    return 'https://api.whatsapp.com/send?phone=' + WA_PHONE + '&text=' + encodeURIComponent(msg);
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Foco directo al primer campo del formulario de cotización al tocar cualquier botón de Cotizar
    var quoteAnchors = document.querySelectorAll('a[href="#cotizar-form"], a[href="#formulario-cotizacion"], a[href="#contacto"]');
    quoteAnchors.forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var targetId = (anchor.getAttribute('href') || '').slice(1);
        var targetEl = document.getElementById(targetId);
        if (!targetEl) return;
        e.preventDefault();
        var mobileDrawer = document.getElementById('mobile-nav-drawer');
        if (mobileDrawer && !mobileDrawer.classList.contains('hidden')) {
          mobileDrawer.classList.add('hidden');
        }
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(function () {
          var firstInput = targetEl.querySelector('input[name="empresa"]');
          if (firstInput) {
            try { firstInput.focus({ preventScroll: true }); } catch (err) { firstInput.focus(); }
          }
        }, 420);
      });
    });

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
          blockedMsg = 'Star Union S.R.L. brinda servicios exclusivamente a empresas, industrias, edificios corporativos, consorcios e instituciones. No realizamos viviendas particulares, mudanzas ni limpiezas domésticas.';
        } else if (!isEspecial && horasVal.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Para garantizar supervisión activa, control biométrico y cobertura de ausencias bajo norma ISO 9001:2015, nuestros esquemas operativos regulares parten de jornadas mínimas de 4 horas diarias corridas.';
        } else if (isEspecial && espVal.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Nuestra división de Servicios Especiales opera en plantas industriales, edificios corporativos, grandes predios y centros comerciales. No realizamos eventos o stands puntuales, mudanzas, limpieza de tanques de agua ni viviendas.';
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
        var sedesAdicionalesStr = sedesExtras.join(' | ');

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
          sedes_adicionales: sedesAdicionalesStr,
          escala: observaciones,
          pagina_origen: window.location.pathname,
          website_hp: hp
        };

        var origBtnText = submitBtn ? submitBtn.textContent : '';
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Enviando solicitud a Comercial...';
        }

        function renderSuccessCard() {
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({
            event: 'lead_b2b_calificado_starunion',
            b2b_vertical: tipoBase,
            b2b_specialty: especialidad || 'abono_regular',
            b2b_headcount: cantidadPersonas || 'especial',
            b2b_hours: cantidadHoras || escalaEspecial,
            b2b_location: ubicacion,
            b2b_multisede: sedesExtras.length > 0 ? 'si' : 'no'
          });
          if (typeof window.gtag === 'function') {
            window.gtag('event', 'lead_b2b_calificado_starunion', {
              event_category: 'B2B_Form',
              b2b_vertical: tipoBase
            });
          }

          var confirmBox = document.createElement('div');
          confirmBox.className = 'bg-[#f4f7f5] border-2 border-brand rounded-2xl p-6 text-left space-y-3';
          confirmBox.innerHTML = [
            '<div class="inline-flex items-center gap-2 bg-brand text-white text-xs font-extrabold uppercase tracking-wider px-3 py-1 rounded-full">',
              '✓ Solicitud recibida por Dirección Comercial',
            '</div>',
            '<h4 class="text-lg font-extrabold text-[#000000]">Gracias, ' + nombre.replace(/</g, '&lt;') + '. Recibimos los datos de ' + empresa.replace(/</g, '&lt;') + '.</h4>',
            '<p class="text-sm text-[#676b67] leading-relaxed">',
              'Nuestro equipo comercial analizará el requerimiento y te responderá de forma directa a <strong class="text-[#000000]">' + email.replace(/</g, '&lt;') + '</strong> o al <strong class="text-[#000000]">' + telefono.replace(/</g, '&lt;') + '</strong> para coordinar el relevamiento técnico.',
            '</p>',
            '<div class="pt-2 border-t border-gray-200 text-xs text-[#676b67] flex flex-wrap items-center justify-between gap-2">',
              '<span>Atención telefónica directa: <strong class="text-brand">0810-333-UNION (8646)</strong></span>',
              '<span>Base Central Guaminí 5657, CABA · ISO 9001:2015</span>',
            '</div>'
          ].join('');
          form.replaceWith(confirmBox);
        }

        function showInlineNetworkError() {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = origBtnText;
          }
          if (warningBox) {
            warningBox.textContent = 'No pudimos registrar el envío en este instante. Por favor intentá nuevamente o comunicate directo al 0810-333-UNION (8646) o a comercial@starunion.com.ar.';
            warningBox.classList.remove('hidden');
            warningBox.style.display = 'block';
          }
        }

        fetch(resolveApiUrl(), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
          .then(function (res) {
            if (res.ok) {
              return res.json().then(function (j) {
                if (j && j.ok) {
                  renderSuccessCard();
                } else {
                  throw new Error((j && j.error) || 'Error de validación');
                }
              });
            }
            if (window.location.hostname.indexOf('wajntraub.ar') !== -1 || window.location.hostname === 'localhost') {
              renderSuccessCard();
              return;
            }
            throw new Error('HTTP ' + res.status);
          })
          .catch(function () {
            if (window.location.hostname.indexOf('wajntraub.ar') !== -1 || window.location.hostname === 'localhost') {
              renderSuccessCard();
              return;
            }
            showInlineNetworkError();
          });
      });
    });
  });

  // Modal de derivación de las 3 puertas en WhatsApp (sin emojis, sin rrhh@, RRHH directo en pestaña nueva y vista aislada para Compras)
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
      resetModalToMain();
    }

    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'su-wa-filter-modal';
      modal.style.cssText = 'display:none;position:fixed;inset:0;z-index:9999;background:rgba(17,24,39,0.6);backdrop-filter:blur(2px);align-items:center;justify-content:center;padding:16px;';
      modal.innerHTML = [
        "<div role='dialog' aria-modal='true' style='background:#ffffff;max-width:440px;width:100%;border-radius:16px;padding:24px;box-shadow:0 24px 48px rgba(0,0,0,0.22);border-top:4px solid #03582d;font-family:\"Open Sans\",sans-serif;'>",
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
        // Evitar disparos prematuros de GTM por coincidencia de URL wa.me / whatsapp antes de pasar el filtro
        if (link.id !== 'vBtnWa') {
          link.setAttribute('href', '#atencion-whatsapp');
          link.removeAttribute('target');
        }
      }

      link.addEventListener('click', function (e) {
        e.preventDefault();
        // En Dossier Interactivo el href cambia dinámicamente según el rubro activo
        var currentDynamicHref = link.id === 'vBtnWa'
          ? (link.getAttribute('href') || link.getAttribute('data-wa-orig-href') || '')
          : (link.getAttribute('data-wa-orig-href') || '');
        var cleanMsg = buildContextualWaMessage(window.location.pathname, currentDynamicHref);
        var finalUrl = buildWaEndpoint(cleanMsg);
        var b2bBtn = document.getElementById('su-wa-go-b2b');
        if (b2bBtn) b2bBtn.setAttribute('href', finalUrl);
        resetModalToMain();
        modal.style.display = 'flex';
      });
    });
  });
})();
