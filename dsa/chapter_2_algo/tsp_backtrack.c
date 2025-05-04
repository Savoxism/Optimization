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

// recursion
void Try(int k) {
    if (k == n) {  
        int total_cost = current_cost + cost_matrix[path[k - 1]][0];  
        if (total_cost < best_cost) {
            best_cost = total_cost;  
        }
        return;
    }

    for (int next_city = 1; next_city < n; next_city++) {  
        if (!visited[next_city]) {  
            visited[next_city] = true;
            path[k] = next_city;
            current_cost += cost_matrix[path[k - 1]][next_city];

            if (current_cost < best_cost) {  
                Try(k + 1);
            }

            // Backtrack
            visited[next_city] = false;
            current_cost -= cost_matrix[path[k - 1]][next_city];
        }
    }
}

int main() {
    // Read input
    scanf("%d", &n); 

    // cost matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            scanf("%d", &cost_matrix[i][j]);
        }
    }

    path[0] = 0;  
    visited[0] = true;
    Try(1);
    printf("%d\n", best_cost);
    return 0;
}
