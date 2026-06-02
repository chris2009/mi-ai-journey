# L07 — Docker para AI

> Los contenedores hacen que "funciona en mi máquina" sea cosa del pasado.

**Tipo:** Build  
**Lenguajes:** Docker  
**Prerequisitos:** Fase 0, Lecciones 01 y 03  
**Tiempo:** ~60 minutos

---

## Objetivos de aprendizaje

- Construir una imagen Docker con GPU, CUDA, PyTorch y librerías AI desde un Dockerfile
- Montar directorios del host como volúmenes para persistir modelos, datasets y código
- Configurar el NVIDIA Container Toolkit para exponer GPUs dentro de contenedores
- Orquestar aplicaciones AI de múltiples servicios (servidor de inferencia + base de datos vectorial) usando Docker Compose

---

## El problema

Entrenaste un modelo en tu laptop con PyTorch 2.3, CUDA 12.4 y Python 3.12. Tu colega tiene PyTorch 2.1, CUDA 11.8 y Python 3.10. Tu modelo falla en su máquina. Tu Dockerfile funciona en ambas.

Los proyectos de AI son pesadillas de dependencias: Python, PyTorch, drivers CUDA, cuDNN, librerías C de sistema, y paquetes especializados que necesitan versiones exactas del compilador. Docker empaqueta todo esto en una imagen única que corre idénticamente en cualquier lugar.

---

## El concepto

Docker envuelve tu código, runtime, librerías y herramientas del sistema en una unidad aislada llamada **contenedor**. Piénsalo como una máquina virtual ligera, excepto que comparte el kernel del OS host en lugar de correr el suyo propio, por lo que arranca en segundos.

### Por qué los proyectos AI necesitan Docker más que otros

1. **Los drivers GPU son frágiles.** El código CUDA 12.4 no corre en CUDA 11.8. Docker aísla el toolkit CUDA dentro del contenedor mientras comparte el driver GPU del host via NVIDIA Container Toolkit.

2. **Los pesos de modelos son grandes.** Un modelo de 7B parámetros pesa 14 GB en fp16. No quieres re-descargarlo cada vez que rebuilds. Los volúmenes de Docker montan un directorio de modelos desde el host.

3. **Las arquitecturas multi-servicio son comunes.** Una aplicación AI real no es solo un script Python. Es un servidor de inferencia, una base de datos vectorial para RAG, quizás un frontend web. Docker Compose orquesta todo con un comando.

### Vocabulario clave

| Término | Qué significa |
|---------|---------------|
| Image | Plantilla read-only. Tu receta. Construida desde un Dockerfile. |
| Container | Instancia corriendo de una image. Tu cocina. |
| Dockerfile | Instrucciones para construir una image. Capa por capa. |
| Volume | Almacenamiento persistente que sobrevive reinicios del contenedor. |
| docker-compose | Herramienta para definir aplicaciones multi-contenedor en YAML. |

---

## Paso a paso

### Paso 1: Instalar Docker

```bash
# Ubuntu
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar para que el cambio de grupo tenga efecto
```

Verificar:

```bash
docker --version
docker run hello-world
```

### Paso 2: NVIDIA Container Toolkit

Permite a los contenedores Docker acceder a tu GPU.

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
    sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Probar acceso GPU dentro de un contenedor:

```bash
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
```

**Arquitectura del toolkit:**
- El **driver CUDA** vive en el **host**
- El **toolkit CUDA** (librerías) vive **dentro del contenedor**
- `--gpus all` activa el puente entre ambos

### Paso 3: Imágenes base — cuál elegir

```
nvidia/cuda:12.4.1-devel-ubuntu22.04
  Toolkit CUDA completo. Compiladores incluidos.
  Usar para: construir paquetes que necesitan nvcc (flash-attn, bitsandbytes)
  Tamaño: ~4 GB

nvidia/cuda:12.4.1-runtime-ubuntu22.04
  Solo runtime CUDA. Sin compiladores.
  Usar para: correr código pre-compilado
  Tamaño: ~1.5 GB

python:3.12-slim
  Sin CUDA. Solo CPU.
  Usar para: inferencia en CPU, herramientas ligeras
  Tamaño: ~150 MB
```

### Paso 4: Escribir un Dockerfile para AI

```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Instalaciones que cambian poco van ARRIBA (se cachean)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv git curl \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# PyTorch — capa pesada pero estable
RUN python -m pip install --no-cache-dir torch==2.6.0 \
    --index-url https://download.pytorch.org/whl/cu124

# Paquetes adicionales
RUN python -m pip install --no-cache-dir numpy jupyter flask

WORKDIR /workspace

VOLUME ["/workspace", "/models"]

EXPOSE 8888 5000

CMD ["python"]
```

**Regla de orden de capas: lo que cambia menos va arriba (se cachea). Lo que cambia más va abajo.**

```
FROM nvidia/cuda...       ← nunca cambia
RUN apt-get install...    ← cambia poco
RUN pip install torch...  ← cambia poco
COPY ./mi_codigo .        ← cambia mucho → AL FINAL
```

Construir:

```bash
docker build -t ai-dev .
```

Correr (con GPU):

```bash
docker run --rm -it --gpus all \
    -v $(pwd):/workspace \
    -v ~/models:/models \
    ai-dev python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
```

### Paso 5: Volúmenes — por qué son críticos en AI

```bash
-v ~/models:/models      # modelo de 14 GB descargado una vez, vive en el host
-v $(pwd):/workspace     # código persistente entre rebuilds
-v ~/datasets:/data      # datasets grandes en el host
```

Dentro de tu script:

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("/models/llama-7b")
# El modelo vive en el host. Puedes rebuildar el contenedor sin re-descargarlo.
```

### Paso 6: Docker Compose para aplicaciones AI multi-servicio

```yaml
services:
  ai-dev:
    build:
      context: .
      dockerfile: Dockerfile
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ../../..:/workspace
      - ~/models:/models
    ports:
      - "8888:8888"
      - "5000:5000"
    stdin_open: true
    tty: true

  qdrant:
    image: qdrant/qdrant:v1.12.5
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
```

```bash
docker compose up -d      # levanta ai-dev + qdrant en segundo plano
docker compose down       # para todo
docker compose down -v    # para todo + elimina volúmenes
```

Los servicios se comunican por nombre: `http://qdrant:6333` desde el contenedor ai-dev.

### Paso 7: Comandos útiles de Docker para AI

```bash
docker ps                                    # contenedores corriendo
docker images                                # imágenes y sus tamaños
docker system prune -a                       # liberar espacio en disco
docker exec -it <container_id> nvidia-smi   # monitorear GPU dentro del contenedor
docker logs -f <container_id>               # ver logs en tiempo real
```

---

## Ejercicios

1. Construye el Dockerfile y corre `python -c "import torch; print(torch.__version__)"` dentro del contenedor
2. Levanta el stack de docker-compose y verifica que Qdrant es accesible en `http://localhost:6333/collections`
3. Agrega `flask` al Dockerfile, rebuilda, y corre un servidor API simple en el puerto 5000
4. Mide el tamaño de la imagen con `docker images`

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| Container | "VM ligera" | Proceso aislado que usa el kernel del host, con su propio filesystem y red |
| Image layer | "Paso cacheado" | Cada instrucción del Dockerfile crea una capa. Las capas sin cambios se cachean; los rebuilds son rápidos |
| NVIDIA Container Toolkit | "GPU en Docker" | Hook de runtime que expone GPUs del host a contenedores via `--gpus` |
| Volume mount | "Carpeta compartida" | Directorio del host mapeado al contenedor. Los cambios persisten después de que el contenedor para |
| Base image | "Punto de partida" | La imagen `FROM` sobre la que construye tu Dockerfile. Determina qué viene pre-instalado |
