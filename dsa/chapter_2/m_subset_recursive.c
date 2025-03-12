#include <stdio.h>

int n, m, solutionCount;
int a[100];

void PrintSolution() {
    int i;
    for (i = 1; i <= m; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");
    solutionCount++;
}

void Try(int k) {
    int j;
    for (j = a[k-1] + 1; j <= n - m + k; j++) {
        a[k] = j;
        if (k == m)
            PrintSolution();
        else
            Try(k + 1);
    }
}

int main(void) {
    scanf("%d %d", &n, &m);
    solutionCount = 0;
    a[0] = 0;
    Try(1);
    printf("%d", solutionCount);
    return 0;
}
