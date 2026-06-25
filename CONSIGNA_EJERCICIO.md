# 🧪 Ejercicio Clase 5 — QA y Testing con GenIA
## Simulador Mundial 2026 | IA para Developers — CDA × Alkemy

---

## Contexto

Sos QA Engineer del equipo que construyó el Simulador del Mundial 2026.
Tu trabajo es demostrar que el sistema funciona correctamente antes del deploy.

Vas a usar el **modo interactivo del agente**: en lugar de pedirle todo de una,
describís lo que querés testear y el agente pregunta, planifica y pide tu GO
antes de generar nada.

**Regla de oro:** cargá `QA.md` en el agente antes de empezar.
Sin ese archivo, el agente no entra en modo interactivo y genera tests genéricos.

---

## Setup

```bash
cd ejercicio-alumnos/
pip install -r requirements.txt
uvicorn main:app --reload        # en una terminal
pytest tests/ -v                 # verificar que arranca en verde
```

---

## Cómo usar el modo interactivo

1. Cargá `QA.md` en el agente
2. Abrí `PROMPT_RTC_QA.md`
3. Usá el **Prompt RTC - Parte 1** y completá:
   - qué endpoint o flujo querés testear
   - qué comportamiento te preocupa
4. El agente pregunta — respondé con precisión
5. El agente muestra un PLAN — leelo antes de aprobar
6. Si el plan está bien: escribí **El plan está aprobado. Aplica el plan.**
7. El agente genera casos + código + evidencia para documentar

No le pidas al agente "generame tests" directamente. Primero tiene que preguntar y mostrar un plan.

---

## Parte 1 — Modo interactivo: endpoint a elección (25 min)

Elegí UNO de estos endpoints y activá el modo interactivo:

**Opción A — POST /simulator/run**
```
Quiero testear el endpoint de simulación.
Me preocupa [completar con lo que te preocupa a vos].
```

**Opción B — GET /metrics/dashboard**
```
Quiero testear el dashboard de métricas.
Me preocupa [completar con lo que te preocupa a vos].
```

**Opción C — POST /teams/ o POST /players/**
```
Quiero testear el CRUD de equipos/jugadores.
Me preocupa [completar con lo que te preocupa a vos].
```

### Lo que tenés que entregar

Archivo `SESION_INTERACTIVA.md` con:
- El prompt RTC completado con el endpoint/riesgo elegido
- Las preguntas que hizo el agente y tus respuestas
- El PLAN que mostró el agente (copiado del chat)
- Tu decisión: aplica el plan / ajustes pedidos / NO-GO (por qué)
- El código pytest generado (o el link al archivo)

---

## Parte 2 — Tests en verde (20 min)

Corrés los tests generados por el agente:
```bash
pytest tests/test_qa_clase5.py -v
```

Si alguno falla:
- Describile el error al agente en el mismo chat
- El agente ajusta el código
- Repetís hasta que todos estén en verde

### Lo que tenés que entregar

Archivo `tests/test_qa_clase5.py` con todos los tests en verde.
Screenshot o copia del output de pytest al final.

---

## Parte 3 — Smoke test frontend manual (15 min)

Usá el bloque **Prompt RTC - Parte 3: smoke test frontend** de `PROMPT_RTC_QA.md`.

El agente te va a preguntar sobre el dispositivo, las secciones críticas
y si querés enfocarte en algo específico. Respondé con lo que realmente
necesitás verificar.

Ejecutá el checklist que genera el agente manualmente en el browser.

### Lo que tenés que entregar

Archivo `SMOKE_TEST_REPORT.md` con:
- El checklist generado por el agente
- Estado de cada ítem: ✅ Pasó / ❌ Falló / ⚠️ Observación
- Si algo falló: comportamiento observado vs esperado

---

## Parte 4 — QA Report final (20 min)

Activá el modo interactivo para el reporte:
```
Quiero generar el QA Report de esta sesión.
Tengo X tests en verde, Y fallaron.
El smoke test tuvo estos resultados: [resumí].
```

El agente te pregunta sobre el contexto del build, la audiencia del reporte
y qué nivel de detalle necesitás. Respondé y dale GO.

### Lo que tenés que entregar

Archivo `QA_REPORT.md` con conclusión **GO / NO-GO / GO con observaciones**.

---

## Entrega final

```
ejercicio-alumnos/
├── SESION_INTERACTIVA.md      ← Parte 1 (conversación + plan + go)
├── tests/
│   └── test_qa_clase5.py      ← Parte 2 (tests en verde)
├── SMOKE_TEST_REPORT.md       ← Parte 3
└── QA_REPORT.md               ← Parte 4
```

---

## Criterios de evaluación

| Dimensión | Peso |
|-----------|------|
| La sesión interactiva muestra ida y vuelta real con el agente (no un prompt directo) | 25% |
| El plan fue validado antes del GO — se nota que el alumno lo leyó y decidió | 20% |
| Los tests nuevos no duplican los existentes y todos pasan en verde | 30% |
| El QA Report tiene una conclusión GO/NO-GO fundamentada con evidencia real | 25% |
