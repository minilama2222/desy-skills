---
name: desy-styles-reference
description: "Reference of the DESY design tokens (colors, spacing, typography, shadows) extracted from desy-html library. Invoke when the user asks which utility class to use (e.g. `p-base` vs `p-4`?, `mb-lg` vs `mb-7`?, `text-primary` vs `text-blue-700`?), when reviewing existing code for token compliance, or when Tailwind defaults conflict with the design system. Covers the 8/16/28/32px canonical spacing scale, the primary/neutral/warning/success/info/alert color families with light/base/dark variants, and typography classes (`c-h1`/`c-paragraph-base`/etc.)."
---

# desy-styles-reference

Catálogo de los **tokens de diseño del sistema DESY** (colores, espaciado, tipografía, sombras), extraídos directamente del source CSS de la librería `desy-html`. Referencia obligatoria antes de aplicar cualquier estilo visual en un proyecto DESY.

## Cuándo usarla
- **Triggers:** *"¿qué color uso para...?"*, *"¿qué espaciado para este gap?"*, *"`p-base` o `p-4`?"*, *"`text-primary-base` o `text-blue-700`?"*, *"`mb-lg` o `mb-7`?"*, *"el h1 me sale más pequeño que en el gold, ¿qué clase uso?"*, *"¿qué font-size tiene `c-h1`?"*, *"¿qué radio tiene el botón?"*.
- **Cargar:** on-demand en cualquier paso de implementación, especialmente cuando el output no coincide con el gold.
- **NO usar para:** implementar componente con macro existente (la macro ya aplica tokens — no tocar), generar Nunjucks (→ `desy-implement-component`; consultar este solo para overrides), proyecto que NO es starter DESY (tokens distintos), validar contraste (→ `desy-validate-accessibility`).

## Posición en el workflow DESY
**On-demand** — se invoca en cualquier punto de la cadena cuando hay duda sobre qué token usar. Relación estrecha con `desy-implement-component` (overrides), `desy-design-match` (discrepancias), `desy-validate-accessibility` (ratios de contraste). Workflow completo en `desy-preflight-check`.

## Errores típicos que evita
- ❌ **Utility classes Tailwind por defecto** en lugar de tokens del proyecto: `text-blue-700`, `p-4`, `text-3xl font-semibold` rompen la coherencia cromática y tipográfica del sistema.
- ❌ **Colores hex hardcodeados** (`#00607a`) en vez de `bg-primary-base`: rompe si el sistema actualiza el token central.
- ❌ **Tipografía con `text-3xl font-semibold`** en lugar de `c-h1`: la clase semántica encapsula tipo + peso + tamaño + line-height + color. El utility class solo da una parte.
- ❌ **Valores de espaciado arbitrarios** (`gap-3`, `p-5`): el sistema usa escala canónica {8, 16, 28, 32}px.
- ❌ **Sombras de focus manuales** cuando las macros ya las aplican: las macros DESY ya traen `--shadow-outline-focus` correcto.
- ❌ **`lg:grid-cols-5` "no existe"** porque no aparece en el CSS precompilado: Vite genera utilities on-demand, el precompilado no las trae todas (patrón documentado en `desy-design-match`).

## Siguiente skill típica
→ **On-demand según la duda resuelta:** si era color de componente → `desy-implement-component`; si era spacing/tipografía contra gold → `desy-design-match`; si era contraste WCAG → `desy-validate-accessibility`; si era radio/sombra → `desy-implement-layout-patterns` o `desy-implement-component`. Típicamente NO es paso final — siempre vuelve a una skill de implementación.

## Related

- `desy-implement-component` — cómo usar las macros de la librería (este skill es la base visual, implement es la aplicación práctica).
- `desy-scaffold-project` — cómo arrancar el proyecto donde se aplican estos tokens.
- `desy-validate-accessibility` — para validar que el uso de color cumple ratios WCAG (los pares `*-base` sobre `*-light` y blanco están pensados para AA).
- `desy-design-match` — para diagnosticar discrepancias visuales post-implementación.

**Aplica siempre utility classes de Tailwind 4 con los tokens semánticos del proyecto, NUNCA utility classes con valores por defecto.**

| ❌ Incorrecto | ✅ Correcto | Por qué |
|---|---|---|
| `text-blue-700` | `text-primary-base` | `text-blue-700` es de la paleta Tailwind por defecto; rompe la coherencia cromática del sistema de diseño del Gobierno de Aragón |
| `text-3xl font-semibold` (en un h1) | `c-h1` | La tipografía tiene clases semánticas dedicadas que encapsulan el sistema |
| `p-4` | `p-base` | `p-4` no existe como token del proyecto; `p-base` (= 1rem) es la unidad base del spacing |
| `text-red-600` | `text-alert-base` | El rojo del sistema de alertas tiene un matiz específico (`#d22333`), no el rojo de Tailwind |
| `bg-gray-100` | `bg-neutral-lighter` | El gris del sistema es `#f6f6f5`, más cálido que el `gray-100` de Tailwind |
| `gap-4` | `gap-base` | Mismo motivo que `p-base` |
| `rounded-md` | `rounded-sm` o `rounded` (sin prefijo → 0) | Los radius del proyecto son distintos |

**Cómo verificar que estás usando bien los tokens:** después de `npm run build`, abre `dist/css/styles.css` y comprueba que las utility classes que usaste (`bg-primary-base`, `p-base`, etc.) aparecen en el CSS compilado. Si usaste algo como `text-3xl` y NO aparece, el sistema de diseño lo está ignorando.

## Colores (tokens semánticos del proyecto)

Fuente: `node_modules/desy-html/src/css/styles.css` (variables CSS que Tailwind 4 expone como utility classes).

### Paleta primaria (Gobierno de Aragón)

| Token | Valor | Uso típico |
|---|---|---|
| `--color-primary-base` | `#00607a` | Color principal: links, botones primary, acentos |
| `--color-primary-dark` | `#00475c` | Hover/active de primary |
| `--color-primary-light` | `#d6eaf0` | Fondo de elementos primary (selección, hover sutil) |

**Utility classes:** `bg-primary-base`, `bg-primary-light`, `text-primary-base`, `text-primary-dark`, `border-primary-base`, `ring-primary-base`, etc.

### Paleta neutral (texto y superficies)

| Token | Valor | Uso típico |
|---|---|---|
| `--color-neutral-dark` | `#5e616b` | Texto secundario (descripciones, hints) |
| `--color-neutral-base` | `#92949b` | Texto deshabilitado, bordes sutiles, separadores |
| `--color-neutral-light` | `#ededec` | Fondo de hover, separadores |
| `--color-neutral-lighter` | `#f6f6f5` | Fondo de página (body) |

**Utility classes:** `text-neutral-dark`, `text-neutral-base`, `bg-neutral-light`, `bg-neutral-lighter`, `border-neutral-base`, `border-neutral-dark`, `border-neutral-light`.

### Paleta semántica (estados)

| Token | Valor | Uso típico |
|---|---|---|
| `--color-alert-base` | `#d22333` | Errores, validación fallida, acciones destructivas |
| `--color-alert-dark` | `#a40014` | Hover de alert |
| `--color-alert-light` | `#fbd3ce` | Fondo de error suave, bordes de error |
| `--color-warning-base` | `#fdcb33` | Foco visible, avisos |
| `--color-warning-dark` | `#b88e12` | Hover de warning |
| `--color-warning-light` | `#fef6b2` | Fondo de aviso |
| `--color-success-base` | `#24d14c` | Confirmaciones, success |
| `--color-success-dark` | `#1aa23a` | Hover de success |
| `--color-success-light` | `#dcf8e2` | Fondo de success |
| `--color-info-base` | `#fa99002` | Información |
| `--color-info-dark` | `#c97a00` | Hover de info |
| `--color-info-light` | `#feebcc` | Fondo de info |

**Utility classes:** `text-alert-base`, `bg-alert-light`, `border-alert-base`, `text-warning-base`, `bg-success-light`, etc.

### Tipografía estructural

| Token | Valor | Uso típico |
|---|---|---|
| `--color-heading-base` | `#3c4c5c` | Color base de headings (si no usas las clases `c-h*`) |
| `--color-heading-dark` | `#26374a` | Headings destacados |
| `--color-code` | `#c10007` | Texto de `<code>` |

### Básicos

| Token | Valor | Uso típico |
|---|---|---|
| `--color-white` | `#ffffff` | Fondo de cards, botones secundarios |
| `--color-black` | `#1f2331` | Texto principal, focus rings, sombras |
| `--color-transparent` | `transparent` | Fondos invisibles |

## Espaciado (escala de tokens del proyecto)

**Unidad base: 1rem (`--spacing-base`).** Todo el espaciado del proyecto se basa en múltiplos de esta unidad. NO uses valores arbitrarios (`p-4`, `m-2`, `gap-3`) — usa los tokens.

| Token | Valor | Equivalente aproximado | Uso típico |
|---|---|---|---|
| `--spacing-xs` | 0.25rem | ~4px | Espaciado muy fino (entre icono y texto inline) |
| `--spacing-sm` | 0.5rem | ~8px | Separación pequeña (label-input, texto-texto) |
| `--spacing-base` | 1rem | 16px | **Unidad base** — separación estándar entre bloques |
| `--spacing-lg` | 1.75rem | ~28px | Separación entre secciones de la misma página |
| `--spacing-xl` | 2.5rem | ~40px | Separación entre bloques principales (form-botones) |
| `--spacing-2xl` | 5rem | ~80px | Separación entre secciones de la página |
| `--spacing-3xl` | 10rem | ~160px | Separación entre hero y contenido |

**Utility classes (todas funcionan con los tokens):**

- **Padding:** `p-base`, `p-sm`, `p-lg`, `px-base`, `py-base`, `pt-base`, `pb-base`, `p-xs`, `p-xl`, `p-2xl`, `p-3xl`, etc.
- **Margin:** `m-base`, `mt-sm`, `mb-lg`, `mx-auto`, `my-base`, etc.
- **Gap (flex/grid):** `gap-base`, `gap-sm`, `gap-lg`, `gap-x-base`, `gap-y-sm`
- **Space-between (con `>`):** `space-y-base`, `space-y-sm`

**Importante:** el sistema no tiene `p-4` o `m-2`. Si necesitas `1rem` usa `p-base`; si necesitas `0.5rem` usa `p-sm`; si necesitas `0.25rem` usa `p-xs`. Si necesitas un valor que no está en la escala, probablemente no lo necesitas — usa el token más cercano.

## Tipografía (clases semánticas `c-h*` y `c-paragraph-*`)

Documentado en detalle en `desy-implement-component` → sección "Clases tipográficas de DESY". Resumen:

| Elemento | Clase | Notas |
|---|---|---|
| Título principal | `c-h1` | Una por página (o H2 con `c-h1` si la jerarquía visual lo requiere) |
| Subtítulo | `c-h2` | |
| Encabezado menor | `c-h3` | |
| Encabezado auxiliar | `c-h4` | |
| Párrafo estándar | `c-paragraph-base` | Default para `<p>` |
| Párrafo destacado (intro) | `c-paragraph-lead` | Bajo el H1 |
| Párrafo pequeño | `c-paragraph-sm` | Hints, notas, metadatos |

**Regla:** NUNCA utility classes (`text-3xl font-semibold`, `text-base leading-normal`) para tipografía. SIEMPRE `c-h*` o `c-paragraph-*`.

## Sombras y focus (tokens específicos)

El proyecto tiene sombras semánticas para focus rings y elevación:

| Token | Valor | Uso |
|---|---|---|
| `--shadow-outline-focus` | `inset 0 -2px 0 0 var(--color-black)` | Foco de links y botones |
| `--shadow-outline-focus-input` | `inset 0 0 0 3px var(--color-black)` | Foco de inputs (alto contraste) |
| `--shadow-outline-black` | `0 0 0 3px var(--color-black)` | Foco externo |
| `--shadow-outline-warning` | `0 0 0 3px var(--color-warning-base)` | Foco amarillo (legacy, no recomendado) |
| `--shadow-outline-alert` | `0 0 0 2px var(--color-alert-base)` | Foco de error |
| `--shadow-solid-primary-base` | `0 1px 0 0 var(--color-primary-base)` | Sombras sólidas (1px) sobre primary |

**Regla:** el foco de los componentes ya está implementado en las macros (`c-button`, `c-input`). No añadas sombras de focus manuales. Para focus personalizado, usa `--shadow-outline-focus` (negro inset) — es el patrón consistente del sistema.

## Radius (redondeo de bordes)

Los radius del proyecto son discretos. No uses `rounded-md` ni `rounded-lg` por defecto:

| Token | Valor | Uso |
|---|---|---|
| `--radius-xs` | 0.125rem | Bordes muy sutiles (a veces invisible) |
| `--radius-sm` | 0.25rem | **Default** para inputs, botones, cards (lo aplica Tailwind como `rounded-sm`) |
| `--radius-lg` | 0.5rem | Cards grandes, modales |

**Utility classes:** `rounded-xs`, `rounded-sm`, `rounded-lg`. Si quieres sin redondeo: `rounded-none`.

## Iconografía (inline SVG, no archivos externos)

**Regla:** los iconos de DESY van **inline en el HTML/TSX**, no como archivos externos. Cada macro que necesita icono lo acepta como parámetro `icon` o lo incluye directo en su template.

**Si necesitas un icono específico** que no esté en una macro:
1. Busca primero si está en `node_modules/desy-html/src/templates/includes/_icons.html.njk` o similar
2. Si no, busca en la doc oficial: `https://desy.aragon.es/componente-...-codigo.html.md` (los iconos vienen en el código de ejemplo)
3. Si tampoco, descárgalo de Figma Community (la librería DESY oficial) e incrústalo inline

**Regla para SVG inline:** `aria-hidden="true"` y `focusable="false"` en iconos decorativos; `role="img"` y `aria-label="..."` en iconos con significado.

## Componentes con `c-*` (bloques UI completos)

Para 107 bloques UI ya implementados (botones, inputs, tablas, modales, menús, etc.), consulta `desy-implement-component` → "Mapeo de componentes". Los más usados:

- `c-button`, `c-button--primary`, `c-button--secondary`, `c-button--alert`, `c-button--sm/base/lg`
- `c-input`, `c-input--sm/base/lg`
- `c-breadcrumbs`
- `c-link`, `c-link--neutral`, `c-link--alert`
- `c-pill`, `c-pill--primary/alert/success/warning`
- `c-notification`, `c-notification--primary/alert/success/warning`
- `c-table`, `c-table-advanced`, `c-table--no-responsive`
- `c-skip-link`, `c-form-group`, `c-form-group--error`

## Cómo verificar que el output usa los tokens del proyecto

**Checklist de auto-verificación post-build:**

1. `npm run build` termina sin errores
2. Abre `dist/css/styles.css` y comprueba que las utility classes que usaste (`bg-primary-base`, `p-base`, etc.) aparecen en el archivo
3. Si una utility class que usaste **NO** aparece en el CSS compilado, significa que Tailwind 4 no la reconoce — probablemente usaste un valor por defecto en lugar del token del proyecto
4. Compara el output visualmente con el gold oficial — si los colores o espaciados difieren, probablemente hay un token que no se aplicó

**Comando de verificación rápida (en la raíz del proyecto):**

```bash
# ¿Qué utility classes se generaron en el CSS compilado?
grep -oE '\.(bg|text|border|p|m|gap)-(primary|neutral|alert|warning|success|info)' dist/css/styles.css | sort -u
```

Si la lista de utility classes que ves en el grep NO incluye las que tú escribiste, revisa los tokens.

## Ejemplos: bueno vs malo

### ❌ Malo (utility Tailwind por defecto)

```html
<h1 class="text-3xl font-semibold mb-4 text-gray-900">Datos de identidad</h1>
<p class="text-base text-gray-700 leading-normal mb-2">Indica tus datos...</p>
<button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md">Siguiente</button>
```

**Problemas:**
- `text-3xl font-semibold` → debería ser `c-h1`
- `text-gray-900` → debería ser `text-black` o `text-heading-dark` (gris del proyecto)
- `bg-blue-600` → debería ser `bg-primary-base`
- `rounded-md` → debería ser `rounded-sm`

### ✅ Bueno (tokens del proyecto)

```html
<h1 class="c-h1">Datos de identidad</h1>
<p class="c-paragraph-base">Indica tus datos...</p>
<button class="c-button c-button--primary">Siguiente</button>
```

**Para casos donde necesitas tokens sueltos (no hay macro):**

```html
<!-- Eyebrow encima del h1 -->
<p class="text-sm font-semibold text-primary-base">Paso 1 de 3</p>
<!-- Equivalente con c-paragraph-sm: -->
<p class="c-paragraph-sm text-primary-base">Paso 1 de 3</p>

<!-- Separación entre bloques -->
<div class="py-xl">...</div>
<!-- Equivalente en spacing: -->
<div class="py-2xl">...</div>

<!-- Fondo neutro sutil -->
<section class="bg-neutral-lighter p-base">...</section>
```

## Cuándo este skill NO se necesita

- Estás implementando un componente con macro existente (`componentButton`, `componentInput`, etc.) → no toques tokens, la macro ya los aplica
- Estás modificando `custom.css` del proyecto para overrides específicos del proyecto → usa este skill como referencia pero el override es legítimo
- Estás en un proyecto que **no** es un starter DESY → este skill no aplica, el sistema de diseño es otro

## Anti-patterns

- ❌ Usar `text-blue-*`, `text-red-*`, `text-green-*` de Tailwind por defecto
- ❌ Usar `text-3xl`, `text-4xl`, `font-bold` para tipografía (debería ser `c-h*`)
- ❌ Usar `p-4`, `m-2`, `gap-3` (valores arbitrarios de Tailwind en lugar de tokens)
- ❌ Usar `bg-gray-*` para fondos neutros (debería ser `bg-neutral-*`)
- ❌ Usar `rounded-md/lg` sin verificar el radius del proyecto
- ❌ Añadir sombras de focus manuales en lugar de las que ya aplican las macros
- ❌ Hardcodear colores hex (`#00607a`) en lugar de `bg-primary-base`

## Related

- `desy-implement-component` — cómo usar las macros de la librería (este skill es la base visual, implement es la aplicación práctica)
- `desy-scaffold-project` — cómo arrancar el proyecto donde se aplican estos tokens
- `desy-validate-accessibility` — para validar que el uso de color cumple ratios WCAG (los pares `*-base` sobre `*-light` y blanco están pensados para AA)
