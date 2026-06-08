# Vectores, Matrices y Operaciones

> Toda red neuronal es solo multiplicación de matrices con pasos extra.

**Tipo:** Construcción
**Lenguajes:** Python, Julia
**Prerrequisitos:** Fase 1, Lección 01 (Intuición de Álgebra Lineal)
**Tiempo:** ~60 minutos

## Objetivos de aprendizaje

- Construir una clase Matrix con operaciones elemento a elemento, multiplicación de matrices, transposición, determinante e inversa
- Distinguir la multiplicación elemento a elemento de la multiplicación matricial y explicar cuándo aplica cada una
- Implementar una sola capa densa de red neuronal (`relu(W @ x + b)`) usando solo la clase Matrix construida desde cero
- Explicar las reglas de *broadcasting* y cómo funciona la suma de sesgos (*bias*) en los frameworks de redes neuronales

## El problema

Quieres construir una red neuronal. Lees el código y ves esto:

```
output = activation(weights @ input + bias)
```

Ese `@` es multiplicación de matrices. Los `weights` son una matriz. El `input` es un vector. Si no sabes qué hacen esas operaciones, esta línea es magia. Si lo sabes, es el *forward pass* completo de una capa en tres operaciones.

Cada imagen que procesa tu modelo es una matriz de valores de píxeles. Cada *embedding* de palabra es un vector. Cada capa de cada red neuronal es una transformación matricial. No puedes construir sistemas de IA sin tener fluidez en operaciones matriciales, de la misma forma que no puedes escribir código sin entender variables.

Esta lección construye esa fluidez desde cero.

## El concepto

### Vectores: listas ordenadas de números

Un vector es una lista de números con dirección y magnitud. En IA, los vectores representan puntos de datos, *features* o parámetros.

```
v = [3, 4]        -- un vector 2D
w = [1, 0, -2]    -- un vector 3D
```

Un vector 2D `[3, 4]` apunta a las coordenadas (3, 4) en un plano. Su longitud (magnitud) es 5 (el triángulo 3-4-5):

$$\|v\| = \sqrt{3^2 + 4^2} = \sqrt{25} = 5$$

### Matrices: cuadrículas de números

Una matriz es una cuadrícula 2D. Filas y columnas. Una matriz $m \times n$ tiene $m$ filas y $n$ columnas.

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix} \quad \text{-- matriz } 2\times 3 \text{ (2 filas, 3 columnas)}$$

En las redes neuronales, las matrices de pesos transforman vectores de entrada en vectores de salida. Una capa con 784 entradas y 128 salidas usa una matriz de pesos de $128 \times 784$.

### Por qué importan las formas (*shapes*)

La multiplicación de matrices tiene una regla estricta: $(m \times n) @ (n \times p) = (m \times p)$. Las dimensiones internas deben coincidir.

$$(128 \times 784) @ (784 \times 1) = (128 \times 1)$$
$$\underbrace{(128 \times 784)}_{\text{pesos}} \;\; \underbrace{(784 \times 1)}_{\text{entrada}} \;\; \to \;\; \underbrace{(128 \times 1)}_{\text{salida}}$$

Dimensiones internas: $784 = 784$ — válido.

Si te aparece un error de *shape mismatch* en PyTorch, esta es la razón.

### El mapa de operaciones

| Operación | Qué hace | Uso en redes neuronales |
|-----------|-------------|-------------------|
| Suma | Combina elemento a elemento | Sumar el sesgo (*bias*) a la salida |
| Multiplicación escalar | Escala cada elemento | *Learning rate* × gradientes |
| Multiplicación matricial | Transforma vectores | *Forward pass* de una capa |
| Transposición | Intercambia filas y columnas | Backpropagation |
| Determinante | Resumen en un solo número | Verificar si es invertible |
| Inversa | Deshace una transformación | Resolver sistemas lineales |
| Identidad | Matriz que no hace nada | Inicialización, conexiones residuales |

### Multiplicación elemento a elemento vs. multiplicación matricial

Esta distinción confunde constantemente a los principiantes.

**Elemento a elemento:** multiplica posiciones correspondientes. Ambas matrices deben tener la misma forma.

$$\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} * \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix} = \begin{pmatrix} 5 & 12 \\ 21 & 32 \end{pmatrix}$$

**Multiplicación matricial:** productos punto entre filas y columnas. Las dimensiones internas deben coincidir.

$$\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} @ \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix} = \begin{pmatrix} 1\cdot 5 + 2\cdot 7 & 1\cdot 6 + 2\cdot 8 \\ 3\cdot 5 + 4\cdot 7 & 3\cdot 6 + 4\cdot 8 \end{pmatrix} = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$$

Operaciones diferentes, resultados diferentes, reglas diferentes.

### Broadcasting

Cuando sumas un vector de sesgo (*bias*) a una matriz de salidas, las formas no coinciden. El *broadcasting* estira el arreglo más pequeño para que encaje.

$$\begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix} + [10, 20, 30]$$

El *broadcasting* estira el vector a través de las filas:

$$\begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix} + \begin{pmatrix} 10 & 20 & 30 \\ 10 & 20 & 30 \end{pmatrix} = \begin{pmatrix} 11 & 22 & 33 \\ 14 & 25 & 36 \end{pmatrix}$$

Todo *framework* moderno hace esto automáticamente. Entenderlo evita confusiones cuando las formas parecen incorrectas pero el código corre sin error.

## Constrúyelo

### Paso 1: Clase Vector

```python
class Vector:
    def __init__(self, data):
        self.data = list(data)
        self.size = len(self.data)

    def __repr__(self):
        return f"Vector({self.data})"

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, scalar):
        return Vector([x * scalar for x in self.data])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.data, other.data))

    def magnitude(self):
        return sum(x ** 2 for x in self.data) ** 0.5
```

### Paso 2: Clase Matrix con operaciones centrales

```python
class Matrix:
    def __init__(self, data):
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.shape = (self.rows, self.cols)

    def __repr__(self):
        rows_str = "\n  ".join(str(row) for row in self.data)
        return f"Matrix({self.shape}):\n  {rows_str}"

    def __add__(self, other):
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __sub__(self, other):
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def scalar_multiply(self, scalar):
        return Matrix([
            [self.data[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def element_wise_multiply(self, other):
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def matmul(self, other):
        return Matrix([
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ])

    def transpose(self):
        return Matrix([
            [self.data[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ])

    def determinant(self):
        if self.shape == (1, 1):
            return self.data[0][0]
        if self.shape == (2, 2):
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        det = 0
        for j in range(self.cols):
            minor = Matrix([
                [self.data[i][k] for k in range(self.cols) if k != j]
                for i in range(1, self.rows)
            ])
            det += ((-1) ** j) * self.data[0][j] * minor.determinant()
        return det

    def inverse_2x2(self):
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular, no inverse exists")
        return Matrix([
            [self.data[1][1] / det, -self.data[0][1] / det],
            [-self.data[1][0] / det, self.data[0][0] / det]
        ])

    @staticmethod
    def identity(n):
        return Matrix([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])
```

### Paso 3: Verlo funcionar

```python
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

print("A + B =", (A + B).data)
print("A @ B =", A.matmul(B).data)
print("A^T =", A.transpose().data)
print("det(A) =", A.determinant())
print("A^-1 =", A.inverse_2x2().data)

I = Matrix.identity(2)
print("A @ A^-1 =", A.matmul(A.inverse_2x2()).data)
```

### Paso 4: Conectarlo con redes neuronales

```python
import random

inputs = Matrix([[0.5], [0.8], [0.2]])
weights = Matrix([
    [random.uniform(-1, 1) for _ in range(3)]
    for _ in range(2)
])
bias = Matrix([[0.1], [0.1]])

def relu_matrix(m):
    return Matrix([[max(0, val) for val in row] for row in m.data])

pre_activation = weights.matmul(inputs) + bias
output = relu_matrix(pre_activation)

print(f"Input shape: {inputs.shape}")
print(f"Weight shape: {weights.shape}")
print(f"Output shape: {output.shape}")
print(f"Output: {output.data}")
```

Esto es una sola capa densa: $\text{output} = \text{relu}(W \mathbin{@} x + b)$. Cada capa densa de cada red neuronal hace exactamente esto.

## Úsalo

NumPy hace todo lo anterior en menos líneas y órdenes de magnitud más rápido.

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A + B =\n", A + B)
print("A * B (element-wise) =\n", A * B)
print("A @ B (matrix multiply) =\n", A @ B)
print("A^T =\n", A.T)
print("det(A) =", np.linalg.det(A))
print("A^-1 =\n", np.linalg.inv(A))
print("I =\n", np.eye(2))

inputs = np.random.randn(3, 1)
weights = np.random.randn(2, 3)
bias = np.array([[0.1], [0.1]])
output = np.maximum(0, weights @ inputs + bias)

print(f"\nNeural network layer: {weights.shape} @ {inputs.shape} = {output.shape}")
print(f"Output:\n{output}")
```

El operador `@` en Python invoca `__matmul__`. NumPy lo implementa con rutinas BLAS optimizadas escritas en C y Fortran. Las mismas matemáticas, 100 veces más rápido.

*Broadcasting* en NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy automáticamente hace *broadcast* del *bias* 1D a través de ambas filas. Así es como funciona la suma de sesgos en cada *framework* de redes neuronales.

## Envíalo (Ship It)

Esta lección produce un *prompt* para enseñar operaciones matriciales mediante intuición geométrica. Ver `outputs/prompt-matrix-operations.md`.

La clase Matrix construida aquí es la base del mini-framework de redes neuronales que construimos en la Fase 3, Lección 10.

## Ejercicios

1. **Verifica la inversa.** Multiplica `A @ A.inverse_2x2()` y confirma que obtienes la matriz identidad. Pruébalo con tres matrices $2\times 2$ diferentes. ¿Qué sucede cuando el determinante es cero?

2. **Implementa la inversa $3\times 3$.** Extiende la clase Matrix para calcular inversas de matrices $3\times 3$ usando el método de la adjunta (*adjugate*). Pruébalo contra `np.linalg.inv` de NumPy.

3. **Construye una red de dos capas.** Usando solo tu clase Matrix (sin NumPy), crea una red neuronal de dos capas: entrada (3) → oculta (4) → salida (2). Inicializa pesos aleatorios, ejecuta un *forward pass* y verifica que todas las formas sean correctas.

## Términos clave

| Término | Lo que dice la gente | Lo que realmente significa |
|------|----------------|----------------------|
| Vector | "Una flecha" | Una lista ordenada de números. En IA: un punto en un espacio de alta dimensión. |
| Matriz | "Una tabla de números" | Una transformación lineal. Mapea vectores de un espacio a otro. |
| Multiplicación matricial | "Solo multiplicar los números" | Productos punto entre cada fila de la primera matriz y cada columna de la segunda. El orden importa. |
| Transposición | "Voltearla" | Intercambiar filas y columnas. Convierte una matriz $m \times n$ en una $n \times m$. Crítico en backpropagation. |
| Determinante | "Algún número de la matriz" | Mide cuánto escala la matriz un área (2D) o un volumen (3D). Cero significa que la transformación aplasta una dimensión. |
| Inversa | "Deshacer la matriz" | La matriz que revierte la transformación. Solo existe cuando el determinante no es cero. |
| Matriz identidad | "La matriz aburrida" | El equivalente matricial de multiplicar por 1. Se usa en conexiones residuales (ResNets). |
| Broadcasting | "Magia que arregla formas" | Estirar un arreglo más pequeño para que coincida con uno más grande, repitiéndolo a lo largo de las dimensiones faltantes. |
| Elemento a elemento | "Multiplicación normal" | Multiplicar posiciones correspondientes. Ambos arreglos deben tener la misma forma (o ser compatibles por *broadcasting*). |

## Lecturas adicionales

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) - intuición visual para cada operación cubierta aquí
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) - las reglas exactas que sigue NumPy
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf) - referencia concisa de álgebra lineal específica para ML
