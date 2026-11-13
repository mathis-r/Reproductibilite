import random

def check_property(repetitions):
    holds = 0
    for _ in range(repetitions):
        x, y, z = random.random(), random.random(), random.random()
        if (x * y) * z == x * (y * z):
            holds += 1
    return 100 * holds / repetitions

print(check_property(10000))