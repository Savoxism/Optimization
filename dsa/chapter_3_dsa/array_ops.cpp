#include <iostream>
using namespace std;

int arr[100] = {3, 7, 12, 18, 25};

int arr_size = 5;

bool search(int arr[], int size, int key) {
    for (int i = 0; i < size; i++) {
        if (arr[i] == key) {
            return true;
        }
    }
    return false;
}

int retrieve(int arr[], int size, int index) {
    if (index >= 0 && index < size) {
        return arr[index];
    }
    return -1;
}

void traverse(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

bool insert(int arr[], int &arr_size, int pos, int value) {
    if (pos < 0 || pos > arr_size) return false;

    // Shift elements to the right
    for (int i = arr_size; i > pos; i--) {
        arr[i] = arr[i-1];
    }
    arr[pos] = value;
    arr_size++;
    return true;
}

bool remove(int arr[], int &arr_size, int pos) {
    if (pos < 0 || pos >= arr_size) return false;

    // Shift elements to the left
    for (int i = pos; i < arr_size - 1; i++) {
        arr[i] = arr[i+1];
    }
    arr_size--;
    return true;
}

int main() {

    // Traverse
    traverse(arr, arr_size);

    // Insert
    insert(arr, arr_size, 2, 10);
    traverse(arr, arr_size);

    // Delete
    remove(arr, arr_size, 3);
    traverse(arr, arr_size);

    // Search
    cout << "Find 25? " << (search(arr, arr_size, 25) ? "Yes": "No") <<endl;

    // Retrieve 
    cout << "arr[1] = " << retrieve(arr, arr_size, 1) << endl;
    return 0;
}
