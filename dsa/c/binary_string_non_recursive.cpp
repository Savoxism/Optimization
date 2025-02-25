#include<iostream>
using namespace std;
int n, solutionCount, k;

int a[100], s[100];

void PrintSolution() {
    int i, j;
    solutionCount++;
    cout<<"String # "<<solutionCount<<": ";
    for (i=1; i <= n; i++) {
        cout <<a[i]<<" ";
    }
    cout<<endl;
}

void GenerateString() {
    k = 1; s[k] = 0;
    while (k > 0) {
        while (s[k] <= 1) {
            a[k] = s[k];
            s[k] = s[k] + 1;
            if (k == n) PrintSolution();
            else {
                k = k + 1;
                s[k] = 0;
            }
        }
        k = k - 1; // Backtrack
    }
}
