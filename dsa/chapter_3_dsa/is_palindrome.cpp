#include <iostream>
#include <string>
using namespace std;

// g++ -std=c++17 -Wall is_palindrome.cpp -o is_palindrome
int is_palindrome(const string& str) {
    int n = str.size();

    for (int i = 0; i < n / 2; i++) {
        if (str[i] != str[n - i - 1]) {
            return 0;
        }
    }
    return 1;
}

int main() {
    string user_input;
    getline(cin, user_input);
    cout << is_palindrome(user_input) << endl;
    return 0;
}