def Euler(func, n = 50, h = 0.01, x = 1, y = 1):
    for i in range(n):
        y = y + h * func(x, y)
        x = x + h
    return x, y

print(Euler(lambda x, y: 6 * x ** 2 + 5 * x * y))
