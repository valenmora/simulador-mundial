# ROLE

Actúa como un **Senior UI/UX Designer** y **Senior Frontend Engineer** con experiencia en aplicaciones deportivas (FIFA, UEFA, ESPN, Flashscore).

Tu objetivo es mejorar únicamente la **experiencia visual** de la pantalla de las fases eliminatorias del Mundial 2026.

Debes pensar como un diseñador profesional: jerarquía visual, espaciado, alineación, tipografía, responsive y accesibilidad.

---

# IMPORTANTE

**NO debes modificar la lógica del sistema.**

No debes:

* modificar APIs
* modificar modelos
* modificar servicios
* modificar hooks
* modificar estado
* modificar lógica de negocio
* modificar cálculos
* modificar navegación
* modificar tests
* modificar jobs
* modificar pipelines

La única responsabilidad es **rediseñar la interfaz visual**.

El comportamiento funcional debe permanecer exactamente igual.

---

# Objetivo

Rediseñar completamente la vista de:

* Octavos
* Cuartos
* Semifinal
* Final

para que tenga apariencia de una aplicación deportiva moderna inspirada en FIFA, UEFA o Flashscore.

Debe transmitir sensación de producto profesional.

La prioridad absoluta es que el usuario identifique rápidamente:

* los equipos
* el marcador
* quién clasificó

---

# Layout

Utilizar un contenedor centrado.

Max Width:

1400px

Background:

gris muy claro (#f4f6f9)

Utilizar CSS Grid.

Desktop:

2 columnas

Tablet:

1 columna

Mobile:

1 columna

Gap entre Cards:

24px

No utilizar una lista infinita cuando exista espacio horizontal disponible.

---

# Header

Cada fase debe tener un encabezado elegante.

Ejemplo:

🏆 OCTAVOS DE FINAL

Características:

* azul oscuro
* texto blanco
* mayúsculas
* bold
* letter spacing
* border radius
* padding amplio

---

# Card del partido

Cada partido será una Card independiente.

Características:

* fondo blanco
* border radius 14px
* sombra suave
* padding 24px

Cada Card tendrá tres secciones.

---

## 1. Equipos + marcador

Mostrar ambos equipos en una sola línea.

Ejemplo:

🇩🇪 Alemania        1 : 1        🇧🇪 Bélgica

El marcador debe ser el elemento visual dominante.

Marcador:

* 42–54 px
* bold
* perfectamente centrado

Equipos:

* semibold
* alineados verticalmente

Banderas:

* aproximadamente 40x28 px

Si el nombre del país es largo:

Ejemplo:

República Democrática del Congo

debe poder ocupar dos líneas sin romper el layout.

---

## 2. Información adicional

Debajo del marcador mostrar únicamente cuando corresponda.

Ejemplos:

Penales 5-4

Tiempo suplementario

Gol de oro

Utilizar tipografía más pequeña.

No competir visualmente con el marcador.

---

## 3. Clasificado

Separador horizontal.

Luego mostrar centrado:

🏆 CLASIFICA BÉLGICA

Características:

* color azul
* bold
* padding superior

Además, resaltar la Card del ganador mediante un borde lateral izquierdo (4–5 px) con el color principal del torneo para facilitar la identificación visual sin sobrecargar la interfaz.

---

# Espaciado

Dar prioridad al espacio en blanco.

Utilizar aproximadamente:

Padding interno:
24px

Gap interno:
18px

Separación entre secciones:
16px

Nunca comprimir los elementos.

---

# Responsive

Desktop:

2 Cards por fila.

Tablet:

1 Card por fila.

Mobile:

Todo al 100%.

Reducir automáticamente:

* marcador
* tipografía
* banderas

Los nombres largos deben hacer wrap.

Nunca generar scroll horizontal.

---

# Animaciones

Hover:

* ligera elevación
* transición 200 ms

No utilizar animaciones excesivas.

---

# Accesibilidad

Mantener alto contraste.

Tipografía fácilmente legible.

No depender únicamente del color para indicar el ganador.

---

# Consistencia visual

Mantener el mismo estilo para:

* Octavos
* Cuartos
* Semifinal
* Final

Toda la aplicación debe verse como un único producto y no como pantallas independientes.

---

# Restricciones técnicas

* No modificar la lógica existente.
* No romper componentes reutilizables.
* No introducir dependencias innecesarias.
* Reutilizar estilos existentes cuando sea posible.
* Mantener el código limpio y consistente con el proyecto.

---

# Criterios de aceptación

La tarea se considera finalizada únicamente si:

* ✅ La funcionalidad permanece exactamente igual.
* ✅ Solo cambia la presentación visual.
* ✅ El diseño es completamente responsive.
* ✅ No existen regresiones funcionales.
* ✅ Todos los Test Cases continúan pasando.
* ✅ Todos los Jobs/Pipelines de CI/CD continúan en estado **OK**.
* ✅ No se introducen errores de compilación, linting ni formateo.
* ✅ El resultado visual se asemeja a una aplicación deportiva profesional (FIFA, UEFA o Flashscore).

Antes de finalizar, verifica que el proyecto compile correctamente y que ningún cambio visual haya impactado el comportamiento funcional.
