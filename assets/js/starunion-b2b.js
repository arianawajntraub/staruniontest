/**
 * STAR UNION S.R.L. — MOTOR DE CONVERSIÓN B2B, FILTRO DE ALCANCE Y SEPARACIÓN DE LAS 3 PUERTAS
 * 1) Presupuestos B2B -> envío directo en página a contacto@starunion.com.ar con Reply-To al cliente + respaldo.
 * 2) Recursos Humanos -> formulario online oficial de RRHH + rrhh@starunion.com.ar + Portal del equipo (Browix).
 * 3) Proveedores -> compras@starunion.com.ar visible para copiar en 1 clic (cero mailto, cero WhatsApp comercial).
 */

(function () {
  var RRHH_GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/1DNqTP8ulFgupMDxXNAVVS9XWzghCX99wbGdbEYLCEVk/viewform';
  var EMAIL_RRHH = 'rrhh@starunion.com.ar';
  var EMAIL_COMPRAS = 'compras@starunion.com.ar';

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
      btn.textContent = feedbackText || '✓ Correo copiado';
      setTimeout(function () {
        btn.textContent = orig;
      }, 2200);
    }
  }

  // Exponer utilidad global para botones "Copiar correo" en #contacto / #postularse
  window.suCopyEmail = function (emailStr, btnEl) {
    copyPlainText(emailStr, btnEl, '✓ Copiado: ' + emailStr);
  };

  document.addEventListener('DOMContentLoaded', function () {
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

      // Multi-sede dinámico (oculto por defecto para el 80%+ de consultas de 1 sola ubicación)
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
            '<button type="button" title="Quitar sede" class="js-remove-sede sm:col-span-1 text-gray-400 hover:text-gray-800 font-bold text-sm py-1">✕</button>'
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

        // Mostrar u ocultar campo "Otro rubro"
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

        // Alternar unidad de medida: Dotación/Horas semanales (1° a 5°) vs. Especialidad/Alcance (6° Servicios especiales)
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

        // Evaluar bloqueos corteses (viviendas, mudanzas, pocas horas aisladas o eventos/tanques)
        var blockedMsg = '';
        if (val.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Star Union S.R.L. brinda servicios exclusivamente a empresas, industrias, edificios corporativos, consorcios e instituciones. No realizamos viviendas particulares, mudanzas ni limpiezas domésticas.';
        } else if (!isEspecial && horasVal.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Para garantizar supervisión activa, control biométrico y reemplazo de ausencias bajo norma ISO 9001:2015, nuestros esquemas operativos regulares parten de jornadas mínimas de 4 horas diarias corridas.';
        } else if (isEspecial && espVal.indexOf('NO_CALIFICA') === 0) {
          blockedMsg = 'Nuestra división de Servicios Especiales opera en plantas industriales, edificios corporativos, grandes predios y centros comerciales. No realizamos eventos o stands puntuales, mudanzas, limpieza de tanques domiciliarios ni viviendas.';
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
          tipoBase.indexOf('NO_CALIFICA') === 0 ||
          cantidadHoras.indexOf('NO_CALIFICA') === 0 ||
          especialidad.indexOf('NO_CALIFICA') === 0
        ) {
          evaluateFormState();
          return;
        }

        // Recolectar sedes adicionales si se cargaron
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
          // Disparar conversión primaria limpia para GA4 / Google Ads SOLO tras envío válido B2B
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
              'Nuestro equipo comercial analizará el esquema solicitado y te responderá de forma directa a <strong class="text-[#000000]">' + email.replace(/</g, '&lt;') + '</strong> o al <strong class="text-[#000000]">' + telefono.replace(/</g, '&lt;') + '</strong> para coordinar el relevamiento técnico.',
            '</p>',
            '<div class="pt-2 border-t border-gray-200 text-xs text-[#676b67] flex flex-wrap items-center justify-between gap-2">',
              '<span>Atención telefónica directa: <strong class="text-brand">0810-333-UNION (8646)</strong></span>',
              '<span>Base Central Guaminí 5657, CABA · ISO 9001:2015</span>',
            '</div>'
          ].join('');
          form.replaceWith(confirmBox);
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
            // En entorno estático de previsualización (GitHub Pages sin motor PHP activo), mostrar confirmación visual de prueba
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
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = origBtnText;
            }
            alert('No pudimos conectar con el servidor en este instante. Podés comunicarte directo al 0810-333-UNION (8646) o escribir a contacto@starunion.com.ar.');
          });
      });
    });
  });

  // Micro-filtro tecnológico de 3 puertas en botones de WhatsApp (separa Empresas, RRHH y Proveedores)
  document.addEventListener('DOMContentLoaded', function () {
    var waLinks = document.querySelectorAll('a[href*="api.whatsapp.com"], a[href*="wa.me"]');
    if (!waLinks.length) return;

    var modal = document.getElementById('su-wa-filter-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'su-wa-filter-modal';
      modal.style.cssText = 'display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.55);align-items:center;justify-content:center;padding:16px;';
      modal.innerHTML = [
        "<div style='background:#ffffff;max-width:440px;width:100%;border-radius:16px;padding:24px;box-shadow:0 20px 40px rgba(0,0,0,0.25);border-top:5px solid #03582d;font-family:\"Open Sans\",sans-serif;'>",
          "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>",
            "<span style='font-size:11px;font-weight:800;text-transform:uppercase;color:#03582d;letter-spacing:0.05em;'>Atención directa Star Union</span>",
            "<button type='button' id='su-wa-close' aria-label='Cerrar ventana' style='background:none;border:none;font-size:18px;cursor:pointer;color:#6b7280;'>✕</button>",
          "</div>",
          "<h3 style='font-size:18px;font-weight:800;color:#000000;margin:0 0 6px 0;'>¿Con qué área querés comunicarte?</h3>",
          "<p style='font-size:13px;color:#4b5563;margin:0 0 16px 0;line-height:1.45;'>Seleccioná una opción para derivarte con el equipo correspondiente sin demoras:</p>",
          "<div style='display:flex;flex-direction:column;gap:10px;'>",
            "<a id='su-wa-go-b2b' href='#' target='_blank' rel='noopener' style='display:block;text-align:center;background:#03582d;color:#ffffff;font-weight:800;font-size:13.5px;padding:14px 16px;border-radius:10px;text-decoration:none;'>🏢 Solicitar cotización para mi empresa o institución →</a>",
            "<button type='button' id='su-wa-toggle-rrhh' style='width:100%;text-align:center;background:#f3f4f6;color:#111827;font-weight:700;font-size:13px;padding:12px 16px;border-radius:10px;border:1px solid #d1d5db;cursor:pointer;font-family:\"Open Sans\",sans-serif;'>👷 Busco trabajo / enviar CV a Recursos Humanos</button>",
            "<div id='su-wa-rrhh-panel' style='display:none;background:#f9fafb;border:1px solid #d1d5db;border-radius:10px;padding:12px;font-size:12px;color:#374151;'>",
              "<p style='margin:0 0 8px 0;line-height:1.4;'><strong>Canal exclusivo de Recursos Humanos:</strong> El WhatsApp comercial no recibe currículums. Cargá tus datos online o escribí a RRHH:</p>",
              "<a href='" + RRHH_GOOGLE_FORM_URL + "' target='_blank' rel='noopener' style='display:block;text-align:center;background:#111827;color:#ffffff;font-weight:700;padding:10px 12px;border-radius:8px;text-decoration:none;margin-bottom:8px;'>📋 Completar formulario online de postulación ↗</a>",
              "<div style='display:flex;align-items:center;justify-content:space-between;gap:8px;background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:7px 10px;margin-bottom:6px;'>",
                "<span style='font-weight:700;color:#000000;'>" + EMAIL_RRHH + "</span>",
                "<button type='button' id='su-copy-rrhh-btn' style='background:#f3f4f6;border:1px solid #d1d5db;border-radius:6px;padding:4px 8px;font-size:11px;font-weight:700;cursor:pointer;color:#111827;'>Copiar correo</button>",
              "</div>",
              "<a href='https://browix.com' target='_blank' rel='noopener' style='display:block;text-align:center;color:#03582d;font-weight:700;text-decoration:underline;padding-top:2px;'>Ingresar al portal del equipo (Browix) ↗</a>",
            "</div>",
            "<button type='button' id='su-wa-toggle-compras' style='width:100%;text-align:center;background:#ffffff;color:#374151;font-weight:700;font-size:12.5px;padding:11px 16px;border-radius:10px;border:1px solid #e5e7eb;cursor:pointer;font-family:\"Open Sans\",sans-serif;'>📦 Soy proveedor de insumos o servicios</button>",
            "<div id='su-wa-compras-panel' style='display:none;background:#f9fafb;border:1px solid #d1d5db;border-radius:10px;padding:12px;font-size:12px;color:#374151;'>",
              "<p style='margin:0 0 8px 0;line-height:1.4;'><strong>Recepción de propuestas de proveedores:</strong> Copiá la casilla de Compras y envianos tu presentación o catálogo por correo:</p>",
              "<div style='display:flex;align-items:center;justify-content:space-between;gap:8px;background:#ffffff;border:1px solid #d1d5db;border-radius:8px;padding:8px 10px;'>",
                "<span style='font-weight:800;color:#000000;font-size:12.5px;user-select:all;'>" + EMAIL_COMPRAS + "</span>",
                "<button type='button' id='su-copy-compras-btn' style='background:#03582d;border:none;border-radius:6px;padding:6px 10px;font-size:11px;font-weight:700;cursor:pointer;color:#ffffff;'>Copiar correo</button>",
              "</div>",
            "</div>",
          "</div>",
        "</div>"
      ].join('');
      document.body.appendChild(modal);

      document.getElementById('su-wa-close').addEventListener('click', function () {
        modal.style.display = 'none';
      });
      modal.addEventListener('click', function (e) {
        if (e.target === modal) modal.style.display = 'none';
      });

      document.getElementById('su-wa-go-b2b').addEventListener('click', function () {
        if (typeof window.gtag === 'function') {
          window.gtag('event', 'contacto_wa_empresa_b2b', { event_category: 'B2B_Lead' });
        }
        modal.style.display = 'none';
      });

      document.getElementById('su-wa-toggle-rrhh').addEventListener('click', function () {
        var rrhhP = document.getElementById('su-wa-rrhh-panel');
        var compP = document.getElementById('su-wa-compras-panel');
        compP.style.display = 'none';
        rrhhP.style.display = rrhhP.style.display === 'none' ? 'block' : 'none';
      });

      document.getElementById('su-wa-toggle-compras').addEventListener('click', function () {
        var rrhhP = document.getElementById('su-wa-rrhh-panel');
        var compP = document.getElementById('su-wa-compras-panel');
        rrhhP.style.display = 'none';
        compP.style.display = compP.style.display === 'none' ? 'block' : 'none';
      });

      document.getElementById('su-copy-rrhh-btn').addEventListener('click', function () {
        copyPlainText(EMAIL_RRHH, this, '✓ Copiado');
      });

      document.getElementById('su-copy-compras-btn').addEventListener('click', function () {
        copyPlainText(EMAIL_COMPRAS, this, '✓ Copiado');
      });
    }

    waLinks.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        var targetHref = link.getAttribute('href');
        var b2bBtn = document.getElementById('su-wa-go-b2b');
        b2bBtn.setAttribute('href', targetHref);
        document.getElementById('su-wa-rrhh-panel').style.display = 'none';
        document.getElementById('su-wa-compras-panel').style.display = 'none';
        modal.style.display = 'flex';
      });
    });
  });
})();
