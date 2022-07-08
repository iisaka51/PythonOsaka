query = select(c for c in Customer
            if sum(o.total_price for o in c.orders) > 2)

# print(query)
