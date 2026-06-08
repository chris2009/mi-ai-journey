import numpy as np

# TU CÓDIGO:
# 1. Construye una matriz 3x3 donde una columna (o fila) sea combinación lineal de las otras
#    Pista: si la columna 2 = columna 0 + columna 1, el rango será 2 (no 3)
# 2. Verifica el rango con np.linalg.matrix_rank()
# 3. Imprime la matriz y su rango
matrix = np.array([[1, 2, 3], [4, 5, 9], [7, 8, 15]])
rank = np.linalg.matrix_rank(matrix)
print("Matriz:")
print(matrix)
print(f"Rango de la matriz: {rank}")
