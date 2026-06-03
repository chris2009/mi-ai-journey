# Contexto del proyecto — mi-ai-journey

## Quién soy
Christian (christian.cajusol@utec.edu.pe). Aprendo AI Engineering siguiendo el currículo de 20 fases en `ai-engineering-from-scratch/`. Claude me guía lección a lección en español.

## Repo
- **Este directorio**: `D:\APRENDIZAJE\AI_ENGINEERING` → git repo conectado a https://github.com/chris2009/mi-ai-journey (rama: `main`)
- **Currículo de referencia**: `ai-engineering-from-scratch/` — solo lectura, nunca commitear (está en .gitignore)

## Entorno
- VS Code abierto en modo **WSL: Ubuntu** (siempre usar `code .` desde la terminal WSL)
- Python venv en `.venv/` — activar con `source .venv/bin/activate`
- GPU: RTX 4070 Laptop (8.6 GB VRAM), CUDA 12.5, PyTorch 2.6.0+cu124
- API keys en `.env` (no commitear): ANTHROPIC_API_KEY, OPENAI_API_KEY

## Progreso actual

### Fase 00 — Setup & Tooling (🔄 En progreso)
| Lección | Tema | Estado |
|---------|------|--------|
| L01 | Dev Environment | ✅ |
| L02 | Git & Collaboration | ✅ |
| L03 | GPU Setup & Cloud | ✅ |
| L04 | APIs & Keys | ✅ |
| L05 | Jupyter Notebooks | ✅ |
| L06 | Python Environments | ✅ |
| L07 | Docker for AI | ✅ |
| L08 | Editor Setup | ✅ |
| L09 | Data Management | ✅ |
| L10 | Terminal & Shell | ✅ |
| L11 | Linux para AI | ✅ |
| L12 | Debugging & Profiling | ⬜ |

## Convenciones de archivos por lección
Cada lección completada debe producir:
1. **Lección traducida**: `progreso/fase-XX-nombre/lecciones/L0Y-nombre.md` — traducción completa del `en.md` al español
2. **Ejercicios**: `progreso/fase-XX-nombre/ejercicios/0Y-nombre/` — código de los ejercicios
3. **Outputs**: `progreso/fase-XX-nombre/ejercicios/0Y-nombre/outputs/` — resultados reales de correr los ejercicios
4. **Notas**: `progreso/fase-XX-nombre/notas.md` — resumen de conceptos clave + quiz scores
5. **APRENDIZAJE.md** — diario acumulativo con código y resultados reales
- Commit después de cada lección completada
- README.md se actualiza con el progreso al terminar cada lección

## METODOLOGÍA DE ENSEÑANZA — CRÍTICO
**Rol de Claude:** Guía. Explica conceptos, da instrucciones paso a paso, verifica resultados.
**Rol de Christian:** Ejecuta. Escribe el código, corre los comandos, comparte los outputs.

### Flujo por lección:
1. Claude lee `en.md` y lo traduce al español → guarda en `lecciones/L0Y-nombre.md`
2. Claude pregunta a Christian: "¿Ya leíste la lección?" — esperar confirmación antes de continuar
3. Claude administra pre-quiz con AskUserQuestion
4. Claude guía los ejercicios del `.md` traducido UNO POR UNO — Christian los ejecuta
5. Christian comparte el output → Claude lo verifica, guarda en `outputs/` y explica qué significa
6. Claude administra post-quiz con AskUserQuestion
7. Claude actualiza notas.md, APRENDIZAJE.md, CLAUDE.md, README.md
8. Commit + push

**Claude NO corre código. Christian SÍ corre código.**
**Claude NO escribe ejercicios por Christian. Claude GUÍA a Christian para que los escriba.**

## Mantenimiento de este archivo
**Actualizar CLAUDE.md siempre que:**
- Se complete una lección (cambiar ⬜/🔄 a ✅ en la tabla de progreso)
- Se cambie de fase
- Se agregue una convención nueva al proyecto
