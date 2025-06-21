void minHeapify(int A[], int i, int heapSize) {
    int l = left(i);
    int r = right(i);
    int smallest = i;
    if (l < heapSize && A[l] < A[i]) smallest = l;
    if (r < heapSize && A[r] < A[smallest]) smallest = r;
    if (smallest != i)
    {
        swap(A[i], A[smallest]);
        minHeapify(A, smallest, heapSize);
    }
}