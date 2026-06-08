import math


class Vector:
    def __init__(self, components):
        self.components = list(components)
        self.dim = len(self.components)

    def dot(self, other):
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        return sum(x**2 for x in self.components) ** 0.5

    def cosine_similarity(self, other):
        return self.dot(other) / (self.magnitude() * other.magnitude())

    def angle_between(self, other):
        # TU CÓDIGO AQUÍ
        cos_angle = self.cosine_similarity(other)
        # Aseguramos que el valor esté en el rango [-1, 1] para evitar errores de dominio
        cos_angle = max(min(cos_angle, 1), -1)
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def __repr__(self):
        return f"Vector({self.components})"


# Pruebas
a = Vector([1, 0])
b = Vector([0, 1])
c = Vector([1, 1])

print(f"Ángulo entre [1,0] y [0,1]: {a.angle_between(b):.1f}°")  # debe dar 90.0°
print(f"Ángulo entre [1,0] y [1,1]: {a.angle_between(c):.1f}°")  # debe dar 45.0°
print(f"Ángulo entre [1,0] y [1,0]: {a.angle_between(a):.1f}°")  # debe dar 0.0°
