from math import sqrt, exp, cos, sin, pi, e
# https://ru.wikipedia.org/wiki/Тестовые_функции_для_оптимизации

def Rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def Rastrigin(x, y):
    return 20 + x ** 2 + y ** 2 - 10 * (cos(2 * pi * x) + cos(2 * pi * y))

def Ackley(x, y):
    return -20*exp(-0.2*sqrt(0.5*(x**2+y**2)))-exp(0.5*(cos(2*pi*x)+cos(2*pi*y)))+e+20

def Sphere(x, y):
    return x**2 + y**2

def Himmelblau(x, y):
    return (x**2+y-11)**2 + (x+y**2-7)**2

def Holder(x, y):
    return -1 * abs(sin(x)*cos(y)*exp(abs(1 - (sqrt(x**2 + y**2))/pi) ))
