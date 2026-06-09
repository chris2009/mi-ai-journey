# Quiz — L10 Terminal & Shell

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 1/2

### P1
**Pregunta:** Lanzas un training de 6 horas con `python train.py &` y cierras la terminal. ¿Qué pasa?
**Respuesta elegida:** (respuesta incorrecta) ❌
**Correcto:** No — el proceso muere al cerrar la terminal (pierde su proceso padre). Para training largo hay que usar `tmux` (o `nohup`). tmux es la única opción que también permite reconectarse y ver el output en tiempo real.

### P2
**Pregunta:** ¿Qué hace `2>&1` en `python train.py > log.txt 2>&1`?
**Respuesta elegida:** Redirige stderr al mismo destino que stdout — así tanto los errores como la salida normal van al mismo archivo de log ✅
**Correcto:** Sí

---

## Post-quiz — 3/3

### P1
**Pregunta:** ¿Cuál es el comando tmux para desconectarse de una sesión sin matarla?
**Respuesta elegida:** `Ctrl+B d` (detach) — la sesión sigue corriendo en segundo plano; se recupera con `tmux attach -t nombre` ✅
**Correcto:** Sí

### P2
**Pregunta:** Después de correr `source ~/.bashrc`, tu venv se desactiva. ¿Por qué y cómo lo arreglas?
**Respuesta elegida:** `source ~/.bashrc` resetea el PATH, borrando la activación del venv. Fix: correr el alias `ae` después (con ruta absoluta, funciona desde cualquier directorio) ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Qué hace `grep "loss:" train.log | awk '{print $NF}'`?
**Respuesta elegida:** Filtra las líneas que contienen "loss:" y extrae el último campo de cada una (el valor numérico) ✅
**Correcto:** Sí — pipe: grep filtra líneas, awk extrae columna.

---

**Resultado final: pre 1/2 · post 3/3** ✅
El concepto de `command &` vs tmux fue el fallado en el pre-quiz.
