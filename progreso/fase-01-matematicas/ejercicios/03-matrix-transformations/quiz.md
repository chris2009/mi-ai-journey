# Quiz — L03 Matrix Transformations

## Pre-quiz — 3/3

### P1
**Pregunta:** Si compones dos transformaciones como `result = B @ A @ point`, ¿qué transformación se aplica primero al punto?
**Opciones:**
- A) A se aplica primero, luego B ← **elegida**
- B) B se aplica primero, luego A
- C) Da igual, el resultado es el mismo

**Correcto:** ✅ Sí — la matriz más cercana al vector (a la derecha) actúa primero; su resultado entra a la siguiente hacia la izquierda.

---

### P2
**Pregunta:** ¿Qué hace especial a un autovector (eigenvector) de una matriz A?
**Opciones:**
- A) La matriz solo lo escala, nunca cambia su dirección ← **elegida**
- B) La matriz lo rota pero preserva su magnitud
- C) Es el vector con la mayor magnitud después de la transformación

**Correcto:** ✅ Sí — $A @ v = \lambda v$: el vector resultante apunta en la misma dirección, solo cambia su magnitud por el factor $\lambda$.

---

### P3
**Pregunta:** Una matriz de transformación tiene determinante = -1. ¿Qué le hace al espacio?
**Opciones:**
- A) Preserva el área pero invierte la orientación (reflexión) ← **elegida**
- B) Colapsa el espacio en una dimensión menor
- C) Duplica el área de cualquier figura

**Correcto:** ✅ Sí — valor absoluto 1 = área conservada; signo negativo = orientación invertida. Firma de una reflexión.

---

## Post-quiz — 3/3

### P1
**Pregunta:** Tienes una matriz de transformación con det = 0. ¿Qué le ocurre al círculo unitario si la aplicas?
**Opciones:**
- A) El círculo se aplasta a una línea (o un punto) — la transformación es irreversible ← **elegida**
- B) El círculo se deforma en una elipse — la transformación estira más en una dirección
- C) El círculo se refleja — la orientación queda invertida pero la forma se conserva

**Correcto:** ✅ Sí — det = 0 colapsa una dimensión: el espacio 2D se aplasta sobre una línea (rango 1) o un punto (rango 0). Sin inversa posible.

---

### P2
**Pregunta:** En PCA, los autovectores de la matriz de covarianza indican las direcciones de las componentes principales. ¿Qué indica el autovalor correspondiente?
**Opciones:**
- A) Cuánta varianza de los datos captura esa componente ← **elegida**
- B) El número de muestras que caen sobre esa dirección
- C) El ángulo de rotación que se necesita para alinear los datos en esa dirección

**Correcto:** ✅ Sí — el autovalor mide cuánto escala la matriz en esa dirección; en la covarianza, eso equivale a la varianza proyectada sobre esa componente.

---

### P3
**Pregunta:** Compones rotación R y escalado S. ¿Por qué S @ R y R @ S dan resultados distintos?
**Opciones:**
- A) Porque la rotación y el escalado afectan ejes distintos; aplicarlos en distinto orden produce trayectorias diferentes para los puntos ← **elegida**
- B) Porque la rotación es una operación más costosa y siempre debe ir última
- C) No dan resultados distintos si los ángulos y factores son pequeños

**Correcto:** ✅ Sí — escalar primero alarga los ejes antes de rotar; rotar primero mueve los puntos antes de que el escalado los estire en las nuevas posiciones. La no-conmutatividad es algebraica, no depende de la magnitud.

---

**Resultado final: pre 3/3 · post 3/3** ✅
