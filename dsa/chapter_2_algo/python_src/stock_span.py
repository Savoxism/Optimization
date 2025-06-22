
# def calculate_span(prices):
#     n = len(prices)
#     span = [0] * n

#     for i in range(n):
#         span[i] = 1
#         j = i - 1
#         while j >= 0 and prices[j] <= prices[i]:
#             span[i] += 1
#             j -= 1
#     return span

def calculate_span(prices):
    n = len(prices)
    span = [0] * n
    stack = []

    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        
        # if stack if empty -> prices[i] > all previous prices
        if not stack:
            span[i] = i + 1
        else:
            span[i] = i - stack[-1]
        
        stack.append(i)

    return span

prices = [100, 60, 70, 65, 80, 85]
span = calculate_span(prices)
print(max(span))