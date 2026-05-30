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

## Dudas y pendientes

