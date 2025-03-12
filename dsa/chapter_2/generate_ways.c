#include <stdio.h>

int k, n;
int x[41];

void Try(int i, int sum) {
    if ( i == k + 1) {
        if (sum == n) {
            for (int j = 1; j <= k; j++) {
                printf("%d", x[j]);
                if ( j < k) {
                    printf(" ");
                }
            }
            printf("\n");
        }
        return;
    }

    // Recursion
    for (int val = (i == 1 ? 1 : x[i - 1]); val <= n - sum; val++) {
        x[i] = val;
        Try(i + 1, sum + val);
    }
}

int main() {
    scanf("%d %d", &k, &n);
    Try(1, 0);  
    return 0;
}