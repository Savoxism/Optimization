#include<bits/stdc++.h>
using namespace std;
 
struct node{
    int data;
    node *left, *right;
};
 
int sum = 0;
 
node *makeNode(int id) {
    node *newNode = (node*) malloc(sizeof(node));
    if (newNode == NULL) {
        printf("Out of mem"); exit(1);
    }
    newNode->data = id; newNode->left = NULL; newNode->right = NULL;
    return newNode;
}
 
node *findNode(node *root, int v) {//find node with data = v (use preorder)
    if (root == NULL) return NULL;
    if (root->data == v) return root;
    node *res = findNode(root->left, v);
    if (res != NULL) return res;
    else
        return findNode(root->right, v);
}
 
bool isBST(node *root){//return true if it is BST; otherwise return false
      if (root == NULL) return 1;
      if (root->left != NULL && root->left->data > root->data) return 0;
      if (root->right != NULL && root->right->data < root->data) return 0;
      return isBST(root->left) && isBST(root->right);
}
void addLeft(node *root, int u, int v) {//create u and make u as left child of v
     node *nodeu = findNode(root, u); if (nodeu != NULL) return;
     node * nodev = findNode(root, v); if (nodev == NULL) return;
     if (nodev->left != NULL) return;
     nodev->left = makeNode(u);
     sum += u;
}
void addRight(node *root, int u, int v) {//create u and make u as right child of v
     node *nodeu = findNode(root, u); if (nodeu != NULL) return;
     node * nodev = findNode(root, v); if (nodev == NULL) return;
     if (nodev->right != NULL) return;
     nodev->right = makeNode(u);
     sum += u;
}
 
int main() {
   char cmd[20];
   node *root;
   while (1) {
       scanf("%s",cmd);
       if (strcmp(cmd, "*") ==0) break;
       if (strcmp(cmd, "MakeRoot") == 0) {
            int id; scanf("%d", &id);
            root = makeNode(id);
            sum +=id;
       }
       else if (strcmp(cmd, "AddLeft") == 0) {
           int u, v; scanf("%d %d", &u, &v); addLeft(root, u, v);
       }
       else if (strcmp(cmd, "AddRight") == 0) {
           int u, v; scanf("%d %d", &u, &v); addRight(root, u, v);
       }
   }
   bool res = isBST(root);
   printf("%d %d", res, sum);
 
}
 