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
| L05 | Jupyter Notebooks | 🔄 En progreso |
| L06–L12 | (pendientes) | ⬜ |

## Convenciones
- Notas por fase: `progreso/fase-XX-nombre/notas.md`
- Ejercicios: `progreso/fase-XX-nombre/ejercicios/`
- Artefactos reutilizables (prompts, skills): `outputs/`
- Commit después de cada lección completada
- README.md se actualiza con el progreso al terminar cada lección

## Cómo guiar las lecciones
1. Leer `ai-engineering-from-scratch/phases/XX-nombre/YY-leccion/docs/en.md`
2. Explicar en español, hacer ejercicios prácticos
3. Si hay `quiz.json`, administrar el quiz al final
4. Actualizar `progreso/.../notas.md` y `README.md`
5. Commit + push al terminar
