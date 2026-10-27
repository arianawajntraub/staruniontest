# Auditoría con Datos Reales de Google Analytics 4 (`356146296`) y Google Ads (`4477242318`) — Star Union S.R.L.

> **Fecha de extracción por API:** 26 de Octubre de 2026
> **Propiedad GA4:** `properties/356146296` (`Star Union - GA4` | Measurement ID: `G-YDDJQHK8VC`)
> **Cuenta de Google Ads vinculada:** `4477242318` (Vinculada por `marielg@gmail.com`)
> **Plataforma de Mailing:** `perfit / email`

---

## 1. Confirmación de tu Intuición: Google Ads cayó un -90% en 5 meses

Tu percepción de que *"Ads está en caída"* es **100% exacta**. Mirá la serie histórica mensual extraída directamente de GA4 (`Paid Search` = `google / cpc`):

| Mes (2026) | Sesiones Pagas (`Google Ads`) | Sesiones con Interacción | Eventos Clave (`contacto_wa` + `contacto_web`) | Variación vs. Pico de Mayo |
| :--- | :---: | :---: | :---: | :---: |
| **Mayo 2026** | **2.040** | 1.451 | 377 | Base pico |
| **Junio 2026** | **892** | 622 | 207 | -56,3% |
| **Julio 2026** | **356** | 257 | 72 | -82,5% |
| **Agosto 2026** | **263** | 195 | 46 | -87,1% |
| **Septiembre 2026** | **254** | 180 | 49 | -87,5% |
| **Octubre 2026 (al día 26)** | **205** | 159 | 48 | **-90,0%** |

---

## 2. ¿En qué está gastando Mariel el presupuesto de Google Ads hoy? (Últimos 90 días)

De las **737 sesiones** que trajo Google Ads en los últimos 90 días, el **85% del tráfico se fue en solo dos cosas que NO traen clientes B2B nuevos**:

| Campaña en Google Ads | Grupo de Anuncios (`Ad Group`) | Sesiones (90 días) | % del Tráfico de Ads | Eventos Clave | Diagnóstico Técnico Real |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`Search-Marca`** | `Star union` | **328** | **44,5%** | 56 | **Gasto redundante y contaminado de CVs:** Se está pagando casi la mitad del tráfico de Ads por gente que escribe `"star union"`, `"starunion"` o `"star union direccion"` (gente que ya busca a la empresa, postulantes de trabajo o empleados). |
| **`Star Union - Red de Búsqueda`** | `Empresa de Limpieza` | **255** | **34,6%** | 51 | **Bolsa genérica sin filtro B2B:** Usa palabras amplias (`"agencia de limpieza"`, `"empresa de limpieza"`, `"higiene profesional"`) que están colando búsquedas domésticas, eventos y competidores chicos. |
| **`Dynamic Search`** | `Dynamic` | **34** | **4,6%** | 5 | Anuncios dinámicos automáticos sin control de vertical. |
| **`Star Union - Red de Búsqueda`** | `Final de Obra` | **30** | **4,1%** | **11** | **¡36,6% de conversión!** Funciona muy bien pero recibe apenas 1 clic cada 3 días. |
| **`Star Union - Red de Búsqueda`** | `Oficinas` | **22** | **3,0%** | **7** | Muy buen interés (31,8% de conversión), pero casi sin presupuesto (1 clic cada 4 días). |
| **`Star Union - Red de Búsqueda`** | `Consorcios` | **4** | **0,5%** | 2 | Testimonial (4 clics en 3 meses). |
| **`Star Union - Red de Búsqueda`** | **`Fabricas y Limpieza Industrial`** | **2** | **0,3%** | **0** | **¡2 clics en 90 días para la vertical más rentable de la empresa!** |
| **`Star Union - Red de Búsqueda`** | **`Industria alimenticia`** | **2** | **0,3%** | **0** | **2 clics en 90 días.** |
| **`Star Union - Red de Búsqueda`** | **`Universidades y Colegios`** | **2** | **0,3%** | **0** | **2 clics en 90 días.** |
| **`Star Union - Red de Búsqueda Trelew`** | `Grupo dinámico` | **1** | **0,1%** | **0** | **1 clic en 90 días.** |
| **Clínicas / Hospitales / Vidrios en Altura / Bahía Blanca / Neuquén** | *(No existen activos)* | **0** | **0,0%** | **0** | **0 clics.** |

---

## 3. Términos de Búsqueda Reales (`Query`) que se colaron en Google Ads (Pruebas en GA4)

En el grupo `Empresa de Limpieza` (palabras clave `agencia de limpieza`, `empresa de limpieza`, `higiene profesional`), Google Ads cobró clics por personas que buscaron:
- ❌ `"zolvers argentina"` (plataforma de empleadas domésticas por hora).
- ❌ `"empresa de limpieza domiciliaria"` (casas particulares — viola la regla número 1 de Star Union).
- ❌ `"limpieza de colchones caba"`, `"limpieza de campanas caba"`, `"limpieza integral de cocina"`.
- ❌ `"servicio de limpieza para eventos"`, `"empresa de limpieza para eventos"`.
- ❌ `"alumbrado barrido y limpieza provincia de buenos aires"` (gente buscando pagar la boleta municipal de ABL).
- ❌ `"productos de limpieza para empresas"`, `"productos de limpieza para industria alimentaria"`, `"valot"`, `"prohygiene argentina"` (gente buscando comprar papel higiénico o bidones de lavandina, no contratar servicio de personal).
- ❌ `"empresas de limpieza en jujuy"`, `"limpar rosario"` (zonas donde Star Union no opera).
- ❌ Nombres de decenas de empresas/agencias donde la gente busca mandar CV: `"el cacique limpieza srl"`, `"c planet limpieza"`, `"lukas empresa de limpieza"`, `"brillamil limpieza"`, `"rens limpieza"`, `"pertenecer empresa de limpieza"`, `"los soles empresa de limpieza"`.

---

## 4. El Problema Crítico de Medición: Los Postulantes de Empleo están inflando las conversiones de WhatsApp

Mirá en qué páginas del sitio viejo se dispararon los eventos en los últimos 90 días:
- **`/interesados.php` (Página de Postulantes Laborales / CVs):**
  - Tuvo **`890` envíos de formulario (`form_submit`)** de personas buscando trabajo.
  - Y además disparó **`94` conversiones `contacto_wa` (`KeyEvents`)** porque el botón de WhatsApp está visible para postulantes.
- **`/` (Home):**
  - Disparó **`837` conversiones `contacto_wa`**, la enorme mayoría provenientes de búsquedas de marca (`"star union"`) de postulantes o empleados que tocan el botón de WhatsApp en vez de ir a RRHH.
- **Consecuencia en Google Ads:** Como `contacto_wa` está importada como conversión principal en Google Ads, cada vez que un postulante busca `"star union"` en la campaña `Search-Marca` y toca WhatsApp, **Google Ads registra una conversión exitosa y gasta todo el presupuesto en `Search-Marca` y en `agencia de limpieza`**, dejando con **2 clics en 90 días** a `Fabricas y Limpieza Industrial`.

---

## 5. Tus Campañas de Mailing en Perfit (`perfit / email`) y los Motores de IA (`chatgpt.com`)

### A. Perfit (`505` sesiones de empresas en 90 días $\rightarrow$ `0` conversiones en la web vieja)
- `julio 26` + reenvío: **208 sesiones**
- `agosto 26`: **45 sesiones**
- `Septiembre 26` + reenvío: **157 sesiones**
- `Octubre 26`: **94 sesiones**
- **Diagnóstico:** Tus envíos y reenvíos a los 5 días en Perfit **sí hacen que las empresas entren a la web (`505` visitas B2B puras)**, pero en la web vieja (`0` conversiones) miran y se van sin dejar formulario. Por eso el **Radar Comercial de los Clics de Mailing (`radar-comercial/index.html`)** que te armamos es clave: toma esos clics de Perfit y obliga a accionarlos 1-a-1 por dominio con el gancho Post-Paritarias o Vidrios en Altura.

### B. Motores de IA (`chatgpt.com`, `gemini.google.com`, `perplexity.ai`)
- En los últimos 90 días ya entraron **89 sesiones desde asistentes de IA** (creciendo de 12 en junio a 40 en septiembre) y generaron **13 contactos directos por WhatsApp (`14,6%` de conversión)**.
- Subiendo hoy el archivo `llms.txt` que ya te dejé listo, este canal B2B gratuito va a crecer mucho más rápido.

---

## 6. Qué pedirle a Mariel (con estos números en la mano)

1. **Bajar al mínimo o pausar `Search-Marca` (que hoy se lleva el 44,5% de los clics pagos):** Quien busca `"star union"` ya entra por el resultado orgánico #1; pagar por `"star union"` solo financia clics de postulantes de empleo y empleados.
2. **Negativizar de inmediato en toda la cuenta:** `domiciliaria`, `particular`, `casas`, `hogar`, `por hora`, `zolvers`, `colchones`, `sillones`, `campanas`, `eventos`, `productos`, `insumos`, `abl`, `trabajo`, `empleo`, `cv`, `curriculum`, `postularse`, `rrhh`, `rosario`, `jujuy`, `cordoba`, `mendoza`.
3. **Pasar el presupuesto de `Search-Marca` y `agencia de limpieza` a los 4 Grupos B2B de Alto Ticket en Concordancia de Frase/Exacta:**
   - **Grupo 1 — Industrial / Fábricas / Logística** (que hoy tuvo solo 2 clics en 90 días): `"empresa de limpieza industrial"`, `"limpieza de plantas industriales"`, `"limpieza de fabricas"`, `"limpieza de depositos y centros logisticos"`.
   - **Grupo 2 — Edificios de Oficinas y Corporativos** (que hoy tuvo solo 22 clics en 90 días): `"empresa de limpieza para oficinas"`, `"servicio de limpieza corporativa"`, `"limpieza de edificios corporativos"`.
   - **Grupo 3 — Puerta de Entrada Rápida (Vidrios en Altura + Final de Obra):** `"limpieza de vidrios en altura empresas"`, `"limpieza de fachadas vidriadas"`, `"empresa de limpieza final de obra"` (este último ya convierte al **36,6%**).
   - **Grupo 4 — Clínicas, Sanatorios, Universidades y Colegios:** `"empresa de limpieza hospitalaria"`, `"limpieza para clinicas y sanatorios"`, `"empresa de limpieza para universidades y colegios"`.
