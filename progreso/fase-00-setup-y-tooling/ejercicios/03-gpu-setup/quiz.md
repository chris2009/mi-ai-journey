# Quiz — L03 GPU Setup & Cloud

> Nota: preguntas reconstruidas desde sesión compactada. No se encontró score de quiz separado en notas.md para esta lección.

## Quiz — score no registrado explícitamente

### P1
**Pregunta:** Mides el speedup GPU vs CPU y obtienes 2x sin warm-up y 15x con warm-up. ¿Cuál es el número real?
**Respuesta elegida:** 15x — el primer run incluye overhead de inicialización CUDA (JIT + init), lo que distorsiona la medición ✅
**Correcto:** Sí — siempre hacer al menos un run de warm-up antes de medir performance GPU.

---

### P2
**Pregunta:** Tu GPU tiene 8.6 GB de VRAM. ¿Cuántos parámetros puedes cargar en fp16?
**Respuesta elegida:** ~4.3B parámetros (fp16 = 2 bytes/parámetro → 8.6 GB / 2 = 4.3B) ✅
**Correcto:** Sí — con cuantización int4 (0.5 bytes/parámetro) caben el doble: ~8-9B parámetros.

---

**Benchmark verificado:**
```
CPU:  0.463s  (matriz 5000×5000)
GPU:  0.032s  (con warm-up)
Speedup real: 15x
```
