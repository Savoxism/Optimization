#include <stdio.h>

int n;
int a[100];

void printSolution() {
    for (int i = 0; i <= n; i++) {
        printf("%d", a[i]);
    }
    printf("\n");
}

void Try(int k) {
    for (int candidate = 0; candidate <= 1; candidate++) {
        if (candidate == 1 && k > 1 && a[k-1] == 1) {
            continue;
        }
        a[k] = candidate;
        if (k == n) {
            printSolution();
        } else {
            Try(k + 1);
        }
    }
}

int main(void) {
    scanf("%d", &n);
    Try(1);
    return 0;
}
