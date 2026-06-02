#!/usr/bin/env bash
# Ejercicio L08: Verificar extensiones de VS Code y configuración del editor

echo "=== L08 — Editor Setup: Verificación ==="
echo ""

REQUIRED_EXTENSIONS=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-toolsai.jupyter"
    "eamodio.gitlens"
    "ms-python.debugpy"
    "ms-python.black-formatter"
    "charliermarsh.ruff"
)

echo "--- Extensiones instaladas ---"
INSTALLED=$(code --list-extensions 2>/dev/null)
echo "$INSTALLED"
echo ""

echo "--- Verificación de extensiones requeridas ---"
ALL_OK=true
for ext in "${REQUIRED_EXTENSIONS[@]}"; do
    if echo "$INSTALLED" | grep -qi "$ext"; then
        echo "  [PASS] $ext"
    else
        echo "  [FAIL] $ext — instalar con: code --install-extension $ext"
        ALL_OK=false
    fi
done
echo ""

echo "--- settings.json del proyecto ---"
SETTINGS_FILE="$(git rev-parse --show-toplevel 2>/dev/null)/.vscode/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo "  [PASS] .vscode/settings.json existe"
    echo "  Configuraciones clave:"
    grep -E "typeCheckingMode|formatOnSave|rulers|scrolling|autoSave" "$SETTINGS_FILE" | head -10
else
    echo "  [FAIL] .vscode/settings.json no encontrado"
fi

echo ""
if $ALL_OK; then
    echo "=== Todas las extensiones requeridas están instaladas ==="
else
    echo "=== Algunas extensiones faltan — ver arriba ==="
fi
