from matrix import Matrix

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])
C = Matrix([[1, 3], [0, 1]])

invA = A.inverse_2x2()
invB = B.inverse_2x2()
invC = C.inverse_2x2()
print("A^-1 =", invA.data)
print("A @ A^-1 =", A.matmul(invA).data)
print("B^-1 =", invB.data)
print("B @ B^-1 =", B.matmul(invB).data)
print("C^-1 =", invC.data)
print("C @ C^-1 =", C.matmul(invC).data)

D = Matrix([[2, 0], [1, 0]])
print("D =", D.inverse_2x2().data)  # Esto debería lanzar un error porque D es singular
