#include <iostream>
#include <vector>
#include <algorithm>

void printArray(const std::vector<int>& arr) {
    for (int val : arr) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}

void bubbleSortOptimized(std::vector<int>& arr) {
    int n = arr.size();
    bool swapped;
    for (int i = 0; i < n - 1; ++i) {
        swapped = false; // Initialize swapped to false for each pass
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true; // Set swapped to true if a swap occurred
            }
        }

        // If no two elements were swapped in inner loop, the array is sorted
        if (!swapped) {
            break;
        }
    }
}

int main() {
    std::vector<int> my_list = {5, 1, 4, 2, 8};

    std::cout << "Original list: ";
    printArray(my_list);

    bubbleSortOptimized(my_list);
    return 0;
}