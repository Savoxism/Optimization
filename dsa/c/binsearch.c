#include <stdio.h>

int binsearch(int low, int high, int S[], int key) {
    if (low <= high) {
        int mid = (low + high) / 2;
        if (S[mid] == key) {
            return mid;
        }
        else if (key < S[mid]) {
            return binsearch(low, mid - 1, S, key);
        }
        else {
            return binsearch(mid + 1, high, S, key);
        }
    }
    return -1;
}

int main(void) {
    int S[] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    int n = sizeof(S) / sizeof(S[0]);

    printf("Array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", S[i]);
    }
    printf("\n");

    int key;
    printf("Enter the key to search: ");
    scanf("%d", &key);

    int index = binsearch(0, n - 1, S, key);

    if (index != -1) {
        printf("Key %d found at index %d.\n", key, index);
    } else {
        printf("Key %d not found in the array.\n", key);
    }
    return 0;
}
