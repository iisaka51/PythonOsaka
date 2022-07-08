from pydal import DAL, Field

db=DAL("sqlite://dal_example.db")

tmp=db.define_table('person',
                    Field('id', 'integer'),
                    Field('name', 'string', length=32, required=True),
                    migrate='person.table')

person_id=db.person.insert(name="new_person")
db.commit()
