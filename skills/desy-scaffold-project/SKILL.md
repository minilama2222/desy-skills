---
name: desy-scaffold-project
description: "Scaffold a DESY project with the chosen library. Clone official starter, install deps with NVM, rename, verify dev server. Use after choose-library."
---

# desy-scaffold-project

Crea el esqueleto de un proyecto nuevo con la librería DESY elegida: clona el starter oficial de Bitbucket, configura NVM, instala dependencias, renombra el proyecto y verifica que arranca.

## When to use this skill

- Acabas de decidir qué librería usar (`desy-choose-library`) y necesitas arrancar
- Vas a empezar un proyecto DESY desde cero
- Quieres migrar un proyecto existente al stack de una librería DESY

## Inputs que necesitas

Antes de aplicar el skill, confirma con el equipo:

1. **Librería elegida** (desy-html / desy-angular / desy-ionic)
2. **Nombre del proyecto** (sin espacios, kebab-case: `mi-app-tramites`)
3. **Node version target** (NVM, .nvmrc) — recomendado: LTS más reciente
4. **¿LTS o latest?** Para desy-angular, hay LTS (v13 = Angular 16) o latest (v19)

## Workflow general (las 3 librerías)

```
1. NVM setup (si no lo tiene)
2. Clonar starter de Bitbucket
3. Renombrar el proyecto (solo desy-angular)
4. Instalar dependencias
5. Arrancar dev server y verificar
6. Commit inicial
```

---

## Pasos específicos por librería

### 🟦 desy-html (sitios web, portales)

**Stack:** Vite + Tailwind CSS + Nunjucks + Open Sans (Google Fonts)

**Comandos:**

```bash
# 1. (Si no tienes NVM) Instalar NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# Reinicia la terminal o: source ~/.bashrc

# 2. Instalar Node LTS
nvm install --lts
nvm use --lts
node --version  # verificar

# 3. Crear .nvmrc para fijar la versión del proyecto
echo "lts/*" > .nvmrc

# 4. Clonar starter
git clone https://bitbucket.org/sdaragon/desy-html-starter.git mi-proyecto
cd mi-proyecto

# 5. Instalar dependencias
npm install

# 6. Arrancar dev server
npm run dev
# Por defecto arranca en http://localhost:5173 (Vite)
# Verás la página de inicio del starter

# 7. Verificación rápida
curl -sI http://localhost:5173/ | head -3
# Espera: HTTP/1.1 200 OK

# 8. Build de producción (opcional)
npm run build
ls dist/  # debería tener los HTML compilados

# 9. Commit inicial
git add . && git commit -m "feat: scaffold from desy-html-starter"
```

**Plantillas starter** (revisar antes de implementar):
- `https://desy.aragon.es/plantillas-sin-sesion-iniciada-p1.html.md` (landing webapp)
- `https://desy.aragon.es/plantillas-con-sesion-iniciada.html.md` (con auth)
- `https://desy.aragon.es/plantillas-portal-p1.html.md` (portales)
- `https://desy.aragon.es/plantillas-edicion.html.md` (CRUD)
- `https://desy.aragon.es/plantillas-correo-p1.html.md` (email HTML)

---

### 🟧 desy-angular (webapps, intranets)

**Stack:** Angular 19 + esbuild + TypeScript + RxJS + Tailwind utility classes

**Comandos:**

```bash
# 1. (Si no tienes NVM) Instalar NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc

# 2. Instalar Node LTS
nvm install --lts
nvm use --lts
node --version  # verificar

# 3. Crear .nvmrc
echo "lts/*" > .nvmrc

# 4. Clonar starter (con latest o LTS)
# Latest (Angular 19):
git clone https://bitbucket.org/sdaragon/desy-angular-starter.git mi-app
# LTS (Angular 16, v13):
# git clone --branch v13 https://bitbucket.org/sdaragon/desy-angular-starter.git mi-app

cd mi-app

# 5. Renombrar el proyecto (CRÍTICO en desy-angular)
# El starter se llama 'desy-angular-starter'; hay que renombrarlo en:
#   - angular.json (projects.desy-angular-starter → projects.mi-app)
#   - package.json (name: "mi-app")
#   - src/index.html (<title>desy-angular-starter</title>)
#   - src/app/ (estructura interna, generalmente app.module.ts y app.component.ts)
#   - README.md

# Manualmente o con un script (recomendado):
find . -type f \( -name "*.json" -o -name "*.html" -o -name "*.ts" -o -name "*.md" \) -not -path "./node_modules/*" -not -path "./.git/*" -exec sed -i 's/desy-angular-starter/mi-app/g' {} \;

# Verifica con:
grep -r "desy-angular-starter" --include="*.json" --include="*.html" --include="*.ts" --include="*.md" . 2>/dev/null | grep -v node_modules
# Si queda algo, renómbralo a mano

# 6. Instalar dependencias
# IMPORTANTE: --legacy-peer-deps por conflictos de peer dependencies en algunos paquetes
npm install --legacy-peer-deps

# 7. Arrancar dev server
npm run dev
# Por defecto en http://localhost:4200 (Angular)
# Verás la página de inicio con el logo DESY

# 8. Verificación
curl -sI http://localhost:4200/ | head -3
# Espera: HTTP/1.1 200 OK

# 9. Build de producción
npm run build-prod
ls dist/  # debería tener los bundles minificados

# 10. Tests E2E (Playwright)
npm run e2e

# 11. Commit
git add . && git commit -m "feat: scaffold from desy-angular-starter (renamed to mi-app)"
```

**Plantillas starter** (revisar antes de implementar):
- `https://desy.aragon.es/plantillas-sin-sesion-iniciada-p1.html.md` (landing)
- `https://desy.aragon.es/plantillas-con-sesion-iniciada.html.md` (con auth)
- `https://desy.aragon.es/plantillas-edicion.html.md` (CRUD)

**Convención de desy-angular v19:**
- Componentes standalone por defecto (`standalone: true`)
- Imports en cada componente (no NgModules)
- Signals para estado local
- Inputs con `[input]="value"`, outputs con `(outputEvent)="handler()"`

---

### 🟪 desy-ionic (apps móviles nativas iOS/Android)

**Stack:** Ionic + Angular + Capacitor (builds nativas iOS/Android) + TypeScript

**Comandos:**

```bash
# 1. Instalar NVM (si no)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc

# 2. Instalar Node LTS
nvm install --lts
nvm use --lts
node --version

# 3. Crear .nvmrc
echo "lts/*" > .nvmrc

# 4. Clonar starter
git clone https://bitbucket.org/sdaragon/desy-ionic.git mi-app
cd mi-app

# 5. Instalar dependencias
npm install

# 6. Arrancar en navegador (para desarrollo rápido sin emulador)
npm start
# http://localhost:8100 (Ionic dev server)
# También puedes usar `ionic serve`

# 7. Verificación
curl -sI http://localhost:8100/ | head -3

# 8. Setup de Capacitor (para builds nativas)
npx cap add ios          # requiere Xcode en macOS
npx cap add android      # requiere Android Studio

# 9. Build + sync a las plataformas
npm run build
npx cap sync              # sincroniza web build a iOS y Android

# 10. Abrir en IDE nativo
npx cap open ios          # abre Xcode
npx cap open android      # abre Android Studio

# 11. Build nativo (en Xcode/Android Studio)
# iOS: Product → Archive → Distribute App
# Android: Build → Generate Signed Bundle / APK

# 12. Tests
npm test                  # unit tests
npm run e2e               # e2e tests (si están configurados)

# 13. Commit
git add . && git commit -m "feat: scaffold from desy-ionic (iOS + Android targets)"
```

**Consideraciones especiales para móvil:**
- **Gestos:** usar directivas nativas de Ionic (swipe, tap, long-press)
- **Accesibilidad táctil:** targets `>= 44x44px` (WCAG 2.5.5)
- **Notificaciones push:** configurar Capacitor Push plugin
- **Almacenamiento offline:** Capacitor Storage o SQLite
- **Capacitor CLI:** `npx cap` para sincronizar, no `ionic cap` (legacy)

**Recursos:**
- Storybook de componentes: `https://desy.aragon.es/desy-ionic`
- Librería Figma: `https://www.figma.com/community/file/1383376074462615538/desy-ionic`
- Capacitor docs: `https://capacitorjs.com/docs`

---

## Verificación post-scaffold

Después de aplicar los pasos, verifica:

```bash
# 1. El dev server arranca
curl -sI http://localhost:5173/  # o :4200 / :8100 según librería
# Espera: HTTP/1.1 200 OK

# 2. La página tiene el título correcto
curl -s http://localhost:5173/ | grep -i "<title>"
# desy-html: el título del starter
# desy-angular: <title>mi-app</title>
# desy-ionic: el título del proyecto

# 3. La página carga el CSS de DESY
curl -s http://localhost:5173/ | grep -i "desy\|tailwind"
# Debe haber referencias a los estilos

# 4. El build de producción funciona
npm run build
ls dist/  # o dist/mi-app/  # debe tener archivos compilados
```

## Gotchas

- **No olvidar `.nvmrc`.** Sin él, cada dev instalará una versión distinta de Node y eso rompe builds.
- **No saltarse `--legacy-peer-deps` en desy-angular.** Las peer dependencies de Angular 19 + algunas librerías de terceros entran en conflicto y la install falla sin esa flag.
- **No renombrar antes de instalar.** `npm install` corre scripts post-install que asumen el nombre original. Renombra PRIMERO, luego instala.
- **No commitear `node_modules` ni `dist/`.** El `.gitignore` del starter ya los excluye, pero verifica.
- **Para desy-ionic, no abrir Xcode/Android Studio antes del primer build.** El comando `npx cap add ios` falla si no hay Xcode instalado. Verifica primero.
- **No usar `ionic cap` (legacy).** Usa `npx cap` (Capacitor CLI directo).
- **En macOS con M1/M2, puede haber issues con `node-gyp`.** Si pasa, instala con `arch -arm64 npm install` o usa Node ARM64.

## Variables de entorno comunes

Aunque DESY no requiere secrets por defecto, conviene tener un `.env` desde el inicio:

```bash
# .env.example (común a las 3 librerías)
NODE_ENV=development
PORT=5173  # o el que corresponda

# Si usas analytics o tracking
ANALYTICS_URL=

# Si integras con servicios externos
API_BASE_URL=
API_KEY=
```

**Nunca** commitear `.env` real — solo `.env.example`.

## Próximos pasos (qué hacer después del scaffold)

1. **Identificar pantallas** que vas a implementar
2. Para cada pantalla, buscar la **plantilla** correspondiente en DESY: `desy-choose-library` → "Plantilla" te da el patrón
3. Para cada componente, generar el código: `desy-implement-component`
4. Validar accesibilidad de cada componente: `desy-validate-accessibility`
5. Tests E2E con Playwright (incluido en desy-angular-starter)

## Examples (resumen)

### Ejemplo: Scaffold de un portal con desy-html

```bash
# 1. Decisión (desy-choose-library)
# Portal web público, SEO crítico → desy-html

# 2. Setup (desy-scaffold-project)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
nvm install --lts
git clone https://bitbucket.org/sdaragon/desy-html-starter.git portal-aragon
cd portal-aragon
npm install
npm run dev
# http://localhost:5173 — listo para maquetar

# 3. Implementar componentes
# (desy-implement-component — generar cada componente)
# Por ejemplo: Header-advanced, footer, cards, formularios

# 4. Validar accesibilidad
# (desy-validate-accessibility — axe-core + tests manuales)
```

### Ejemplo: Scaffold de una webapp con desy-angular

```bash
# 1. Decisión
# Webapp de gestión, equipo Angular 19 → desy-angular latest

# 2. Setup
git clone https://bitbucket.org/sdaragon/desy-angular-starter.git webapp-expedientes
cd webapp-expedientes
find . -type f \( -name "*.json" -o -name "*.html" -o -name "*.ts" -o -name "*.md" \) -not -path "./node_modules/*" -not -path "./.git/*" -exec sed -i 's/desy-angular-starter/webapp-expedientes/g' {} \;
npm install --legacy-peer-deps
npm run dev
# http://localhost:4200 — listo para maquetar

# 3. Implementar
# Tabla avanzada + acciones en lote, modal destructiva, paginación

# 4. Validar
# axe-core + tests de teclado + lector de pantalla
```

### Ejemplo: Scaffold de una app móvil con desy-ionic

```bash
# 1. Decisión
# App para ciudadanía, iOS + Android → desy-ionic

# 2. Setup
git clone https://bitbucket.org/sdaragon/desy-ionic.git mi-app-ciudadana
cd mi-app-ciudadana
npm install
npx cap add ios
npx cap add android
npm start
# http://localhost:8100 — Ionic dev server
npx cap open ios  # abre Xcode
npx cap open android  # abre Android Studio

# 3. Implementar
# Tabs, action sheets, modales, gestos específicos móvil

# 4. Validar
# Accesibilidad táctil (44x44px), gestos, foco en navegación
```

## Related

- **Skill: `desy-choose-library`** — paso anterior, qué librería usar
- **Skill: `desy-implement-component`** — siguiente paso, generar código de componentes
- **Skill: `desy-validate-accessibility`** — siguiente paso, validar WCAG 2.2 AA
- **Repos en Bitbucket:** `https://bitbucket.org/sdaragon/`
- **Tutorial oficial:** `https://desy.aragon.es/como-empezar-tutorial.html.md`
- **Mapa del ecosistema DESY:** [`/docs/ecosystem-map.md`](../../docs/ecosystem-map.md)
