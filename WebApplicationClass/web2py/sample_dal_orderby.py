people=db().select(db.person.name,orderby=db.person.name)
order=db.person.name|~db.person.birth
people=db().select(db.person.name,orderby=order)
people=db().select(db.person.name,orderby=order, groupby=db.person.name)
people=db().select(db.person.name,orderby=order,limitby=(0,100))
