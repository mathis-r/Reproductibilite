#include <stdio.h>
#include <stdlib.h>
#include <math.h>


double nyear(double n, double val)
{
    return n*val;
}

int main()
{
    double argent = M_E;
    for (int i = 1; i < 51 ; i++)
    {
        argent -=1;
        argent = nyear(i,argent);
    }
    argent -=1;
    printf("Argent : %f\n", argent);
    return 0;
}