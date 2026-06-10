# fase-01-matematicas

## Resumen

### L01 — Linear Algebra Intuition ✅

Los vectores son puntos/direcciones en el espacio; las matrices son transformaciones que mueven esos puntos. El producto punto mide similitud (la base de búsqueda semántica, RAG y attention). La independencia lineal y el rango determinan si un sistema de ecuaciones tiene solución única o si hay redundancia (features correlacionados → matriz mal condicionada). La proyección extrae la componente de un vector en una dirección dada — es el corazón de la regresión lineal, PCA y attention. Gram-Schmidt convierte vectores independientes en una base ortonormal (lo que hace `np.linalg.qr` internamente).

### L03 — Matrix Transformations ✅

Cada matriz $2\times2$ es una máquina espacial: rotación (preserva distancias y ángulos, $|\det|=1$), escalado (estira/comprime ejes, $\det = s_x \cdot s_y$), cizallamiento (inclina ejes, $\det = 1$) y reflexión (invierte orientación, $\det = -1$). Al componer transformaciones, el orden importa: $S @ R \neq R @ S$. Los autovectores son las direcciones que la matriz solo escala — $A @ v = \lambda v$; los autovalores dicen cuánto. La ecuación característica $\det(A - \lambda I) = 0$ los produce. Esta es la matemática detrás de PCA (autovectores de la covarianza), estabilidad de RNNs (autovalores con $|\lambda| < 1$) y clustering espectral. La propiedad $\det(ABC) = \det(A)\cdot\det(B)\cdot\det(C)$ conecta composición con escalado de área.

### L02 — Vectors, Matrices & Operations ✅

La multiplicación matricial $(m \times n) @ (n \times p) = (m \times p)$ es la operación central de toda red neuronal: cada capa densa es $\text{output} = \text{relu}(W \mathbin{@} x + b)$. Es muy distinta de la multiplicación elemento a elemento (misma forma, combina posiciones 1 a 1) — confundirlas es el error más común de los principiantes. El determinante mide cuánto escala una transformación un área/volumen: si es cero, la matriz colapsa una dimensión y pierde información de forma irreversible, por lo que no tiene inversa (es singular). El broadcasting permite sumar arreglos de formas distintas estirando el más pequeño — así es como se suma el bias en cada framework. Construir una red de dos capas a mano deja ver la "sparsity" de ReLU: en cada forward pass, solo un subconjunto de neuronas queda activo (el resto se apaga a cero).

### L04 — Calculus for ML ✅

La derivada $f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$ mide la pendiente/tasa de cambio en un punto; el gradiente $\nabla f=[\partial f/\partial x_1,\ldots,\partial f/\partial x_n]$ generaliza esto a varias variables y apunta en la dirección de mayor ascenso. El descenso de gradiente $w_{\text{nuevo}}=w_{\text{viejo}}-\alpha\cdot\nabla f$ es la regla de actualización detrás de todo entrenamiento de redes neuronales: un learning rate $\alpha$ muy grande hace diverger/oscilar el entrenamiento, uno muy pequeño converge demasiado lento. La Hessiana (matriz de segundas derivadas parciales) revela la curvatura de la función: autovalores del mismo signo → mínimo o máximo local; signos mixtos → punto de silla. La serie de Taylor conecta ambos métodos de optimización: la aproximación de orden 1 ($f(x+h)\approx f(x)+f'(x)h$) es exactamente el descenso de gradiente, y la de orden 2 (que añade $\frac{1}{2}f''(x)h^2$, usando la Hessiana) es el método de Newton. La regla de la cadena multivariable, aplicada sistemáticamente a través de un grafo de cómputo de adelante hacia atrás, es exactamente backpropagation.

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
| Rotación | Matriz ortogonal; $\det = 1$ siempre | Data augmentation (rotar imágenes), transformaciones 3D |
| Escalado | Matriz diagonal $\text{diag}(s_x, s_y)$; $\det = s_x s_y$ | Normalización de features, zoom en imágenes |
| Cizallamiento | Inclina un eje; $\det = 1$ | Data augmentation, perspectiva |
| Autovector/autovalor | $A @ v = \lambda v$ — dirección que la matriz solo escala | PCA (componentes principales), estabilidad de RNNs, spectral clustering |
| Ecuación característica | $\det(A - \lambda I) = 0$ — polinomio cuyas raíces son los autovalores | Encontrar autovalores de cualquier matriz cuadrada |
| Eigendecomposición | $A = V @ D @ V^{-1}$ — separa la matriz en sus escalados fundamentales | Análisis de redes neuronales, compresión matricial |
| Derivada | $f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$ — pendiente/tasa de cambio | Base de todo entrenamiento por gradientes |
| Derivada numérica | $\frac{f(x+h)-f(x-h)}{2h}$ — diferencia central, sin fórmula analítica | Verificar gradientes (`gradcheck` en PyTorch) |
| Gradiente | $\nabla f=[\partial f/\partial x_1,\ldots]$ — dirección de máximo ascenso | Dirección de actualización en cada paso de entrenamiento |
| Descenso de gradiente | $w_{\text{nuevo}}=w_{\text{viejo}}-\alpha\nabla f$ | Algoritmo central de optimización en deep learning |
| Learning rate | Escala el tamaño del paso $\alpha$ | Muy alto → diverge/oscila; muy bajo → converge lento |
| Regla de la cadena | $\frac{dy}{dx}=f'(g(x))\cdot g'(x)$ | Base matemática de backpropagation |
| Hessiana | Matriz de segundas derivadas parciales; sus autovalores describen curvatura | Mínimo (autovalores +), máximo (autovalores -), silla (signos mixtos) |
| Serie de Taylor | $f(x+h)\approx f(x)+f'(x)h+\frac{1}{2}f''(x)h^2+\ldots$ | Orden 1 = descenso de gradiente; orden 2 = método de Newton |
| Jacobiano | Matriz de derivadas de una función vectorial $\mathbb{R}^n\to\mathbb{R}^m$ | Forma en que fluyen los gradientes entre capas |
| Momentum | Velocidad que acumula gradientes pasados: $v\leftarrow\beta v+\nabla f$, $w\leftarrow w-\alpha v$ | Acelera convergencia; base de SGD+momentum y Adam |

**Insight clave (L01):** proyectar sobre $[1,1,\ldots,1]$ extrae el promedio de las componentes — es la base de centrar datos antes de PCA y de por qué la media es la "mejor aproximación constante" en mínimos cuadrados.

**Insight clave (L02):** una matriz singular ($\det = 0$) colapsa el espacio en una dimensión menor — pierde información de forma irreversible, así que no existe transformación que la "deshaga". Esa es la misma idea del rango deficiente de L01, vista ahora desde el determinante.

**Insight clave (L03):** $\det(ABC) = \det(A)\cdot\det(B)\cdot\det(C)$ — solo el escalado cambia el área; rotación y cizallamiento la preservan. Aplicar una composición de transformaciones a un círculo convierte el círculo en una elipse inclinada, y la simetría central siempre se conserva en transformaciones lineales.

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

### L03 — Matrix Transformations

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | Rotación 45°, escalado $(2, 0.5)$ y cizallamiento $k_x=1$ sobre cuadrado unitario + verificar distancias | distancias A-B y B-C: $1.0 \to 1.0$ tras rotar — isometría confirmada |
| 2 | Autovalores de $\begin{pmatrix}4&2\\1&3\end{pmatrix}$ a mano + función propia + NumPy | $\lambda = 5$ y $\lambda = 2$; autovectores coinciden (salvo signo) entre función propia y NumPy |
| 3 | Composición $(R_{30°} \to S_{1.5,0.8} \to Sh_{0.3})$ sobre 8 puntos en círculo + verificar $\det$ | $\det(\text{compuesta}) = 1.2 = 1.0 \times 1.2 \times 1.0$ ✓; círculo → elipse inclinada |

**Quiz L03: pre 3/3 · post 3/3** ✅

### L04 — Calculus for ML

| # | Ejercicio | Resultado |
|---|-----------|-----------|
| 1 | Derivada numérica de $x^2$ en $x\in\{-2,-1,0,1,2\}$ | numérica = analítica = $2x$ en los 5 casos |
| 2 | Gradiente numérico de $f(x,y)=x^2+3xy+y^2$ en $(1,2)$ | $[8.0000, 7.0000]$ — coincide con el analítico $[2x+3y,\,3x+2y]=[8,7]$ |
| 3 | Descenso de gradiente 1D en $f(x)=x^2$ desde $x=5$ | converge geométricamente a 0 (factor $0.8$ por paso, $\alpha=0.1$) |
| 4 | Descenso de gradiente 2D en $f(x,y)=x^2+y^2$ desde $(4,3)$ | $(4,3)\to(0.0050, 0.0037)$ en 30 pasos, $f\to3.8\times10^{-5}$ |
| 5 | Comparación numérica vs analítica: $x^2,x^3,\sin(x),e^x,1/x$ en $x=2$ | error $\sim10^{-9}$–$10^{-10}$ en todas |
| 6 | Hessiana numérica: silla $f=x^2-y^2$ vs cuenco $f=x^2+y^2$ en $(0,0)$ | silla → $[[2,0],[0,-2]]$ (signos mixtos = punto de silla); cuenco → $[[2,0],[0,2]]$ (ambos +, mínimo) |
| 7 | Aproximación de Taylor de $\sin(h)$ para $h\in\{0.1,0.5,1,2\}$ | orden1 = orden2 = $h$ (porque $f''(0)=0$); el error vs. $\sin(h)$ crece con $h$ |
| 8 | Regresión lineal manual (descenso de gradiente sobre $y=2x+1$, 200 épocas) | $w\to2.08$, $b\to0.73$; pérdida $67.03\to0.0137$ |
| 9 | Misma regresión con NumPy vectorizado | $y\approx2.09x+0.66$ |
| Ej.1 | `numerical_second_derivative` de $x^3$ en $x=2$ | $f''(2)=12.000000$ = analítica ($6x$) |
| Ej.2 | Descenso de gradiente para $f(x,y)=(x-3)^2+(y+1)^2$ desde $(0,0)$ | converge exactamente a $(3.0000, -1.0000)$ |
| Ej.3 | Momentum vs. sin momentum en $f(x)=x^4-3x^2$ desde $x=0.5$ | sin momentum: convergencia monótona a $1.2247$; con momentum ($\beta=0.9$): overshoot a $1.4458$ y oscilación antes de asentarse; ambos $f\to-2.25$ |

**Quiz L04: pre 2/3 · post 4/4** ✅ (el concepto de Hessiana/punto de silla, fallado en el pre-quiz, quedó dominado en el post-quiz tras el Paso 6)

## Dudas y pendientes

- Ninguna pendiente. L01–L04 completadas. De L03: el signo de los autovectores no es único (válidos ambos: $v$ y $-v$); solo el determinante del escalado rompe la simetría circular al componer transformaciones. De L04: el momentum no siempre converge más rápido en pasos absolutos — puede sobrepasar el mínimo y oscilar (Ej.3); su ventaja real aparece en superficies con curvatura desigual entre direcciones.
