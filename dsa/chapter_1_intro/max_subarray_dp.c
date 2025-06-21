#include <stdio.h>
#include <limits.h>

#define max(a, b) ((a) > (b) ? (a) : (b))

int MaxSub(int arr[], int n) {
    int si = arr[0];
    int ei = arr[0];

    for (int i = 1; i < n; i++) {
        ei = max(arr[i], ei + arr[i]);
        si = max(si, ei);
    }
    return si;
}

int main() {
    int arr[] = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    int n = sizeof(arr) / sizeof(arr[0]);
    int maxSum = MaxSub(arr, n);  // Call the correct function name
    printf("Maximum subarray sum is %d\n", maxSum);
    return 0;
}