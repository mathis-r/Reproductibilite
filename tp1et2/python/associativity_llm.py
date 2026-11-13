#!/usr/local/bin/python3
import random
from pathlib import Path

def check_associativity(generator, trials=1_000_000):
    equal_count = 0
    for _ in range(trials):
        x, y, z = generator(), generator(), generator()
        if (x + y) + z == x + (y + z):
            equal_count += 1
    return (equal_count / trials) * 100

random.seed(42)
pct_uniform = check_associativity(random.random)
pct_gaussian = check_associativity(lambda: random.gauss(0, 1))

print(f"Uniform [0, 1): {pct_uniform:.2f}%")
print(f"Gaussian (0, 1): {pct_gaussian:.2f}%")

with open("./out/answer_associativity_llm.txt", "w") as f:
    f.write(str(pct_uniform / 100) + "\n")
