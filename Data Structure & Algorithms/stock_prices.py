stock_prices = [100, 60, 70, 65, 80, 85]

# span = [0] * len(stock_prices)
# for i in range(len(stock_prices)):
#     for j in range(i-1, -1, -1):
#         if stock_prices[i] >= stock_prices[j]:
#             span[i] += 1
#         else:
#             break
# print(span)

def stock_span(prices):
    n = len(prices)
    span = [0] * n
    stack = []
    
    for i in range(n):
        while stack and stack[-1][1] <= prices[i]:
            stack.pop()
            
        span[i] = i + 1 if not stack else i - stack[-1][0]
        
        stack.append((i, prices[i]))
        
    return span

print(stock_span(stock_prices))
