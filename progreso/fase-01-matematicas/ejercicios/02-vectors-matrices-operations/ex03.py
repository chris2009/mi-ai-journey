import random

from matrix import Matrix


# Entrada x: forma (3, 1)
inputs = Matrix([
    [0.5],
    [0.8],
    [0.2]
])


# Pesos de la primera capa W1: forma (4, 3)
# 4 neuronas ocultas, cada una recibe 3 entradas
W1 = Matrix([
    [random.uniform(-1, 1) for _ in range(3)]
    for _ in range(4)
])


# Sesgo de la primera capa b1: forma (4, 1)
# Un bias para cada neurona oculta
b1 = Matrix([
    [0.1],
    [0.1],
    [0.1],
    [0.1]
])


# Pesos de la segunda capa W2: forma (2, 4)
# 2 neuronas de salida, cada una recibe 4 valores de la capa oculta
W2 = Matrix([
    [random.uniform(-1, 1) for _ in range(4)]
    for _ in range(2)
])


# Sesgo de la segunda capa b2: forma (2, 1)
# Un bias para cada neurona de salida
b2 = Matrix([
    [0.1],
    [0.1]
])


def relu_matrix(m):
    return Matrix([
        [max(0, val) for val in row]
        for row in m.data
    ])


# Primera capa
# z1 = W1 @ inputs + b1
pre_activation_1 = W1.matmul(inputs) + b1

# h = ReLU(z1)
hidden = relu_matrix(pre_activation_1)


# Segunda capa
# z2 = W2 @ hidden + b2
pre_activation_2 = W2.matmul(hidden) + b2

# y = ReLU(z2)
output = relu_matrix(pre_activation_2)


print("Inputs:\n", inputs)
print("Shape inputs:", inputs.shape)

print("\nW1:\n", W1)
print("Shape W1:", W1.shape)

print("\nb1:\n", b1)
print("Shape b1:", b1.shape)

print("\nPre-activation 1 = W1 @ inputs + b1:\n", pre_activation_1)
print("Shape pre_activation_1:", pre_activation_1.shape)

print("\nHidden = ReLU(pre_activation_1):\n", hidden)
print("Shape hidden:", hidden.shape)

print("\nW2:\n", W2)
print("Shape W2:", W2.shape)

print("\nb2:\n", b2)
print("Shape b2:", b2.shape)

print("\nPre-activation 2 = W2 @ hidden + b2:\n", pre_activation_2)
print("Shape pre_activation_2:", pre_activation_2.shape)

print("\nOutput = ReLU(pre_activation_2):\n", output)
print("Shape output:", output.shape)
