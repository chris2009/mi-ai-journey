# fase-01-matematicas

## Resumen

### L01 — Linear Algebra Intuition ✅

Los vectores son puntos/direcciones en el espacio; las matrices son transformaciones que mueven esos puntos. El producto punto mide similitud (la base de búsqueda semántica, RAG y attention). La independencia lineal y el rango determinan si un sistema de ecuaciones tiene solución única o si hay redundancia (features correlacionados → matriz mal condicionada). La proyección extrae la componente de un vector en una dirección dada — es el corazón de la regresión lineal, PCA y attention. Gram-Schmidt convierte vectores independientes en una base ortonormal (lo que hace `np.linalg.qr` internamente).

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

**Insight clave:** proyectar sobre $[1,1,\ldots,1]$ extrae el promedio de las componentes — es la base de centrar datos antes de PCA y de por qué la media es la "mejor aproximación constante" en mínimos cuadrados.

## Ejercicios completados

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | `angle_between` entre vectores | 90°, 45°, 0° — correcto en los 3 casos |
| 2 | Matriz de escalado $\begin{pmatrix}2&0\\0&3\end{pmatrix}$ aplicada a $[1,1]$ | $[1,1] \to [2,3]$ |
| 3 | Cosine similarity entre 5 embeddings aleatorios (dim 50) | par más similar: `word_2` y `word_3` (0.3000) |
| 4 | Verificar ortonormalidad de Gram-Schmidt (vía QR) | productos punto $\approx 10^{-16}$, normas $= 1.0000$ |
| 5 | Matriz $3\times3$ de rango 2 | rango verificado = 2; columnas abarcan un plano (no todo $\mathbb{R}^3$) |
| 6 | Proyección de $[1,2,3]$ sobre $[1,1,1]$ | $[2,2,2]$ — el promedio repetido |

**Quiz: pre 2/3 · post 3/3** ✅ (mejora notable en el concepto de rango/LoRA, fallado en pre-quiz y dominado en post-quiz)

## Dudas y pendientes

- Ninguna pendiente — L01 completada. Diferenciar advertencias del *type checker* (Pylance) de errores reales en tiempo de ejecución quedó claro tras el caso de `most_similar_pair` en el ejercicio 3.
