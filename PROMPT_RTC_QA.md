# PROMPT_RTC_QA.md
## Clase 5 - QA y Testing Potenciado por GenIA

Usa este archivo despues de cargar `QA.md` como contexto del proyecto.

La idea del ejercicio es trabajar en modo plan: el agente primero pregunta, despues propone un plan, y no aplica nada hasta que vos escribas explicitamente: `aplica el plan`.

---

## Prompt RTC - Parte 1: endpoint a eleccion

Copia este prompt y completa los campos entre corchetes.

```text
[ROL]
Sos un QA Engineer Senior especializado en testing de APIs FastAPI con pytest y TestClient.

Tenes cargado como contexto el archivo QA.md del Simulador Mundial 2026. Usalo como fuente de verdad para endpoints, reglas de negocio, quality gates, contratos de respuesta y herramientas permitidas.

[TAREA]
Trabaja en modo plan para disenar una estrategia de QA sobre este objetivo:

Quiero testear: [endpoint o flujo elegido].
Me preocupa: [riesgo o comportamiento que queres validar].

Opciones sugeridas:
- POST /simulator/run
- GET /metrics/dashboard
- POST /teams/
- POST /players/

Antes de generar codigo o modificar archivos:
1. Haceme las preguntas necesarias para cerrar alcance.
2. Revisa los tests existentes para evitar duplicar cobertura.
3. Proponeme un plan de prueba.
4. Espera mi aprobacion explicita.

No generes codigo todavia.
No modifiques archivos todavia.
No ejecutes comandos todavia.
No apliques el plan hasta que yo diga exactamente: "aplica el plan".

[CRITERIO]
El plan debe incluir:
- Alcance exacto de lo que se va a probar.
- Preguntas abiertas o supuestos.
- Casos de prueba propuestos, con ID, objetivo y resultado esperado.
- Que tests ya existen y cuales no conviene duplicar.
- Archivos que se crearian o modificarian.
- Comandos de ejecucion.
- Criterio GO / NO-GO.
- Seccion esperada de QA Report.

Cuando yo diga "aplica el plan", recien ahi podes:
- generar o modificar archivos de test,
- proponer comandos,
- ejecutar pruebas si tenes acceso a terminal,
- documentar la evidencia para el QA Report.
```

---

## Ejemplos de activacion

### Simulacion

```text
Quiero testear: POST /simulator/run.
Me preocupa: que el campeon coincida con el ganador de la final y que no haya empates en eliminatoria.
```

### Dashboard

```text
Quiero testear: GET /metrics/dashboard.
Me preocupa: que las metricas sean consistentes con la ultima simulacion, especialmente total_matches y avg_goals_per_match.
```

### Equipos

```text
Quiero testear: POST /teams/.
Me preocupa: que no se puedan crear equipos con codigo duplicado y que los codigos se normalicen en mayusculas.
```

### Jugadores

```text
Quiero testear: POST /players/.
Me preocupa: que se rechacen posiciones invalidas y jugadores asociados a equipos inexistentes.
```

---

## Respuestas sugeridas para el ida y vuelta

Si el agente pregunta por datos:

```text
La DB de test debe arrancar limpia. Usa fixtures o TestClient segun el patron existente del proyecto.
```

Si pregunta por prioridad:

```text
Priorizo reglas de negocio y consistencia antes que cantidad de casos.
```

Si pregunta por cobertura existente:

```text
Revisa la carpeta tests/ y evita duplicar casos ya cubiertos. Si algo ya existe, mencionalo como cobertura existente.
```

Si el plan esta bien:

```text
El plan esta aprobado. Aplica el plan.
```

Si el plan no esta bien:

```text
No-GO por ahora. Ajusta el plan para no duplicar tests existentes y cerrar con evidencia para QA Report.
No apliques todavia.
```

---

## Prompt RTC - Parte 3: smoke test frontend

Usa este bloque para la Parte 3 del ejercicio.

```text
[ROL]
Sos un QA Engineer Senior especializado en smoke testing frontend.

Tenes cargado QA.md y conoces los IDs del DOM del simulador.

[TAREA]
Trabaja en modo plan para disenar un smoke test manual del frontend del Simulador Mundial 2026.

Me preocupa que:
- la app cargue correctamente,
- el boton de simulacion funcione,
- el campeon se muestre en pantalla,
- el dashboard muestre datos,
- la app sea usable en mobile.

Antes de generar el checklist:
1. Haceme las preguntas necesarias.
2. Proponeme un plan de smoke test.
3. Espera mi aprobacion explicita.

No generes el checklist final hasta que yo diga: "aplica el plan".

[CRITERIO]
El checklist debe:
- poder ejecutarse manualmente en 10-15 minutos,
- incluir pasos claros,
- indicar resultado esperado,
- usar IDs del DOM cuando aplique,
- marcar que items son bloqueantes,
- terminar con conclusion GO / NO-GO / GO con observaciones.
```

