#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

// Fast 32-bit pseudo-random number generator
static uint32_t xorshift32(uint32_t *state) {
    uint32_t x = *state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return *state = x;
}

// Generates a random float in [-1.0, 1.0]
static float rand_float(uint32_t *state) {
    uint32_t r = xorshift32(state);
    return ((float)r / (float)UINT32_MAX) * 2.0f - 1.0f;
}

int main(void) {
    const long total_trials = 10000000;
    long total_matches = 0;
    uint32_t rng_state = (uint32_t)time(NULL);

    for (long i = 0; i < total_trials; i++) {
        float x = rand_float(&rng_state);
        float y = rand_float(&rng_state);
        float z = rand_float(&rng_state);

        // Test floating-point addition associativity
        if ((x + y) + z == x + (y + z)) {
            total_matches++;
        }
    }

    double percentage = ((double)total_matches / (double)total_trials) * 100.0;

    printf("Total trials:  %ld\n", total_trials);
    printf("Associative:   %ld\n", total_matches);
    printf("Percentage:    %.2f%%\n", percentage);

    FILE *f = fopen("out/answer_associativity_llm.txt", "w");
    if (f == NULL) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }
    fprintf(f, "%f\n", (double)total_matches / (double)total_trials);
    fclose(f);

    return 0;
}