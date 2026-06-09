# Quiz — L02 Git & Collaboration

> Nota: preguntas reconstruidas desde sesión compactada. El score registrado en notas.md es "Quiz: 3/3 ✅" sin distinción pre/post.

## Quiz — 3/3 ✅

### P1
**Pregunta:** ¿Cuál es el orden correcto del flujo diario en git?
**Respuesta elegida:** `git add` → `git commit` → `git push` ✅
**Correcto:** Sí — primero staging (add), luego snapshot local (commit), luego sincronizar con el remoto (push).

---

### P2
**Pregunta:** ¿Qué tipos de archivos de AI nunca deben commitearse en git?
**Respuesta elegida:** Checkpoints de modelos (*.pt, *.pth, *.safetensors, *.ckpt, *.bin) — pesan cientos de MB a GB ✅
**Correcto:** Sí — los binarios grandes van en HuggingFace Hub o DVC, no en git.

---

### P3
**Pregunta:** ¿Qué hace `git checkout -b experiment/mi-idea`?
**Respuesta elegida:** Crea una nueva rama Y cambia a ella en un solo paso ✅
**Correcto:** Sí — `-b` equivale a `git branch nombre` + `git checkout nombre` combinados.

---

**Resultado final: 3/3** ✅
