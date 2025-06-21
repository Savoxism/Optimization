#include <iostream>
#include <vector>

// Function to merge two sorted subarrays arr[l..m] and arr[m+1..r]
void merge(std::vector<int>& arr, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    // Create temporary arrays
    std::vector<int> L(n1);
    std::vector<int> R(n2);

    // Copy data to temporary arrays L[] and R[]
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    // Initial indexes of first and second subarrays
    int i = 0, j = 0;

    // Initial index of merged subarray
    int k = l;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], if there are any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], if there are any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// Main function that sorts arr[l..r] using merge()
void mergeSort(std::vector<int>& arr, int l, int r) {
    if (l < r) {
        // Find the middle point
        int m = l + (r - l) / 2;

        // Recursively sort first and second halves
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        // Merge the sorted halves
        merge(arr, l, m, r);
    }
}

// Helper function to print the array
void printArray(const std::vector<int>& arr) {
    for (int val : arr) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> my_list = {6, 5, 12, 10, 9, 1};

    std::cout << "Original list: ";
    printArray(my_list);

    mergeSort(my_list, 0, my_list.size() - 1);

    std::cout << "Sorted list: ";
    printArray(my_list);

    std::vector<int> another_list = {38, 27, 43, 3, 9, 82, 10};
    std::cout << "\nOriginal list: ";
    printArray(another_list);

    mergeSort(another_list, 0, another_list.size() - 1);

    std::cout << "Sorted list: ";
    printArray(another_list);

    return 0;
}