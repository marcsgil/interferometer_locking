from random import uniform


def evolve_system(x, k, A):
    return (x + uniform(-A, A)) * (1 - k)
