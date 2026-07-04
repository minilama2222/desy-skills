---
name: desy-design-match
description: "Workflow iterativo para que la implementación visual de una página DESY coincida con la imagen de referencia. Cubre el proceso de medir, comparar y afinar spacing/tipografía después de la primera pasada estructural. NO cubre la fuente de verdad de los tokens (eso es desy-styles-reference)."
---

# desy-design-match

Workflow de **fidelidad visual**: cómo acercarse a una imagen de referencia (gold HTML servible, mockup, captura de Figma) cuando se está implementando una página del sistema de diseño DESY. Complementa a `desy-styles-reference` (que es la fuente de verdad de los tokens).

## When to use this skill

- Acabas de terminar la 1ª pasada estructural de una página y hay diferencias visibles con la referencia
- El build pasa, los contadores coinciden, pero la página se ve "rara" en algún detalle (spacing, tipografía, layout)
- Necesitas decidir si una discrepancia concreta (4px, 8px, 28px) es ruido del navegador o merece un fix
- El usuario reporta "esto se ve mal" sin más detalle

**NO uses este skill si:**
- Estás en la 1ª pasada (esqueleto) — preocúpate primero de la estructura y los bindings
- Solo quieres consultar qué token usar → `desy-styles-reference`
- La diferencia es funcional, no visual (e.g. un campo no se envía, un evento no dispara)
- La plantilla de página usada **no es la correcta** para el tipo de página (e.g. usar `_template.home.njk` para un portal institucional en vez de `_template.with-header-advanced.njk`). Antes de medir discrepancias, valida la plantilla con [`desy-choose-page-template`](.). Sin plantilla correcta, las diferencias visuales masivas no se arreglan con tuning de tokens — son estructurales.

## Regla de oro: la imagen de referencia manda

> "Analiza bien los espacios verticales (márgenes, paddings, gaps, alineaciones) y la tipografía (tamaños, line-heights) a partir de la imagen de referencia. Si es necesario para acercarte a la imagen, usa modificadores como `mb-0`, `-mt-X`, `mb-X`, `mt-X` (o quita los que pusiste por defecto). El spacing por defecto del design system no es la verdad absoluta: la imagen de referencia manda."

### Medidas canónicas del design system

Extraídas de la documentación oficial de tipografía de DESY. Antes de inventar márgenes, mira si el valor que necesitas está en esta tabla:

| Elemento | Clase | font-size | line-height | margin-bottom |
|---|---|---|---|---|
| h1 grande | `.c-h0` | 40px | 50px | mb-8 (32px) |
| **h1 estándar** | **`.c-h1`** | **30px** | **37.5px** | **mb-lg (28px)** |
| h2 | `.c-h2` | 24px | 30px | mb-base (16px) |
| h3 | `.c-h3` | 18px | 22.5px | mb-sm (8px) |
| h4 | `.c-h4` | 16px | 20px | mb-sm (8px) |
| Párrafo destacado | `.c-paragraph-lg` | 18px | 28px | mb-lg (28px) |
| **Párrafo por defecto** | **`.c-paragraph-base`** | **16px** | **24px** | **mb-base (16px)** |
| Párrafo pequeño | `.c-paragraph-sm` | 14px | 20px | mb-sm (8px) |

**Canónico = {8, 16, 28, 32}px** (mb-sm, mb-base, mb-lg, mb-8). Nada intermedio a no ser que la referencia lo pida explícitamente.

## Workflow iterativo de fidelidad visual

### Paso 1 — 1ª pasada (esqueleto)

**Objetivo:** estructura, form groups, bindings, build OK, lint OK, 0 console errors, contadores coinciden con la referencia.

**No te obsesiones con spacing/tipografía en esta fase.** El objetivo es que la página "exista" y funcione. Las desviaciones menores se afinan en los pasos siguientes.

### Paso 2 — Verificación visual

Captura side-by-side de tu implementación contra la referencia:
- Tu página: el URL local de tu dev server (e.g. `http://localhost:PUERTO/ruta/pagina`)
- La referencia servida (si es HTML): el URL donde sirves el gold (e.g. `http://localhost:OTRO_PUERTO/ruta/gold.html`)

Usa **cualquier herramienta de captura de screenshots headless** que tengas disponible: Puppeteer, Playwright, browser-automation, scripts con `headless-chrome --screenshot`, o lo que sea. Lo importante es obtener dos PNGs a la misma resolución.

Construye un HTML side-by-side con la implementación a la izquierda y la referencia a la derecha. Captura ese HTML para tener una vista única de comparación.

### Paso 3 — Mide y reporta discrepancias

Para cada elemento clave (h1, primer párrafo, primer input, último form group, botones), captura en ambas páginas:
- `font-size` y `line-height` (tipografía)
- `margin-top` y `margin-bottom` (espaciado vertical)
- `width` del primer input (anchura)

**No asumas "se ve igual". Mide.** Las discrepancias de 1-3px son ruido del navegador; las de 4-12px son afinables; las de >12px requieren atención.

Presenta al usuario una tabla como esta:

| # | Elemento | Referencia | Implementación | Δ | Categoría |
|---|---|---|---|---|---|
| 1 | gap h1 → lead | 12px | -8px | -20px | 🔴 bloqueante |
| 2 | lead font-size | 16px | 18px | +2px | 🟡 afinable |
| 3 | input width | 936px | 499px | -437px | 🔴 bloqueante |

### Paso 4 — Espera OK del usuario

**No apliques fixes automáticamente.** Cada discrepancia puede tener un "vale, arréglalo" o un "no merece la pena, déjalo así". Espera el visto bueno explícito.

### Paso 5 — Aplica el fix mínimo

Para cada discrepancia aprobada:
- Aplica el cambio más simple que la resuelva (un `mb-0`, un `-mt-base`, un cambio de clase)
- Re-captura y re-mide para verificar
- Si la diferencia se reduce a < 4px, márcala como "resuelta"
- Si no se resuelve, hay causa más profunda (margen de padre, padding de contenedor, font-size heredado) — vuelve al checklist del Paso 3

### Paso 6 — Confirmación explícita

La página solo está "terminada" cuando el usuario lo confirma. La 1ª pasada es "esqueleto listo", no "página lista". No te auto-declares terminado.

## Tipos de referencia

### HTML servible (gold del benchmark, otra página ya construida)

**Ventaja:** puedes inspeccionar el DOM directamente. Tienes acceso a todas las APIs de estilos computados del navegador (`getComputedStyle` en DevTools, equivalente en cualquier browser-automation library).

Cómo medir (genérico):
1. Sirve el HTML en un puerto local
2. Captura el screenshot con la herramienta que tengas
3. Inspecciona con cualquier API que devuelva los estilos computados del navegador
4. Compara con tu implementación elemento a elemento

### Imagen bitmap (mockup, screenshot de Figma, JPG/PNG sin DOM)

**Limitación:** no hay DOM que inspeccionar. Tienes que analizar píxeles.

Cómo medir:
1. Captura tu implementación con la herramienta que tengas
2. **Análisis visual con un LLM con capacidad de visión** (pásale la imagen y pregúntale: "qué distancia hay entre X e Y en píxeles", "qué font-size aproximado tiene este h1", "qué grosor de margen hay entre estos dos bloques")
3. **Análisis pixel-art con una herramienta de diff de imágenes** (PIL, ImageMagick, o similar) — para medir distancias exactas entre regiones y encontrar bordes
4. Combina ambos: el LLM te da la lectura cualitativa, el pixel-art te da la cuantitativa

**Tolerancia:** menos preciso que DOM. Apunta a ±2-3px de precisión, no ±0.5px.

## Cómo investigar discrepancias (checklist)

Cuando veas "esto se ve raro", recorre esta lista en orden:

1. **¿El elemento existe?** A veces un componente no renderiza por un binding roto. Inspecciona el DOM (HTML servible) o la captura (bitmap).
2. **¿El font-size coincide?** Compara con la tabla de medidas canónicas. Si tu implementación usa una utility distinta (e.g. `text-lg` en vez de `c-paragraph-lg`), corrígelo.
3. **¿El line-height coincide?** A veces el `leading-tight` o `leading-normal` cambia la altura del bloque aunque el font-size sea correcto.
4. **¿Los márgenes verticalesson los de la tabla?** Sobreescribir `mb-sm` cuando el canónico es `mb-lg` es un anti-pattern común.
5. **¿Hay márgenes que se cancelan?** Un `mb-X` en el padre y un `-mt-Y` en el hijo pueden dar gaps no intencionales. Inspecciona ambos.
6. **¿El padding del contenedor afecta?** A veces un `py-base` o `py-xl` en el wrapper cambia la distancia entre el h1 y el siguiente bloque.
7. **¿Es ruido del navegador?** Si la diferencia es < 4px y no hay causa obvia, probablemente es sub-pixel rendering. Déjalo.

## Anti-patterns

- ❌ **Aplicar `mb-sm` a un `c-h1` "porque queda mejor"** sin medir. El design system ya da `mb-lg` por una razón. Si necesitas otro valor, mídelo contra la referencia primero.
- ❌ **Asumir que "el design system tiene la verdad"** sin comparar con la referencia. Las páginas específicas pueden salirse de los defaults canónicos.
- ❌ **Sobreescribir 4-5 márgenes de una pasada** sin verificar cada uno por separado. Cambios aislados son más fáciles de revertir.
- ❌ **"Está suficientemente bien"** cuando hay > 4px de desviación visible. El usuario nota 4px en un header; 8px lo nota todo el mundo.
- ❌ **Capturar solo tu implementación** (sin la referencia al lado). Sin referencia, no hay forma de saber si hay discrepancia.
- ❌ **Aplicar el fix sin esperar OK.** El usuario puede preferir "déjalo así" si la discrepancia es menor.
- ❌ **"Es ruido del navegador" cuando es > 4px.** El sub-pixel rendering explica 1-2px, no 8-12px.

## Caso de estudio: wizard de 3 pasos (h1 + lead)

Ilustra el workflow completo de este skill, de 1ª pasada a fidelidad total. Útil como referencia para páginas con la misma estructura (h1 + lead introductorio + form).

### Punto de partida (1ª pasada "terminada")

El esqueleto se hizo aplicando los overrides que parecían razonables: `mb-sm` en el h1, `mb-base` en el lead, etc. ng build pasaba, lint pasaba, 0 console errors. Pero el visual "se veía raro" sin saber decir qué.

### Aplicación del workflow

**Paso 2 (verificación):** captura side-by-side contra el gold. **A primera vista** todo "parece" igual, pero al hacer zoom se ve que el párrafo "Necesitamos..." está **pegado al h1 en la versión angular, separado en el gold**.

**Paso 3 (medir):** tabla de discrepancias con `getComputedStyle` del navegador:

| # | Elemento | Gold | Angular | Δ | Categoría |
|---|---|---|---|---|---|
| 1 | h1.fontSize | 30px | 30px | 0 | 🟢 trivial |
| 2 | h1.mb | 28px | 8px | +20 | 🔴 bloqueante |
| 3 | lead.fontSize | 18px | 18px | 0 | 🟢 trivial |
| 4 | lead.mt | -16px | -16px | 0 | 🟢 trivial |
| 5 | lead.mb | 28px | 16px | +12 | 🔴 bloqueante |
| 6 | gap h1→lead | 12px | -8px (overlap) | +20 | 🔴 bloqueante |

**Diagnóstico:** tres bloqueantes, dos de los cuales tienen el mismo origen (h1.mb). El "gap negativo" es consecuencia directa del h1.mb demasiado bajo.

### Fixes (2 líneas, 0 efectos colaterales)

```diff
- <h1 class="c-h1 w-full mb-sm">Datos de identidad</h1>
+ <h1 class="c-h1 w-full">Datos de identidad</h1>

- <p class="c-paragraph-lg mb-base">Necesitamos estos datos...</p>
+ <p class="-mt-base c-paragraph-lg mb-lg">Necesitamos estos datos...</p>
```

**Por qué funciona:** el gold tiene `c-h1` sin override (mb-lg 28px natural) + `-mt-base` (-16px) en el lead. La combinación `mb-lg + grid-gap - mt-base` da 12px limpios. Mi versión había sobreescrito el `mb-lg` natural con `mb-sm` (8px) y usado `mb-base` (16px) en el lead —破坏了 la fórmula y causaba overlap.

### Verificación tras el fix

Las 5 métricas quedan en Δ=0 entre gold y angular. ng build pasa, lint pasa, 0 console errors, contadores coinciden (7 inputs, 3 selects, 1 checkbox, 6 fieldsets, etc.). Tiempo total: ~10 minutos desde 1ª pasada a fidelidad total.

### Lección reutilizable

> **El "mb-sm en h1" es un anti-pattern común.** Cuando veas un h1 con un override de margin-bottom, comprueba primero que el siguiente elemento no use `-mt-X` para contrarrestar el `mb-lg` natural. Si lo hace, el override rompe la fórmula. El patrón "c-h1 sin override + lead con -mt-base" es el idiomático en este design system.

## Snippets genéricos

> **Estos snippets son ejemplos conceptuales. Adapta la sintaxis exacta a la herramienta de captura y al LLM que tengas disponibles. Lo importante es la idea, no la API concreta.**

### Capturar screenshot de la implementación

```js
// Pseudocódigo. Adapta a tu herramienta (Puppeteer, Playwright, browser-automation, etc.)
const browser = abrirBrowser({ viewport: { width: 1280, height: 1024 } });
const page = browser.newPage();
await page.goto('http://localhost:PUERTO/ruta/pagina');
await page.esperar({ tiempo: 2000 }); // dar tiempo a fuentes y animaciones
await page.capturarScreenshot({ path: 'implementacion.png', fullPage: true });
browser.cerrar();
```

### Capturar screenshot de la referencia (HTML servible)

```js
// Igual que arriba, apuntando al URL donde sirves la referencia
await page.goto('http://localhost:OTRO_PUERTO/ruta/gold.html');
```

### Inspeccionar estilos computados (HTML servible)

```js
// Pseudocódigo. Equivale a getComputedStyle en DevTools del navegador.
const medidas = await page.evaluar(() => {
  const h1 = document.querySelector('h1');
  const lead = document.querySelector('p.lead, .lead, p[class*="-mt-base"]');
  const input = document.querySelector('input[type="text"]');
  return {
    h1: { fontSize: getComputedStyle(h1).fontSize, marginBottom: getComputedStyle(h1).marginBottom },
    lead: { fontSize: getComputedStyle(lead).fontSize, marginTop: getComputedStyle(lead).marginTop },
    input: { width: getComputedStyle(input).width },
  };
});
```

### Comparar dos PNGs con un LLM visión (bitmap)

```js
// Pseudocódigo. Adapta al SDK de tu LLM.
// Pásale ambas imágenes al LLM con un prompt como:
// "Compara estas dos capturas. La de la izquierda es la referencia, la de la derecha es mi implementación.
//  Mide las siguientes distancias en píxeles:
//    - bottom del h1 → top del primer párrafo
//    - height del primer input
//    - cualquier otra discrepancia visual notable (font-size, márgenes, alineaciones)
//  Devuelve una tabla con las medidas de cada lado y la diferencia."
```

### Construir side-by-side

```js
// Pseudocódigo. Genera un HTML con dos imágenes lado a lado, ábrelo en browser, captura.
const html = `<html><body style="display:flex; gap:8px; background:#1f2331; margin:0; padding:16px">
  <div style="flex:1"><img src="gold.png" style="width:100%; display:block"></div>
  <div style="flex:1"><img src="implementacion.png" style="width:100%; display:block"></div>
</body></html>`;
// Guardar el HTML en disco, abrirlo con la misma herramienta de captura, guardar el screenshot.
```

## Related

- `desy-styles-reference` — fuente de verdad de los tokens (colores, spacing, tipografía)
- `desy-implement-component` — para generar el código Nunjucks inicial
- `desy-angular-translator` — para traducir Nunjucks a Angular
- `desy-validate-accessibility` — para validar WCAG 2.2 AA tras la implementación
- `desy-component-recognizer` — para identificar qué componentes usar en un mockup
