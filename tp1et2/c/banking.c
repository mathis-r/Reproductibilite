#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double nyear(double n, double val) { return n * val; }

int main() {
  double argent = M_E;
  for (int i = 1; i < 51; i++) {
    argent -= 1;
    argent = nyear(i, argent);
  }
  argent -= 1;
  FILE *f = fopen("out/answer_banking.txt", "w");
  if (f == NULL) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }
  fprintf(f, "%f\n", argent);
  fclose(f);
  // printf("Argent : %f\n", argent);
  return 0;
}
