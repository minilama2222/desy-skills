# DESY Skills

Skills (procedimientos canónicos) para que agentes de IA y desarrolladores humanos implementen el sistema de diseño [DESY](https://desy.aragon.es/) del Gobierno de Aragón con las librerías oficiales (`desy-html`, `desy-angular`, `desy-ionic`).

## 🎯 Objetivo

Un equipo sin maquetadores puede partir de un mockup hecho con Figma, identificar los componentes DESY que necesita, y generar el código correcto con la librería adecuada — sin tener que leer toda la documentación.

## 📚 Skills disponibles (6)

| Skill | Tamaño | Función |
|---|---:|---|
| [`desy-choose-library`](./skills/desy-choose-library) | 14.7KB | Qué librería (`desy-html`, `desy-angular`, `desy-ionic`) y qué starter usar según el caso de uso |
| [`desy-scaffold-project`](./skills/desy-scaffold-project) | 28KB | Cómo clonar el starter, `npm install`, configurar build, documenta la regla "nunca uses la librería directamente, siempre el starter" |
| [`desy-styles-reference`](./skills/desy-styles-reference) | 13.8KB | Catálogo de tokens visuales del proyecto: colores semánticos, espaciado (`p-base`, `mb-sm`), tipografía (`c-h1`, `c-paragraph-base`), sombras, radius, iconografía |
| [`desy-implement-component`](./skills/desy-implement-component) | 28KB | Cómo usar los macros de la librería Nunjucks/Angular/Ionic, tipografía semántica, catálogo de las 16 plantillas oficiales del starter |
| [`desy-validate-accessibility`](./skills/desy-validate-accessibility) | — | Checklist WCAG 2.2 AA para validar el output |
| [`desy-component-recognizer`](./skills/desy-component-recognizer) | 12KB + 627KB catalog | Reconocer componentes DESY desde un mockup o screenshot, con 10 reglas críticas y un linter de validación post-reconocimiento |

## 🔧 Linter de variantes

[`desy-component-recognizer/assets/linter.py`](./skills/desy-component-recognizer/assets/linter.py) — valida las identificaciones del recognizer contra el catálogo:

| Status | Significado |
|---|---|
| ✅ OK | Variante documentada en el catálogo |
| 🟡 COMPOSITION | Combinación no documentada, pero los modificadores atómicos sí existen |
| 🟣 CSS_CLASS | Parece una clase CSS (`c-link`, `c-button`), no una variante |
| 🟠 SUSPICIOUS | Contiene `ds-focus` o `estado focus` (clase demo, no de producción) |
| ⚠️ WARNING | Variante no documentada — **decisión humana** (no error) |
| ❌ UNKNOWN | Componente no existe en el catálogo |

**Uso:**
```bash
cd skills/desy-component-recognizer
python3 assets/linter.py  # lee catalog.json automáticamente
```

## 🏗️ Estructura del repo

```
desy-skills/
├── README.md              ← este fichero
├── LICENSE                 ← EUPL-1.2 (mismo que desy-html)
├── CONTRIBUTING.md        ← cómo añadir un nuevo skill
├── docs/                   ← documentación extendida, decisiones de diseño
│   ├── ecosystem-map.md
│   └── skills-strategy.md
└── skills/                 ← 6 skills aprobados
    ├── desy-choose-library/SKILL.md
    ├── desy-scaffold-project/SKILL.md
    ├── desy-styles-reference/SKILL.md
    ├── desy-implement-component/SKILL.md
    ├── desy-validate-accessibility/SKILL.md
    └── desy-component-recognizer/
        ├── SKILL.md                            # 12KB orquestador
        └── assets/
            ├── catalog.json                    # 627KB, 57 comps, 653 ejemplos
            ├── catalog-summary.md               # 11KB resumen de variantes
            └── linter.py                        # 5.4KB validador post-reconocimiento
```

## 🪷 Cómo se usan estos skills

**Por un agente de IA** (OpenClaw, Claude, etc.): el skill vive en el catálogo de skills del agente. Cuando el usuario hace una pregunta o tarea que matchea con la `description` del frontmatter, el agente lo invoca automáticamente. El **skill pack** completo (los 6 SKILL.md concatenados) tiene ~110KB y se carga como contexto cuando se necesita.

**Por un humano:** cada `SKILL.md` es Markdown legible. Se puede leer directamente en GitHub o clonar y usar como referencia.

## 📊 Estado del proyecto

- **6 skills aprobados** (commits `482c96e` → `05f28eb`)
- **Catálogo:** 57 componentes, 653 ejemplos extraídos del repo `desy-html` (develop branch)
- **Benchmark de capacidad:** 5/5 patrones de "Páginas y flujos" validados con opencode + M3, todos ACEPTABLE+
- **Validación del recognizer:** 21 mockups de la doc oficial analizados
- **Linter:** 100% de los reconocimientos procesables (0% WARNING real en los 3 mockups re-validados)

## 🤝 Cómo contribuir

Ver [CONTRIBUTING.md](./CONTRIBUTING.md). Cada propuesta de skill entra como PR contra `main`, con su propia rama o worktree.

**Workflow de iteración** (validado en 2026-06-07):
1. Identificar un gap (test falla, feedback del usuario, o análisis de la librería)
2. Aplicar fix al skill correspondiente con un commit descriptivo
3. Re-validar empíricamente con el test que reveló el gap
4. Si el fix es correcto, el test mejora; si no, iterar

## 📄 Licencia

EUPL-1.2 — ver [LICENSE](./LICENSE). Misma licencia que la librería `desy-html` del Gobierno de Aragón.

## 🪷 Sobre el sistema de diseño DESY

DESY es el sistema de diseño oficial del Gobierno de Aragón para crear aplicaciones web accesibles, consistentes y conformes con la identidad corporativa. Sigue WCAG 2.1 nivel AA. Más información: [desy.aragon.es](https://desy.aragon.es/).

**Fuentes primarias:**
- Doc oficial: <https://desy.aragon.es/>
- Repo `desy-html` (develop): <https://bitbucket.org/sdaragon/desy-html/src/develop/>
- Tutorial: <https://desy.aragon.es/como-empezar-tutorial.html.md>
- Patrones de páginas: <https://desy.aragon.es/patrones.html.md>
