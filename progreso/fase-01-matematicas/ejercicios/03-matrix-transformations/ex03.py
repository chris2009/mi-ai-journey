import math

# Este ejercicio muestra cómo aplicar transformaciones a un conjunto de puntos en el plano.
# Usaremos las funciones de transformación definidas en matrices_transformacion.py
from matrices_transformacion import (
    determinant,
    mat_mul,
    mat_vec_mul,
    rotation_2d,
    scaling_2d,
    shearing_2d,
)

# Generamos 8 puntos alrededor de un círculo unitario, separados por pi/4
points = [[math.cos(math.pi * i / 4), math.sin(math.pi * i / 4)] for i in range(8)]
print("Puntos Originales (Separados por pi/4 alrededdor de un circulo):")
for i, p in enumerate(points):
    print(f"  Punto {i}: ({p[0]:.4f}, {p[1]:.4f})")

# Aplicamos una rotación de 30 grados a cada punto
theta = 30 * (math.pi / 180)  # Convertir a radianes
R = rotation_2d(theta)
print("\nPuntos después de rotar 30 grados:")
for i, p in enumerate(points):
    rotated = mat_vec_mul(R, p)
    print(f"  Punto {i}: ({rotated[0]:.4f}, {rotated[1]:.4f})")

# Aplicamos un escalado de 1.5x en x y 0.8x en y
S = scaling_2d(1.5, 0.8)
print("\nPuntos después de escalar 1.5x en x y 0.8x en y:")
for i, p in enumerate(points):
    scaled = mat_vec_mul(S, p)
    print(f"  Punto {i}: ({scaled[0]:.4f}, {scaled[1]:.4f})")

# Aplicamos un shearing con kx=0.3
Sh = shearing_2d(0.3, 0)
print("\nPuntos después de shearing con kx=0.3:")
for i, p in enumerate(points):
    sheared = mat_vec_mul(Sh, p)
    print(f"  Punto {i}: ({sheared[0]:.4f}, {sheared[1]:.4f})")

# Ahora calculamos la determinante de la matriz compuesta
composed = mat_mul(Sh, mat_mul(S, R))
det_composed = determinant(composed)
print(f"\nDeterminante de la matriz compuesta: {det_composed:.4f}")

# Para comprobar que la composición de transformaciones es correcta
det_R = determinant(R)
det_S = determinant(S)
det_Sh = determinant(Sh)
print(f"Determinante de R: {det_R:.4f}")
print(f"Determinante de S: {det_S:.4f}")
print(f"Determinante de Sh: {det_Sh:.4f}")
print(f"Producto de determinantes: {det_R * det_S * det_Sh:.4f}")

print("\nPuntos después de la COMPOSICIÓN (R → S → Sh):")
for i, point in enumerate(points):
    result = mat_vec_mul(composed, point)
    print(f"  Punto {i}: ({result[0]:.4f}, {result[1]:.4f})")
