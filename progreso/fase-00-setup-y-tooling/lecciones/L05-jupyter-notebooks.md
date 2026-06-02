# L05 — Jupyter Notebooks

> Los notebooks son el banco de laboratorio del AI engineering. Aquí se prototipar; lo que funciona se mueve a producción.

**Tipo:** Build  
**Lenguajes:** Python  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~30 minutos

---

## Objetivos de aprendizaje

- Instalar y lanzar JupyterLab o VS Code con la extensión Jupyter
- Usar magic commands (`%timeit`, `%%time`, `%matplotlib inline`) para benchmarks y visualización
- Distinguir cuándo usar notebooks vs scripts y aplicar el flujo "explorar en notebooks, producir en scripts"
- Identificar y evitar las trampas comunes: ejecución fuera de orden, estado oculto, memory leaks

---

## El problema

Todos los papers de AI, tutoriales y competencias de Kaggle usan Jupyter notebooks. Te permiten correr código por partes, ver outputs inline, mezclar código con explicaciones, e iterar rápido. Si intentas aprender AI sin notebooks, es como hacer tarea de matemáticas sin papel borrador.

Pero los notebooks tienen trampas reales. Saber cuándo usar uno y cuándo usar un script te ahorrará pesadillas de debugging.

---

## El concepto

Un notebook es una lista de celdas. Cada celda es código o texto.

```
┌─────────────────────────────────────┐
│ Celda Markdown                      │
│ # Mi Experimento                    │
│ Probando learning rate 0.01         │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│ Celda de código  ►                  │
│ model.fit(X, y, lr=0.01)           │
│ ─────────────────────────────────── │
│ Output: loss = 0.342               │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│ Celda de código  ►                  │
│ plt.plot(losses)                    │
│ ─────────────────────────────────── │
│ [gráfico inline]                    │
└─────────────────────────────────────┘
```

El **kernel** es un proceso Python corriendo en segundo plano. Cuando ejecutas una celda, envía el código al kernel, que lo ejecuta y devuelve el resultado. Todas las celdas comparten el mismo kernel, así que las variables persisten entre celdas.

Eso de "cualquier orden en que hagas clic" es tanto el superpoder como el pie de cañón.

---

## Paso a paso

### Paso 1: Elegir tu interfaz

| Interfaz | Instalar | Mejor para |
|----------|----------|------------|
| JupyterLab | `pip install jupyterlab` luego `jupyter lab` | Experiencia IDE completa, múltiples tabs |
| Jupyter Notebook | `pip install notebook` luego `jupyter notebook` | Simple, liviano |
| VS Code | Instalar extensión "Jupyter" | Ya en tu editor, integración con git |

Las tres leen y escriben el mismo archivo `.ipynb`. Usa lo que prefieras.

```bash
# Instalar JupyterLab
uv pip install jupyterlab
jupyter lab
```

### Paso 2: Atajos de teclado esenciales

Operas en dos modos. Presiona `Escape` para modo comando (barra azul), `Enter` para modo edición (barra verde).

**Modo comando (más usados):**

| Tecla | Acción |
|-------|--------|
| `Shift+Enter` | Correr celda, moverse a la siguiente |
| `A` | Insertar celda arriba |
| `B` | Insertar celda abajo |
| `DD` | Eliminar celda |
| `M` | Convertir a markdown |
| `Y` | Convertir a código |

**`Shift+Enter` es el que usarás miles de veces al día. Aprende ese primero.**

### Paso 3: Magic commands

No son Python. Son comandos específicos de Jupyter que empiezan con `%` (line magic) o `%%` (cell magic).

**Medir tiempo de tu código:**

```python
# %timeit corre muchas veces y promedia → el número real
%timeit np.random.randn(10000)
# Salida: 45.2 μs ± 1.3 μs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
```

```python
# %%time corre una sola vez → wall time
%%time
model.fit(X_train, y_train, epochs=10)
# Salida: Wall time: 2.34 s
```

**Diferencia crítica:**
- `%timeit` → para microbenchmarks (operaciones de arrays, funciones individuales)
- `%%time` → para entrenamiento, carga de datos (no quieres repetirlo miles de veces)

**Activar plots inline:**

```python
%matplotlib inline
# Ahora plt.show() renderiza directamente en el notebook
```

**Instalar paquetes sin salir del notebook:**

```python
!pip install scikit-learn  # ! ejecuta cualquier comando shell
```

### Paso 4: Outputs enriquecidos

Los notebooks auto-muestran la última expresión de una celda:

```python
import pandas as pd

df = pd.DataFrame({
    "modelo": ["Linear", "Random Forest", "Red Neuronal"],
    "precisión": [0.72, 0.89, 0.94],
    "tiempo_entrenamiento": [0.1, 2.3, 45.6]
})
df  # renderiza como tabla HTML formateada, no texto plano
```

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.title("Plot Inline")
plt.show()
# El gráfico aparece directamente debajo de la celda
```

---

## Notebooks vs Scripts: cuándo usar cuál

| Usa notebooks para | Usa scripts para |
|-------------------|------------------|
| Explorar datos | Pipelines de entrenamiento |
| Prototipar un modelo | Utilidades reutilizables |
| Visualizar resultados | Código que corre en schedule |
| Explicar tu trabajo | Código de producción |
| Ejercicios del curso | Paquetes y librerías |

**Regla: explora en notebooks, produce en scripts.**

---

## Trampas comunes

| Trampa | Fix |
|--------|-----|
| **Ejecución fuera de orden**: corriste celda 5, luego 2, luego 7. Funciona para ti pero no para otros | `Kernel > Restart & Run All` antes de compartir |
| **Estado oculto**: eliminaste una celda pero su variable vive en memoria | Reiniciar el kernel regularmente |
| **Memory leak**: cargaste datasets de 4 GB sin liberar | `del variable` + `gc.collect()` |

---

## Ejercicios

1. Crea un notebook y usa `%timeit` para comparar list comprehension vs NumPy para crear un array de 100,000 números aleatorios
2. Crea un notebook con celdas markdown y código que cargue un CSV, muestre un DataFrame y grafique un chart. Luego corre `Kernel > Restart & Run All` para verificar que funciona de arriba a abajo
3. Prueba el notebook en Google Colab con GPU gratuita

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| Kernel | "Lo que corre mi código" | Proceso Python separado que ejecuta celdas y mantiene variables en memoria |
| Cell | "Un bloque de código" | Unidad ejecutable independiente en un notebook, ya sea código o markdown |
| Magic command | "Trucos de Jupyter" | Comandos especiales con `%` o `%%` que controlan el entorno del notebook |
| `.ipynb` | "Archivo de notebook" | Archivo JSON con celdas, outputs y metadata. Significa IPython Notebook |
