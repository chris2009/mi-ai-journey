# L10 — Terminal & Shell

> La terminal es donde viven los AI engineers. Ponte cómodo aquí.

**Tipo:** Learn  
**Lenguajes:** —  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~35 minutos

---

## Objetivos de aprendizaje

- Usar piping, redirects y `grep` para filtrar y procesar logs de entrenamiento desde la línea de comandos
- Crear sesiones tmux persistentes con múltiples paneles para entrenamiento concurrente y monitoreo de GPU
- Monitorear recursos del sistema y GPU con `htop`, `nvtop` y `nvidia-smi`
- Transferir archivos entre máquinas locales y remotas con SSH, `scp` y `rsync`

---

## El problema

Pasarás más tiempo en la terminal que en cualquier editor. Runs de entrenamiento, monitoreo de GPU, tail de logs, sesiones remotas SSH, gestión de entornos. Cada flujo de trabajo de AI toca el shell. Si eres lento aquí, eres lento en todo.

Esta lección cubre las habilidades de terminal que importan para trabajo de AI. Sin historia de Unix. Sin deep-dive en Bash scripting. Solo lo que necesitas.

---

## El concepto

```
┌─────────────────────────────────────────────────────────┐
│  sesión tmux: training                                   │
│  ┌─────────────────────────┬─────────────────────────┐  │
│  │ Panel 1: Training run   │ Panel 2: GPU monitor    │  │
│  │ python train.py         │ watch -n1 nvidia-smi    │  │
│  │ Epoch 12/100 ...        │ GPU: 78% | Mem: 14/24G  │  │
│  └─────────────────────────┴─────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Panel 3: Logs + experiments                        │  │
│  │ tail -f logs/train.log | grep loss                 │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

Tres cosas corriendo al mismo tiempo. Una terminal. Puedes desconectarte, ir a casa, volver por SSH y reconectarte. El entrenamiento sigue corriendo.

---

## Paso a paso

### Paso 1: Conoce tu shell

Verifica qué shell estás corriendo:

```bash
echo $SHELL
```

La mayoría de sistemas usan `bash` o `zsh`. Ambos funcionan bien. Los comandos de este curso funcionan en cualquiera.

Cosas clave que saber:

```bash
# Navegar
cd ~/projects/ai-engineering-from-scratch
pwd
ls -la

# Búsqueda en historial (el atajo más útil que aprenderás)
# Ctrl+R luego escribe parte de un comando anterior
# Presiona Ctrl+R de nuevo para ciclar entre coincidencias

# Limpiar terminal
clear   # o Ctrl+L

# Cancelar un comando en ejecución
# Ctrl+C

# Suspender un comando (reanudar con fg)
# Ctrl+Z
```

### Paso 2: Piping y redirects

El piping conecta comandos entre sí. Así es como procesas logs, filtras output y encadenas herramientas. Lo usarás constantemente.

```bash
# Contar cuántas veces aparece "loss" en un log
cat train.log | grep "loss" | wc -l

# Extraer solo los valores de loss del output de entrenamiento
grep "loss:" train.log | awk '{print $NF}' > losses.txt

# Ver un archivo de log actualizarse en tiempo real, filtrando errores
tail -f train.log | grep --line-buffered "ERROR"

# Ordenar experimentos por accuracy final
grep "final_accuracy" results/*.log | sort -t= -k2 -n -r

# Redirigir stdout y stderr a archivos separados
python train.py > output.log 2> errors.log

# Redirigir ambos al mismo archivo
python train.py > train_full.log 2>&1
```

Los tres redirects que necesitas:

| Símbolo | Qué hace |
|---------|----------|
| `>` | Escribe stdout a archivo (sobreescribe) |
| `>>` | Agrega stdout al archivo |
| `2>` | Escribe stderr a archivo |
| `2>&1` | Envía stderr al mismo lugar que stdout |
| `\|` | Envía stdout de un comando como stdin al siguiente |

### Paso 3: Procesos en segundo plano

Los runs de entrenamiento toman horas. No quieres mantener tu terminal abierta todo el tiempo.

```bash
# Correr en segundo plano (output sigue yendo a la terminal)
python train.py &

# Correr en segundo plano, inmune al hangup (cerrar la terminal no lo mata)
nohup python train.py > train.log 2>&1 &

# Ver qué está corriendo en segundo plano
jobs
ps aux | grep train.py

# Traer un job de segundo plano al frente
fg %1

# Matar un proceso en segundo plano
kill %1
# o encontrar su PID y matar ese
kill $(pgrep -f "train.py")
```

La diferencia entre `&`, `nohup` y `screen`/`tmux`:

| Método | ¿Sobrevive al cierre de terminal? | ¿Puedes reconectarte? |
|--------|----------------------------------|----------------------|
| `command &` | No | No |
| `nohup command &` | Sí | No (revisa el archivo de log) |
| `screen` / `tmux` | Sí | **Sí** |

Para cualquier cosa de más de unos pocos minutos, usa tmux.

### Paso 4: tmux

tmux te permite crear sesiones de terminal persistentes con múltiples paneles. Es la herramienta más útil para gestionar runs de entrenamiento.

```bash
# Instalar (Ubuntu)
sudo apt install tmux

# Instalar (macOS)
brew install tmux

# Iniciar una sesión con nombre
tmux new -s training

# Dividir horizontalmente
# Ctrl+B luego "

# Dividir verticalmente
# Ctrl+B luego %

# Navegar entre paneles
# Ctrl+B luego flechas

# Desconectarse (la sesión sigue corriendo)
# Ctrl+B luego d

# Reconectarse
tmux attach -t training

# Listar sesiones
tmux ls

# Matar una sesión
tmux kill-session -t training
```

**Un flujo de trabajo típico de entrenamiento con tmux:**

```bash
# 1. Crear sesión
tmux new -s train

# 2. Panel 1: iniciar entrenamiento
python train.py --epochs 100 --lr 1e-4

# 3. Ctrl+B, " para dividir → monitorear GPU
watch -n1 nvidia-smi

# 4. Ctrl+B, % para dividir verticalmente → tail de logs
tail -f logs/experiment.log

# 5. Desconectarse con Ctrl+B, d
#    Ir por un café, volver
#    tmux attach -t train
```

### Paso 5: Monitoreo con htop y nvtop

```bash
# Procesos del sistema (mejor que top)
htop

# Procesos de GPU (si tienes GPU NVIDIA)
# Instalar: sudo apt install nvtop (Ubuntu) o brew install nvtop (macOS)
nvtop

# Check rápido de GPU sin nvtop
nvidia-smi

# Ver uso de GPU actualizándose cada segundo
watch -n1 nvidia-smi

# Ver qué procesos están usando la GPU
nvidia-smi --query-compute-apps=pid,name,used_memory --format=csv
```

**Atajos de `htop` que usarás:**
- `F6` o `>` para ordenar por columna (ordenar por memoria para encontrar memory leaks)
- `F5` para toggle de vista de árbol (ver procesos hijos)
- `F9` para matar un proceso
- `/` para buscar un nombre de proceso

### Paso 6: SSH para cajas GPU remotas

Cuando rentas una GPU en la nube (Lambda, RunPod, Vast.ai), te conectas por SSH.

```bash
# Conexión básica
ssh user@gpu-box-ip

# Con una llave específica
ssh -i ~/.ssh/my_gpu_key user@gpu-box-ip

# Copiar archivos al remoto
scp model.pt user@gpu-box-ip:~/models/

# Copiar archivos desde el remoto
scp user@gpu-box-ip:~/results/metrics.json ./

# Sincronizar un directorio completo (más rápido para muchos archivos)
rsync -avz ./data/ user@gpu-box-ip:~/data/

# Port forwarding (acceder a Jupyter/TensorBoard remotos localmente)
ssh -L 8888:localhost:8888 user@gpu-box-ip
# Luego abrir localhost:8888 en el navegador

# SSH config para conveniencia
# Agregar a ~/.ssh/config:
# Host gpu
#     HostName 192.168.1.100
#     User ubuntu
#     IdentityFile ~/.ssh/gpu_key
#
# Luego solo:
# ssh gpu
```

### Paso 7: Aliases útiles para trabajo de AI

Agrega estos a tu `~/.bashrc` o `~/.zshrc`:

```bash
# GPU status de un vistazo
alias gpu='nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader'

# Matar todos los procesos Python de entrenamiento
alias killtraining='pkill -f "python.*train"'

# Activar entorno virtual rápidamente
alias ae='source .venv/bin/activate'

# Vigilar loss del entrenamiento
alias watchloss='tail -f logs/*.log | grep --line-buffered "loss"'

# Shortcuts de tmux
alias ta='tmux attach -t'
alias tls='tmux ls'
alias tn='tmux new -s'
```

El archivo `code/shell_aliases.sh` del currículo contiene el set completo con funciones adicionales: `trainenv` (crea sesión tmux con 3 paneles preconfigurados), `syncto`/`syncfrom` (rsync simplificado), `newexp` (crea directorio de experimento con timestamp), `hfdownload` (descarga modelos de HF), `psg` (grep de procesos).

### Paso 8: Patrones comunes de terminal para AI

Estos aparecen repetidamente en la práctica:

```bash
# Correr entrenamiento, loggear todo, notificar cuando termine
python train.py 2>&1 | tee train.log; echo "DONE" | mail -s "Training complete" you@email.com

# Comparar dos logs de experimento lado a lado
diff <(grep "accuracy" exp1.log) <(grep "accuracy" exp2.log)

# Encontrar los archivos de modelo más grandes (limpiar espacio en disco)
find . -name "*.pt" -o -name "*.safetensors" | xargs du -h | sort -rh | head -20

# Contar líneas en todos los archivos Python (ver qué tan grande es tu proyecto)
find . -name "*.py" | xargs wc -l | tail -1

# Revisar espacio en disco (los datos de entrenamiento llenan discos rápido)
df -h
du -sh ./data/*

# Verificar variables de entorno antes de entrenar
env | grep -i cuda
env | grep -i torch
```

---

## Cuándo usar cada herramienta

| Herramienta | Cuándo la usas |
|-------------|---------------|
| tmux | En cada run de entrenamiento (Fases 3+) |
| `tail -f` + `grep` | Monitorear logs de entrenamiento |
| `nohup` / `&` | Tareas rápidas en segundo plano |
| `htop` / `nvtop` | Debuggear entrenamiento lento, errores OOM |
| SSH + `rsync` | Trabajar en GPUs de la nube |
| Piping + redirects | Procesar resultados de experimentos |
| Aliases | Ahorrar tiempo en comandos repetitivos |

---

## Ejercicios

1. Instala tmux, crea una sesión con tres paneles, corre `htop` en uno, `watch -n1 date` en otro, y un script Python en el tercero. Desconéctate y reconéctate.
2. Agrega los aliases de `code/shell_aliases.sh` a tu configuración de shell y recarga con `source ~/.bashrc` (o `~/.zshrc`).
3. Crea un log de entrenamiento falso con `for i in $(seq 1 100); do echo "epoch $i loss: $(echo "scale=4; 1/$i" | bc)"; sleep 0.1; done > fake_train.log` y luego usa `grep`, `tail` y `awk` para extraer solo los valores de loss.
4. Configura una entrada SSH config para un servidor que tengas acceso (o usa `localhost` para practicar la sintaxis).

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| Shell | "La terminal" | El programa que interpreta tus comandos (bash, zsh, fish) |
| tmux | "Multiplexor de terminal" | Programa que te permite correr múltiples sesiones de terminal dentro de una ventana, y desconectarte/reconectarte |
| Pipe | "La barra" | El operador `\|` que envía el output de un comando como input al siguiente |
| PID | "Process ID" | Número único asignado a cada proceso en ejecución, usado para monitorearlo o matarlo |
| nohup | "No hangup" | Corre un comando inmune a la señal de hangup, para que cerrar la terminal no lo mate |
| SSH | "Conectarse al servidor" | Secure Shell, protocolo encriptado para correr comandos en una máquina remota |
