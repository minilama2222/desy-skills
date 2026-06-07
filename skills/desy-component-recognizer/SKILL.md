---
name: desy-component-recognizer
description: "Reconoce componentes del Design System DESY (Digital Service Standard) a partir de imágenes (mockups, screenshots). Usa el catálogo de descripciones visuales de los 57 componentes y sus 653 ejemplos. Output: tabla con componente, variante, ubicación, notas."
---

# desy-component-recognizer

Skill para identificar componentes UI del Design System DESY analizando imágenes (mockups, screenshots, fotos de pizarras, etc.). Combina visión multimodal con un catálogo de descripciones visuales mantenidas por el equipo de SDA (Servicios Digitales de Aragón).

## When to use this skill

- El usuario te pasa una imagen de un mockup o screenshot y te pide "qué componentes tiene", "reconoce los componentes", "identifica el stack"
- Necesitas mapear un diseño visual a los nombres técnicos de la librería
- Estás haciendo un audit de "qué componentes DESY usa este diseño" para una migración o refactor
- El usuario te da una imagen de referencia (ej: "como este mockup pero con X cambios") y necesitas identificar qué se reutiliza

**NO uses este skill si:**
- El usuario solo quiere implementar un componente ya identificado (usa `desy-implement-component` directamente)
- No tienes la imagen (es solo texto)

## El catálogo

El catálogo completo está en `assets/catalog.json` (~627KB) — 57 componentes y 653 ejemplos, cada uno con su `visualDescription` escrita por el equipo SDA. Estructura:

```json
{
  "<componente>": {
    "total_examples": N,
    "examples": [
      {
        "name": "por defecto",
        "description": "opcional: contexto o pseudoclase que simula",
        "data_keys": ["text", "disabled", "classes"],
        "visual_description": "Botón rectangular con borde azul de 1-2px, fondo blanco, ..."
      }
    ],
    "params": [{ "name": "...", "type": "...", "required": true, "description": "..." }]
  }
}
```

Para usar el catálogo, **cárgalo con `read` o `cat`** y haz matching contra la imagen. Es un JSON, no es enorme.

## Workflow

### Paso 1: Recibe la imagen

Cuando recibas una imagen (vía `image` tool, anexo en chat, o ruta en disco):
1. **Si la imagen es grande (>2000px de alto)**, divídela mentalmente por zonas (header, sidebar, main, footer)
2. **Detecta si es pantalla completa** (mobile, tablet, desktop) — el layout y la visibilidad de elementos cambia

### Paso 2: Análisis visual con M3 multimodal

Usa la herramienta `image` (que es M3 multimodal) con el prompt:

```
Analiza esta imagen y lista TODOS los elementos UI visibles. Para cada elemento indica:
- Tipo de elemento (botón, input, card, tabla, etc.)
- Variante probable (primary, secondary, alert, etc.)
- Color/es principal/es
- Texto visible
- Estado (default, hover, active, focus, disabled)
- Posición en la imagen (header / sidebar / main / footer, izquierda / centro / derecha, arriba / medio / abajo)
- Si tiene icono, qué forma
```

Esto te da una **lista cruda de elementos visuales** (sin necesariamente los nombres de componentes DESY).

### Paso 3: Matching con el catálogo

Para cada elemento identificado en el paso 2:

1. **Lee el catálogo** (`assets/catalog.json`)
2. **Busca los componentes candidatos** comparando:
   - **Forma y layout** (botón rectangular, input con label, card con header+body+footer, etc.)
   - **Color** (azul primario, gris neutro, rojo alerta, etc.)
   - **Estado** (fondo sólido, borde, ghost, etc.)
   - **Posición** (header → componentHeader; input en form → componentInput o compound como input-group, date-input, etc.)
3. **Para candidatos similares** (ej: "input" vs "input-group" vs "date-input"), usa las reglas de "cuándo usar" más abajo
4. **Asigna la variante** más probable (ej: "primary", "alert", "por defecto deshabilitado")

### Paso 4: Output en tabla

Devuelve SIEMPRE en este formato (es el que espera el sistema, según `desy-identify`):

```markdown
| Nº | Componente | Variante | Ubicación en imagen | Notas adicionales |
|:--:|:-----------|:---------|:--------------------|:------------------|
| 1 | button | primario | header, derecha | "Acceder" |
| 2 | input | text | main, formulario | label "Nombre" |
| 3 | input | text | main, formulario | label "Apellido 1" |
| 4 | input | text | main, formulario | label "NIF", pattern NIF/NIE |
| 5 | error-message | alert | main, debajo del input NIF | "Formato no válido" |
| 6 | button | primario | main, final del form | "Siguiente" |
| 7 | button | default | main, final del form | "Atrás", disabled |
| 8 | footer | - | footer | institucional con 3 logos |
```

**Reglas para la tabla:**
- **Numerar secuencialmente** (1, 2, 3...) de arriba a abajo, izquierda a derecha
- **Una fila por componente** (no por subelemento). Ej: si ves un `input-group` con 2 inputs + 1 botón, UNA sola fila para `input-group` (no 3 filas)
- **Solo descomponer en atómicos** (button, input, label) cuando NO haya un compuesto (input-group, date-input, checkboxes, modal) que coincida
- **Variante:** la del catálogo (`primario`, `alerta`, `default`, `text`, `sm`, `lg`, etc.)
- **Ubicación:** header/nav/main/aside/footer + posición relativa
- **Notas:** texto visible, iconos, colores específicos, relaciones con otros componentes

## Reglas críticas de matching

Estas son las confusiones más comunes — revísalas SIEMPRE antes de proponer un componente:

### 1. **"dialog" NO es un botón, es el resultado de hacer click**

`componentDialog` se invoca con un `<button>` que tiene el `data-module="c-dialog"` o `data-dialog-open` y un `<div data-module="c-dialog-content">` con el contenido del diálogo. **En el screenshot verás el botón (que parece un button normal), NO el diálogo (que está oculto).** Si ves un modal o diálogo visible, ya está abierto. Identifica el botón que lo dispara.

### 2. **"modal" vs "dialog" vs "drawer"**

- `modal`: bloquea toda la UI, fondo oscuro overlay, contenido centrado. Es el "modal tradicional"
- `dialog`: similar al modal pero más semántico, usa el `<dialog>` nativo de HTML. Para confirmaciones
- `drawer`: panel lateral que entra desde un lado (derecha/izquierda/abajo). NO bloquea toda la UI

Si ves overlay oscuro cubriendo la página → modal o dialog. Si ves panel lateral → drawer (que es un pattern de offcanvas en DESY, no un componente directo).

### 3. **"input" vs "input-group" vs "date-input" vs "datepicker"**

- `input` (componente atómico): UN solo input. Default de la librería
- `input-group`: composición de label + input + hint + error-message. Lo que ves el 90% de las veces en formularios
- `date-input`: input de fecha con formato dd/mm/yyyy, validación específica
- `datepicker`: calendario popup que aparece al hacer click en un date-input

**Si ves un campo con label, input y (opcionalmente) hint debajo:** probablemente es `input-group`. Si el input tiene formato de fecha con calendario → `date-input`. Si ves un popup calendario abierto → `datepicker`.

### 4. **"table" vs "table-advanced"**

- `table`: tabla HTML estándar con estilos DESY (`.c-table`)
- `table-advanced`: tabla con paginación, búsqueda, selección múltiple, acciones en lote. Si ves filtros, checkboxes en header, paginación → `table-advanced`

### 5. **header vs header-mini vs header-advanced**

Distinguir los 3 tipos de header por la estructura visible:

- **`header-mini`**: UNA sola banda muy fina. Solo el logo (típicamente el escudo de Aragón). Sin nav, sin perfil de usuario. Aparece en páginas minimalistas (login, error 404, mapa web, accesibilidad).
- **`header`**: UNA sola banda con logo + (opcionalmente) nombre de la app + nav + perfil. Aparece en webapps con sesión iniciada.
- **`header-advanced`**: TRES bandas visibles. Banda 1: branding institucional (logo Aragón). Banda 2: nombre del portal. Banda 3: nav principal con megamenú. Aparece en portales públicos (ej: "Portal de Salud").

**Patrones visuales para distinguirlos:**
- Si ves una sola franja fina con solo el logo → `header-mini`
- Si ves una franja con logo + nombre de app + nav (todo en una línea) → `header`
- Si ves 3 franjas apiladas (logo arriba, nombre del portal en medio con fondo oscuro, nav abajo) → `header-advanced`

**Confusión típica:** a veces un header "normal" se confunde con header-advanced por tener subnav. La regla: header-advanced SIEMPRE tiene 3 bandas visualmente distintas. Header normal tiene 1 sola banda, aunque tenga subnav debajo.

### 6. **menu-horizontal vs menu-navigation vs menubar**

- `menu-horizontal`: barra de navegación horizontal simple, una sola línea
- `menu-navigation`: navegación más completa, puede tener submenús, branding integrado
- `menubar`: patrón tipo desktop application (File, Edit, View...), con menús desplegables por click

**Si ves una nav horizontal en un header web** → `menu-navigation`. Si es una nav simple con 3-4 links sin submenús → `menu-horizontal`. Si parece un menú de aplicación tipo Word → `menubar`.

### 7. **`alert` MUESTRA un `notification` — identifica el notification, no el alert**

**Regla crítica**: el componente `alert` (componentAlert) es un **wrapper/contenedor** que casi siempre renderiza un `notification` (componentNotification) DENTRO. El notification es lo que el usuario ve: icono + texto + botón X de cerrar. El alert es solo el rectángulo con borde/fondo que lo envuelve.

- **Si ves un cuadro de aviso con icono + texto + botón cerrar:** es un `notification` (éxito, alerta, advertencia, o información). **No es alert.**
- **Si ves el wrapper (borde y fondo) sin el notification dentro:** es `alert` solo.

**Patrón de código típico:**
```njk
{{ componentAlert({
  "type": "success",
  "titleText": "...",
  "content": ...  ← aquí va el componentNotification
}) }}
```

**Variantes de notification que verás más frecuentemente:**
- `éxito` (verde, icono de check) — "Te has identificado correctamente", "Operación completada"
- `alerta` (rojo, icono de exclamación) — errores
- `advertencia` (amarillo, icono de warning) — avisos
- `información` (azul, icono de i) — información general

**Falso positivo histórico:** en el mockup `patron-pagina-acceso-cargando`, M3 reconoció "alert" cuando en realidad era un `notification` (éxito) con el texto "Te has identificado correctamente".

### 8. **Ejemplos visualmente similares ≠ mismo componente**

Dos ejemplos pueden verse casi iguales pero diferir en:
- **Parámetros** (ej: button con `text` distinto, no es otra variante — es la misma con otro label)
- **JavaScript global** que interactúa (ej: combo vs select — el combo tiene JS que filtra, el select no)
- **Pseudoclase simulada** (ej: "por defecto con estado hover" usa `ds-hover` para forzar el estilo de hover; NO es hover real)

**Si dos elementos se ven iguales y solo difiere el texto**, es el mismo componente, no es una variante nueva.

### 9. **El "recuadro con border 1px" NO es parte del componente**

En el catálogo de ejemplos (las páginas de `examples-X.html`), cada ejemplo está enmarcado por un `<div class="border border-neutral-base">` (la macro `componentExample` en `docs/_macro.component-example.njk`). **Este recuadro es del catálogo, no del componente.** Cuando analices una captura del catálogo, ignora el recuadro exterior.

### 10. **Colores de marca vs colores de UI**

- **Azul petroléo/petróleo (#00607a)** = color primario, muchos componentes
- **Verde, rojo, amarillo** = estados (success, alert, warning)
- **No confundir rojo de "alerta" con rojo de "link clickeado"** (los links visited pueden ser rojos pero NO son alert)

## Limitaciones conocidas

- **El catálogo es de `desy-html` (v16.x).** Los componentes de `desy-angular` o `desy-ionic` no están catalogados. Si el mockup usa Ionic (mobile-first, gesture-driven) o Angular Material, NO uses este skill.
- **El catálogo no incluye patrones compuestos** (header + nav + dropdown + button = "header con menú de usuario"). El skill identifica los componentes individuales, tú los describes como "patrón compuesto" en las notas.
- **El skill no genera código.** Solo identifica. Para implementar lo identificado, usa `desy-implement-component`.
- **Estados hover/active/focus NO se ven en screenshots estáticos.** Si el screenshot NO simula estos estados, no los infieras — marca como "no visible" o "no verificable".
- **El skill puede confundirse con patrones de otros sistemas de diseño** (Bootstrap, Material, Tailwind UI, etc.). Si dudas, pregunta al usuario o pide más screenshots.

## Verificación de la identificación

Después de hacer el matching, pregúntate:

1. **¿El componente identificado existe en el catálogo?** (búscalo en `catalog.json`)
2. **¿La variante coincide con un ejemplo conocido?** (compara con `visual_description` del ejemplo)
3. **¿Hay un componente compuesto más apropiado?** (input-group en vez de input solo)
4. **¿El contexto de uso tiene sentido?** (un input-group con label "Fecha de nacimiento" → date-input sería más específico que input genérico)

Si 2+ checks fallan, re-evalúa el matching. Si todavía dudas, propón 2 candidatos y deja al usuario elegir.

## Ejemplo completo de uso

**Input:** screenshot de una página de login DESY

**Output esperado:**

```markdown
| Nº | Componente | Variante | Ubicación en imagen | Notas adicionales |
|:--:|:-----------|:---------|:--------------------|:------------------|
| 1 | skip-link | - | top, oculto hasta focus | "Saltar al contenido principal" |
| 2 | header | mini | header | logo Aragón, sin nav (no logueado) |
| 3 | link | primary | main, parte superior | "He olvidado mi contraseña" |
| 4 | input-group | text | main, formulario | label "Usuario", hint con icono |
| 5 | input-group | password | main, formulario | label "Contraseña", con ojito |
| 6 | button | primary | main, final del form | "Acceder", ancho completo |
| 7 | link | default | main, debajo del form | "Crear cuenta nueva" |
| 8 | footer | - | footer | institucional con 3 logos |
```

## Validación con gold estándar

Si tienes un screenshot gold oficial (ej: `https://desy.aragon.es/componente-X-codigo.html.md`), compáralo con tu identificación:
- **Componentes:** ¿coinciden? (debería ser 100% para mocks del mismo sistema)
- **Variantes:** ¿coinciden? (debería ser 100% para mocks exactos)
- **Ubicación:** ¿coincide la posición relativa? (puede variar en mocks rediseñados)

Las discrepancias en mocks rediseñados son SEÑALES de mejora (ej: el usuario migró de variant `default` a variant `primary`, eso es información valiosa).

## Related

- `desy-implement-component` — después de identificar, implementa con el componente correcto
- `desy-styles-reference` — para conocer los tokens visuales (colores, espaciado) que el catálogo referencia
- `desy-choose-library` — si el mockup es desy-html, desy-angular o desy-ionic, esto lo decide
- `desy-scaffold-project` — para arrancar un proyecto donde implementar lo identificado
