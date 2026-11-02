#!/usr/local/bin/python3
import random
import sys
import argparse
import json


def equals(x, y, z):
    return (x + (y + z) == (x + y) + z)


def test(minrand, maxrand):
    results = []
    pourcentage = 0
    for i in range(100):
        results.append(equals(random.uniform(minrand, maxrand), random.uniform(minrand, maxrand),
                              random.uniform(minrand, maxrand)))
        pourcentage += results[i]
    pourcentage /= 100
    # print("Résultat : ",pourcentage)
    return pourcentage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=1000)
    parser.add_argument("--minrand", type=float, default=0.0)
    parser.add_argument("--maxrand", type=float, default=1.0)
    args = parser.parse_args()
    tests = []
    for i in range(args.repetitions):
        tests.append(test(args.minrand, args.maxrand))
    percentage = sum(tests) / len(tests)
    print(json.dumps(
        {"repetitions": args.repetitions, "minrand": args.minrand, "maxrand": args.maxrand, "percentage": percentage}))
    return 0


if __name__ == "__main__":
    main()
