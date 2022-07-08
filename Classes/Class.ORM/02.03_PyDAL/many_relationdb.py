from pydal import DAL, Field

db = DAL("sqlite://manyrel.db")

db.define_table('person',
                Field('name'),
                migrate='manyrel_person.table')

db.define_table('thing',
                Field('name'),
                migrate='manyrel_thing.table')

db.define_table('ownership',
                Field('person', 'reference person'),
                Field('thing', 'reference thing'),
                migrate='manyrel_ownership.table')

if __name__ == '__main__':
    person_data = [dict(name='Alex'), dict(name='Bob'), dict(name='Carl')]
    thing_data  = [dict(name='Boat'), dict(name='Chair'), dict(name='Shoes')]

    db.person.bulk_insert(person_data)
    db.thing.bulk_insert(thing_data)

    db.ownership.insert(person=1, thing=1)  # Alex owns Boat
    db.ownership.insert(person=1, thing=2)  # Alex owns Chair
    db.ownership.insert(person=2, thing=3)  # Bob owns Shoes
    db.ownership.insert(person=3, thing=1)  # Curt owns Boat too

    db.commit()
    db.close()
