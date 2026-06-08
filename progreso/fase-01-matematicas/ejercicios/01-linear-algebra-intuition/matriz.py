from vector import Vector


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
        rows = []
        for i in range(self.shape[0]):
            row = []
            for j in range(other.shape[1]):
                row.append(
                    sum(
                        self.rows[i][k] * other.rows[k][j] for k in range(self.shape[1])
                    )
                )
            rows.append(row)
        return Matrix(rows)

    def transpose(self):
        return Matrix(
            [
                [self.rows[j][i] for j in range(self.shape[0])]
                for i in range(self.shape[1])
            ]
        )

    def __repr__(self):
        return f"Matrix({self.rows})"


"""Ejercicio: Implementa una matriz de rotación 90° y aplícala a un punto"""
rotation_90 = Matrix([[0, -1], [1, 0]])
point = Vector([3, 1])

rotated = rotation_90 @ point
print(f"Original: {point}")
print(f"Rotado 90°: {rotated}")
