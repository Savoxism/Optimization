#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// node definition
typedef struct Node {
    char data;
    struct Node* next;
} Node;

// Stack
typedef struct {
    Node* top;
} Stack;

// Queue
typedef struct {
    Node* front;
    Node* rear;
} Queue;

// function to create new node
Node* createNode(char c) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = c;
    newNode->next = NULL;
    return newNode;
}

// Stack operation
void push(Stack* s, char c) {
    Node* newNode = createNode(c);
    newNode->next = s->top;
    s->top = newNode;
}

char pop(Stack* s) {
    if (s->top == NULL) return '\0';
    Node* temp = s->top;
    char val = temp->data;
    s->top = temp->next;
    free(temp);
    return val;
}

// Queue operation
void enqueue(Queue* q, char c) {
    Node* newNode = createNode(c);
    if (q->rear == NULL) {
        q->front = q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

char dequeue(Queue* q) {
    if (q->front == NULL) return '\0';
    Node* temp = q->front;
    char val = temp->data;
    q->front = temp->next;
    if (q->front == NULL) q->rear = NULL;
    free(temp);
    return val;
}

int isPalindrome(const char* str) {
    Stack s = {NULL};
    Queue q = {NULL, NULL};

    // adding elements into stack and queue 
    for (int i = 0; str[i] != '\0'; i++) {
        if (isalpha(str[i])) {
            char c = tolower(str[i]);
            push(&s, c);
            enqueue(&q, c);
        }
    }

    while (s.top != NULL && q.front != NULL) {
        char c1 = pop(&s);
        char c2 = dequeue(&q);
        if (c1 != c2) return 0;
    }
    return 1;
}

int main() {
    char input[1000];
    printf("enter string: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = '\0';

    if (isPalindrome(input)) {
        printf("✅ Chuỗi là palindrome!\n");
    } else {
        printf("❌ Chuỗi không phải là palindrome.\n");
    }

    return 0;
}


// code to run: gcc -o main palindrome_queue.c