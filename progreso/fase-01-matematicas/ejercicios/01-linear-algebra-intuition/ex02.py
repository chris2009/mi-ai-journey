class Vector:
    def __init__(self, components):
        self.components = list(components)

    def __repr__(self):
        return f"Vector({self.components})"


class Matrix:
    def __init__(self, rows):
        self.rows = [list(row) for row in rows]
        self.shape = (len(self.rows), len(self.rows[0]))

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return Vector(
                [
                    sum(
                        self.rows[i][j] * other.components[j]
                        for j in range(self.shape[1])
                    )
                    for i in range(self.shape[0])
                ]
            )

    def __repr__(self):
        return f"Matrix({self.rows})"


# TU CÓDIGO: define la matriz de escalado y aplícala
# Pista: una matriz de escalado 2D que escala x por 2 e y por 3 es:
#   [[2, 0],
#    [0, 3]]

# scaling = Matrix(...)
# v = Vector([1, 1])
# result = scaling @ v
# print(...)
scaling = Matrix([[2, 0], [0, 3]])
v = Vector([1, 1])
result = scaling @ v

print(f"Original: {v}")
print(f"Escalado: {result}")
