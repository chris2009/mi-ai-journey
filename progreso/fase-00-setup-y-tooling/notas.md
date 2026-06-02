# Fase 00 — Setup & Tooling

## Lección 01 — Dev Environment ✅

### Resumen
Stack de 4 capas para AI Engineering:
1. Sistema base (OS, shell, git, GPU drivers)
2. Package managers (uv, pnpm, cargo)
3. Language runtimes (Python, Node.js, Rust)
4. AI/ML libraries (PyTorch, NumPy, etc.)

Se instala de abajo hacia arriba — cada capa depende de la anterior.

### Setup completado
| Herramienta | Versión | Estado |
|-------------|---------|--------|
| Python | 3.13.0 | ✅ |
| Node.js | 20.19.5 | ✅ |
| Rust | 1.96.0 | ✅ |
| uv | 0.11.17 | ✅ |
| pnpm | 11.5.0 | ✅ |
| PyTorch | 2.6.0+cu124 | ✅ |
| CUDA | 12.5 | ✅ |
| GPU | RTX 4070 Laptop (8GB VRAM) | ✅ |

### Virtual environment
- Ubicación: `/mnt/d/APRENDIZAJE/AI_ENGINEERING/.venv`
- Activar: `source .venv/bin/activate`

### Verificación oficial
```
Result: 7/7 core checks passed, 2/2 GPU checks passed
```

### Conceptos clave
- **uv**: package manager de Python, 10-100x más rápido que pip
- **pnpm**: package manager de Node.js (alternativa eficiente a npm)
- **rustup**: instalador oficial de Rust (no usar snap/apt)
- **Virtual environment**: aísla dependencias del curso del sistema global

## Lección 02 — Git & Collaboration ✅

### Flujo diario
```
Working Directory → Staging Area → Local Repo → GitHub
    (editas)         git add        git commit    git push
```

### Branching para experimentos
```bash
git checkout -b experiment/mi-idea   # crea y cambia de rama
git checkout master                  # vuelve a main
git merge experiment/mi-idea         # integra cambios
```

### .gitignore para AI Engineering
Excluir checkpoints de modelos (pesan cientos de MB a GB):
```
*.pt, *.pth, *.safetensors, *.ckpt, *.bin
```

### Conceptos clave
- **add → commit → push**: orden correcto del flujo diario
- **`-b` en checkout**: crea y cambia al branch en un solo paso
- **Model checkpoints**: binarios grandes, nunca en git (usar HuggingFace Hub o DVC)

### Quiz: 3/3 ✅

## Lección 03 — GPU Setup & Cloud ✅

### Benchmark CPU vs GPU (RTX 4070 Laptop)
| Modo | Tiempo (matriz 5000x5000) |
|------|--------------------------|
| CPU | 0.463s |
| GPU (con warm-up) | 0.032s |
| **Speedup real** | **15x** |

> Sin warm-up el resultado fue 2x — el overhead de inicialización CUDA distorsiona la primera medición.

### Estimación de VRAM
```
Regla fp16: parámetros = VRAM_bytes / 2
8.6 GB → ~4.3B parámetros en fp16
8.6 GB → ~8-9B parámetros en int4 (cuantizado)
```
Modelos que caben localmente: Llama 3.2 3B, Phi-3.5 Mini (3.8B)

### Conceptos clave
- **CUDA warm-up**: primera operación GPU incluye JIT + init, no medir sin warm-up
- **VRAM**: memoria del GPU, independiente de la RAM del sistema; limita tamaño del modelo
- **fp16**: 2 bytes/parámetro (mitad de fp32), pérdida mínima de precisión
- **int4**: cuantización a 4 bits, ~0.5 bytes/parámetro, cabe el doble de modelo

## Lección 04 — APIs & Keys ✅

### Patrón universal de API
```
Tu código → HTTP POST [URL + API key + JSON body] → Servidor
          ← JSON response ←
```

### Campos clave en la respuesta JSON
| Campo | Descripción |
|-------|-------------|
| `content[0].text` | Texto de respuesta del modelo |
| `usage.input_tokens` | Tokens enviados (se cobran) |
| `usage.output_tokens` | Tokens recibidos (se cobran) |
| `stop_reason: "end_turn"` | El modelo terminó normalmente |

### Seguridad de API keys
- Nunca en el código — siempre en `.env`
- `.env` en `.gitignore` (ya configurado)
- Cargar con `python-dotenv`: `load_dotenv()` antes de `os.environ[...]`

### Conceptos clave
- **SDK vs HTTP crudo**: el SDK simplifica headers, serialización y errores — pero es solo HTTP por debajo
- **Rate limit**: límite de requests por minuto/hora — manejar con retry + backoff
- **input/output tokens**: unidad de facturación, no palabras

### Output generado
- `outputs/prompts/api-troubleshooter.md`

## Lección 05 — Jupyter Notebooks ✅

### Benchmark list comprehension vs NumPy (100k elementos)
| Método | List | NumPy | Speedup |
|--------|------|-------|---------|
| `%timeit` (promedio) | 5.25 ms | 42.3 μs | **~124x** |
| Manual (1 run) | 4.75 ms | 1.01 ms | 5x |

> La medición manual mintió igual que el GPU sin warm-up en L03. `%timeit` corre miles de veces y promedia — ese es el número real.

### Magic commands clave
| Comando | Uso |
|---------|-----|
| `%timeit` | Microbenchmark — corre muchas veces y promedia |
| `%%time` | Wall time de una celda — corre una sola vez |
| `%matplotlib inline` | Plots inline en el notebook |
| `!comando` | Ejecutar shell desde el notebook |

### Trampas comunes
| Trampa | Fix |
|--------|-----|
| Ejecución fuera de orden | `Kernel > Restart & Run All` antes de compartir |
| Estado oculto (celda borrada, variable viva) | Reiniciar kernel regularmente |
| Memory leak | `del var` + `gc.collect()` |

### Cuándo notebook vs script
- **Notebook**: explorar datos, prototipar, visualizar, explicar
- **Script**: pipelines, utilidades reutilizables, producción, código con schedule

### Setup de kernel en VS Code + WSL
```bash
# Registrar el venv como kernel de Jupyter
python -m ipykernel install --user --name=ai-engineering --display-name "Python (AI Engineering)"

# Instalar extensiones en WSL (no en Windows)
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.python
```

### Quiz: pre 1/2 · post 3/3 ✅

## Lección 06 — Python Environments ✅

### El problema: dependency hell
Sin venvs, instalar `torch 2.4` para un proyecto rompe el que necesitaba `torch 2.1`.
Con venvs: cada proyecto tiene su propio intérprete y paquetes aislados.

### Herramientas
| Tool | Cuándo usarla |
|------|--------------|
| `uv venv` | La mayoría de proyectos — 10-100x más rápido que pip |
| `venv` (built-in) | Si no tienes `uv` |
| `conda` | Necesitas controlar CUDA toolkit o estás en cluster |

### Regla crítica: uv no instala pip
```bash
# En un venv creado con uv, siempre usar:
uv pip list
uv pip install paquete
uv pip show paquete
# NO usar: python -m pip  (pip no está instalado en el venv)
```

### Aislamiento demostrado
```bash
# test-env:  numpy==1.26.4  (instalado manualmente)
# .venv:     numpy==2.4.4   (ya existía)
# → coexisten sin conflicto
```

### pyproject.toml con grupos opcionales
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

### CUDA compatibility check
```bash
nvidia-smi | grep "CUDA Version"   # → 12.5 (driver)
python -c "import torch; print(torch.version.cuda)"  # → 12.4 (PyTorch)
# Regla: PyTorch CUDA <= driver CUDA  ✅
# Si fuera al revés → "CUDA not available" aunque GPU esté presente
```

### Quiz: pre 2/2 · post 3/3 ✅

## Lección 07 — Docker for AI ✅

### Vocabulario clave
| Término | Qué es |
|---------|--------|
| Image | Plantilla read-only. Construida desde un Dockerfile. |
| Container | Instancia corriendo de una image. |
| Volume | Directorio del host mapeado al container. Persiste entre reinicios. |
| docker-compose | Orquesta múltiples servicios con un comando. |

### Regla de orden en Dockerfile
Lo que cambia menos → más arriba (se cachea). Lo que cambia más → abajo.
```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04  # nunca cambia
RUN apt-get install python3 ...              # cambia poco
RUN pip install torch ...                    # cambia poco
COPY ./mi_codigo .                           # cambia mucho → AL FINAL
```

### Volumes — por qué son críticos en AI
```bash
-v ~/models:/models   # modelo 14GB descargado una vez, vive en el host
-v $(pwd):/workspace  # código persistente entre rebuilds
```

### NVIDIA Container Toolkit
- El **driver CUDA** vive en el **host**
- El **toolkit CUDA** (librerías) vive **dentro del container**
- `--gpus all` activa el puente entre ambos

### Resultado verificado
```
ai-dev-l07: PyTorch 2.6.0+cu124, CUDA: True  (7.92 GB)
RTX 4070 Laptop accesible desde dentro del container ✅
```

### Errores encontrados y fixes
1. `python3.12` no existe en Ubuntu 22.04 repos → usar `python3` (3.10)
2. `torch==2.3.1` no existe para cu124 → versión mínima es `2.4.0` (usamos `2.6.0`)

### Docker Compose — un comando para todo el stack
```bash
docker compose up -d     # levanta ai-dev + qdrant
docker compose down      # para todo
docker compose down -v   # para todo + elimina volumes
```
Servicios se comunican por nombre: `http://qdrant:6333` desde ai-dev.

### Quiz: pre 2/2 · post 2/3 ✅

## Lección 08 — Editor Setup ✅

### Las 5 capas del setup para AI Engineering
```
5. Remote Development  → SSH a GPU boxes / cloud VMs
4. Terminal Integration → scripts, nvidia-smi, debug
3. AI-Specific Settings → format-on-save, type checking, rulers
2. Extensions          → Python, Jupyter, Pylance, GitLens, Black, Ruff
1. Base Editor         → VS Code
```

### Extensiones instaladas
| Extensión | Para qué sirve |
|-----------|----------------|
| Python | Soporte de lenguaje, detección de venv, run/debug |
| Pylance | Type checking rápido, autocompletado, resolución de imports |
| Jupyter | Correr notebooks en VS Code, variable explorer |
| GitLens | Blame inline — quién cambió qué y cuándo |
| Remote SSH | Abrir carpeta de GPU remota como si fuera local |
| Debugpy | Debugging paso a paso para Python |
| Black Formatter | Formato automático al guardar |
| Ruff | Linting rápido, detecta errores comunes |

> Remote SSH no se instala en WSL — va en el lado Windows (es la extensión que inicia la conexión desde tu máquina local).

### Settings clave en `.vscode/settings.json`
| Setting | Por qué importa |
|---------|----------------|
| `typeCheckingMode: "basic"` | Detecta shape mismatches de tensores antes de correr |
| `formatOnSave: true` | Black formatea al guardar — nunca formatear a mano |
| `rulers: [88, 120]` | Black corta en 88, referencia visual para comentarios en 120 |
| `notebook.output.scrolling: true` | Sin esto, 10k líneas de training loop explotan el panel |
| `files.autoSave: afterDelay` | Guarda 1s después de escribir — nunca código stale |

### SSH config para GPU remota
```
Host gpu-box
    HostName 203.0.113.50
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```
Luego: `Remote-SSH: Connect to Host > gpu-box` conecta instantáneamente.

### Alternativas al editor
| Editor | Cuándo usarlo |
|--------|--------------|
| Cursor | VS Code fork con AI integrada — mismo ecosystem, mismas extensiones |
| Windsurf | Igual que Cursor, otra opción AI-first |
| Neovim | Solo si ya eres experto — no aprender en paralelo con AI Engineering |

### Quiz: pre 2/2 · post 3/3 ✅

## Lección 09 — Data Management ✅

### El flujo de datos en AI Engineering
```
Hugging Face Hub → datasets library → caché local (~/.cache/huggingface/)
       ↓
Conversión de formato (CSV / JSON / Parquet / Arrow)
       ↓
Splits: train / val / test → pipeline de entrenamiento
```

### Formatos — cuándo usar cada uno
| Formato | Tamaño | Velocidad | Cuándo usarlo |
|---------|--------|-----------|---------------|
| CSV | Grande | Lento | Intercambio, hojas de cálculo |
| JSON | Grande | Lento | APIs, datos anidados |
| **Parquet** | **Pequeño** | **Rápido** | **Almacenamiento ML — el estándar** |
| Arrow | Pequeño | Más rápido | Memoria interna — lo que usa `datasets` |

### Benchmark real (500 filas GLUE/MRPC)
```
CSV:     123,970 bytes
JSON:    144,585 bytes
Parquet:  88,412 bytes   → 1.4x más pequeño que CSV
```

### Splits 70/15/15 con seed fijo
```python
split1 = ds.train_test_split(test_size=0.30, seed=42)
split2 = split1["test"].train_test_split(test_size=0.50, seed=42)
# seed=42 → mismos índices en cada ejecución → reproducibilidad garantizada
```

### Streaming — memoria constante sin importar el tamaño
```python
ds = load_dataset("nyu-mll/glue", "mrpc", split="train", streaming=True)
# Procesa fila a fila. RAM no crece aunque el dataset tenga 200 GB.
```

### Manejo de archivos grandes
| Método | Complejidad | Cuándo usarlo |
|--------|-------------|---------------|
| `.gitignore` | Baja | Proyectos personales, datos re-descargables |
| Git LFS | Media | Equipos compartiendo pesos de modelos vía git |
| DVC | Alta | Reproducir experimentos exactos en distintas máquinas |

### Datasets — namespaces actualizados (datasets 4.x + huggingface_hub 1.x)
```python
"nyu-mll/glue"                               # antes: "glue"
"stanfordnlp/imdb"                           # antes: "imdb"
"cornell-movie-review-data/rotten_tomatoes"  # antes: "rotten_tomatoes"
```

### Caché automático
```
~/.cache/huggingface/datasets/   ← datasets
~/.cache/huggingface/hub/        ← modelos
```
Segunda llamada → carga desde caché, 0 HTTP requests.

### Quiz: pre 2/2 · post 3/3 ✅

## Lección 09 — Data Management ✅

### El flujo de datos en AI Engineering
```
Hugging Face Hub → datasets library → caché local (~/.cache/huggingface/)
       ↓
Conversión de formato (CSV / JSON / Parquet / Arrow)
       ↓
Splits: train / val / test → pipeline de entrenamiento
```

### Formatos — cuándo usar cada uno
| Formato | Tamaño | Velocidad | Cuándo usarlo |
|---------|--------|-----------|---------------|
| CSV | Grande | Lento | Intercambio, hojas de cálculo |
| JSON | Grande | Lento | APIs, datos anidados |
| **Parquet** | **Pequeño** | **Rápido** | **Almacenamiento ML — el estándar** |
| Arrow | Pequeño | Más rápido | Memoria interna — lo que usa `datasets` |

### Benchmark real (500 filas GLUE/MRPC)
```
CSV:     123,970 bytes
JSON:    144,585 bytes
Parquet:  88,412 bytes   → 1.4x más pequeño que CSV
```

### Splits 70/15/15 con seed fijo
```python
split1 = ds.train_test_split(test_size=0.30, seed=42)
split2 = split1["test"].train_test_split(test_size=0.50, seed=42)
# seed=42 → mismos índices en cada ejecución → reproducibilidad garantizada
```

### Streaming — memoria constante sin importar el tamaño
```python
ds = load_dataset("nyu-mll/glue", "mrpc", split="train", streaming=True)
# Procesa fila a fila. RAM no crece aunque el dataset tenga 200 GB.
```

### Manejo de archivos grandes
| Método | Complejidad | Cuándo usarlo |
|--------|-------------|---------------|
| `.gitignore` | Baja | Proyectos personales, datos re-descargables |
| Git LFS | Media | Equipos compartiendo pesos de modelos vía git |
| DVC | Alta | Reproducir experimentos exactos en distintas máquinas |

### Datasets — namespaces actualizados (datasets 4.x + huggingface_hub 1.x)
```python
"nyu-mll/glue"                               # antes: "glue"
"stanfordnlp/imdb"                           # antes: "imdb"
"cornell-movie-review-data/rotten_tomatoes"  # antes: "rotten_tomatoes"
```

### Caché automático
```
~/.cache/huggingface/datasets/   ← datasets
~/.cache/huggingface/hub/        ← modelos
```
Segunda llamada → carga desde caché, 0 HTTP requests.

### Quiz: pre 2/2 · post 3/3 ✅
