# Mi Diario de AI Engineering

Documentación acumulativa de todo lo aprendido fase a fase.  
Cada sección incluye conceptos clave, scripts reales y resultados de quiz.

> **Regla:** Este archivo se actualiza al terminar cada lección.

---

## Fase 00 — Setup & Tooling

### L01 — Dev Environment ✅

**Concepto central:** El stack de AI Engineering tiene 4 capas. Se instala de abajo hacia arriba.

```
Capa 4 → AI/ML libraries    (PyTorch, NumPy, HuggingFace)
Capa 3 → Language runtimes  (Python, Node.js, Rust)
Capa 2 → Package managers   (uv, pnpm, cargo)
Capa 1 → Sistema base       (OS, shell, git, GPU drivers)
```

**Setup completado:**

| Herramienta | Versión | Nota |
|-------------|---------|------|
| Python | 3.13.0 | vía uv |
| PyTorch | 2.6.0+cu124 | con soporte CUDA |
| CUDA | 12.5 | para RTX 4070 Laptop |
| uv | 0.11.17 | 10-100x más rápido que pip |
| Node.js | 20.19.5 | para herramientas JS |
| Rust | 1.96.0 | vía rustup (no snap/apt) |

**Resultado de verificación:**
```
7/7 core checks passed, 2/2 GPU checks passed
```

**Reglas que aprendí:**
- Siempre usar `source .venv/bin/activate` antes de trabajar
- Nunca instalar Rust con snap/apt — solo con `rustup`
- Virtual environment aísla el proyecto del sistema global

---

### L02 — Git & Collaboration ✅

**Concepto central:** Flujo de trabajo diario con git.

```
Working Directory → Staging Area → Local Repo → GitHub
    (editas)          git add        git commit    git push
```

**Comandos esenciales:**

```bash
git add archivo.py           # staging
git commit -m "mensaje"      # snapshot local
git push origin main         # sincronizar con GitHub

git checkout -b experiment/mi-idea   # crear y cambiar de rama
git merge experiment/mi-idea         # integrar cambios
git log --oneline -10                # ver historial
```

**Regla crítica para AI Engineering:**
```gitignore
# Nunca commitear checkpoints de modelos (pesan GB)
*.pt
*.pth
*.safetensors
*.ckpt
*.bin
*.h5
```

**Quiz: 3/3** ✅

---

### L03 — GPU Setup & Cloud ✅

**Concepto central:** La GPU no es mágicamente rápida — hay que medirla bien.

**Script del benchmark CPU vs GPU:**

```python
# progreso/fase-00-setup-y-tooling/ejercicios/03_gpu_benchmark.py
import torch
import time

size = 5000
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    # Warm-up obligatorio: la primera op incluye JIT + init de CUDA
    torch.cuda.synchronize()
    _ = a_gpu @ b_gpu
    torch.cuda.synchronize()

    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU (con warm-up): {gpu_time:.3f}s")
    print(f"Speedup real: {cpu_time / gpu_time:.0f}x")

    # Calcular VRAM disponible
    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
    params_fp16 = (vram_gb * 1e9) / 2
    print(f"VRAM disponible: {vram_gb:.1f} GB")
    print(f"Modelo más grande en fp16: ~{params_fp16/1e9:.1f}B parámetros")
```

**Resultados reales (RTX 4070 Laptop):**

| Medición | CPU | GPU | Speedup |
|----------|-----|-----|---------|
| Sin warm-up | 0.463s | 0.230s | 2x (falso) |
| Con warm-up | 0.463s | 0.032s | **15x (real)** |

**Reglas de medición:**
- Siempre hacer warm-up antes de medir GPU
- Usar `torch.cuda.synchronize()` antes y después — la GPU es asíncrona
- Sin sync, el timer para antes de que la GPU termine

**Estimación de VRAM → tamaño de modelo:**

```
fp16  → 2 bytes/parámetro  → 8.6 GB soporta ~4.3B params
int4  → 0.5 bytes/parámetro → 8.6 GB soporta ~8-9B params (cuantizado)

Modelos que caben en RTX 4070 Laptop:
- Llama 3.2 3B     ✅ (en fp16)
- Phi-3.5 Mini 3.8B ✅ (en fp16)
- Llama 3.1 8B     ✅ (en int4)
```

---

### L04 — APIs & Keys ✅

**Concepto central:** Toda API de AI es HTTP POST con JSON. El SDK es solo un wrapper conveniente.

**Script con SDK (forma recomendada):**

```python
# progreso/fase-00-setup-y-tooling/ejercicios/04_api_call.py
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()  # carga .env antes de leer variables

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[{"role": "user", "content": "What is a neural network in one sentence?"}]
)

print(response.content[0].text)
```

**Script con HTTP crudo (lo que hace el SDK por debajo):**

```python
# progreso/fase-00-setup-y-tooling/ejercicios/04_api_raw_http.py
import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

url = "https://api.anthropic.com/v1/messages"
headers = {
    "Content-Type": "application/json",
    "x-api-key": os.environ["ANTHROPIC_API_KEY"],
    "anthropic-version": "2023-06-01",
}
body = json.dumps({
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
}).encode()

req = urllib.request.Request(url, data=body, headers=headers, method="POST")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print("Respuesta:", result["content"][0]["text"])
    print(json.dumps(result, indent=2))
```

**Campos clave de la respuesta JSON:**

```json
{
  "content": [{"text": "...respuesta..."}],
  "usage": {
    "input_tokens": 12,
    "output_tokens": 38
  },
  "stop_reason": "end_turn"
}
```

**Reglas de seguridad:**
```bash
# .env (nunca commitear)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```
```python
load_dotenv()              # primero
os.environ["API_KEY"]      # luego leer
```

**Patrón de manejo de errores:**
```python
# Rate limit: esperar y reintentar con backoff exponencial
# 429 = demasiadas requests → esperar más
# 401 = key inválida → revisar .env
# 500 = error del servidor → reintentar
```

---

### L05 — Jupyter Notebooks ✅

**Concepto central:** Explorar en notebooks, ejecutar en scripts.

**Magic commands esenciales:**

```python
%timeit expresion          # microbenchmark: corre N veces, promedia
%%time                     # wall time de la celda completa: corre 1 vez
%matplotlib inline         # plots inline en el notebook
!comando_shell             # ejecutar bash desde el notebook
%env VARIABLE              # ver variable de entorno
```

**Ejercicio 1 — Benchmark list comprehension vs NumPy:**

```python
import numpy as np
import time

# %timeit (promedio de miles de runs — el número real)
%timeit [x**2 for x in range(100_000)]   # → 5.25 ms
%timeit np.arange(100_000)**2            # → 42.3 μs  ← 124x más rápido

# Medición manual (una sola vez — incluye overhead, menos precisa)
start = time.perf_counter()
_ = [x**2 for x in range(100_000)]
list_time = time.perf_counter() - start

start = time.perf_counter()
_ = np.arange(100_000)**2
numpy_time = time.perf_counter() - start

print(f"Speedup manual: {list_time/numpy_time:.0f}x")  # → 5x (distorsionado)
```

> **Lección:** La medición manual (1 run) mintió igual que el GPU sin warm-up.
> `%timeit` promedia miles de runs y da el tiempo real: **NumPy es 124x más rápido**.

**Ejercicio 2 — DataFrame + Plot auto-contenido:**

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "modelo": ["Linear Regression", "Random Forest", "Neural Network", "XGBoost"],
    "accuracy": [0.72, 0.89, 0.94, 0.91],
    "tiempo_train_s": [0.1, 2.3, 45.6, 8.2],
})
df  # en Jupyter: renderiza tabla HTML automáticamente

# Plot: barras + scatter en la misma figura
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar(df["modelo"], df["accuracy"], color="steelblue")
axes[1].scatter(df["tiempo_train_s"], df["accuracy"], s=100)
plt.tight_layout()
plt.show()
```

**Trampas comunes y sus fixes:**

| Trampa | Síntoma | Fix |
|--------|---------|-----|
| Ejecución fuera de orden | Funciona solo en tu máquina | `Kernel > Restart & Run All` antes de compartir |
| Estado oculto | Variable existe aunque borraste la celda | Reiniciar kernel regularmente |
| Memory leak | Proceso crece sin parar | `del var` + `gc.collect()` |

**Cuándo usar cada uno:**

| Notebook ✅ | Script ✅ |
|-------------|----------|
| Explorar datos | Pipelines de entrenamiento |
| Prototipar modelos | Utilidades reutilizables |
| Visualizar resultados | Código en producción |
| Explicar tu trabajo | Código con schedule |

**Setup de kernel en VS Code + WSL (fix documentado):**

```bash
# Registrar el venv como kernel de Jupyter
python -m ipykernel install --user --name=ai-engineering \
    --display-name "Python (AI Engineering)"

# Instalar extensiones para WSL (necesario aunque estén en Windows)
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.python
```

**Quiz: pre 1/2 · post 3/3** ✅

---

### L06 — Python Environments ✅

**Concepto central:** Cada proyecto necesita su propio entorno aislado. Sin eso, es dependency hell.

**El problema:**
```
Proyecto A → torch 2.4 (CUDA 12.4)
Proyecto B → torch 2.1 (CUDA 11.8)
Sin venvs → solo puede existir uno → el otro se rompe
```

**Herramientas:**

| Tool | Cuándo usarla |
|------|--------------|
| `uv venv` | La mayoría de proyectos — 10-100x más rápido |
| `venv` (built-in) | Si no tienes `uv` |
| `conda` | Necesitas controlar CUDA toolkit o estás en cluster |

**Regla crítica — uv no instala pip:**
```bash
# venvs creados con uv NO tienen pip interno — usar siempre:
uv pip list
uv pip install paquete
uv pip show paquete
```

**Aislamiento demostrado en ejercicio:**
```bash
# Crear segundo venv y demostrar que los paquetes no se mezclan
uv venv /tmp/test-env
source /tmp/test-env/bin/activate
uv pip install "numpy==1.26.4"
python -c "import numpy; print(numpy.__version__)"  # → 1.26.4

deactivate
source .venv/bin/activate
python -c "import numpy; print(numpy.__version__)"  # → 2.4.4 — ¡aislados!
```

**pyproject.toml con grupos opcionales:**
```toml
[project]
name = "mi-ai-journey"
requires-python = ">=3.11"
dependencies = ["numpy>=1.26", "matplotlib>=3.8", "jupyter>=1.0"]

[project.optional-dependencies]
torch = ["torch>=2.3", "torchvision>=0.18"]
llm   = ["anthropic>=0.39", "openai>=1.50", "python-dotenv>=1.0"]
ml    = ["scikit-learn>=1.4", "pandas>=2.0"]
```
```bash
uv pip install -e ".[torch]"        # base + PyTorch
uv pip install -e ".[llm]"          # base + LLM SDKs
uv pip install -e ".[torch,llm]"    # todo junto
```

**CUDA compatibility check:**
```bash
nvidia-smi | grep "CUDA Version"                    # → 12.5 (driver)
python -c "import torch; print(torch.version.cuda)" # → 12.4 (PyTorch)
# Regla: PyTorch CUDA <= driver CUDA ✅
# Si PyTorch CUDA > driver → "CUDA not available" aunque la GPU esté presente
```

**Resultado verificado (RTX 4070 Laptop):**

| | Versión |
|---|---|
| Driver CUDA | 12.5 |
| PyTorch CUDA | 12.4 ✅ |

**Quiz: pre 2/2 · post 3/3** ✅

---

## Fase 01 — Math Foundations ⬜

*Pendiente*

---

## Fase 02 — ML Fundamentals ⬜

*Pendiente*

---

## Fase 03 — Deep Learning Core ⬜

*Pendiente*

---

## Fase 04 — Computer Vision ⬜

*Pendiente*

---

## Fase 05 — NLP Foundations to Advanced ⬜

*Pendiente*

---

## Fase 06 — Speech & Audio ⬜

*Pendiente*

---

## Fase 07 — Transformers Deep Dive ⬜

*Pendiente*

---

## Fase 08 — Generative AI ⬜

*Pendiente*

---

## Fase 09 — Reinforcement Learning ⬜

*Pendiente*

---

## Fase 10 — LLMs from Scratch ⬜

*Pendiente*

---

## Fase 11 — LLM Engineering ⬜

*Pendiente*

---

## Fase 12 — Multimodal AI ⬜

*Pendiente*

---

## Fase 13 — Tools & Protocols ⬜

*Pendiente*

---

## Fase 14 — Agent Engineering ⬜

*Pendiente*

---

## Fase 15 — Autonomous Systems ⬜

*Pendiente*

---

## Fase 16 — Multi-Agent & Swarms ⬜

*Pendiente*

---

## Fase 17 — Infrastructure & Production ⬜

*Pendiente*

---

## Fase 18 — Ethics, Safety & Alignment ⬜

*Pendiente*

---

## Fase 19 — Capstone Projects ⬜

*Pendiente*
