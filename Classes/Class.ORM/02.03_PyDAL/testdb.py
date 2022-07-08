from pydal import DAL, Field
from test_data import test_data

db=DAL("sqlite://test.db")

person = db.define_table('person',
                Field('name', required=True),
                Field('age', type='integer'),
                Field('belongs'),
                migrate='person.table')

if __name__ == '__main__':
    for data in test_data:
        person.insert(name=data['name'],
                  age=data['age'],
                  belongs=data['belongs'])

    db.commit()
    db.close()
