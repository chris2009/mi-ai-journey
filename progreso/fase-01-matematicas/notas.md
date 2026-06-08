# fase-01-matematicas

## Resumen

### L01 — Linear Algebra Intuition ✅

Los vectores son puntos/direcciones en el espacio; las matrices son transformaciones que mueven esos puntos. El producto punto mide similitud (la base de búsqueda semántica, RAG y attention). La independencia lineal y el rango determinan si un sistema de ecuaciones tiene solución única o si hay redundancia (features correlacionados → matriz mal condicionada). La proyección extrae la componente de un vector en una dirección dada — es el corazón de la regresión lineal, PCA y attention. Gram-Schmidt convierte vectores independientes en una base ortonormal (lo que hace `np.linalg.qr` internamente).

### L02 — Vectors, Matrices & Operations ✅

La multiplicación matricial $(m \times n) @ (n \times p) = (m \times p)$ es la operación central de toda red neuronal: cada capa densa es $\text{output} = \text{relu}(W \mathbin{@} x + b)$. Es muy distinta de la multiplicación elemento a elemento (misma forma, combina posiciones 1 a 1) — confundirlas es el error más común de los principiantes. El determinante mide cuánto escala una transformación un área/volumen: si es cero, la matriz colapsa una dimensión y pierde información de forma irreversible, por lo que no tiene inversa (es singular). El broadcasting permite sumar arreglos de formas distintas estirando el más pequeño — así es como se suma el bias en cada framework. Construir una red de dos capas a mano deja ver la "sparsity" de ReLU: en cada forward pass, solo un subconjunto de neuronas queda activo (el resto se apaga a cero).

## Conceptos clave

| Concepto | Idea central | Conexión con AI |
|----------|-------------|-----------------|
| Vector | Punto/dirección en espacio n-dimensional | Embeddings (palabra, imagen, usuario) |
| Matriz | Transformación lineal entre espacios | Pesos de redes neuronales, attention |
| Producto punto | $a \cdot b = \sum a_i b_i$ — mide alineación | Cosine similarity, búsqueda RAG, attention scores |
| Independencia lineal | Ningún vector es combinación de los demás | Evitar multicolinealidad en features |
| Rango | # de columnas/filas independientes | LoRA (actualizaciones de bajo rango), condición del sistema |
| Proyección | $\text{proj}_\mathbf{b}(\mathbf{a}) = \frac{\mathbf{a}\cdot\mathbf{b}}{\mathbf{b}\cdot\mathbf{b}}\mathbf{b}$ | Regresión lineal, PCA, reducción de dimensionalidad |
| Gram-Schmidt / QR | Construye una base ortonormal | Solvers numéricos estables, cómputo de autovalores |
| Multiplicación matricial | $(m\times n) @ (n\times p) = (m\times p)$ — productos punto fila×columna | Forward pass de cada capa de red neuronal |
| Determinante | Mide el escalado de área/volumen; cero = colapsa una dimensión | Verificar si una matriz es invertible (singularidad) |
| Inversa | $A^{-1} = \frac{1}{\det(A)}\text{adj}(A)$ — deshace una transformación | Resolver sistemas lineales; solo existe si $\det(A) \neq 0$ |
| Broadcasting | Estira el arreglo más pequeño para que encaje con el más grande | Suma de bias en cada framework de redes neuronales |

**Insight clave (L01):** proyectar sobre $[1,1,\ldots,1]$ extrae el promedio de las componentes — es la base de centrar datos antes de PCA y de por qué la media es la "mejor aproximación constante" en mínimos cuadrados.

**Insight clave (L02):** una matriz singular ($\det = 0$) colapsa el espacio en una dimensión menor — pierde información de forma irreversible, así que no existe transformación que la "deshaga". Esa es la misma idea del rango deficiente de L01, vista ahora desde el determinante.

## Ejercicios completados

### L01 — Linear Algebra Intuition

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | `angle_between` entre vectores | 90°, 45°, 0° — correcto en los 3 casos |
| 2 | Matriz de escalado $\begin{pmatrix}2&0\\0&3\end{pmatrix}$ aplicada a $[1,1]$ | $[1,1] \to [2,3]$ |
| 3 | Cosine similarity entre 5 embeddings aleatorios (dim 50) | par más similar: `word_2` y `word_3` (0.3000) |
| 4 | Verificar ortonormalidad de Gram-Schmidt (vía QR) | productos punto $\approx 10^{-16}$, normas $= 1.0000$ |
| 5 | Matriz $3\times3$ de rango 2 | rango verificado = 2; columnas abarcan un plano (no todo $\mathbb{R}^3$) |
| 6 | Proyección de $[1,2,3]$ sobre $[1,1,1]$ | $[2,2,2]$ — el promedio repetido |

**Quiz L01: pre 2/3 · post 3/3** ✅

### L02 — Vectors, Matrices & Operations

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | Verificar $A \mathbin{@} A^{-1} = I$ con 3 matrices $2\times2$ + caso singular | identidad confirmada en los 3 casos; matriz singular lanza `ValueError` correctamente |
| 2 | Inversa $3\times3$ por método de la adjunta (cofactores) | coincide exactamente con `np.linalg.inv` |
| 3 | Red de dos capas (3 → 4 → 2) solo con clase `Matrix` | shapes correctas en cada paso; `hidden = [0, 0, 0, 0.745]` ilustra sparsity de ReLU |

**Quiz L02: pre 3/3 · post 3/3** ✅ (dominó los conceptos desde el pre-quiz)

## Dudas y pendientes

- Ninguna pendiente. L01 y L02 completadas. De L01: diferenciar advertencias del *type checker* (Pylance) de errores reales en tiempo de ejecución quedó claro tras el caso de `most_similar_pair`. De L02: quedó clara la conexión entre determinante cero, rango deficiente (L01) y pérdida irreversible de información en una transformación.
