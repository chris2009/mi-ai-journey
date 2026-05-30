# 🤖 AI Engineering from Scratch — Guía en Español

> **Repo:** https://github.com/rohitg00/ai-engineering-from-scratch  
> **Licencia:** MIT (gratis, úsalo como quieras)  
> **Nivel:** Intermedio (necesitas saber programar, no necesitas saber IA)

---

## ¿Qué es esto en una línea?

Un **curso completo y gratuito de IA** con más de 230 lecciones prácticas, donde en cada lección construyes algo real que puedes reutilizar después.

---

## ¿Qué lo hace diferente a otros cursos?

| Otros cursos | Este curso |
|---|---|
| Solo Python | Python, TypeScript, Rust y Julia |
| "Aprendí algo" | Terminas con un portafolio de herramientas reales |
| Un solo tema (solo NLP, o solo visión) | Todo: matemáticas, ML, DL, LLMs, agentes, enjambres |
| Videos o documentación | Código ejecutable + notebooks + docs |

---

## ¿Qué vas a construir al final?

Al terminar el curso tendrás una carpeta `outputs/` con:

```
outputs/
├── prompts/       → Plantillas de prompts para tareas de IA
├── skills/        → Archivos SKILL.md para agentes de código como Claude Code
├── agents/        → Definiciones de agentes listos para desplegar
└── mcp-servers/   → Servidores MCP que construiste durante el curso
```

Todas estas herramientas son reales e instalables en Claude Code, Cursor u otros agentes.

---

## Las 20 Fases del Curso

| Fase | Tema | Lecciones |
|------|------|-----------|
| 0 | Configuración del entorno (Dev, Git, GPU, Docker) | 12 |
| 1 | Matemáticas (álgebra lineal, cálculo, probabilidad) | 22 |
| 2 | Machine Learning clásico (regresión, árboles, SVM) | 18 |
| 3 | Deep Learning desde cero (redes neuronales, backprop) | 13 |
| 4 | Visión por Computadora (CNN, YOLO, difusión) | 16 |
| 5 | NLP de básico a avanzado (embeddings, atención) | 18 |
| 6 | Audio y Voz (ASR, TTS, Whisper, clon de voz) | 12 |
| 7 | Transformers a fondo (BERT, GPT, ViT) | 14 |
| 8 | IA Generativa (GANs, Diffusion, Stable Diffusion) | 14 |
| 9 | Aprendizaje por Refuerzo (RL, PPO, RLHF) | 12 |
| 10 | LLMs desde cero (tokenizers, pretraining, fine-tuning) | 14 |
| 11 | Ingeniería de LLMs (RAG, LoRA, function calling) | 13 |
| 12 | IA Multimodal (CLIP, video+lenguaje) | 11 |
| 13 | Herramientas y Protocolos (MCP, Tool Use) | 10 |
| 14 | Agentes de IA (loops, memoria, planificación) | 15 |
| 15 | Sistemas Autónomos (auto-healing, monitoreo) | 11 |
| 16 | Multi-Agente y Enjambres (swarms, coordinación) | 14 |
| 17 | Infraestructura y Producción (Docker, K8s, edge) | 11 |
| 18 | Ética, Seguridad y Alineamiento | 6 |
| 19 | Proyectos Capstone (mini GPT, RAG, agente autónomo) | 5 |

---

## ¿Cómo funciona cada lección?

Cada lección sigue estos 6 pasos:

1. **Motto** — La idea central en una línea
2. **Problem** — Por qué esto importa
3. **Concept** — Diagramas visuales e intuición
4. **Build It** — Lo implementas desde cero
5. **Use It** — Lo mismo pero con frameworks reales
6. **Ship It** — El prompt, skill o agente que produce esta lección

Y cada lección tiene esta estructura de archivos:

```
phases/XX-nombre-fase/NN-nombre-leccion/
├── code/        → Implementaciones ejecutables
├── notebook/    → Jupyter notebooks para experimentar
├── docs/
│   └── en.md    → Documentación de la lección
└── outputs/     → Prompts, skills, agentes generados
```

---

## Guía de Inicio Rápido

### Requisitos

- Saber programar en Python (u otro lenguaje)
- Ganas de entender cómo funciona la IA de verdad
- Git instalado
- Python 3.8+

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/rohitg00/ai-engineering-from-scratch.git
cd ai-engineering-from-scratch
```

### Paso 2 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3 — Verificar tu entorno

```bash
python phases/00-setup-and-tooling/01-dev-environment/code/verify.py
```

### Paso 4 — Empezar la primera lección real

```bash
python phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py
```

### Paso 5 — Seguir el orden recomendado

Sigue las fases en orden (0 → 1 → 2 → ... → 19). No saltes a las fases avanzadas sin las bases: el curso está diseñado para que cada fase construya sobre la anterior.

---

## Rutas de Aprendizaje Sugeridas

### 🚀 Ruta Rápida — Solo LLMs y Agentes (2-3 meses)
```
Fase 0 → Fase 1 (parcial) → Fase 10 → Fase 11 → Fase 13 → Fase 14
```

### 🧠 Ruta Completa — Ingeniero de IA (6-12 meses)
```
Fases 0 → 1 → 2 → 3 → 7 → 10 → 11 → 14 → 19
```

### 👁️ Ruta Visión + Generativa (3-4 meses)
```
Fase 0 → Fase 1 → Fase 3 → Fase 4 → Fase 7 → Fase 8
```

### 🤖 Ruta Multi-Agente (avanzado)
```
Fases 0, 1, 11, 13, 14, 15, 16
```

---

## Lenguajes que se usan

- **Python** — 92% del curso (principal)
- **Julia** — Para matemáticas y álgebra lineal
- **TypeScript** — Para agentes y herramientas MCP
- **Rust** — Para partes de alto rendimiento (inferencia, audio en tiempo real)

---

## Cómo Contribuir

- Agrega lecciones nuevas → ver `CONTRIBUTING.md`
- Traduce lecciones a español u otros idiomas
- Agrega outputs (prompts, skills, agentes) a lecciones existentes
- Haz fork para tu equipo o escuela → ver `FORKING.md`

---

## Recursos Útiles del Repo

| Archivo | ¿Para qué? |
|---------|-----------|
| `README.md` | Visión general y tabla completa de lecciones |
| `ROADMAP.md` | Seguimiento del progreso del curso |
| `CONTRIBUTING.md` | Cómo contribuir lecciones |
| `FORKING.md` | Cómo hacer fork para tu organización |
| `LESSON_TEMPLATE.md` | Plantilla para crear nuevas lecciones |
| `glossary/terms.md` | Glosario de términos de IA |
| `requirements.txt` | Dependencias Python del curso |

---

## En Resumen

Este repo es básicamente una **universidad de IA gratuita y de código abierto**. No te enseña a *usar* herramientas de IA — te enseña a *construirlas desde cero*. Al terminar no solo sabes cómo funciona la IA, sino que tienes un portafolio real de prompts, agentes y servidores MCP que puedes instalar en Claude Code o cualquier otro agente.

**Lo único que necesitas es saber programar y tener disposición para aprender.**
