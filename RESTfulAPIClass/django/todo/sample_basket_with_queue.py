from queue import Queue

basket = Queue()

basket.put('apple')
basket.put('banana')
basket.put('orange')

last_item = basket.get()
print(last_item)
print(basket)

first_item = basket.popleft()
print(first_item)
print(basket)
