#include <stdio.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_N 50

int n;
int cost_matrix[MAX_N][MAX_N];
int best_cost = INT_MAX;
int current_cost = 0;
int path[MAX_N];
bool visited[MAX_N];
int min_edge = INT_MAX;

// find the smallest non-zero edge cost in the given cost matrix 
void find_min_edge() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i != j && cost_matrix[i][j] < min_edge) {
                min_edge = cost_matrix[i][j];
            }
        }
    }
}

void Try(int k) {
    if (k == n) {
        int total_cost = current_cost + cost_matrix[path[k - 1]][0];
        if (total_cost < best_cost) {
            best_cost = total_cost;
        }
        return;
    }

    for (int i = 1; i < n; i++) {
        if (!visited[i]) {
            int expected_cost = current_cost + cost_matrix[path[k-1]][i] + (n - k) * min_edge;
            if (expected_cost < best_cost) {
                visited[i] = true;
                path[k] = i;
                current_cost += cost_matrix[path[k-1]][i];

                Try(k + 1);

                // backtrack
                visited[i] = false;
                current_cost -= cost_matrix[path[k-1]][i];
            }
        }
    }
}

int main() {
    scanf("%d", &n); 

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            scanf("%d", &cost_matrix[i][j]);
        }
    }

    find_min_edge();  
    path[0] = 0;  
    visited[0] = true;
    Try(1);  
    printf("%d\n", best_cost); 
    return 0;
}
