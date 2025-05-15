#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_SIZE 100
typedef int ItemType;

// Array representation
typedef struct {
    ItemType items[MAX_SIZE];
    int front;
    int rear;
    int count;
} Queue;

Queue* init() {
    Queue* Q = (Queue*)malloc(sizeof(Queue));
    Q->front = 0;
    Q->rear = -1;
    Q->count = 0;
    return Q;
}

bool isEmpty(Queue* Q) {
    return Q->count == 0;
}

bool isFull(Queue* Q) {
    return Q->count == MAX_SIZE;
}

ItemType frontQ(Queue* Q) {
    if (isEmpty(Q)) {
        printf("Error: Queue is empty\n");
        return -1;
    }
    return Q->items[Q->front];
}

void enqueue(Queue* Q, ItemType x) {
    if (isFull(Q)) {
        printf("Error: Queue is full\n");
        return;
    }
    Q->rear = (Q->rear + 1) % MAX_SIZE;
    Q->items[Q->rear] = x;
    Q->count++;
}

ItemType dequeue(Queue* Q) {
    if (isEmpty(Q)) {
        printf("Error: Queue is empty\n");
        return -1;
    }
    ItemType x = Q->items[Q->front];
    Q->front = (Q->front + 1) % MAX_SIZE;
    Q->count--;
    return x;
}

void print(Queue* Q) {
    if (isEmpty(Q)) {
        printf("Queue is empty\n");
        return;
    }
    printf("Queue: ");
    int current = Q->front;
    for (int i = 0; i < Q->count; i++) {
        printf("%d ", Q->items[current]);
        current = (current + 1) % MAX_SIZE;
    }
    printf("\n");
}

int sizeQ(Queue* Q) {
    return Q->count;
}

// Example usage
int main() {
    Queue* Q = init();
    
    enqueue(Q, 10);
    enqueue(Q, 20);
    enqueue(Q, 30);
    
    print(Q);  // Queue: 10 20 30
    
    printf("Front element: %d\n", frontQ(Q));  // Front element: 10
    printf("Queue size: %d\n", sizeQ(Q));      // Queue size: 3
    
    printf("Dequeued: %d\n", dequeue(Q));      // Dequeued: 10
    
    print(Q);  // Queue: 20 30
    
    free(Q);
    return 0;
}