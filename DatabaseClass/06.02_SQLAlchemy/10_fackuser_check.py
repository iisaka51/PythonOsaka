checklist = ['Edwardo', 'fakeuser']
session.query(User).filter(User.name.in_(checklist)).all()

# session.rollback()
