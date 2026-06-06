# DESY Skills

Skills (procedimientos canónicos) para que agentes de IA y desarrolladores humanos implementen el sistema de diseño [DESY](https://desy.aragon.es/) del Gobierno de Aragón con las librerías oficiales (`desy-html`, `desy-angular`, `desy-ionic`).

## 🎯 Objetivo

Un equipo sin maquetadores puede partir de un mockup hecho con Figma, identificar los componentes DESY que necesita, y generar el código correcto con la librería adecuada — sin tener que leer toda la documentación.

## 📚 Skills disponibles

*(Esta sección se llenará a medida que se aprueben skills.)*

## 🏗️ Estructura del repo

```
desy-skills/
├── README.md              ← este fichero
├── LICENSE                 ← licencia del proyecto
├── CONTRIBUTING.md        ← cómo añadir un nuevo skill
├── docs/                   ← documentación extendida, decisiones de diseño
└── skills/                 ← cada skill en su propia carpeta
    └── <skill-name>/
        ├── SKILL.md       ← frontmatter + cuerpo del skill
        ├── references/    ← docs complementarios cargados bajo demanda
        ├── scripts/       ← helpers deterministas (opcional)
        └── assets/        ← templates, fixtures (opcional)
```

## 🪷 Cómo se usan estos skills

**Por un agente de IA** (OpenClaw, Claude, etc.): el skill vive en el catálogo de skills del agente. Cuando el usuario hace una pregunta o tarea que matchea con la `description` del skill, el agente lo invoca automáticamente.

**Por un humano:** cada `SKILL.md` es Markdown legible. Se puede leer directamente en GitHub o clonar y usar como referencia.

## 🤝 Cómo contribuir

Ver [CONTRIBUTING.md](./CONTRIBUTING.md). Cada propuesta de skill entra como PR contra `main`, con su propia rama o worktree.

## 📄 Licencia

MIT — ver [LICENSE](./LICENSE).

## 🪷 Sobre el sistema de diseño DESY

DESY es el sistema de diseño oficial del Gobierno de Aragón para crear aplicaciones web accesibles, consistentes y conformes con la identidad corporativa. Sigue WCAG 2.1 nivel AA. Más información: [desy.aragon.es](https://desy.aragon.es/).
