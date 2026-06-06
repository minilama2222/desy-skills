---
name: desy-implement-component
description: "Generate copy-pasteable DESY component code in desy-html (Nunjucks), desy-angular (TS), or desy-ionic. Use when implementing a specific DESY component with given requirements."
---

# desy-implement-component

Genera código copy-pasteable para un componente DESY concreto en la librería adecuada, con los parámetros que pida el equipo.

## When to use this skill

- El equipo sabe QUÉ componente necesita (ej: "un botón de enviar", "una tabla con paginación", "un modal de confirmación")
- El equipo ya tiene claro en qué librería va a trabajar (desy-html / desy-angular / desy-ionic)
- Se necesita el código listo para pegar con los parámetros concretos

## Inputs que necesitas pedir

Antes de generar código, confirma con el equipo:

1. **Componente** (nombre exacto o descripción visual)
2. **Librería** (desy-html / desy-angular / desy-ionic)
3. **Parámetros clave:**
   - Texto / label
   - Variante (primary, secondary, danger, etc.) si aplica
   - Estado (default, disabled, loading, active)
   - Atributos ARIA / accesibilidad (si hay requisitos especiales)
   - Icono (si lo lleva)
   - Link o acción (href, routerLink, onClick)
4. **Contexto de uso:**
   - ¿Está dentro de un formulario?
   - ¿Necesita preventDoubleClick?
   - ¿Es parte de un patrón conocido? (ej: acciones de tabla → ver `patrones-acciones-tabla`)

## Workflow

### Paso 1: Identifica la URL del ejemplo "copia y pega"

Usa la tabla de mapeo de la sección "Mapeo de componentes" más abajo. Cada componente tiene su URL canónica en la documentación.

### Paso 2: Lee el ejemplo oficial

`web_fetch` la URL del ejemplo. La doc viene en dos formatos:
- **HTML / Nunjucks**: `https://desy.aragon.es/componente-<nombre>-codigo.html.md`
- **Angular**: `https://desy.aragon.es/angular-md/demo-<nombre>.md`
- **Ionic**: `https://desy.aragon.es/desy-ionic` (Storybook) o `https://bitbucket.org/sdaragon/desy-ionic` (repo)

### Paso 3: Adapta los parámetros

Copia el ejemplo y sustituye los parámetros con los del equipo. Mantén las clases CSS y atributos ARIA del ejemplo — son obligatorios para accesibilidad.

### Paso 4: Verifica accesibilidad

- ¿Tiene `alt` si lleva imagen?
- ¿Tiene `aria-label` si el texto visible no es descriptivo?
- ¿El foco es visible? (DESY lo asegura por defecto, pero verifica)
- ¿Contraste de color suficiente? (usar variantes oficiales)

### Paso 5: Genera el snippet final

Devuelve el código en un bloque de código con el lenguaje correcto (`html`, `typescript`, `angular`, etc.). Indica también:
- Archivo donde va
- Props de TypeScript si es Angular/Ionic
- Dependencias a importar

## Mapeo de componentes (subset crítico)

### Componentes principales

| Componente | URL HTML | URL Angular | Notas |
|---|---|---|---|
| Button | https://desy.aragon.es/componente-botones-codigo.html.md | https://desy.aragon.es/angular-md/demo-button.md | Variantes: default, primary, secondary, danger |
| Header (webapp) | https://desy.aragon.es/componente-cabeceras-app-codigo.html.md | https://desy.aragon.es/angular-md/demo-header.md | Cabecera estándar |
| Header-advanced (portal) | https://desy.aragon.es/componente-cabeceras-codigo.html.md | https://desy.aragon.es/angular-md/demo-header-advanced.md | 3 bandas, megamenú |
| Footer | https://desy.aragon.es/componente-footer-codigo.html.md | https://desy.aragon.es/angular-md/demo-footer.md | |
| Skip-link | https://desy.aragon.es/componente-cabeceras-skiplink-codigo.html.md | https://desy.aragon.es/angular-md/demo-skip-link.md | Obligatorio para accesibilidad |

### Formularios

| Componente | URL HTML | URL Angular |
|---|---|---|
| Input | https://desy.aragon.es/componente-input-text-codigo.html.md | https://desy.aragon.es/angular-md/demo-input.md |
| Textarea | https://desy.aragon.es/componente-textarea-codigo.html.md | https://desy.aragon.es/angular-md/demo-textarea.md |
| Checkbox | https://desy.aragon.es/componente-checkboxes-codigo.html.md | https://desy.aragon.es/angular-md/demo-checkboxes.md |
| Radio | https://desy.aragon.es/componente-radios-codigo.html.md | https://desy.aragon.es/angular-md/demo-radios.md |
| Select | https://desy.aragon.es/componente-selector-codigo.html.md | https://desy.aragon.es/angular-md/demo-select.md |
| Datepicker | https://desy.aragon.es/componente-datepicker-codigo.html.md | https://desy.aragon.es/angular-md/demo-datepicker.md |
| File-upload | https://desy.aragon.es/componente-file-upload-codigo.html.md | https://desy.aragon.es/angular-md/demo-file-upload.md |
| Tree | https://desy.aragon.es/componente-tree-codigo.html.md | https://desy.aragon.es/angular-md/demo-tree.md |

### Datos y avisos

| Componente | URL HTML | URL Angular |
|---|---|---|
| Table | https://desy.aragon.es/componente-tabla-codigo.html.md | https://desy.aragon.es/angular-md/demo-table.md |
| Table-advanced | https://desy.aragon.es/componente-tabla-codigo.html.md | https://desy.aragon.es/angular-md/demo-table-advanced.md |
| Modal | https://desy.aragon.es/componente-modal-codigo.html.md | https://desy.aragon.es/angular-md/demo-modal.md |
| Notification | https://desy.aragon.es/componente-notificaciones-codigo.html.md | https://desy.aragon.es/angular-md/demo-notification.md |
| Alert | https://desy.aragon.es/componente-notificaciones-alert-codigo.html.md | https://desy.aragon.es/angular-md/demo-alert.md |
| Card | https://desy.aragon.es/componente-card-codigo.html.md | https://desy.aragon.es/angular-md/demo-card.md |
| Spinner | https://desy.aragon.es/componente-spinner-codigo.html.md | https://desy.aragon.es/angular-md/demo-spinner.md |
| Pill | https://desy.aragon.es/componente-pills-codigo.html.md | https://desy.aragon.es/angular-md/demo-pill.md |
| Status | https://desy.aragon.es/componente-status-codigo.html.md | https://desy.aragon.es/angular-md/demo-status.md |
| Error-summary | https://desy.aragon.es/componente-error-summary-codigo.html.md | https://desy.aragon.es/angular-md/demo-error-summary.md |

### Navegación

| Componente | URL HTML | URL Angular |
|---|---|---|
| Breadcrumbs | https://desy.aragon.es/componente-breadcrumbs-codigo.html.md | https://desy.aragon.es/angular-md/demo-breadcrumbs.md |
| Pagination | https://desy.aragon.es/componente-paginacion-codigo.html.md | https://desy.aragon.es/angular-md/demo-pagination.md |
| Menu-navigation | https://desy.aragon.es/componente-menu-navigation-codigo.html.md | https://desy.aragon.es/angular-md/demo-menu-navigation.md |
| Menu-vertical | https://desy.aragon.es/componente-menu-vertical-codigo.html.md | https://desy.aragon.es/angular-md/demo-menu-vertical.md |
| Search-bar | https://desy.aragon.es/componente-searchbar-codigo.html.md | https://desy.aragon.es/angular-md/demo-search-bar.md |
| Links-list | https://desy.aragon.es/componente-links-list-codigo.html.md | https://desy.aragon.es/angular-md/demo-links-list.md |
| Tabs | https://desy.aragon.es/componente-tabs-codigo.html.md | https://desy.aragon.es/angular-md/demo-tabs.md |

### Mostrar/ocultar

| Componente | URL HTML | URL Angular |
|---|---|---|
| Accordion | https://desy.aragon.es/componente-acordeon-codigo.html.md | https://desy.aragon.es/angular-md/demo-accordion.md |
| Dropdown | https://desy.aragon.es/componente-dropdown-codigo.html.md | https://desy.aragon.es/angular-md/demo-dropdown.md |
| Tooltip | https://desy.aragon.es/componente-tooltip-codigo.html.md | https://desy.aragon.es/angular-md/demo-tooltip.md |
| Toggle | https://desy.aragon.es/componente-toggle-codigo.html.md | https://desy.aragon.es/angular-md/demo-toggle.md |
| Details | https://desy.aragon.es/componente-detalles-codigo.html.md | https://desy.aragon.es/angular-md/demo-details.md |
| Menubar | https://desy.aragon.es/componente-menubar-codigo.html.md | https://desy.aragon.es/angular-md/demo-menubar.md |

> Para el **catálogo completo** y componentes no listados: https://desy.aragon.es/componentes.html.md

## Examples

### Ejemplo 1: Botón "Enviar" en desy-angular

**Input del equipo:**
- Componente: Button
- Librería: desy-angular
- Texto: "Enviar"
- type: submit
- preventDoubleClick: true
- disabled: true inicialmente

**Output generado:**

```html
<!-- app/formulario.component.html -->
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
  imports: [DesyButtonComponent, /* ... */],
  templateUrl: './formulario.component.html',
})
export class FormularioComponent {
  onSubmit() {
    // lógica de envío
  }
}
```

**Notas:**
- Usamos `[disabled]` con una expresión, no estático: mejor UX que un botón siempre disabled
- `preventDoubleClick: true` evita doble submit
- Importar `DesyButtonComponent` (o el módulo correspondiente) es necesario

### Ejemplo 2: Tabla con paginación en desy-html

**Input del equipo:**
- Componente: Table-advanced
- Librería: desy-html
- Columnas: ID, Nombre, Email, Acciones
- Datos: viene del backend
- 10 filas por página

**Output generado:**

```html
<table class="c-table c-table-advanced">
  <thead>
    <tr>
      <th>ID</th>
      <th>Nombre</th>
      <th>Email</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    {% for item in items %}
      <tr>
        <td>{{ item.id }}</td>
        <td>{{ item.nombre }}</td>
        <td>{{ item.email }}</td>
        <td>
          <a href="/items/{{ item.id }}/edit">Editar</a>
          <a href="/items/{{ item.id }}/delete">Eliminar</a>
        </td>
      </tr>
    {% endfor %}
  </tbody>
</table>
```

**Notas:**
- `items` viene del controller / data layer
- Para paginación, ver patrón: https://desy.aragon.es/componente-paginacion-codigo.html.md
- Para "Acciones de tabla" con múltiples botones, ver patrón: https://desy.aragon.es/patrones-acciones-tabla.html

### Ejemplo 3: Modal de confirmación en desy-ionic

**Input del equipo:**
- Componente: Modal
- Librería: desy-ionic
- Título: "¿Eliminar este registro?"
- Cuerpo: "Esta acción no se puede deshacer."
- Botones: "Cancelar" (secundario) + "Eliminar" (danger)

**Output generado:**

```html
<ion-modal [isOpen]="isModalOpen" (didDismiss)="cerrarModal()">
  <ng-template>
    <ion-header>
      <ion-toolbar>
        <ion-title>¿Eliminar este registro?</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <p>Esta acción no se puede deshacer.</p>
      <div class="ion-text-end">
        <ion-button fill="clear" (click)="cerrarModal()">Cancelar</ion-button>
        <ion-button color="danger" (click)="confirmarEliminar()">Eliminar</ion-button>
      </div>
    </ion-content>
  </ng-template>
</ion-modal>
```

**Notas:**
- `color="danger"` aplica el color de peligro de DESY
- Accesibilidad: el título es el primer elemento focuseable
- Para patrones completos de eliminación, ver: https://desy.aragon.es/patrones-acciones-tabla.html

## Gotchas

- **No inventar nombres de props.** Si un prop no aparece en la tabla oficial, pregunta al equipo o consulta la URL de la demo. Un prop mal nombrado pasa el compile pero no funciona.
- **No saltarse atributos ARIA.** DESY los incluye por defecto en sus ejemplos. Si los quitas, rompes accesibilidad.
- **En Angular/Ionic, importar el componente.** Olvidar el import en `imports: []` es el error más común.
- **En desy-html, no usar `class` directamente.** Usar el `params.classes` del macro Nunjucks, no escribir `class="..."` en el HTML.
- **No mezclar librerías.** Un proyecto no debería tener desy-html y desy-angular al mismo tiempo para el mismo componente. Complica mantenimiento y versionado.

## Related

- Skill: `desy-choose-library` (paso anterior — qué librería usar)
- Skill: `desy-scaffold-project` (paso siguiente — setup inicial)
- Catálogo completo: https://desy.aragon.es/componentes.html
- Patrones: https://desy.aragon.es/patrones.html
- Versiones: https://desy.aragon.es/desarrollo-versiones.html (qué versión de desy-html corresponde a cada versión de desy-angular)
