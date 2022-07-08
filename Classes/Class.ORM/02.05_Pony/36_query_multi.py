v1 = select((c, sum(c.orders.total_price))
            for c in Customer if sum(c.orders.total_price) > 100)

# print(v1)
# print(v1.first())
