#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    float data;
    struct Node *next;
} Node;

typedef struct Stack {
    Node *top;
} Stack;

Stack* StackConstruct() {
    Stack* s = (Stack*)malloc(sizeof(Stack));
    if (s != NULL) {
        s->top = NULL;
    }
    return s;
}

int StackEmpty(Stack* s) {
    return (s->top == NULL);
}

int StackFull(Stack* s) {
    // In linked list implementation, stack is never full
    // unless we run out of memory
    return 0;
}

int StackPush(Stack* s, float* item) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        return 0;
    }

    newNode->data = *item;
    newNode->next = s->top;
    s->top = newNode;
    return 1;
}

float pop(Stack* s) {
    if (StackEmpty(s)) {
        return -1;
    }

    Node* temp = s->top;
    float data = temp->data;
    s->top = s->top->next;
    free(temp);
    return data;
}

void Disp(Stack* s) {
    if (StackEmpty(s)) {
        printf("Stack is empty\n");
        return;
    }

    Node* current = s->top;
    while (current != NULL) {
        printf("%.2f\n", current->data);
        current = current->next;
    }
}

int main() {
    Stack* s = StackConstruct();
    float item1 = 10.5;
    float item2 = 20.5;
    float item3 = 30.5;
    
    StackPush(s, &item1);
    StackPush(s, &item2);
    StackPush(s, &item3);
    
    printf("After pushing three items:\n");
    Disp(s);
    
    printf("\nPopped item: %.2f\n", pop(s));
    printf("\nAfter popping one item:\n");
    Disp(s);
    
    return 0;
}