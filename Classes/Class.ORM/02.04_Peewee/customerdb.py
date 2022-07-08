from peewee import *
import datetime

db = SqliteDatabase('customer.db')

class Customer(Model):

    name = TextField()
    age = IntegerField()

    class Meta:
        database = db
        db_table = 'customers'

class Reservation(Model):

    customer = ForeignKeyField(Customer, backref='reservations')
    created = DateField(default=datetime.date.today)

    class Meta:
        database = db
        db_table = 'reservations'


def populate_database():

    customer_data = [
        { 'name': 'Jack Bauer',    'age': 55 },
        { 'name': "Chloe O'Brian", 'age': 0  },
        { 'name': 'Anthony Tony',  'age': 29 },
        { 'name': 'David Gilmour', 'age': 75 },
        { 'name': 'Ann Wilson',    'age': 71 },
        { 'name': 'Nacy Wilson',   'age': 67 },
    ]
    order_data = [
        { 'customer': 1, 'created': '2021-8-17' },
        { 'customer': 2, 'created': '2021-8-18' },
        { 'customer': 3, 'created': '2021-8-19' },
        { 'customer': 4, 'created': '2021-8-20' },
        { 'customer': 5, 'created': '2021-8-21' },
    ]

    Customer.create_table()
    Reservation.create_table()

    customers = Customer.insert_many(customer_data)
    customers.execute()
    reservations = Reservation.insert_many(order_data)
    reservations.execute()


if __name__ == '__main__':
    populate_database()

