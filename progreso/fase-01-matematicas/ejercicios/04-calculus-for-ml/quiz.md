# Quiz — L04 Calculus for ML

## Pre-quiz — 2/3

### P1
**Pregunta:** ¿Qué representa la derivada de una función en un punto?
**Opciones:**
- A) La pendiente de la tangente a la curva en ese punto ← **elegida**
- B) El valor de la función en ese punto
- C) El área bajo la curva hasta ese punto

**Correcto:** ✅ Sí — $f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}$ es exactamente la pendiente de la recta tangente en $x$.

---

### P2
**Pregunta:** Si el learning rate ($\alpha$) en el descenso de gradiente es demasiado grande, ¿qué puede ocurrir?
**Opciones:**
- A) El entrenamiento puede diverger / oscilar ← **elegida**
- B) El entrenamiento converge más rápido sin riesgos
- C) El gradiente se vuelve cero inmediatamente

**Correcto:** ✅ Sí — pasos demasiado grandes sobrepasan el mínimo repetidamente; la pérdida puede oscilar o crecer sin control.

---

### P3
**Pregunta:** Si la matriz Hessiana de una función en un punto crítico tiene autovalores 3 y -1, ¿qué tipo de punto es?
**Opciones:**
- A) Un mínimo local
- B) Un máximo local
- C) Un punto de silla
- D) No se puede determinar ← **elegida**

**Correcto:** ❌ No — la respuesta correcta es **C) Un punto de silla**. Autovalores con signos mixtos (uno positivo, uno negativo) significan que la función sube en una dirección y baja en otra: Hessiana indefinida → punto de silla. Sí se puede determinar a partir de los signos de los autovalores.

---

## Post-quiz — 4/4

### P1
**Pregunta:** Si la matriz Hessiana de una función en un punto crítico tiene autovalores 5 y -3, ¿qué tipo de punto es?
**Opciones:**
- A) Mínimo local
- B) Máximo local
- C) Punto de silla ← **elegida**
- D) No se puede determinar

**Correcto:** ✅ Sí — autovalores con signos mixtos → Hessiana indefinida → punto de silla, sin importar los valores exactos. Concepto reforzado en el Paso 6 (`hessiana.py`): silla $\to$ autovalores 2 y -2; cuenco $\to$ autovalores 2 y 2.

---

### P2
**Pregunta:** En backpropagation, ¿cómo se calcula el gradiente de la pérdida respecto a un peso ubicado varias capas atrás en la red?
**Opciones:**
- A) Multiplicando las derivadas locales a lo largo del camino desde la pérdida hasta ese peso (regla de la cadena) ← **elegida**
- B) Sumando todos los gradientes de la red
- C) Calculando una derivada directa, sin pasos intermedios
- D) Usando solo la matriz Hessiana

**Correcto:** ✅ Sí — el gradiente es el producto de las derivadas locales en cada arista del grafo de cómputo, desde la salida hasta el parámetro. Cuando los caminos se bifurcan y se unen, las contribuciones se suman (regla de la cadena multivariable).

---

### P3
**Pregunta:** ¿Qué hace el término de 'momentum' en el descenso de gradiente?
**Opciones:**
- A) Acumula gradientes pasados como "velocidad" ← **elegida**
- B) Reduce los pesos a cero gradualmente
- C) Calcula la segunda derivada exacta
- D) Reemplaza completamente el gradiente actual

**Correcto:** ✅ Sí — $v_{\text{nuevo}} = \beta v + \nabla f$, luego $x_{\text{nuevo}} = x - \alpha v$. Vimos en el Ejercicio 3 cómo esto produce overshoot y oscilación alrededor del mínimo de $f(x)=x^4-3x^2$, a diferencia de la convergencia monótona sin momentum.

---

### P4
**Pregunta:** La actualización $w_{\text{nuevo}} = w_{\text{viejo}} - \alpha \cdot \frac{\partial L}{\partial w}$ (descenso de gradiente estándar) corresponde a aproximar la función con Taylor de:
**Opciones:**
- A) Primer orden (lineal) ← **elegida**
- B) Segundo orden (cuadrático)
- C) Orden cero (constante)
- D) No tiene relación con Taylor

**Correcto:** ✅ Sí — $f(x+h) \approx f(x) + f'(x)h$ es la aproximación lineal (orden 1); minimizarla da el paso del descenso de gradiente. El orden 2 (con la Hessiana) corresponde al método de Newton.

---

**Resultado final: pre 2/3 · post 4/4** ✅ (el concepto de Hessiana/punto de silla, fallado en el pre-quiz, quedó dominado en el post-quiz tras el Paso 6)
