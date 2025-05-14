#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    float data;
    struct Node *next;
} Node;

typedef struct Stack {
    Node *top;
} Stack;

