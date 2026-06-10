def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def numerical_second_derivative(f, x, h=1e-4):
    return (numerical_derivative(f, x + h, h) - numerical_derivative(f, x - h, h)) / (2 * h)

def f(x):
    return x ** 3

result = numerical_second_derivative(f, 2.0)
print(f"f''(2) numérica  = {result:.6f}")
print(f"f''(2) analítica = 6*x = {6 * 2}")
