# Quiz — L06 Python Environments

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 2/2

### P1
**Pregunta:** ¿Por qué necesitas un virtual environment por proyecto en lugar de instalar todo globalmente?
**Respuesta elegida:** Para aislar dependencias — dos proyectos pueden necesitar versiones distintas del mismo paquete (ej. torch 2.1 vs 2.4) sin conflicto ✅
**Correcto:** Sí — sin venvs, instalar una versión rompe los proyectos que usaban la otra.

### P2
**Pregunta:** ¿Qué comando usas para instalar paquetes en un venv creado con `uv`?
**Respuesta elegida:** `uv pip install paquete` — uv no instala pip en el venv, así que `python -m pip` no funciona ✅
**Correcto:** Sí — regla crítica: en venvs de uv, siempre usar `uv pip`, nunca `python -m pip`.

---

## Post-quiz — 3/3

### P1
**Pregunta:** Tu PyTorch fue compilado con CUDA 12.4 pero el driver de tu GPU soporta CUDA 12.5. ¿Funciona?
**Respuesta elegida:** Sí — la regla es PyTorch CUDA ≤ driver CUDA. El driver es retrocompatible hacia versiones menores del toolkit ✅
**Correcto:** Sí — si fuera al revés (PyTorch CUDA > driver), GPU aparece como "not available".

### P2
**Pregunta:** ¿Qué ventaja tiene `uv` sobre `pip` para instalar dependencias?
**Respuesta elegida:** uv es 10-100x más rápido — está escrito en Rust y resuelve dependencias en paralelo ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Para qué sirven los grupos opcionales en `pyproject.toml` como `[project.optional-dependencies]`?
**Respuesta elegida:** Para instalar solo las dependencias que necesita cada caso de uso (ej. `.[torch]` para GPU, `.[llm]` para APIs) sin instalar todo siempre ✅
**Correcto:** Sí

---

**Resultado final: pre 2/2 · post 3/3** ✅
