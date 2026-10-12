#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int equals(double x, double y, double z)
{
    return (x + (y + z) == (x + y) + z);
}

double test(void)
{
    srand48(time(NULL));
    double compteur_vrai = 0;
    double compteur_faux = 0;
    int results[101];
    results[0] = equals(0.1,0.2,0.3);
    if (results[0])
    {
        compteur_vrai++;
    } else
    {
        compteur_faux++;
        //printf("%f %f %f : %f != %f\n",0.1,0.2,0.3,0.1+(0.2+0.3),(0.1+0.2)+0.3);
    }
    //printf("%d\n",results[0]);

    double pourcentage = 0;

    for (int i = 1; i < 101; i++)
    {
        double x = drand48()*100;
        double y = drand48()*100;
        double z = drand48()*100;
        results[i] = equals(x,y,z);
        if (results[i])
        {
            compteur_vrai++;
        } else
        {
            compteur_faux++;
            //printf("%f %f %f : %f != %f\n",x,y,z, x + (y + z), (x + y) + z);
        }
        //printf("%d\n",results[i]);
    }

    //printf("%f\n",compteur_vrai);
    pourcentage = compteur_vrai/101;
    //printf("%d\n",results[19]);
    //printf("Résultat : %f ; nb faux : %f, nb vrai : %f\n",pourcentage, compteur_faux, compteur_vrai);
    return pourcentage;
}

int main()
{
    double tests[100] = {0};
    double sum = 0;
    for (int i = 1; i < 100; i++)
    {
        tests[i] = test();
        sum += tests[i];
    }
    printf("Moyenne = %f\n", sum/100.0);
    return 0;
}