# L11 — Linux para AI

> La mayoría del AI corre en Linux. Necesitas saber lo suficiente para no quedarte atascado.

**Tipo:** Learn  
**Lenguajes:** —  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~30 minutos

---

## Objetivos de aprendizaje

- Navegar el sistema de archivos de Linux y realizar operaciones esenciales desde la línea de comandos
- Gestionar permisos de archivos con `chmod` y `chown` para resolver errores de "Permission denied"
- Instalar paquetes del sistema con `apt` y preparar una GPU box nueva para trabajo de AI
- Identificar las diferencias macOS-a-Linux que comúnmente complican a desarrolladores en máquinas remotas

---

## El problema

Desarrollas en macOS o Windows. Pero en el momento que SSH-eas a una GPU box en la nube, rentas una instancia Lambda, o levantas una máquina EC2, llegas a Ubuntu. La terminal es tu única interfaz. No hay Finder, no hay Explorer, no hay GUI. Si no puedes navegar el sistema de archivos, instalar paquetes y gestionar procesos desde la línea de comandos, te quedas pagando horas de GPU idle mientras googleas "cómo descomprimir un archivo en Linux."

Esta es una guía de supervivencia. Cubre exactamente lo que necesitas para operar en una máquina Linux remota para trabajo de AI. Nada más.

---

## Estructura del sistema de archivos

Linux organiza todo bajo una sola raíz `/`. No hay `C:\` ni `/Volumes`. Los directorios que realmente tocarás:

```
/
├── home/tu-usuario/    → Tus archivos — clona repos, corre entrenamiento aquí
├── tmp/                → Archivos temporales, se limpian al reiniciar
├── usr/                → Programas y librerías del sistema
├── etc/                → Archivos de configuración
├── var/log/            → Logs — revisar cuando algo falla
├── mnt/ o /media/      → Discos externos y volúmenes
└── proc/ y /sys/       → Archivos virtuales — info del kernel y hardware
```

Tu directorio home es `~` o `/home/tu-usuario`. Casi todo lo que haces ocurre aquí.

---

## Comandos esenciales

Estos son los 15 comandos que cubren el 95% de lo que harás en una GPU box remota.

### Moverse

```bash
pwd                         # ¿Dónde estoy?
ls                          # ¿Qué hay aquí?
ls -la                      # ¿Qué hay aquí, incluyendo archivos ocultos con detalles?
cd /ruta/al/dir             # Ir allá
cd ~                        # Ir a home
cd ..                       # Subir un nivel
```

### Archivos y directorios

```bash
mkdir mi-proyecto           # Crear un directorio
mkdir -p a/b/c              # Crear directorios anidados de una vez

cp archivo.txt backup.txt   # Copiar un archivo
cp -r src/ src-backup/      # Copiar un directorio (recursivo)

mv viejo.txt nuevo.txt      # Renombrar un archivo
mv archivo.txt /tmp/        # Mover un archivo

rm archivo.txt              # Eliminar un archivo (sin papelera, desaparece para siempre)
rm -rf mi-dir/              # Eliminar un directorio y todo lo que contiene
```

> `rm -rf` es permanente. No hay deshacer. Verifica la ruta antes de presionar Enter.

### Leer archivos

```bash
cat archivo.txt             # Imprimir archivo completo
head -20 archivo.txt        # Primeras 20 líneas
tail -20 archivo.txt        # Últimas 20 líneas
tail -f log.txt             # Seguir un log en tiempo real (Ctrl+C para parar)
less archivo.txt            # Desplazarse por un archivo (q para salir)
```

### Buscar

```bash
grep "error" training.log           # Encontrar líneas que contienen "error"
grep -r "learning_rate" .           # Buscar en todos los archivos del directorio actual
grep -i "cuda" config.yaml          # Búsqueda sin distinción de mayúsculas

find . -name "*.py"                 # Encontrar todos los archivos Python bajo el dir actual
find . -name "*.ckpt" -size +1G     # Encontrar checkpoints mayores a 1GB
```

---

## Permisos

Cada archivo en Linux tiene un dueño y bits de permisos. Te los encontrarás cuando scripts no se ejecuten o no puedas escribir en un directorio.

```bash
ls -l train.py
# -rwxr-xr-- 1 user group 2048 Mar 19 10:00 train.py
#  ^^^             permisos del dueño: leer, escribir, ejecutar
#     ^^^          permisos del grupo: leer, ejecutar
#        ^^        todos los demás: solo leer
```

Arreglos comunes:

```bash
chmod +x train.sh           # Hacer un script ejecutable
chmod 755 deploy.sh         # Dueño: todo, otros: leer+ejecutar
chmod 644 config.yaml       # Dueño: leer+escribir, otros: solo leer

chown user:group archivo.txt  # Cambiar dueño (requiere sudo)
```

Cuando algo dice "Permission denied", casi siempre es un problema de permisos. `chmod +x` o `sudo` arreglan la mayoría de los casos.

---

## Gestión de paquetes (apt)

Ubuntu usa `apt`. Así instalas software a nivel de sistema.

```bash
sudo apt update             # Actualizar la lista de paquetes (siempre hacer esto primero)
sudo apt install -y htop    # Instalar un paquete (-y omite la confirmación)
sudo apt install -y build-essential  # Compilador C, make, etc. Necesario para muchos paquetes Python

apt list --installed        # ¿Qué está instalado?
sudo apt remove htop        # Desinstalar
```

Paquetes comunes que instalarás en una GPU box nueva:

```bash
sudo apt update && sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    tmux \
    htop \
    unzip \
    python3-venv
```

---

## Usuarios y sudo

Normalmente estás logueado como usuario regular. Algunas operaciones necesitan acceso root (admin).

```bash
whoami                      # ¿Qué usuario soy?
sudo comando                # Correr un solo comando como root
sudo su                     # Convertirse en root (exit para volver, usar con cuidado)
```

En instancias GPU en la nube, normalmente eres el único usuario y ya tienes acceso sudo. No corras todo como root. Usa sudo solo cuando sea necesario.

---

## Procesos y systemd

Cuando tu entrenamiento se cuelga, o necesitas verificar qué está corriendo:

```bash
htop                        # Visor interactivo de procesos (q para salir)
ps aux | grep python        # Encontrar procesos Python corriendo
kill 12345                  # Parar el proceso con PID 12345 (graceful)
kill -9 12345               # Forzar terminación (usar cuando el graceful no funciona)
nvidia-smi                  # Procesos GPU y uso de memoria
```

systemd gestiona servicios (daemons en segundo plano). Lo usarás si corres servidores de inferencia:

```bash
sudo systemctl start nginx          # Iniciar un servicio
sudo systemctl stop nginx           # Pararlo
sudo systemctl restart nginx        # Reiniciarlo
sudo systemctl status nginx         # Verificar si está corriendo
sudo systemctl enable nginx         # Iniciar automáticamente al arrancar
```

---

## Espacio en disco

Las GPU boxes suelen tener espacio en disco limitado. Modelos y datasets lo llenan rápido.

```bash
df -h                       # Uso de disco para todas las unidades montadas
df -h /home                 # Uso de disco para /home específicamente

du -sh *                    # Tamaño de cada ítem en el directorio actual
du -sh ~/.cache             # Tamaño de tu caché (pip, modelos de HF van aquí)
du -sh /data/checkpoints/   # Cuánto pesan tus checkpoints

# Encontrar los mayores consumidores de espacio
du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20
```

Ahorros de espacio comunes:

```bash
# Limpiar caché de pip
pip cache purge

# Limpiar caché de apt
sudo apt clean

# Eliminar checkpoints viejos que no necesitas
rm -rf checkpoints/epoch_01/ checkpoints/epoch_02/
```

---

## Red (networking)

Descargarás modelos, transferirás archivos y llamarás APIs desde la línea de comandos.

```bash
# Descargar archivos
wget https://ejemplo.com/modelo.bin                   # Descargar un archivo
curl -O https://ejemplo.com/datos.tar.gz              # Lo mismo con curl
curl -s https://api.ejemplo.com/health | python3 -m json.tool  # Llamar una API, imprimir JSON

# Transferir archivos entre máquinas
scp modelo.bin user@remoto:/datos/                    # Copiar archivo al remoto
scp user@remoto:/datos/resultados.csv .               # Copiar archivo desde remoto
scp -r user@remoto:/datos/checkpoints/ ./local-dir/   # Copiar directorio

# Sincronizar directorios (más rápido que scp para transferencias grandes)
rsync -avz --progress ./datos/ user@remoto:/datos/
rsync -avz --progress user@remoto:/resultados/ ./resultados/
```

Usa `rsync` en lugar de `scp` para cualquier cosa grande. Solo transfiere los bytes cambiados y maneja conexiones interrumpidas.

---

## tmux: Mantener sesiones vivas

Cuando SSH-eas a una caja remota, cerrar tu laptop mata tu run de entrenamiento. tmux lo previene.

```bash
tmux new -s train           # Iniciar nueva sesión llamada "train"
# ... iniciar entrenamiento, luego:
# Ctrl+B, luego D            # Desconectarse (el entrenamiento sigue corriendo)

tmux ls                     # Listar sesiones
tmux attach -t train        # Reconectarse a la sesión

# Dentro de tmux:
# Ctrl+B, luego %            # Dividir panel verticalmente
# Ctrl+B, luego "            # Dividir panel horizontalmente
# Ctrl+B, luego flechas      # Cambiar entre paneles
```

Siempre corre trabajos de entrenamiento largos dentro de tmux. Siempre.

---

## WSL2 para usuarios de Windows

Si estás en Windows, WSL2 te da un entorno Linux real sin dual-boot.

```bash
# En PowerShell (admin)
wsl --install -d Ubuntu-24.04

# Después del reinicio, abrir Ubuntu desde el menú Inicio
sudo apt update && sudo apt upgrade -y
```

WSL2 corre un kernel Linux real. Todo en esta lección funciona dentro de él. Tus archivos de Windows están en `/mnt/c/Users/TuNombre/` desde dentro de WSL.

El passthrough de GPU funciona con los drivers NVIDIA instalados en el lado Windows. Instala el driver NVIDIA para Windows (no el de Linux), y CUDA estará disponible dentro de WSL2.

---

## Gotchas: de macOS a Linux

Cosas que te van a complicar si vienes de macOS:

| macOS | Linux | Notas |
|-------|-------|-------|
| `brew install` | `sudo apt install` | Los nombres de paquetes a veces difieren. `brew install htop` vs `sudo apt install htop` funciona igual, pero `brew install readline` vs `sudo apt install libreadline-dev` no. |
| `open archivo.txt` | `xdg-open archivo.txt` | Pero no tendrás GUI en una caja remota. Usa `cat` o `less`. |
| `pbcopy` / `pbpaste` | No disponible | Pipe al portapapeles no existe por SSH. |
| `~/.zshrc` | `~/.bashrc` | macOS usa zsh por defecto. La mayoría de servidores Linux usan bash. |
| `/opt/homebrew/` | `/usr/bin/`, `/usr/local/bin/` | Los binarios viven en lugares distintos. |
| `sed -i '' 's/a/b/' archivo` | `sed -i 's/a/b/' archivo` | El sed de macOS necesita string vacío después de `-i`. Linux no. |
| Filesystem case-insensitive | Filesystem case-sensitive | `Modelo.py` y `modelo.py` son dos archivos distintos en Linux. |
| Saltos de línea `\n` | Saltos de línea `\n` | Igual. Pero Windows usa `\r\n`, que rompe scripts bash. Corre `dos2unix` para arreglarlo. |

---

## Tarjeta de referencia rápida

```
Navegación:   pwd, ls, cd, find
Archivos:     cp, mv, rm, mkdir, cat, head, tail, less
Búsqueda:     grep, find
Permisos:     chmod, chown, sudo
Paquetes:     apt update, apt install
Procesos:     htop, ps, kill, nvidia-smi
Servicios:    systemctl start/stop/restart/status
Disco:        df -h, du -sh
Red:          curl, wget, scp, rsync
Sesiones:     tmux new/attach/detach
```

---

## Ejercicios

1. Navega a tu directorio home, crea una carpeta `proyecto-linux`, crea tres archivos vacíos dentro con `touch`, y listarlos con `ls -la`.
2. Instala `htop` con apt, córrelo, e identifica qué proceso está usando más memoria.
3. Inicia una sesión tmux, corre `sleep 300` dentro, desconéctate, lista las sesiones, y reconéctate.
4. Usa `df -h` para ver el espacio disponible en disco, luego usa `du -sh ~/.cache/*` para encontrar qué está ocupando espacio en tu caché.
5. Transfiere un archivo de tu máquina local a una remota usando `scp`, luego haz la misma transferencia con `rsync` y compara la experiencia.

---

## Términos clave

| Término | Lo que significa |
|---------|-----------------|
| Root `/` | Raíz del sistema de archivos — todo parte de aquí |
| `~` | Atajo para `/home/tu-usuario` |
| `chmod` | Change mode — modifica permisos de archivos |
| `sudo` | Superuser do — ejecuta como administrador |
| `apt` | Advanced Package Tool — instalador de paquetes de Ubuntu/Debian |
| `systemd` | Sistema de init moderno — gestiona servicios del sistema |
| `rsync` | Remote sync — sincroniza archivos eficientemente, solo transfiere cambios |
| PID | Process ID — número único de cada proceso en ejecución |
