#include <stdio.h>
#include <limits.h>

#define N 10

int n = 4;
int distanceMatrix[N][N] = {
    {0, 10, 15, 20},
    {10, 0, 35, 25},
    {15, 35, 0, 30},
    {20, 25, 30, 0}
};
int visited[N];
int path[N], bestPath[N];
int minCost = INT_MAX;

void TSP(int currPos, int currLen, int currCost) {
    if (currLen == n) {
        if (distanceMatrix[currPos][0]) {
            int totalCost = currCost + distanceMatrix[currPos][0];
            if (totalCost < minCost) {
                minCost = totalCost;
                for (int i = 0; i < n; i++) {
                    bestPath[i] = path[i];
                }
            }
            return;
        }
    }
    
    for (int next = 0; next < n; next++) {
        if (!visited[next] && distanceMatrix[currPos][next]) {
            visited[next] = 1;
            path[currLen] = next;
            TSP(next, currLen + 1, currCost + distanceMatrix[currPos][next]);
            visited[next] = 0;
        }
    }
}

int main() {
    for (int i = 0; i < n; i++) visited[i] = 0;
    path[0] = 0;
    visited[0] = 1;

    TSP(0, 1, 0);

    printf("Minimum cost: %d\nPath: ", minCost);
    for (int i = 0; i < n; i++) printf("%d ", bestPath[i]);
    printf("0\n"); 
    return 0;
}


