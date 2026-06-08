# DESY Skills — Estrategia de Uso

> **Documento estratégico** que explica qué skills forman parte del catálogo, cuándo usar cada uno, en qué orden, y casos de uso típicos. Para devs que llegan al repo y necesitan saber "qué skill ejecuto para mi tarea X".

## 🎯 Catálogo de skills

| # | Skill | Para qué |
|---|---|---|
| 1 | `desy-choose-library` | Decidir qué librería DESY usar |
| 2 | `desy-scaffold-project` | Montar el esqueleto del proyecto |
| 3 | `desy-styles-reference` | Consultar tokens del design system (colores, espaciado, tipografía, sombras) |
| 4 | `desy-component-recognizer` | Identificar componentes DESY desde un mockup/screenshot |
| 5 | `desy-implement-component` | Generar código de un componente concreto (Nunjucks/Angular/Ionic) |
| 6 | `desy-angular-translator` | Traducir código Nunjucks a Angular (TypeScript + template) |
| 7 | `desy-design-match` | Verificar fidelidad visual vs imagen de referencia tras 1ª pasada |
| 8 | `desy-validate-accessibility` | Validar WCAG 2.2 AA antes de mergear |

## 🗺️ Flujo del desarrollador (cuándo usar cada skill)

```
   ┌─────────────────────────┐
   │ 1. desy-choose-library   │  ← Tienes un proyecto nuevo o migración
   └────────────┬────────────┘
                ▼
   ┌─────────────────────────┐
   │ 2. desy-scaffold-project│  ← Tienes librería elegida, necesitas arrancar
   └────────────┬────────────┘
                ▼
   ┌────────────────────────────────────────┐
   │3. desy-component-recognizer  (opcional)│  ← Tienes un mockup, identifica componentes
   └────────────┬───────────────────────────┘
                ▼
   ┌────────────────────────────────────────┐
   │4. desy-implement-component    (Nunjucks) │  ← Genera código de cada componente
   └────────────┬───────────────────────────┘
                ▼
   ┌────────────────────────────────────────┐
   │5. desy-angular-translator    (si aplica) │  ← Si target es Angular, traduce Nunjucks → Angular
   └────────────┬───────────────────────────┘
                ▼
   ┌────────────────────────────────────────┐
   │6. desy-design-match     (iterativo)    │  ← 1ª pasada → captura → medir → esperar OK → fix
   └────────────┬───────────────────────────┘
                ▼
   ┌────────────────────────────────────────┐
   │7. desy-validate-accessibility  (a11y)   │  ← Antes de mergear
   └────────────────────────────────────────┘
```

Cada skill tiene un output concreto que el siguiente puede consumir.

## 📚 Detalle de cada skill

### 1. `desy-choose-library`

**Cuándo usarla:**
- "Voy a empezar un proyecto nuevo, ¿qué librería uso?"
- "Tengo que migrar un proyecto legacy a DESY, ¿por dónde empiezo?"
- "Mi equipo duda entre desy-angular y desy-ionic, ¿qué recomiendas?"

**Cuándo NO usarla:**
- Ya sabes la librería que vas a usar (salta al scaffold)
- Es un fix de un componente existente (salta al implement)

**Inputs necesarios:** tipo de producto (portal / webapp / app móvil), perfil del equipo, requisitos no funcionales.

**Output:** recomendación razonada + comandos iniciales + siguiente skill.

**Tiempo típico:** 5-15 minutos (conversación guiada).

### 2. `desy-scaffold-project`

**Cuándo usarla:**
- Acabas de decidir la librería y quieres arrancar
- Vas a empezar un proyecto DESY desde cero
- Quieres migrar un proyecto existente al stack de la librería

**Cuándo NO usarla:**
- Tienes ya un proyecto DESY funcionando
- Solo quieres actualizar una dependencia

**Inputs necesarios:** librería, nombre del proyecto, target Node version (NVM).

**Output:** proyecto clonado + deps instaladas + dev server arrancando + commit inicial.

**Tiempo típico:** 10-20 minutos (depende de la velocidad de la red para clonar Bitbucket y descargar npm).

### 3. `desy-implement-component`

**Cuándo usarla:**
- "Necesito un botón de enviar con texto 'Enviar'"
- "Necesito una tabla con paginación y filtros"
- "Necesito un modal de confirmación destructiva"
- "Verifica que mi componente cumple accesibilidad"

**Cuándo NO usarla:**
- Estás buscando un patrón completo (ej: acciones de tabla) — ve a la doc de patrones directamente
- Estás auditando accesibilidad — usa el `desy-validate-accessibility`

**Inputs necesarios:** nombre del componente, librería, parámetros (texto, variante, estado, contexto de uso).

**Output:** código copy-pasteable con verificación de accesibilidad.

**Tiempo típico:** 5-10 minutos por componente.

### 4. `desy-validate-accessibility`

**Cuándo usarla:**
- Antes de mergear cualquier PR con UI nueva
- Al auditar código existente
- Después de implementar un componente nuevo
- Antes de la revisión oficial de accesibilidad (obligatoria por RD 1112/2018)

**Cuándo NO usarla:**
- Si la pieza que vas a mergear no tiene UI (lógica, types, tests)
- Si acabas de empezar el proyecto y aún no hay nada que validar

**Inputs necesarios:** URL local de la página o ruta al componente.

**Output:** reporte de accesibilidad con issues detectados + acciones correctivas.

**Tiempo típico:** 30-60 minutos por página completa (15 min scan automático + 30-45 min tests manuales).

### 3. `desy-styles-reference` (soporte transversal)

**Cuándo usarla:**
- Necesitas saber el nombre de un token (color, espaciado, tipografía) y no quieres inventar una utility Tailwind por defecto
- Aplicas color, fondo, borde, margin, padding, gap, tipografía
- Quieres verificar que un color tiene el contraste correcto según WCAG

**Cuándo NO usarla:**
- Para saber QUÉ librería usar (eso es `desy-choose-library`)
- Para saber CÓMO usar un componente concreto (eso es `desy-implement-component`)

**Inputs necesarios:** nombre aproximado del token (e.g. "color primary", "spacing entre campos", "h1 font-size").

**Output:** tabla de tokens relevantes + la utility class exacta del design system + nota sobre cuándo NO usar esa utility.

**Tiempo típico:** <2 minutos (lookup puro).

### 4. `desy-component-recognizer` (soporte transversal)

**Cuándo usarla:**
- Tienes un mockup de Figma o un screenshot de una página existente y necesitas saber qué componentes DESY usar
- Estás auditando un mockup para identificar inconsistencias con el design system
- Quieres validar que un componente que ya implementaste es el correcto

**Cuándo NO usarla:**
- Ya tienes la lista de componentes que necesitas (salta a `desy-implement-component`)
- Estás generando un mockup desde cero (no tienes qué reconocer)

**Inputs necesarios:** imagen del mockup o screenshot (idealmente 1280×2400px).

**Output:** lista de componentes DESY identificados, con su variante exacta + linter que valida contra el catálogo.

**Tiempo típico:** 5-15 minutos por mockup (con verificación del linter).

### 6. `desy-angular-translator` (soporte transversal)

**Cuándo usarla:**
- Tienes código Nunjucks de `desy-html` y necesitas pasarlo a TypeScript + template de `desy-angular`
- Estás aprendiendo las convenciones de `desy-angular` partiendo de tu conocimiento de `desy-html`
- Estás auditando código que mezcla ambos paradigmas

**Cuándo NO usarla:**
- Estás trabajando solo con `desy-html` (no necesitas Angular)
- Estás en `desy-ionic` (la traducción a Ionic es distinta)
- Necesitas la traducción **inversa** (Angular → HTML)

**Inputs necesarios:** fragmento de código Nunjucks (`{{ componentX({...}) }}`) + librería target.

**Output:** componente Angular con clase TS, template HTML, y notas sobre convenciones que difieren entre Nunjucks y Angular.

**Tiempo típico:** 5-10 minutos por componente (más si es conceptual: modal, table-advanced, date-input, input-group).

### 7. `desy-design-match` (soporte transversal)

**Cuándo usarla:**
- Acabas de terminar la 1ª pasada estructural de una página y hay diferencias visibles con la imagen de referencia
- El build pasa, los contadores coinciden, pero algo se ve "raro" (spacing, tipografía, layout)
- Necesitas decidir si una discrepancia (4px, 8px, 28px) es ruido del navegador o merece un fix
- El usuario reporta "esto se ve mal" sin más detalle

**Cuándo NO usarla:**
- Estás en la 1ª pasada (esqueleto) — preocúpate primero de la estructura y los bindings
- Solo quieres consultar qué token usar → `desy-styles-reference`
- La diferencia es funcional, no visual

**Inputs necesarios:** URL de tu implementación + URL de la imagen de referencia (puede ser un gold HTML servido, una URL de Figma, o un PNG/mockup).

**Output:** tabla de discrepancias con magnitud en px + clasificación (trivial/afinable/bloqueante) + fixes propuestos esperando tu OK.

**Tiempo típico:** 10-30 minutos para afinado de 1 página (la 1ª pasada ya está hecha).

## 🎯 Casos de uso típicos

### Caso 1: "Soy nuevo en DESY, ¿por dónde empiezo?"

1. Lee [`/docs/ecosystem-map.md`](ecosystem-map.md) — el mapa mental del ecosistema
2. Lee [`desy-choose-library/SKILL.md`](../skills/desy-choose-library/SKILL.md) — para entender las opciones
3. Haz la decisión con tu equipo
4. Ejecuta `desy-scaffold-project` para arrancar
5. Para cada componente que implementes, usa `desy-implement-component`
6. Antes de mergear, valida con `desy-validate-accessibility`

### Caso 2: "Voy a implementar una pantalla nueva de un proyecto DESY existente"

1. Identifica qué plantilla es (sin sesión, con sesión, portal, edición, correo)
2. Identifica qué componentes necesitas
3. Para cada componente, usa `desy-implement-component`
4. Compón la pantalla siguiendo la plantilla como guía
5. Antes del PR, valida con `desy-validate-accessibility`

### Caso 3: "Hay un bug de accesibilidad en un componente"

1. Lee el componente actual
2. Consulta `desy-implement-component` para ver las buenas prácticas
3. Aplica el fix
4. Valida con `desy-validate-accessibility`

### Caso 4: "Vamos a publicar la webapp en stores (iOS/Android)"

1. ¿Ya decidiste? `desy-choose-library` te lleva a `desy-ionic`
2. `desy-scaffold-project` con librería `desy-ionic`
3. Implementa con `desy-implement-component` (recordando que las convenciones de móvil difieren)
4. Valida accesibilidad táctil y gestos: `desy-validate-accessibility`
5. Configura Capacitor para builds nativas: `npx cap add ios/android`, `npx cap sync`

### Caso 5: "Necesito un mockup rápido para un cliente"

1. Mira los prototipos en Figma:
   - DESY: https://www.figma.com/community/file/1167029569064210460
   - desy-ionic: https://www.figma.com/community/file/1383376074462615538/desy-ionic
2. Identifica qué componentes vas a necesitar
3. Si el cliente valida el mockup, vuelve a `desy-choose-library` + `desy-scaffold-project` + `desy-implement-component`
4. Si no tienes que codificar todavía, no hace falta scaffoldear todavía

### Caso 6: "Estoy manteniendo un proyecto DESY legacy y necesito entender qué tiene"

1. Lee [`/docs/ecosystem-map.md`](ecosystem-map.md)
2. Lee `package.json` para ver la versión de la librería y la versión de DESY
3. Cruza con la [tabla de versiones](https://desy.aragon.es/desarrollo-versiones.html) para entender qué versión de desy-html corresponde
4. Para cada componente, consulta la doc oficial del componente concreto
5. Si vas a actualizar, usa `desy-validate-accessibility` para auditar primero

## 🧠 Estrategias de uso avanzadas

### Estrategia A: "Skill chaining" (encadenar skills)

Usa el output de un skill como input del siguiente:

```
desy-choose-library output: "usar desy-angular latest"
        ↓
desy-scaffold-project input: librería = "desy-angular", nombre = "mi-app"
        ↓
desy-scaffold-project output: "proyecto en http://localhost:4200"
        ↓
desy-component-recognizer input: mockup.png (opcional, si tienes diseño)
        ↓
desy-component-recognizer output: [button primary, input email, ...]
        ↓
desy-styles-reference: lookup de tokens específicos (color, spacing) si dudas
        ↓
desy-implement-component input: componente = "button", librería = "desy-angular", params = {...}
        ↓
desy-implement-component output: código Nunjucks copy-pasteable
        ↓
desy-angular-translator input: código Nunjucks anterior (si target = Angular)
        ↓
desy-angular-translator output: componente Angular con TS + template
        ↓
desy-design-match input: URL implementación + URL gold
        ↓
desy-design-match output: tabla de discrepancias → fixes propuestos
        ↓
desy-validate-accessibility input: URL = "http://localhost:4200/mi-pantalla"
        ↓
desy-validate-accessibility output: reporte WCAG 2.2 AA
```

### Estrategia B: "Skill como reference card"

Los skills están pensados para ser leídos por humanos también. Úsalos como reference cards en el README de tu proyecto:

```markdown
# Mi Proyecto

Para saber cómo implementar componentes, mira [`desy-implement-component`](https://github.com/minilama2222/desy-skills/blob/main/skills/desy-implement-component/SKILL.md).
```

### Estrategia C: "Skill como entrada para un agente"

Si integras OpenClaw u otro agente en tu proyecto, los skills se pueden instalar localmente y el agente los invocará automáticamente cuando el dev pida algo:

> "Necesito un modal de confirmación"
> → el agente matchea con `desy-implement-component`
> → invoca el skill
> → genera el código

### Estrategia D: "Skill en paralelo con el codebase"

Mantén los skills actualizados cuando:
- Sale una nueva versión de DESY
- Encuentras un gotcha nuevo al implementar
- Aparece un patrón nuevo en la doc oficial

Pull request con tu mejora: ver [CONTRIBUTING.md](../CONTRIBUTING.md).

## ❌ Anti-estrategias (lo que NO hacer)

- **No inventes nombres de props.** Si un prop no aparece en la tabla oficial, verifica en la URL de la demo. Mejor preguntar que inventar.
- **No mezcles librerías.** Un proyecto no debería tener desy-html y desy-angular para el mismo componente. Complica mantenimiento y versionado.
- **No hagas scaffold si no tienes claro qué librería.** Empieza por `desy-choose-library`.
- **No valides accesibilidad solo con herramientas automáticas.** axe-core y pa11y detectan ~30-40%. El resto requiere test manual.
- **No skip el test de teclado.** Es donde más se rompe la accesibilidad sin que nos demos cuenta.
- **No publiques sin validar accesibilidad.** Es obligatoria por RD 1112/2018. Mejor descubrir los issues antes que después.

## 📊 Métricas de éxito

Para saber si los skills están ayudando:

- **Tiempo de onboarding:** de 0 a "PR mergeado" debería bajar de semanas a días
- **Bugs de accesibilidad pre-merge:** 0
- **Re-trabajo por mal copy-paste:** bajo
- **Satisfacción del equipo:** el skill responde a "¿cómo hago X?" en <5 min

## 🔄 Versionado

- **v0.1** (inicial): 4 skills MVP — `choose-library`, `scaffold-project`, `implement-component`, `validate-accessibility`. Cubre los casos de uso más comunes.
- **v0.2** (intermedia): +4 skills de soporte — `styles-reference` (catálogo de tokens), `component-recognizer` (reconocer desde mockup), `angular-translator` (Nunjucks → Angular), `design-match` (fidelidad visual). Cubre el ciclo completo de maquetación.
- **v0.3** (actual): 8 skills. Validado con wizard de 3 pasos (paso-1, paso-2, paso-3) con fidelidad 100% al gold tras 1 fix.
- **v1.0** (estabilidad): los 8 skills cubriendo el 90% de casos, sin cambios breaking.

## 🤝 Contribuir

¿Has encontrado un caso de uso que los skills actuales no cubren? ¿Un gotcha? ¿Una mejora?

1. Abre un Issue describiendo el caso
2. Crea un branch `skill/<nombre>` o `improve/<skill-name>`
3. Sigue la estructura de SKILL.md
4. PR contra main

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para más detalle.

## Related

- [`ecosystem-map.md`](ecosystem-map.md) — mapa mental del ecosistema DESY
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — cómo añadir/mejorar skills
- [`README.md`](../README.md) — overview del repo
