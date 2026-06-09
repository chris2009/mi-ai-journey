# Quiz — L04 APIs & Keys

> Nota: preguntas reconstruidas desde sesión compactada. No se encontró score de quiz separado en notas.md para esta lección.

## Quiz — score no registrado explícitamente

### P1
**Pregunta:** ¿Por qué nunca debes poner una API key directamente en el código?
**Respuesta elegida:** Porque el código va a git — si se hace push accidentalmente, la key queda expuesta en el historial público de forma permanente ✅
**Correcto:** Sí — siempre usar `.env` + `python-dotenv`, con `.env` en `.gitignore`.

---

### P2
**Pregunta:** En la respuesta JSON de la API de Anthropic, ¿qué campo contiene el texto generado?
**Respuesta elegida:** `content[0].text` ✅
**Correcto:** Sí — la respuesta tiene estructura: `response.content[0].text` para el texto, `response.usage.input_tokens` / `output_tokens` para facturación.

---

### P3
**Pregunta:** ¿Qué diferencia hay entre usar el SDK de Anthropic y hacer HTTP directo?
**Respuesta elegida:** El SDK simplifica headers, serialización JSON y manejo de errores — pero internamente es solo HTTP POST ✅
**Correcto:** Sí — el SDK es una capa de conveniencia; el protocolo subyacente es idéntico.

---

**Output generado:** `outputs/prompts/api-troubleshooter.md`
