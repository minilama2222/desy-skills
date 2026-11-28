---
name: desy-validate-accessibility
description: "Valida la accesibilidad WCAG 2.2 AA de páginas y componentes DESY. Úsala SIEMPRE al terminar de maquetar o modificar una página DESY, antes de darla por terminada, también en sesiones sin servidor ni usuario: trae un checklist que se ejecuta con grep sobre el HTML (fieldsets con legend, un solo h1, labels, skip-link). Úsala también antes de mergear, en auditorías y en revisiones de accesibilidad, con axe-core y tests manuales."
---

# desy-validate-accessibility

Valida la accesibilidad WCAG 2.2 AA de componentes o páginas implementadas con DESY. Combina herramientas automáticas con tests manuales (teclado, lector de pantalla, contraste).

> ⚠️ **Para el agente (importante):** hay dos niveles.
> - **El «Checklist sin servidor» se ejecuta siempre**, también en sesiones autónomas: solo lee ficheros (`grep` sobre el HTML compilado), no instala nada ni necesita servidor.
> - **Los bloques bash del Workflow (axe-core, Pa11y) son REFERENCE TEMPLATES** que el usuario o el equipo ejecuta en su propio proyecto. **NO los ejecutes automáticamente** sin confirmación explícita: `npm install --save-dev` modifica el `package.json` del usuario y el scan contra `localhost` asume un dev server corriendo.

## Cuándo usarla
- **Triggers:** *"valida accesibilidad"*, *"comprueba WCAG"*, *"pasa el axe"*, *"audita accesibilidad"*, *"¿es accesible?"*, *"cumple WCAG 2.2 AA?"*, *"preparamos release, hay que pasar revisión oficial"*.
- **Cargar:** tras `desy-design-match`, antes del merge/release.
- **NO usar para:** implementar componente (→ `desy-implement-component` primero, validar después), consultar token (→ `desy-styles-reference`), diferencia visual no a11y (→ `desy-design-match`), auditar contraste aislado (→ WebAIM/Colour Contrast Analyser directo).

## Posición en el workflow DESY
Paso **5** de la secuencia de `desy-preflight-check` — después de `desy-implement-*` + `desy-design-match`, antes de dar la página por terminada y antes del merge.

## Errores típicos que evita
- ❌ **Mergear UI sin pasar axe-core**: el primer escaneo encuentra 5-15 issues triviales (labels sin `for`, contraste < 4.5:1, headings sin jerarquía).
- ❌ **Confiar solo en automáticas**: axe-core y pa11y detectan ~30-40% de issues. El resto requiere test manual (teclado, lector de pantalla).
- ❌ **Saltarse lector de pantalla**: mensaje de error no asociado al campo, `role="alert"` mal aplicado, landmarks duplicados son invisibles a axe pero críticos.
- ❌ **No probar teclado en modales**: foco que escapa al hacer Tab, Esc que no cierra, foco que no vuelve al botón origen — pasa el scan pero rompe la experiencia.
- ❌ **Auditar solo en desktop**: test responsive (375px, tablet) revela target size táctil, scroll horizontal, menús hamburguesa inaccesibles.

## Siguiente skill típica
→ Si validación OK: mergear / release / revisión oficial.
→ Si issues: **`desy-implement-component`** (fix específico) o **`desy-styles-reference`** (si el issue es de tokens de contraste).
→ Si la página no es accesible por problema visual WCAG: `desy-implement-layout-patterns` o `desy-design-match`.
→ Si target es desy-angular: re-validar tras traducir.

## Related

- **Skill: `desy-implement-component`** — generó el código que se valida aquí.
- **Skill: `desy-choose-library`** — eligió la librería usada.
- **Skill: `desy-scaffold-project`** — montó el proyecto.
- **Skill: `desy-design-match`** — afina visualmente antes de validar a11y.
- **Skill: `desy-styles-reference`** — fuente de verdad de tokens (consultar ratios de contraste).
- **Mapa del ecosistema DESY:** `docs/ecosystem-map.md` (en este repo).
- **Doc oficial DESY accesibilidad:** `https://desy.aragon.es/como-empezar-accesibilidad.html.md`

Antes de aplicar este skill, asegúrate de tener:

- El proyecto DESY corriendo localmente (`npm run dev` o `ionic serve`)
- Node y npm disponibles
- Opcional pero recomendado: navegador Chrome o Firefox con extensiones instaladas
- Opcional: lector de pantalla (NVDA en Windows, VoiceOver en macOS, Orca en Linux)

## Checklist sin servidor (sesiones autónomas)

Sobre el HTML compilado de la página (`dist/<pagina>.html` en `desy-html-starter`). Cada comprobación dice el resultado esperado; si falla, corrige antes de dar la página por terminada.

```bash
P=dist/<pagina>.html
# 1. Un solo h1 → 1
grep -o '<h1[ >]' "$P" | wc -l
# 2. Un fieldset por grupo de campos y por checkbox legal → ≥ nº de grupos
grep -c '<fieldset' "$P"
# 3. Cada fieldset con su legend → el mismo número que el anterior
grep -c '<legend' "$P"
# 4. Cada input, select y textarea con su label → no imprime nada
for id in $(grep -oE '<(input|select|textarea)[^>]* id="[^"]+"' "$P" | grep -v 'type="hidden"' | sed -E 's/.* id="([^"]+)".*/\1/'); do grep -q "for=\"$id\"" "$P" || echo "sin label: $id"; done
# 5. Skip-link → ≥ 1
grep -c 'c-skip-link' "$P"
# 6. <html> con lang → no imprime nada
perl -0777 -ne 'print "falta lang en <html>\n" unless /<html\b[^>]*\slang=["\x27]?[a-z]/i' "$P"
# 7. <title> no vacío → no imprime nada
perl -0777 -ne 'print "falta <title> o está vacío\n" unless /<title>\s*[^<\s][^<]*<\/title>/i' "$P"
# 8. <meta name="viewport"> → no imprime nada
perl -0777 -ne 'print "falta <meta name=\"viewport\">\n" unless /<meta\b[^>]*\sname=["\x27]?viewport/i' "$P"
# 9. Ningún submit deshabilitado (también <button> sin type, que envía) → no imprime nada
perl -0777 -ne 'while (/<form\b.*?<\/form>/gs) { for (my @b = $& =~ /<(?:button|input)\b[^>]*>/g) { s/\s+/ /g; print "submit deshabilitado: $_\n" if / disabled(?:[ =>\/]|$)/ && (/^<button/ && !/ type="(?:button|reset)"/ || / type="submit"/) } }' "$P"
# 10. Cada <button> dentro de un <form> con type explícito → no imprime nada
perl -0777 -ne 'while (/<form\b.*?<\/form>/gs) { for (my @b = $& =~ /<button\b[^>]*>/g) { s/\s+/ /g; print "sin type: $_\n" unless / type="/ } }' "$P"
```

- [ ] Los títulos visibles de sección son h2 (o h3) **fuera** del fieldset, y la `legend` los repite con `class="sr-only"`. Una `legend class="c-h2"` deja el `main` sin encabezados.
- [ ] Los encabezados no saltan de nivel (h1 → h2 → h3).
- [ ] Los iconos decorativos llevan `aria-hidden="true"`, y los botones que solo tienen icono, `aria-label`.
- [ ] Los botones del formulario que no envían (Cancelar, Añadir, Ver contraseña) llevan `type="button"`: sin `type`, un `<button>` dentro de `<form>` envía el formulario (la macro `button` de desy-html no pone `type`, y en desy-angular el valor por defecto es `submit`). El submit no se deshabilita: se valida al enviar y se muestran los errores.

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
| **Foco tras enviar con errores** | Al recargar la página con errores, el foco va al resumen de errores o al primer campo con error |

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
| Lectura de un input con error | "Nombre, no válido, edición, requerido, error: el campo es obligatorio" |
| Lectura de un formulario completo | "Formulario de contacto" (por `aria-label` o `aria-labelledby`) |
| Lectura de una tabla | "Tabla, 3 filas, 4 columnas. Encabezado: Mes, Pago 1, Pago 2" |
| Lectura de un modal al abrirse | Anuncia el diálogo con su título (por `aria-labelledby`), p. ej. "¿Eliminar expediente?, diálogo"; en la variante destructiva, el foco cae en "Cancelar, botón" |
| Lectura de un link que abre nueva ventana | Lee el aviso dentro del enlace, p. ej. "Informe anual (se abre en ventana nueva), enlace" (texto visible o `sr-only`, no `title`) |
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
| Texto normal (todo el que no es texto grande) | 4.5:1 |
| Texto grande (≥24 px, o ≥18.66 px en negrita) | 3:1 |
| Componentes de interfaz e iconos funcionales (no decorativos) | 3:1 |
| Bordes de inputs | 3:1 |

**Comprobar:**
- Texto sobre fondo blanco
- Texto sobre colores `light` (mensajes de estado)
- Texto sobre colores `base` (botones, solo permitido si semibold ≥16px; a ese tamaño sigue siendo texto normal y necesita 4.5:1)
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
- [x] Texto sobre base: 16px+ semibold y 4.5:1+
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
- 2.5.8 Target Size (Minimum): 24×24 px CSS como mínimo, o espaciado equivalente: [ok / falla]
- 2.5.5 Target Size (Enhanced), AAA, recomendación: 44×44 px: [ok / falla]
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
- [ ] Si lleva solo icono: `aria-label` en el `<button>` que describe la acción, y el SVG con `aria-hidden="true"` (el nombre lo lleva el botón, no el icono)
- [ ] Si abre en ventana nueva (`target="_blank"`): el aviso va dentro del enlace, con texto visible o con `<span class="sr-only">(se abre en ventana nueva)</span>`. No uses el atributo `title` para avisar: solo se ve al pasar el ratón y no llega por teclado (MWG `accessibility`)
- [ ] Disabled: `aria-disabled` automático, NO botón invisible. El submit de un formulario no se deshabilita: se valida al enviar
- [ ] Estados: default / loading / success / error
- [ ] Contraste: border primary-base 1px sobre fondo blanco

### Inputs / Formularios
- [ ] `<label>` visible y único, apunta al `id` del input
- [ ] `id` único por input
- [ ] `name` para envío del formulario
- [ ] `autocomplete` cuando aplique (`email`, `tel`, `postal-code`, etc.)
- [ ] `type` correcto (`text`, `email`, `tel`, `date`, etc.)
- [ ] Si tiene hint: `<p id="hint">` + `aria-describedby` en el input
- [ ] Si tiene error, sigue el patrón de errores:

  > Con error de servidor: la macro emite `aria-invalid="true"` y `aria-errormessage`; el mensaje va con la macro `errorMessage` (prefijo `<span class="sr-only">Error:</span>`); arriba del formulario, un resumen de errores con enlaces a cada campo; al recargar, foco en el resumen o en el primer campo con error. Validación en el cliente: consulta MWG `accessible-error-announcement` y `validate-input-after-interaction` (`aria-invalid="false"` hasta `:user-invalid`). No se fija `aria-invalid="true"` a mano en el marcado.
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
- [ ] Variante destructiva: foco inicial en Cancelar (la acción segura), en lugar del encabezado. El botón Cancelar tiene `id` y se pasa como tercer argumento (`focusFirst`) de `openDialog`. En desy-html, en el botón que abre el modal: `"onclick": "openDialog('modal-eliminar', this, 'boton-cancelar-eliminar')"`.

> Choque con MWG `dialog`: MWG recomienda `<dialog>` nativo sin `role`/`aria-modal`. Los componentes `modal` y `dialog` de DESY son `<div>` gestionados por `dialog.js`, que exige `role="dialog"`; por eso aquí sí se pide. Mejora pendiente en la librería: migrar a `<dialog>` nativo.

### Imágenes
- [ ] `alt` descriptivo (o `alt=""` si decorativa)
- [ ] Si SVG personalizado informativo, fuera de un botón o enlace: `role="img"` + `aria-label`

### Iconos
- [ ] Si acompañan texto: `aria-hidden=true`
- [ ] Si van solos dentro de un botón o enlace: `aria-hidden="true"` en el icono y `aria-label` en el control, que describa la acción
- [ ] Si van solos y transmiten información (estado, aviso) fuera de un control: `role="img"` + `aria-label`

### Navegación
- [ ] Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`
- [ ] Skip-link en cada cabecera
- [ ] Migas de pan con `<nav aria-label="Migas de pan">`
- [ ] Paginación con `aria-label="Paginación de resultados"`
- [ ] Menú móvil con `aria-expanded` y `aria-controls`

### Contraste (recordatorio)
- [ ] Texto sobre fondo blanco: usar colores `neutral-base` o más oscuros (4.5:1+)
- [ ] Texto sobre colores `base` (botones): solo permitido si peso semibold y ≥16px, y con 4.5:1 (16 px semibold no es texto grande)
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
   - Si hay confirmación, abre el modal con el foco en Cancelar (`focusFirst` de `openDialog`) ✅

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

### Ejemplo: Detección de issue específico (error que el lector no anuncia)

**Contexto:** el equipo hizo un formulario de login con el `<input>` escrito a mano, sin la macro `input` de DESY, y el mensaje de error es un `<p>` suelto debajo del campo.

**Test:**
- Submit con el email mal escrito
- axe-core no lo detecta: el campo tiene label y el mensaje se ve
- **Test manual con lector de pantalla:**
  - Tras recargar, el foco va al resumen de errores
  - Al ir al campo, el lector lee: "Email, edición" — **NO dice "error"** ni lee el mensaje
- **Issue:** el mensaje de error no está asociado al campo, porque el campo no sale de la macro

**Fix:** usar la macro `input` con `errorMessage` y seguir el patrón de errores (resumen de errores con enlace al campo, foco al recargar). No se añade `aria-invalid` a mano: la macro emite `aria-invalid` y `aria-errormessage` solo cuando recibe `errorMessage`, y deja de emitirlos cuando el campo es válido.

```njk
{{ componentInput({
  "id": "email",
  "name": "email",
  "type": "email",
  "autocomplete": "email",
  "label": { "text": "Email" },
  "errorMessage": { "text": "El formato del email no es válido" }
}) }}
```

Si la validación se hace en el cliente, sin recargar, consulta MWG `accessible-error-announcement` y `validate-input-after-interaction`.

**Re-test:** lector de pantalla ahora lee "Email, no válido, edición, error: el formato del email no es válido" ✅

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
