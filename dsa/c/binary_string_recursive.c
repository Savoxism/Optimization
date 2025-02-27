#include <stdio.h>

int n;
int a[100];

void PrintSolution() {
    int i;
    for (i = 1; i <= n; i++) {
        printf("%d", a[i]);
    }
    printf("\n");
}

void Try(int k) {
    int j;
    for (j = 0; j <= 1; j++) {
        a[k] = j;
        if (k == n)
            PrintSolution();
        else
            Try(k + 1);
    }
}

int main(void) {
    scanf("%d", &n);
    Try(1);
    return 0;
}
