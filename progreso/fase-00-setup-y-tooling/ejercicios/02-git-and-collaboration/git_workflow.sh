#!/usr/bin/env bash
# Ejercicio L02: Flujo de trabajo Git para AI Engineering
# Corre este script para verificar que tu entorno git está correctamente configurado

set -euo pipefail

echo "=== L02 — Git & Collaboration: Verificación de Ejercicios ==="
echo ""

# Ejercicio 1: Verificar que estás en el repo correcto y en la rama main
echo "--- Ejercicio 1: Repositorio y rama ---"
echo "Repo remoto:"
git remote -v
echo ""
echo "Rama actual:"
git branch --show-current
echo ""

# Ejercicio 2: Mostrar el .gitignore actual (debe excluir pesos de modelos)
echo "--- Ejercicio 2: .gitignore para AI ---"
echo "Entradas de modelos en .gitignore:"
grep -E "\.(pt|pth|safetensors|bin|onnx)" "$(git rev-parse --show-toplevel)/.gitignore" || \
    echo "  [!] Faltan entradas para archivos de modelo"
echo ""

# Ejercicio 3: Historial de commits (cómo se añadieron las lecciones)
echo "--- Ejercicio 3: Historial de commits ---"
git log --oneline -15
echo ""

echo "=== Resumen ==="
echo "  Rama:   $(git branch --show-current)"
echo "  Commits: $(git rev-list --count HEAD)"
echo "  Último: $(git log -1 --format='%h %s')"
