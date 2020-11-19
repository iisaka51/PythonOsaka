set=(1,2,3)
rows=db(db.paper.id.belongs(set)).select(db.paper.ALL)
print(rows[0].title)
