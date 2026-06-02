# L04 — APIs y Claves

> Cada API de AI funciona igual: envías una solicitud, recibes una respuesta. Los detalles cambian, el patrón no.

**Tipo:** Build  
**Lenguajes:** Python, TypeScript  
**Prerequisitos:** Fase 0, Lección 01  
**Tiempo:** ~30 minutos

---

## Objetivos de aprendizaje

- Almacenar API keys de forma segura usando variables de entorno y archivos `.env`
- Hacer una llamada a la API de LLM usando el SDK de Python de Anthropic y HTTP crudo
- Comparar los formatos de solicitud/respuesta del SDK vs HTTP para debugging
- Identificar y manejar errores comunes de API: autenticación y rate limits

---

## El problema

A partir de la Fase 11 llamarás a APIs de LLM (Anthropic, OpenAI, Google). En las fases 13-16 construirás agentes que usan estas APIs en bucles. Necesitas entender cómo funcionan las API keys, cómo almacenarlas de forma segura y cómo hacer tu primera llamada.

---

## El concepto

```
Tu código → HTTP POST [URL + API key + body JSON] → Servidor API
          ← JSON response ←
```

Cada llamada a la API tiene:
1. Un endpoint (URL)
2. Una API key (autenticación)
3. Un cuerpo de solicitud (lo que quieres)
4. Un cuerpo de respuesta (lo que recibes)

---

## Paso a paso

### Paso 1: Almacenar API keys de forma segura

**Nunca pongas API keys en el código.** Usa variables de entorno o archivos `.env`.

```bash
# Opción 1: variable de entorno en la sesión
export ANTHROPIC_API_KEY="sk-ant-..."
```

```bash
# Opción 2: archivo .env (agregar a .gitignore)
# Archivo: .env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

```python
# Cargar en Python con python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # carga .env
key = os.environ["ANTHROPIC_API_KEY"]
```

### Paso 2: Primera llamada a la API (Python SDK)

```python
import anthropic

client = anthropic.Anthropic()  # toma la key de ANTHROPIC_API_KEY automáticamente

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[{"role": "user", "content": "¿Qué es una red neuronal en una oración?"}]
)

print(response.content[0].text)
print(f"Tokens usados: input={response.usage.input_tokens}, output={response.usage.output_tokens}")
```

### Paso 3: HTTP crudo (sin SDK)

Esto es lo que el SDK hace por debajo. Útil para debuggear:

```python
import os
import urllib.request
import json

url = "https://api.anthropic.com/v1/messages"
headers = {
    "Content-Type": "application/json",
    "x-api-key": os.environ["ANTHROPIC_API_KEY"],
    "anthropic-version": "2023-06-01",
}
body = json.dumps({
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "¿Qué es una red neuronal en una oración?"}],
}).encode()

req = urllib.request.Request(url, data=body, headers=headers, method="POST")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print(result["content"][0]["text"])
```

### Campos clave en la respuesta JSON

| Campo | Descripción |
|-------|-------------|
| `content[0].text` | Texto de respuesta del modelo |
| `usage.input_tokens` | Tokens enviados (se cobran) |
| `usage.output_tokens` | Tokens recibidos (se cobran) |
| `stop_reason: "end_turn"` | El modelo terminó normalmente |

---

## APIs en este curso

| API | Cuándo la necesitas | Tier gratuito |
|-----|---------------------|---------------|
| Anthropic (Claude) | Fases 11-16 (agentes, herramientas) | $5 crédito al registrarse |
| OpenAI | Fase 11 (comparación) | $5 crédito al registrarse |
| Hugging Face | Fases 4-10 (modelos, datasets) | Gratis |

---

## Ejercicios

1. Consigue una API key de Anthropic y haz tu primera llamada a la API
2. Prueba la versión HTTP cruda y compara el formato de respuesta con el del SDK
3. Usa intencionalmente una API key incorrecta y lee el mensaje de error

---

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|---------|---------------------|--------------------------|
| API key | "Contraseña de la API" | String único que identifica tu cuenta y autoriza requests |
| Rate limit | "Me están limitando" | Máximo de requests por minuto/hora para prevenir abuso |
| Token | "Una palabra" (en contexto API) | Unidad de facturación: tokens de entrada y salida se cobran por separado |
| Streaming | "Respuestas en tiempo real" | Recibir la respuesta palabra por palabra en vez de esperar la respuesta completa |
