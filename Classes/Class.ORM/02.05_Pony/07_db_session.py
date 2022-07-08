@db_session
def print_person_name(person_id):
    p = Person[person_id]
    print(p.name)

@db_session
def add_car(person_id, make, model):
    Car(make=make, model=model, owner=Person[person_id])
