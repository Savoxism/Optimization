#define MAX 5

typedef struct Queue {
    int data[MAX];
    int front, rear;
    int count
} Queue;

int Enqueue(Queue *q, int x) {
    if (q->count < MAX) {
        q->data[q->rear] = x;
        q -> rear = (q -> rear + 1) % MAX;
        q->count++;
        return 1;
    }
    return 0;
}

int Dequeue(Queue *q) {
    if (q->count > 0) {
        int x = q->data[q->front];
        q->front = (q->front+1) % MAX;
        q->count--;
        return x;
    }
    return -1;
}