#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int key;
    struct TreeNode *left, *right, *parent;
} TreeNode;

TreeNode *root = NULL;

// create new node
TreeNode* create_new(int key) {
    TreeNode *node = (TreeNode*)malloc(sizeof(TreeNode));
    node->key = key;
    node->left = node->right = node->parent = NULL;
    return node;
}

// searching
TreeNode* search(TreeNode *node, int target) {
    if (node == NULL || node->key == target) {
        return node;
    }

    if (target < node->key) return search(node->left, target);

    else return search(node->right, target);
}

// Find max, min
TreeNode* find_min(TreeNode *node) {
    while (node && node->left) {
        node = node->left;
    }
    return node;
}

TreeNode* find_max(TreeNode *node) {
    while (node && node->right)
        node = node->right;
    return node;
}

// Traversal, intially points to the root of the BST 
void inorder(TreeNode *node) {
    if (node) {
        inorder(node->left);
        print("%d", node->key);
        inorder(node->right);
    }
}

void preorder(TreeNode *node) {
    if (node) {
        printf("%d", node->key);
        preorder(node->left);
        preorder(node->right);
    }
}

void postorder(TreeNode *node) {
    if (node) {
        postorder(node->left);
        postorder(node->right);
        printf("%d ", node->key);
    }
}

// Predecessor & Successor 
TreeNode* sucessor(TreeNode *x) {
    TreeNode *y;
    if (x->right != NULL) {
        return find_min(x->right);
    }
    y = x->parent;
    while (y != NULL && x == y->right) {
        x = y;
        y = y->parent;
    }
    return y;
}

TreeNode* predecessor(TreeNode *x) {
    TreeNode *y;
    if (x->left != NULL) {
        return find_max(x->left);
    }
    y = x->parent;
    while (y != NULL && x == y->left) {
        x = y;
        y = y->parent;
    }
    return y;
}

// Insert & Delete
void insert(int key) {
    TreeNode *new_node = create_new(key);
    TreeNode *y = NULL;
    TreeNode *x = root;

    // keeping the trailing path
    while (x) {
        y = x;
        if (key < x->key) {
            x = x->left;
        }
        else {
            x = x->right;
        }
    }

    new_node->parent = y; 

    // insertion process
    if (y == NULL) {
        root = new_node;
    } else if (key < y->key) {
        y->left = new_node;
    } else {
        y->right = new_node;
    }
}

void transplant(TreeNode *u, TreeNode *v) {
    if (u->parent == NULL) {
        root = v;
    } else if (u == u->parent->left) {
        u->parent->left = v;
    } else {
        u->parent->right = v;
    }
    if (v)
        v->parent = u->parent;
}

void delete(int key) {
    TreeNode *z = search(root, key);
    if (z == NULL)
        return;
    if (z->left == NULL) {
        transplant(z, z->right);
    } else if (z->right == NULL) {
        transplant(z, z->left);
    } else {
        TreeNode *y = find_min(z->right);
        if (y->parent != z) {
            transplant(y, y->right);
            y->right = z->right;
            y->right->parent = y;
        }
        transplant(z, y);
        y->left = z->left;
        y->left->parent = y;
    }
    free(z);
}


// TESTING
int main() {
    int keys[] = {15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9};
    int n = sizeof(keys) / sizeof(keys[0]);
    for (int i = 0; i < n; i++)
        insert(keys[i]);

    printf("Inorder trước khi xóa: ");
    inorder(root);
    printf("\n");

    delete(6);
    delete(15);

    printf("Inorder sau khi xóa: ");
    inorder(root);
    printf("\n");

    printf("Preorder: ");
    preorder(root);
    printf("\n");

    printf("Postorder: ");
    postorder(root);
    printf("\n");

    return 0;
}













