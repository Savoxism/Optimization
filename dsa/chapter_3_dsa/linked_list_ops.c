#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char name[50];
    char phone[20];
    struct Node *next;
} Node;

Node* make_node(const char*name, const char*phone) {
    Node* p = malloc(sizeof(Node));
    strcpy(p->name, name);
    strcpy(p->phone, phone);
    p->next = NULL;
    return p;
}

void traverse(Node* head) {
    Node* current = head;
    while (current) {
        printf("Name: %s, Phone: %s\n", current->name, current->phone);
        current = current->next;
    }
}

int main(void) {
    Node* head = make_node("Alice",   "123-4567");
    head->next = make_node("Bob",     "987-6543");
    head->next->next = make_node("Charlie", "555-6789");

    
    traverse(head);

    Node* tmp;
    while (head) {
        tmp = head;
        head = head->next;
        free(tmp);
    }
    return 0;
}