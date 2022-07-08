db_config = {
    'scheme': 'mysql',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'data'
}

from peewee_ext import connect

db = connect(**db_config)
