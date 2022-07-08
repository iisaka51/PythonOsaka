from peewee import *

DATABASE = 'tweepee.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('from_user', 'to_user'), True),
        )

class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()

def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])


if __name__ == '__main__':
    create_tables()
