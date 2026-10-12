#!/usr/bin/python3
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
    tests =[]
    for i in range(100):
        tests.append(test())
    with open("answer_associativity.txt", "w") as f:
        f.write(str(sum(tests)/len(tests))+"\n")
    #print(sum(tests)/len(tests))
    return 0

if __name__ == "__main__":
    main()
