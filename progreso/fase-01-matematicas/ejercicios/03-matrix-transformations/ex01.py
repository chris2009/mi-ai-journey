import math

from matrices_transformacion import mat_vec_mul, rotation_2d, scaling_2d, shearing_2d

# Esquinas del cuadrado unitario
A = [0, 0]
B = [1, 0]
C = [1, 1]
D = [0, 1]

# rotación de 45 grados
theta = 45 * (3.14159265 / 180)  # Convertir a radianes
R = rotation_2d(theta)
# print(f"Rotación de 45 grados:\nR = {R}")
print("=====================================================================")
print("Ejecución Manual")
print("=====================================================================")
print("Rotación de 45 grados:")
print(f"A' = {R[0][0]*A[0] + R[0][1]*A[1]:.4f}, {R[1][0]*A[0] + R[1][1]*A[1]:.4f}")
print(f"B' = {R[0][0]*B[0] + R[0][1]*B[1]:.4f}, {R[1][0]*B[0] + R[1][1]*B[1]:.4f}")
print(f"C' = {R[0][0]*C[0] + R[0][1]*C[1]:.4f}, {R[1][0]*C[0] + R[1][1]*C[1]:.4f}")
print(f"D' = {R[0][0]*D[0] + R[0][1]*D[1]:.4f}, {R[1][0]*D[0] + R[1][1]*D[1]:.4f}")

print("=====================================================================")
print("Ejecución en loop")
print("=====================================================================")
corners = {"A": A, "B": B, "C": C, "D": D}
for name, point in corners.items():
    result = mat_vec_mul(R, point)
    print(f"{name}' = ({result[0]:.4f}, {result[1]:.4f})")

# Escalado por 2 en todas las esquinas
S = scaling_2d(2, 0.5)
print("=====================================================================")
print("Escalado por 2 en todas las esquinas:")
for name, point in corners.items():
    result = mat_vec_mul(S, point)
    print(f"{name}' = ({result[0]:.1f}, {result[1]:.1f})")

# Shearing con kx=1
Sh = shearing_2d(1, 0)
print("=====================================================================")
print("Shearing con kx=1:")
for name, point in corners.items():
    result = mat_vec_mul(Sh, point)
    print(f"{name}' = ({result[0]:.1f}, {result[1]:.1f})")


# Distancias originales
dist_AB_orig = math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
dist_BC_orig = math.sqrt((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2)

# Distancias después de rotar
A_r = mat_vec_mul(R, A)
B_r = mat_vec_mul(R, B)
C_r = mat_vec_mul(R, C)

dist_AB_rot = math.sqrt((B_r[0] - A_r[0]) ** 2 + (B_r[1] - A_r[1]) ** 2)
dist_BC_rot = math.sqrt((C_r[0] - B_r[0]) ** 2 + (C_r[1] - B_r[1]) ** 2)

print(f"Distancia A-B: antes={dist_AB_orig:.4f}, después={dist_AB_rot:.4f}")
print(f"Distancia B-C: antes={dist_BC_orig:.4f}, después={dist_BC_rot:.4f}")
