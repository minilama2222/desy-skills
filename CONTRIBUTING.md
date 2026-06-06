# Cómo contribuir

Gracias por querer añadir o mejorar un skill de DESY. Este documento explica el flujo.

## 📋 Tipos de contribución

1. **Nuevo skill** — proponer uno que no existe
2. **Mejora de skill existente** — añadir ejemplos, clarificar, etc.
3. **Fix de bug** en la doc o en un script auxiliar
4. **Discusión** — abrir un Issue antes de proponer algo grande

## 🌿 Flujo de trabajo con worktrees

Cada cambio se hace en su propio worktree (rama separada). Pasos:

```bash
# 1. Clonar el repo (primera vez)
git clone https://github.com/minilama2222/desy-skills.git
cd desy-skills

# 2. Crear rama + worktree para tu contribución
git worktree add -b skill/<nombre-corto> ../desy-skills-<nombre-corto>

# 3. Trabajar en la nueva carpeta
cd ../desy-skills-<nombre-corto>

# 4. Crear el skill siguiendo la estructura de skills/
mkdir -p skills/<skill-name>
# escribir SKILL.md + frontmatter + cuerpo

# 5. Commit
git add skills/<skill-name>/
git commit -m "feat(skill): add <skill-name>"

# 6. Push de la rama
git push -u origin skill/<nombre-corto>

# 7. Abrir PR en GitHub
gh pr create --title "Add <skill-name>" --body "..."
```

## ✍️ Anatomía de un SKILL.md

```markdown
---
name: skill-name-here
description: "Una línea de qué hace y cuándo usarlo. ≤ 160 bytes."
---

# Skill Name

Cuerpo del skill. Markdown. Legible por humanos Y por agentes.

## When to use this skill
- Caso 1
- Caso 2

## Workflow
1. Paso 1
2. Paso 2

## Examples
...

## Related
- enlaces a otros skills, docs, etc.
```

## ✅ Checklist antes de abrir PR

- [ ] El frontmatter tiene `name` y `description` (≤ 160 bytes)
- [ ] El `description` empieza con un verbo o un nombre (no un workflow entero)
- [ ] El cuerpo tiene secciones claras (`When to use`, `Workflow`, etc.)
- [ ] Los ejemplos son copy-pasteable
- [ ] No hay secrets ni credenciales en los ejemplos
- [ ] El SKILL.md es lean (no copy-paste de toda la doc de DESY)
- [ ] Si el skill tiene `references/`, los paths están bajo ese dir

## 🛡️ Revisión

Cada PR pasa por:
1. **Scan automático** (security scanner del workshop)
2. **Revisión manual** por el maintainer
3. **Test manual** (probar el skill en un agente real)

Un skill se "aprueba" cuando se mergea a `main`.
