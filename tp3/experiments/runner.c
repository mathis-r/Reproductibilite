#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>

#ifdef USE_SINGLE
typedef float num_t;
#define ONE 1.0f
#else
typedef double num_t;
#define ONE 1.0
#endif

// PRNG simple et rapide (xorshift64)
static uint64_t state = 42;
static inline uint64_t next_u64(void) {
    uint64_t x = state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    return state = x;
}

static inline double next_double01(void) {
    return (next_u64() >> 11) * (1.0 / 9007199254740992.0);
}

static inline num_t gen_num(int dist) {
    double r;
    if (dist == 0) { // Uniform01: [0.00001, 1.0]
        r = 0.00001 + 0.99999 * next_double01();
    } else if (dist == 1) { // UniformNeg1Pos1: [-1.0, 1.0]
        r = -1.0 + 2.0 * next_double01();
        if (r == 0.0) r = 0.00001;
    } else { // Gaussian via Box-Muller
        double u1 = next_double01();
        double u2 = next_double01();
        if (u1 <= 1e-15) u1 = 1e-15;
        r = sqrt(-2.0 * log(u1)) * cos(2.0 * 3.14159265358979323846 * u2);
        if (r == 0.0) r = 0.00001;
    }
    return (num_t)r;
}

int main(int argc, char **argv) {
    if (argc < 4) return 1;
    int prop = atoi(argv[1]);
    int dist = atoi(argv[2]);
    long reps = atol(argv[3]);
    if (argc >= 5) state = (uint64_t)strtoull(argv[4], NULL, 10);
    if (state == 0) state = 42;

    long matches = 0;
    for (long i = 0; i < reps; i++) {
        num_t x = gen_num(dist);
        num_t y = gen_num(dist);
        num_t z = gen_num(dist);
        bool eq = false;
        if (prop == 0) { // AssocAdd
            eq = ((x + y) + z == x + (y + z));
        } else if (prop == 1) { // AssocMul
            eq = ((x * y) * z == x * (y * z));
        } else if (prop == 2) { // Distributivity
            eq = (x * (y + z) == (x * y) + (x * z));
        } else if (prop == 3) { // InverseMul
            eq = (x * (ONE / x) == ONE);
        }
        if (eq) matches++;
    }

    double pct = 100.0 * (double)matches / (double)reps;
    printf("%.6f\n", pct);
    return 0;
}
