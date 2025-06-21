#include <stdio.h>
#include <string.h>

#define MAXN 1000

char a[] = "bananinn";
char b[] = "kaninan";
int mem[MAXN][MAXN];

int max(int x, int y) {
    return x > y ? x : y;
}

int lcs(int i, int j) {
    if (i == -1 || j == -1) return 0;
    if (mem[i][j] != -1) {
        return mem[i][j];
    }

    int res;
    if (a[i] == b[j]) res = 1 + lcs(i - 1, j - 1);
    else res = max(lcs(i, j - 1), lcs(i - 1, j));

    mem[i][j] = res;
    return res;
}

int main() {
    memset(mem, -1, sizeof(mem));
    int n = strlen(a);
    int m = strlen(b);
    printf("Length of LCS: %d\n", lcs(n - 1, m - 1));
    return 0;
}