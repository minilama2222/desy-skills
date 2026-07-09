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
Paso **0** de la cadena canónica — debe ejecutarse SIEMPRE antes del paso 1. No tiene paso anterior; es el punto de entrada.

```
[desy-preflight-check]                ← ESTÁS AQUÍ
   │
   ├── si PROYECTO_NO_EXISTE → [desy-scaffold-project]
   │
   └── si PROYECTO_OK → reporte contexto y continúa
            ↓
       [desy-component-recognizer]    ← paso 0.5 (solo si hay imagen)
            ↓
       [desy-choose-library]          ← paso 1
            ↓
       [desy-choose-page-template]    ← paso 2
            ↓
       [desy-scaffold-project]        ← paso 3 (si preflight OK, omitir)
            ↓
       [desy-implement-pattern / implement-component / implement-layout-patterns]  ← pasos 4-6
            ↓
       [desy-design-match]            ← paso 7
            ↓
       [desy-validate-accessibility]  ← paso 8
            ↓ (si target es desy-angular)
       [desy-angular-translator]      ← paso 9
            ↓ (on-demand durante todo el flujo)
       [desy-styles-reference]        ← consulta de tokens
```

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

### Paso 4: Si hay imagen de referencia → cargar component-recognizer

Si el usuario proporcionó una imagen (screenshot, mockup, gold), invoca `desy-component-recognizer` con esa imagen **antes** de continuar con `desy-choose-page-template`. Esto identifica qué componentes del catálogo hay que usar y evita improvisar placeholders.

Si NO hay imagen, salta directamente a `desy-choose-library`.

## Errores típicos que evita
- ❌ **Planificar implementación sobre carpeta vacía**: sesión OCX julio 2026 (maqueta 404 Portal Salud) planeó 6 pasos sobre `attached_assets/` sin verificar. Tuvo que retroceder.
- ❌ **Asumir librería sin verificar**: el agente salta directo a `desy-choose-library` cuando ya hay Angular 19 en pie.
- ❌ **Asumir versión outdated**: sin leer `package.json`, el agente puede usar APIs de una versión no instalada.
- ❌ **HTML estático "a ojo"** sin starter clonado: el output no se compila, no usa macros reales (anti-patrón detectado en benchmarks 2026-06-07).
- ❌ **Saltarse el check por pereza**: "el usuario ya dijo desy-html, no hace falta verificar".

## Siguiente skill típica
→ Si preflight OK y no hay imagen: `desy-choose-library` (paso 1) → `desy-choose-page-template` (paso 2).
→ Si preflight OK y hay imagen: `desy-component-recognizer` (paso 0.5) → `desy-choose-library` (paso 1).
→ Si preflight = NO_EXISTE: `desy-scaffold-project` → volver a invocar `desy-preflight-check` para re-verificar.

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