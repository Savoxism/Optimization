#include <stdio.h>

int binarySearch(int arr[], int left, int right, int target) {
    if (left > right) {
        return -1;
    }

    int mid = left + (right - left) / 2;

    if (arr[mid] == target) {
        return mid;
    }

    else if (arr[mid] < target) {
        return binarySearch(arr, mid + 1, right, target);
    }
    else {
        return binarySearch(arr, left, mid - 1, target);
    }
}

int main() {
    int arr[] = {1, 3, 5, 7, 9, 11, 13};
    int size = sizeof(arr) / sizeof(arr[0]);
    int target = 7;

    int result = binarySearch(arr, 0, size - 1, target);
    if (result != -1)
        printf("Found %d at index %d\n", target, result);
    else
        printf("%d not found in array\n", target);

    return 0;
}