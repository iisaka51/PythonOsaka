import pickledb

db = pickledb.load('data.db', False)

things = ['one', 'two', 'three', 'four', 'five']

for i, thing in enumerate(things, start=1):
    db.set(thing, i)

db.dump()
