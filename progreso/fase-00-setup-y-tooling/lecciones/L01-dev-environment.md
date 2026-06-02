# L01 — Entorno de Desarrollo

> Tus herramientas moldean tu pensamiento. Configúralas una vez, configúralas bien.

**Tipo:** Build  
**Lenguajes:** Python, Node.js, Rust  
**Prerequisitos:** Ninguno  
**Tiempo:** ~45 minutos

---

## Objetivos de aprendizaje

- Instalar Python 3.11+, Node.js 20+ y Rust desde cero
- Configurar entornos virtuales y gestores de paquetes para builds reproducibles
- Verificar acceso a GPU con CUDA y correr una operación de tensor de prueba
- Entender el stack de 4 capas: sistema, paquetes, runtimes, librerías AI

---

## El problema

Estás a punto de aprender AI engineering en 200+ lecciones usando Python, TypeScript y Rust. Si tu entorno está roto, cada lección se convierte en una batalla contra las herramientas en vez de aprender.

La mayoría de personas saltea la configuración del entorno. Luego pasan horas depurando errores de imports, conflictos de versiones y drivers de CUDA faltantes. Vamos a hacer esto una vez, correctamente.

---

## El concepto

Un entorno de AI engineering tiene 4 capas:

```
Capa 4 → Librerías AI/ML     (PyTorch, JAX, transformers, etc.)
Capa 3 → Language runtimes   (Python 3.11+, Node 20+, Rust)
Capa 2 → Package managers    (uv, pnpm, cargo)
Capa 1 → Base del sistema    (OS, shell, git, editor, GPU drivers)
```

Se instala de abajo hacia arriba. Cada capa depende de la anterior.

---

## Paso a paso

### Paso 1: Base del sistema

Verifica tu sistema e instala lo esencial.

```bash
# Ubuntu/Debian (WSL2)
sudo apt update && sudo apt install -y build-essential git curl wget
```

### Paso 2: Python con uv

`uv` es 10-100x más rápido que pip y maneja entornos virtuales automáticamente.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

uv python install 3.12

uv venv
source .venv/bin/activate

uv pip install numpy matplotlib jupyter
```

Verificar:

```python
import sys
print(f"Python {sys.version}")

import numpy as np
print(f"NumPy {np.__version__}")
a = np.array([1, 2, 3])
print(f"Vector: {a}, producto punto consigo mismo: {np.dot(a, a)}")
```

### Paso 3: Node.js con pnpm

Para lecciones de TypeScript (agentes, servidores MCP, apps web).

```bash
curl -fsSL https://fnm.vercel.app/install | bash
fnm install 22
fnm use 22

npm install -g pnpm
node -e "console.log('Node', process.version)"
```

### Paso 4: Rust

Para lecciones de alto rendimiento (inferencia, sistemas).

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# Nota: NO usar snap ni apt para instalar Rust — solo rustup

rustc --version
cargo --version
```

### Paso 5: Configuración de GPU (si tienes una)

```bash
nvidia-smi  # verifica que el driver esté instalado

# Instalar PyTorch con CUDA
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

```python
import torch
print(f"CUDA disponible: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    mem = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"VRAM: {mem:.1f} GB")
```

### Paso 6: Verificar todo

```bash
python phases/00-setup-and-tooling/01-dev-environment/code/verify.py
```

---

## Uso en el curso

| Lenguaje | Usado en | Gestor de paquetes |
|----------|----------|-------------------|
| Python | Fases 1-12 (ML, DL, NLP, Vision, Audio, LLMs) | uv |
| TypeScript | Fases 13-17 (Herramientas, Agentes, Enjambres, Infra) | pnpm |
| Rust | Fases 12, 15-17 (Sistemas de alto rendimiento) | cargo |

---

## Ejercicios

1. Corre el script de verificación y corrige cualquier falla
2. Crea un entorno virtual Python para este curso e instala PyTorch
3. Escribe un "hello world" en Python, Node.js y Rust, y corre cada uno

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| uv | "El package manager rápido" | Gestor de paquetes Python 10-100x más rápido que pip, maneja también venvs |
| Virtual environment | "Un venv" | Directorio aislado con su propio intérprete Python y paquetes |
| rustup | "El instalador de Rust" | Instalador oficial de Rust. Nunca usar snap/apt para Rust |
| CUDA | "Programación GPU" | Plataforma de cómputo paralelo de NVIDIA para correr código en la GPU |
| VRAM | "Memoria GPU" | RAM de video en la GPU, separada de la RAM del sistema. Limita el tamaño del modelo |
