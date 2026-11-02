#!/usr/local/bin/python3
import math

def nyear(n,val):
    return n*val;


def main():
    argent = math.e
    for i in range(1,51):
        argent -=1
        argent=nyear(i,argent)
    argent -=1
    with open("./out/answer_banking.txt","w") as f:
        f.write(str(argent)+"\n")
    return 0

if __name__ == "__main__":
    main()
