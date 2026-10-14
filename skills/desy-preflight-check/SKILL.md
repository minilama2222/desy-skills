---
name: desy-preflight-check
description: "Pre-flight check obligatorio antes de cualquier tarea DESY. Verifica si existe proyecto DESY, identifica la librería (desy-html / desy-angular / desy-ionic), detecta la versión instalada. Si no hay proyecto, bifurca al flujo scaffold con permiso del usuario. Invocar SIEMPRE antes de desy-choose-library, desy-choose-page-template, desy-implement-pattern o cualquier skill de implementación."
---

# desy-preflight-check

Verifica el estado del proyecto antes de planificar cualquier tarea DESY. Es la **primera skill que se debe cargar** en una sesión de trabajo DESY, sin excepciones.

> 🎯 **Para el agente:** esta skill existe porque el patrón detectado en sesiones reales (junio-julio 2026) muestra que un agente cargado con skills DESY tiende a saltar directo a `desy-choose-library` o `desy-implement-pattern` sin verificar si el proyecto existe. Resultado: planificar 6 pasos de implementación sobre una carpeta vacía. Esta skill cierra ese gap con un check explícito de runtime.

## Cuándo usarla
- **Triggers:** *"maqueta esta página con DESY"*, *"implementa X con desy-html"*, *"crea un componente DESY"*, *"tengo esta imagen / mockup, hazme la página"*, *"añade una página a mi proyecto DESY"*.
- **Cargar:** SIEMPRE al iniciar tarea DESY, antes de `desy-choose-library` + `desy-implement-*`.
- **NO usar para:** usuario ya dio contexto explícito (librería + repo + ruta) y se va directo a `desy-implement-pattern`; tarea puramente conceptual; validar output ya implementado (→ `desy-validate-accessibility` o `desy-design-match`).

## Posición en el workflow DESY

Paso **0** y **orquestador** de la cadena. Esta skill no termina al detectar el proyecto: decide qué skills se cargan después y en qué orden. Cada paso de la tabla es una **invocación de la herramienta `Skill`**, no un recordatorio: leer el nombre de una skill no la carga.

**Secuencia obligatoria para maquetar una página DESY:**

| # | Invoca | Cuándo | Por qué |
|---|---|---|---|
| 1 | `desy-component-recognizer` | Si hay imagen de referencia | Decide componente, variante, tamaño y fieldsets antes de escribir código |
| 2 | `desy-choose-page-template` | Siempre | La plantilla trae header, footer y el espacio superior del contenido |
| 3 | `desy-implement-pattern`, `desy-implement-layout-patterns`, `desy-implement-component` | Según la tabla del recognizer: patrón, estructura (fieldset, grid, acciones) o componente suelto | Las reglas de fieldset, acciones de página, tamaños y anchos están ahí |
| 4 | `desy-design-match` | Siempre que haya imagen, antes de dar la página por terminada | Mide tipografía, anchos y márgenes contra la referencia y los lleva al token |
| 5 | `desy-validate-accessibility` | Siempre, al final | Checklist sin servidor: fieldsets, un solo h1, labels, skip-link |
| — | `desy-styles-reference` | Cada vez que vayas a escribir una clase de utilidad que no sale de una macro (`mb-`, `gap-`, `w-`, `max-w-`, `grid-cols-`, `text-`) | Evita Tailwind por defecto y valores arbitrarios en px |

Si `PROYECTO_NO_EXISTE`, antes va `desy-scaffold-project` (Paso 2). `desy-choose-library` solo si la librería no está decidida. Si el destino es `desy-angular`, `desy-angular-translator` va después del paso 5.

**Regla:** la página **no está terminada** hasta haber invocado `desy-design-match` y `desy-validate-accessibility` y haber pasado el checklist de salida (Paso 5). Un build en verde no es «terminado».

## Cómo aplicar

### Paso 1: Detección de existencia del proyecto

Ejecuta este check desde la raíz del directorio de trabajo:

```bash
test -f package.json && test -d node_modules && echo "PROYECTO_OK" || echo "PROYECTO_NO_EXISTE"
```

Si el directorio tiene subcarpetas con `package.json` (monorepo), pregunta al usuario cuál es la raíz del proyecto DESY.

### Paso 2: Si PROYECTO_NO_EXISTE → bifurcar al scaffold

**Comportamiento esperado:** el agente NO debe seguir planificando implementación. En su lugar:

1. Pregunta al usuario: *"El directorio está vacío (o no tiene un proyecto DESY clonado). ¿Quieres que clone el starter oficial de [librería detectada o preguntada]?"*
2. Si el usuario confirma, invoca `desy-scaffold-project` para arrancar el proyecto.
3. Si el usuario prefiere hacerlo manualmente, pasa los comandos del bloque `## Setup inicial` de `desy-scaffold-project` y espera a que termine.

**Por qué este paso es obligatorio:** sin starter clonado, no hay `node_modules/desy-html` (o `desy-angular`/`desy-ionic`), y por tanto no se pueden usar los macros, los SVGs ni los tokens del proyecto. Generar HTML "a ojo" produce un output que **no se compila** con la toolchain oficial.

### Paso 3: Si PROYECTO_OK → identificar contexto

Lee el `package.json` y reporta:

```bash
jq '{ name: .name, desy_html: .dependencies["desy-html"] // .devDependencies["desy-html"], desy_angular: .dependencies["desy-angular"] // .devDependencies["desy-angular"], desy_ionic: .dependencies["desy-ionic"] // .devDependencies["desy-ionic"], scripts_dev: .scripts.dev, scripts_build: .scripts.build }' package.json
```

Devuelve al usuario:

- **Proyecto:** `<name>` del `package.json`
- **Librería detectada:** desy-html / desy-angular / desy-ionic / mixta (anomalía)
- **Versión:** semver instalada (de `dependencies` o `devDependencies`)
- **Comando dev:** `npm run dev` o el que esté definido
- **Comando build:** `npm run build` o `npm run build-prod` o el equivalente

### Paso 4: Encadena las skills con `Skill`

Con el proyecto identificado, invoca con la herramienta `Skill` las skills de la secuencia de «Posición en el workflow DESY», en ese orden:

1. Si hay imagen (screenshot, mockup, `referencia.png`): `desy-component-recognizer` **antes** de escribir código. Su tabla de salida (componente, variante, tamaño, fieldset) es la lista de trabajo.
2. `desy-choose-page-template`.
3. Las skills de implementación que pida la tabla del recognizer.
4. `desy-design-match` y `desy-validate-accessibility` al final, aunque la página «se vea bien».

Si NO hay imagen, empieza en el punto 2.

### Paso 5: Checklist de salida (antes de decir «terminado»)

Cada comando tiene que dar el resultado indicado. Si no lo da, vuelve a la skill que se indica.

```bash
# 1. Un fieldset por grupo de campos y por checkbox legal (HTML compilado): ≥ nº de grupos
#    → desy-implement-layout-patterns
grep -c '<fieldset' dist/<pagina>.html

# 2. Exactamente un h1 (HTML compilado): 1 → desy-validate-accessibility
grep -o '<h1[ >]' dist/<pagina>.html | wc -l

# 3. Ni valores arbitrarios ni escala numérica de Tailwind en las clases que escribiste
#    (fuente de la página): vacío → desy-styles-reference
grep -oE '(class=|\"classes\": )\"[^\"]*\"' src/<pagina>.html | grep -E '\[[^]]+\]|\b[mp][trblxy]?-[1-9]|\bgap(-[xy])?-[0-9]|[a-z0-9]!( |\")'
```

- [ ] He invocado `desy-design-match` y comparado con la referencia al mismo viewport (1280 px de ancho).
- [ ] He invocado `desy-validate-accessibility` y pasado su checklist sin servidor.
- [ ] Las acciones de página («Volver», «Cancelar», «Ver más») son `c-button c-button--transparent`, no `c-link`.

## Errores típicos que evita
- ❌ **Planificar implementación sobre carpeta vacía**: sesión OCX julio 2026 (maqueta 404 Portal Salud) planeó 6 pasos sobre `attached_assets/` sin verificar. Tuvo que retroceder.
- ❌ **Asumir librería sin verificar**: el agente salta directo a `desy-choose-library` cuando ya hay Angular 19 en pie.
- ❌ **Asumir versión outdated**: sin leer `package.json`, el agente puede usar APIs de una versión no instalada.
- ❌ **HTML estático "a ojo"** sin starter clonado: el output no se compila, no usa macros reales (anti-patrón detectado en benchmarks 2026-06-07).
- ❌ **Saltarse el check por pereza**: "el usuario ya dijo desy-html, no hace falta verificar".

## Siguiente skill típica
→ Si preflight = NO_EXISTE: `desy-scaffold-project` → volver a invocar `desy-preflight-check` para re-verificar.
→ Si preflight OK: la secuencia de «Posición en el workflow DESY», empezando por `desy-component-recognizer` si hay imagen y terminando **siempre** en `desy-design-match` + `desy-validate-accessibility`.

## Anti-patterns

- ❌ Saltarse esta skill "porque el usuario ya dijo la librería". El usuario puede equivocarse o el proyecto puede haber cambiado desde la última sesión.
- ❌ Asumir que una carpeta con `node_modules` significa proyecto DESY. Verificar `package.json` + `desy-html` / `desy-angular` / `desy-ionic` en deps.
- ❌ En monorepos, asumir que la raíz es el proyecto DESY. Preguntar.
- ❌ Continuar planificando 5 pasos de implementación cuando preflight devolvió NO_EXISTE. La cadena se rompe en ese punto — bifurcar a scaffold.
- ❌ Confundir "directorio con archivos sueltos" (ej. solo `attached_assets/` o `README.md`) con proyecto DESY. El criterio es `package.json` + `node_modules/<librería>`.

## Related

- **Skill: `desy-scaffold-project`** — siguiente paso si preflight = NO_EXISTE.
- **Skill: `desy-choose-library`** — siguiente paso si preflight OK y no hay imagen.
- **Skill: `desy-component-recognizer`** — siguiente paso si preflight OK y hay imagen.
- **Mapa del ecosistema DESY:** `docs/ecosystem-map.md` (en este repo).
- **Doc oficial:** https://desy.aragon.es/como-empezar-tutorial.html.md