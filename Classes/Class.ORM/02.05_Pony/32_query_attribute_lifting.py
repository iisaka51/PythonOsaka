query = select(c for c in Customer
            if sum(c.orders.total_price) > 2)

# print(query)
