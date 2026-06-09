from autovalor_autovectores import eigenvalues_2x2, eigenvector_2x2, mat_vec_mul

# MANUALMENTE CALCULADO
# Los autovalores de A son 2 y 5
# Los autovectores correspondientes son: (-1,1) y (2,1) respectivamente
# Pero normalizados son: (-0.7071, 0.7071) y (0.8944, 0.4472) respectivamente

# MATRIZ A
A = [[4, 2], [1, 3]]
print("=====================================================================")
print("Cálculo de autovalores y autovectores por FUNCION DESDE CERO:")
print("=====================================================================")
print(f"MATRIZ A:\n{A}")
vals = eigenvalues_2x2(A)
print(f"Eigenvalues: {vals[0]:.4f}, {vals[1]:.4f}")

for val in vals:
    vec = eigenvector_2x2(A, val)
    result = mat_vec_mul(A, vec)
    scaled = [val * vec[0], val * vec[1]]
    print(f"  lambda={val:.1f}, v={[round(x,4) for x in vec]}")
    print(f"    A@v = {[round(x,4) for x in result]}")
    print(f"    l*v = {[round(x,4) for x in scaled]}")

print("=====================================================================")
print("Cálculo de autovalores y autovectores por LIBRERÍA:")
print("=====================================================================")

import numpy as np

A_np = np.array(A)
eigenvalues, eigenvectors = np.linalg.eig(A_np)
print(f"Eigenvalues: {eigenvalues[0]:.4f}, {eigenvalues[1]:.4f}")
for i in range(len(eigenvalues)):
    print(f"  lambda={eigenvalues[i]:.1f}, v={[round(x,4) for x in eigenvectors[:,i]]}")
