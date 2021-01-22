checklist = ['Edwardo', 'fakeuser']
session.query(User).filter(User.name.in_(checklist)).all()

# ed.name
# fake_user in session
