#include <iostream>
#include <vector>
#include <algorithm>

void selectionSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; ++i) {
        int min_index = i;
        for (int j = i + 1; j < n;
        ++j) {
            if (arr[j] < arr[min_index]) {
                min_index = j;
            }
        }
        
        if (min_index != i) {
            std::swap(arr[i], arr[min_index]);
        }
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
    std::vector<int> my_list = {6, 4, 1, 5, 3, 2};

    std::cout << "Original list: ";
    printArray(my_list);

    selectionSort(my_list);

    std::cout << "Sorted list: ";
    printArray(my_list);

    return 0;
}