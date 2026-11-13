import random
import numpy as np

def check_property(repetitions):
    holds = 0
    for _ in range(repetitions):
        x, y, z = np.float32(random.random()), np.float32(random.random()), np.float32(random.random())
        if (x * y) * z == x * (y * z):
            holds += 1
    return 100 * holds / repetitions

print(check_property(10000))