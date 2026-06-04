# L12 — Debugging and Profiling

> Los peores bugs de AI no crashean. Entrenan silenciosamente con basura y reportan una curva de loss perfecta.

**Tipo:** Build
**Lenguaje:** Python
**Prerrequisitos:** Lección 1 (Dev Environment), familiaridad básica con PyTorch
**Tiempo:** ~60 minutos

---

## Objetivos de aprendizaje

- Usar `breakpoint()` condicional y `debug_print` para inspeccionar shapes de tensores, dtypes y valores NaN durante el entrenamiento
- Perfilar training loops con `cProfile`, `line_profiler` y `tracemalloc` para encontrar cuellos de botella
- Detectar bugs comunes de AI: shape mismatches, NaN loss, data leakage, y tensores en el dispositivo equivocado
- Configurar TensorBoard para visualizar curvas de loss, histogramas de pesos y distribuciones de gradientes

---

## El Problema

El código de AI falla de manera diferente al código normal. Una app web crashea con un stack trace. Un training loop mal configurado corre durante 8 horas, quema $200 en tiempo de GPU, y produce un modelo que predice el promedio de cada input. El código nunca tiró error. El bug era un tensor en el dispositivo equivocado, un `.detach()` olvidado, o labels filtrándose en los features.

Necesitas herramientas de debugging que atrapen estos fallos silenciosos antes de que desperdicien tu tiempo y cómputo.

---

## El Concepto

El debugging de AI opera en tres niveles:

```
3. Dinámicas de Entrenamiento
   Curvas de loss, normas de gradientes, activaciones
         ↓
2. Operaciones de Tensores
   Shapes, dtypes, devices, valores NaN/Inf
         ↓
1. Python Estándar
   Breakpoints, logging, profiling, memoria
```

La mayoría de la gente salta directo al nivel 3 (mirando TensorBoard). Pero el 80% de los bugs de AI viven en los niveles 1 y 2.

---

## Construyéndolo

### Parte 1: Print Debugging (Sí, funciona)

El print debugging se descarta. No debería. Para código de tensores, un print statement preciso gana a pasar por el debugger porque necesitas ver shapes, dtypes y rangos de valores todos a la vez.

```python
def debug_print(name, tensor):
    print(f"{name}: shape={tensor.shape}, dtype={tensor.dtype}, "
          f"device={tensor.device}, "
          f"min={tensor.min().item():.4f}, max={tensor.max().item():.4f}, "
          f"mean={tensor.mean().item():.4f}, "
          f"has_nan={tensor.isnan().any().item()}")
```

Llama esto después de cada operación sospechosa. Cuando encuentres el bug, quita los prints. Simple.

### Parte 2: Python Debugger (pdb y breakpoint)

El debugger built-in está subestimado para trabajo de AI. Pon `breakpoint()` en tu training loop e inspecciona tensores de forma interactiva.

```python
def training_step(model, batch, criterion, optimizer):
    inputs, labels = batch
    outputs = model(inputs)
    loss = criterion(outputs, labels)

    if loss.item() > 100 or torch.isnan(loss):
        breakpoint()  # ← el debugger se detiene aquí

    loss.backward()
    optimizer.step()
```

Cuando el debugger te deja adentro, comandos útiles:

| Comando | Qué hace |
|---------|----------|
| `p outputs.shape` | Ver shape del tensor |
| `p loss.item()` | Ver valor del loss |
| `p torch.isnan(outputs).sum()` | Contar NaNs |
| `p model.fc1.weight.grad` | Verificar gradientes |
| `c` | Continuar ejecución |
| `q` | Salir del debugger |

Esto es debugging condicional: solo para cuando algo se ve mal. Para un training run de 10,000 pasos, eso importa.

### Parte 3: Python Logging

Reemplaza print statements con logging cuando tu debugging va más allá de una revisión rápida.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("training.log"),   # guarda en archivo
        logging.StreamHandler()                # también muestra en terminal
    ]
)
logger = logging.getLogger(__name__)

logger.info("Iniciando entrenamiento: lr=%.4f, batch_size=%d", lr, batch_size)
logger.warning("Spike de loss detectado: %.4f en el paso %d", loss.item(), step)
logger.error("NaN loss en el paso %d, deteniendo", step)
```

El logging te da timestamps, niveles de severidad y output a archivo. Cuando un training run falla a las 3 AM, quieres un archivo de log, no output de terminal que se desplazó fuera de la pantalla.

### Parte 4: Medir tiempo de secciones

Saber dónde se va el tiempo es el primer paso para optimizar.

```python
import time

class Timer:
    def __init__(self, name=""):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        elapsed = time.perf_counter() - self.start
        print(f"[{self.name}] {elapsed:.4f}s")

with Timer("carga de datos"):
    batch = next(dataloader_iter)

with Timer("forward pass"):
    outputs = model(batch)

with Timer("backward pass"):
    loss.backward()
```

**Hallazgo común:** la carga de datos toma el 60% del tiempo de entrenamiento. El fix es `num_workers > 0` en tu DataLoader, no una GPU más rápida.

### Parte 5: cProfile y line_profiler

Cuando necesitas más que timers manuales:

```bash
python -m cProfile -s cumtime train.py
```

Esto muestra cada llamada de función ordenada por tiempo acumulado. Para profiling línea por línea:

```bash
pip install line_profiler
```

```python
@profile
def train_step(model, data, target):
    output = model(data)
    loss = F.cross_entropy(output, target)
    loss.backward()
    return loss

# Correr con: kernprof -l -v train.py
```

### Parte 6: Profiling de Memoria

#### Memoria CPU con tracemalloc

```python
import tracemalloc

tracemalloc.start()

# tu código aquí
model = build_model()
data = load_dataset()

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
for stat in top_stats[:10]:
    print(stat)
```

#### Memoria CPU con memory_profiler

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def load_data():
    raw = read_csv("data.csv")       # ver el salto de memoria aquí
    processed = preprocess(raw)       # y aquí
    return processed

# Correr con: python -m memory_profiler tu_script.py
```

#### Memoria GPU con PyTorch

```python
import torch

if torch.cuda.is_available():
    print(torch.cuda.memory_summary())
    print(f"Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
    print(f"Cached: {torch.cuda.memory_reserved() / 1e9:.2f} GB")
```

**Cuando te golpea OOM (Out of Memory):**

1. Reduce el batch size (lo primero que probar, siempre)
2. Usa `torch.cuda.empty_cache()` para liberar memoria cacheada
3. Usa `del tensor` seguido de `torch.cuda.empty_cache()` para intermedios grandes
4. Usa mixed precision (`torch.cuda.amp`) para reducir el uso de memoria a la mitad
5. Usa gradient checkpointing para modelos muy profundos

### Parte 7: Bugs comunes de AI y cómo atraparlos

#### Shape Mismatch

El bug más frecuente. Un tensor tiene shape `[batch, features]` cuando el modelo espera `[batch, channels, height, width]`.

```python
def check_shapes(model, sample_input):
    print(f"Input: {sample_input.shape}")
    hooks = []

    def make_hook(name):
        def hook(module, inp, out):
            in_shape = inp[0].shape if isinstance(inp, tuple) else inp.shape
            out_shape = out.shape if hasattr(out, "shape") else type(out)
            print(f"  {name}: {in_shape} -> {out_shape}")
        return hook

    for name, module in model.named_modules():
        hooks.append(module.register_forward_hook(make_hook(name)))

    with torch.no_grad():
        model(sample_input)

    for h in hooks:
        h.remove()
```

Corre esto una vez con un batch de muestra. Mapea cada transformación de shape en tu modelo.

#### NaN Loss

NaN loss significa que algo explotó. Causas comunes:

- Learning rate demasiado alto
- División por cero en loss custom
- Log de cero o número negativo
- Gradientes que explotan en RNNs

```python
def detect_nan(model, loss, step):
    if torch.isnan(loss):
        print(f"NaN loss en el paso {step}")
        for name, param in model.named_parameters():
            if param.grad is not None:
                if torch.isnan(param.grad).any():
                    print(f"  Gradiente NaN en {name}")
                if torch.isinf(param.grad).any():
                    print(f"  Gradiente Inf en {name}")
        return True
    return False
```

#### Data Leakage

Tu modelo logra 99% de accuracy en el test set. Suena genial. Es un bug.

```python
def check_data_leakage(train_set, test_set, id_column="id"):
    train_ids = set(train_set[id_column].tolist())
    test_ids = set(test_set[id_column].tolist())
    overlap = train_ids & test_ids
    if overlap:
        print(f"DATA LEAKAGE: {len(overlap)} muestras en train Y test")
        return True
    return False
```

También revisa temporal leakage: usar datos futuros para predecir el pasado. Ordena por timestamp antes de hacer el split.

#### Wrong Device (Dispositivo equivocado)

Tensores en dispositivos diferentes (CPU vs GPU) causan errores en runtime. Pero a veces un tensor silenciosamente se queda en CPU mientras todo lo demás está en GPU, y el entrenamiento simplemente corre más lento.

```python
def check_devices(model, *tensors):
    model_device = next(model.parameters()).device
    print(f"Dispositivo del modelo: {model_device}")
    for i, t in enumerate(tensors):
        if t.device != model_device:
            print(f"  WARNING: tensor {i} en {t.device}, modelo en {model_device}")
```

### Parte 8: TensorBoard Básico

TensorBoard te muestra qué está pasando dentro del entrenamiento a lo largo del tiempo.

```bash
pip install tensorboard
```

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("runs/experimento_1")

for step in range(num_steps):
    loss = train_step(model, batch)

    writer.add_scalar("loss/train", loss.item(), step)
    writer.add_scalar("lr", optimizer.param_groups[0]["lr"], step)

    if step % 100 == 0:
        for name, param in model.named_parameters():
            writer.add_histogram(f"pesos/{name}", param, step)
            if param.grad is not None:
                writer.add_histogram(f"gradientes/{name}", param.grad, step)

writer.close()
```

Para lanzarlo:

```bash
tensorboard --logdir=runs
```

**Qué buscar en TensorBoard:**

| Síntoma | Causa probable |
|---------|---------------|
| Loss no baja | Learning rate demasiado bajo, o problema de arquitectura |
| Loss oscila mucho | Learning rate demasiado alto |
| Loss va a NaN | Inestabilidad numérica |
| Train loss baja, val loss sube | Overfitting |
| Histogramas de pesos colapsan a cero | Vanishing gradients |
| Histogramas de gradientes explotan | Necesitas gradient clipping |

### Parte 9: VS Code Debugger

Para debugging interactivo, configura VS Code con un `launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Training",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

Pon breakpoints haciendo click en el margen. Usa el panel Variables para inspeccionar propiedades de tensores. La Debug Console te deja correr expresiones Python arbitrarias durante la ejecución.

Útil para stepping a través de pipelines de preprocesamiento de datos donde quieres ver cada transformación.

---

## Flujo de debugging que atrapa la mayoría de los bugs de AI

1. **Antes de entrenar:** Corre `check_shapes` con un batch de muestra. Verifica que dimensiones de input y output coincidan con lo esperado.
2. **Primeros 10 pasos:** Usa `debug_print` en loss, outputs y gradientes. Confirma que nada es NaN y que los valores están en rangos razonables.
3. **Durante el entrenamiento:** Logea loss, learning rate y normas de gradientes. Usa TensorBoard para visualización.
4. **Cuando algo se rompe:** Pon `breakpoint()` en el punto de falla. Inspecciona tensores interactivamente.
5. **Para rendimiento:** Mide el tiempo de carga de datos vs forward vs backward pass. Perfila memoria si estás cerca de OOM.

---

## Ejercicios

1. **debug_tools.py + NaN injection:** Corre `debug_tools.py` y lee la salida de cada sección. Luego modifica el modelo para introducir un NaN (pista: divide por cero en el forward pass) y observa cómo el detector lo atrapa.

2. **cProfile:** Perfila un training loop con `cProfile` e identifica la función más lenta.

3. **tracemalloc:** Usa `tracemalloc` para encontrar qué línea en tu pipeline de carga de datos asigna más memoria.

4. **TensorBoard:** Configura TensorBoard para un training run simple e identifica si el modelo está haciendo overfitting.

5. **breakpoint() interactivo:** Usa `breakpoint()` dentro de un training loop. Practica inspeccionar shapes de tensores, dispositivos y valores de gradientes desde el prompt del debugger.

---

## Términos clave

| Término | Significado |
|---------|-------------|
| `debug_print` | Función que muestra shape, dtype, device, min/max/mean y NaN de un tensor |
| `breakpoint()` | Detiene ejecución y abre el debugger pdb interactivo |
| `cProfile` | Profiler de Python que mide tiempo por función |
| `line_profiler` | Profiler línea por línea (requiere `@profile` decorator) |
| `tracemalloc` | Módulo stdlib para rastrear asignaciones de memoria |
| `memory_profiler` | Profiler línea por línea de memoria RAM |
| `SummaryWriter` | Clase de PyTorch para escribir datos a TensorBoard |
| Shape mismatch | Error cuando las dimensiones del tensor no coinciden con lo que espera la capa |
| NaN loss | Pérdida numérica; indica valores que explotaron o división por cero |
| Data leakage | Datos del test set que se filtraron al training set |
| OOM | Out of Memory — sin VRAM disponible en GPU |
| Gradient clipping | Técnica para limitar el tamaño máximo de los gradientes y evitar explosión |
| Overfitting | Train loss baja pero val loss sube — el modelo memorizó el training set |
| Vanishing gradients | Gradientes que se vuelven tan pequeños que los pesos no se actualizan |
