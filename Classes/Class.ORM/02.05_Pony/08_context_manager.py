with db_session:
    p = Person(name='Kate', age=33)
    Car(make='Audi', model='R8', owner=p)

