# API Troubleshooter

Prompt para diagnosticar errores comunes al llamar APIs de LLMs.

## Prompt

```
Recibí este error al hacer una llamada a la API de [Anthropic/OpenAI]:

<error>
[pega el error aquí]
</error>

Mi código es:
<code>
[pega el código relevante]
</code>

Diagnóstica el problema y dame los pasos exactos para resolverlo.
```

## Errores comunes y causas

| Error | Causa probable |
|-------|---------------|
| `401 Unauthorized` | API key incorrecta o no configurada |
| `429 Too Many Requests` | Rate limit alcanzado — espera y reintenta |
| `400 Bad Request` | Parámetro inválido (model, max_tokens, formato de messages) |
| `529 Overloaded` | Servidor de la API saturado — reintenta con backoff |
| `KeyError: ANTHROPIC_API_KEY` | Variable de entorno no cargada (falta `load_dotenv()`) |

## Checklist de debug

1. ¿El archivo `.env` existe en la raíz del proyecto?
2. ¿Llamaste `load_dotenv()` antes de `os.environ[...]`?
3. ¿El nombre del modelo es exacto? (ej: `claude-haiku-4-5-20251001`)
4. ¿`messages` es una lista de dicts con `role` y `content`?
5. ¿`max_tokens` está especificado?
