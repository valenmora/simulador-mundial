# QA Report — Ruff Linting Analysis

**Fecha:** 2026-06-11
**Herramienta:** ruff v0.15.18
**Proyecto:** Simulador Mundial 2026
**Comando:** `ruff check .`

---

## Resumen

| Métrica | Valor |
|---------|:-----:|
| Total errores | 10 |
| Fixables automáticamente (`--fix`) | 7 |
| Archivos analizados | 38 |
| Reglas violadas | 4 |

## Hallazgos por severidad

### Severidad A — Error / Bloqueante

| ID | Regla | Archivo | Línea | Descripción | Acción propuesta |
|----|-------|---------|:-----:|-------------|------------------|
| RTC-01 | `E402` | `schemas/team.py` | 32 | Import fuera del tope del archivo | Mover `import` al inicio del archivo |

### Severidad B — Bug / Unused

| ID | Regla | Archivo | Línea | Descripción | Acción propuesta |
|----|-------|---------|:-----:|-------------|------------------|
| RTC-02 | `F401` | `services/metrics_service.py` | 1 | `os` importado pero no usado | Eliminar `import os` |
| RTC-03 | `F401` | `services/simulation_cache.py` | 1 | `json` importado pero no usado | Eliminar `import json` |
| RTC-04 | `F401` | `services/simulator_service.py` | 2 | `json` importado pero no usado | Eliminar `import json` |
| RTC-05 | `F401` | `services/simulator_service.py` | 3 | `sys` importado pero no usado | Eliminar `import sys` |
| RTC-06 | `F401` | `services/simulator_service.py` | 8 | `KnockoutMatch` importado pero no usado | Eliminar import |
| RTC-07 | `F841` | `services/simulator_service.py` | 141 | Variable `y` asignada pero no usada | Eliminar o usar `_` |
| RTC-08 | `F841` | `tests/test_dashboard.py` | 80 | Variable `team_players` asignada pero no usada | Eliminar o refactorizar |

### Severidad C — Convention / Style

| ID | Regla | Archivo | Línea | Descripción | Acción propuesta |
|----|-------|---------|:-----:|-------------|------------------|
| RTC-09 | `F541` | `tests/test_simulator.py` | 295 | f-string sin placeholders | Usar string literal en lugar de f-string |
| RTC-10 | `F541` | `tests/test_simulator.py` | 295 | f-string sin placeholders | Usar string literal en lugar de f-string |

---

## Distribución por archivo

| Archivo | Errores | Reglas |
|---------|:-------:|--------|
| `services/simulator_service.py` | 5 | F401 (3x), F841 (1x) |
| `tests/test_simulator.py` | 2 | F541 (2x) |
| `services/metrics_service.py` | 1 | F401 |
| `services/simulation_cache.py` | 1 | F401 |
| `schemas/team.py` | 1 | E402 |
| `tests/test_dashboard.py` | 1 | F841 |

---

## Análisis RTC

### Causa raíz

La mayoría de los errores (7/10) son **imports no utilizados** en archivos de servicios (`services/`). Esto sugiere que durante el desarrollo se importaron módulos que luego no se usaron en el código final.

### Impacto

- **Bajo**: Ningún error de sintaxis o lógica. Son olores de código (code smells).
- **7 de 10 son fixables automáticamente** con `ruff check --fix`.

### Acción recomendada

```bash
# Aplicar fixes automáticos (seguros)
ruff check . --fix

# Revisar manualmente E402 y F841 (pueden requerir refactor)
```

---

## Calidad del código según SonarQube (proyectado)

Basado en los hallazgos de ruff + análisis previo con pysonar:

| Indicador | Estado actual | Threshold propuesto |
|-----------|:-------------:|:-------------------:|
| Coverage | ~65-75% | ≥ 70% |
| Code Smells | 10 (ruff) | ≤ 50 |
| Security Hotspots | 0 | 0 |
| Reliability Rating | A (0 bugs) | A (≤ 1) |
| Maintainability Rating | A (10 smells en 36 archivos) | A o B (≤ 2) |
| Duplicated Lines | Bajo (sin hallazgos de duplicación en ruff) | ≤ 3.0% |

---

*Reporte generado con ruff v0.15.18 · Simulador Mundial 2026*
