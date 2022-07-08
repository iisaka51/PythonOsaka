import pickledb

db = pickledb.load('data.db', False)

for k in db.getall():
    print(k, db.get(k))
