# L02 — Git y Colaboración

> El control de versiones no es opcional. Cada experimento, modelo y lección que construyas aquí se registra.

**Tipo:** Learn  
**Lenguajes:** —  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~30 minutos

---

## Objetivos de aprendizaje

- Configurar la identidad de git y usar el flujo diario de add, commit y push
- Crear y fusionar ramas para experimentos aislados sin romper main
- Escribir un `.gitignore` que excluya checkpoints de modelos y archivos binarios grandes
- Navegar el historial de commits con `git log` para entender la evolución del proyecto

---

## El problema

Estás a punto de escribir cientos de archivos de código en 20 fases. Sin control de versiones perderás trabajo, romperás cosas que no podrás deshacer, y no tendrás forma de colaborar con otros.

Git es la herramienta. GitHub es donde vive el código.

---

## El concepto

```
Working Directory → Staging Area → Local Repo → Remote (GitHub)
    (editas)          git add        git commit    git push
                                                ↑
                                             git fetch/pull
```

Tres cosas para recordar:
1. Guarda seguido (`git commit`)
2. Sube al remoto (`git push`)
3. Usa ramas para experimentos (`git checkout -b experiment`)

---

## Paso a paso

### Paso 1: Configurar git

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tuemail@ejemplo.com"
```

### Paso 2: El flujo diario

```bash
git status                              # ver qué cambió
git add archivo.py                      # staging
git commit -m "Agrega implementación del perceptrón"
git push origin main
```

### Paso 3: Ramas para experimentos

```bash
git checkout -b experiment/nuevo-optimizador   # crea rama y cambia a ella

# ... hacer cambios, commitear ...

git checkout main
git merge experiment/nuevo-optimizador
```

### Paso 4: .gitignore para AI Engineering

Los checkpoints de modelos pueden pesar cientos de MB a varios GB. Nunca van en git.

```gitignore
# Pesos de modelos
*.pt
*.pth
*.safetensors
*.ckpt
*.bin
*.onnx

# Datos
data/*.parquet
data/*.csv

# Entornos virtuales
.venv/
__pycache__/
*.pyc

# API keys
.env
```

---

## Comandos esenciales para el curso

| Comando | Cuándo usarlo |
|---------|---------------|
| `git clone` | Obtener un repo |
| `git add` + `git commit` | Guardar tu trabajo |
| `git push` | Respaldar en GitHub |
| `git checkout -b` | Probar algo sin romper main |
| `git log --oneline` | Ver qué has hecho |

No necesitas rebase, cherry-pick ni submódulos para este curso.

---

## Ejercicios

1. Crea un branch llamado `my-progress`, crea un archivo, commitéalo y súbelo
2. Crea un `.gitignore` que excluya archivos de checkpoints de modelos (`.pt`, `.pth`, `.safetensors`)
3. Mira el historial del repo con `git log --oneline`

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| Commit | "Guardar" | Un snapshot de todo tu proyecto en un momento del tiempo |
| Branch | "Una copia" | Un puntero a un commit que avanza mientras trabajas |
| Merge | "Combinar código" | Tomar cambios de una rama y aplicarlos a otra |
| Remote | "La nube" | Una copia de tu repo alojada en otro lugar (GitHub, GitLab) |
| Staging area | "Área intermedia" | Zona donde seleccionas qué cambios van en el próximo commit |
