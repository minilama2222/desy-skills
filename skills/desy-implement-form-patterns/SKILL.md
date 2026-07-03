---
name: desy-implement-form-patterns
description: DESY form grouping patterns: fieldset+legend, responsive grids, action sections. Use for wizard steps or multi-section forms.
---

# desy-implement-form-patterns

Patrones estructurales para montar formularios DESY: agrupación semántica (`fieldset`+`legend`), grids responsivos para campos, acciones de página, spacing contextual. Complementa a `desy-implement-component` (que cubre componentes individuales).

**Hallazgo 2026-07-03 (test del wizard Paso 3 - Dirección postal):** El output del skill `desy-implement-component` por sí solo produce inputs coherentes pero sin agrupación semántica ni estructura responsive de grid. Este skill añade la capa estructural que falta.

## When to use this skill

- Te piden una página de formulario completa (wizard, formulario de edición, alta de datos)
- Vas a montar varios inputs en una grid y necesitas saber qué grid usar
- Necesitas agrupar inputs por sección semántica (Domicilio, Ubicación, etc.) con fieldset+legend
- Tienes acciones al final del form (Siguiente, Atrás, Saltar, etc.) y necesitas el patrón de section+ul
- Necesitas saber cuándo aplicar `mt-base mb-base lg:mt-0 lg:mb-0` vs nada

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

## Related

- **Skill: `desy-implement-component`** — sección "Ancho de inputs, selects y textareas en grid (patrón w-full)" para los 4 patrones de ancho que aplican aquí
- **Skill: `desy-validate-accessibility`** — para auditar el fieldset+legend sr-only, los landmarks y la jerarquía de headings tras aplicar estos patrones
- **Skill: `desy-styles-reference`** — para tokens concretos (`mt-base`, `mb-base`, `gap-x-4`, `lg:grid-cols-4`)
- **Skill: `desy-scaffold-project`** — para crear el proyecto donde va este form (paso previo)
- **Catálogo:** https://desy.aragon.es/patrones.html
- **Ejemplo gold verificado:** wizard del Paso 3 (Dirección postal) en https://desy.aragon.es/patrones.html
