def is_palindrome(string):
    n = len(string)
    for i in range(n // 2):
        if string[i] != string[- i - 1]:
            return 0
        break
    return 1

user_input = input()
print(is_palindrome(str(user_input)))
