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

DESY define **4 familias de plantillas** + plantillas especiales. La distinción principal es **portal público vs webapp** (con o sin auth):

- **Portal o sitio web informativo** (público, navegación institucional, sin login): cabecera `header-advanced` de 3 bandas. Solo este tipo usa `with-header-advanced`.
- **WebApps** (públicas sin loguear, o autenticadas tras loguear): cabecera `header` normal de 1 banda. El resto de plantillas pertenecen a esta categoría.
- **Edición de contenido** (formularios de edición con cabecera de edición): variante de webapp.
- *Especiales*: `home` (solo para la home del starter, **NO usar en producción**), `mfe*` (iframes MFE), `test` (solo para tests).

**Regla clave**: solo `with-header-advanced` tiene 3 bandas. El resto tiene header normal (1 banda). Si la página es de un portal informativo público, header-advanced. Si es una webapp (login, gestor, app autenticada), header normal.

## Tabla de selección

| Tipo de página / caso | Plantilla desy-html | Layout desy-angular | Cabecera | Notas |
|---|---|---|---|---|
| **Portal o sitio web informativo** (home de portal, secciones, **404**) | `_template.with-header-advanced.njk` | `advanced-header-layout` | `header-advanced` (3 bandas) | Único caso con header-advanced. Para portales institucionales como Portal de Salud, Vivienda, etc. |
| **WebApp sin loguear** (mapa web, accesibilidad, landing, login) | `_template.logged-out.njk` | `logged-out-layout` | `header` normal (1 banda) | Páginas públicas de una webapp, antes de autenticarse. |
| **WebApp autenticada base** (sin selector de apps) | `_template.logged.njk` | `logged-layout` | `header` normal (1 banda) | Webapp autenticada simple. |
| **WebApp autenticada con selector de apps** (gestor, intranet con varias apps) | `_template.logged-selector.njk` | `logged-selector-layout` | `header` normal (1 banda) | Permite cambiar entre apps desde la cabecera. |
| **WebApp cabecera fija** (sticky al scroll) | `_template.logged-selector-fixed.njk` | `logged-selector-fixed-layout` | `header` normal (1 banda) | Cabecera visible al hacer scroll. |
| **WebApp cabecera fija + headroom.js** | `_template.logged-selector-fixed-headroom.njk` | `logged-selector-fixed-headroom-layout` | `header` normal (1 banda) | Cabecera se oculta al bajar, aparece al subir. |
| **WebApp con subcabecera** | `_template.logged-selector-subheader.njk` | `logged-selector-subheader-layout` | `header` normal (1 banda) | Subcabecera bajo el header para navegación de contenidos relacionados. |
| **WebApp con menú lateral** (sidebar) | `_template.logged-selector-with-sidebar.njk` | `logged-selector-sidebar-layout` | `header` normal (1 banda) | Sidebar 25% + sección interior 75%. |
| **Edición cabecera fija** | `_template.edit-fixed.njk` | `edit-selector-fixed-layout` | `header` edición (1 banda) | Formulario de edición con cabecera de edición fija. |
| **Edición con sidebar sticky** | `_template.edit-fixed-with-sticky-sidebar.njk` | (componer con `logged-selector-sidebar-layout` + bloques edit) | `header` edición (1 banda) | Edición con menú lateral sticky. |

**Caso real validado (Portal de Salud, 2026-07-04)**: dentro del mismo dominio `salud.aragon.es` coexisten 2 apps distintas con plantillas distintas:

- **Portal Salud** (público) → `_template.with-header-advanced.njk` (header-advanced tuneado con "Portal de Salud" + nav institucional). Ej: página 404.
- **Gestor de expedientes** (webapp autenticada) → `_template.logged-selector.njk` (header normal con dropdown "Gestor de expedientes" + nav Inicio/Expedientes/Bandejas + user). Ej: inicio con cards, manual de ayuda con FAQs, wizard paso 1-3.

Lección: dentro de un mismo portal institucional pueden convivir múltiples webapps. La elección de plantilla NO se decide por "el sitio en general" sino por **la página concreta** y su contexto de acceso (público vs autenticado vs edición).

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