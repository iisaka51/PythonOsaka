from customerdb import *

customer = (Customer
            .select()
            .where(Customer.name == 'Jack Bauer')
            .get())

def func(data):
    for d in data:
        print(f'{d.id} {d.created}')

# print(customer)
# print(customer.name)
# func(customer.reservations)
# print(customer.reservations)
