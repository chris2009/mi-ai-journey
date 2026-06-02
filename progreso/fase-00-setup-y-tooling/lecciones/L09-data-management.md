# L09 — Gestión de Datos

> Los datos son el combustible. Cómo los gestionas determina qué tan rápido vas.

**Tipo:** Build  
**Lenguajes:** Python  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~45 minutos

---

## Objetivos de aprendizaje

- Cargar, transmitir en streaming y cachear datasets usando la librería `datasets` de Hugging Face
- Convertir entre CSV, JSON, Parquet y Arrow y explicar sus tradeoffs
- Crear splits de train/validación/test reproducibles con seeds fijos
- Gestionar archivos grandes de modelos y datasets con `.gitignore`, Git LFS o DVC

---

## El problema

Todo proyecto de AI empieza con datos. Necesitas encontrar datasets, descargarlos, convertir entre formatos, dividirlos para entrenamiento y evaluación, y versionarlos para que los experimentos sean reproducibles. Hacerlo manualmente cada vez es lento y propenso a errores. Necesitas un flujo de trabajo repetible.

---

## El concepto

```
Hugging Face Hub
       ↓
datasets library  →  cargar / streaming
       ↓
Caché local (~/.cache/huggingface/) ← se descarga una vez, carga desde caché
       ↓
Conversión de formato (CSV, JSON, Parquet, Arrow)
       ↓
Splits: train / val / test
       ↓
Tu pipeline de entrenamiento
```

La librería `datasets` de Hugging Face es la forma estándar de cargar datos para trabajo de AI. Maneja descarga, caché, conversión de formatos y streaming.

---

## Paso a paso

### Paso 1: Instalar las librerías

```bash
uv pip install datasets huggingface_hub
```

### Paso 2: Cargar un dataset

```python
from datasets import load_dataset

# Nota: datasets 4.x + huggingface_hub 1.x requieren "namespace/nombre"
dataset = load_dataset("nyu-mll/glue", "mrpc")
print(dataset)
print(dataset["train"][0])
```

Después de la primera descarga, carga desde caché en `~/.cache/huggingface/datasets/`. Segunda llamada = 0 requests HTTP.

### Paso 3: Streaming para datasets grandes

Algunos datasets son demasiado grandes para caber en disco. El streaming carga fila por fila sin descargar todo.

```python
dataset = load_dataset("nyu-mll/glue", "mrpc", split="train", streaming=True)

for i, ejemplo in enumerate(dataset):
    print(ejemplo["sentence1"][:80])
    if i >= 4:
        break
```

El streaming da un `IterableDataset`. Procesas filas a medida que llegan. El uso de memoria se mantiene constante sin importar el tamaño del dataset.

### Paso 4: Formatos de datos

La librería usa Apache Arrow internamente. Puedes convertir a otros formatos:

```python
dataset = load_dataset("nyu-mll/glue", "mrpc", split="train")

dataset.to_csv("glue_mrpc_train.csv")
dataset.to_json("glue_mrpc_train.json")
dataset.to_parquet("glue_mrpc_train.parquet")
```

**Comparación de formatos:**

| Formato | Tamaño | Velocidad de lectura | Mejor para |
|---------|--------|---------------------|------------|
| CSV | Grande | Lento | Legibilidad humana, hojas de cálculo |
| JSON | Grande | Lento | APIs, datos anidados |
| **Parquet** | **Pequeño** | **Rápido** | **Analítica, consultas por columnas, almacenamiento ML** |
| Arrow | Pequeño | El más rápido | Procesamiento en memoria (lo que usa `datasets` internamente) |

**Resultado real (500 filas GLUE/MRPC):**
```
CSV:     123,970 bytes
JSON:    144,585 bytes
Parquet:  88,412 bytes  → 1.4x más pequeño que CSV
```

### Paso 5: Splits de datos

Cada proyecto ML necesita tres splits:

- **Train**: el modelo aprende de aquí (típicamente 80%)
- **Validación**: verificas el progreso durante el entrenamiento (típicamente 10%)
- **Test**: evaluación final después del entrenamiento — tocarlo solo una vez

```python
dataset = load_dataset("nyu-mll/glue", "mrpc", split="train")

# Split 80/10/10
split1 = dataset.train_test_split(test_size=0.20, seed=42)
split2 = split1["test"].train_test_split(test_size=0.50, seed=42)

train_ds = split1["train"]
val_ds   = split2["train"]
test_ds  = split2["test"]

print(f"Train: {len(train_ds)}, Val: {len(val_ds)}, Test: {len(test_ds)}")
# El mismo seed produce el mismo split cada vez → reproducibilidad garantizada
```

### Paso 6: Descargar y cachear modelos

```python
from huggingface_hub import hf_hub_download, snapshot_download

# Descargar un archivo específico
model_path = hf_hub_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    filename="config.json"
)
print(f"Cacheado en: {model_path}")

# Descargar el modelo completo
model_dir = snapshot_download("sentence-transformers/all-MiniLM-L6-v2")
print(f"Modelo completo en: {model_dir}")
```

Los modelos se cachean en `~/.cache/huggingface/hub/`. Una vez descargados, cargan instantáneamente en las siguientes ejecuciones.

### Paso 7: Manejar archivos grandes

Los pesos de modelos y datasets grandes no van en git.

**Opción A: .gitignore (la más simple)**

```gitignore
*.bin
*.safetensors
*.pt
*.onnx
data/*.parquet
data/*.csv
models/
```

**Opción B: Git LFS (rastrear archivos grandes en git)**

```bash
git lfs install
git lfs track "*.bin"
git lfs track "*.safetensors"
git add .gitattributes
```

Git LFS almacena punteros en tu repo y los archivos reales en un servidor separado. GitHub da 1 GB gratis.

**Opción C: DVC (control de versiones de datos)**

```bash
pip install dvc
dvc init
dvc add data/training_set.parquet
git add data/training_set.parquet.dvc data/.gitignore
git commit -m "Rastrear datos de entrenamiento con DVC"
```

DVC crea archivos `.dvc` pequeños que apuntan a tus datos. Los datos viven en S3, GCS u otro backend.

| Método | Complejidad | Mejor para |
|--------|-------------|------------|
| .gitignore | Baja | Proyectos personales, datos re-descargables |
| Git LFS | Media | Equipos compartiendo pesos de modelos via git |
| DVC | Alta | Experimentos reproducibles, datasets grandes, equipos |

Para este curso, `.gitignore` es suficiente.

---

## Datasets usados en el curso

| Dataset | Lecciones | Tamaño | Qué enseña |
|---------|-----------|--------|------------|
| IMDB / GLUE / MRPC | Tokenización, clasificación | ~84 MB | Clasificación de texto |
| WikiText | Modelado de lenguaje | 181 MB | Predicción de siguiente token |
| SQuAD | Sistemas de QA | 35 MB | Question answering |
| MNIST | Visión básica | 21 MB | Clasificación de imágenes |

No necesitas descargarlos todos ahora. Cada lección especifica lo que necesita.

---

## Ejercicios

1. Carga el dataset `nyu-mll/glue` con la config `mrpc` e inspecciona los primeros 5 ejemplos del split de train
2. Carga el mismo dataset en modo streaming y cuenta cuántos ejemplos puedes procesar en 10 segundos
3. Convierte el dataset a Parquet y CSV, y compara los tamaños de archivo
4. Crea un split 70/15/15 con seed fijo y verifica los tamaños

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| Dataset split | "Datos de entrenamiento" | Un subconjunto nombrado (train/val/test) usado en diferentes etapas del ciclo de vida ML |
| Streaming | "Carga lazy" | Procesar datos fila a fila desde una fuente remota sin descargar el dataset completo |
| Parquet | "CSV comprimido" | Formato de archivo columnar optimizado para consultas analíticas y eficiencia de almacenamiento |
| Arrow | "DataFrame rápido" | Formato columnar en memoria usado internamente por la librería datasets para lecturas zero-copy |
| Git LFS | "Git para archivos grandes" | Extensión que almacena archivos grandes fuera del repo git mientras mantiene punteros en el control de versiones |
| DVC | "Git para datos" | Sistema de control de versiones para datasets y modelos que se integra con almacenamiento en la nube |
| Caché | "Ya descargado" | Copia local de datos obtenidos previamente, almacenada en `~/.cache/huggingface/` por defecto |
