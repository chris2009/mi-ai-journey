# Quiz — L12 Debugging & Profiling

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 2/2

### P1
**Pregunta:** Usas `tracemalloc` para medir la memoria de un tensor PyTorch de 13 MB y muestra solo 131 bytes. ¿Por qué?
**Respuesta elegida:** PyTorch asigna memoria de tensores en C++ (fuera del heap Python) — `tracemalloc` solo ve objetos Python puros, no el buffer del tensor ✅
**Correcto:** Sí — para medir memoria real de tensores usar `tensor.element_size() * tensor.nelement()` o `torch.cuda.memory_allocated()`.

### P2
**Pregunta:** Tu modelo tiene `loss/train → 0` y `loss/val → 1.94 (plana)` en TensorBoard. ¿Qué indica?
**Respuesta elegida:** Overfitting clásico — el modelo memorizó el set de entrenamiento pero no generalizó al set de validación ✅
**Correcto:** Sí — la divergencia entre train loss bajando a cero y val loss estancada es la firma visual del overfitting.

---

## Post-quiz — 3/3

### P1
**Pregunta:** `isnan()` retorna `False` para un tensor pero `loss` es `nan`. ¿Cómo es posible?
**Respuesta elegida:** El tensor contiene `inf` o `-inf` — `isnan()` no detecta infinitos. `inf - inf = nan`, `inf * 0 = nan`. Hay que verificar también con `isinf()` ✅
**Correcto:** Sí

### P2
**Pregunta:** `cProfile` muestra que el backward pass (37.7%) y el optimizer Adam (24.1%) dominan el tiempo. ¿Qué tipo de cuello de botella es?
**Respuesta elegida:** CPU-bound en la fase de gradientes — el tiempo de cómputo está en Python/CPU, no en I/O ni en el GPU. Optimizar: mover más operaciones al GPU ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Qué ventaja tiene `breakpoint()` condicional (`if loss > 100: breakpoint()`) sobre poner un breakpoint fijo en el debugger?
**Respuesta elegida:** Solo activa el debugger cuando ocurre la condición anómala — no interrumpe los miles de steps normales, solo para cuando el loss explota ✅
**Correcto:** Sí — fundamental para debugging de training loops largos donde el bug solo aparece en ciertos batches.

---

**Resultado final: pre 2/2 · post 3/3** ✅
