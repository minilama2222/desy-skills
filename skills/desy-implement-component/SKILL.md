---
name: desy-implement-component
description: "Generate copy-pasteable DESY component code in desy-html, desy-angular, or desy-ionic. Use when implementing a specific component with given requirements."
---

# desy-implement-component

Genera código copy-pasteable para un componente DESY concreto en la librería adecuada, con los parámetros que pida el equipo, garantizando accesibilidad WCAG 2.2 AA.

## Regla fundamental (lee esto antes de implementar)

> **Antes de generar ningún componente, confirma que el proyecto es un starter DESY clonado (`desy-html-starter`, `desy-angular-starter` o `desy-ionic`). Si no lo es, este skill no aplica — primero hay que aplicar `desy-scaffold-project` para clonar el starter y dejarlo listo.**

Razón: este skill trabaja **dentro** de un proyecto DESY (sobre la estructura de directorios, los macros de la librería, las convenciones de build del starter). Implementar componentes sin un starter DESY como base produce HTML/TSX/Angular que NO se compila con la toolchain oficial, NO usa los macros reales, y genera un output inconsistente con cualquier proyecto DESY real.

**Antes de aplicar estilos visuales (colores, espaciado, tipografía), consulta también `desy-styles-reference`** para conocer los tokens del proyecto (`bg-primary-base`, `p-base`, `c-h1`, etc.) y evitar inventar utility classes con valores por defecto de Tailwind. La combinación de macros (este skill) + tokens (`desy-styles-reference`) es lo que produce un output visualmente fiel al gold.

Si te piden "hazme una página X" y no estás en un starter DESY:
1. Aplica primero `desy-scaffold-project` (clonar el starter adecuado, `npm install`)
2. Verifica que `node_modules/<librería>` existe y que `npm run build` produce un `dist/`
3. **Ahora** aplica este skill para generar el componente o página dentro de ese proyecto
4. El output final debe ser el `dist/` compilado, no HTML suelto

## When to use this skill

- El equipo sabe QUÉ componente necesita (ej: "un botón de enviar", "una tabla con paginación", "un modal de confirmación")
- El equipo ya tiene claro en qué librería va a trabajar (desy-html / desy-angular / desy-ionic)
- Se necesita el código listo para pegar con los parámetros concretos
- El equipo quiere verificar la accesibilidad de un componente antes de mergear

## Inputs que necesitas pedir

Antes de generar código, confirma con el equipo:

1. **Componente** (nombre exacto o descripción visual)
2. **Librería** (desy-html / desy-angular / desy-ionic)
3. **Parámetros clave:**
   - Texto / label
   - Variante (primary, secondary, danger, etc.) si aplica
   - Estado (default, disabled, loading, active, error)
   - Atributos ARIA / accesibilidad (si hay requisitos especiales)
   - Icono (si lo lleva, qué icono Streamline)
   - Link o acción (href, routerLink, onClick)
   - Para formularios: name, id, label asociado, validación
4. **Contexto de uso:**
   - ¿Está dentro de un formulario?
   - ¿Necesita preventDoubleClick?
   - ¿Es parte de un patrón conocido? (ej: acciones de tabla → ver `patrones-acciones-tabla`)

## Clases tipográficas de DESY (usar SIEMPRE, nunca utility classes Tailwind)

**Regla fundamental:** para tipografía en un proyecto DESY, usa las **clases semánticas de la librería**, NUNCA utility classes Tailwind como `text-3xl font-semibold` o `text-base leading-normal`. Las clases de la librería encapsulan el tipo, peso, tamaño, interlineado y color que el sistema de diseño ha definido como coherentes con el resto del proyecto.

### Catálogo (verificado en `node_modules/desy-html/src/css/styles.css` y usado en plantillas oficiales)

| Elemento | Clase | Notas |
|---|---|---|
| Título principal de página | `c-h1` | Una sola por página (el H1 visible). En otras plantillas, los H2 visuales también llevan `c-h1` (la jerarquía visual no siempre coincide con la jerarquía DOM) |
| Subtítulo | `c-h2` | Para secciones de segundo nivel |
| Encabezado menor | `c-h3` | Para sub-secciones |
| Encabezado auxiliar | `c-h4` | Rara vez, para tarjetas o items |
| Párrafo estándar | `c-paragraph-base` | El default para `<p>` |
| Párrafo destacado (lead) | `c-paragraph-lead` | Para introductorio bajo el H1 |
| Párrafo pequeño | `c-paragraph-sm` | Para notas, hints, metadatos |

### Combinaciones habituales (vistas en `src/plantilla-editar-con-cabecera-fija-y-sidebar-sticky.html`)

- `<h2 class="c-h1 c-anchor-scroll-edit">Sección</h2>` — H2 con estilo de H1 y ancla editable
- `<p class="c-paragraph-base mb-0">` — párrafo estándar sin margen inferior
- `<p class="c-paragraph-base">` — párrafo estándar con margen inferior

### Reglas prácticas

1. **Un H1 con `c-h1` por página** (o un H2 con `c-h1` si la jerarquía visual lo requiere)
2. **Párrafos siempre con `c-paragraph-base`** o `c-paragraph-lead` si es intro
3. **NO** usar `text-*`, `font-*`, `leading-*` para tipografía — son la antítesis del sistema de diseño
4. **Excepción:** spacing (`mb-base`, `mt-sm`) y color contextual (`text-primary-base` para acentos) sí se pueden aplicar como utility classes encima de las `c-*`

### Por qué importa (lección del benchmark 2026-06-07)

Un agente que produce tipografía con utility classes Tailwind produce un output que **se ve coherente técnicamente** (estructura, ARIA, macros) pero **roto visualmente** — el h1 se ve más pequeño que el del gold, los párrafos tienen interlineado distinto, los acentos cromáticos no aparecen. La comparativa semántica pasa (es "Aceptable"), pero la visual falla.

## Workflow

### Paso 1: Identifica la URL del ejemplo "copia y pega"

Usa la tabla de mapeo de la sección **Mapeo de componentes** más abajo. Cada componente tiene su URL canónica en la documentación. Hay 3 formatos:
- **HTML / Nunjucks (desy-html):** `https://desy.aragon.es/componente-<nombre>-codigo.html.md`
- **Angular (desy-angular):** `https://desy.aragon.es/angular-md/demo-<nombre>.md`
- **Ionic (desy-ionic):** Storybook en `https://desy.aragon.es/desy-ionic` o repo en Bitbucket

### Paso 2: Lee el ejemplo oficial

`web_fetch` la URL del ejemplo. La doc viene con:
- Descripción visual
- Parámetros del componente (YAML en desy-html, tabla de inputs/outputs en desy-angular)
- Ejemplo en macro Nunjucks y HTML (desy-html) o código TS + template (desy-angular)
- Múltiples variantes (estados, tamaños)

### Paso 3: Adapta los parámetros

Copia el ejemplo y sustituye los parámetros con los del equipo. Mantén:
- Las clases CSS oficiales (utility classes de Tailwind en desy-html, components en desy-angular)
- Los atributos ARIA del ejemplo (son obligatorios para accesibilidad)
- La estructura semántica del HTML (no sustituir `<button>` por `<div>`)

### Paso 4: Verifica accesibilidad (CRÍTICO)

Comprueba el [checklist de accesibilidad](#checklist-de-accesibilidad-wcag-22-aa) más abajo. Si algo falla, corregir antes de devolver el código.

### Paso 5: Genera el snippet final

Devuelve el código en un bloque con el lenguaje correcto (`html`, `typescript`, `angular`, `ionic`). Indica también:
- Archivo donde va (ruta en el proyecto)
- Props de TypeScript si es Angular/Ionic
- Dependencias a importar
- Notas de uso (restricciones, combinaciones)

## Mapeo de componentes (subset crítico)

Las URLs siguen el patrón: `https://desy.aragon.es/componente-<nombre>-codigo.html.md` para HTML y `https://desy.aragon.es/angular-md/demo-<nombre>.md` para Angular.

### Componentes principales (obligatorios)

| Componente | URL HTML | URL Angular | Notas |
|---|---|---|---|
| **Button** | `componente-botones-codigo.html.md` | `angular-md/demo-button.md` | 4 variantes (default/primario/transparente/alerta), 3 tamaños, estados (default/loading/success) |
| **Header (webapp)** | `componente-cabeceras-app-codigo.html.md` | `angular-md/demo-header.md` | Cabecera estándar 1 banda, 56px alto |
| **Header-mini (parte de advanced)** | `componente-cabeceras-mini-codigo.html.md` | `angular-md/demo-header-mini.md` | Banda de 45px, obligatoria en portales |
| **Header-advanced (portal)** | `componente-cabeceras-codigo.html.md` | `angular-md/demo-header-advanced.md` | 3 bandas + hero opcional |
| **Footer** | `componente-footer-codigo.html.md` | `angular-md/demo-footer.md` | 5 variantes de financiación UE (FEDER/FEADER/FSE+/Plurifondo/Sólo UE) |
| **Skip-link** | `componente-cabeceras-skiplink-codigo.html.md` | `angular-md/demo-skip-link.md` | Obligatorio para accesibilidad en cada cabecera |

### Formularios

| Componente | URL HTML | URL Angular |
|---|---|---|
| **Input text** | `componente-input-text-codigo.html.md` | `angular-md/demo-input.md` |
| **Input fieldset** | `componente-input-text-fieldset-codigo.html.md` | — |
| **Textarea** | `componente-textarea-codigo.html.md` | `angular-md/demo-textarea.md` |
| **Selector** | `componente-selector-codigo.html.md` | `angular-md/demo-select.md` |
| **File upload** | `componente-file-upload-codigo.html.md` | `angular-md/demo-file-upload.md` |
| **Datepicker** | `componente-datepicker-codigo.html.md` | `angular-md/demo-datepicker.md` |
| **Radio** | `componente-radios-codigo.html.md` | `angular-md/demo-radios.md` |
| **Checkbox** | `componente-checkboxes-codigo.html.md` | `angular-md/demo-checkboxes.md` |
| **Tree** | `componente-tree-codigo.html.md` | `angular-md/demo-tree.md` |
| **Bloques de datos** | `componente-bloques-de-datos-codigo.html.md` | — |
| **Label** | `componente-label-codigo.html.md` | `angular-md/demo-label.md` |
| **Pista (hint)** | `componente-pista-codigo.html.md` | `angular-md/demo-hint.md` |
| **Mensaje de error** | `componente-mensaje-error-codigo.html.md` | `angular-md/demo-error-message.md` |

### Datos y avisos

| Componente | URL HTML | URL Angular |
|---|---|---|
| **Tabla simple** | `componente-tabla-simple-codigo.html.md` | `angular-md/demo-table.md` |
| **Tabla avanzada** | `componente-tabla-simple-codigo.html.md` (filtros/ordenación) | `angular-md/demo-table-advanced.md` |
| **Tabla con árbol** | `componente-tabla-con-arbol-codigo.html.md` | `angular-md/demo-table-tree.md` |
| **Item** | `componente-item-codigo.html.md` | `angular-md/demo-item.md` |
| **Item de estado** | `componente-status-codigo.html.md` | `angular-md/demo-status.md` |
| **Listado descripciones** | `componente-description-list-codigo.html.md` | `angular-md/demo-description-list.md` |
| **Píldoras** | `componente-pills-codigo.html.md` | `angular-md/demo-pill.md` |
| **Modal** | `componente-modal-codigo.html.md` | `angular-md/demo-modal.md` |
| **Modal dialog** | `componente-modal-dialog-codigo.html.md` | — |
| **Notificaciones** | `componente-notificaciones-codigo.html.md` | `angular-md/demo-notification.md` |
| **Resumen de errores** | `componente-error-summary-codigo.html.md` | `angular-md/demo-error-summary.md` |
| **Card** | `componente-card-codigo.html.md` | `angular-md/demo-card.md` |
| **Spinner** | `componente-spinner-codigo.html.md` | `angular-md/demo-spinner.md` |

### Navegación y mostrar/ocultar

| Componente | URL HTML | URL Angular |
|---|---|---|
| **Barra de búsqueda** | `componente-searchbar-codigo.html.md` | `angular-md/demo-search-bar.md` |
| **Listado de enlaces** | `componente-links-list-codigo.html.md` | `angular-md/demo-links-list.md` |
| **Menú de navegación** | `componente-menu-navigation-codigo.html.md` | `angular-md/demo-menu-navigation.md` |
| **Menú horizontal** | `componente-menu-horizontal-codigo.html.md` | `angular-md/demo-menu-horizontal.md` |
| **Menú vertical** | `componente-menu-vertical-codigo.html.md` | `angular-md/demo-menu-vertical.md` |
| **Migas de pan** | `componente-breadcrumbs-codigo.html.md` | `angular-md/demo-breadcrumbs.md` |
| **Paginación** | `componente-paginacion-codigo.html.md` | `angular-md/demo-pagination.md` |
| **Acordeón** | `componente-acordeon-codigo.html.md` | `angular-md/demo-accordion.md` |
| **Acordeón histórico** | `componente-acordeon-historico-codigo.html.md` | `angular-md/demo-accordion-historic.md` |
| **Barra de menús** | `componente-menubar-codigo.html.md` | `angular-md/demo-menubar.md` |
| **Desplegable** | `componente-dropdown-codigo.html.md` | `angular-md/demo-dropdown.md` |
| **Detalles** | `componente-detalles-codigo.html.md` | `angular-md/demo-details.md` |
| **Globo de ayuda (tooltip)** | `componente-tooltip-codigo.html.md` | `angular-md/demo-tooltip.md` |
| **Interruptor (toggle)** | `componente-toggle-codigo.html.md` | `angular-md/demo-toggle.md` |
| **Pestañas (tabs)** | `componente-tabs-codigo.html.md` | `angular-md/demo-tabs.md` |

> Para el **catálogo completo** y componentes no listados: `https://desy.aragon.es/componentes.html.md`

## Checklist de accesibilidad WCAG 2.2 AA

Aplica a cada componente que generes:

### General
- [ ] **Landmarks presentes:** `<header>`, `<nav>`, `<main>`, `<footer>` en la página
- [ ] **Skip-link** en cada cabecera (salta a `<main>`)
- [ ] **Foco visible** siempre (no `outline: none` sin alternativa)
- [ ] **No `<br>` para espaciado** (usar margins)
- [ ] **Unidades `rem`** (no `px` absolutos)
- [ ] **No tablas para maquetación**
- [ ] **No widgets externos de accesibilidad** (lectores de pantalla incrustados, etc.)

### Botones
- [ ] Elemento `<button>` (no `<div>` ni `<a>` salvo que enlace)
- [ ] Etiqueta clara (verbo en infinitivo, 1-2 palabras, no mayúsculas)
- [ ] Si lleva icono + texto: `aria-hidden=true` en SVG, texto describe la acción
- [ ] Si lleva solo icono: `role=img` + `aria-label` que describe la acción
- [ ] Si `target=_blank`: atributo `title` avisando

### Inputs / Formularios
- [ ] `<label>` visible y único, apunta al `id` del input
- [ ] `id` único por input
- [ ] `name` para envío del formulario
- [ ] `autocomplete` cuando aplique (navegador puede autocompletar)
- [ ] `type` correcto (`text`, `email`, `tel`, `date`, etc.)
- [ ] Si tiene hint: `<p id="hint">` + `aria-describedby` en el input
- [ ] Si tiene error: `<p id="error">` con `<span class="sr-only">Error:</span>` + `aria-errormessage` en el input + `aria-invalid=true`
- [ ] Foco al error-summary al submit con errores
- [ ] `<form>` con `aria-label` o `aria-labelledby`

### Tablas
- [ ] `<table role=grid>` con `<caption>` (visible o sr-only)
- [ ] `<thead>`, `<tbody>`, `<tfoot>` separados
- [ ] `<th scope=col|row>`, `tabindex=-1` en cabeceras
- [ ] `aria-sort` en columnas ordenables
- [ ] Navegación con flechas entre celdas
- [ ] En anchuras pequeñas: scroll horizontal + caption siempre visible

### Modales
- [ ] `role=dialog`, `aria-modal=true`, `aria-labelledby` al título
- [ ] Foco atrapado dentro del modal
- [ ] Esc cierra el modal
- [ ] Click fuera del contenedor cierra el modal
- [ ] Icono de cierre con `aria-label`
- [ ] Variante destructiva: botón principal a la derecha, color `alert`

### Imágenes
- [ ] `alt` descriptivo (o `alt=""` si decorativa)
- [ ] Si SVG personalizado: `role=img` + `aria-label`

### Iconos
- [ ] Si acompañan texto: `aria-hidden=true` (el texto ya describe la acción)
- [ ] Si van solos: `role=img` + `aria-label` que describa la acción, no el icono

### Contraste
- [ ] Texto sobre fondo blanco: usar colores `neutral-base` o más oscuros
- [ ] Texto sobre colores `base` (botones): solo permitido si peso semibold y ≥16px
- [ ] Texto sobre colores `light`: en mensajes de estado, no en texto principal

## Examples

### Ejemplo 1: Botón "Enviar" en desy-angular

**Input del equipo:**
- Componente: Button
- Librería: desy-angular
- Texto: "Enviar"
- type: submit
- preventDoubleClick: true
- disabled dinámico: `formulario.invalid`

**Snippet generado (template):**

```html
<desy-button
  [type]="'submit'"
  [text]="'Enviar'"
  [disabled]="formulario.invalid"
  [preventDoubleClick]="true"
  (clickEvent)="onSubmit()">
</desy-button>
```

```typescript
// app/formulario.component.ts
import { Component } from '@angular/core';
import { DesyButtonComponent } from 'desy-angular';

@Component({
  selector: 'app-formulario',
  standalone: true,
  imports: [DesyButtonComponent, ReactiveFormsModule],
  templateUrl: './formulario.component.html',
})
export class FormularioComponent {
  formulario = this.fb.group({ /* ... */ });
  constructor(private fb: FormBuilder) {}
  onSubmit() { /* lógica */ }
}
```

**Accesibilidad verificada:**
- ✅ Elemento `<desy-button>` renderiza `<button type="submit">`
- ✅ `aria-disabled` automático cuando `disabled=true`
- ✅ `preventDoubleClick` evita doble submit
- ✅ El texto describe la acción ("Enviar")
- ✅ Contraste OK (variant default)

### Ejemplo 2: Tabla con acciones en lote en desy-html (patrón `acciones-de-tabla`)

**Input del equipo:**
- Pantalla: webapp con lista de expedientes
- Componente: Tabla + acciones en lote
- Librería: desy-html
- Patrón: `acciones-de-tabla` (no reinventar)

**Snippet generado (macro):**

```njk
{% from "components/checkboxes/_macro.checkboxes.njk" import componentCheckboxes %}
{% from "components/details/_macro.details.njk" import componentDetails %}
{% from "components/menubar/_macro.menubar.njk" import componentMenubar %}

{# Instrucciones de funcionamiento de la tabla #}
{% call componentDetails({
  "summary": { "html": "Acerca de esta tabla" },
  "classes": "mb-xs text-sm"
})  %}
    <div id="descTableExpedientes" class="grid gap-sm">
      <p>En la primera columna es posible seleccionar uno o más expedientes. Puedes seleccionar todos con la casilla "Seleccionar todo".</p>
      <p>La segunda columna contiene enlaces al detalle del expediente.</p>
      <p>Las cabeceras tienen opción de ordenación.</p>
      <p>Puedes realizar acciones sobre los expedientes seleccionados con los botones superiores.</p>
    </div>
{% endcall %}

{# Barra de Acciones #}
<section class="flex flex-col lg:flex-row lg:flex-wrap lg:w-full" aria-labelledby="acciones-expedientes">
  <h3 id="acciones-expedientes" class="sr-only">Selección múltiple y Acciones sobre la tabla de expedientes</h3>
  <div class="lg:flex sm:flex-1">
    <form action="#">
      {{ componentCheckboxes({
        "idPrefix": "todos-expedientes",
        "name": "todos-expedientes",
        "classes": "c-checkboxes--sm mt-sm -mb-xl ml-base",
        "items": [{
          "value": "todas",
          "text": "Seleccionar todo",
          "label": { "classes": "text-sm -mt-1" }
        }]
      }) }}
    </form>
  </div>
  <div class="flex lg:items-start lg:ml-auto lg:pl-base order-first lg:order-last">
    {{ componentMenubar({
      "id": "actions-expedientes-menubar",
      "ariaLabel": "Acciones sobre los expedientes seleccionados",
      "items": [
        { "text": "Aceptar", "id": "actions-exp-aceptar", "href": "#", "classes": "c-menubar__button--sm mb-sm mr-sm" },
        { "text": "Archivar", "id": "actions-exp-archivar", "href": "#", "classes": "c-menubar__button--sm mb-sm mr-sm" },
        { "text": "Reenviar", "id": "actions-exp-reenviar", "href": "#", "classes": "c-menubar__button--sm mb-sm mr-sm", "sub": {
          "items": [{ "role": "menuitem", "text": "A una bandeja personal" }, { "role": "menuitem", "text": "A un organismo" }],
          "attributes": { "aria-labelledby": "actions-exp-reenviar" }
        }}
      ]
    }) }}
  </div>
</section>

{# Tabla #}
{# Aquí iría la tabla con las columnas y filas #}
```

**Accesibilidad verificada:**
- ✅ `<details>` con summary focuseable (skip-link a instrucciones de la tabla)
- ✅ `<section aria-labelledby="acciones-expedientes">` con `<h3 class="sr-only">`
- ✅ Checkbox "Seleccionar todo" con label visible y `aria-label` único
- ✅ Menubar con `ariaLabel` y submenús con `role=menuitem`
- ✅ Tabla con `role=grid`, `aria-sort` en columnas ordenables, navegación por teclado

### Ejemplo 3: Modal de confirmación destructiva en desy-ionic

**Input del equipo:**
- Componente: Modal
- Librería: desy-ionic
- Tipo: Destructiva (botón "Eliminar" con color alert)
- Título: "¿Eliminar este expediente?"
- Cuerpo: "Esta acción no se puede deshacer. Se eliminarán también todos los documentos asociados."

**Snippet generado:**

```html
<ion-modal [isOpen]="isModalOpen" (didDismiss)="cerrarModal()">
  <ng-template>
    <ion-header>
      <ion-toolbar>
        <ion-title>¿Eliminar este expediente?</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <p>Esta acción no se puede deshacer. Se eliminarán también todos los documentos asociados.</p>
      <div class="ion-text-end">
        <ion-button fill="clear" (click)="cerrarModal()">Cancelar</ion-button>
        <ion-button color="danger" (click)="confirmarEliminar()">Eliminar</ion-button>
      </div>
    </ion-content>
  </ng-template>
</ion-modal>
```

**Accesibilidad verificada:**
- ✅ `role=dialog`, `aria-modal=true` (automático en `ion-modal`)
- ✅ Título claro que describe la acción a confirmar
- ✅ Foco atrapado en el modal
- ✅ Esc cierra el modal
- ✅ Botón destructivo (`color="danger"`) a la derecha
- ✅ Botón secundario (`fill="clear"`) a la izquierda

## Gotchas

- **No inventar nombres de props.** Si un prop no aparece en la tabla oficial, pregunta al equipo o consulta la URL de la demo. Un prop mal nombrado pasa el compile pero no funciona.
- **El output NO es HTML estático, es Nunjucks que se compila con Vite.** Cuando trabajas con `desy-html`, las páginas son archivos `.njk` (Nunjucks) en `src/templates/pages/`, y los componentes se invocan como **macros** (`{% from "components/<x>/_macro.<x>.njk" import componentX %}` + `{{ componentX({...params}) }}`). El HTML final que ve el navegador es el resultado de `npm run build`, no el `.njk` literal. Si el agente genera HTML estático con clases DESY, **NO es el flujo correcto** — está imitando, no usando la librería. Esto fue un fallo crítico del benchmark 2026-06-07: el agente generó HTML estático en lugar de Nunjucks + macros.
- **Si te piden una PÁGINA COMPLETA (no un componente suelto), primero clona el starter o trabaja dentro de uno.** Pasos: (1) `git clone https://bitbucket.org/sdaragon/desy-html-starter.git` a un dir temporal, (2) `npm install` para tener la librería `desy-html` en `node_modules/`, (3) generar el `.njk` en `src/templates/pages/`, (4) `npm run build` para compilar, (5) servir el `dist/` resultante. Revisa la sección `## Estructura de directorios del proyecto (modelo librería/starter/build)` de `desy-scaffold-project` para paths reales.
- **El CSS que recibe el navegador es CSS compilado del proyecto, no de la librería.** Tailwind 4 escanea el proyecto y solo incluye las clases USADAS. Si el agente inventa una clase que no se usa en Nunjucks, no aparecerá en el CSS compilado y la página se verá rota. Paths inventados (observados en benchmarks con IA) que NO debes usar: `/assets/css/main.css`, `/assets/img/logo-X.svg`. Paths reales: `src/css/styles.css`, `public/images/<archivo>`, inline SVG para logos.
- **No saltarse atributos ARIA.** DESY los incluye por defecto en sus ejemplos. Si los quitas, rompes accesibilidad.
- **En Angular/Ionic, importar el componente.** Olvidar el import en `imports: []` es el error más común.
- **En desy-html, usar `params.classes` del macro Nunjucks, no escribir `class="..."` en el HTML directamente.**
- **No mezclar librerías.** Un proyecto no debería tener desy-html y desy-angular al mismo tiempo para el mismo componente.
- **El `autocomplete` no es opcional.** Es accesibilidad: el navegador autocompleta, el usuario no tiene que recordar. Usar `autocomplete="email"`, `autocomplete="tel"`, `autocomplete="postal-code"`, etc.
- **Las acciones destructivas SIEMPRE piden confirmación modal.** No usar toast ni notificación — el usuario debe confirmar conscientemente.

## Related

- **Skill: `desy-choose-library`** — paso anterior, qué librería usar
- **Skill: `desy-scaffold-project`** — paso siguiente, setup del proyecto
- **Catálogo completo:** `https://desy.aragon.es/componentes.html`
- **Patrones:** `https://desy.aragon.es/patrones.html`
- **Versiones:** `https://desy.aragon.es/desarrollo-versiones.html` (qué versión de desy-html corresponde a cada versión de desy-angular)
- **Mapa del ecosistema DESY:** [`/docs/ecosystem-map.md`](../../docs/ecosystem-map.md) (en este repo)
- **Accesibilidad WCAG 2.2:** `https://www.w3.org/TR/WCAG22/`
- **W3C ARIA Authoring Practices:** `https://www.w3.org/WAI/ARIA/apg/`
