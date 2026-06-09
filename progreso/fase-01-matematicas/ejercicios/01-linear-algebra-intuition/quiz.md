# Quiz — L01 Linear Algebra Intuition

> Nota: preguntas reconstruidas desde el resumen de sesión compactada; el enunciado exacto puede variar ligeramente.

## Pre-quiz — 2/3

### P1
**Pregunta:** ¿Qué mide el producto punto entre dos vectores?
**Respuesta elegida:** La similitud direccional (alineación) entre los vectores ✅
**Correcto:** Sí

### P2
**Pregunta:** ¿Qué significa que una matriz tenga rango deficiente (rango < n)?
**Respuesta elegida:** (respuesta incorrecta seleccionada) ❌
**Correcto:** No — el rango deficiente significa que algunas columnas son combinaciones lineales de las demás: hay dimensiones redundantes y el sistema no tiene solución única. Es la base de LoRA: las actualizaciones de pesos se confinan a un subespacio de bajo rango.

### P3
**Pregunta:** ¿Qué hace la proyección de un vector **a** sobre un vector **b**?
**Respuesta elegida:** Extrae la componente de **a** en la dirección de **b** ✅
**Correcto:** Sí

---

## Post-quiz — 3/3

### P1
**Pregunta:** ¿Por qué la cosine similarity se usa en búsqueda semántica (RAG)?
**Respuesta elegida:** Porque mide el ángulo entre vectores (independiente de la magnitud), capturando similitud de significado ✅
**Correcto:** Sí

### P2
**Pregunta:** ¿Qué implica que la matriz de features tenga rango deficiente para un modelo de ML?
**Respuesta elegida:** Los features son redundantes/correlacionados → la matriz es mal condicionada → pesos inestables ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Qué produce Gram-Schmidt y por qué importa numéricamente?
**Respuesta elegida:** Una base ortonormal (vectores perpendiculares de norma 1) — más estable que una base arbitraria para cálculos numéricos ✅
**Correcto:** Sí

---

**Resultado final: pre 2/3 · post 3/3** ✅
El concepto rango/LoRA fue el único fallado en el pre-quiz y quedó dominado en el post-quiz.
