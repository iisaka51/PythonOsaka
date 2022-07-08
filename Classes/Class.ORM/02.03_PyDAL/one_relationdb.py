from pydal import DAL, Field

db = DAL("sqlite://onerel.db")

db.define_table('person',
                Field('name'),
                migrate='onerel_person.table')

db.define_table('car',
                Field('name'),
                Field('owner_id', 'reference person'),
                migrate='onerel_car.table')

if __name__ == '__main__':
    db.person.insert(name='Alex')
    db.person.insert(name='Bob')
    db.person.insert(name='Carl')

    db.car.insert(name='Mustang Cobra', owner_id=1)
    db.car.insert(name='Corvette Stingray', owner_id=1)
    db.car.insert(name='Dodge Viper ', owner_id=2)

    db.commit()
    db.close()
