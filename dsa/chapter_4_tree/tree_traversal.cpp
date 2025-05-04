#include <iostream>
#include <unordered_map>
#include <vector>
#include <sstream>
using namespace std;


struct Node {
    int id;
    Node* firstChild = nullptr;
    Node* nextSibling = nullptr;
    Node(int _id) : id(_id) {}
};

unordered_map<int, Node*> nodes;
Node* root = nullptr;

void makeRoot(int u) {
    root = new Node(u);
    nodes[u] = root;
}

void insert(int u, int v) {
    Node* parent = nodes[v];
    Node* newNode = new Node(u);
    nodes[u] = newNode;

    if (!parent->firstChild) {
        parent ->firstChild = newNode;
    } else {
        Node* child = parent->firstChild;
        while (child->nextSibling) {
            child = child->nextSibling;
        }
        child->nextSibling = newNode;
    }
}

// root -> left -> right
void preorder(Node* node, vector<int>& res) {
    if (!node) return;
    res.push_back(node->id); // nút hiện tại 
    preorder(node->firstChild, res);
    preorder(node->nextSibling, res);
}

// left -> root -> right
void inorder(Node* node, vector<int>& res) {
    if (!node) return;
    if (node->firstChild) {
        inorder(node->firstChild, res);
    }
    res.push_back(node->id);
    if (node->firstChild) {
        Node* sibling = node->firstChild->nextSibling;
        while (sibling) {
            inorder(sibling, res);
            sibling = sibling->nextSibling;
        }
    }
}

// left -> right -> root
void postorder(Node* node, vector<int>& res) {
    if (!node) return;
    postorder(node->firstChild, res);
    res.push_back(node->id);
    postorder(node->nextSibling, res);
}

int main() {
    string line;
    while (getline(cin, line)) {
        if (line == "*") break;

        stringstream ss(line);
        string cmd;
        ss >> cmd;

        if (cmd == "MakeRoot") {
            int u; ss >> u;
            makeRoot(u);
        } else if (cmd == "Insert") {
            int u, v; ss >> u >> v;
            insert(u, v);
        } else if (cmd == "PreOrder") {
            vector<int> res;
            preorder(root, res);
            for (int i = 0; i < res.size(); ++i) {
                if (i) cout << " ";
                cout << res[i];
            }
            cout << "\n";
        } else if (cmd == "InOrder") {
            vector<int> res;
            inorder(root, res);
            for (int i = 0; i < res.size(); ++i) {
                if (i) cout << " ";
                cout << res[i];
            }
            cout << "\n";
        } else if (cmd == "PostOrder") {
            vector<int> res;
            postorder(root, res);
            for (int i = 0; i < res.size(); ++i) {
                if (i) cout << " ";
                cout << res[i];
            }
            cout << "\n";
        }
    }
    return 0;
}
