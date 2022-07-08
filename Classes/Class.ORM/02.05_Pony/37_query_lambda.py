v1 = Customer.select(lambda c: sum(c.orders.total_price) > 100)

# print(v1)
# print(v1.first())
