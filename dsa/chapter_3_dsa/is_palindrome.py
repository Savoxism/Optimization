string = input()
n = len(string)

for i in range(n // 2):
    if string[i] != string[-i - 1]:
        print(0)
    break

print(1)

