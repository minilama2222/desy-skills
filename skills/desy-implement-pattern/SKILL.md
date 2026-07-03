---
name: desy-implement-pattern
description: Apply DESY patterns: pick one of 19 atomic patterns from .md, or start from a similar pattern and tune it to build forms/lists/sections.
---

# desy-implement-pattern

Implementa uno o más patrones atómicos de DESY cuando necesitas construir secciones de página que NO son un componente suelto ni una plantilla completa. Por ejemplo: un domicilio postal, una lista de acciones de tabla, una barra de búsqueda.

**Hallazgo 2026-07-03:** los 19 patrones atómicos oficiales tienen su código completo (macro Nunjucks + HTML renderizado + Cuándo/Qué componentes/Accesibilidad) en los archivos `.md` (`https://desy.aragon.es/patrones-X.html.md`). NO requieren `curl`, iframes ni extracción de `<pre>`. Un simple `web_fetch` de la URL `.md` devuelve todo lo necesario.

## Cuándo usar este skill

* Te piden implementar una **sección de página DESY** que es mayor que un componente individual pero menor que una plantilla completa (form snippet, list, navigation block, content section).
* Tienes claro **qué patrón necesitas** (por nombre, descripción o screenshot).
* Estás en un proyecto DESY (HTML, Angular o Ionic) clonado y con `node_modules` listo.

**Cuándo NO usar este skill:**

* Componente suelto (un solo botón, un input, una card) → `desy-implement-component`.
* Página completa con plantilla (header + footer + skip-link + el patrón dentro) → `desy-scaffold-project` para crear la página y luego vuelve aquí para implementar el patrón dentro.
* Estructuras de agrupación de form (fieldset+legend sr-only, grid responsive, acciones en section+ul) → `desy-implement-form-patterns` (complementario).

## Los 19 patrones atómicos

Excluye la categoría **"Páginas y flujos"** (5 patrones) porque esas son composiciones de plantilla + patrones, ya cubiertas por `desy-scaffold-project` + este skill.

### Cómo pedimos información (5)

| Patrón | URL canónica | Descripción |
|---|---|---|
| Aceptar políticas de privacidad | `https://desy.aragon.es/patrones-aceptar-politicas.html.md` | Verificación antes de enviar el formulario |
| Configurar cookies | `https://desy.aragon.es/patrones-configurar-cookies.html.md` | Política de cookies y preferencias |
| Datos de identidad | `https://desy.aragon.es/patrones-datos-identidad.html.md` | Nombre y NIF/NIE agrupados en fieldset |
| Datos de contacto | `https://desy.aragon.es/patrones-datos-contacto.html.md` | Correo electrónico y móvil |
| Domicilio postal | `https://desy.aragon.es/patrones-domicilio-postal.html.md` | Calle, número, piso, código postal, provincia, municipio |

### Cómo mostramos información (5)

| Patrón | URL canónica | Descripción |
|---|---|---|
| Acciones de tabla | `https://desy.aragon.es/patrones-acciones-tabla.html.md` | Detalles y acciones en bloque sobre items de tabla |
| Grupo de acciones | `https://desy.aragon.es/patrones-grupo-acciones.html.md` | Listado de acciones primarias/secundarias/terciarias |
| Listados | `https://desy.aragon.es/patrones-listados.html.md` | Colecciones de items con enlaces |
| Title de página | `https://desy.aragon.es/patrones-title.html.md` | El texto de la pestaña del navegador |
| Títulos y encabezados | `https://desy.aragon.es/patrones-titulos-encabezados.html.md` | Encabezados de primer nivel al principio de la página |

### Ayudar a navegar y encontrar (6)

| Patrón | URL canónica | Descripción |
|---|---|---|
| Avanzar y retroceder | `https://desy.aragon.es/patrones-avanzar-retroceder.html.md` | Navegar entre pasos de un wizard (3 variantes) |
| Barra de progreso | `https://desy.aragon.es/patrones-barra-progreso.html.md` | Divide un formulario en pasos más pequeños |
| Buscar | `https://desy.aragon.es/patrones-buscar.html.md` | Búsqueda en aplicaciones web o portales |
| Filtrar | `https://desy.aragon.es/patrones-filtrar.html.md` | Mostrar opciones de ordenación y filtrado |
| Megamenú en portales | `https://desy.aragon.es/patrones-megamenu.html.md` | Bloque de navegación desplegable |
| Volver atrás | `https://desy.aragon.es/patrones-volver-atras.html.md` | Regresar a la página anterior |

### Ayudar a resolver (3)

| Patrón | URL canónica | Descripción |
|---|---|---|
| Asistencia contextual | `https://desy.aragon.es/patrones-asistencia-contextual.html.md` | Widget flotante de ayuda (esquina inferior derecha) |
| Preguntas frecuentes | `https://desy.aragon.es/patrones-preguntas-frecuentes.html.md` | FAQs en formato claro y directo |
| Soporte | `https://desy.aragon.es/patrones-soporte.html.md` | Formas de contactar con el Gobierno de Aragón |

## Workflow

### Paso 1: Identifica el patrón

* **Por nombre:** "implementa el patrón de domicilio postal" → `patrones-domicilio-postal.html.md`.
* **Por descripción:** "necesito un bloque para pedir los datos de dirección" → mismo patrón (el agente mapea la descripción al nombre).
* **Por screenshot:** usa `desy-component-recognizer` para identificar visualmente el patrón, luego vuelve aquí.

### Paso 2: Obtén el código

El código está en el archivo `.md` correspondiente. Un `web_fetch` de la URL devuelve:

* **Macro Nunjucks** completo (en bloque `js`) — listo para copiar/pegar en `includes/_pattern.X.njk`.
* **HTML renderizado** (en bloque `html`) — el HTML final con classes DESY que verás en el navegador.
* **Cuándo lo utilizamos** — el contexto de uso.
* **Qué componentes utilizamos** — los `desy-*` específicos.
* **Accesibilidad** — los requisitos WCAG del patrón.

No requiere `curl`, ni iframes, ni extracción de `<pre>`. **Un `web_fetch` basta.**

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
* **Fieldset+legend sr-only** — SIEMPRE (patrón del skill `desy-implement-form-patterns`).

### Paso 4: Renderiza

```bash
cd /root/desy-html-starter-test   # o el proyecto DESY que corresponda
npm run build                     # produce dist/
```

Verifica el output en `dist/`. Sirve con `npm run start` o `http-server dist/ -p 8080`.

### Paso 5: Integra en plantilla (si aplica)

Si la página necesita plantilla (header + footer + skip-link + main), usa `desy-scaffold-project` para elegir la plantilla oficial, y monta el patrón dentro del `contentBlock`.

## Cómo TUNEAR un patrón (similar pero no igual)

A veces lo que necesitas no es un patrón de los 19, pero está cerca. Por ejemplo:

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
* **No inventes macros nuevos:** antes de crear uno custom, busca en los 19 si hay uno similar. Si no, combina macros existentes.
* **Documenta el tuneo:** si modificas significativamente, deja un comentario en el HTML/Nunjucks explicando qué patrón tuneaste y por qué.

### Anti-patterns de tuneo

* ❌ Eliminar el `<fieldset><legend class="sr-only">` porque "no se ve". El legend DEBE ir sr-only; el título visible va en H1/H2 fuera.
* ❌ Añadir inputs sueltos sin fieldset agrupador — pierdes agrupación semántica y accesibilidad.
* ❌ Cambiar un input por un select sin mantener `name` y `label.text` — rompe el binding del formulario.
* ❌ Reemplazar `<desy-button>` por `<a>` para "Saltar" — la variante `c-button--transparent` existe.
* ❌ Inventar nombres de utility classes (`w-[150px]`, `bg-custom-blue`) — usa solo las de DESY/Tailwind.
* ❌ Cambiar el patrón por completo en vez de tomar uno cercano y tunearlo — si necesitas un wizard, usa Avanzar+retroceder como base, no inventes tu propio flujo.

## Related

* **Skill: `desy-implement-component`** — para implementar componentes sueltos (no patrones completos).
* **Skill: `desy-implement-form-patterns`** — para patrones estructurales de forms (fieldset+legend sr-only, grid responsive, acciones en section+ul). Complementario: este skill (patterns) usa los patrones de agrupación del otro.
* **Skill: `desy-scaffold-project`** — para crear la página que contendrá los patrones.
* **Skill: `desy-component-recognizer`** — para identificar el patrón visualmente desde un screenshot.
* **Catálogo oficial:** `https://desy.aragon.es/patrones.html.md`
* **Componentes:** `https://desy.aragon.es/componentes.html.md`