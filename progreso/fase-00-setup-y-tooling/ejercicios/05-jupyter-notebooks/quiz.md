# Quiz — L05 Jupyter Notebooks

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 1/2

### P1
**Pregunta:** ¿Cuál es la diferencia entre `%timeit` y `%%time`?
**Respuesta elegida:** (respuesta incorrecta) ❌
**Correcto:** No — `%timeit` corre el código miles de veces y promedia (microbenchmark preciso); `%%time` mide el wall time de toda una celda en una sola ejecución (rápido pero menos preciso). El benchmark manual mintió igual que el GPU sin warm-up.

### P2
**Pregunta:** ¿Cuándo usar un notebook vs un script `.py`?
**Respuesta elegida:** Notebook para explorar/prototipar/visualizar; script para pipelines, producción y código con schedule ✅
**Correcto:** Sí

---

## Post-quiz — 3/3

### P1
**Pregunta:** Tu notebook produjo resultados distintos al correrlo en orden vs. correr celdas sueltas. ¿Qué lo causó y cómo lo arreglas?
**Respuesta elegida:** Estado oculto — una variable de una celda borrada sigue viva en memoria. Fix: `Kernel > Restart & Run All` ✅
**Correcto:** Sí

### P2
**Pregunta:** Benchmark real: list comprehension tardó 5.25 ms y NumPy 42.3 μs para 100k elementos. ¿Cuánto más rápido es NumPy?
**Respuesta elegida:** ~124x más rápido — NumPy opera en C con vectorización SIMD, sin overhead del intérprete Python por elemento ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Qué hace `!nvidia-smi` dentro de un notebook?
**Respuesta elegida:** Ejecuta el comando en el shell del sistema operativo desde la celda del notebook ✅
**Correcto:** Sí — el prefijo `!` pasa el comando al shell, igual que correrlo en la terminal.

---

**Resultado final: pre 1/2 · post 3/3** ✅
El concepto de `%timeit` vs `%%time` fue el único fallado en el pre-quiz.
