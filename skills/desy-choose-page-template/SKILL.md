---
name: desy-choose-page-template
description: "Pick the right DESY page template (portal, logged, logged-selector, logged-out, edit-fixed, etc.) by page type. Library-agnostic. Use before scaffolding."
---

# desy-choose-page-template

Ayuda a decidir qué plantilla de página DESY usar para una página nueva o una migración, según el tipo de página. La decisión es **independiente de la librería**: las mismas plantillas existen en `desy-html` (como `_template.X.njk`) y en `desy-angular` (como `X-layout`).

## Cuándo usar este skill

- Vas a crear una página nueva y necesitas saber qué plantilla extiende antes de empezar.
- Estás migrando una página existente a DESY y necesitas mapear al template correcto.
- Estás revisando una implementación y necesitas validar que la plantilla elegida es la adecuada.
- **NO** usar para elegir librería (eso es `desy-choose-library`). **NO** usar para implementar el contenido dentro de la plantilla (eso es `desy-implement-layout-patterns` + `desy-implement-component`).

## Taxonomía oficial (de `desy.aragon.es/plantillas.html`)

DESY define **4 familias de plantillas** + plantillas especiales:

1. **Sin sesión iniciada** → páginas públicas antes de autenticarse.
2. **Con sesión iniciada** → 6 variantes para webapps autenticadas.
3. **Edición de contenido** → 2 variantes para formularios de edición.
4. **Portal web** → cabeceras avanzadas de 3 bandas para portales institucionales.
5. *Especiales*: `home` (solo para la home del starter, **NO usar en producción**), `mfe*` (iframes MFE).

## Tabla de selección

| Tipo de página / caso | Plantilla desy-html | Layout desy-angular | Notas |
|---|---|---|---|
| **Portal web** (home de portal, secciones, **404**) | `_template.with-header-advanced.njk` | `advanced-header-layout` | Cabecera de 3 bandas (`header-advanced` con `title`, `customNavigationHtml`, `offcanvas`). Para portales institucionales como Portal de Salud. |
| **Sin sesión iniciada** (mapa web, accesibilidad, landing) | `_template.logged-out.njk` | `logged-out-layout` | Cabecera estándar sin auth ni selector. |
| **Webapp base** (autenticada, sin selector de apps) | `_template.logged.njk` | `logged-layout` | Webapp autenticada simple. |
| **Webapp con selector de apps** | `_template.logged-selector.njk` | `logged-selector-layout` | Permite cambiar entre apps desde la cabecera. |
| **Webapp cabecera fija** (sticky al scroll) | `_template.logged-selector-fixed.njk` | `logged-selector-fixed-layout` | Cabecera visible al hacer scroll. |
| **Webapp cabecera fija + headroom.js** | `_template.logged-selector-fixed-headroom.njk` | `logged-selector-fixed-headroom-layout` | Cabecera se oculta al bajar, aparece al subir. |
| **Webapp con subcabecera** | `_template.logged-selector-subheader.njk` | `logged-selector-subheader-layout` | Subcabecera bajo el header para navegación de contenidos relacionados. |
| **Webapp con menú lateral** (sidebar) | `_template.logged-selector-with-sidebar.njk` | `logged-selector-sidebar-layout` | Sidebar 25% + sección interior 75%. |
| **Edición cabecera fija** | `_template.edit-fixed.njk` | `edit-selector-fixed-layout` | Formulario de edición con cabecera de edición fija. |
| **Edición con sidebar sticky** | `_template.edit-fixed-with-sticky-sidebar.njk` | (componer con `logged-selector-sidebar-layout` + bloques edit) | Edición con menú lateral sticky. |

## Bloques disponibles en las plantillas

Todas las plantillas extienden con bloques Nunjucks (o slots Angular) que se override para añadir contenido:

| Bloque | Descripción |
|---|---|
| `pageSpinnerBlock` | Spinner oculto detrás del contenido |
| `headerBlock` | Cabecera (normalmente NO se override; se tunearía vía params) |
| `headerSkipLinkBlock` | Skip-link para accesibilidad |
| `subheaderBlock` | Subcabecera opcional |
| `subheaderNavigation` / `subheaderActions` / `subheaderTitle` / `subheaderMenu` | Sub-bloques de subcabecera |
| `headerNavigationEditBlock` / `headerTitleEditBlock` / `headerActionsEditBlock` | Solo en edición |
| `notificationHeaderBlock` / `notificationInnerContentBlock` / `notificationFooterBlock` | Notificaciones contextuales |
| `contentBlock` | **El principal**: aquí va el contenido de la página |
| `innerContentBlock` | Contenido dentro de sección interior (con sidebar) |
| `sidebarBlock` | Menú lateral (25% del ancho) |
| `footerBlock` | Pie (normalmente NO se override) |
| `modalBlock` | Zona de modales |

## Workflow de selección

1. **Identifica el tipo de página** según la tabla.
2. **Decide librería** si aún no está decidida: `desy-choose-library`.
3. **Elige el template/layout** de la tabla.
4. **Extiende o usa como contenedor**:
   - `desy-html`: `{% extends "templates/pages/_template.X.njk" %}` (ruta relativa desde `src/`) o `node_modules/desy-html/src/templates/pages/_template.X.njk`.
   - `desy-angular`: el layout correspondiente en `src/app/feature-modules/page-templates/layouts/X-layout/`, configurado como contenedor de la página (router-outlet + imports del layout module).
5. **Override solo los bloques que necesites**. `headerBlock` y `footerBlock` rara vez se override; se configuran vía params de `componentHeader(...)` / `componentFooter(...)`.
6. **Valida** con `desy-design-match` que el rendering coincide con el gold de referencia.

## Anti-patrones (errores frecuentes)

- ❌ **Usar `_template.home.njk` para páginas que no son la home del starter**. Solo aplica a la home de `desy-html-starter`. Si la usas para un 404 o un portal, sale con header local del starter (`Inicio/Plantillas/Spinners/Páginas`) en lugar del header institucional correcto.
- ❌ **Asumir que la cabecera visible define la plantilla**. La cabecera puede tunearse en cualquier plantilla; el factor decisivo es la **familia** (portal, sin sesión, webapp, edición), no la cabecera concreta.
- ❌ **Override `headerBlock` o `footerBlock` directamente** cuando solo necesitas tunear parámetros. Pasa los params al `componentHeader(...)` / `componentFooter(...)` dentro del bloque de cabecera/pie del template.
- ❌ **Inventar una nueva plantilla** en lugar de elegir una existente. Las 10 de la tabla cubren los casos del 95% de páginas institucionales.
- ❌ **Confundir plantillas con patrones atómicos**. Las plantillas (`logged-layout`, etc.) son el chrome completo de la página. Los patrones atómicos (`_pattern.X.njk`, como FAQs, cards, errores) son secciones dentro de `contentBlock`. Se complementan, no se sustituyen.

## Relación con otros skills

- **Previo**: `desy-choose-library` (decide librería: desy-html / desy-angular / desy-ionic).
- **Siguiente**:
  - `desy-scaffold-project` (crea el proyecto a partir del starter).
  - `desy-implement-layout-patterns` (estructura del contenido dentro de `contentBlock`).
  - `desy-implement-pattern` (patrones atómicos como FAQs, cards, errores dentro de `contentBlock`).
  - `desy-implement-component` (componentes sueltos: botón, input, card).
- **Validación**:
  - `desy-design-match` (compara contra gold de referencia).
  - `desy-validate-accessibility` (verifica WCAG 2.2 AA).
- **Traducción**:
  - `desy-angular-translator` (si la implementación es en desy-angular).

## Origen de la información

- Documentación oficial: <https://desy.aragon.es/plantillas.html.md>
- Plantillas individuales: <https://desy.aragon.es/plantillas-{familia}.html.md>
- Repos fuente:
  - `bitbucket.org/sdaragon/desy-html/src/master/src/templates/pages/_template.*.njk`
  - `bitbucket.org/sdaragon/desy-angular/src/master/src/app/feature-modules/page-templates/layouts/`
- Hallazgo 2026-07-04: gap detectado al replicar un 404 del Portal de Salud con el flujo correcto Vite + Nunjucks + macros de desy-html. Inicialmente usé `_template.home.njk` (incorrecto para portales institucionales); el bug visual resultante fue corregido usando `_template.with-header-advanced.njk` tuneado.