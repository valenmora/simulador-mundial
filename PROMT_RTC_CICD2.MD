Diagnosticar un pipeline rojo

```text
[ROL]
Sos un DevOps engineer senior con experiencia en GitHub Actions y aplicaciones FastAPI
en Python. Tenés cargado como contexto el archivo ARCHITECTURE.md del Simulador
Mundial 2026.

Stack del proyecto:
- FastAPI + SQLite + SQLAlchemy (BD en memoria en CI/CD: sqlite:///:memory:)
- pytest-cov 5.x — cobertura actual 89%, umbral Quality Gate: 80%
- Ruff — 10 hallazgos conocidos en la codebase (ver ARCHITECTURE.md)
- seed_and_simulate.py — levanta FastAPI internamente y llama a /simulator/run
- GitHub Pages — deploy del dist/ generado por el job 'simulate'
- test_frontend_smoke.py SIEMPRE excluido en CI (requiere browser)

[TAREA]
El pipeline del Simulador Mundial 2026 falló. Este es el log completo del job:

--- LOG DE GITHUB ACTIONS ---
Parse coverage .xml and validate
Run import xml.etree.ElementTree as ET
Coverage: 77.83%
Quality Gate FAIL: coverage 77.83% < 80%
Error: Process completed with exit code 1.

Respondé con exactamente esta estructura:

## Job que falló

🔍 Quality Gate >= 80%

## Step exacto
Parse coverage .xml and validate

## Causa raíz
Run import xml.etree.ElementTree as ET
Coverage: 77.83%
Quality Gate FAIL: coverage 77.83% < 80%
Error: Process completed with exit code 1.


## Verificación local antes del próximo push
[comando PowerShell para reproducir y confirmar el fix]

## ¿Bloquea el Mundial?
[¿el error impide que el simulador corra? sí/no + por qué en una línea]

[CRITERIO]
- NO modifiques el workflow ni archivos que no sean el fix mínimo necesario
- Si el log no tiene suficiente información, indicá qué flag agregar al comando fallido
- Si el problema es en el job simulate: revisar primero si DATABASE_URL está seteado
  y si seed_and_simulate.py puede importar la app sin errores de dependencias
- El fix debe lograr pipeline verde en el siguiente push
- NO resuelvas nada. Solo analizá y reportá.
```
