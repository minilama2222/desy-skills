---
name: desy-choose-library
description: "Decide whether to use desy-html, desy-angular, or desy-ionic for a DESY project based on requirements. Use when starting a new project or evaluating library choice."
---

# desy-choose-library

Ayuda a un equipo a decidir qué librería DESY usar para un proyecto nuevo o una migración.

## When to use this skill

- El equipo va a empezar un proyecto con DESY y no sabe qué librería encaja
- Hay que migrar código existente a DESY
- Hay que evaluar pros/contras antes de comprometerse a un stack

## Decision framework

### Pregunta 1: ¿Qué tipo de producto?

| Producto | Cabecera | Librería recomendada |
|---|---|---|
| Sitio web / portal (contenido público) | `header-advanced` (3 bandas) | **desy-html** |
| Webapp (gestión, CRUD, datos) | `header` estándar | **desy-angular** o **desy-ionic** |
| App móvil nativa iOS/Android | `header-mobile` | **desy-ionic** |
| App híbrida (móvil + web con un solo codebase) | `header-mobile` + `header` | **desy-ionic** |

### Pregunta 2: ¿Equipo y stack?

| Perfil del equipo | Recomendación |
|---|---|
| Sin experiencia previa en frameworks JS, contenido estático | desy-html |
| Equipo Angular sólido | desy-angular (reciente, Angular 19) |
| Equipo Angular + quiere publicar en App Store / Play Store | desy-ionic |
| Necesita migrar un proyecto legacy a DESY poco a poco | desy-html primero, desy-angular después |

### Pregunta 3: ¿Requisitos no funcionales?

| Requisito | Si sí | Si no |
|---|---|---|
| SEO crítico | desy-html (mejor para indexación) | da igual |
| Carga en <1s en 3G | desy-html (más ligero) | da igual |
| Autenticación centralizada (DIGA, MFE) | desy-angular o desy-ionic | desy-html |
| Accesibilidad WCAG 2.1 AA obligatoria | las 3 lo cumplen, da igual | da igual |
| Publicar en stores (iOS/Android) | desy-ionic (con Capacitor) | da igual |

## Workflow

1. **Identifica el producto** con la pregunta 1
2. **Cruza con el perfil del equipo** (pregunta 2)
3. **Aplica los requisitos no funcionales** (pregunta 3)
4. **Recomienda** la librería
5. **Documenta la decisión** y enlaza al starter correspondiente

## Output esperado

Una recomendación clara con:
- Librería elegida
- Starter de Bitbucket a usar
- Comando de instalación inicial
- Plantillas de DESY a considerar
- URLs a la documentación relevante

## Examples

### Ejemplo 1: Portal web de información

**Contexto:** Portal de información turística de Aragón, contenido público, necesita SEO, equipo de maquetadores que conocen HTML/CSS pero no Angular.

**Decisión:**
- Pregunta 1 → Sitio web/portal → **desy-html**
- Pregunta 2 → Sin Angular → confirma **desy-html**
- Pregunta 3 → SEO crítico → confirma **desy-html**

**Output:**
- Librería: `desy-html`
- Starter: https://bitbucket.org/sdaragon/desy-html-starter
- Comandos:
  ```bash
  git clone https://bitbucket.org/sdaragon/desy-html-starter.git mi-portal
  cd mi-portal
  npm install
  npm run dev
  ```
- Cabecera: `header-advanced` (3 bandas)
- Plantilla: `plantillas-portal-p1.html`

### Ejemplo 2: Webapp de gestión de expedientes

**Contexto:** Aplicación interna para funcionarios, con login, gestión CRUD, tablas grandes, integración con backend ya existente.

**Decisión:**
- Pregunta 1 → Webapp → **desy-angular**
- Pregunta 2 → Equipo con Angular → confirma **desy-angular**
- Pregunta 3 → Autenticación centralizada → confirma **desy-angular**

**Output:**
- Librería: `desy-angular` (Angular 19)
- Starter: https://bitbucket.org/sdaragon/desy-angular-starter
- Comandos:
  ```bash
  git clone https://bitbucket.org/sdaragon/desy-angular-starter.git mi-webapp
  cd mi-webapp
  # Renombrar ocurrencias de 'desy-angular-starter' por el nombre del proyecto
  npm install --legacy-peer-deps
  npm run dev
  ```
- Cabecera: `header` (estándar)
- Plantilla: `plantillas-con-sesion-iniciada.html`

### Ejemplo 3: App móvil para ciudadanía

**Contexto:** App que los ciudadanos se bajan del App Store, acceso a sus datos personales, formularios offline-friendly.

**Decisión:**
- Pregunta 1 → App móvil → **desy-ionic**
- Pregunta 2 → Equipo con Angular + quieren publicar → confirma **desy-ionic**
- Pregunta 3 → Necesita publicación en stores → confirma **desy-ionic**

**Output:**
- Librería: `desy-ionic`
- Storybook: https://desy.aragon.es/desy-ionic
- Stack: Ionic + Angular + Capacitor (iOS/Android)

## Related

- Skill: `desy-implement-component` (siguiente paso tras elegir librería)
- Skill: `desy-scaffold-project` (scaffolding tras elegir)
- Doc oficial: https://desy.aragon.es/como-empezar-tutorial.html
- Tutorial para IA: https://desy.aragon.es/como-empezar-tutorial.html.md
