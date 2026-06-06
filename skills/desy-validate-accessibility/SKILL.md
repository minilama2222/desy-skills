---
name: desy-validate-accessibility
description: "Validate WCAG 2.2 AA accessibility of DESY components and pages. Use before merging UI, auditing, or reviewing accessibility. Combines automated + manual tests."
---

# desy-validate-accessibility

Valida la accesibilidad WCAG 2.2 AA de componentes o páginas implementadas con DESY. Combina herramientas automáticas con tests manuales (teclado, lector de pantalla, contraste).

## When to use this skill

- Antes de mergear cualquier PR con UI nueva
- Al auditar código existente
- Después de implementar un componente con `desy-implement-component`
- Antes de pasar el proyecto a revisión de accesibilidad oficial (obligatoria por RD 1112/2018)
- Cuando se modifica un componente existente y se quiere verificar que sigue siendo accesible

## Prerequisitos

Antes de aplicar este skill, asegúrate de tener:

- El proyecto DESY corriendo localmente (`npm run dev` o `ionic serve`)
- Node y npm disponibles
- Opcional pero recomendado: navegador Chrome o Firefox con extensiones instaladas
- Opcional: lector de pantalla (NVDA en Windows, VoiceOver en macOS, Orca en Linux)

## Workflow

### Paso 1: Automated scan con axe-core

**Setup del proyecto** (one-time):

```bash
# Instalar axe-core CLI globalmente (o como devDep)
npm install --save-dev @axe-core/cli
# o instalar Pa11y como alternativa
npm install --save-dev pa11y
```

**Scan contra la página en dev:**

```bash
# Opción 1: axe-core CLI
npx axe http://localhost:4200/ --exit  # desy-angular
# o
npx axe http://localhost:5173/ --exit  # desy-html
# o
npx axe http://localhost:8100/ --exit  # desy-ionic

# Opción 2: Pa11y
npx pa11y http://localhost:4200/ --standard WCAG2AA
```

El scan detecta:
- Contraste de color insuficiente
- Labels ausentes o mal asociados
- Roles ARIA incorrectos
- Foco no visible
- Estructura de headings rota (saltos de h1 a h3)
- Imágenes sin alt
- Botones sin texto accesible
- Formularios sin labels

**Si el scan reporta errores:** corregir antes de seguir con los tests manuales.

### Paso 2: Test de navegación por teclado

Manual, ~10 minutos. Recorre la página solo con teclado:

| Acción | Esperado |
|---|---|
| **Tab** desde el principio | El foco va al primer elemento focuseable |
| **Skip-link visible al primer Tab** | Hay un enlace "Saltar al contenido" que al activarse salta a `<main>` |
| **Foco visible** | El elemento enfocado tiene outline visible (no `outline: none` sin alternativa) |
| **Tab secuencial** | Recorre todos los elementos interactivos en orden lógico |
| **Shift+Tab** | Va hacia atrás correctamente |
| **Enter / Space en botón** | Activa el botón |
| **Esc en modal** | Cierra el modal y devuelve el foco al botón que lo abrió |
| **Flechas en select** | Cambia la opción seleccionada |
| **Flechas en tabs** | Cambia entre tabs (W3C APG) |
| **Flechas en tablas** (role=grid) | Navega entre celdas |
| **Foco al error-summary** | Al submit de formulario con errores, el foco va al título del resumen |

**Si algo falla:** corregir el orden de focus, añadir skip-link, restaurar outline, etc.

### Paso 3: Test con lector de pantalla

Manual, ~15 minutos. Activa NVDA / VoiceOver / Orca y recorre la página:

| Acción | Esperado |
|---|---|
| Lectura de la cabecera | "Banner, navegación principal, lista de X items" |
| Lectura del skip-link | "Saltar al contenido principal, enlace" |
| Activación del skip-link | Salta a `<main>` |
| Lectura del menú de navegación | "Menú de navegación, lista de X items" |
| Lectura de un botón con icono + texto | Lee SOLO el texto (icono es `aria-hidden=true`) |
| Lectura de un botón solo con icono | Lee el `aria-label` (ej: "Eliminar, botón") |
| Lectura de un input | Lee el label + el tipo (ej: "Nombre, edición, requerido") |
| Lectura de un input con error | "Nombre, edición, requerido, error: el campo es obligatorio" |
| Lectura de un formulario completo | "Formulario de contacto" (por `aria-label` o `aria-labelledby`) |
| Lectura de una tabla | "Tabla, 3 filas, 4 columnas. Encabezado: Mes, Pago 1, Pago 2" |
| Lectura de un modal al abrirse | "Diálogo modal, ¿Eliminar expediente?, título" |
| Lectura de un link que abre nueva ventana | Anuncia "enlace Se abre en ventana nueva" (por `title`) |
| Navegación por landmarks (D / L en NVDA) | Recorre `<header>`, `<nav>`, `<main>`, `<footer>` |

**Si algo falla:** corregir `aria-label`s, roles, descripciones, etc.

### Paso 4: Test de contraste y color

Manual + herramientas:

```bash
# Opción 1: Colour Contrast Analyser (aplicación nativa)
# Descargar de https://www.tpgi.com/color-contrast-checker/

# Opción 2: WebAIM contrast checker online
# https://webaim.org/resources/contrastchecker/

# Opción 3: extensión del navegador
# Chrome: Accessibility Insights
# Firefox: WCAG Contrast checker
```

**Reglas WCAG 2.2 AA:**

| Elemento | Ratio mínimo |
|---|---|
| Texto normal (≥18px o ≥14px bold) | 4.5:1 |
| Texto grande (≥18px bold o ≥24px) | 3:1 |
| Iconos UI (funcionales, no decorativos) | 3:1 |
| Boundaries de inputs | 3:1 |

**Comprobar:**
- Texto sobre fondo blanco
- Texto sobre colores `light` (mensajes de estado)
- Texto sobre colores `base` (botones, solo permitido si semibold ≥16px)
- Borders de inputs (1px) sobre fondo

### Paso 5: Test responsive (mobile + desktop)

Manual:

```bash
# Abrir DevTools (F12) → toggle device toolbar (Ctrl+Shift+M)
# Probar en:
# - iPhone SE (375x667)
# - iPhone 14 (390x844)
# - iPad (768x1024)
# - Desktop (1280x800)
# - Desktop wide (1920x1080)
```

**Verificar:**
- Cabecera colapsa correctamente (menú hamburguesa en móvil)
- Tablas hacen scroll horizontal (no se rompen)
- Inputs no pierden foco al abrir teclado virtual
- Foco visible sigue siendo visible en pantallas táctiles

### Paso 6: Generar el reporte

Tras todos los tests, compila un reporte de accesibilidad:

```markdown
# Reporte de accesibilidad — [componente/página]

**Fecha:** YYYY-MM-DD
**Versión:** commit-hash
**Librería:** desy-html / desy-angular / desy-ionic
**Versión DESY:** X.Y.Z
**Tester:** [tu nombre]

## Automated scan (axe-core)
- [x] Sin errores
- [ ] X errores: [listar]

## Navegación por teclado
- [x] Tab secuencial OK
- [x] Skip-link presente y funcional
- [x] Foco visible en todos los elementos
- [x] Esc cierra modales
- [ ] X falla: [detalle]

## Lector de pantalla (NVDA / VoiceOver)
- [x] Landmarks correctos
- [x] Botones anuncian su acción
- [x] Inputs con label + estado
- [x] Formularios con descripción
- [x] Tablas legibles
- [x] Modales anunciados al abrir
- [ ] X falla: [detalle]

## Contraste y color
- [x] Texto principal: 4.5:1+
- [x] Texto sobre base: 16px+ semibold
- [x] Borders inputs: 3:1+
- [ ] X falla: [detalle]

## Responsive
- [x] Móvil (375px)
- [x] Tablet (768px)
- [x] Desktop (1280px)
- [x] Anchuras pequeñas: scroll horizontal en tablas
- [x] Menú hamburguesa funcional
- [ ] X falla: [detalle]

## Issues detectados
1. [Severidad alta] Descripción del problema, dónde ocurre, cómo reproducir
2. [Severidad media] ...
3. [Severidad baja] ...

## Acciones correctivas
- [ ] [Issue 1] Asignado a [persona], fecha límite
- [ ] [Issue 2] ...

## WCAG 2.2 AA — checklist
- 1.1.1 Non-text Content: [ok / falla]
- 1.3.1 Info and Relationships: [ok / falla]
- 1.4.3 Contrast (Minimum): [ok / falla]
- 1.4.11 Non-text Contrast: [ok / falla]
- 2.1.1 Keyboard: [ok / falla]
- 2.1.2 No Keyboard Trap: [ok / falla]
- 2.4.3 Focus Order: [ok / falla]
- 2.4.7 Focus Visible: [ok / falla]
- 2.5.5 Target Size (AAA, pero es best practice): [ok / falla]
- 3.3.1 Error Identification: [ok / falla]
- 3.3.2 Labels or Instructions: [ok / falla]
- 4.1.2 Name, Role, Value: [ok / falla]
- 4.1.3 Status Messages: [ok / falla]
```

## Checklist WCAG 2.2 AA por categoría de componente

### Botones
- [ ] Elemento `<button>` (no `<div>` ni `<a>` salvo que enlace)
- [ ] Etiqueta clara (verbo en infinitivo, 1-2 palabras, no mayúsculas)
- [ ] Si lleva icono + texto: `aria-hidden=true` en SVG
- [ ] Si lleva solo icono: `role=img` + `aria-label`
- [ ] Si `target=_blank`: atributo `title` avisando
- [ ] Disabled: `aria-disabled` automático, NO botón invisible
- [ ] Estados: default / loading / success / error
- [ ] Contraste: border primary-base 1px sobre fondo blanco

### Inputs / Formularios
- [ ] `<label>` visible y único, apunta al `id` del input
- [ ] `id` único por input
- [ ] `name` para envío del formulario
- [ ] `autocomplete` cuando aplique (`email`, `tel`, `postal-code`, etc.)
- [ ] `type` correcto (`text`, `email`, `tel`, `date`, etc.)
- [ ] Si tiene hint: `<p id="hint">` + `aria-describedby` en el input
- [ ] Si tiene error: `<p id="error">` con `<span class="sr-only">Error:</span>` + `aria-errormessage` + `aria-invalid=true`
- [ ] Foco al error-summary al submit con errores
- [ ] `<form>` con `aria-label` o `aria-labelledby`
- [ ] Foco visible: NO `outline: none` sin alternativa
- [ ] Border input error: 1px alert-dark

### Tablas
- [ ] `<table role=grid>` con `<caption>` (visible o sr-only)
- [ ] `<thead>`, `<tbody>`, `<tfoot>` separados
- [ ] `<th scope=col|row>`, `tabindex=-1` en cabeceras
- [ ] `aria-sort` en columnas ordenables
- [ ] Navegación con flechas entre celdas
- [ ] En anchuras pequeñas: scroll horizontal + caption siempre visible
- [ ] `aria-describedby` apuntando al `<details>` con instrucciones si es tabla compleja

### Modales
- [ ] `role=dialog`, `aria-modal=true`, `aria-labelledby` al título
- [ ] Foco atrapado dentro del modal
- [ ] Esc cierra el modal
- [ ] Click fuera del contenedor cierra el modal
- [ ] Foco al cerrarse vuelve al elemento que lo abrió
- [ ] Icono de cierre con `aria-label`
- [ ] Variante destructiva: botón principal a la derecha, color `alert`

### Imágenes
- [ ] `alt` descriptivo (o `alt=""` si decorativa)
- [ ] Si SVG personalizado: `role=img` + `aria-label`

### Iconos
- [ ] Si acompañan texto: `aria-hidden=true`
- [ ] Si van solos: `role=img` + `aria-label` que describa la acción

### Navegación
- [ ] Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`
- [ ] Skip-link en cada cabecera
- [ ] Migas de pan con `<nav aria-label="Migas de pan">`
- [ ] Paginación con `aria-label="Paginación de resultados"`
- [ ] Menú móvil con `aria-expanded` y `aria-controls`

### Contraste (recordatorio)
- [ ] Texto sobre fondo blanco: usar colores `neutral-base` o más oscuros (4.5:1+)
- [ ] Texto sobre colores `base` (botones): solo permitido si peso semibold y ≥16px (3:1+)
- [ ] Texto sobre colores `light`: en mensajes de estado, no en texto principal
- [ ] Borders de inputs: 3:1+ sobre fondo

## Gotchas

- **No confiar solo en herramientas automáticas.** axe-core y pa11y detectan ~30-40% de issues. El resto requiere test manual.
- **No usar `outline: none` sin alternativa.** El foco debe ser siempre visible.
- **No confiar en `aria-hidden=true` para "ocultar" elementos a todos.** Solo oculta de lectores de pantalla, no de la vista.
- **No usar `placeholder` para información importante.** El placeholder desaparece al escribir.
- **No anidar landmarks.** `<header>` dentro de `<main>` rompe la jerarquía.
- **No usar tablas para layout.** Aunque "se vea bien", rompe la semántica de tablas.
- **No saltarse tests de teclado después de añadir interactividad nueva.** El foco y los shortcuts de teclado se rompen fácil.
- **No añadir iconos sin texto o aria-label.** Iconos sueltos son "elementos decorativos" para un lector de pantalla.

## Examples (uso típico)

### Ejemplo: Validar un componente Button antes de mergear

**Contexto:** dev acaba de implementar un botón "Eliminar" con variante destructiva. Quiere mergear. Antes, valida accesibilidad.

**Pasos con el skill:**

1. **Scan automático con axe-core** (5 min):
   ```bash
   npx axe http://localhost:4200/mi-pantalla --exit
   # Espera: 0 errores. Si hay, corregir antes de seguir.
   ```

2. **Test de teclado** (5 min):
   - Tab → foco al botón, outline visible ✅
   - Enter → activa la acción ✅
   - Si hay confirmación, abre modal con foco en título ✅

3. **Test con lector de pantalla** (5 min):
   - Botón anuncia: "Eliminar, botón" (no "icono de papelera, botón")
   - Si loading, anuncia: "Eliminando, por favor espere"

4. **Checklist específica de Button** (ver arriba en "Checklist WCAG 2.2 AA por categoría"):
   - ✅ Elemento `<button>` (no `<div>`)
   - ✅ Texto claro ("Eliminar", verbo en infinitivo)
   - ✅ Variante destructiva con color "alert" o "danger"
   - ✅ Si loading, previene doble click
   - ✅ Modal de confirmación posterior

5. **Reporte**: sin issues detectados → puede mergear.

### Ejemplo: Auditar accesibilidad de una página completa antes de release

**Contexto:** la app está a punto de pasar a revisión oficial de accesibilidad (obligatoria por RD 1112/2018). Auditar toda la home y las 5 pantallas principales.

**Pasos:**

1. **Scan automático por página** (10 min total):
   ```bash
   for url in / /tramites /notificaciones /mis-datos /ayuda /aviso-legal; do
     echo "--- $url ---"
     npx axe http://localhost:4200$url --exit | tail -5
   done
   ```

2. **Tests manuales por página** (10 min cada una = 60 min):
   - Navegación con teclado: ¿skip-link, orden de foco, focus visible?
   - Lector de pantalla: ¿landmarks, headings, labels correctos?
   - Contraste: ¿texto sobre fondos en cada zona?
   - Responsive: ¿móvil, tablet, desktop?

3. **Generar reporte** (15 min):
   - Una sección por página
   - Issues por severidad
   - Acciones correctivas con asignado y fecha
   - Checklist WCAG 2.2 firmado

4. **Pasar a revisión oficial**:
   - Adjuntar el reporte
   - Si hay issues altos, NO publicar hasta corregirlos
   - Issues medios: corregir antes de próxima release
   - Issues bajos: backlog

### Ejemplo: Detección de issue específico (aria-invalid faltante)

**Contexto:** el equipo hizo un formulario de login sin `aria-invalid` en los inputs con error.

**Test:**
- Submit con campo vacío
- axe-core detecta: "Form elements must have labels" — falso positivo (label existe)
- **Test manual con lector de pantalla:**
  - Introduce email mal
  - Submit → focus al error summary
  - Lector lee: "Email, edición" — **NO dice "error"**
- **Issue:** falta `aria-invalid=true` y `aria-errormessage` con id del mensaje de error

**Fix** (en `componente-input-text-codigo.html`):
```html
<!-- ANTES -->
<input type="email" id="email" name="email" />

<!-- DESPUÉS -->
<input
  type="email"
  id="email"
  name="email"
  aria-invalid="true"
  aria-errormessage="email-error"
/>
<p id="email-error" class="text-alert-dark text-sm">
  <span class="sr-only">Error:</span>
  El formato del email no es válido
</p>
```

**Re-test:** lector de pantalla ahora lee "Email, edición, error: el formato del email no es válido" ✅

## Recursos

- **WCAG 2.2:** https://www.w3.org/TR/WCAG22/
- **W3C ARIA Authoring Practices Guide:** https://www.w3.org/WAI/ARIA/apg/
- **axe-core:** https://github.com/dequelabs/axe-core
- **pa11y:** https://pa11y.org/
- **WebAIM contrast checker:** https://webaim.org/resources/contrastchecker/
- **Colour Contrast Analyser:** https://www.tpgi.com/color-contrast-checker/
- **MDN Accesibilidad:** https://developer.mozilla.org/es/docs/Web/Accessibility
- **Libro "Accesibilidad Web. WCAG 2.2 de forma sencilla":** https://olgacarreras.blogspot.com/2024/02/libro-accesibilidad-web-wcag-22-de.html
- **Real Decreto 1112/2018:** https://www.boe.es/diario_boe/txt.php?id=BOE-A-2018-12699
- **UNE-EN 301549:2022** (norma europea)

## Related

- **Skill: `desy-implement-component`** — generó el código a validar
- **Skill: `desy-choose-library`** — eligió la librería usada
- **Skill: `desy-scaffold-project`** — montó el proyecto
- **Mapa del ecosistema DESY:** [`/docs/ecosystem-map.md`](../../docs/ecosystem-map.md) (en este repo)
- **Doc oficial DESY accesibilidad:** `https://desy.aragon.es/como-empezar-accesibilidad.html.md`
