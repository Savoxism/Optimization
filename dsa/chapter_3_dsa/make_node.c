#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

Node* makeNode(int value) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = value;
    newNode->next = NULL;
    return newNode;
}

Node *insertToHead(Node* head, int X) {
    Node *new_node = makeNode(X);
    new_node->next = head; // connect new node to current head
    head = new_node; // head is updated to point to new node 
    return head; // return because this is pass by value 
}

Node *Insert_After(Node *cur, int X) {
    Node *new_node = makeNode(X);
    new_node->next = cur->next; // connect new node to the next of current node
    cur->next = new_node; // current node points to new node
    return new_node; // return the new node    
}


void printList(Node* head) {
    Node* cur = head;
    while (cur != NULL) {
        printf("%d", cur->data);  
        cur = cur->next;
        if (cur != NULL) {
            printf(" -> ");  
        }
    }
    printf("\n");  
}


int main() {
    Node* head = NULL; // Start with an empty list
    int n, value;
    printf("Enter the number of nodes: ");
    scanf("%d", &n);

    printf("Enter %d integers:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &value);
        head = insertToHead(head, value); // Insert each value at the head
    }

    printList(head);

    Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next; // Move to the next node
        free(temp); // Free the old head
    }
    return 0;
}