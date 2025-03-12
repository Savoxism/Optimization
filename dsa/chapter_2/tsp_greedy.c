#include <stdio.h>
#include <limits.h>
#include <stdbool.h>

#define MAX_N 100

int n;
int cost_matrix[MAX_N][MAX_N]; // stores the cost between cities

// Read input 
void read_input() {
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            scanf("%d", &cost_matrix[i][j]);
        }
    }
}

int greedy_tsp() {
    bool visited[MAX_N] = {false};
    int current_city = 0; // start from city 0 
    int total_cost = 0;

    for (int i = 0; i < n - 1; i++) {
        visited[current_city] = true;
        int min_cost = INT_MAX;
        int next_city = -1;

        for (int neighbor = 0; neighbor < n; neighbor++) {
            if (!visited[neighbor] && cost_matrix[current_city][neighbor] < min_cost) {
                min_cost = cost_matrix[current_city][neighbor];
                next_city = neighbor;
            }
        }
        if (next_city != -1) {
            total_cost += min_cost;
            current_city = next_city;
        }
    }
    total_cost += cost_matrix[current_city][0]; // return to city 0
    return total_cost;
}


int main() {
    read_input();  
    int total_cost = greedy_tsp();
    printf("%d\n", total_cost);
    return 0;
}



