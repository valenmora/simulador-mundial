# PROMPT_RTC_CICD

## ROL

Sos un DevOps Engineer Senior especializado en GitHub Actions, CI/CD, GitHub Pages y aplicaciones Python 3.12.

Tenés como contexto el archivo `ARQUITECTURA.md` del proyecto "Simulador Mundial 2026".

Tomalo como fuente de verdad para:

* Arquitectura del proyecto
* Estructura de carpetas
* Dependencias
* Cobertura actual (~89%)
* Tests existentes
* Hallazgos actuales de Ruff
* Flujo de simulación del Mundial

El proyecto es una aplicación FastAPI que genera un sitio estático con los resultados de una simulación completa del Mundial 2026.

NO existe backend desplegado en producción.

La simulación se ejecuta durante el pipeline y genera archivos estáticos dentro de `dist/`, que luego se publican mediante GitHub Pages.

El servicio `SimulatorService` auto-crea los equipos necesarios cuando la base está vacía, por lo que puede utilizarse:

DATABASE_URL=sqlite:///:memory:

sin pasos previos de seed manual.

---

## TAREA

Generar el archivo completo: .github/workflows/ci.yml completo para el Simulador Mundial 2026.

El pipeline tiene una arquitectura específica: en vez de hacer deploy de un backend, el job 4 SIMULA EL MUNDIAL durante el build de GitHub Actions y genera un sitio estático en dist/ que se publica en GitHub Pages sin ningún servidor en producción.
Esto es posible porque el SimulatorService auto-seedea 32 equipos si la BD está vacía (services/simulator_service.py línea 37-38). Con sqlite:///: memory: el pipeline puede correr POST /simulator/run sin preparación previa.
En caso de no contar con un repositorio para subir el archivo para ver en acción el pipeline pedime el remoto 


El workflow debe contener EXACTAMENTE 5 jobs encadenados mediante `needs`.

Orden:

1. lint
2. tests
3. quality-gate
4. simulate
5. deploy

---

## DISPARADORES

### Push

Ejecutar pipeline completo:

```yaml
on:
  push:
    branches:
      - main
```

### Pull Request

Ejecutar jobs 1-4 únicamente:

```yaml
pull_request:
  branches:
    - main
```

---

## PERMISSIONS

Definir a nivel workflow:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

---

## JOB 1 — Lint Ruff

### Nombre

Lint Ruff

### Configuración

```yaml
runs-on: ubuntu-latest
```

### Steps

* Checkout repositorio
* Setup Python 3.12
* Instalar Ruff

```bash
pip install ruff
```

* Ejecutar:

```bash
ruff check .
```

### Comportamiento esperado

Si Ruff devuelve errores, el pipeline debe fallar.

No usar herramientas adicionales.

---

## JOB 2 — Tests + Coverage

### Nombre

Tests + Coverage

### Depends

```yaml
needs: lint
```

### Configuración

```yaml
runs-on: ubuntu-latest
```

### Variables

```yaml
DATABASE_URL=sqlite:///:memory:
```

### Steps

* Checkout
* Setup Python 3.12
* Instalar dependencias

```bash
pip install -r requirements.txt
```

* Ejecutar tests

```bash
pytest \
  --cov=. \
  --cov-report=xml \
  --ignore=tests/test_frontend_smoke.py
```

### Artifact

Subir:

```text
coverage.xml
```

Artifact name:

```text
coverage-report
```

---

## JOB 3 — Quality Gate ≥ 80%

### Nombre

Quality Gate ≥ 80%

### Depends

```yaml
needs: tests
```

### Configuración

```yaml
runs-on: ubuntu-latest
```

### Steps

* Descargar artifact coverage-report

* Parsear coverage.xml utilizando EXCLUSIVAMENTE:

```python
xml.etree.ElementTree
```

No usar:

* coverage.py
* jq
* xmllint
* dependencias externas

### Regla

Leer:

```xml
<coverage line-rate="0.89">
```

Extraer:

```python
line-rate
```

Validar:

```text
line-rate >= 0.80
```

### Resultado

Si cobertura < 80%:

```bash
exit 1
```

Mostrar en logs:

```text
Coverage: XX.XX%
```

---

## JOB 4 — Simular Mundial 2026

### Nombre

Simular Mundial 2026

### Depends

```yaml
needs: quality-gate
```

### Configuración

```yaml
runs-on: ubuntu-latest
```

### Variables

```yaml
DATABASE_URL=sqlite:///:memory:
```

### Steps

* Checkout
* Setup Python 3.12
* Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar

```bash
python seed_and_simulate.py
```

### Validaciones

Debe existir:

```text
dist/index.html
```

Si no existe:

```bash
exit 1
```

### Salida de logs

Imprimir:

```text
🏆 Campeón: <nombre>
```

para que quede visible en GitHub Actions.

### Artifact

Subir carpeta:

```text
dist/
```

Artifact name:

```text
github-pages
```

Además configurar Pages mediante:

```yaml
actions/configure-pages@v5
```

---

## JOB 5 — Deploy GitHub Pages

### Nombre

Deploy GitHub Pages

### Depends

```yaml
needs: simulate
```

### Condición

Ejecutar solamente cuando:

```yaml
github.ref == 'refs/heads/main'
```

### Configuración

```yaml
runs-on: ubuntu-latest
```

### Environment

```yaml
environment:
  name: github-pages
```

### Deploy

Usar:

```yaml
actions/deploy-pages@v4
```

### Resultado esperado

GitHub Actions debe mostrar automáticamente la URL publicada.

---

## RESTRICCIONES

* Generar YAML válido.
* No devolver explicaciones.
* No devolver texto fuera del YAML.
* No incluir comentarios innecesarios.
* Utilizar versiones estables actuales de Actions.
* Todos los jobs deben tener nombres descriptivos.
* Mantener el workflow minimalista.
* El archivo debe estar listo para copiar y pegar en `.github/workflows/ci.yml`.

---

## VALIDACIÓN FINAL

Antes de devolver el resultado verificar:

* Sintaxis YAML correcta.
* Existen exactamente 5 jobs.
* Todos los jobs usan `needs`.
* Coverage gate ≥ 80%.
* Artifact coverage-report generado.
* Artifact github-pages generado.
* Deploy solo en main.
* Compatible con Python 3.12.
* Compatible con GitHub Pages.
* Compatible con FastAPI + pytest.
* Compatible con sqlite:///:memory:.
* Devuelve únicamente el contenido del archivo YAML.
