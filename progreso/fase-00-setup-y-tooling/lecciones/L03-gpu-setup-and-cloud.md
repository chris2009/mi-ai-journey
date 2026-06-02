# L03 — Configuración de GPU y Cloud

> Entrenar en CPU está bien para aprender. Entrenar en serio necesita una GPU.

**Tipo:** Build  
**Lenguajes:** Python  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~45 minutos

---

## Objetivos de aprendizaje

- Verificar disponibilidad de GPU local usando `nvidia-smi` y la API CUDA de PyTorch
- Configurar Google Colab con GPU T4 para experimentos gratuitos en la nube
- Hacer un benchmark de multiplicación de matrices CPU vs GPU y medir el speedup
- Estimar el modelo más grande que cabe en tu VRAM usando la regla de fp16

---

## El problema

La mayoría de lecciones de las fases 1-3 corren bien en CPU. Pero cuando empieces a entrenar CNNs, transformers o LLMs (fases 4+), necesitas aceleración GPU. Un entrenamiento que tarda 8 horas en CPU tarda 10 minutos en GPU.

Tienes tres opciones: GPU local, GPU en la nube, o Google Colab (gratis).

---

## El concepto

```
Opciones disponibles:

1. GPU NVIDIA local
   Costo: $0 (ya la tienes)
   Setup: Instalar CUDA + cuDNN
   Mejor para: uso regular, datasets grandes

2. Google Colab (tier gratuito)
   Costo: $0
   Setup: Ninguno
   Mejor para: experimentos rápidos, sin GPU en casa

3. GPU en la nube (Lambda, RunPod, Vast.ai)
   Costo: $0.20-2.00/hr
   Setup: SSH + instalar
   Mejor para: entrenamiento serio, modelos grandes
```

---

## Paso a paso

### Opción 1: GPU NVIDIA local

Verificar si tienes una:

```bash
nvidia-smi
```

Verificar en Python:

```python
import torch

print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Versión CUDA: {torch.version.cuda}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    mem = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"VRAM: {mem:.1f} GB")
```

### Opción 2: Google Colab

1. Ir a colab.research.google.com
2. Runtime > Change runtime type > T4 GPU
3. Correr `!nvidia-smi` para verificar

### Sin GPU? Sin problema.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando: {device}")
```

La mayoría de lecciones funcionan en CPU.

---

## Benchmark: CPU vs GPU

```python
import torch
import time

size = 5000

a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

# Medir CPU
start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    # Warm-up CRÍTICO: primera operación incluye JIT + inicialización CUDA
    _ = a_gpu @ b_gpu
    torch.cuda.synchronize()

    # Medir GPU (con warm-up)
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")
```

> **Resultado real en RTX 4070 Laptop:** CPU: 0.463s, GPU (con warm-up): 0.032s → **15x más rápido**
> Sin warm-up el resultado fue 2x — el overhead de inicialización CUDA distorsiona la primera medición.

---

## Estimación de VRAM

Regla general fp16: 2 bytes por parámetro

```
8.6 GB VRAM → ~4.3B parámetros en fp16
8.6 GB VRAM → ~8-9B parámetros en int4 (cuantizado)
```

Modelos que caben en una RTX 4070 Laptop (8.6 GB):
- Llama 3.2 3B ✅
- Phi-3.5 Mini (3.8B) ✅

---

## Ejercicios

1. Corre el benchmark CPU vs GPU y registra tus tiempos
2. Verifica cuánta VRAM tienes y estima el modelo más grande que cabe (2 bytes/parámetro en fp16)
3. Si no tienes GPU, corre el benchmark en Google Colab y compara

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| CUDA | "Programación GPU" | Plataforma de cómputo paralelo de NVIDIA para correr código en GPU |
| VRAM | "Memoria GPU" | RAM de video en la GPU, separada de la RAM del sistema. Limita el tamaño del modelo |
| fp16 | "Media precisión" | Punto flotante de 16 bits, usa la mitad de memoria que fp32 con pérdida mínima de precisión |
| CUDA warm-up | "Primera operación lenta" | La primera operación GPU incluye JIT + inicialización CUDA — no medir sin warm-up |
| int4 | "Cuantización a 4 bits" | ~0.5 bytes/parámetro — cabe el doble de modelo en la misma VRAM |
