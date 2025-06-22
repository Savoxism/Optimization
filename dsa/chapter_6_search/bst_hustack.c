#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

Node* insert(Node* root, int k) {
    if (root == NULL) {
        Node* newNode = (Node*)malloc(sizeof(Node));
        newNode->key = k;
        newNode->left = newNode->right = NULL;
        return newNode;
    }
    if (k < root->key) {
        root->left = insert(root->left, k);
    } else if (k > root->key) {
        root->right = insert(root->right, k);
    }
    return root;
}

void preorder(Node* root) {
    if (root == NULL) return;
    printf("%d ", root->key);
    preorder(root->left);
    preorder(root->right);
}

int main() {
    Node* root = NULL;
    char line[100];
    int k;
    while (fgets(line, sizeof(line), stdin)) {
        if (line[0] == '#') break;
        if (sscanf(line, "insert %d", &k) == 1) {
            root = insert(root, k);
        }
    }
    preorder(root);
    printf("\n");
    // Free memory is optional here (exercise)
    return 0;
}