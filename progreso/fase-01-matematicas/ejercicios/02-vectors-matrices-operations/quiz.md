# Quiz — L02 Vectors, Matrices & Operations

> Nota: preguntas reconstruidas desde el resumen de sesión compactada; el enunciado exacto puede variar ligeramente.

## Pre-quiz — 3/3

### P1
**Pregunta:** Una capa densa tiene pesos de forma (128, 784) y entrada de forma (784, 1). ¿Cuál es la forma de la salida?
**Respuesta elegida:** (128, 1) ✅
**Correcto:** Sí — regla $(m\times n) @ (n\times p) = (m\times p)$: dimensiones internas deben coincidir.

### P2
**Pregunta:** ¿Cuál es la diferencia entre multiplicación elemento a elemento (`*`) y multiplicación matricial (`@`)?
**Respuesta elegida:** Elemento a elemento combina posiciones correspondientes (misma forma); matricial hace productos punto fila×columna (las dimensiones internas deben coincidir) ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Qué hace el broadcasting al sumar un bias de forma (128,) a una salida de forma (32, 128)?
**Respuesta elegida:** Estira el bias a lo largo de las filas para que encaje con (32, 128) ✅
**Correcto:** Sí

---

## Post-quiz — 3/3

### P1
**Pregunta:** Una matriz tiene determinante 0. ¿Qué significa geométricamente?
**Respuesta elegida:** Colapsa el espacio en una dimensión menor — la transformación aplasta puntos y pierde información de forma irreversible (no existe inversa) ✅
**Correcto:** Sí

### P2
**Pregunta:** En tu red de dos capas, la capa oculta produjo `[0, 0, 0, 0.745]`. ¿Qué fenómeno ilustra esto?
**Respuesta elegida:** La sparsity de ReLU — la mayoría de neuronas se apagan (output = 0 si preactivación < 0); solo un subconjunto queda activo ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Por qué se usa multiplicación matricial (y no elemento a elemento) en las capas densas de una red neuronal?
**Respuesta elegida:** Porque cada neurona de salida combina TODAS las entradas (productos punto fila×columna) — eso requiere matmul, no multiplicación posición a posición ✅
**Correcto:** Sí

---

**Resultado final: pre 3/3 · post 3/3** ✅
Dominó los tres conceptos —reglas de shape, element-wise vs. matmul, broadcasting/determinante— desde el pre-quiz.
