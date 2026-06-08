import random

from matrix import Matrix

inputs = Matrix([[0.5], [0.8], [0.2]])
weights = Matrix([[random.uniform(-1, 1) for _ in range(3)] for _ in range(2)])
bias = Matrix([[0.1], [0.1]])


def relu_matrix(m):
    return Matrix([[max(0, val) for val in row] for row in m.data])


pre_activation = weights.matmul(inputs) + bias
output = relu_matrix(pre_activation)

print(f"Input shape: {inputs.shape}")
print(f"Weight shape: {weights.shape}")
print(f"Output shape: {output.shape}")
print(f"Output: {output.data}")
