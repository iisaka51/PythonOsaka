users = session.query(User)

ed = users.filter_by(name='ed').first()
