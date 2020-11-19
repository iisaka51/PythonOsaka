nested_select=db()._select(db.authorship.paper_id)
rows=db(db.paper.id.belongs(nested_select)).select(db.paper.ALL)
print(rows[0].title)
