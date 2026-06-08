# Skill Prompts Collection

> **Colección de prompts de prueba** para testear las 8 skills `desy-*` de forma individual o combinada, en cualquier entorno que soporte SKILL.md (OpenClaw, OpenCode, Claude Code, Codex). Cada prompt está diseñado para activar el skill correspondiente, con contexto suficiente para que el agente tenga con qué trabajar.
>
> **Cómo usar:**
> 1. Copia el prompt tal cual
> 2. Pégalo en el chat del agente
> 3. Observa la respuesta: el agente debería invocar el skill y producir un output coherente con su descripción
> 4. Compara el output con lo que esperas (columna "Output esperado" en cada caso)
>
> **Para prompts combinados:** están pensados para que el agente encadene skills. Suelen partir de un input realista (mockup, HTML, descripción de proyecto) y el output es una cadena de artefactos.

---

## 1. Prompts individuales (2 por skill)

### `desy-choose-library`

#### Caso 1.1 — Decisión desde cero
**Prompt:**
> Voy a empezar un proyecto nuevo. Es un portal de transparencia para el Gobierno de Aragón con 3 secciones: normativa, búsqueda de documentos y un formulario de solicitud. El equipo es de 4 personas (2 frontend, 1 backend, 1 devops), todos con experiencia previa en HTML/CSS pero ninguno conoce Angular. El sitio debe ser accesible WCAG 2.2 AA. ¿Qué librería DESY me recomiendas y por qué?

**Output esperado:** El agente recomienda `desy-html` (sitio web, no webapp, equipo no conoce Angular), justifica brevemente, y enlaza con `desy-scaffold-project` como siguiente paso.

#### Caso 1.2 — Migración de proyecto legacy
**Prompt:**
> Mantenemos una webapp Angular 14 con Bootstrap 4 que tiene un wizard de 4 pasos, 8 pantallas CRUD y un dashboard. Queremos migrarla a DESY. ¿Qué librería tiene más sentido y cuáles son los principales gotchas de la migración?

**Output esperado:** Recomendación razonada de `desy-angular` (no romper el modelo mental del equipo), consideraciones de versión de Angular (v14 → 20.3), y advertencias concretas (e.g. el 4% de los componentes DESY no son traducción 1:1, mejor revisar `desy-angular-translator` antes de migrar).

---

### `desy-scaffold-project`

#### Caso 2.1 — Arrancar portal nuevo
**Prompt:**
> Quiero arrancar un portal de noticias con `desy-html` (Nunjucks + Vite + Tailwind 4). El proyecto se llama `aragon-noticias`, va a correr en Node 20 LTS. ¿Qué pasos exactos sigo desde cero hasta tener el dev server funcionando en `localhost:5173`?

**Output esperado:** Comandos concretos: `nvm use 20`, `git clone https://bitbucket.org/sdaragon/desy-html-starter.git aragon-noticias`, `cd aragon-noticias && npm install`, `npm run dev`. Confirmación de que el dev server arranca y cómo verificar.

#### Caso 2.2 — Migrar un proyecto Angular existente
**Prompt:**
> Tengo un proyecto Angular 17 con 3 pantallas, quiero añadir `desy-angular` para usar sus componentes. ¿Lo añado como librería aparte o hay un starter oficial de `desy-angular` que ya tenga la integración hecha?

**Output esperado:** El agente explica la regla de oro: "nunca uses la librería directamente, siempre el starter". Indica clonar `desy-angular-starter`, instalar, y migrar componentes uno a uno (no convertir todo de golpe).

---

### `desy-styles-reference`

#### Caso 3.1 — Lookup de color
**Prompt:**
> ¿Cuál es el token del design system para el color principal de los botones primarios? ¿Y su variante hover? ¿Y el color de los bordes de los inputs en estado de focus? Dame la utility class exacta en cada caso.

**Output esperado:** Tabla con `text-primary-base` (#00607a), `hover:text-primary-dark` (#00475c), `focus:border-black`. Nota sobre por qué NO usar `text-blue-700` o equivalentes Tailwind por defecto.

#### Caso 3.2 — Lookup de espaciado
**Prompt:**
> Necesito un padding interno de 16px en una card, y un margin-bottom de 28px entre el h1 y el primer párrafo. ¿Qué utility classes del design system uso, y por qué no `p-4` o `mb-7`?

**Output esperado:** `p-base` (1rem = 16px) y `mb-lg` (1.75rem = 28px), con explicación: el design system tiene unidades canónicas `{8, 16, 28, 32}px` mapeadas a `sm/base/lg/8`, y saltarse a `mb-7` (28px arbitrario) rompe la coherencia.

---

### `desy-component-recognizer`

#### Caso 4.1 — Reconocer desde mockup bitmap
**Prompt:**
> Te paso un screenshot de un mockup de Figma a 1280×2400px. Identifica los componentes DESY que ves, con su variante exacta. Adjunto: `mockup.png` (NOTA: en este test sustituye por una captura real de https://desy.aragon.es/patron-pagina-paso-3-direccion-postal.html).

**Output esperado:** Lista de componentes con sus variantes (e.g. `button.primary`, `input-group` con fieldset, `checkboxes` con fieldset sr-only, `header.logged-selector`). Si hay variantes no documentadas, marcarlas como WARNING.

#### Caso 4.2 — Verificar reconocimiento con linter
**Prompt:**
> Acabo de identificar estos componentes en un mockup: `button.primary`, `header.logged-selector`, `notification.success`, `table.simple`, `input.datepicker`, `dropdown.searchable`. Pásalos por tu linter y dime cuáles están documentados, cuáles son combinaciones, y cuáles son falsos positivos.

**Output esperado:** Tabla con status por componente (OK / COMPOSITION / CSS_CLASS / SUSPICIOUS / WARNING / UNKNOWN). Para `dropdown.searchable` y `input.datepicker` que pueden tener issues, justificar la clasificación.

---

### `desy-implement-component`

#### Caso 5.1 — Componente simple (button)
**Prompt:**
> Necesito un botón "Enviar" con la variante primaria, tamaño estándar, y tipo submit (para que dispare el form). Genera el código Nunjucks para `desy-html` y también el TypeScript + template para `desy-angular`. Verifica que el output cumple WCAG 2.2 AA.

**Output esperado:** Fragmento Nunjucks con `{{ componentButton({text: "Enviar", type: "submit", classes: "c-button--primary"}) }}` y su equivalente Angular con `<desy-button [text]="'Enviar'" [type]="'submit'" [classes]="'c-button--primary'"></desy-button>`. Notas sobre atributos a11y que el componente añade automáticamente.

#### Caso 5.2 — Componente compuesto (modal)
**Prompt:**
> Necesito un modal de confirmación destructiva ("¿Eliminar este expediente? Esta acción no se puede deshacer") con un botón "Cancelar" (transparente) y un botón "Eliminar" (alerta). Genera el código Nunjucks con `desy-html`. Incluye el backdrop, el aria-modal, y el foco atrapado.

**Output esperado:** Macro `{{ componentModal({...}) }}` con su contenido interior (texto + 2 botones), o un fragmento HTML estructurado si el macro no soporta todo. Notas sobre a11y: `role=dialog`, `aria-modal=true`, `aria-labelledby` al título, foco atrapado, cierre con Escape.

---

### `desy-angular-translator`

#### Caso 6.1 — Traducción trivial
**Prompt:**
> Traduce este Nunjucks a Angular con `desy-angular`:
> ```
> {{ componentButton({
>   "text": "Ir a usuarios",
>   "href": "/usuarios",
>   "classes": "c-button--primary"
> }) }}
> ```
> Asume que el proyecto usa `desy-angular` 18.1.0 + Angular 20.3.

**Output esperado:** `<desy-button [text]="'Ir a usuarios'" [href]="'/usuarios'" [classes]="'c-button--primary'">Ir a usuarios</desy-button>` con la nota de que los bindings van entre corchetes y los strings entre comillas simples.

#### Caso 6.2 — Traducción conceptual
**Prompt:**
> Tengo este Nunjucks que es un `{{ componentInputGroup({items: [...]}) }}` con 3 inputs (nombre, apellidos, email) en un fieldset "Datos personales". El item.email es un select con opciones vacía, "particular" y "empresa". Traduce a Angular con `desy-angular` y considera el contexto del FormGroup.

**Output esperado:** Componente Angular con FormGroup reactivo (uno FormControl por cada item.name), `[items]` array con `ItemInputGroupData[]`, labelData con `text`, selectItems con `value/text/selected`, y la envoltura `<form [formGroup]="...">`. Advertencia de que sin FormGroup, los `[formControlName]` internos fallan con "Cannot read properties of null".

---

### `desy-design-match`

#### Caso 7.1 — Captura de HTML servible
**Prompt:**
> Te paso dos URLs:
> - Mi implementación: `http://localhost:4200/mi-pagina`
> - La referencia (HTML servible): `http://localhost:4300/gold.html`
> Captura las dos con la herramienta de screenshots que tengas, mide los estilos computados del h1, párrafo lead, y primer input en cada una, y dame una tabla de discrepancias con clasificación (trivial/afinable/bloqueante).

**Output esperado:** Tabla con `| # | Elemento | Ref | Impl | Δ | Categoría |` para 5-7 elementos. Las discrepancias < 4px se marcan triviales, 4-12px afinables, >12px bloqueantes. Sugerencia de aplicar `mb-0`, `-mt-X`, o quitar overrides.

#### Caso 7.2 — Análisis desde mockup bitmap
**Prompt:**
> Te paso una imagen `mockup.png` (sustituye por una captura de https://desy.aragon.es/patron-pagina-paso-3-direccion-postal.html) y un screenshot `mi-pagina.png` (sustituye por una captura de tu implementación). Mide las siguientes distancias en píxeles con tu herramienta de visión: (a) bottom del h1 → top del primer párrafo, (b) altura del primer input, (c) cualquier otro gap visual notable. Devuelve una tabla con las medidas de cada lado y la diferencia.

**Output esperado:** Análisis cualitativo de las distancias. El LLM con visión puede no dar precisión sub-píxel, pero debe identificar gaps visibles > 4px. Sugerencia: si quieres precisión exacta, renderiza la referencia y compárala con `getComputedStyle` (necesitas HTML servible, no solo bitmap).

---

### `desy-validate-accessibility`

#### Caso 8.1 — Validar componente nuevo
**Prompt:**
> Acabo de implementar un botón "Eliminar" con `aria-label="Eliminar expediente"` pero sin texto visible (solo un icono). Pásalo por tu checklist de WCAG 2.2 AA y dime si cumple, y si no, qué falta.

**Output esperado:** Análisis de la checklist: (1) El `aria-label` cubre el icono sin texto → cumple con 1.1.1 Non-text content. (2) ¿El foco es visible? → probablemente falta `focus:outline-...`. (3) ¿El color de "alerta" tiene contraste AA sobre fondo? → verificar #d22333 sobre #f6f6f5. (4) ¿Hay alternativa para `aria-hidden` o texto visible? → a veces mejor un `<span class="sr-only">Eliminar</span>` que `aria-label`.

#### Caso 8.2 — Auditoría de página completa
**Prompt:**
> Página `http://localhost:4200/expedientes` (lista CRUD con tabla, filtros, paginación). Dame el checklist completo de WCAG 2.2 AA que debería aplicar, en orden, y dime qué herramientas automáticas vs manuales necesito para cada punto.

**Output esperado:** Lista estructurada: (1) Scan automático con axe-core o pa11y (~30% de issues). (2) Test manual de teclado (tab order, focus visible, traps en modales) — donde se descubre la mayoría. (3) Test con lector de pantalla (NVDA en Windows, VoiceOver en macOS) para confirmar anuncios y roles ARIA. (4) Verificación de contraste de color específica. Tiempo total estimado: 30-60 min por página.

---

## 2. Prompts combinados (8 casos)

Estos prompts están diseñados para que el agente encadene 2-4 skills. El output esperado es una cadena de artefactos.

### Combinado 2.1 — Mockup bitmap → portal Nunjucks completo

**Prompt:**
> Te paso una imagen `mockup-portal.png` (sustituye por una captura de https://desy.aragon.es/patron-pagina-acceso-cargando.html). El proyecto se llama `mi-portal`, va a ser un sitio web (no webapp), accesible WCAG 2.2 AA. El equipo son 3 devs con experiencia en HTML/CSS.
>
> Quiero que en un solo flujo:
> 1. Recomiendes la librería DESY adecuada
> 2. Scaffoldees el proyecto
> 3. Reconozcas los componentes del mockup
> 4. Generes el código Nunjucks de cada componente
> 5. Verifiques fidelidad visual con `desy-design-match` comparando tu output contra el mockup original
> 6. Valides accesibilidad WCAG 2.2 AA
>
> Si en algún paso encuentras un problema, sigue y márcalo al final como issue a resolver.

**Skills esperadas:** `choose-library` → `scaffold-project` → `component-recognizer` → `implement-component` → `design-match` → `validate-accessibility`

**Output esperado:** Secuencia de 6 outputs. Cada uno empieza con qué skill se invocó. El último es un reporte de issues pendientes si los hay.

---

### Combinado 2.2 — HTML gold → código Angular

**Prompt:**
> Te paso el HTML servible del gold en `http://localhost:4300/patron-pagina-paso-3-direccion-postal.html` (o adjunta el archivo). Es un wizard step de 3 pasos con 7 inputs, 3 selects y 1 checkbox. El target es Angular con `desy-angular` 18.1.0.
>
> Quiero que en un flujo:
> 1. Reconozcas los componentes DESY del HTML
> 2. Traduzcas el HTML a Angular (TypeScript + template)
> 3. Verifiques fidelidad visual con `desy-design-match` comparando contra el HTML servible
> 4. Valides accesibilidad
>
> Si hay discrepancias de tipografía o espaciado, ajústalas siguiendo la regla "la imagen de referencia manda" de `desy-design-match`.

**Skills esperadas:** `component-recognizer` → `angular-translator` → `design-match` → `validate-accessibility`

**Output esperado:** Componente Angular con la estructura del gold, más reporte de fidelidad con tabla de discrepancias (debería ser Δ=0 si está bien hecho).

---

### Combinado 2.3 — Mockup mobile → app Ionic

**Prompt:**
> Te paso una imagen `mockup-mobile.png` (sustituye por una captura de https://desy.aragon.es/ionic/) de un wizard de 3 pasos para móvil. Vamos a hacer una app nativa con `desy-ionic` + Capacitor.
>
> Quiero que en un flujo:
> 1. Recomiendes la librería (móvil nativo → debería ser `desy-ionic`)
> 2. Scaffoldees el proyecto
> 3. Reconozcas los componentes del mockup
> 4. Generes el código para `desy-ionic` (no Nunjucks ni Angular puro)
> 5. Verifiques accesibilidad táctil (tamaños de tap target ≥ 44×44, gestos no esenciales)
>
> La navegación es iOS + Android (iPhone 13+ y Pixel 5+).

**Skills esperadas:** `choose-library` → `scaffold-project` → `component-recognizer` → `implement-component` (en modo Ionic) → `validate-accessibility`

**Output esperado:** Estructura del proyecto Ionic, componentes generados, y un checklist de a11y táctil.

---

### Combinado 2.4 — Proyecto legacy HTML → auditoría de migración a DESY

**Prompt:**
> Tengo un proyecto webapp Angular 14 con Bootstrap 4, ~30 pantallas. Quiero migrar a DESY sin romper nada.
>
> Quiero que en un flujo:
> 1. Recomiendes el approach de migración (¿big bang, incremental, strangler pattern?)
> 2. Identifiques qué pantallas son "sin sesión iniciada" vs "con sesión iniciada" (de las 5 plantillas DESY)
> 3. Para una pantalla concreta (`/expedientes`), reconozcas los componentes del HTML actual y los mapees a equivalentes DESY
> 4. Valides accesibilidad DESY
>
> No quiero que generes código todavía. Solo la auditoría y el plan.

**Skills esperadas:** `choose-library` (recomendación) → `component-recognizer` (auditoría) → `validate-accessibility`

**Output esperado:** Plan de migración por fases, con estimación de esfuerzo, lista de componentes Bootstrap 4 que mapean a DESY (y cuáles no tienen equivalente directo).

---

### Combinado 2.5 — Solo decisión y arquitectura (sin código)

**Prompt:**
> Estoy diseñando la arquitectura de un proyecto nuevo. Es un portal de transparencia con 3 perfiles de usuario (ciudadano, funcionario, administrador), 12 pantallas, y necesita ser multi-idioma (es/ca/en). El equipo son 5 devs full-stack.
>
> Quiero que en un flujo:
> 1. Recomiendes librería y starter
> 2. Defines la arquitectura de componentes (qué nivel de atomicidad, dónde van los macros/template, cómo se comparten entre proyectos si es multi-tenant)
> 3. Defines la estrategia i18n
> 4. Defines el approach de theming (si lo necesitan para white-label)
>
> No quiero código todavía. Solo decisiones de arquitectura y justificación.

**Skills esperadas:** `choose-library` + conocimiento transversal de `styles-reference` (para theming) + `scaffold-project` (para multi-tenant si aplica)

**Output esperado:** Documento de arquitectura con: stack recomendado, organización de carpetas, estrategia i18n, estrategia de theming. Sin código, pero con ejemplos de nombres de archivos.

---

### Combinado 2.6 — Verificar visualmente un PR antes de mergear

**Prompt:**
> Tengo un PR abierto en `mi-proyecto` que cambia la página `/expedientes`. Adjunto:
> - URL del dev server: `http://localhost:4200/expedientes`
> - URL del gold (referencia): `http://localhost:4300/expedientes.html`
> - Captura del mockup original: `mockup-expedientes.png`
>
> Quiero que en un flujo:
> 1. Verifiques fidelidad visual vs gold (HTML servible) con `desy-design-match` — incluye capturar ambas y reportar discrepancias
> 2. Verifiques fidelidad visual vs mockup (bitmap) — solo cualitativo con tu LLM visión
> 3. Valides accesibilidad WCAG 2.2 AA
> 4. Si todo está bien, dame el OK para mergear. Si hay issues, lista los bloqueantes que hay que resolver antes del merge.
>
> El umbral: cero bloqueantes para mergear. Triviales y afinables se documentan como follow-up.

**Skills esperadas:** `design-match` (2 veces) → `validate-accessibility`

**Output esperado:** Tabla de discrepancias (gold vs impl), análisis cualitativo (mockup vs impl), reporte de a11y, veredicto final (OK / bloqueantes).

---

### Combinado 2.7 — Reemplazar un componente en producción

**Prompt:**
> En mi proyecto DESY actual, el componente "tabla de expedientes" está renderizando con la variante "simple" pero la página `/expedientes` (CRUD con acciones en lote) necesita la variante "advanced". Adjunto captura del estado actual.
>
> Quiero que en un flujo:
> 1. Reconozcas el componente actual (¿es realmente "table simple" o hay confusión?)
> 2. Verifiques el catálogo (`desy-styles-reference` para tokens, `desy-component-recognizer` para variantes)
> 3. Generes el código Nunjucks de la variante "table-advanced" con selección múltiple, paginación, y acciones por fila
> 4. Verifiques accesibilidad (roles ARIA, navegación por teclado, `aria-rowcount`, etc.)
>
> El output debe ser copy-pasteable al `index.html` actual.

**Skills esperadas:** `component-recognizer` → `styles-reference` (consulta) → `implement-component` → `validate-accessibility`

**Output esperado:** Confirmación de la variante actual, código nuevo con todas las propiedades de table-advanced, lista de cambios a aplicar (no solo el snippet, sino "qué líneas reemplazar").

---

### Combinado 2.8 — Generar una pantalla desde cero con gold como referencia

**Prompt:**
> Vamos a crear la pantalla `/configuracion` de mi proyecto `mi-webapp` (Angular con `desy-angular`).
>
> Adjunto:
> - Mockup de Figma: `mockup-configuracion.png` (sustituye por una captura de https://desy.aragon.es/patron-pagina-perfil-de-usuario.html)
> - URL del gold: `http://localhost:4300/perfil.html` (HTML servible)
>
> La pantalla tiene que tener: datos del usuario, preferencias de notificaciones, cambio de contraseña, y zona de "Eliminar cuenta".
>
> Quiero que en un flujo:
> 1. Reconozcas los componentes del mockup y del gold
> 2. Identifiques qué template de las 5 plantillas DESY aplica mejor
> 3. Generes el componente Angular con TypeScript + template
> 4. Verifiques fidelidad visual contra el gold (HTML servible, no solo mockup)
> 5. Apliques los fixes de `desy-design-match` si hay discrepancias
> 6. Valides accesibilidad
>
> Asume que el FormGroup ya está creado en otro sitio; este componente es autocontenido.

**Skills esperadas:** `component-recognizer` → `styles-reference` (lookup) → `angular-translator` (si hubiera HTML de referencia) → `implement-component` (Angular) → `design-match` → `validate-accessibility`

**Output esperado:** Componente Angular funcional con todo el flujo verificado. El más largo de los prompts combinados — útil como stress test del encadenamiento.

---

## 3. Notas de uso

### Cuándo usar prompts individuales vs combinados

- **Individuales:** para testear 1 skill en concreto. Útil cuando acabas de añadir/modificar un skill y quieres verificar que sigue funcionando.
- **Combinados:** para testear el encadenamiento. Útil cuando quieres ver si el agente sabe cuándo invocar cada skill y en qué orden.

### Cómo adaptar los prompts

- **Sustituye los placeholders** (`mockup.png`, `http://localhost:4200/...`) por URLs o paths reales de tu entorno.
- **Si no tienes mockup:** algunos prompts funcionan solo con descripción textual; en ese caso el agente no podrá invocar `component-recognizer` y tendrás que saltarlo.
- **Si no tienes gold HTML servible:** los prompts de fidelidad visual se degradan — `desy-design-match` puede trabajar con bitmap pero con menos precisión.

### Qué observar en las respuestas

- **¿Invocó el skill correcto?** Verifica que la `description` del frontmatter matchee con tu petición.
- **¿Produjo un output coherente con el skill?** Compara con los outputs esperados de arriba.
- **¿Se detiene cuando no tiene info?** Un buen skill debe pedir aclaraciones en vez de inventar.
- **¿Cita docs del design system?** Los skills que dicen "consultar la doc oficial" deberían hacerlo y dar URLs concretas, no inventar props.

### Cómo reportar fallos

Si un skill falla en tu entorno (no se invoca, output incoherente, alucinaciones, etc.):
1. Anota qué prompt usaste
2. Anota qué output obtuviste vs qué esperabas
3. Anota el entorno (cliente, modelo, versión)
4. Abre un Issue en el repo con esos 3 datos

---

## Related

- [README.md](../README.md) — catálogo completo de skills
- [skills-strategy.md](./skills-strategy.md) — estrategia de uso de skills, flujo del desarrollador
- [ecosystem-map.md](./ecosystem-map.md) — mapa mental del ecosistema DESY
