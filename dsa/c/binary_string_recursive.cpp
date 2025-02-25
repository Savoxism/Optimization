#include <iostream>
using namespace std;

int n, solutionCount;
int a[100];

void PrintSolution() {
    int i, j;
    solutionCount++;
    cout<<"String # " <<solutionCount<<": ";
    for (i=1; i < n; i++) {
        j = a[i];
        cout<<j<<" ";
    }
    cout<<endl;
}

void Try(int k) {
    for (int j = 0; j <= 1; j++) {
        a[k] = j;
        // Check if a complete solution has been found 
        if (k == n) PrintSolution();
        else Try(k+1);
    }
}

int main()
{
    cout<<"Enter n = "; cin>>n;
    solutionCount = 0; Try(1); // always call Try(1) first 
    cout<<"Number of strings "<<solutionCount;
}