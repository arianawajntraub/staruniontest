# Informe de Auditoría y Encuesta Tipográfica: Unificación del Sistema Tipográfico (Star Union S.R.L.)

**Fecha:** 2026-10-28T14:24:00Z  
**Autor:** Explorer Agente Especializado en Relevamiento Tipográfico  
**Destinatario:** Orquestador Padre (`e86356a5-39e5-4a9e-ba35-f025439cb0eb`)  
**Directorio de Trabajo:** `/Users/arianawajntraub/Documents/antigravity/star-union/.agents/teamwork/explorer_survey_typography`  
**Alcance del Relevamiento:** 10 Páginas Públicas + Dossier Interactivo (`/dossier/`) + Snippets y Configuración Global.

---

## 1. Observation (Observaciones Directas)

Se realizó un escaneo exhaustivo línea por línea sobre el bloque `<head>`, configuraciones de Tailwind CSS, reglas `<style>` y jerarquía de encabezados (`<h1>`, `<h2>`, `<h3>`, `<h4>`, párrafos) en los 11 archivos HTML objetivo y recursos compartidos:

### 1.1 Inventario de Fuentes Declaradas en `<head>` y Conexiones Externas

| Archivo | Preconnects (`googleapis` / `gstatic`) | Enlace Google Fonts (`family=...`) | Familias Importadas | Pesos Declarados |
| :--- | :---: | :--- | :--- | :--- |
| `index.html` (L. 10-12) | **NO** | `family=Open+Sans:ital,wght@0,300..800;1,300..800` | `Open Sans` | 300 a 800 (normal e itálica) |
| `la-empresa/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300;400;500;600;700;800` | `Inter` | 300, 400, 500, 600, 700, 800 |
| `certificacion-iso/index.html` (L. 8-10) | **NO** | `family=Open+Sans:ital,wght@0,300..800;1,300..800` | `Open Sans` | 300 a 800 (normal e itálica) |
| `limpieza-industrial/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600..800` | `Inter` + `Plus Jakarta Sans` | Inter (300..700), PJS (600..800) |
| `limpieza-en-altura/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300;400;500;600;700;800` | `Inter` | 300, 400, 500, 600, 700, 800 |
| `grandes-superficies/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600..800` | `Inter` + `Plus Jakarta Sans` | Inter (300..700), PJS (600..800) |
| `consorcios/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600..800` | `Inter` + `Plus Jakarta Sans` | Inter (300..700), PJS (600..800) |
| `clinicas-y-hospitales/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600..800` | `Inter` + `Plus Jakarta Sans` | Inter (300..700), PJS (600..800) |
| `universidades-y-clubes/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600..800` | `Inter` + `Plus Jakarta Sans` | Inter (300..700), PJS (600..800) |
| `servicios-especiales/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600..800` | `Inter` + `Plus Jakarta Sans` | Inter (300..700), PJS (600..800) |
| `dossier/index.html` (L. 10-12) | **SÍ** | `family=Inter:wght@300;400;500;600;700;800` | `Inter` | 300, 400, 500, 600, 700, 800 |

### 1.2 Configuración de Tailwind (`tailwind.config`) y Estilos Locales (`<style>`)

1. **`index.html`**:
   - Tailwind (L. 48-49): `fontFamily: { sans: ['"Open Sans"', 'sans-serif'], heading: ['"Open Sans"', 'sans-serif'] }`
   - Estilo en `<style>` (L. 60): `body { font-size: 1.125rem; color: #676b67; background-color: #ffffff; }`
   - Clases en `<body>` (L. 69): `class="bg-white antialiased selection:bg-brand selection:text-white"`
2. **`certificacion-iso/index.html`**:
   - Tailwind (L. 41): `fontFamily: { sans: ['"Open Sans"', 'sans-serif'] }` (no define `heading`).
   - Estilo en `<style>` (L. 51): `body { font-size: 1.125rem; color: #676b67; }`
   - Clases en `<body>` (L. 53): `class="bg-gray-50 antialiased selection:bg-brand selection:text-white"` (Fondo gris en lugar de blanco puro).
3. **`la-empresa/index.html`**:
   - Tailwind (L. 17): `fontFamily: { sans: ['Inter', 'sans-serif'] }`
   - Estilo en `<style>` (L. 28-29):  
     `body { font-family: 'Inter', sans-serif; color: #676b67; background-color: #ffffff; }`  
     `h1, h2, h3, h4, .font-heading { color: #000000; }`
   - Tamaño base: No definido en CSS (toma el valor por defecto del navegador: `1rem` = `16px`).
4. **`limpieza-en-altura/index.html`**:
   - Tailwind (L. 40): `fontFamily: { sans: ['Inter', 'sans-serif'] }`
   - Estilo en `<style>` (L. 51-52):  
     `body { font-family: 'Inter', sans-serif; color: #676b67; background-color: #ffffff; }`  
     `h1, h2, h3, h4, .font-heading { color: #000000; }`
   - Tamaño base: `1rem` = `16px`.
5. **6 Páginas de Verticales (`limpieza-industrial`, `grandes-superficies`, `consorcios`, `clinicas-y-hospitales`, `universidades-y-clubes`, `servicios-especiales`)**:
   - Tailwind (L. 17-20):  
     ```javascript
     fontFamily: {
         sans: ['"Inter"', 'sans-serif'],
         display: ['"Plus Jakarta Sans"', 'sans-serif'],
     }
     ```
   - Estilo en `<style>` (L. 31-32):  
     ```css
     body { font-family: 'Inter', sans-serif; color: #676b67; background-color: #ffffff; }
     h1, h2, h3, h4 { font-family: 'Plus Jakarta Sans', sans-serif; color: #000000; }
     ```
   - Tamaño base: No definido en CSS (`1rem` = `16px`).
6. **`dossier/index.html`**:
   - Tailwind (L. 17): `fontFamily: { sans: ['Inter', 'sans-serif'] }`
   - Estilo en `<style>` (L. 28-29):  
     `body { font-family: 'Inter', sans-serif; color: #676b67; background-color: #f9fafb; }`  
     `h1, h2, h3, h4 { color: #000000; }`
   - Tamaño base: `1rem` = `16px`.

### 1.3 Recursos Compartidos y Snippets
- Directorio `assets/css/`: Vacío (sin archivos `.css` globales).
- No existe archivo `tailwind.config.js` externo; la configuración de Tailwind se inyecta directamente vía `<script src="https://cdn.tailwindcss.com"></script>` y objeto inline `tailwind.config = { ... }` en el `<head>` de cada archivo.
- Archivos de snippet `header.html` y `footer.html`: Contienen el marcado unificado de navegación y pie corporativo con clases utilitarias (`text-xs`, `text-sm`, `font-bold`, `font-extrabold`), pero sin declaración propia de familias tipográficas.

---

## 2. Logic Chain (Cadena de Razonamiento)

1. **Evidencia de Fragmentación Trilateral:**
   - La observación 1.1 demuestra que coexisten 3 ecosistemas tipográficos incompatibles:
     a) **Grupo A (Open Sans):** `index.html` y `certificacion-iso/index.html`.
     b) **Grupo B (Inter + Plus Jakarta Sans):** 6 páginas verticales (`limpieza-industrial`, `grandes-superficies`, `consorcios`, `clinicas-y-hospitales`, `universidades-y-clubes`, `servicios-especiales`).
     c) **Grupo C (Inter únicamente):** `la-empresa/index.html`, `limpieza-en-altura/index.html` y `dossier/index.html`.
2. **Impacto en la Experiencia de Usuario y Percepción de Marca:**
   - Al hacer clic desde la Home (`index.html`, en Open Sans con cuerpo a 18px) hacia cualquier vertical (ej. `limpieza-industrial/index.html`, con títulos en Plus Jakarta Sans y cuerpo en Inter a 16px), el usuario experimenta:
     - Un salto abrupto de tamaño de fuente (reducción del 12.5% en textos no acotados).
     - Un choque visual de anatomía tipográfica: Open Sans posee una altura de x generosa, aperturas amplias y estilo humanista; Plus Jakarta Sans es estrictamente geométrico con remates mecánicos circulares; e Inter es un neo-grotesco suizo neutro y compacto.
     - Sensación de estar navegando dos sitios web distintos construidos en épocas o por proveedores diferentes, lo cual atenta directamente contra el requerimiento R1 de `ORIGINAL_REQUEST.md`.
3. **Penalización de Performance y Carga de Recursos:**
   - En las páginas de los grupos B y C se descargan archivos de fuentes dobles (`Inter` + `Plus Jakarta Sans`) que no aportan valor de marca.
   - Paradójicamente, las únicas dos páginas que sí usan la fuente oficial de Star Union (`index.html` y `certificacion-iso/index.html`) **carecen de las etiquetas `<link rel="preconnect">`**, lo que retrasa la resolución DNS y el handshake TLS con los servidores de Google Fonts, provocando FOUT (Flash of Unstyled Text) o FOIT (Flash of Invisible Text).
4. **Anomalía del Tamaño Base de Cuerpo (18px vs 16px):**
   - El requerimiento R1 de `ORIGINAL_REQUEST.md` exige explícitamente:  
     *"ajustar pesos, interlineados, jerarquías de títulos... y cuerpo de texto (1rem / 16px limpio y proporcionado) para que navegar entre la Home y cualquier vertical se sienta un único sitio corporativo de primer nivel"*.
   - El `body { font-size: 1.125rem; }` presente en `index.html` (L. 60) y `certificacion-iso/index.html` (L. 51) es el causante directo de la desproporción respecto de las otras 9 páginas. Al unificar la base en `1rem` (16px) y `line-height: 1.6`, se restablece la armonía con los componentes de interfaz, tablas y formularios.
5. **Inconsistencias en Jerarquía de Encabezados (H1, H2, H3, H4):**
   - **H1 (Hero):** Varía de 68px (`index.html`) a 60px (`certificacion-iso`), 48px (`la-empresa` y `altura`), 42px (las 6 verticales) y 36px (`dossier`).
   - **H2 (Secciones):** En Home conviven `text-4xl` y `text-5xl`, en ISO `text-3xl`, `text-4xl` y `text-5xl`, y en verticales `text-2xl sm:text-3xl` y `text-3xl`.
   - **H3 (Tarjetas):** En Home las tarjetas de verticales usan `text-2xl font-bold text-[#024121]`, mientras que en las páginas de verticales las tarjetas de alcance usan `text-lg font-extrabold text-[#000000]`.
   - La estandarización debe fijar una escala matemática consistente y proporcional para cada nivel en todo el ecosistema.

---

## 3. Caveats (Advertencias y Supuestos)

1. **Páginas Internas Fuera del Catálogo Público Directo:**
   - Se auditaron adicionalmente `accesos/index.html`, `brochures/index.html`, `brochures/editables/*.html`, `radar-comercial/index.html`, `acuerdos/index.html` y `relevamiento-gerencia/index.html`.
   - `accesos/index.html` es el Linktree central interno (bloqueado con `robots: noindex`).
   - Los brochures editables (`brochures/editables/*.html`) son plantillas de impresión CSS A4 para generar PDFs. Si bien también usan `Inter` y `Plus Jakarta Sans`, la unificación obligatoria del requerimiento R1 rige sobre las **10 páginas públicas + dossier/index.html**.
2. **Dependencia de Tailwind CDN:**
   - Dado que el sitio no corre un bundler local (como Vite, Webpack o PostCSS CLI) sino Tailwind CDN vía script (`cdn.tailwindcss.com`), la modificación de `tailwind.config` y `<style>` debe aplicarse de manera precisa y consistente en cada uno de los 11 archivos HTML.
3. **Ajuste de Párrafos en la Home (`index.html`):**
   - Al cambiar `body { font-size: 1.125rem; }` a `1rem` en `index.html`, los párrafos que dependían de la herencia del body pasarán a medir 16px. Aquellos párrafos que requieran destacarse como lead/bajada editorial mantendrán explícitamente `text-lg` (18px) o `text-xl` (20px), manteniendo la legibilidad sin alterar el diseño de tarjetas y grillas.

---

## 4. Conclusion (Plan de Unificación Recomendado para Open Sans)

Se recomienda implementar el siguiente plan de unificación tipográfica integral de 4 pasos en las 10 páginas públicas y el dossier:

### Paso 1: Bloque Universal en `<head>` con Preconnect y Open Sans
Reemplazar en los 11 archivos HTML los links a Google Fonts por el siguiente bloque limpio y optimizado:
```html
<!-- TIPOGRAFÍA OFICIAL STAR UNION: OPEN SANS -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
```

### Paso 2: Unificación del Objeto `tailwind.config`
Estandarizar en los 11 archivos HTML el bloque de fuentes de Tailwind:
```javascript
tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Open Sans"', 'sans-serif'],
                heading: ['"Open Sans"', 'sans-serif'],
                display: ['"Open Sans"', 'sans-serif'] // Alias retrocompatible para evitar roturas
            },
            colors: {
                brand: { DEFAULT: '#03582d', dark: '#024121', light: '#047a3e' },
                accent: { DEFAULT: '#ffcc29', hover: '#e5b622' },
                neutral: { custom: '#676b67', dark: '#111827', light: '#ffffff' }
            }
        }
    }
}
```

### Paso 3: Regla Maestra en `<style>` (Base 1rem / 16px)
Reemplazar en los 11 archivos el bloque `<style>` para fijar el estándar editorial:
```css
body {
    font-family: 'Open Sans', sans-serif;
    font-size: 1rem; /* 16px base uniforme */
    line-height: 1.6;
    color: #676b67;
    background-color: #ffffff;
}
h1, h2, h3, h4, .font-heading, .font-display {
    font-family: 'Open Sans', sans-serif;
    color: #000000;
}
```
*(En `certificacion-iso/index.html` alinear la clase del `<body>` a `bg-white` para eliminar el salto con `bg-gray-50`).*

### Paso 4: Escala Tipográfica Editorial Estandarizada

| Nivel | Rol en la Página | Clases Tailwind Recomendadas | Tamaño Visual | Peso | Leading | Tracking |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **H1 (Home Hero)** | Título principal de la portada | `text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.1] text-white` | 36 / 48 / 60px | 800 | 1.10 | `-0.025em` |
| **H1 (Páginas Interiores)** | Título hero de vertical / sede / dossier | `text-3xl sm:text-4xl lg:text-[42px] font-extrabold text-[#000000] tracking-tight leading-[1.14]` | 30 / 36 / 42px | 800 | 1.14 | `-0.025em` |
| **H2 (Secciones Principales)** | Título de módulo (Alcance, Diferenciales) | `text-2xl sm:text-3xl font-extrabold text-[#000000] tracking-tight leading-tight` | 24 / 30px | 800 | 1.25 | `-0.025em` |
| **H2 (Sección CTA Final)** | Bloque de cierre y llamada a la acción | `text-3xl sm:text-4xl font-extrabold text-[#000000] leading-tight` | 30 / 36px | 800 | 1.25 | normal |
| **H3 (Tarjetas y Protocolos)** | Tarjetas de 6 protocolos, cajas de servicios | `text-lg sm:text-xl font-bold text-[#000000] leading-snug` | 18 / 20px | 700 | 1.35 | normal |
| **H4 / Subtítulos** | Columnas de pie, micro-títulos de formulario | `text-xs sm:text-sm font-bold uppercase tracking-wider text-[#000000]` | 12 / 14px | 700 | 1.40 | `0.05em` |
| **Bajada / Lead (`p.lead`)** | Resumen destacado de hero | `text-base sm:text-lg text-[#676b67] leading-relaxed font-normal` | 16 / 18px | 400 | 1.625 | normal |
| **Cuerpo Estándar (`p`)** | Texto corriente de párrafos y tarjetas | `text-sm sm:text-base text-[#676b67] leading-relaxed font-normal` | 14 / 16px | 400 | 1.60 | normal |
| **Microcopy / Badges** | Etiquetas superiores, migas de pan, metadatos | `text-xs font-semibold uppercase tracking-wider` | 12px | 600 | 1.40 | `0.05em` |

---

## 5. Verification Method (Método de Verificación Independiente)

Para verificar de forma programática y reproducible que el plan resuelve el 100% de las inconsistencias detectadas:

### 5.1 Comandos de Inspección Automatizada
1. **Comprobar la eliminación total de `Inter` y `Plus Jakarta Sans` en las páginas públicas y dossier:**
   ```bash
   grep -En "family=(Inter|Plus\+Jakarta\+Sans)" \
     index.html \
     la-empresa/index.html \
     certificacion-iso/index.html \
     limpieza-industrial/index.html \
     limpieza-en-altura/index.html \
     grandes-superficies/index.html \
     consorcios/index.html \
     clinicas-y-hospitales/index.html \
     universidades-y-clubes/index.html \
     servicios-especiales/index.html \
     dossier/index.html
   ```
   *Criterio de éxito:* 0 resultados.

2. **Comprobar la presencia uniforme de Open Sans y preconnects en las 11 páginas:**
   ```bash
   grep -En "family=Open\+Sans" \
     index.html \
     la-empresa/index.html \
     certificacion-iso/index.html \
     limpieza-industrial/index.html \
     limpieza-en-altura/index.html \
     grandes-superficies/index.html \
     consorcios/index.html \
     clinicas-y-hospitales/index.html \
     universidades-y-clubes/index.html \
     servicios-especiales/index.html \
     dossier/index.html
   ```
   *Criterio de éxito:* Exactamente 1 coincidencia por archivo (11 coincidencias en total).

3. **Comprobar la erradicación de `body { font-size: 1.125rem`:**
   ```bash
   grep -En "font-size:\s*1\.125rem" \
     index.html \
     la-empresa/index.html \
     certificacion-iso/index.html \
     limpieza-industrial/index.html \
     limpieza-en-altura/index.html \
     grandes-superficies/index.html \
     consorcios/index.html \
     clinicas-y-hospitales/index.html \
     universidades-y-clubes/index.html \
     servicios-especiales/index.html \
     dossier/index.html
   ```
   *Criterio de éxito:* 0 resultados.

4. **Comprobar la consistencia del color de fondo en `<body>`:**
   ```bash
   grep -En '<body class="[^"]*bg-gray-50' certificacion-iso/index.html
   ```
   *Criterio de éxito:* 0 resultados tras la unificación con `bg-white`.

### 5.2 Condiciones de Invalidación
- Si alguna página interior mantiene declaraciones de `font-family: 'Plus Jakarta Sans'` o `font-family: 'Inter'`, la unificación tipográfica queda invalidada.
- Si la Home mantiene `1.125rem` en el body, persistirá el salto de escala de texto entre páginas.
