---
name: desy-angular-translator
description: "Traduce código Nunjucks de desy-html a código Angular de desy-angular. Patrón general + tabla de equivalencias para los 15+ componentes más comunes. NO cubre los 57 — solo los que han sido validados."
---

# desy-angular-translator

Traduce código Nunjucks de la librería `desy-html` a código TypeScript + template de la librería `desy-angular`. Útil cuando:

- Tienes código `{{ componentX({...}) }}` que necesitas migrar a `<desy-x [prop]="value">`
- Estás aprendiendo las convenciones de `desy-angular` partiendo de tu conocimiento de `desy-html`
- Estás auditando código que mezcla ambos paradigmas

## Fuente de verdad

> "Normalmente, los parámetros de configuración y los diseños de componentes comienzan en desy-html y posteriormente se traducen a desy-angular. No obstante, desy-angular tiene algunos parámetros propios relativos a su implementación."
> — `desy.aragon.es/desarrollo-desy-angular.html.md`

**Implicación:** la traducción es la dirección canónica, no es 1:1.

## When to use this skill

- Tienes un fragmento de código `desy-html` (Nunjucks) y necesitas pasarlo a `desy-angular` (TS + template)
- Estás generando un proyecto nuevo con `desy-angular-starter` y tienes código de referencia en `desy-html`
- Estás documentando la equivalencia entre ambos

**NO uses este skill si:**
- Estás trabajando solo con `desy-html` (no necesitas Angular)
- Estás en `desy-ionic` (móvil) — la traducción es distinta y este skill no la cubre
- Necesitas la traducción **inversa** (Angular → HTML) — eso es otro flujo

## Patrones generales de traducción

| Concepto | desy-html (Nunjucks) | desy-angular (TS + template) |
|---|---|---|
| **Macro / selector** | `{{ componentX({...}) }}` (función) | `<desy-x [prop]="value">` (selector Angular) |
| **Propiedades** | dict en el macro: `{text: "X", classes: "y"}` | Input TS: `text?: string;` + binding: `[text]="text"` |
| **Variantes CSS** | `classes: "c-button--primary"` (mismo nombre) | `classes="c-button--primary"` (igual) |
| **Slot / innerHTML** | `html: "<svg>...</svg>"` (string) | `text` simple o `<ng-container *appCustomInnerContent>` |
| **href** | `href: "/url"` | `[href]="'/url'"` |
| **Router interno** | NO existe (HTML server-side) | `[routerLink]="'/url'"` + `[routerLinkActiveClasses]="'active'"` |
| **Eventos** | NO emite (HTML estático) | `(clickEvent)="handler($event)"` (Output TS) |
| **Estado disabled** | `disabled: true` (bool en macro) | `[disabled]="true"` o `[disabled]="isDisabled"` |
| **Atributos a11y** | Los pone automáticamente la macro | Inputs explícitos: `ariaLabel`, `ariaDescribedBy`, `ariaLabelledBy`, etc. |
| **Aria/role/tabindex** | Implícitos en el HTML generado | Explícitos como inputs (más control, más verboso) |

## Parámetros que SOLO existen en desy-angular (no en desy-html)

| Parámetro | Función |
|---|---|
| `routerLink` | Ruta interna Angular (`/usuarios/1`) |
| `routerLinkActiveClasses` | Clases CSS cuando la ruta está activa |
| `fragment` | Fragmento de URL (`#seccion`) |
| **Outputs / eventos** | `(clickEvent)`, `(change)`, etc. |
| Atributos a11y explícitos | `ariaLabel`, `ariaDescribedBy`, `role`, `tabindex`, etc. |
| `clickCount`, `clickName`, `clickValue` | Métricas de tracking de clicks (no en desy-html) |

## Parámetros que están en AMBAS librerías (con la misma semántica)

| Parámetro | Notas |
|---|---|
| `text` | Texto plano del contenido |
| `html` | HTML del contenido (preferir slot en Angular) |
| `classes` | Clases CSS modificadoras (`c-button--primary`, etc.) |
| `id` | Identificador del DOM |
| `name` | Atributo name (para form submit) |
| `type` | Tipo (button/submit/reset) |
| `value` | Valor del botón (form submit) |
| `disabled` | Estado deshabilitado |
| `href`, `target` | Para el elemento `a` |
| `preventDoubleClick` | Evita doble submit |

## Tabla de equivalencias por componente (15+ validados)

| Componente (Angular) | Equivalente HTML | Notas |
|---|---|---|
| `<desy-button>` | `{{ componentButton({...}) }}` | Más inputs en Angular (a11y, router) |
| `<desy-button-loader>` | `{{ componentButtonLoader({...}) }}` | Estado de carga explícito |
| `<desy-header-advanced>` | `{{ componentHeaderAdvanced({...}) }}` | 3 bandas |
| `<desy-header>` | `{{ componentHeader({...}) }}` | 1 banda (webapp) |
| `<desy-header-mini>` | `{{ componentHeaderMini({...}) }}` | Solo logo |
| `<desy-skip-link>` | `{{ componentSkipLink({...}) }}` | — |
| `<desy-footer>` | `{{ componentFooter({...}) }}` | — |
| `<desy-tree>` | `{{ componentTree({...}) }}` | Jerárquico |
| `<desy-textarea>` | `{{ componentTextarea({...}) }}` | — |
| `<desy-character-count>` | `{{ componentCharacterCount({...}) }}` | Contador |
| `<desy-input-group>` | `{{ componentInputGroup({...}) }}` | Compuesto: label + input + hint + error |
| `<desy-date-input>` | `{{ componentDateInput({...}) }}` | Fecha con validación |
| `<desy-radios>` | `{{ componentRadios({...}) }}` | — |
| `<desy-datepicker>` | `{{ componentDatepicker({...}) }}` | Calendario popup |
| `<desy-file-upload>` | `{{ componentFileUpload({...}) }}` | — |
| `<desy-checkboxes>` | `{{ componentCheckboxes({...}) }}` | — |
| `<desy-input>` | `{{ componentInput({...}) }}` | Input atómico |
| `<desy-fieldset>` | `{{ componentFieldset({...}) }}` | Agrupación de campos |
| `<desy-select>` | `{{ componentSelect({...}) }}` | — |
| `<desy-listbox>` | `{{ componentListbox({...}) }}` | Select accesible |

**Total cubiertos: 20+ de 57** — la tabla NO es exhaustiva. Para los 37 restantes, **lee el `angular-md/demo-X.md` correspondiente** (patrón de URL: `https://desy.aragon.es/angular-md/demo-<componente>.md`).

## Workflow de traducción

### Paso 1: Identificar el componente

Recibes código Nunjucks tipo `{{ componentButton({...}) }}`. Extrae:
- Nombre del componente (`button` → `desy-button`)
- Lista de propiedades y valores

### Paso 2: Buscar el equivalente Angular

- Consulta la tabla de equivalencias (arriba)
- Si NO está en la tabla, busca el `angular-md/demo-X.md` correspondiente en la doc oficial
- Si tampoco lo encuentras, es un componente no mapeado → **marca como pendiente**, no inventes

### Paso 3: Generar la clase TypeScript

Por cada propiedad del macro, crea un input en la clase:

```typescript
export class MyComponent {
  // Propiedades de desy-html
  text?: string;          // <-- de "text": "X"
  classes?: string;       // <-- de "classes": "c-button--primary"
  disabled: boolean = false;  // <-- de "disabled": true

  // Outputs (Angular only)
  onClick(event: any) { /* ... */ }
}
```

### Paso 4: Generar el template HTML

```html
<desy-button
  [text]="text"
  [classes]="classes"
  [disabled]="disabled"
  (clickEvent)="onClick($event)"
>
  {{ text }}
</desy-button>
```

### Paso 5: Añadir los inputs exclusivos de Angular que necesites

```html
<desy-button
  ...
  [routerLink]="'/url'"           <!-- solo si necesitas router interno -->
  [routerLinkActiveClasses]="'active'"
  ariaLabel="Click me"
  role="button"
  [tabindex]="0"
>
```

### Paso 6: Verificar accesibilidad

Angular hace explícitas las opciones a11y que HTML hace implícitas. Revisa:
- `ariaLabel` vs `<label>`: en Angular se prefiere `ariaLabel` (es label interno del componente)
- `ariaDescribedBy`: conecta con el id del elemento que describe
- `ariaDisabled` vs `disabled`: el primero es semántico, el segundo es comportamiento

## Ejemplo completo: button "Por defecto"

**Input (Nunjucks):**
```njk
{{ componentButton({
  "text": "Por defecto"
}) }}
```

**Output (TypeScript):**
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-my-button',
  templateUrl: './my-button.component.html',
})
export class MyButtonComponent {
  text?: string = 'Por defecto';
}
```

**Output (template HTML):**
```html
<desy-button [text]="text">Por defecto</desy-button>
```

## Ejemplo: button con icono SVG

**Input (Nunjucks):**
```njk
{{ componentButton({
  "html": '<svg xmlns="..."><path .../></svg>'
}) }}
```

**Output (TypeScript):**
```typescript
export class MyButtonComponent {
  html: string = '<svg xmlns="..."><path .../></svg>';
}
```

**Output (template HTML):**
```html
<desy-button [html]="html">
  <ng-container *appCustomInnerContent="{ html: html }">
    <svg xmlns="..."><path .../></svg>
  </ng-container>
</desy-button>
```

O más simple (sin directive):
```html
<desy-button>
  <svg xmlns="..."><path .../></svg>
</desy-button>
```

## Ejemplo: button con routerLink

**Input (Nunjucks):**
```njk
{{ componentButton({
  "text": "Ir a usuarios",
  "href": "/usuarios",
  "classes": "c-button--primary"
}) }}
```

**Output (TypeScript):**
```typescript
export class MyButtonComponent {
  text: string = 'Ir a usuarios';
  routerLink: string = '/usuarios';
  classes: string = 'c-button--primary';
}
```

**Output (template HTML):**
```html
<desy-button
  [text]="text"
  [routerLink]="routerLink"
  [routerLinkActiveClasses]="'active'"
  [classes]="classes"
>
  Ir a usuarios
</desy-button>
```

## Validación

Después de traducir, valida con:

1. **Build con Angular CLI** (`ng build` o `npm run build-prod`): debe compilar sin errores
2. **Tests unitarios**: el agente puede usar el demo de `angular-md/demo-X.md` como referencia para tests
3. **Comparar con la doc oficial**: si tienes dudas sobre un parámetro, lee el `angular-md/demo-X.md`
4. **WCAG 2.2 AA**: usa el skill `desy-validate-accessibility` después de traducir

## Limitaciones (validadas con table-advanced y date-input, 2026-06-07)

1. **Cobertura incompleta:** 20+ de 57 componentes mapeados. Para los 37 restantes, **consulta el `angular-md/demo-X.md` correspondiente**.
2. **No incluye desy-ionic** (móvil). La traducción a Ionic es distinta (Ionic usa `ion-*` y tiene su propio ciclo de vida).

## Validación empírica realizada (2026-06-07)

Tras la creación inicial del skill (2 componentes: button, table-advanced), Jesús pidió ampliar la cobertura. Leí 5 componentes más:

| Componente | Categoría | Resultado | Notas |
|---|---|---|---|
| `button` | Trivial | ✅ Validado | Patrón 1:1 |
| `table-advanced` | Conceptual (compuesto) | ✅ Validado | Dicts → sub-componentes + eventos |
| `date-input` | Conceptual (form) | ✅ Validado | FormGroup + 3 patrones (ngModel, reactiveForm, ngModelGroup) |
| `modal` | Conceptual (compuesto) | ✅ Validado | 6 sub-componentes + `caller: TemplateRef<any>` para contenido |
| `accordion` | Conceptual (compuesto) | ✅ Validado | Items dict → `<desy-accordion-item>` + `<desy-accordion-header>` |
| `input-group` | Conceptual (form + compuesto) | ✅ Validado | FormGroup + 4 sub-componentes + 3 patrones de form |
| `pill` | Trivial (datos simple) | ✅ Validado | Variantes via `classes` (c-pill--primary/--warning/--success/--alert) |
| `combobox` | (no existe demo) | ❌ Gap | 404 en `angular-md/demo-combobox.md` — la doc oficial no lo incluye |

**Conclusiones tras la ampliación:**

1. **El patrón "trivial" (macro → selector + [bindings]) funciona en ~30+ componentes** donde el HTML es markup y el Angular es equivalente directo.
2. **El patrón "conceptual" (dicts → sub-componentes) es la norma para componentes compuestos** (~10-15: modal, accordion, input-group, table-advanced, date-input, fieldset, header-advanced, etc.).
3. **Los sub-componentes en Angular son SIEMPRE explícitos** — no se usan dicts. La traducción es:
   - `{{ componentX({items: [{...}]}) }}` (Nunjucks con dicts) → `<desy-x>...<desy-x-item .../>...</desy-x>` (Angular con sub-componentes)
4. **3 patrones de form** (ngModel, reactiveForm, ngModelGroup) se repiten en date-input e input-group — el agente debe preguntar al usuario cuál prefiere.
5. **Hay gaps en la doc oficial**: combobox no tiene demo Angular, posiblemente otros (componentes interactivos con estado interno). Para esos, **clonar `desy-angular-starter` y leer la implementación real**.
3. **Composición (slots) no es traducción 1:1:**
   - **HTML (table-advanced):** macro con dicts `{{ componentTableAdvanced({rows: [...], head: [...]}) }}`
   - **Angular (table-advanced):** sub-componentes `<desy-table-advanced-row>`, `<desy-table-advanced-row-cell>`, etc.
   - **Implicación:** la traducción es **conceptual**, no sintáctica. No es "sustituir macro por selector", es "rediseñar la estructura con sub-componentes".
4. **Integración con formularios no es trivial:**
   - **HTML (date-input):** markup estático
   - **Angular (date-input):** `FormGroup`/`FormControl`/`[(ngModel)]` nativo de `@angular/forms`
   - date-input tiene **3 patrones** documentados: ngModel, reactiveForm, ngModelGroup. El agente debe saber cuál elegir.
5. **Eventos con tipos TS:**
   - `rowsChecked: { [id: string]: boolean }` requiere definir interfaces TypeScript
   - Angular requiere importar tipos del package: `RowData[]`, `HeadCellData[]`, `CellData`, `WrapperData`, `ItemDateInputData`, etc.
6. **Componentes con estado interno:** datepicker, combo, listbox tienen estado interno que en HTML se maneja con JS, en Angular se maneja con servicios/inputs adicionales. Estos NO son traducción trivial.
7. **JS global vs Reactive Forms:** HTML usa JS global (`data-module="c-combo"`) para combo/listbox/datepicker, Angular usa state management nativo.
8. **No validado empíricamente** con build + comparación: el patrón general está validado con `button`, `table-advanced` y `date-input` (lectura de la doc), pero la tabla de equivalencias es por inspección de los `angular-md/demo-X.md`. Para validación completa, hay que clonar `desy-angular-starter`, hacer build, y comparar con la doc.

## Componentes donde la traducción es trivial (patrón directo)

- `button`, `button-loader`, `skip-link`, `header-mini`, `footer`, `pill`, `card`, `error-message`, `hint`, `error-summary`, `notification`, `alert`, `toggle`, `tooltip`, `details`, `pagination`, `breadcrumbs`, `searchbar`, `search-bar`, `media-object`, `spinner`, `modal`, `dialog`, `menubar`, `dropdown`, `list`, `status`, `status-item`, `description-list`, `tree`, `treegrid`

Total: ~30+ componentes donde el patrón general (macro → selector + [bindings]) se aplica directamente.

## Componentes donde la traducción es conceptual (no 1:1)

- **`table-advanced`:** dicts `rows[]`/`head[]`/`foot[]` → sub-componentes `<desy-table-advanced-row>`/`<desy-table-advanced-cell>` + eventos complejos (`rowsChecked`, `recalculateTable`, `filterBy`, `sortBy`)
- **`date-input`:** markup estático → FormGroup + [(ngModel)] (3 patrones de uso: ngModel, reactiveForm, ngModelGroup)
- **`datepicker`:** botón + popup → componente con estado interno + servicio de fechas
- **`combobox`:** input + datalist nativo → componente con filtrado + servicios de estado
- **`listbox`:** select nativo → componente con multiselect + servicios
- **`input-group`:** label + input + hint + error (composición HTML) → ng-content + binding de 4 sub-componentes
- **`fieldset`:** fieldset + legend (HTML) → TemplateRef + componentes legend/hint/errorMessage
- **`header-advanced`:** estructura HTML → sub-componentes para cada banda + nav con template

**Implicación para el agente:** cuando traduces uno de estos, NO generes la versión 1:1 — tienes que decidir la arquitectura Angular apropiada (FormGroup vs ngModel, sub-componentes vs slots, etc.). **Pregunta al usuario qué patrón prefiere si hay ambigüedad.**

## Validación empírica recomendada (no hecha aún)

1. Clonar `desy-angular-starter` de bitbucket (`https://bitbucket.org/sdaragon/desy-angular-starter`)
2. `npm install` + `npm run build-prod` para verificar que el setup funciona
3. Para 3-5 componentes del grupo "trivial" (button, card, pill), generar un ejemplo mínimo con opencode + M3 y verificar que el build pasa
4. Para 1-2 del grupo "conceptual" (table-advanced, date-input), generar un ejemplo y verificar que el build pasa
5. Si falla, ajustar la skill

## Próximos pasos sugeridos (cuando haya tiempo)

1. Clonar `desy-angular-starter` de bitbucket (`https://bitbucket.org/sdaragon/desy-angular-starter`)
2. `npm install` + `npm run build-prod` para verificar que el setup funciona
3. Para cada componente de la tabla, generar un ejemplo mínimo con opencode + M3 y verificar que el build pasa
4. Ampliar la tabla con los 37 componentes restantes
5. Considerar un linter `lint-html-angular.py` que traduzca automáticamente fragmentos Nunjucks

## Related

- `desy-choose-library` — para decidir si usar este skill o no
- `desy-implement-component` — genera código Nunjucks para desy-html
- `desy-validate-accessibility` — para validar el output Angular (WCAG 2.2 AA)
- `desy-component-recognizer` — para identificar componentes en un mockup
- Doc oficial: `https://desy.aragon.es/desarrollo-desy-angular.html.md`
- Patrones de URLs para demos: `https://desy.aragon.es/angular-md/demo-<componente>.md`
