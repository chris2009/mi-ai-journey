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

### L07 — Docker for AI ✅

**Concepto central:** Containers hacen que "funciona en mi máquina" sea cosa del pasado.

**Vocabulario:**

| Término | Analogía | Qué es |
|---------|----------|--------|
| Image | Receta | Plantilla read-only construida desde un Dockerfile |
| Container | Cocina en uso | Instancia corriendo de una image |
| Volume | Carpeta compartida | Directorio del host mapeado al container — persiste |
| docker-compose | Director de orquesta | Levanta múltiples servicios con un comando |

**Regla de orden en Dockerfile — capas de menor a mayor cambio:**
```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04  # nunca cambia → arriba
RUN apt-get install python3 ...              # cambia poco
RUN pip install torch==2.6.0 ...             # cambia poco
COPY ./mi_codigo .                           # cambia mucho → abajo
```
Si `COPY` estuviera arriba: cada cambio de código invalida el cache de PyTorch (GB) y lo reinstala.

**Dockerfile del ejercicio:**
```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y python3 python3-pip git curl \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir torch==2.6.0 \
    --index-url https://download.pytorch.org/whl/cu124

RUN python -m pip install --no-cache-dir numpy jupyter flask

WORKDIR /workspace
EXPOSE 8888 5000
CMD ["python"]
```

**Volumes — críticos en AI:**
```bash
docker run --rm --gpus all \
    -v $(pwd):/workspace \    # código → persiste
    -v ~/models:/models \     # modelos 14GB → se descargan una sola vez
    ai-dev-l07 python train.py
```

**NVIDIA Container Toolkit:**
- Driver CUDA → vive en el **host** (RTX 4070)
- Toolkit CUDA (librerías) → vive **dentro del container**
- `--gpus all` → activa el puente entre ambos

**Docker Compose — stack completo:**
```bash
docker compose up -d      # ai-dev + qdrant en background
docker compose down -v    # para todo + elimina volumes
```
Servicios se hablan por nombre: `http://qdrant:6333` desde ai-dev.

**Resultado verificado:**
```
ai-dev-l07 (7.92 GB): PyTorch 2.6.0+cu124, CUDA: True ✅
RTX 4070 Laptop accesible desde dentro del container
```

**Errores reales encontrados:**
1. `python3.12` no existe en Ubuntu 22.04 repos → usar `python3` (3.10)
2. `torch==2.3.1` no existe para cu124 → versión mínima disponible es `2.4.0`

**Quiz: pre 2/2 · post 2/3** ✅

---

### L08 — Editor Setup ✅

**Concepto central:** El editor es tu co-piloto. Configurarlo bien una vez ahorra 20 minutos diarios de fricción.

**Las 5 capas del setup:**
```
5. Remote Development  → SSH a GPU boxes / cloud VMs
4. Terminal Integration → scripts, nvidia-smi, debug
3. AI-Specific Settings → format-on-save, type checking, rulers
2. Extensions          → Python, Jupyter, Pylance, GitLens, Black, Ruff
1. Base Editor         → VS Code
```

**Extensiones instaladas:**

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension ms-python.debugpy
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
# Remote SSH → instalar en Windows, no en WSL
```

**Settings críticos para AI (`.vscode/settings.json`):**

```jsonc
{
    "python.analysis.typeCheckingMode": "basic",  // detecta shape mismatches de tensores
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true               // nunca formatear a mano
    },
    "editor.rulers": [88, 120],                   // Black corta en 88
    "notebook.output.scrolling": true,            // evita que 10k líneas exploten el panel
    "files.autoSave": "afterDelay",               // nunca correr código stale
    "files.autoSaveDelay": 1000,
    "terminal.integrated.scrollback": 10000,
    "search.exclude": { "**/.venv": true }        // excluye venv de búsquedas
}
```

**Por qué `typeCheckingMode: basic` es crítico para AI:**
Detecta errores de tipo en tensores *antes* de lanzar un training run de 8 horas.
```python
# Pylance marca esto con squiggly rojo:
model(x)        # x es List, pero model espera Tensor
loss(pred, y)   # y es float, pero loss espera LongTensor
```

**Terminal split para monitoreo de GPU:**
```
Panel izquierdo: python train.py
Panel derecho:   watch -n 1 nvidia-smi
```

**SSH config para conectar a GPU remota:**
```
Host gpu-box
    HostName 203.0.113.50
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```
Después: `Remote-SSH: Connect to Host > gpu-box` → VS Code completo en el servidor remoto.

**Alternativas evaluadas:**
| Editor | Veredicto |
|--------|-----------|
| Cursor | VS Code fork con AI integrada — mismas extensiones y settings |
| Windsurf | Igual que Cursor, otra opción AI-first |
| Neovim | Solo si ya eres experto — no aprender junto con AI Engineering |

**Reglas que aprendí:**
- Remote SSH se instala en Windows (inicia la conexión), no en WSL
- `notebook.output.scrolling` es imprescindible antes del primer training loop
- `search.exclude` con `.venv` evita que grep te devuelva miles de resultados de librerías

**Quiz: pre 2/2 · post 3/3** ✅

---

### L09 — Data Management ✅

**Concepto central:** Los datos son el combustible. La librería `datasets` de HF maneja descarga, caché, streaming y conversión de formatos en una sola API.

**Flujo completo:**
```
Hugging Face Hub → datasets library → ~/.cache/huggingface/
       ↓
Conversión: CSV / JSON / Parquet / Arrow
       ↓
Splits: train / val / test → pipeline de entrenamiento
```

**Instalación:**
```bash
uv pip install datasets huggingface_hub
```

**Cargar un dataset (con caché automático):**
```python
from datasets import load_dataset

ds = load_dataset("nyu-mll/glue", "mrpc")
print(ds["train"][0])
# Segunda llamada → carga desde caché, 0 HTTP requests
```

**Streaming — para datasets que no caben en disco:**
```python
ds = load_dataset("nyu-mll/glue", "mrpc", split="train", streaming=True)
for example in ds:
    process(example)  # RAM constante, sin importar el tamaño del dataset
```

**Conversión de formatos:**
```python
sample.to_csv("data.csv")
sample.to_json("data.json")
sample.to_parquet("data.parquet")  # ← el más eficiente para ML
```

**Benchmark real (500 filas GLUE/MRPC):**
```
CSV:     123,970 bytes
JSON:    144,585 bytes
Parquet:  88,412 bytes  → 1.4x más pequeño, mucho más rápido de leer
```

**Splits reproducibles con seed fijo:**
```python
split1 = ds.train_test_split(test_size=0.30, seed=42)
split2 = split1["test"].train_test_split(test_size=0.50, seed=42)
train, val, test = split1["train"], split2["train"], split2["test"]
# Resultado: 2567 / 550 / 551 (70% / 15% / 15%)
# seed=42 → mismos índices en cada máquina
```

**Descargar archivos de modelos:**
```python
from huggingface_hub import hf_hub_download, snapshot_download

path = hf_hub_download("sentence-transformers/all-MiniLM-L6-v2", "config.json")
# Cachea en ~/.cache/huggingface/hub/ — siguiente llamada es instantánea
```

**Manejo de archivos grandes:**
| Método | Complejidad | Cuándo usarlo |
|--------|-------------|---------------|
| `.gitignore` | Baja | Proyectos personales, datos re-descargables |
| Git LFS | Media | Equipos compartiendo pesos vía git (1 GB gratis en GitHub) |
| DVC | Alta | Reproducir experimentos exactos en distintas máquinas |

**Regla aprendida — namespaces en datasets 4.x:**
```python
# datasets 4.x + huggingface_hub 1.x requieren namespace/nombre completo
"nyu-mll/glue"                               # antes: "glue"
"stanfordnlp/imdb"                           # antes: "imdb"
"cornell-movie-review-data/rotten_tomatoes"  # antes: "rotten_tomatoes"
```

**Quiz: pre 2/2 · post 3/3** ✅

---

### L10 — Terminal & Shell ✅

**Concepto central:** La terminal es donde viven los AI engineers. tmux + piping + aliases ahorran horas cada semana.

**Sesión tmux con 3 paneles (ejercicio real):**
```
Panel 1: htop          → monitoreo de procesos del sistema
Panel 2: watch -n1 date → proceso periódico en vivo
Panel 3: python3 script → training simulado (steps 0-999)
Barra:   [training]0:python3*
```

**Redirects esenciales:**
```bash
python train.py > output.log 2>&1            # stdout + stderr al mismo archivo
python train.py > out.log 2> err.log         # separados
grep "loss:" train.log | awk '{print $NF}'   # extraer solo valores numéricos
grep "loss:" train.log | wc -l               # contar epochs: 100
```

**nohup vs tmux:**
| Método | Sobrevive cierre terminal | Reconexión |
|--------|--------------------------|------------|
| `command &` | No | No |
| `nohup command &` | Sí | No — solo archivo de log |
| `tmux` | Sí | **Sí** — en vivo |

**Alias `gpu` en acción (RTX 4070 Laptop):**
```
$ gpu
0, NVIDIA GeForce RTX 4070 Laptop GPU, 6 %, 228 MiB, 8188 MiB, 55
```

**SSH config — simplifica acceso a GPUs remotas:**
```
Host gpu
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/gpu_key
# Resultado: "ssh gpu" en lugar de "ssh -i ~/.ssh/gpu_key ubuntu@192.168.1.100"
```

**Aprendizaje clave:** `source ~/.bashrc` resetea el PATH y desactiva el venv.
Solución: alias `ae` con **ruta absoluta** funciona desde cualquier directorio.

**Quiz: pre 1/2 · post 3/3** ✅

---

### L11 — Linux para AI ✅

**Concepto central:** La mayoría del AI corre en Linux. Si no sabes navegar la terminal en un servidor remoto, pagas GPU idle mientras googleas.

**Filesystem — directorios que importan:**
```
~/           → tu home, aquí trabajas
/tmp/        → temporales, se borran al reiniciar
/var/log/    → logs del sistema, revisar cuando algo falla
/etc/        → configuración del sistema
```

**Ejercicio 1 — archivos creados:**
```bash
$ ls -la ~/proyecto-linux/
-rw-r--r-- 1 xtian xtian 0 Jun 3 02:05 archivo1.txt
-rw-r--r-- 1 xtian xtian 0 Jun 3 02:05 archivo2.txt
-rw-r--r-- 1 xtian xtian 0 Jun 3 02:05 archivo3.txt
# -rw-r--r-- = dueño:rw-, grupo:r--, otros:r--
```

**Ejercicio 2 — proceso con más memoria:**
```
PID 4968: vscode-server (Pylance) — 150M RES, 9.5% MEM
```

**Ejercicio 4 — disco real:**
```
D:\ (Windows): 31G libres (94% usado) — AJUSTADO
pip cache:   6.4 GB  →  pip cache purge
uv cache:    5.8 GB  →  uv cache clean
Total recuperable: ~12.2 GB
```

**kill vs kill -9:**
```bash
kill 12345    # SIGTERM — el proceso puede hacer cleanup antes de morir
kill -9 12345 # SIGKILL — el kernel lo mata sin darle oportunidad de nada
```

**rsync vs scp para transferencias grandes:**
```bash
rsync -avz --progress ./data/ user@gpu:/data/
# Solo transfiere bytes cambiados. Si se interrumpe, reanuda donde quedó.
# scp empezaría de cero.
```

**Gotcha crítico:** Linux es case-sensitive. `Model.py` y `model.py` son archivos distintos.
Un `import Model` que funciona en macOS puede sillar en el servidor Ubuntu.

**Quiz: pre 2/2 · post 3/3** ✅


### L12 — Debugging and Profiling ✅

**Concepto central:** Los bugs de AI no crashean — producen resultados incorrectos silenciosamente. El 80% de los bugs vive en los niveles de Python estándar y operaciones de tensores, no en TensorBoard.

**debug_print — inspección completa de un tensor:**
```python
def debug_print(name, tensor):
    print(f"{name}: shape={tensor.shape}, dtype={tensor.dtype}, "
          f"device={tensor.device}, "
          f"min={tensor.min().item():.4f}, max={tensor.max().item():.4f}, "
          f"has_nan={tensor.isnan().any().item()}")
```

**breakpoint() condicional — solo para cuando algo falla:**
```python
if loss.item() > 100 or torch.isnan(loss):
    breakpoint()  # abre pdb; comandos: p tensor.shape, c, q
```

**Ejercicio 1 — device mismatch detectado:**
```
Model device: cuda:0
  Tensor 0: cpu [MISMATCH]  ← tensor olvidado en CPU
  Tensor 1: cuda:0 [OK]
GPU: RTX 4070 Laptop — tensor 10k×10k: 400.6 MB → 0.0 MB tras empty_cache()
```

**Ejercicio 1b — NaN injection:**
```python
out = out / (out - out)  # 0/0 → NaN/Inf
# debug_print detecta: min=-inf, max=inf, mean=nan
# detect_nan() confirma: NaN loss detected at step 1
# Nota: has_nan=False porque isnan() no atrapa inf
```

**Ejercicio 2 — cProfile breakdown (100 steps, CPU):**
```
backward pass:   0.191s  (37.7%)  ← más lento
Adam optimizer:  0.122s  (24.1%)
linear layers:   0.061s  (12.0%)
zero_grad:       0.026s   (5.1%)
```

**Ejercicio 3 — tracemalloc vs memoria real:**
```
tracemalloc ve:      131 B  (solo objeto Python)
Memoria real tensor: 13.1 MB (50×256×256×float32)
→ Usar: tensor.element_size() * tensor.nelement()
```

**Ejercicio 4 — TensorBoard overfitting:**
```
loss/train: 0.025 → ~0.000  (memoriza 50 muestras)
loss/val:   1.92  → ~1.94   (plana, no generaliza)
→ Overfitting clásico confirmado visualmente
```

**Quiz: pre 2/2 · post 3/3** ✅

---

## Fase 01 — Math Foundations 🔄

### L01 — Linear Algebra Intuition ✅

**Concepto central:** Los vectores son puntos/direcciones en el espacio; las matrices son transformaciones que mueven esos puntos. Toda red neuronal es, en el fondo, una secuencia de transformaciones lineales.

**Vectores desde cero (Python):**

```python
class Vector:
    def __init__(self, components):
        self.components = list(components)

    def dot(self, other):
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        return sum(x**2 for x in self.components) ** 0.5

    def cosine_similarity(self, other):
        return self.dot(other) / (self.magnitude() * other.magnitude())
```

**Ejercicios y resultados reales:**

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | `angle_between` entre vectores | `[1,0]` vs `[0,1]` → 90° · `[1,0]` vs `[1,1]` → 45° · `[1,0]` vs `[1,0]` → 0° |
| 2 | Matriz de escalado $\begin{pmatrix}2&0\\0&3\end{pmatrix}$ sobre $[1,1]$ | `Original: [1, 1]` → `Escalado: [2, 3]` |
| 3 | Cosine similarity entre 5 embeddings aleatorios (dim 50) | par más similar: `word_2` y `word_3` con similitud `0.3000` |
| 4 | Verificar ortonormalidad de Gram-Schmidt vía `np.linalg.qr` | productos punto $\approx 10^{-16}$ (≈0), normas $= 1.0000$ |
| 5 | Matriz $3\times3$ con rango 2 | `[[1,2,3],[4,5,9],[7,8,15]]` → rango = 2 (columnas dependientes: $v_3 = -v_1 + 2v_2$) |
| 6 | Proyección de $[1,2,3]$ sobre $[1,1,1]$ | `[2. 2. 2.]` — el promedio de las componentes repetido |

**Insights que me llevo:**
- El rango deficiente no es solo "menos información" — hace que las ecuaciones normales queden singulares: el sistema no tiene solución única de pesos y queda mal condicionado. Así es como LoRA explota esto a propósito (actualizaciones de pesos confinadas a un subespacio de bajo rango).
- Proyectar un vector sobre $[1,1,\ldots,1]$ da literalmente el promedio de sus componentes — la dirección donde "todas las variables valen lo mismo" es la mejor aproximación constante en mínimos cuadrados. Es la base de centrar datos antes de PCA.
- Diferencia entre advertencia del *type checker* (Pylance, líneas subrayadas en rojo) y error real en tiempo de ejecución: el código puede correr perfecto aunque el editor marque una posible inconsistencia de tipos que la lógica del programa garantiza que nunca ocurre.

**Quiz: pre 2/3 · post 3/3** ✅ (el concepto de rango/LoRA, fallado en el pre-quiz, quedó dominado en el post-quiz)

---

### L02 — Vectors, Matrices & Operations ✅

**Concepto central:** Toda red neuronal es multiplicación de matrices con pasos extra: $\text{output} = \text{relu}(W \mathbin{@} x + b)$. La regla de formas $(m\times n) @ (n\times p) = (m\times p)$ explica cada error de *shape mismatch* en PyTorch, y la diferencia entre multiplicación elemento a elemento (combina posición a posición, mismas formas) y multiplicación matricial (productos punto fila×columna, dimensiones internas coinciden) es la confusión más común de los principiantes.

**Matrix desde cero (Python) — núcleo de las operaciones:**

```python
class Matrix:
    def matmul(self, other):
        return Matrix([
            [sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
             for j in range(other.cols)]
            for i in range(self.rows)
        ])

    def determinant(self):
        if self.shape == (2, 2):
            return self.data[0][0]*self.data[1][1] - self.data[0][1]*self.data[1][0]
        det = 0
        for j in range(self.cols):
            minor = Matrix([[self.data[i][k] for k in range(self.cols) if k != j]
                            for i in range(1, self.rows)])
            det += ((-1) ** j) * self.data[0][j] * minor.determinant()
        return det
```

**Ejercicios y resultados reales:**

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | Verificar $A \mathbin{@} A^{-1} = I$ con 3 matrices $2\times2$ + caso singular | identidad confirmada en los 3 casos (`[[1,0],[0,1]]`); matriz singular `[[1,2],[2,4]]` lanza `ValueError: Matrix is singular, no inverse exists` |
| 2 | Inversa $3\times3$ por método de la adjunta (cofactores + transposición + división entre el determinante) | `[[1,2,3],[0,1,4],[5,6,0]]` → inversa idéntica a `np.linalg.inv` hasta el último decimal |
| 3 | Red de dos capas (entrada 3 → oculta 4 → salida 2) solo con clase `Matrix` (sin NumPy) | shapes correctas en cada paso: $(3,1)\to(4,1)\to(4,1)\to(2,1)\to(2,1)$; `hidden = [0, 0, 0, 0.745]` |

**Insights que me llevo:**
- Una matriz singular ($\det = 0$) colapsa el espacio en una dimensión menor — dos puntos distintos terminan en el mismo lugar, así que ninguna transformación puede "reconstruir" de dónde vinieron. Por eso el determinante cero implica "no invertible": es la misma idea del rango deficiente de L01, vista ahora desde el escalado de área/volumen.
- El método de la adjunta ($A^{-1} = \frac{1}{\det(A)}\text{adj}(A)$) muestra que la inversa no es una caja negra — se construye explícitamente a partir de cofactores y cofactores son determinantes de menores. Esa es la base para entender por qué factorizaciones como LU o QR existen: evitan calcular inversas explícitas porque son numéricamente más estables.
- Construir la red de dos capas a mano dejó ver la *sparsity* de ReLU en vivo: de 4 neuronas ocultas, 3 salieron en `0` (preactivación negativa apagada) y solo 1 pasó información. En cada forward pass solo un subconjunto de neuronas está realmente "activo" — con pesos sin entrenar es ruido, pero en una red entrenada esa dispersión refleja qué *features* detectó cada neurona.

**Quiz: pre 3/3 · post 3/3** ✅ (dominó los tres conceptos —reglas de shape, element-wise vs. matmul, broadcasting/determinante— desde el pre-quiz)

---

### L03 — Matrix Transformations ✅

**Concepto central:** Una matriz no es solo una cuadrícula de números — es una máquina espacial. Rotación ($|\det|=1$, preserva distancias), escalado ($\det = s_x \cdot s_y$, estira ejes), cizallamiento ($\det=1$, inclina) y reflexión ($\det=-1$, invierte orientación) son los cuatro tipos fundamentales. Al componer $S @ R \neq R @ S$ — el orden importa porque cada transformación opera sobre el espacio que dejó la anterior. Los autovectores son las direcciones que sobreviven a la transformación (solo se escalan); los autovalores dicen cuánto. La ecuación característica $\det(A - \lambda I) = 0$ los produce.

**Funciones de transformación desde cero:**

```python
def rotation_2d(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]

def eigenvalues_2x2(matrix):
    a, b = matrix[0]; c, d = matrix[1]
    trace = a + d; det = a*d - b*c
    discriminant = trace**2 - 4*det
    sqrt_disc = discriminant**0.5
    return ((trace + sqrt_disc)/2, (trace - sqrt_disc)/2)
```

**Ejercicios y resultados reales:**

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | Rotación 45°, escalado $(2, 0.5)$ y cizallamiento $k_x=1$ sobre cuadrado unitario + verificar distancias | distancias A-B y B-C: $1.0 \to 1.0$ tras rotar — isometría confirmada |
| 2 | Autovalores de $\begin{pmatrix}4&2\\1&3\end{pmatrix}$ a mano + función propia + NumPy | $\lambda_1=5$, $\lambda_2=2$; autovectores: $(0.894, 0.447)$ y $(\pm0.707, \mp0.707)$ — signo indistinto |
| 3 | Composición $(R_{30°} \to S_{1.5,0.8} \to Sh_{0.3})$ sobre 8 puntos en círculo + verificar $\det$ | $\det(\text{compuesta})=1.2 = 1.0\times1.2\times1.0$ ✓; círculo $\to$ elipse inclinada |

**Insights que me llevo:**
- El signo de un autovector es arbitrario: $v$ y $-v$ son igualmente válidos (los autovectores se definen salvo múltiplo escalar). NumPy y la función propia pueden dar signos opuestos y ambos son correctos.
- $\det(ABC) = \det(A)\cdot\det(B)\cdot\det(C)$: al componer transformaciones, solo el escalado cambia el área — rotación y cizallamiento la dejan intacta. Esta propiedad conecta la geometría de las transformaciones con el álgebra de los determinantes.
- Aplicar la composición a un círculo da una elipse inclinada: el escalado aplastó y estiró, la rotación giró, el cizallamiento inclinó. La simetría central del círculo ($-p$ opuesto a $p$) sobrevive porque las transformaciones lineales preservan el origen.

**Quiz: pre 3/3 · post 3/3** ✅

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
