#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int k, n;
    scanf("%d %d", &k, &n); 

    int **dp = malloc((n + 1) * sizeof(int *));
    for (int i = 0; i <= n; i++) {
        dp[i] = malloc((k + 1) * sizeof(int));
    }

    for (int i = 0; i <= n; i++) {
        int upperBound = (i < k) ? i : k;
        for (int j = 0; j <= upperBound; j++) {
            if (j == 0 || j == i)
                dp[i][j] = 1;
            else
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
        }
    }
    
    printf("%d\n", dp[n][k]);
    
    for (int i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);
    
    return 0;
}
