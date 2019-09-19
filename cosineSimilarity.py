from math import sqrt
def cosSim(a, b):
    prod = 0
    mod_a = 0
    mod_b = 0
    for i in range(len(a)):
        prod += a[i] * b[i]
        mod_a += a[i]*a[i]
        mod_b += b[i]*b[i]
    return (prod/(sqrt(mod_a*mod_b)))
