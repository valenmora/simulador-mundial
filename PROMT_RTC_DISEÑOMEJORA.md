# Nueva mejora de UI – Sección Final del Torneo

## Rol

Actúa como un Senior UI/UX Designer especializado en aplicaciones deportivas (FIFA, UEFA, ESPN y Flashscore) y como un Senior Frontend Engineer.

Tu única responsabilidad es mejorar la presentación visual.

No debes modificar:

- lógica
- APIs
- estado
- navegación
- componentes funcionales
- modelos
- servicios
- tests
- pipelines
- jobs

Todos los Test Cases y Jobs de CI/CD deben continuar pasando.

---

# Objetivo

Rediseñar la parte final del torneo para que tenga una jerarquía visual más profesional.

Actualmente existen dos secciones independientes:

- Tercer Puesto
- Final

Visualmente parecen dos pantallas distintas.

Quiero que ambas formen parte de un mismo bloque denominado:

🏆 FASE FINAL

---

# Nueva estructura

Eliminar los dos encabezados independientes.

En su lugar mostrar un único encabezado.

Ejemplo:

┌────────────────────────────────────────────────────────────────────┐
                         🏆 FASE FINAL
└────────────────────────────────────────────────────────────────────┘

Debajo del encabezado colocar ambas Cards en la misma fila.

Desktop:

┌────────────────────────────┐    ┌──────────────────────────────────────┐
│ 🥉 Tercer Puesto           │    │ 🏆 Final                            │
│                            │    │                                      │
│ Curazao      1 : 0 ALG     │    │ Irán          1 : 0        Suecia    │
│                            │    │                                      │
│ 🥉 Clasifica Curazao       │    │ 🏆 CAMPEÓN IRÁN                     │
└────────────────────────────┘    └──────────────────────────────────────┘

---

# Jerarquía visual

La Final debe ser claramente el partido más importante.

Distribución recomendada:

Tercer Puesto:
35% del ancho

Final:
65% del ancho

No utilizar dos columnas idénticas.

La Final debe tener mayor protagonismo.

---

# Card Final

Debe destacar respecto del resto del torneo.

Características:

- ligeramente más ancha
- marcador más grande
- mayor espacio interior
- badge de Campeón
- trofeo visible
- mejor jerarquía tipográfica

Ejemplo:

🏆 FINAL

Irán          1 : 0          Suecia

──────────────────────────────

🏆 CAMPEÓN DEL MUNDO

IRÁN

---

# Card Tercer Puesto

Mantener el mismo estilo visual del resto de las Cards.

No debe competir visualmente con la Final.

Agregar únicamente:

🥉 Tercer Puesto

y

🥉 Clasifica Curazao

---

# Responsive

Desktop

Mostrar ambas Cards en una misma fila.

Tercer Puesto:
35%

Final:
65%

Tablet

Mantener ambas Cards lado a lado únicamente si existe espacio suficiente.

En caso contrario:

Tercer Puesto

Final

una debajo de la otra.

Mobile

Siempre una debajo de la otra.

---

# Diseño

Mantener el mismo lenguaje visual utilizado en el resto del torneo:

- mismo border radius
- misma sombra
- misma paleta
- misma tipografía
- mismos espaciados

La única excepción es que la Final debe tener mayor jerarquía visual.

---

# Restricciones

No modificar ninguna funcionalidad.

No alterar lógica.

No romper componentes reutilizables.

No cambiar comportamiento.

No introducir dependencias innecesarias.

---

# Criterios de aceptación

✅ Solo cambia el diseño.

✅ La lógica permanece intacta.

✅ Desktop muestra una única sección "FASE FINAL".

✅ La Final ocupa aproximadamente el 65% del ancho.

✅ El Tercer Puesto ocupa aproximadamente el 35%.

✅ El usuario identifica inmediatamente cuál es la Final.

✅ Responsive correctamente implementado.

✅ Todos los Test Cases continúan pasando.

✅ Todos los Jobs de CI/CD continúan en estado OK.

✅ Sin errores de compilación, linting ni regresiones funcionales.