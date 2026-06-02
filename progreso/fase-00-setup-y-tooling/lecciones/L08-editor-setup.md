# L08 — Configuración del Editor

> Tu editor es tu co-piloto. Configúralo una vez para que no estorbe y empiece a trabajar por ti.

**Tipo:** Build  
**Lenguajes:** —  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~20 minutos

---

## Objetivos de aprendizaje

- Instalar VS Code con extensiones esenciales para Python, Jupyter, linting y SSH remoto
- Configurar format-on-save, type checking y scrolling de output de notebooks para flujos de AI
- Configurar Remote SSH para editar y depurar código en máquinas GPU remotas como si fueran locales
- Evaluar alternativas de editor (Cursor, Windsurf, Neovim) y sus tradeoffs para trabajo en AI

---

## El problema

Pasarás miles de horas dentro de tu editor escribiendo Python, corriendo notebooks, depurando loops de entrenamiento y conectándote por SSH a cajas GPU. Un editor mal configurado convierte cada sesión en fricción: sin autocompletado, sin type hints, sin errores inline, formateo manual, y un flujo de terminal torpe.

La configuración correcta tarda 20 minutos. Saltársela cuesta 20 minutos cada día.

---

## El concepto

Un setup de editor para AI engineering necesita 5 cosas:

```
5. Remote Development  → SSH a cajas GPU / VMs en la nube
4. Terminal Integration → correr scripts, depurar, monitorear GPU
3. AI-Specific Settings → format-on-save, type checking, rulers
2. Extensions          → Python, Jupyter, Pylance, GitLens
1. Base Editor         → VS Code (gratis, extensible, universal)
```

---

## Paso a paso

### Paso 1: Instalar VS Code

VS Code es el editor recomendado. Es gratuito, corre en cualquier OS, tiene soporte de primera clase para notebooks Jupyter, y el ecosistema de extensiones cubre todo lo necesario para trabajo de AI.

Verificar desde la terminal:

```bash
code --version
```

### Paso 2: Instalar extensiones esenciales

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension ms-vscode-remote.remote-ssh    # solo en Windows, no en WSL
code --install-extension ms-python.debugpy
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
```

| Extensión | Para qué sirve |
|-----------|----------------|
| Python | Soporte de lenguaje, detección de venv, run/debug |
| Pylance | Type checking rápido, autocompletado, resolución de imports |
| Jupyter | Correr notebooks en VS Code, variable explorer |
| GitLens | Blame inline — ver quién cambió qué y cuándo |
| Remote SSH | Abrir carpeta en GPU remota como si fuera local (instalar en Windows) |
| Debugpy | Debugging paso a paso para Python |
| Black Formatter | Formato automático al guardar |
| Ruff | Linting rápido, detecta errores comunes |

> **Nota WSL:** Remote SSH se instala en Windows, no en WSL. Es la extensión que inicia la conexión desde tu máquina local hacia servidores remotos.

### Paso 3: Configurar settings

Crear `.vscode/settings.json` en el proyecto:

```jsonc
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.inlayHints.functionReturnTypes": true,

    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },

    "black-formatter.args": ["--line-length", "88"],
    "ruff.lint.run": "onSave",

    "editor.rulers": [88, 120],
    "editor.tabSize": 4,
    "editor.bracketPairColorization.enabled": true,
    "editor.minimap.enabled": false,

    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "files.trimTrailingWhitespace": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.ipynb_checkpoints": true,
        "**/*.pyc": true
    },

    "notebook.output.scrolling": true,
    "notebook.output.textLineLimit": 500,

    "terminal.integrated.scrollback": 10000,
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.defaultProfile.linux": "bash",

    "git.autofetch": true,
    "search.exclude": {
        "**/.venv": true
    }
}
```

**Por qué importa cada setting:**

| Setting | Por qué importa |
|---------|----------------|
| `typeCheckingMode: "basic"` | Detecta shape mismatches de tensores antes de correr un training run de 8 horas |
| `formatOnSave: true` | Black formatea al guardar — nunca formatear a mano |
| `rulers: [88, 120]` | Black corta en 88; referencia visual para comentarios en 120 |
| `notebook.output.scrolling: true` | Sin esto, 10k líneas de un training loop explotan el panel |
| `files.autoSave: afterDelay` | Guarda 1s después de escribir — nunca código stale en el training run |

### Paso 4: Terminal integrada

Atajos útiles:

| Acción | Linux/Windows |
|--------|---------------|
| Toggle terminal | `` Ctrl+` `` |
| Nueva terminal | `` Ctrl+Shift+` `` |
| Split terminal | `Ctrl+\` |

**Split de terminal para monitorear GPU:**
- Panel izquierdo: `python train.py`
- Panel derecho: `watch -n 1 nvidia-smi`

### Paso 5: Remote Development (SSH a cajas GPU)

Esta es la extensión más importante para trabajo en AI. Cuando entrenes en instancias remotas (Lambda Labs, Vast.ai, servidor universitario), Remote SSH te permite abrir el filesystem remoto, editar archivos, correr terminales y depurar como si todo fuera local.

Setup:

1. Instalar la extensión Remote SSH en **Windows** (no en WSL)
2. `Ctrl+Shift+P` → "Remote-SSH: Connect to Host"
3. Ingresar `usuario@ip-de-tu-gpu`
4. VS Code instala su componente servidor en la máquina remota automáticamente

Para acceso sin contraseña:

```bash
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
ssh-copy-id usuario@ip-de-tu-gpu
```

Agregar el host a `~/.ssh/config`:

```
Host gpu-box
    HostName 203.0.113.50
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

Ahora `Remote-SSH: Connect to Host > gpu-box` conecta instantáneamente.

---

## Alternativas

| Editor | Cuándo usarlo |
|--------|--------------|
| **Cursor** | Fork de VS Code con AI integrada. Mismas extensiones y formato de settings. |
| **Windsurf** | Otro fork AI-first de VS Code. Mismo ecosistema. |
| **Neovim** | Solo si ya eres experto. No aprender junto con AI Engineering — la curva de aprendizaje competirá con aprender AI. |

---

## Ejercicios

1. Instala todas las extensiones listadas en el Paso 2
2. Crea `.vscode/settings.json` con la configuración de la lección
3. Abre un archivo Python y verifica que Pylance muestra type hints y Black formatea al guardar
4. Si tienes acceso a una máquina remota, configura Remote SSH y abre una carpeta en ella

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| LSP | "Motor de autocompletado" | Language Server Protocol: estándar para que los editores reciban type info, completions y diagnósticos de un servidor específico del lenguaje |
| Pylance | "El plugin de Python" | Servidor de lenguaje Python de Microsoft usando Pyright para type checking e IntelliSense |
| Remote SSH | "Trabajar en el servidor" | Extensión de VS Code que corre un servidor ligero en una máquina remota y transmite la UI a tu editor local |
| Format on save | "Auto-prettier" | El editor corre un formateador (Black, Ruff) cada vez que guardas, para que el estilo siempre sea consistente |
