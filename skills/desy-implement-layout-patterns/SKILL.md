---
name: desy-implement-layout-patterns
description: DESY structural patterns: fieldset+legend, grids, action sections, header with skip-link. Use for any page section that groups or grids content.
---

# desy-implement-layout-patterns

Patrones estructurales de maquetación DESY para agrupar, grid-ear y disponer acciones al final de cualquier sección de página (forms, cards, listados, cabeceras, FAQs, errores). Complementa a `desy-implement-component` (que cubre componentes individuales) y a `desy-implement-pattern` (que cubre patrones de negocio como datos-identidad, domicilio-postal, FAQs).

**Origen del nombre:** antes `desy-implement-form-patterns`, renombrado en 2026-07-03 porque su contenido (fieldset, grids responsive, section+ul, spacing) aplica a cualquier tipo de sección de página, no solo a forms.

**Hallazgo 2026-07-03 (test del wizard Paso 3 - Dirección postal):** El output del skill `desy-implement-component` por sí solo produce inputs coherentes pero sin agrupación semántica ni estructura responsive de grid. Este skill añade la capa estructural que falta.

**Hallazgo 2026-07-03 (acceso al repo `gorilas/desy.aragon.es`):** Estos patterns son transversales en el sitio oficial. Se aplican también a cards (`cards-misma-altura`), cabeceras (`cabecera-editar`), errores (`errores-estaticos`), notificaciones, FAQs, listados, etc.

## When to use this skill

- Te piden una página con un form (wizard, formulario de edición, alta de datos)
- Vas a montar varios inputs en una grid y necesitas saber qué grid usar
- Necesitas agrupar inputs por sección semántica (Domicilio, Ubicación, etc.) con fieldset+legend
- Tienes acciones al final del form (Siguiente, Atrás, Saltar, etc.) y necesitas el patrón de section+ul
- Necesitas saber cuándo aplicar `mt-base mb-base lg:mt-0 lg:mb-0` vs nada

## Paso 0: ¿tienes referencia visual? Bucle "compara → busca ejemplo → aplica tuneando"

**Cuándo aplica este paso:** antes de elegir el patrón estructural (header, footer, fieldset, grid, acciones), cuando tengas una referencia visual (gold del sitio oficial, mockup de Figma, captura de un sitio similar). NO aplica si solo tienes texto o si vas a implementar sin referencia.

**Pre-requisito del Paso 0 (Paso -0.5):** identifica primero la **plantilla de página** que vas a extender con `desy-choose-page-template` (por ejemplo: `_template.with-header-advanced.njk` para portales institucionales, `_template.logged-selector.njk` para webapps autenticadas, `_template.logged-out.njk` para páginas públicas sin auth). Sin la plantilla correcta, el header y el footer no se montarán como en el gold (ej. usar `_template.home.njk` para un portal da header local del starter en vez del header-advanced institucional).

**El bucle (3 pasos):**

1. **Compara** la referencia contra tu 1ª pasada. Identifica qué difiere estructuralmente. Usa `desy-design-match` para medir discrepancias si tienes el gold servible (HTML o screenshot).
2. **Busca el ejemplo concreto** del catálogo DESY que más se acerca a la referencia. Para header, `desy-component-recognizer` (regla 5) clasifica por nº de bandas: `header-mini` (1 banda fina), `header` (1 banda con nav+user), `header-advanced` (3 bandas). Para otros componentes, cada `_examples.<componente>.njk` lista ejemplos tuneables (header: 14, footer: 15, etc.).
3. **Aplica tuneando.** El ejemplo concreto da la estructura (bandas, posiciones, clases, anchos). Los params del componente (texto, items, dropdown) se ajustan al caso concreto.

**Ejemplo validado 2026-07-04 (wizard paso-1, Gobierno de Aragón):**

- *Referencia (gold):* header con logo Aragón + dropdown "Gestor de expedientes" + nav Inicio/Expedientes/Bandejas + dropdown "Ana Pérez". Footer con links + Creado por SDA + CC BY 4.0 + dirección + logos EU/Fondos Europeos.
- *Componente clasificado:* `header` (1 banda, webapp autenticada). NO `header-advanced` (que sería 3 bandas).
- *Ejemplo del catálogo elegido:* "Con todo" (`_examples.header.njk`, ejemplo #13) — coincide estructuralmente con el gold.
- *Tuneo header:* cambiar `navigation.items` (Navigation item 1/2/3 → Inicio/Expedientes/Bandejas) y `dropdown.items` (Marta Pérez → Ana Pérez).
- *Ejemplo del catálogo elegido footer:* "Con logo feder y otros logos personalizados" (`_examples.footer.njk`) — coincide con los logos EU/Fondos Europeos del gold.
- *Tuneo footer:* el ejemplo ya trae los logos correctos; ajustar solo textos de los links.

**Nomenclatura validada (2026-07-04, corregir uso):**

- NO usar "chrome" para el logo. Usar **logo extendido** (`yourlogo-expanded.svg`, con texto, header webapp) y **logo contraído** (`yourlogo-compact.svg`, sin texto, móvil / header-mini). Existe también **logo mini** (`yourlogo-mini.svg`) para header-mini en pantallas muy estrechas.

**Cuándo NO aplicar este paso:**

- ❌ Si no tienes referencia visual (implementas solo con texto del usuario).
- ❌ Si el componente no está en el catálogo (caso edge; documentar primero antes de improvisar).
- ❌ Si la referencia coincide exactamente con un ejemplo ya aplicado (no hace falta re-trabajar).

**Relación con `desy-design-match`:**

`desy-design-match` afina la fidelidad visual fina (spacing, tipografía, márgenes) en 2ª pasada. Este Paso 0 elige el patrón estructural correcto en 1ª pasada. Orden: primero Paso 0 (estructura), luego `desy-design-match` (fidelidad).

## Fieldset+legend sr-only para grupos semánticos

**Regla:** cualquier grupo de inputs relacionados **se envuelve en `<fieldset>` con `<legend class="sr-only">`**, incluso si el grupo es un único checkbox.

El legend SIEMPRE va con `class="sr-only"`:
- Es accesible para screen readers (lee "Domicilio postal" al entrar al grupo)
- No aparece visualmente (el título visible va en un H1/H2 fuera del fieldset)
- Cumple WCAG 2.2 (cada grupo tiene su landmark navegable)

### Patrón de grupo de inputs relacionados

```html
<fieldset>
  <legend class="sr-only">Domicilio postal</legend>
  <div class="grid lg:grid-cols-4 gap-x-4">
    <!-- inputs del grupo -->
  </div>
</fieldset>
```

### Patrón de un único checkbox (privacidad, términos)

```html
<fieldset>
  <legend class="sr-only">Política de privacidad y protección de datos</legend>
  <div class="c-checkboxes" data-module="c-checkboxes">
    <div class="relative flex items-start py-base">
      <div class="flex items-center mx-sm">
        <input class="w-6 h-6 ..." id="politicas-rgpd" name="check-politicas" type="checkbox">
      </div>
      <div class="pt-0.5 leading-5">
        <label class="block" for="politicas-rgpd">Acepto la <a href="#" class="c-link">política de privacidad</a> (Obligatorio)</label>
      </div>
    </div>
  </div>
</fieldset>
```

**Por qué fieldset incluso para un solo checkbox:** el campo tiene valor legal (consentimiento). Sin fieldset+legend, no hay agrupación semántica que un screen reader pueda anunciar al entrar.

### Anti-patterns

- ❌ Poner el título del grupo dentro del `<legend>` visible (debe sr-only para evitar redundancia con el H1/H2)
- ❌ Usar `<div>` con `role="group"` (no es estándar, mejor fieldset que ya lo provee)
- ❌ Olvidar `<fieldset>` y meter los inputs sueltos (rompe navegación por landmarks)

## Grid responsivo del formulario

### Grid madre: solo desktop

```html
<div class="grid lg:grid-cols-4 gap-x-4">
  <!-- items del grid -->
</div>
```

- **Solo `lg:grid-cols-N`** (no `grid-cols-*` mobile explícito). En mobile cada item va a su propia fila.
- **`gap-x-4`** (1rem horizontal). NO `gap-lg` (es para layouts más amplios).
- Separación vertical entre filas viene de `gap-y-*` del form padre (no del grid).

### Selección de `lg:grid-cols-N`

| Caso de uso | Columnas | Razón |
|---|---|---|
| 2 campos lado a lado en desktop | `lg:grid-cols-2` | Inputs variables (email + confirmar) |
| Formulario denso (4 campos cortos) | `lg:grid-cols-4` | Como Paso 3: Tipo de vía + Vía + ... |
| Grid mixto (1 corto + 2 largos) | `lg:grid-cols-5` | Como Paso 3 Ubicación: CP + Provincia + Municipio |

**Regla práctica:** cuenta cuántas columnas CABEN en el contenido más ancho. Si tus inputs más anchos ocupan 3 de 4 columnas (e.g. Vía), los demás ocupan el resto (Tipo de vía = 1 col).

### Items del grid: `col-span-*`

```html
<div class="c-form-group lg:col-span-3">
  <label>Vía</label>
  <input class="w-full">
</div>
```

- Mobile: cada item = 1 fila completa (implícito).
- Desktop: `lg:col-span-*` indica columnas a ocupar.
- `col-span-1` por defecto si no se especifica (omítelo si es 1).

### Patrón para campos cortos múltiples (grid anidado)

Cuando necesitas 4 inputs cortos (Número, Escalera, Piso, Puerta) en una sola fila desktop:

```html
<div class="grid lg:grid-cols-4 gap-x-4">
  <div class="lg:col-span-2 grid grid-cols-4 gap-x-4">
    <!-- grid anidado de 4 cols, vive dentro del col-span-2 del padre -->
    <div class="c-form-group"><label>Número</label><input class="w-full"></div>
    <div class="c-form-group"><label>Escalera</label><input class="w-full"></div>
    <div class="c-form-group"><label>Piso</label><input class="w-full"></div>
    <div class="c-form-group"><label>Puerta</label><input class="w-full"></div>
  </div>
  <div class="c-form-group lg:col-span-2">
    <label>Indicaciones adicionales</label>
    <input class="w-full" autocomplete="address-line2">
  </div>
</div>
```

- Padre: `lg:col-span-2 grid grid-cols-4 gap-x-4` — el grid anidado vive en 50% desktop del grid madre.
- Children: cada input es `col-span-1` del grid anidado.
- Indicaciones: `lg:col-span-2` (50% desktop) en el grid madre, junto al grupo anidado.

**Anti-pattern:** ❌ crear grid de 4 cols separados para cada campo corto. Mejor un grid anidado si van juntos.

## Acciones de página al final del form

**Regla:** toda acción de formulario (Siguiente paso, Atrás, Saltar, Cancelar) se monta en una `<section>` con `<h2 class="sr-only">` que actúa como landmark.

```html
<section class="mt-base mb-base lg:mt-0 lg:mb-0" aria-labelledby="acciones-de-pagina-3">
  <h2 id="acciones-de-pagina-3" class="sr-only">Acciones de página</h2>
  <ul class="flex flex-wrap gap-sm">
    <li><button type="submit" class="c-button c-button--primary">Siguiente paso</button></li>
    <li><button class="c-button c-button--transparent">Saltar</button></li>
  </ul>
</section>
```

### Variantes de botón

| Variante | Cuándo | Ejemplo |
|---|---|---|
| `c-button c-button--primary` | Acción principal del form | Siguiente paso, Enviar, Guardar |
| `c-button c-button--transparent` | Acción secundaria contextual | Saltar, Cancelar paso actual |
| `c-button` | Acción neutra | Atrás, Volver |
| `c-button c-button--alert` | Acción destructiva | Eliminar, Rechazar (con confirmación modal previa) |

**Importante:** "Saltar" es `<button class="c-button c-button--transparent">`, NO un `<a>` pelado. La variante `--transparent` existe en el sistema de diseño para acciones secundarias.

### Layout de los botones

- `<ul class="flex flex-wrap gap-sm">` permite que los botones se reagrupen en mobile si no caben en una fila.
- Cada botón en su `<li>`.
- Orden: principal primero (a la izquierda del flujo natural), secundarios después.

### Spacing contextual

- **Mobile:** `mt-base mb-base` (separación clara entre la sección de acciones y el form).
- **Desktop:** `lg:mt-0 lg:mb-0` (sin márgenes, porque ya está en el grid flow).
- Patrón: `class="mt-base mb-base lg:mt-0 lg:mb-0"`.

## Spacing responsive entre bloques del form

Cuando el form tiene varias secciones (Datos personales, Domicilio, Ubicación, Acciones), el ritmo entre ellas cambia entre mobile y desktop:

```html
<section class="mt-base mb-base lg:mt-0 lg:mb-0">
  <!-- bloque de sección -->
</section>
```

| Breakpoint | Comportamiento | Razón |
|---|---|---|
| Mobile | `mt-base mb-base` | Sin grid, cada sección ocupa fila propia. Necesita margen para respirar. |
| Desktop (`lg+`) | `lg:mt-0 lg:mb-0` | En grid flow, el `gap-x-4` ya separó los items. Márgenes extra serían doble espaciado. |

**Regla:** aplica estos márgenes solo a los HIJOS del form (no al form raíz). El form raíz usa `my-base` o similar como separador con el resto de la página.

## Cuándo `lg:mt-0 lg:mb-0` SÍ y cuándo NO

El patrón `mt-base mb-base lg:mt-0 lg:mb-0` solo aplica cuando los inputs están **dentro de UN SOLO `<desy-input-group>` con fieldset padre** que envuelve varios grupos semánticos con grids internos (como el código oficial del Paso 3 — Domicilio). En ese caso, los grids comparten el mismo form-group padre y `lg:mt-0` en cada grid interno no afecta la separación entre grupos.

**NO apliques `lg:mt-0 lg:mb-0` cuando cada grupo semántico es su PROPIO `<desy-input-group>` separado.** En ese caso, `lg:mt-0` quita la separación visual entre los grupos en desktop y los inputs quedan pegados al input anterior.

### Cómo decidir

| Situación | ¿`lg:mt-0 lg:mb-0`? |
|---|---|
| **Un solo `<desy-input-group>`** con fieldset padre y grids internos | ✅ SÍ (el `lg:mt-0` no afecta entre grupos porque comparten form-group) |
| **Múltiples `<desy-input-group>` separados** (uno por grupo semántico) | ❌ NO — deja solo `mt-base mb-base` |
| **`<section>` de acciones al final del form** | ✅ SÍ — viene después del último grupo de inputs, no necesita margen extra |

### Anti-pattern

❌ Poner `lg:mt-0 lg:mb-0` en cada `<desy-input-group>` cuando son independientes. Resultado: en desktop, los labels del segundo grupo (Número, Código postal, Provincia...) quedan pegados al último input del grupo anterior, con 0px de separación visible.

❌ Asumir que `lg:mt-0` siempre es "mejor" porque "menos es más". En este contexto, separar `mt-base` (8px) entre grupos es la legibilidad correcta.

## Putting it together: estructura de wizard step

```html
<form action="proximo-paso.html">
  <div class="my-base">

    {# Botón volver (atrás) #}
    <a href="/" class="c-button c-button--transparent">
      <svg ...>←</svg>Volver
    </a>
  </div>

  {# Header del paso #}
  <div class="flex flex-col-reverse">
    <h1 id="page-title-3" class="c-h1 w-full">Dirección postal</h1>
    <p class="c-paragraph-base mb-0 text-neutral-dark">Paso 3 de 3</p>
  </div>

  {# Intro opcional #}
  <div class="grid lg:grid-cols-4 gap-x-4 mb-base">
    <div class="col-span-2 lg:col-span-3">
      <p class="-mt-base c-paragraph-base lg:c-paragraph-lg">
        Necesitamos estos datos para enviarte avisos puntuales sobre tus trámites y notificaciones.
      </p>
    </div>
  </div>

  {# Grupo 1: Domicilio #}
  <fieldset>
    <legend class="sr-only">Domicilio postal</legend>
    <div class="grid lg:grid-cols-4 gap-x-4">
      <!-- Tipo de vía (col-span-1) + Vía (col-span-3) -->
      <!-- Número/Escalera/Piso/Puerta (grid anidado) + Indicaciones -->
    </div>
  </fieldset>

  {# Grupo 2: Ubicación #}
  <fieldset>
    <legend class="sr-only">Ubicación</legend>
    <div class="grid lg:grid-cols-5 gap-x-4">
      <!-- CP (w-44 lg:w-full) + Provincia (col-span-2) + Municipio (col-span-2) -->
    </div>
  </fieldset>

  {# Checkbox legal #}
  <div class="c-form-group mt-base">
    <fieldset>
      <legend class="sr-only">Política de privacidad y protección de datos</legend>
      <div class="c-checkboxes" data-module="c-checkboxes">
        <!-- checkbox + label -->
      </div>
    </fieldset>
  </div>

  {# Acciones #}
  <section class="mt-base mb-base lg:mt-0 lg:mb-0" aria-labelledby="acciones-de-pagina-3">
    <h2 id="acciones-de-pagina-3" class="sr-only">Acciones de página</h2>
    <ul class="flex flex-wrap gap-sm">
      <li><button type="submit" class="c-button c-button--primary">Siguiente paso</button></li>
      <li><button class="c-button c-button--transparent">Saltar</button></li>
    </ul>
  </section>
</form>
```

**Notas finales:**
- Cada input individual usa los patrones de `w-full` / `lg:w-full` / `w-44 lg:w-full` documentados en `desy-implement-component` (PR paralelo).
- Los headings (H1, H2) dentro de grid también llevan `w-full`.
- Los párrafos intro pueden usar `col-span-*` para indicar columnas a ocupar en lugar de `w-full`.

## Otros patrones estructurales (no son forms)

Los patrones estructurales de maquetación aplican también a cards, cabeceras, listados, FAQs, errores, notificaciones. El skill `desy-implement-pattern` documenta **qué patrón de negocio** usar; este skill documenta **cómo estructurar la maquetación** cuando esos patrones se renderizan.

### Cabecera con skip-link (header pattern)

Convención oficial de DESY (ver `_pattern.cabecera-editar.njk` y `_pattern.cabecera-item.njk`):

```html
<header class="z-40 bg-white border-b border-neutral-base">
  <div class="container mx-auto px-base">
    <!-- headerSkipLinkBlock — SIEMPRE primero para accesibilidad -->
    <a href="#content" class="c-skip-link">Saltar al contenido principal</a>
    <!-- /headerSkipLinkBlock -->
    <div class="lg:flex lg:flex-wrap lg:w-full py-base">
      <div class="flex-1 mb-base lg:mb-0">
        <!-- headerTitleBlock -->
        <h1 class="c-h1">Título de la página</h1>
        <!-- /headerTitleBlock -->
      </div>
      <!-- headerActionsBlock -->
      <section aria-labelledby="acciones-de-cabecera">
        <h2 id="acciones-de-cabecera" class="sr-only">Menú de acciones</h2>
        <ul class="flex flex-wrap flex-col-reverse lg:flex-row-reverse gap-sm lg:items-center lg:ml-auto lg:pl-base">
          <li><button class="c-button c-button--primary c-button--sm">Guardar y salir</button></li>
          <li><button class="c-button c-button--sm">Guardar</button></li>
          <li><button class="c-button c-button--sm">Salir</button></li>
        </ul>
      </section>
      <!-- /headerActionsBlock -->
    </div>
  </div>
</header>
```

**Reglas:**

* `z-40` para que el header quede por encima del contenido scrollable.
* `border-b border-neutral-base` separa visualmente del main.
* `container mx-auto px-base` alinea el contenido al ancho del container de DESY.
* Skip-link **SIEMPRE PRIMERO** dentro del header (accesibilidad WCAG 2.4.1).
* Acciones a la derecha en desktop con `lg:ml-auto lg:pl-base`.

### Cards grid (misma altura)

Convención oficial de DESY (ver `_pattern.cards-misma-altura.njk`):

```html
<ul class="grid grid-cols-2 lg:grid-cols-4 content-stretch gap-base">
  <li>
    <article class="h-full p-base border border-neutral-base rounded-sm relative hover:bg-neutral-light">
      <h3 id="titulo-card-1" class="c-h3">
        <a href="#" class="c-link c-link--full">Servicios sociales</a>
      </h3>
      <div class="prose max-w-none mb-base">
        <p>Información de discapacidad, dependencia y hogares.</p>
      </div>
    </article>
  </li>
  <li>
    <article class="h-full p-base border border-neutral-base rounded-sm relative hover:bg-neutral-light">
      <h3 id="titulo-card-2" class="c-h3">
        <a href="#" class="c-link c-link--full">Oposiciones</a>
      </h3>
      <div class="prose max-w-none mb-base">
        <p>Consulta las próximas oposiciones.</p>
      </div>
    </article>
  </li>
  <!-- ... más cards ... -->
</ul>
```

**Reglas:**

* `<ul>` con `<li>` por cada card (semántica de lista).
* `grid-cols-2 lg:grid-cols-4` (mobile 2 cols, desktop 4 cols).
* `content-stretch gap-base` — `content-stretch` hace que los items del grid tengan la misma altura; `gap-base` separa las celdas.
* `h-full` en cada `<article>` para que el contenido crezca dentro del item.
* `border border-neutral-base rounded-sm` para card con borde sutil.
* `hover:bg-neutral-light` para feedback visual al pasar el ratón.
* `c-link c-link--full` en el `<a>` del título para que TODO el card sea clickable (no solo el texto).
* `prose max-w-none` para contenido con tipografía enriquecida.

### Error message (role="alert")

Convención oficial de DESY (ver `_pattern.errores-estaticos.njk` y `_pattern.errores-javascript.njk`):

```html
<div role="alert" class="border border-error-base bg-error-lighter rounded-sm p-base mb-base">
  <div class="flex items-start">
    <svg class="w-5 h-5 text-error-base mr-base flex-shrink-0" aria-label="Error" viewBox="0 0 140 140">
      <!-- icono de error (X o triángulo) -->
    </svg>
    <div class="flex-1">
      <h3 class="c-h3 text-error-base">Ha ocurrido un error</h3>
      <p class="c-paragraph-base mt-xs">No se ha podido procesar la solicitud. Inténtalo de nuevo.</p>
      <button class="c-button c-button--primary mt-base">Reintentar</button>
    </div>
  </div>
</div>
```

**Reglas:**

* `role="alert"` es **obligatorio** (live region — los screen readers lo anuncian automáticamente).
* `aria-labelledby` o `aria-label` en el icono SVG para accesibilidad.
* Color semántico: `text-error-base` y `bg-error-lighter` (o `bg-warning-lighter` para warnings).
* Icono + mensaje + acción correctiva (botón Reintentar, enlace Reportar error, etc.).

### Notification / toast (role="status")

Convención oficial de DESY (ver `_pattern.notificacion-identificado.njk`):

```html
<div class="c-notification c-notification--success mt-base" role="status" aria-live="polite">
  <div class="h-full mr-base">
    <svg class="w-5 h-5 text-success-dark" aria-label="Éxito" viewBox="0 0 140 140">
      <!-- icono de check -->
    </svg>
  </div>
  <div class="lg:flex flex-1 self-center">
    <div class="lg:flex-1 lg:self-center">
      <p id="notif-success-title" class="font-bold pr-base focus:outline-hidden focus:underline" tabindex="-1">
        El documento se ha cargado correctamente
      </p>
    </div>
    <div class="absolute top-0 right-0 p-sm">
      <button type="button" class="c-notification-button__close p-sm focus:bg-warning-base focus:border-warning-base focus:shadow-outline-black focus:text-black focus:outline-hidden" aria-label="Cerrar notificación">
        <svg class="w-4 h-4 pointer-events-none" viewBox="0 0 140 140" aria-hidden="true" role="presentation">
          <!-- icono de X -->
        </svg>
      </button>
    </div>
  </div>
</div>
```

**Reglas:**

* `role="status" aria-live="polite"` para notificaciones de éxito (no interrumpe al screen reader).
* `role="alert"` SOLO para errores que requieren atención inmediata.
* `c-notification c-notification--success` (o `--error`, `--warning`, `--info`) para variante visual.
* Botón de cerrar con `aria-label="Cerrar notificación"`.
* `tabindex="-1"` en el título para que screen readers puedan enfocarlo programáticamente.

### FAQs acordeón

Convención oficial de DESY (ver `_pattern.faqs-acordeon.njk`):

```html
<h2 class="c-h3">Preguntas frecuentes</h2>
<div class="c-accordion" data-module="c-accordion">
  <details>
    <summary>
      <h3 class="c-h4 flex-1">¿Qué hacer si surge un error?</h3>
      <svg class="w-4 h-4" aria-hidden="true"><!-- chevron --></svg>
    </summary>
    <div class="py-base">
      <p class="c-paragraph-base">Respuesta de la FAQ...</p>
    </div>
  </details>
  <details>
    <summary>
      <h3 class="c-h4 flex-1">¿Cómo dar permisos a una persona?</h3>
      <svg class="w-4 h-4" aria-hidden="true"><!-- chevron --></svg>
    </summary>
    <div class="py-base">
      <p class="c-paragraph-base">Otra respuesta...</p>
    </div>
  </details>
</div>
```

**Reglas:**

* Usar `<details>` + `<summary>` HTML nativo (sin JavaScript).
* `<h3>` dentro del `<summary>` para que screen readers anuncien correctamente.
* Chevron (SVG) al final del `<summary>` con `aria-hidden="true"` (decorativo).
* `allowMultiple` solo si la pregunta del usuario lo requiere (normalmente un solo acordeón abierto a la vez).
* Si necesitas un comportamiento más complejo (e.g. analítica de apertura), usa `componentAccordion` con JS.

## Convención de bloques `<!-- blockName -->`

En las páginas oficiales del sitio DESY, las secciones dentro de `<form>` o del layout principal están delimitadas por comentarios HTML con el formato `<!-- blockName -->` y `<!-- /blockName -->`. Esta convención es usada por el `markdown-generator` (script de `markdown-generator.config.js`) para extraer secciones al generar la documentación.

```html
<form>
  <!-- notificationHeaderBlock -->
  <!-- /notificationHeaderBlock -->

  <!-- contentBlock -->
  <fieldset>
    <legend class="sr-only">Datos de identidad</legend>
    <!-- contenido del grupo -->
  </fieldset>
  <!-- /contentBlock -->

  <!-- notificationFooterBlock -->
  <!-- /notificationFooterBlock -->
</form>
```

**Reglas:**

* Comentarios `<!-- blockName -->` y `<!-- /blockName -->` son **exactamente simétricos** (mismo `blockName`).
* El `blockName` sigue convención `kebab-case` y empieza con la categoría (e.g. `header`, `content`, `notification`, `actions`).
* Los bloques se usan para delimitar secciones que el markdown-generator puede extraer y documentar.
* Si tu proyecto no usa markdown-generator, la convención sigue siendo útil para organizar el HTML y hacer bloques claramente identificables.

## Anti-patterns estructurales (adicionales)

Además de los anti-patterns ya documentados al inicio:

❌ **`flex-column-reverse` (con guion).** Esta clase NO existe en Tailwind. Es un bug del repo oficial `gorilas/desy.aragon.es` presente en 5 archivos (e.g. `_pattern.acciones-de-cabecera.njk`). La clase correcta es `flex-col-reverse`. Si copias el código del repo tal cual, el patrón de acciones no funcionará en mobile. **Siempre reemplaza `flex-column-reverse` por `flex-col-reverse`** al implementar.

❌ **`<div>` con `role="group"` en lugar de `<fieldset>`.** Para agrupar inputs relacionados semánticamente, usa `<fieldset><legend>` (con legend sr-only si no debe verse). `role="group"` no es estándar y no lo reconoce screen readers consistentemente.

❌ **Skip-link fuera del header o como `<button>`.** Debe ser `<a href="#content">` dentro del `<header>` (o antes del `<main>`). Como `<button>` no funciona porque no tiene href.

❌ **Cards con altura fija (`height: 200px`) en lugar de `h-full`.** Las cards en grid deben tener `h-full` para que igualen altura con las demás. Altura fija rompe en mobile y con contenido variable.

❌ **Notificaciones sin `role="status"` o `role="alert"`.** Sin live region, los screen readers no anuncian el cambio. Errores usan `role="alert"`, éxitos/información usan `role="status"`.

❌ **Botón cerrar notificación sin `aria-label`.** El botón X debe tener `aria-label="Cerrar notificación"` porque solo tiene icono (sin texto).

❌ **Cards grid usando `<div>` en lugar de `<ul>/<li>`.** La semántica de lista es importante para screen readers y navegación por items. Usa `<ul>` para el contenedor y `<li>` para cada card.

## Related

- **Skill: `desy-implement-component`** — sección "Ancho de inputs, selects y textareas en grid (patrón w-full)" para los 4 patrones de ancho que aplican aquí
- **Skill: `desy-implement-pattern`** — para implementar uno de los 55 patrones de negocio (cards, FAQs, errores, headers, listados, megamenu, soporte, cookies, pagination). Complementario: este skill (layout-patterns) define las convenciones ESTRUCTURALES que esos patrones usan.
- **Skill: `desy-validate-accessibility`** — para auditar el fieldset+legend sr-only, los landmarks y la jerarquía de headings tras aplicar estos patrones
- **Skill: `desy-styles-reference`** — para tokens concretos (`mt-base`, `mb-base`, `gap-x-4`, `lg:grid-cols-4`)
- **Skill: `desy-scaffold-project`** — para crear el proyecto donde va este form (paso previo)
- **Catálogo:** https://desy.aragon.es/patrones.html
- **Ejemplo gold verificado:** wizard del Paso 3 (Dirección postal) en https://desy.aragon.es/patrones.html
