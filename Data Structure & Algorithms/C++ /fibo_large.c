#include <stdio.h>
#include <string.h>
#define BASE 10000000000
#define MAX_DIGITS 10000

typedef struct {
    long long d[MAX_DIGITS];
    int len;
} BigInt;

void mul(BigInt *a, int x) {
    long long carry = 0;
    for (int i = 0; i < a->len; i++) {
        long long prod = a->d[i] * x + carry;
        a->d[i] = prod % BASE;
        carry = prod / BASE;
    }
    while (carry) {
        a->d[a->len++] = carry % BASE;
        carry /= BASE;
    }
}

void divi(BigInt *a, int x) {
    long long rem = 0;
    for (int i = a->len - 1; i >= 0; i--) {
        long long cur = a->d[i] + rem * BASE;
        a->d[i] = cur / x;
        rem = cur % x;
    }
    while (a->len > 1 && a->d[a->len - 1] == 0)
        a->len--;
}

int main(void) {
    int k, n;
    scanf("%d %d", &k, &n); 
    if (k > n) return 1;
    if (k > n - k) k = n - k;

    BigInt result;
    memset(result.d, 0, sizeof(result.d));
    result.d[0] = 1;
    result.len = 1;

    for (int i = 1; i <= k; i++) {
        mul(&result, n - k + i);
        divi(&result, i);
    }

    printf("%lld", result.d[result.len - 1]);
    for (int i = result.len - 2; i >= 0; i--)
        printf("%09lld", result.d[i]);
    printf("\n");

    return 0;
}
