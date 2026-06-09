# Quiz — L07 Docker for AI

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 2/2

### P1
**Pregunta:** ¿Cuál es la diferencia entre una imagen Docker y un contenedor?
**Respuesta elegida:** La imagen es la plantilla read-only (construida desde Dockerfile); el contenedor es una instancia corriendo de esa imagen ✅
**Correcto:** Sí — misma relación que clase vs objeto en POO.

### P2
**Pregunta:** ¿Por qué poner `COPY ./mi_codigo .` al final del Dockerfile en lugar de al principio?
**Respuesta elegida:** Porque Docker cachea las capas — lo que cambia más frecuentemente debe ir al final para no invalidar el caché de capas anteriores ✅
**Correcto:** Sí — el código cambia en cada iteración; las dependencias base cambian raro.

---

## Post-quiz — 2/3

### P1
**Pregunta:** ¿Para qué sirve un volume en Docker para AI Engineering?
**Respuesta elegida:** Para persistir datos entre reinicios del contenedor — especialmente modelos de 14+ GB que no quieres re-descargar en cada rebuild ✅
**Correcto:** Sí — `-v ~/models:/models` mapea la carpeta del host al contenedor.

### P2
**Pregunta:** ¿Qué hace `--gpus all` en `docker run`?
**Respuesta elegida:** (respuesta incorrecta) ❌
**Correcto:** No — `--gpus all` activa el puente entre el driver CUDA del host y el toolkit CUDA dentro del contenedor (NVIDIA Container Toolkit). Sin esto, el GPU no es accesible desde el contenedor aunque esté instalado en el host.

### P3
**Pregunta:** ¿Qué ventaja tiene `docker compose` sobre correr contenedores individuales?
**Respuesta elegida:** Orquesta múltiples servicios con un solo comando (`up -d`) y permite que los servicios se comuniquen por nombre (ej. `http://qdrant:6333`) ✅
**Correcto:** Sí

---

**Resultado final: pre 2/2 · post 2/3** ✅
El concepto de `--gpus all` / NVIDIA Container Toolkit fue el fallado en el post-quiz.
