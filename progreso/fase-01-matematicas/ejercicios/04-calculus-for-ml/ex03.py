def f(x):
    return x**4 - 3*x**2

def grad(x):
    return 4*x**3 - 6*x

def gradient_descent(x0, lr, steps):
    x = x0
    history = [x]
    for _ in range(steps):
        x = x - lr * grad(x)
        history.append(x)
    return history

def gradient_descent_momentum(x0, lr, steps, beta=0.9):
    x = x0
    v = 0.0
    history = [x]
    for _ in range(steps):
        v = beta * v + grad(x)
        x = x - lr * v
        history.append(x)
    return history

x0 = 0.5
lr = 0.01
steps = 100

hist_plain = gradient_descent(x0, lr, steps)
hist_momentum = gradient_descent_momentum(x0, lr, steps)

print("Mínimo esperado: x = sqrt(1.5) ≈ 1.2247, f(x) ≈ -2.25")
print()
print(f"{'step':>5} {'sin momentum':>15} {'con momentum':>15}")
for s in [0, 10, 20, 30, 40, 50, 70, 100]:
    print(f"{s:5d} {hist_plain[s]:15.4f} {hist_momentum[s]:15.4f}")

print()
print(f"f(sin momentum) final = {f(hist_plain[-1]):.6f}")
print(f"f(con momentum) final = {f(hist_momentum[-1]):.6f}")
