# DESY — Mapa Mental del Ecosistema

> **Documento de referencia** construido a partir de la lectura de toda la doc oficial en `desy.aragon.es/llms.txt`. Sirve como base para diseñar skills que ayuden a desarrolladores a usar DESY.

## 🌍 Visión general

DESY es el **sistema de diseño oficial del Gobierno de Aragón** para webs/apps accesibles WCAG 2.2 AA. Tiene:
- **3 librerías de implementación** (desy-html, desy-angular, desy-ionic)
- **2 librerías de Figma** (desy-html/angular + desy-ionic)
- **~30 componentes** organizados en 7 categorías
- **22 patrones** (soluciones reutilizables a problemas comunes)
- **5 plantillas** (estructura de páginas completas)
- **Estilos** (color, tipografía, espaciado, retícula, lenguaje, imágenes)
- **Normativa**: WCAG 2.2 + UNE-EN 301549:2022 + RD 1112/2018

## 📚 Las 3 librerías

| Librería | Stack | Para | Cabecera |
|---|---|---|---|
| **desy-html** | Vite + Tailwind + Nunjucks | Sitios web, portales, contenido | `header-advanced` (3 bandas) |
| **desy-angular** | Angular 19 + esbuild + TypeScript | Webapps, intranets, CRUD | `header` estándar |
| **desy-ionic** | Ionic + Angular + Capacitor | Apps móviles nativas iOS/Android | `header-mobile` |

**Relación entre las 3:**
- desy-html es la base visual. Las 3 derivan conceptualmente de ahí.
- desy-angular es la versión "Angular" de los mismos componentes.
- desy-ionic es la versión "móvil-táctil" de los mismos + nuevos específicos (gestos, action sheets).
- Cada versión de desy-angular apunta a una versión específica de desy-html (tabla de versiones).

## 🎨 Estilos (Design Tokens)

### Color
**5 familias semánticas**, cada una con variantes light/base/dark:
- **primary** (interacción) — primary-light/base/dark
- **neutral** (contenido: bordes, textos) — neutral-lighter, neutral-light, neutral-base, neutral-dark, black, white
- **heading** (cabecera) — heading-base/dark
- **Soporte - Advertencia** — warning-light/base/dark
- **Soporte - Éxito** — success-light/base/dark
- **Soporte - Información** — info-light/base/dark
- **Soporte - Alerta** — alert-light/base/dark

**Bordes:** 1px (separadores, inputs), 2px (condicional), 4px (mensajes)
**Paleta para gráficas:** DESY ARAGON (5 colores, accesible AA), Ampliada (10 colores)

### Tipografía
- **Fuente:** Open Sans (Bold, Semibold, Regular)
- **Encabezados:** h0 a h4 (clases c-h0 a c-h4)
- **Párrafos:** c-paragraph-lg/base/sm (con o sin text-neutral-dark)
- **Enlaces:** c-link, c-link--alert, c-link--neutral, c-link--no-underline, c-link--full
- **Listas:** c-ul, c-ul--no-bullets, c-ol
- **Plugin:** Tailwind typography

### Espaciado
- **Elementos:** xs(4) sm(8) base(16) lg(28) xl(40) 2xl(80) 3xl(160) px
- **Anchuras:** xs(320) sm(384) md(448) lg(512) xl(576) px
- **Máx:** max-w-40(160) max-w-64(256) px

### Retícula
- **Breakpoints recomendados:** (sin prefijo, móvil), lg (1024px escritorio)
- **Sistema columnas:** 4 cols escritorio, 2 cols móvil
- **Gap:** `gap-lg` (28px)
- **Combinaciones escritorio:** 100%, 50+50, 75+25, 4×25
- **Combinaciones móvil:** 100%, 50+50
- **Container:** `container mx-auto px-base` (max 1280px)

## 🧩 Componentes (7 categorías, ~30)

### Componentes principales (obligatorios)
- **Botones** — 4 variantes (default/primario/transparente/alerta), 3 tamaños, estados (activo/loading/success/desactivado)
- **Cabeceras** — 3 tipos: estándar (webapps), mini (parte de advanced), advanced (portales)
- **Pie de página** — fondo neutral-lighter, banda financiación europea (5 tipos: FEDER/FEADER/FSE+/Plurifondo/Sólo UE)

### Formularios (5 inputs + 4 grupos)
- **Inputs simples:** Entrada texto, Área texto, Selector, Carga archivos, Calendario
- **Grupos:** Botón radio, Casilla verificación, Árbol, Bloques de datos
- **Anatomía:** label + hint (opcional) + error message + placeholder + char counter
- **Estados:** activo, desactivado, error, focus, hover
- **Tamaños:** estándar (default), pequeño
- **Composición:** columna (default), línea (casos especiales)

### Navegación
- Barra de búsqueda, Listado de enlaces, Menú navegación, Menú horizontal, Menú vertical, Migas de pan, Paginación

### Mostrar y ocultar
- Acordeón, Acordeón histórico, Barra de menús, Desplegable, Detalles, Globo de ayuda (tooltip), Interruptor (toggle), Pestañas (tabs)

### Datos
- Item, Item de estado, Listado descripciones, Píldoras, **Tabla (3 tipos: simple, avanzada, con árbol)**

### Avisos
- Modal (informativa + destructiva), Notificaciones, Resumen de errores

### Información visual
- Card, Iconos (Streamline, 2 sets), Imágenes, Spinner

## 📐 Patrones (22 — soluciones reutilizables)

### Cómo pedimos información
1. Aceptar políticas de privacidad
2. Configurar cookies
3. Datos de identidad (Nombre, NIF/NIE)
4. Datos de contacto (Email, teléfono)
5. Domicilio postal

### Cómo mostramos información
6. **Acciones de tabla** (CRÍTICO para listas CRUD)
7. Grupo de acciones
8. Listados (cards a secciones)
9. Title de página
10. Títulos y encabezados

### Ayudar a navegar y encontrar
11. Avanzar y retroceder
12. Barra de progreso
13. Buscar
14. Filtrar
15. Megamenú en portales
16. Volver atrás

### Ayudar a resolver
17. Asistencia contextual
18. Preguntas frecuentes
19. Soporte

### Páginas y flujos
20. Acceso por MFE
21. **Formulario por pasos** (3 pasos: Nombre+NIF, Email+Teléfono, Dirección postal)
22. **Páginas de aplicaciones** (3 tipos: cards-secciones, items-filtrables, tabla-con-acciones-en-lote)
23. Páginas de portales
24. Otras páginas (FAQs, perfil, contenidos, **mapa web obligatorio**, **declaración de accesibilidad obligatoria**)

## 🧱 Plantillas (5 — páginas completas)

1. **Sin sesión iniciada en aplicación** (landing webapp)
2. **Con sesión iniciada en aplicación** (después de auth)
3. **Edición de contenido** (CRUD)
4. **Portal web** (sitio público con cabecera advanced)
5. **Correo electrónico** (HTML compatible)

## 🔐 Accesibilidad (recurrente)

### Normativa
- **WCAG 2.2** nivel AA (obligatorio)
- **UNE-EN 301549:2022** (norma europea)
- **RD 1112/2018** (Real Decreto español)

### Recursos
- W3C ARIA Authoring Practices Guide (APG)
- Mozilla Developer: Accesibilidad Web y ARIA
- Libro "Accesibilidad Web. WCAG 2.2 de forma sencilla" (Olga Carreras)

### Convenciones técnicas transversales
- **Landmarks:** `<header>`, `<nav>`, `<main>`, `<footer>`
- **Skip-link** en cada cabecera
- **Foco visible** siempre (no ocultar)
- **Roles ARIA** cuando HTML no basta: `role=dialog`, `aria-modal=true`, `aria-labelledby`, `role=img` + `aria-label`
- **Contraste mínimo AA** (texto sobre colores base solo en botones, semibold 16px+)
- **Mobile-first** (diseñar primero móvil)
- **Unidades `rem`** (no `px` absolutos)
- **No `<br>` para espaciado** (usar margins)
- **No tablas para maquetación**
- **No widgets externos de accesibilidad** (parches que obstaculizan)
- **No iconos sin texto** (acompañar con label o aria-label)
- **Foco al error-summary** al submit de formulario con errores
- **Inputs con:** `id` único, label visible, `aria-describedby` para hint, `aria-errormessage` para error, `aria-invalid=true` en error
- **Tablas con:** `role=grid`, `<caption>`, `<thead>`, `<tbody>`, `<tfoot>`, `<th scope=col/row>`, navegación por flechas entre celdas
- **Modales con:** `role=dialog`, `aria-modal=true`, `aria-labelledby` al título, foco atrapado
- **Anuncios y notificaciones:** foco al título del bloque
- **Desplegables y pop-ups:** foco al accionable concreto (cerrar o primer item)
- **Mapa web obligatorio** en pie de página
- **Declaración de accesibilidad obligatoria** en pie de página
- **Mapa web:** `<nav>` con skip-link

## 🔄 Flujo del desarrollador (lo que el skill debería automatizar)

### 1. Decisión inicial
¿Qué tipo de proyecto? → desy-html / desy-angular / desy-ionic

### 2. Setup
- Clonar starter de Bitbucket
- Instalar con NVM
- `npm install` (con --legacy-peer-deps en Angular)
- `npm run dev` para arrancar

### 3. Implementación por pantalla
- Identificar qué pantalla es (de las 5 plantillas)
- Identificar qué componentes necesita
- Para cada componente: ir a la doc de código (HTML o Angular) y copiar el macro
- Si la pantalla es compleja, buscar patrón similar

### 4. Accesibilidad
- Verificar labels visibles
- Verificar roles ARIA
- Verificar contraste
- Verificar focus visible
- Verificar navegación por teclado

### 5. Verificación
- Probar en móvil y escritorio
- Probar con lector de pantalla
- Probar con navegación por teclado

## 🧰 Convenciones del código

### Nunjucks (desy-html)
- Macros en `components/<nombre>/_macro.<nombre>.njk`
- Import con: `{% from "components/<nombre>/_macro.<nombre>.njk" import componentXxx %}`
- Llamada con: `{{ componentXxx({"text": "...", "classes": "..."}) }}`
- Clases Tailwind, no escribir `class="..."` en HTML directamente

### Angular (desy-angular)
- Componentes como `<desy-xxx>`
- Inputs con `[input]="value"`
- Outputs con `(clickEvent)="handler()"`
- Importar `DesyXxxComponent` en `imports: []`
- `standalone: true` por defecto
- TypeScript con clases para demos

### Ionic (desy-ionic)
- Componentes `<ion-xxx>` con prefijo
- `ion-modal`, `ion-content`, `ion-button` con `color="primary|warning|success|info|alert"`
- `(didDismiss)`, `(click)` eventos
- Standalone components también

## 📌 Lo crítico para skills útiles

Para que un skill ayude a un equipo:

1. **Mapeo de la decisión inicial** (qué librería) — claro, sin ambigüedad
2. **Mapeo de componente → librería → URL exacta** (copy-paste)
3. **Reconocer plantillas y patrones** antes de implementar desde cero
4. **Checklist de accesibilidad** que aplicar a cada componente
5. **No inventar nombres de props** — verificar siempre en la doc oficial
6. **Verificar las dependencias** (Bitbucket para starters, npm para paquetes)

## 📂 URLs base para skills

- Índice: `https://desy.aragon.es/llms.txt`
- Tutorial: `https://desy.aragon.es/como-empezar-tutorial.html.md`
- Componentes HTML código: `https://desy.aragon.es/componente-<nombre>-codigo.html.md`
- Componentes Angular código: `https://desy.aragon.es/angular-md/demo-<nombre>.md`
- Componentes Ionic: `https://desy.aragon.es/desy-ionic` (Storybook)
- Patrones: `https://desy.aragon.es/patrones-<nombre>.html.md`
- Plantillas: `https://desy.aragon.es/plantillas-<nombre>.html.md`
- Figma: `https://www.figma.com/community/file/1167029569064210460` (DESY) / `https://www.figma.com/community/file/1383376074462615538/desy-ionic`
- Bitbucket: `https://bitbucket.org/sdaragon/`
