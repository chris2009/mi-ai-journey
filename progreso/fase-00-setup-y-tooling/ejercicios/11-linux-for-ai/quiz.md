# Quiz — L11 Linux para AI

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 2/2

### P1
**Pregunta:** ¿Cuál es la diferencia entre `kill 12345` y `kill -9 12345`?
**Respuesta elegida:** `kill` envía SIGTERM (el proceso puede hacer cleanup antes de morir); `kill -9` envía SIGKILL (el kernel lo mata inmediatamente, sin excepción posible) ✅
**Correcto:** Sí — siempre intentar SIGTERM primero; -9 solo si el proceso está colgado.

### P2
**Pregunta:** Tu script en macOS funciona pero en el servidor Linux falla el import `from Model import ...`. ¿Por qué?
**Respuesta elegida:** Linux es case-sensitive — `Model.py` y `model.py` son archivos distintos. macOS es case-insensitive y no distingue, Linux sí ✅
**Correcto:** Sí — uno de los gotchas más comunes al migrar de macOS a servidores Linux.

---

## Post-quiz — 3/3

### P1
**Pregunta:** ¿Qué hace `chmod 755 deploy.sh` en cada uno de los tres grupos (dueño / grupo / otros)?
**Respuesta elegida:** Dueño: lectura + escritura + ejecución (7); grupo: lectura + ejecución (5); otros: lectura + ejecución (5) ✅
**Correcto:** Sí — en binario: 7=111 (rwx), 5=101 (r-x).

### P2
**Pregunta:** ¿Por qué usar `rsync` en lugar de `scp` para transferir un checkpoint de 14 GB a un servidor?
**Respuesta elegida:** rsync reanuda donde quedó si se interrumpe y solo transfiere los bytes cambiados — scp empieza de cero cada vez ✅
**Correcto:** Sí

### P3
**Pregunta:** Tienes 94% del disco de Windows ocupado. ¿Qué cachés de Python puedes limpiar?
**Respuesta elegida:** `pip cache purge` (~6.4 GB) + `uv cache clean` (~5.8 GB) → ~12.2 GB recuperables ✅
**Correcto:** Sí — estos cachés crecen silenciosamente con cada instalación y son 100% regenerables.

---

**Resultado final: pre 2/2 · post 3/3** ✅
