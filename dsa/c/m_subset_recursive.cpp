#include<iostream>
using namespace std;

int n, m, solutionCount;
int a[100];

void PrintSolution() {
    int i;
    solutionCount++;
    cout<<"Subset # "<<solutionCount<<": ";
    for (i=1; i <= m; i++) {
        cout<<a[i]<<" ";
    }
    cout<<endl;
}

void Try(int k) {
    int j;
    for (j = a[k-1] + 1; j <= n - m + k; j++) {
        a[k] = j;
        if (k == m) PrintSolution();
        else Try(k+1);
    }
}

int main()
{
    cout<<"Enter n = "; cin>>n;
    cout<<"Enter m = "; cin>>m;
    solutionCount = 0; a[0] = 0; Try(1); // always call Try(1) first 
    cout<<"Number of subsets "<<solutionCount;
}   