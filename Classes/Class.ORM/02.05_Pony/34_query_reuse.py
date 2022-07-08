query3 = select(customer.name for customer in query2
            if customer.country == 'USA')

# print(query3)
