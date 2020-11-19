from collections import deque

basket = deque()

basket.append('apple')
basket.append('banana')
basket.append('orange')

last_item = basket.pop()
print(last_item)
print(basket)

first_item = basket.popleft()
print(first_item)
print(basket)
