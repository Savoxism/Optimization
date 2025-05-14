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

Node* insert_front(Node* head, const char* name, const char* phone) {
    Node* new_node = make_node(name, phone);
    new_node->next = head;
    return new_node;
}

Node* insert_after(Node* head, Node* cur, const char* name, const char* phone) {
    if (!cur) return head;
    Node* new_node = make_node(name, phone);
    new_node->next = cur->next;
    cur->next = new_node;
    return head;
}

Node* insert_before(Node* head, Node* cur, const char* name, const char* phone) {
    if (!cur) return head;
    if (cur == head) {
        return insert_front(head, name, phone);
    }

    // goes through the list
    Node* prev = head;
    while (prev->next && prev->next != cur) {
        prev = prev->next;
    }

    if (prev->next == cur) {
        Node* new_node = make_node(name, phone);
        new_node->next = cur;
        prev->next = new_node;
    }
    return head;
}

Node* insert_end(Node* head, const char* name, const char* phone) {
    Node* new_node = make_node(name, phone);
    if (!head) return new_node;
    Node* cur = head;
    while (cur->next) {
        cur = cur->next;
    }
    cur->next = new_node;
    return head;
}

Node* search(Node* head, const char* name) {
    Node* cur = head;
    while (cur) {
        if (strcmp(cur->name, name) == 0) {
            return cur;
        }
        cur = cur -> next;
    }
    return NULL;
}

Node* delete_node(Node* head, const char* name) {
    if (!head) return NULL;

    // Delete head
    if (strcmp(head->name, name) == 0) {
        Node* tmp = head;
        head = head->next;
        free(tmp);
        return head;
    }

    Node* prev = head;
    Node* cur = head->next;
    while (cur) {
        if (strcmp(cur->name, name) == 0) {
            prev->next = cur->next;
            free(cur);
            break;
        }
        // if not arrived at the desired name yet, move rightward 
        prev = cur;
        cur = cur->next;
    }
    return head;
}

// -------------------------------------------------------------------------------- // 
int main(void) {
    Node* head = make_node("Alice",   "123-4567");
    head->next = make_node("Bob",     "987-6543");
    head->next->next = make_node("Charlie", "555-6789");

    head = insert_front(head, "Zara", "111-2222");
    traverse(head);

    // search
    Node* found = search(head, "Bob");
    if (found) {
        printf("\nFound: %s, %s\n", found->name, found->phone);
    }

    // delete
    head = delete_node(head, "Alice");
    printf("\nAfter deleting Alice:\n");
    traverse(head);

    Node* tmp;
    while (head) {
        tmp = head;
        head = head->next;
        free(tmp);
    }
    return 0;
}