from pydal import DAL, Field

db=DAL("sqlite://test.db")

tmp=db.define_table('person',
                    Field('name'),
                    Field('birth','date'),
                    migrate='test_person.table')

person_id=db.person.insert(name="Python",birth='2005-06-22')
person_id=db.person.insert(name="Massimo",birth='1971-12-21')

rows=db().select(db.person.ALL)
for row in rows:
    print(row.name)

me=db(db.person.id==person_id).select()[0]

