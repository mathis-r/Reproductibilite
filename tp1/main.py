import random
import sys

def equals(x,y,z):
    return (x+(y+z)==(x+y)+z)


def main():
    results = []
    pourcentage = 0
    for i in range(100):
        results.append(equals(random.random(), random.random(), random.random()))
        pourcentage += results[i]
    pourcentage /=100
    print("Résultat : ",pourcentage)
    return 0

if __name__ == "__main__":
    main()
