authored_papers=db((db.author.id==db.authorship.author_id) &
                   (db.paper.id==db.authorship.paper_id))

rows=authored_papers.select(db.author.name,db.paper.title)
for row in rows:
    print(f'{row.author.name} {row.paper.title}')
