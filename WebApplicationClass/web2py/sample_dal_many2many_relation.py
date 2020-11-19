tmp=db.define_table('author',
                    Field('name'),
                    migrate='test_author.table')

tmp=db.define_table('paper',
                    Field('title'),
                    migrate='test_paper.table')

tmp=db.define_table('authorship',
                    Field('author_id',db.author),
                    Field('paper_id',db.paper),
                    migrate='test_authorship.table')

aid=db.author.insert(name='Massimo')
pid=db.paper.insert(title='QCD')
tmp=db.authorship.insert(author_id=aid,paper_id=pid)
