#include<iostream>
using namespace std;

int n, countt;
int a[100];

void PrintSolution() {
    int i, j;
    countt++;
    cout<<"String # " <<countt<<": ";
    for (i = 1; i <= n; i++) {
        j = a[i];
        cout<<j<<"  ";
    }
    cout <<endl;
}

void Try(int k) {
    for (int j = 0; j<= 1; j++) {
        a[k] = j;
        if (k == n ) PrintSolution();
        else Try(k+1);
    }
}

int main() {
    cout<<"Enter n = ";cin>>n;
    countt = 0; Try(1);
    cout<<"Number of strings "<<countt;
}