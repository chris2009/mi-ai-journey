import numpy as np
from matrix import Matrix

A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
A = Matrix(A)
print("Matriz A:\n", A)

InvA = A.inverse_3x3()
print("Inversa de A:\n", InvA)

InvA_NP_LINALG = np.linalg.inv(A.data)
print("Inversa de A (NumPy):\n", InvA_NP_LINALG)
