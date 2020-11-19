from pydal import DAL, Field

db = DAL('sqlite://test.db', folder='dbs')
db.define_table('cars', Field('name'), Field('price', 'integer'))

rows = db(db.cars).select()
print(rows.as_json())
