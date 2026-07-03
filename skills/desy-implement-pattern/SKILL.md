---
name: desy-implement-pattern
description: Apply one of 55 DESY patterns (atomic business patterns beyond components): cards, FAQs, errors, actions, headers, listados, megamenu, soporte, cookies, pagination, etc. Use when you need a recognized DESY pattern, or to tune a similar one as starting point for a new page.
---

# desy-implement-pattern

Implementa uno de los **55 patrones atómicos oficiales** de DESY cuando necesitas construir una sección de página que NO es un componente suelto ni una plantilla completa. Por ejemplo: domicilio postal, lista de acciones, FAQ, tarjeta de sección, cabecera de edición, error 404, búsqueda con filtro, etc.

**Hallazgo 2026-07-03 (acceso al repo `gorilas/desy.aragon.es`):** La documentación pública en `https://desy.aragon.es/patrones.html.md` solo lista **19 patrones atómicos**, pero el repo fuente tiene **55 patrones** en `src/templates/includes/_pattern.*.njk`. Esta skill documenta los 55.

**Origen del nombre:** antes `desy-implement-pattern` cubría solo los 19 documentados. Ampliado en 2026-07-03 para cubrir los 36 patterns adicionales que estaban en el repo pero no en la doc oficial.

## Cuándo usar este skill

* Te piden implementar una **sección de página DESY** mayor que un componente individual pero menor que una página completa.
* Tienes claro **qué patrón necesitas** (por nombre, descripción o screenshot).
* Estás en un proyecto DESY (HTML, Angular o Ionic) clonado y con `node_modules` listo.

**Cuándo NO usar este skill:**

* **Componente suelto** (un solo botón, input, card) → `desy-implement-component`.
* **Página completa con plantilla** (header + footer + skip-link + el patrón dentro) → `desy-scaffold-project` para crear la página y luego vuelve aquí para implementar el patrón dentro.
* **Estructuras de agrupación / maquetación** (fieldset+legend, grid responsive, acciones en section+ul, spacing) → `desy-implement-layout-patterns` (complementario).
* **Reconocer un patrón visualmente desde un screenshot** → `desy-component-recognizer`.

## Workflow

### Paso 1: Identifica el patrón

* **Por nombre:** "implementa el patrón de domicilio postal" → `patrones-domicilio-postal.html.md`.
* **Por descripción:** "necesito un bloque para pedir los datos de dirección" → mismo patrón (el agente mapea la descripción al nombre).
* **Por screenshot:** usa `desy-component-recognizer` para identificar visualmente el patrón, luego vuelve aquí.

### Paso 2: Obtén el código

Para los 19 patterns documentados oficialmente: la URL `.md` (e.g. `https://desy.aragon.es/patrones-X.html.md`) tiene el macro Nunjucks + HTML renderizado.

Para los 36 patterns adicionales: el código fuente está en el repo `gorilas/desy.aragon.es` (`src/templates/includes/_pattern.X.njk`). Para acceder, usa:

```bash
gh api "repos/gorilas/desy.aragon.es/contents/src/templates/includes/_pattern.<nombre>.njk?ref=master-github" | python3 -c "import json,sys,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode('utf-8'))"
```

El `.njk` tiene el macro Nunjucks listo para copiar/pegar en `includes/_pattern.X.njk`.

### Paso 3: Adapta el macro

Cambia según necesidad:

* `id`, `name`, `classes` — propios del contexto de tu página.
* `label.text` — el texto específico del campo.
* `items` (en selects) — las opciones reales (no las "Option 1, 2, 3" del ejemplo).
* `autocomplete` — el valor estándar (`name`, `email`, `tel`, `postal-code`, `address-line1`, `address-line2`).
* `required` — `true` si es obligatorio.
* `attributes.size` — para campos muy fijos (NIF: `"19"`).
* `classes` — aplica los 4 patrones de ancho del skill `desy-implement-component`:
  * Inputs: `w-full`.
  * Selects: `lg:w-full`.
  * CP cortos: `w-44 lg:w-full`.
  * NIF muy fijos: `attributes.size: "19"` (sin `w-full`).
* `formGroup.classes` — `lg:col-span-N` para items anidados en la grid.
* **Fieldset+legend sr-only** — SIEMPRE (patrón del skill `desy-implement-layout-patterns`).

### Paso 4: Renderiza

```bash
cd /root/desy-html-starter-test
npm run build
```

Verifica el output en `dist/`. Sirve con `npm run start` o `http-server dist/ -p 8080`.

### Paso 5: Integra en plantilla (si aplica)

Si la página necesita plantilla (header + footer + skip-link + main), usa `desy-scaffold-project` para elegir la plantilla oficial, y monta el patrón dentro del `contentBlock` con `{% include "includes/_pattern.X.njk" %}`.

## Cómo TUNEAR un patrón (similar pero no igual)

A veces lo que necesitas no es un patrón de los 55, pero está cerca. Por ejemplo:

* "Necesito pedir dirección postal + un campo extra de 'referencia'".
* "Necesito una lista de acciones con un campo de búsqueda arriba".
* "Necesito un formulario por pasos pero con un paso intermedio de subida de docs".

### Tipos de tuneo

1. **Añadir/quitar campos.** Copia el macro del patrón y añade/quita inputs. Mantén la estructura grid (`lg:grid-cols-N`, `lg:col-span-*`).
2. **Cambiar componentes.** Cambia un `componentInput` por `componentSelect` o viceversa. Los props principales (`id`, `name`, `label.text`, `autocomplete`, `classes`) se mantienen.
3. **Posicionamiento diferente.** Cambia `lg:col-span-N` o mueve inputs entre fieldsets. Respeta la accesibilidad: cada fieldset debe tener su `<legend class="sr-only">`.
4. **Combinar varios patrones.** Junta macros de varios patrones en un solo formulario. Ejemplo: Datos de identidad + Domicilio postal = formulario completo de dirección personal. Mantén cada patrón en su `<fieldset>` con su legend sr-only.
5. **Variantes de estilo.** El patrón "Avanzar y retroceder" tiene 3 variantes documentadas (siguiente+volver en cabecera, siguiente+volver bajo form, siguiente+saltar). Usa la que aplique.
6. **Reusar el patrón en otra librería.** El macro Nunjucks es para `desy-html`. Para Angular/Ionic, usa los equivalentes (`<desy-input>`, `<desy-select>`, etc.) con la misma estructura semántica.

### Reglas de tuneo

* **Mantén la accesibilidad WCAG:** fieldset+legend sr-only, `<label for>` apuntando al `id` del input, `aria-describedby` para hints, focus-visible.
* **Mantén los 4 patrones de ancho:** inputs `w-full`, selects `lg:w-full`, CP `w-44 lg:w-full`, NIF `attributes.size`.
* **No rompas la grid responsiva:** si añades un input al grid `lg:grid-cols-4`, asegúrate de que las `lg:col-span` sumen 4 en desktop.
* **No inventes macros nuevos:** antes de crear uno custom, busca en los 55 si hay uno similar. Si no, combina macros existentes.
* **Documenta el tuneo:** si modificas significativamente, deja un comentario en el HTML/Nunjucks explicando qué patrón tuneaste y por qué.

### Anti-patterns de tuneo

* ❌ Eliminar el `<fieldset><legend class="sr-only">` porque "no se ve". El legend DEBE ir sr-only; el título visible va en H1/H2 fuera.
* ❌ Añadir inputs sueltos sin fieldset agrupador — pierdes agrupación semántica y accesibilidad.
* ❌ Cambiar un input por un select sin mantener `name` y `label.text` — rompe el binding del formulario.
* ❌ Reemplazar `<desy-button>` por `<a>` para "Saltar" — la variante `c-button--transparent` existe.
* ❌ Inventar nombres de utility classes (`w-[150px]`, `bg-custom-blue`) — usa solo las de DESY/Tailwind.
* ❌ Cambiar el patrón por completo en vez de tomar uno cercano y tunearlo.
* ❌ **Usar `flex-column-reverse` (con guion).** Esta clase NO existe en Tailwind — es un bug del repo `gorilas/desy.aragon.es`. La clase correcta es `flex-col-reverse`. Aparece en 5 archivos del repo (e.g. `_pattern.acciones-de-cabecera.njk`). Si copias el código tal cual, el patrón de acciones no funcionará en mobile. **Siempre reemplaza `flex-column-reverse` por `flex-col-reverse` al implementar.**

## Los 55 patrones atómicos

Excluye la categoría **"Páginas y flujos"** (5 patrones) porque esas son composiciones de plantilla + patrones, ya cubiertas por `desy-scaffold-project` + este skill.

### Cómo pedimos información (7 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Aceptar políticas de privacidad | `https://desy.aragon.es/patrones-aceptar-politicas.html.md` | Verificación antes de enviar el formulario |
| Configurar cookies | `https://desy.aragon.es/patrones-configurar-cookies.html.md` | Política de cookies y preferencias |
| Datos de identidad | `https://desy.aragon.es/patrones-datos-identidad.html.md` | Nombre y NIF/NIE agrupados en fieldset |
| Datos de contacto | `https://desy.aragon.es/patrones-datos-contacto.html.md` | Correo electrónico y móvil |
| Domicilio postal | `https://desy.aragon.es/patrones-domicilio-postal.html.md` | Calle, número, piso, código postal, provincia, municipio |
| Barra de progreso (sm) | repo: `_pattern.formularios-barra-progreso-sm.njk` | Versión pequeña para wizards cortos |
| Barra de progreso | repo: `_pattern.formularios-barra-progreso.njk` | Divide formulario en pasos |

### Cómo mostramos información (10 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Acciones de tabla | `https://desy.aragon.es/patrones-acciones-tabla.html.md` | Detalles y acciones en bloque sobre items de tabla |
| Grupo de acciones | `https://desy.aragon.es/patrones-grupo-acciones.html.md` | Listado de acciones primarias/secundarias/terciarias |
| Listados | `https://desy.aragon.es/patrones-listados.html.md` | Colecciones de items con enlaces |
| Title de página | `https://desy.aragon.es/patrones-title.html.md` | El texto de la pestaña del navegador |
| Títulos y encabezados | `https://desy.aragon.es/patrones-titulos-encabezados.html.md` | Encabezados de primer nivel al principio de la página |
| Cards a secciones principales | repo: `_pattern.cards-a-secciones-principales.njk` | Cards que enlazan a secciones (grid 4 cols) |
| Cards misma altura | repo: `_pattern.cards-misma-altura.njk` | Cards con misma altura (sin botón abajo) |
| Cards misma altura + botón abajo | repo: `_pattern.cards-misma-altura-y-boton-abajo.njk` | Cards con misma altura y botón al pie |
| Listado carrusel | repo: `_pattern.listados-carrusel.njk` | Carrusel de items (no tabla) |
| Paginación | repo: `_pattern.paginacion.njk` | Paginación de listas largas |

### Ayudar a navegar y encontrar (15 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Avanzar y retroceder | `https://desy.aragon.es/patrones-avanzar-retroceder.html.md` | Navegar entre pasos de un wizard (3 variantes) |
| Barra de progreso | `https://desy.aragon.es/patrones-barra-progreso.html.md` | Divide un formulario en pasos |
| Buscar | `https://desy.aragon.es/patrones-buscar.html.md` | Búsqueda en aplicaciones web o portales |
| Filtrar | `https://desy.aragon.es/patrones-filtrar.html.md` | Mostrar opciones de ordenación y filtrado |
| Megamenú en portales | `https://desy.aragon.es/patrones-megamenu.html.md` | Bloque de navegación desplegable |
| Volver atrás | `https://desy.aragon.es/patrones-volver-atras.html.md` | Regresar a la página anterior |
| Menubar filtro + búsqueda | repo: `_pattern.menubar-filtro-busqueda.njk` | Barra de filtros con campo de búsqueda |
| Menubar filtro + orden | repo: `_pattern.menubar-filtro-orden.njk` | Barra de filtros con selector de ordenación |
| Acciones de cabecera | repo: `_pattern.acciones-de-cabecera.njk` | Acciones en la cabecera (Guardar/Salir/Guardar y salir) — *tiene bug `flex-column-reverse`* |
| Cabecera editar | repo: `_pattern.cabecera-editar.njk` | Cabecera con título + acciones de edición |
| Cabecera item | repo: `_pattern.cabecera-item.njk` | Cabecera con título + submenú horizontal |
| Cabecera item service | repo: `_pattern.cabecera-item-service.njk` | Cabecera específica para items de servicio |
| Acciones de página (sólo volver) | repo: `_pattern.acciones-de-pagina-boton-volver.njk` | Solo el botón "Volver" |
| Acciones de página (siguiente + volver) | repo: `_pattern.acciones-de-pagina-siguiente-paso-y-volver.njk` | Siguiente paso + Volver (orden invertido) |
| Acciones de página (siguiente + volver v2) | repo: `_pattern.acciones-de-pagina-siguiente-paso-y-volver-2.njk` | Variante 2 de siguiente + volver |
| Acciones de página (siguiente + saltar) | repo: `_pattern.acciones-de-pagina-siguiente-paso-y-saltar.njk` | Siguiente paso + Saltar (orden directo) |
| Acciones de página (3 botones) | repo: `_pattern.acciones-de-pagina-primaria-secundaria-y-terciarias.njk` | Primaria + secundaria + dropdown terciarias |
| Acciones de página (filtros) | repo: `_pattern.acciones-de-pagina-mostrar-filtros-y-busqueda.njk` (y 2 variantes) | Mostrar/ocultar filtros |
| Acciones de página (buscar en sitio) | repo: `_pattern.acciones-de-pagina-buscar-en-el-sitio.njk` | Buscar en el sitio (botón en cabecera) |
| Acciones primaria-secundaria-terciarias | repo: `_pattern.acciones-primaria-secundaria-y-terciarias.njk` | Variante compacta de 3 botones |
| Título + acciones buscador | repo: `_pattern.titulo-acciones-buscador-de-pagina.njk` | Cabecera de página con título + buscador |
| Título + acciones de página | repo: `_pattern.titulo-acciones-de-pagina.njk` | Cabecera de página con título + acciones |
| Título + pasos + botón volver | repo: `_pattern.titulo-con-pasos-y-boton-de-volver-atras.njk` | Título con indicador de paso + botón volver |
| Búsqueda Google | repo: `_pattern.google-searchbar.njk` | Searchbar con Programmable Search Engine |

### Ayudar a resolver (10 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Asistencia contextual | `https://desy.aragon.es/patrones-asistencia-contextual.html.md` | Widget flotante de ayuda (esquina inferior derecha) |
| Preguntas frecuentes | `https://desy.aragon.es/patrones-preguntas-frecuentes.html.md` | FAQs en formato claro y directo |
| Soporte | `https://desy.aragon.es/patrones-soporte.html.md` | Formas de contactar con el Gobierno de Aragón |
| FAQs acordeón | repo: `_pattern.faqs-acordeon.njk` | FAQs en formato acordeón expandible |
| FAQs listado | repo: `_pattern.faqs-listado.njk` | FAQs en formato listado |
| Ponte en contacto | repo: `_pattern.ponte-en-contacto.njk` | Página de contacto con varias vías |
| Errores estáticos | repo: `_pattern.errores-estaticos.njk` | Errores de validación HTML estáticos |
| Errores JavaScript | repo: `_pattern.errores-javascript.njk` | Errores de validación JS dinámicos |
| Error identificación | repo: `_pattern.error-identificacion.njk` | Pantalla de error tras identificación fallida |
| Error navegador | repo: `_pattern.error-navegador.njk` | Pantalla de error del navegador |

### Notificaciones (3 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Abrir notificaciones | repo: `_pattern.abrir-notificaciones.njk` | Botón/área para abrir panel de notificaciones |
| Notificación identificado | repo: `_pattern.notificacion-identificado.njk` | Toast/banner de identificación en curso |
| Notificación identificado correctamente | repo: `_pattern.notificacion-identificado-correctamente.njk` | Toast/banner de identificación exitosa |

### Cookies (2 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Cookies (completo) | repo: `_pattern.cookies.njk` | Banner completo de cookies con gestión granular |
| Cookies (simple) | repo: `_pattern.cookies-simple.njk` | Banner simple de cookies (aceptar/rechazar) |

### Listados y tablas (4 patrones)

| Patrón | URL canónica / ubicación | Descripción |
|---|---|---|
| Tabla de items | repo: `_pattern.tabla-de-items.njk` | Tabla genérica con acciones por fila |
| Lista de items | repo: `_pattern.lista-de-items.njk` | Lista vertical de items con acciones |
| Paginación | repo: `_pattern.paginacion.njk` | Paginación de resultados |
| Lorem ipsum (large) | repo: `_pattern.loremipsum-large.njk` | Placeholder para demos |

## Tabla de acceso rápido

| Categoría | Doc oficial | Repo | Faltan |
|---|---|---|---|
| Cómo pedimos | 5 | 7 | 2 |
| Cómo mostramos | 5 | 10 | 5 |
| Ayudar a navegar | 6 | 15 | 9 |
| Ayudar a resolver | 3 | 10 | 7 |
| Notificaciones | 0 | 3 | 3 |
| Cookies | 1 | 2 | 1 |
| Listados y tablas | 2 | 4 | 2 |
| **Total** | **19** | **55** | **36** |

## Anti-patterns (lecciones aprendidas)

1. **`flex-column-reverse` (con guion) en 5 archivos del repo oficial.** Esta clase NO existe en Tailwind — la clase correcta es `flex-col-reverse`. Si copias el código del repo tal cual, el patrón de acciones no funcionará en mobile. **Siempre reemplaza `flex-column-reverse` por `flex-col-reverse`** al implementar `_pattern.acciones-de-cabecera.njk` y similares. Detectado en 2026-07-03.

2. **Eliminar el `<fieldset><legend class="sr-only">` porque "no se ve".** El legend DEBE ir sr-only; el título visible va en H1/H2 fuera del fieldset.

3. **Añadir inputs sueltos sin fieldset agrupador.** Pierdes agrupación semántica y accesibilidad.

4. **Cambiar un input por un select sin mantener `name` y `label.text`.** Rompe el binding del formulario.

5. **Reemplazar `<desy-button>` por `<a>` para "Saltar".** La variante `c-button--transparent` existe en el sistema de diseño.

6. **Inventar nombres de utility classes (`w-[150px]`, `bg-custom-blue`).** Usa solo las de DESY/Tailwind.

7. **Cambiar el patrón por completo en vez de tomar uno cercano y tunearlo.** Si necesitas un wizard, usa "Avanzar y retroceder" como base, no inventes tu propio flujo.

## Cómo añadir un nuevo pattern que NO está en el repo

Si necesitas un pattern que ni está en los 55 ni se puede tunear de uno existente:

1. **Componlo de macros existentes** (`desy-implement-component`) + patrones estructurales (`desy-implement-layout-patterns`).
2. **Documéntalo en el repo** creando un `_pattern.X.njk` en `src/templates/includes/` y un `_examples.X.njk` para tests visuales.
3. **Actualiza esta skill** añadiendo el nuevo pattern al índice.

## Related

* **Skill: `desy-implement-component`** — para implementar componentes sueltos (no patrones completos).
* **Skill: `desy-implement-layout-patterns`** — para patrones estructurales de maquetación (fieldset+legend, grid responsive, acciones en section+ul, header con skip-link).
* **Skill: `desy-scaffold-project`** — para crear la página que contendrá los patrones.
* **Skill: `desy-component-recognizer`** — para identificar el patrón visualmente desde un screenshot.
* **Catálogo oficial:** `https://desy.aragon.es/patrones.html.md` (solo 19 de los 55).
* **Repo fuente:** `gorilas/desy.aragon.es` en `src/templates/includes/_pattern.*.njk` (los 55 patterns).