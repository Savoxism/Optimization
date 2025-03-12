#include <stdio.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_N 50

int n, M; // number of cities and cost limit
int cost_matrix[MAX_N][MAX_N];
int path[MAX_N];
bool visited[MAX_N]; // mark visited cities
int current_cost = 0; // current tour cost 
int valid_tour_count = 0; // counter for valid tours

void Try(int k) {
    if (k == n) { // all cities visited
        int total_cost = current_cost + cost_matrix[path[k - 1]][0];
        if (total_cost <= M) {
            valid_tour_count++;
        }
        return;
    }

    for (int i = 1; i < n; i++) {
        if (!visited[i]) {
            visited[i] = true;
            path[k] = i;
            current_cost += cost_matrix[path[k - 1]][i];

            if (current_cost <= M) {
                Try(k + 1);
            }

            visited[i] = false;
            current_cost -= cost_matrix[path[k - 1]][i];
        }
    }
}

int main() {
    // Read input
    scanf("%d %d", &n, &M);  

    // Read cost matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            scanf("%d", &cost_matrix[i][j]);
        }
    }

    path[0] = 0;  
    visited[0] = true;
    Try(1);
    printf("%d\n", valid_tour_count);
    return 0;
}