
Usar estos prompts después de cargar `ARQUITECTURA.md` como contexto del proyecto.
Todos los prompts tienen datos estáticos del proyecto — no hay que editar nada antes de pegar.

**Instrucción para el agente antes de cada prompt:**
> NO resuelvas nada. NO modifiques el código. Analizá y respondé según lo que se pide.

---

## Prompt 1 — Generar el workflow completo de GitHub Actions

```text
[ROL]
Sos un DevOps engineer senior con experiencia en GitHub Actions, pipelines de CI/CD
y aplicaciones FastAPI en Python 3.12.

Tenés cargado como contexto el archivo ARCHITECTURE.md del Simulador Mundial 2026.
Usalo como fuente de verdad: stack tecnológico, estructura del proyecto, quality gates,
cobertura actual (89% — 69 tests) y hallazgos reales de Ruff.

[TAREA]
Generá el archivo .github/workflows/ci.yml completo para el Simulador Mundial 2026.

El pipeline tiene una arquitectura específica: en vez de hacer deploy de un backend,
el job 4 SIMULA EL MUNDIAL durante el build de GitHub Actions y genera un sitio
estático en dist/ que se publica en GitHub Pages — sin ningún servidor en producción.

Esto es posible porque el SimulatorService auto-seedea 32 equipos si la BD está vacía
(services/simulator_service.py línea 37-38). Con sqlite:///:memory: el pipeline puede
correr POST /simulator/run sin preparación previa.
En caso de no contar con un repositorio para subir el archivo para ver en acción el pipeline pedime el remoto
El workflow debe tener exactamente 5 jobs encadenados con needs:

JOB 1 — lint
  runs-on: ubuntu-latest
  - pip install ruff
  - ruff check .
  (Si algún hallazgo de Ruff es MAJOR, el pipeline para acá)

JOB 2 — tests
  needs: lint | runs-on: ubuntu-latest
  - pip install -r requirements.txt
  - python -m pytest tests/ --cov=. --cov-report=xml --ignore=tests/test_frontend_smoke.py -q
  - env: DATABASE_URL=sqlite:///:memory:
  - upload-artifact: name=coverage-report, path=coverage.xml

JOB 3 — quality-gate
  needs: tests | runs-on: ubuntu-latest
  - download-artifact: coverage-report
  - Parsear coverage.xml con xml.etree.ElementTree (solo stdlib, no instalar nada)
  - Verificar line-rate >= 0.80 → si falla: "Quality Gate FAIL: cobertura X% < 80%"
  (Cobertura actual del proyecto: 89% → pasa. Si alguien sube código sin tests y baja a
  79%, el pipeline para aquí y nadie llega al Mundial)

JOB 4 — simulate
  needs: quality-gate | runs-on: ubuntu-latest
  - pip install -r requirements.txt
  - python seed_and_simulate.py
    (Este script levanta FastAPI con BD en memoria, llama a POST /simulator/run,
     GET /metrics/dashboard y GET /teams/, guarda los JSON en dist/data/ y genera
     dist/index.html estático con los datos embebidos — sin fetch al backend)
  - env: DATABASE_URL=sqlite:///:memory:
  - Validar que dist/index.html existe
  - Imprimir el campeón del mundo (leer dist/data/simulation.json)
  - upload-pages-artifact: path=dist/

JOB 5 — deploy
  needs: simulate | runs-on: ubuntu-latest
  - if: github.ref == 'refs/heads/main'
  - environment: github-pages
  - uses: actions/deploy-pages@v4

El workflow debe dispararse en:
- push a branches: [main]   → pipeline completo + deploy
- pull_request a branches: [main] → jobs 1-4, sin deploy

Permissions necesarios para GitHub Pages:
  contents: read
  pages: write
  id-token: write

[CRITERIO]
- YAML válido, listo para commitear en .github/workflows/ci.yml
- Cada job tiene un name descriptivo con el número de step (ej: "② Tests + Coverage")
- El job quality-gate parsea el XML con xml.etree.ElementTree — cero dependencias extra
- El job simulate imprime el campeón al final para que aparezca en el log del pipeline
- El job deploy usa environment: github-pages para mostrar la URL publicada en Actions
- NO incluyas pasos innecesarios ni comentarios de más de 2 líneas
- Al final del archivo, agregá un comentario con el comando PowerShell para probar
  todo localmente antes del push: $env:DATABASE_URL="sqlite:///:memory:"; python seed_and_simulate.py
```
