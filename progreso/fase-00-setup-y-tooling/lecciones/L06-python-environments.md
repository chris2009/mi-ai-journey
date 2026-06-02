# L06 — Entornos Python

> El infierno de dependencias es real. Los entornos virtuales son la cura.

**Tipo:** Build  
**Lenguajes:** Shell  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~30 minutos

---

## Objetivos de aprendizaje

- Crear entornos virtuales aislados usando `uv`, `venv` o `conda`
- Escribir un `pyproject.toml` con grupos de dependencias opcionales y generar lockfiles para reproducibilidad
- Diagnosticar y corregir errores comunes: instalaciones globales, mezcla pip/conda, incompatibilidades de versión CUDA
- Implementar una estrategia de entorno por fase para proyectos con dependencias conflictivas

---

## El problema

Instalas PyTorch 2.4 para un proyecto de fine-tuning. La semana siguiente, otro proyecto necesita PyTorch 2.1. Actualizas globalmente y el primer proyecto se rompe. Bajas la versión y el segundo se rompe.

Esto es **dependency hell**. Ocurre constantemente en trabajo de AI/ML porque:
- PyTorch, JAX y TensorFlow vienen con sus propios bindings de CUDA
- Las librerías de modelos fijan versiones específicas del framework
- `pip install` global sobreescribe lo que había antes
- Las builds de CUDA 11.8 no funcionan con drivers CUDA 12.x (y viceversa)

**La solución:** cada proyecto tiene su propio entorno aislado con sus propios paquetes.

---

## El concepto

```
Sin entornos virtuales:
Sistema Python → torch 2.4.0 (Proyecto A lo necesita)
             → torch 2.1.0 (Proyecto B lo necesita)
             → CONFLICTO: solo puede existir una versión

Con entornos virtuales:
Proyecto A (.venv/) → torch 2.4.0
                   → transformers 4.44
Proyecto B (.venv/) → torch 2.1.0
                   → diffusers 0.28
```

---

## Paso a paso

### Opción 1: uv venv (Recomendada)

`uv` es 10-100x más rápido que pip. Maneja entornos virtuales, versiones de Python y resolución de dependencias en una sola herramienta.

```bash
uv venv                        # crea .venv en el directorio actual
source .venv/bin/activate      # activa el entorno

uv pip install torch numpy     # instalar paquetes
uv pip list                    # listar paquetes instalados
```

> **Regla crítica:** en un venv creado con `uv`, usar SIEMPRE `uv pip`, nunca `python -m pip`. `uv` no instala pip dentro del venv.

```bash
# ✅ Correcto en venv de uv:
uv pip install paquete
uv pip list
uv pip show paquete

# ❌ Incorrecto — pip no está instalado en el venv de uv:
python -m pip list
pip install paquete
```

### Opción 2: venv (Built-in de Python)

Si no puedes instalar `uv`:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install torch numpy
```

Más lento que `uv`, pero funciona en cualquier lugar donde esté Python.

### Opción 3: conda (Cuando lo necesites)

Conda gestiona dependencias no-Python como toolkits CUDA, cuDNN y librerías C. Úsalo cuando:
- Necesitas una versión específica del toolkit CUDA sin instalarlo en el sistema
- Estás en un cluster compartido
- Las instrucciones de instalación dicen "usa conda"

```bash
conda create -n myproject python=3.12
conda activate myproject
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
```

**Regla:** si usas conda para un entorno, usa conda para todos los paquetes de ese entorno. Mezclar `pip install` en un entorno conda causa conflictos difíciles de depurar.

---

## pyproject.toml con grupos opcionales

Reemplaza `requirements.txt`, `setup.py` y `setup.cfg` en un solo archivo:

```toml
[project]
name = "mi-ai-journey"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "numpy>=1.26",
    "matplotlib>=3.8",
    "jupyter>=1.0",
    "ipykernel>=6.0",
]

[project.optional-dependencies]
torch = ["torch>=2.3", "torchvision>=0.18"]
llm   = ["anthropic>=0.39", "openai>=1.50", "python-dotenv>=1.0"]
ml    = ["scikit-learn>=1.4", "pandas>=2.0", "seaborn>=0.13"]
```

Instalar grupos:

```bash
uv pip install -e ".[torch]"      # base + PyTorch
uv pip install -e ".[llm]"        # base + LLM SDKs
uv pip install -e ".[torch,llm]"  # todo junto
```

---

## Errores comunes

### 1. Instalar globalmente

```bash
pip install torch           # MAL: instala al Python del sistema

source .venv/bin/activate
uv pip install torch        # BIEN: instala al entorno virtual
```

Verificar dónde están tus paquetes:

```bash
which python   # debe mostrar .venv/bin/python, NO /usr/bin/python
```

### 2. Olvidar activar el entorno

```bash
python train.py             # usa Python del sistema, faltan paquetes
source .venv/bin/activate
python train.py             # usa Python del proyecto ✅
```

Tu prompt debe mostrar `(.venv) $` cuando el entorno está activo.

### 3. Incompatibilidad de versiones CUDA

```bash
nvidia-smi | grep "CUDA Version"          # → versión del driver (ej: 12.5)
python -c "import torch; print(torch.version.cuda)"  # → versión de PyTorch (ej: 12.4)

# Regla: versión CUDA de PyTorch <= versión CUDA del driver ✅
# Si fuera al revés → "CUDA not available" aunque la GPU esté presente
```

### 4. Committear .venv en git

```bash
echo ".venv/" >> .gitignore
```

Los entornos virtuales pesan 200 MB - 2 GB. Son locales, no portables. Commitear `pyproject.toml` y el lockfile en su lugar.

---

## Demostración de aislamiento

```bash
# Crear segundo entorno de prueba
uv venv test-env --python 3.12
source test-env/bin/activate

# Instalar versión diferente de numpy
uv pip install numpy==1.26.4

# Verificar
python -c "import numpy; print(numpy.__version__)"  # → 1.26.4

# Desactivar y volver al entorno principal
deactivate
source .venv/bin/activate

python -c "import numpy; print(numpy.__version__)"  # → 2.x.x (versión diferente)
```

Las dos versiones coexisten sin conflicto.

---

## Ejercicios

1. Activa el entorno del curso y corre `uv pip list` — lista todos los paquetes instalados
2. Crea un segundo entorno virtual, instala una versión diferente de numpy, y confirma que los dos entornos están aislados
3. Escribe un `pyproject.toml` para un proyecto que necesite PyTorch y el SDK de Anthropic
4. Verifica la compatibilidad CUDA: compara `nvidia-smi` con `torch.version.cuda`

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| Virtual environment | "Un venv" | Directorio aislado con su propio intérprete Python y paquetes, separado del Python del sistema |
| Lockfile | "Dependencias fijadas" | Archivo listando cada paquete y su versión exacta, garantizando instalaciones idénticas |
| pyproject.toml | "El nuevo setup.py" | Archivo estándar de configuración de proyecto Python |
| Transitive dependency | "Dependencia de una dependencia" | El paquete B depende de C; si instalas A que depende de B, C es dependencia transitiva de A |
| CUDA mismatch | "Mi GPU no funciona" | PyTorch fue compilado para una versión de CUDA diferente a la que soporta tu driver |
