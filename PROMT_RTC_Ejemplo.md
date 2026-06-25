## Prompt 3 — Revisar el workflow generado contra la arquitectura real

```text
[ROL]
Sos un DevOps engineer senior y code reviewer. Tenés cargado el archivo
ARCHITECTURE.md del Simulador Mundial 2026 como fuente de verdad.

[TAREA]
Revisá el siguiente workflow de GitHub Actions:

--- WORKFLOW ---
[PEGAR AQUÍ EL CONTENIDO DE .github/workflows/ci.yml]
--- FIN DEL WORKFLOW ---

Verificá que el workflow es consistente con estos datos reales del proyecto:

PROYECTO (fuente: ARCHITECTURE.md):
- Python: 3.12
- Tests: 69 pasados | Cobertura: 89% | Umbral Quality Gate: 80%
- BD en CI: sqlite:///:memory: (NO worldcup.db — es un archivo, no sirve en CI)
- Excluir siempre: tests/test_frontend_smoke.py (requiere browser)
- Script de simulación: seed_and_simulate.py (auto-seedea, no necesita fixtures)
- Hallazgos Ruff conocidos: 10 errores — el F841 en simulator_service.py:141 es MAJOR
- Deploy target: GitHub Pages vía actions/upload-pages-artifact@v3 + actions/deploy-pages@v4

Respondé con:

## Consistencia con el proyecto
[tabla: ítem | esperado | encontrado en el workflow | ¿OK?]

## Problemas encontrados
[lista numerada — archivo y línea del workflow si aplica]

## Riesgos en producción
[¿qué puede fallar en un repo real que no se nota en este ejemplo?]

## Veredicto
GO ✅ / NO-GO 🚨 + razón en una línea

[CRITERIO]
- NO sugieras cambios de arquitectura ni herramientas alternativas
- NO resuelvas nada — solo analizá y reportá
- El veredicto GO requiere que los 5 jobs estén presentes, la BD sea en memoria
  y el deploy target sea GitHub Pages
```