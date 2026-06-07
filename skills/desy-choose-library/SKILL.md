---
name: desy-choose-library
description: "Decide between desy-html, desy-angular, and desy-ionic. Use when starting or migrating a DESY project, or evaluating library choice."
---

# desy-choose-library

Ayuda a un equipo a decidir qué librería DESY usar para un proyecto nuevo, una migración, o una evaluación de stack. Considera el tipo de producto, el perfil del equipo, los requisitos no funcionales y la publicación objetivo.

## Regla fundamental (lee esto antes de recomendar)

> **Nunca se usa la librería directamente. Siempre se parte del starter oficial, que la tiene como dependencia.**

| Si el usuario dice... | Lo correcto es... | Lo incorrecto es... |
|---|---|---|
| "Quiero usar desy-html" | Clonar `desy-html-starter` de Bitbucket, `npm install`, personalizar | `npm install desy-html` en un proyecto vacío |
| "Quiero usar desy-angular" | Clonar `desy-angular-starter` de Bitbucket, `npm install`, personalizar | `npm install desy-angular` en un proyecto vacío |
| "Quiero usar desy-ionic" | Clonar `desy-ionic` de Bitbucket, `npm install`, personalizar | `npm install @ionic/angular` en un proyecto vacío |

La razón: cada starter es un **proyecto scaffolded** con la toolchain ya configurada (Nunjucks+Vite, Angular CLI, Ionic CLI+Capacitor), la estructura de directorios correcta, y la convención de build probada. Instalar la librería directamente deja al agente (o al humano) re-implementando todo eso desde cero, con paths y builds que no van a funcionar. **El starter ES la forma de usar la librería.**

El output esperado de cualquier proyecto DESY es siempre el `dist/` generado por el toolchain del starter correspondiente (`npm run build` con Vite para desy-html, `npm run build-prod` con Angular CLI para desy-angular, `npm run build` con Ionic CLI para desy-ionic).

## When to use this skill

- El equipo va a empezar un proyecto con DESY y no sabe qué librería encaja
- Hay que migrar código existente a DESY
- Hay que evaluar pros/contras antes de comprometerse a un stack
- El equipo duda entre dos librerías y necesita una decisión razonada

## Decision framework (3 preguntas)

### Pregunta 1: ¿Qué tipo de producto?

| Producto | Cabecera | Librería recomendada |
|---|---|---|
| **Sitio web / portal** (contenido público, comunicación unidireccional) | `header-advanced` (3 bandas) | **desy-html** |
| **Webapp** (CRUD, gestión, datos, autenticación) | `header` estándar (1 banda) | **desy-angular** o **desy-ionic** (móvil) |
| **App móvil nativa iOS/Android** | `header-mobile` | **desy-ionic** |
| **App híbrida** (móvil + web con un solo codebase) | `header-mobile` + `header` | **desy-ionic** |

Las 3 librerías comparten la misma identidad visual DESY, pero cada una tiene propósito, stack y casos de uso óptimos.

### Pregunta 2: ¿Cuál es el perfil del equipo y stack?

| Perfil del equipo | Recomendación |
|---|---|
| Maquetadores con experiencia HTML/CSS, sin JS frameworks | **desy-html** |
| Equipo con sólidos conocimientos de Angular 16+ | **desy-angular** (apunta a Angular 19 latest) |
| Equipo con Angular + quiere publicar en App Store / Play Store | **desy-ionic** (incluye Capacitor para builds nativas) |
| Stack legacy a migrar poco a poco (sitio estático, web components) | Empezar con **desy-html** |
| Necesidad de mantener LTS en producción | **desy-angular v13** (Angular 16, solo bugfixes críticos) |

**Relación entre las 3:** cada versión de `desy-angular` apunta a una versión específica de `desy-html` (ver [tabla de versiones](https://desy.aragon.es/desarrollo-versiones.html)). Los parámetros de config y el diseño de componentes nacen en `desy-html` y luego se traducen a `desy-angular`. `desy-ionic` añade los suyos propios para interacción táctil.

### Pregunta 3: ¿Requisitos no funcionales?

| Requisito | Si sí | Si no |
|---|---|---|
| **SEO crítico** (portales, webs públicas) | **desy-html** (mejor para indexación) | da igual |
| **Carga rápida en 3G / SEO / Core Web Vitals** | **desy-html** (más ligero, sin runtime JS) | da igual |
| **Autenticación centralizada** (DIGA, MFE en Gobierno de Aragón) | **desy-angular** o **desy-ionic** | desy-html vale |
| **Accesibilidad WCAG 2.2 AA obligatoria** | Las 3 lo cumplen, da igual | da igual |
| **Publicación en stores** (iOS / Android) | **desy-ionic** (con Capacitor) | da igual |
| **Funciona offline / en avión** | **desy-ionic** (Capacitor + storage) | da igual |
| **Gestión de contenido por personas no técnicas** | **desy-html** + Liferay/WordPress si aplica | depende |
| **Interacción táctil rica** (gestos, swipe, vibración) | **desy-ionic** | desy-angular |

## Workflow

1. **Identifica el producto** con la pregunta 1
2. **Cruza con el perfil del equipo** (pregunta 2)
3. **Aplica los requisitos no funcionales** (pregunta 3)
4. **Recomienda** la librería
5. **Documenta la decisión** y enlaza al starter correspondiente
6. **Verifica** con el equipo la versión concreta a usar (latest vs LTS)

## Output esperado

Una recomendación clara con:
- Librería elegida + versión (latest o LTS)
- Starter de Bitbucket a usar
- Comando de instalación inicial
- Plantilla de DESY a considerar
- Cabecera recomendada según tipo de producto
- URLs a la documentación relevante
- Próximos pasos (siguiente skill: `desy-scaffold-project`)

## Examples

### Ejemplo 1: Portal web de información turística

**Contexto:**
- Portal público del Gobierno de Aragón
- SEO crítico, accesibilidad WCAG 2.1 AA
- Equipo de 3 maquetadores con HTML/CSS pero sin Angular
- Backend ya tiene WordPress/Liferay
- Sin autenticación

**Decisión razonada:**
- Pregunta 1 → Sitio web/portal → **desy-html**
- Pregunta 2 → Sin Angular, equipo maquetador → confirma **desy-html**
- Pregunta 3 → SEO crítico, accesibilidad, sin auth → confirma **desy-html**

**Output:**

```yaml
librería: desy-html (latest)
starter: https://bitbucket.org/sdaragon/desy-html-starter
cabecera: header-advanced (3 bandas)
plantilla: plantillas-portal-p1.html

setup:
  - git clone https://bitbucket.org/sdaragon/desy-html-starter.git mi-portal
  - cd mi-portal
  - npm install
  - npm run dev
  - npm run build

próximo_skill: desy-scaffold-project
plantillas_a_revisar: [plantillas-portal-p1.html]
```

**Notas:**
- El proyecto se integra con WordPress/Liferay para gestión de contenido. Si el equipo necesita maquetar desde CMS, desy-html permite incluir las plantillas DESY dentro del tema del CMS.
- Accesibilidad: aplicar el checklist WCAG 2.2 AA (no saltarse). Revisar con el [libro de Olga Carreras](https://olgacarreras.blogspot.com/2024/02/libro-accesibilidad-web-wcag-22-de.html).
- Mantenimiento: como la librería avanza, fijar versión específica en `package.json` y actualizar con cuidado.

### Ejemplo 2: Webapp de gestión de expedientes

**Contexto:**
- Aplicación interna para funcionarios
- Login con DIGA (MFE del Gobierno de Aragón)
- Tablas con paginación, filtros, acciones en lote
- CRUD sobre entidades (expedientes, documentos)
- Equipo con Angular 16+, 4 devs
- Backend REST ya existe

**Decisión razonada:**
- Pregunta 1 → Webapp → **desy-angular**
- Pregunta 2 → Equipo con Angular → confirma **desy-angular**
- Pregunta 3 → Autenticación centralizada, CRUD complejo → confirma **desy-angular**

**Output:**

```yaml
librería: desy-angular (latest, Angular 19)
starter: https://bitbucket.org/sdaragon/desy-angular-starter
cabecera: header estándar
plantilla: plantillas-con-sesion-iniciada.html
lts_alternativa: desy-angular v13 (Angular 16) si necesitas LTS

setup:
  - git clone https://bitbucket.org/sdaragon/desy-angular-starter.git mi-webapp
  - cd mi-webapp
  - # Renombrar ocurrencias de 'desy-angular-starter' por el nombre del proyecto
  - # Archivos: angular.json, karma.conf.js, package.json, index.html
  - npm install --legacy-peer-deps
  - npm run dev
  - npm run build-prod
  - npm run e2e   # Playwright tests

próximo_skill: desy-scaffold-project
componentes_clave:
  - tabla avanzada (con filtros, ordenación, acciones en lote)
  - input (autocomplete con datos de DIGA)
  - modal (confirmaciones de acciones destructivas)
  - notifcaciones (feedback de operaciones)
  - paginación
patrones_a_usar:
  - acciones-de-tabla (acciones en lote)
  - filtros (ordenación, búsqueda)
  - paginación
  - avanzar-retroceder (si hay wizards)
```

**Notas:**
- Los patrones `acciones-de-tabla` y `filtros` son CRÍTICOS para la UX de una webapp con muchas filas. No reinventar.
- La plantilla `plantillas-con-sesion-iniciada.html` da la estructura base de layout para apps autenticadas.
- Si el equipo no está familiarizado con Tailwind dentro de Angular, hacer un training corto antes. La mayoría de los estilos en desy-angular son utility classes.

### Ejemplo 3: App móvil nativa para ciudadanía

**Contexto:**
- App que los ciudadanos se bajan del App Store y Play Store
- Acceso a sus datos personales (DNI, notificaciones)
- Formularios offline-friendly (solicitudes desde el móvil)
- Notificaciones push
- Equipo con Angular, primer proyecto móvil

**Decisión razonada:**
- Pregunta 1 → App móvil → **desy-ionic**
- Pregunta 2 → Equipo con Angular + quieren publicar → confirma **desy-ionic**
- Pregunta 3 → Publicación en stores, offline, interacción táctil → confirma **desy-ionic**

**Output:**

```yaml
librería: desy-ionic (storybook en https://desy.aragon.es/desy-ionic)
stack: Ionic + Angular + Capacitor (iOS/Android)
cabecera: header-mobile
plantilla: pending (desy-ionic tiene sus propias plantillas para móvil)
figma: https://www.figma.com/community/file/1383376074462615538/desy-ionic

setup:
  - git clone https://bitbucket.org/sdaragon/desy-ionic.git mi-app
  - cd mi-app
  - npm install
  - # Para builds nativas:
  - npx cap add ios
  - npx cap add android
  - npm run build && npx cap sync
  - npx cap open ios     # abre Xcode
  - npx cap open android # abre Android Studio

próximo_skill: desy-scaffold-project
componentes_clave_movil:
  - header-mobile (cabezera específica para móvil)
  - action-sheet (menú contextual)
  - list-mobile (listas con swipe)
  - tabs (navegación inferior)
  - pull-to-refresh
consideraciones_especiales:
  - gestos: usar directivas de Ionic
  - accesibilidad táctil: target >= 44x44px
  - notificaciones push: configurar Capacitor
  - almacenamiento local: Capacitor Storage o SQLite
```

**Notas:**
- desy-ionic es la única de las 3 librerías que tiene directrices específicas de móvil (gestos, vibración, target size).
- Los storybooks (`/desy-ionic`) tienen demos interactivos — usarlos como referencia visual antes de empezar.
- El equipo debe conocer Capacitor (que envuelve Cordova con mejor DX). Si no, training previo.

## Anti-patterns (lo que NO hacer)

- **No mezclar librerías en el mismo proyecto.** Si empiezas con desy-html, no añadas desy-angular para "complementar". Complica mantenimiento y versionado.
- **No elegir desy-angular para un portal estático.** Overhead de Angular + mantenimiento de versiones para un sitio que no lo necesita.
- **No elegir desy-html para una webapp con auth y CRUD.** Terminarás escribiendo tu propio framework encima de Nunjucks. Mal.
- **No ignorar la tabla de versiones.** desy-angular v13 (Angular 16) no tiene las mismas features que desy-angular v19.
- **No asumir que las 3 son intercambiables.** Visualmente similares, técnicamente muy distintas.

## Gotchas

- **Pregunta 1 (tipo de producto) es la más importante.** El equipo muchas veces la salta y va directo a "¿cuál conozco mejor?" — eso es backwards. Empieza siempre por el tipo de producto.
- **El equipo con Angular 16 NO equivale a equipo con desy-angular v13 LTS.** El LTS de DESY actualiza con menos frecuencia que Angular upstream. Verificar siempre la [tabla de versiones](https://desy.aragon.es/desarrollo-versiones.html).
- **No recomendar desy-ionic si el equipo no va a publicar en stores.** El overhead de Capacitor, Xcode/Android Studio, y builds nativas no compensa si el deliverable es solo web.
- **Si el equipo tiene "experiencia con HTML" pero no con Tailwind, desy-html puede ser duro al principio.** El starter ya tiene Tailwind pre-configurado pero requiere familiaridad. Ofrecer un quickstart de Tailwind si dudan.
- **Para portales institucionales grandes, considera hosting y mantenimiento.** desy-html con Vite genera estáticos que se pueden servir desde cualquier CDN. desy-angular requiere Node en producción. La decisión afecta operaciones, no solo desarrollo.
- **El starter de Bitbucket puede estar desactualizado respecto a la doc oficial.** Antes de empezar, comparar la versión del starter con la [tabla de versiones](https://desy.aragon.es/desarrollo-versiones.html).
- **"Quiero SEO crítico pero con autenticación" — colisión de requisitos.** El orden de preguntas resuelve esto: si el producto es un **portal público con login opcional** (ej: zona privada para usuarios registrados pero la mayoría del contenido es público e indexable), entonces **desy-html** es lo correcto — la auth se puede resolver con un subdominio o ruta `/app/*` servida por una SPA aparte. Si por el contrario es una **webapp de gestión cuyo contenido debe indexarse** (ej: buscador interno de expedientes), entonces **desy-angular** con SSR (Angular Universal) es preferible aunque requiera más setup. No existe una opción "SEO + auth total" en DESY: forzar desy-html con auth compleja o desy-angular con SEO crítico es antipatrón. Confirmar con el equipo si el SEO es para el contenido público o para el contenido autenticado, porque la respuesta cambia la librería.

## Related

- **Skill: `desy-scaffold-project`** — siguiente paso, setup del proyecto
- **Skill: `desy-implement-component`** — siguiente paso, generar código de un componente
- **Doc oficial:** https://desy.aragon.es/como-empezar-tutorial.html.md
- **Índice completo:** https://desy.aragon.es/llms.txt
- **Mapa del ecosistema DESY:** [`/docs/ecosystem-map.md`](../../docs/ecosystem-map.md) (en este repo)
- **Tabla de versiones:** https://desy.aragon.es/desarrollo-versiones.html
- **Repos en Bitbucket:** https://bitbucket.org/sdaragon/

## Si el resultado de la decisión no encaja en ninguna de las 3

A veces la respuesta correcta es **no usar DESY**. Algunos casos donde conviene evaluar otras opciones:

- Proyecto con animaciones pesadas o canvas/WebGL → evaluar frameworks especializados (Three.js, Pixi.js) con componentes DESY solo para chrome
- Web con rendering en el servidor (SSR) para SEO extremo → Next.js o similar, no encaja con desy-html/angular/ionic
- Landing pages one-shot con CMS sin maquetadores → consider solo CSS + Figma, sin librería

**Pero:** casi siempre hay una forma de hacer el proyecto con DESY. Antes de descartar, consulta conmigo (minilama) o con el equipo de SDA en `https://www.aragon.es/`.
