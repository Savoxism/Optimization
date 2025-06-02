void insertionSort(int a[], int size) {
    int k, pos, temp;
    for (k = 1; k < size; k++) {
        temp = a[k];
        pos = k;
        while ((pos > 0) && (a[pos-1] > temp)) {
            a[pos] = a[pos - 1];
            pos = pos - 1;
        }
        a[pos] = temp;
    }
}

void main() {
    int a[5] = {8, 4 ,3 ,2, 1};
    insertionSort(a, 5);
    for (int i = 0; i < 5; i++) {
        printf("%d \n", a[i]);
    }
}