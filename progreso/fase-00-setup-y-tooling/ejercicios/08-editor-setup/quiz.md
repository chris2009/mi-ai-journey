# Quiz — L08 Editor Setup

> Nota: preguntas reconstruidas desde sesión compactada.

## Pre-quiz — 2/2

### P1
**Pregunta:** ¿Por qué habilitar `typeCheckingMode: "basic"` en Pylance para proyectos de AI?
**Respuesta elegida:** Detecta shape mismatches de tensores antes de correr el código — ahorra horas de debugging de errores de forma ✅
**Correcto:** Sí — Pylance puede inferir que estás multiplicando tensores incompatibles incluso sin ejecutar.

### P2
**Pregunta:** ¿En qué lado instalar la extensión Remote SSH — en WSL o en Windows?
**Respuesta elegida:** En Windows — es la extensión que inicia la conexión desde tu máquina local hacia el servidor remoto ✅
**Correcto:** Sí — Remote SSH va en el lado que origina la conexión, no en el destino.

---

## Post-quiz — 3/3

### P1
**Pregunta:** ¿Por qué configurar `formatOnSave: true` con Black?
**Respuesta elegida:** Para que el código se formatee automáticamente al guardar — nunca formatear a mano, Black es determinístico (mismo input = mismo output siempre) ✅
**Correcto:** Sí

### P2
**Pregunta:** ¿Qué hace `notebook.output.scrolling: true` y cuándo es crítico?
**Respuesta elegida:** Limita el height del output de celdas — sin esto, 10k líneas de un training loop explota el panel de VS Code ✅
**Correcto:** Sí

### P3
**Pregunta:** ¿Cuándo usarías Cursor o Windsurf en lugar de VS Code estándar?
**Respuesta elegida:** Cuando quieres AI integrada en el editor (autocompletado, refactoring, chat) — son forks de VS Code, mismo ecosystem y extensiones ✅
**Correcto:** Sí

---

**Resultado final: pre 2/2 · post 3/3** ✅
