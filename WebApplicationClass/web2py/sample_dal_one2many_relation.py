tmp=db.define_table('dog',
                    Field('name'),
                    Field('birth','date'),
                    Field('owner',db.person),
                    migrate='test_dog.table')
dog_id=db.dog.insert(name='Snoopy',birth=None,owner=person_id)
