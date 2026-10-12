import math

def nyear(n,val):
    return n*val;


def main():
    argent = math.e
    for i in range(1,51):
        argent -=1
        argent=nyear(i,argent)
    argent -=1
    print(argent)

if __name__ == "__main__":
    main()
