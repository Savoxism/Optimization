#include <stdio.h>
// C:\msys64\ucrt64\bin\gcc.exe linear_search.c -o main.exe

void linearSearch(int a[], int size, int target) {
    int i;
    for (i = 1; i <= size; i++) {
        if (a[i] == target) break;
    }
    if (i <= size) {
        printf("The target is in the array, with index = %d", i);
    } else {
        printf("The target is NOT in the list.");
    }
}

int main() {
    int arr[] = {2, 4, 6, 8, 10};
    int size = sizeof(arr) / sizeof(arr[0]);
    int target = 8;

    linearSearch(arr, size, target);
    return 0;
}