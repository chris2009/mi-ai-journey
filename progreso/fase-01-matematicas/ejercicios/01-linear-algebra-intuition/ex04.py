import numpy as np

# Genera 3 vectores aleatorios en 3D y aplica QR (que internamente usa Gram-Schmidt)
np.random.seed(42)
V = np.random.randn(3, 3)
Q, R = np.linalg.qr(V)

print("Vectores ortonormales (columnas de Q):")
print(Q)

# TU CÓDIGO:
# 1. Verifica que cada par de columnas de Q tiene producto punto ≈ 0
# 2. Verifica que cada columna tiene magnitud (norma) ≈ 1
# Pista: usa np.dot() para el producto punto y np.linalg.norm() para la magnitud
# Pista: Q[:, i] te da la columna i
print("\nVerificación de ortogonalidad:")
for i in range(Q.shape[1]):
    for j in range(i + 1, Q.shape[1]):
        dot_product = np.dot(Q[:, i], Q[:, j])
        print(f"Producto punto entre columna {i} y {j}: {dot_product:.4e}")
print("\nVerificación de normalización:")
for i in range(Q.shape[1]):
    norm = np.linalg.norm(Q[:, i])
    print(f"Norma de columna {i}: {norm:.4f}")
