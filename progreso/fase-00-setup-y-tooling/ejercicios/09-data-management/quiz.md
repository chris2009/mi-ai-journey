# Quiz — L09 Data Management

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 2/2

### P1
**Pregunta:** ¿Qué formato de archivo es el estándar para almacenamiento de datasets en ML?
**Respuesta elegida:** Parquet — más compacto que CSV/JSON y significativamente más rápido de leer ✅
**Correcto:** Sí — benchmark real: CSV 123,970 bytes vs Parquet 88,412 bytes (1.4x más pequeño) para las mismas 500 filas.

### P2
**Pregunta:** ¿Por qué usar `seed=42` (o cualquier seed fija) al hacer train/val/test splits?
**Respuesta elegida:** Para reproducibilidad — el mismo seed garantiza los mismos índices en cada ejecución, evitando data leakage accidental entre splits ✅
**Correcto:** Sí

---

## Post-quiz — 3/3

### P1
**Pregunta:** Tienes un dataset de 200 GB. ¿Cómo lo procesas sin quedarte sin RAM?
**Respuesta elegida:** Con `streaming=True` en `load_dataset` — procesa fila a fila, la RAM se mantiene constante sin importar el tamaño del dataset ✅
**Correcto:** Sí

### P2
**Pregunta:** ¿Cuándo usar DVC en lugar de solo `.gitignore` para datos grandes?
**Respuesta elegida:** Cuando necesitas reproducir experimentos exactos en distintas máquinas — DVC versiona los datos junto al código para garantizar que el mismo commit produzca los mismos resultados ✅
**Correcto:** Sí — `.gitignore` solo excluye; DVC rastrea y sincroniza.

### P3
**Pregunta:** El dataset "glue" ya no carga con ese nombre en datasets 4.x. ¿Por qué y cómo se llama ahora?
**Respuesta elegida:** Los namespaces se actualizaron a formato `organización/dataset` — ahora es `"nyu-mll/glue"` ✅
**Correcto:** Sí — misma convención que HuggingFace Hub.

---

**Resultado final: pre 2/2 · post 3/3** ✅
