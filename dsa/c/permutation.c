#include <stdio.h>
#include <stdbool.h>

int n;
int a[100];
bool used[101]; 

void printPermutation() {
    for (int i = 1; i <= n; i++) {
        printf("%d", a[i]);
        if (i < n)
            printf(" ");
    }
    printf("\n");
}

void Try(int k) {
    for (int candidate = 1; candidate <= n; candidate++) {
        if (!used[candidate]) {
            a[k] = candidate;
            used[candidate] = true;
            if (k == n)
                printPermutation();
            else
                Try(k + 1);
            used[candidate] = false;
        }
    }
}

int main(void) {
    scanf("%d", &n);
    for (int i = 1; i <= n; i++)
        used[i] = false;
    Try(1);
    return 0;
}
