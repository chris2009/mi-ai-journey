import numpy as np

a = np.array([1, 2, 3])
b = np.array([1, 1, 1])

# TU CÓDIGO: calcula la proyección de a sobre b
# Fórmula: proj_b(a) = (a · b / b · b) * b
proj = (np.dot(a, b) / np.dot(b, b)) * b

print(f"a = {a}")
print(f"b = {b}")
print(f"Proyección de a sobre b: {proj}")
