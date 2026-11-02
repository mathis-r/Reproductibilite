#!/usr/local/bin/python3
import random
import sys

def equals(x,y,z):
    return (x+(y+z)==(x+y)+z)


def test():
    results = []
    pourcentage = 0
    for i in range(100):
        results.append(equals(random.random(), random.random(), random.random()))
        pourcentage += results[i]
    pourcentage /=100
    #print("Résultat : ",pourcentage)
    return pourcentage


def main():
    for rep in [100,10000,100000]:
        tests =[]
        for i in range(rep):
            tests.append(test())
        print(sum(tests)/len(tests))
    return 0

if __name__ == "__main__":
    main()
