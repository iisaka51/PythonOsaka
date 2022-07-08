from peewee import *
import datetime

db = SqliteDatabase('note.db')

class BaseModel(Model):
    class Meta:
        database = db
        db_table = 'notes'

class Note(BaseModel):
    text = CharField()
    created = DateField(default=datetime.date.today)


def populate_database():

    data = [
        {'text': 'Went to buy beer', 'created': datetime.date(2021, 8, 17)},
        {'text': 'Drinking beer', 'created': datetime.date(2021, 8, 17)},
        {'text': 'Making pizza', 'created': datetime.date(2021, 8, 19)},
        {'text': 'Eating pizza' }
    ]

    Note.create_table()

    notes = Note.insert_many(data)
    notes.execute()

def clear_table():
    Note.drop_table()


if __name__ == '__main__':
    populate_database()
