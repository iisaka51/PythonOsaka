ed_user.name='Edwardo'
fake_user = User(name='fakeuser',
                 fullname='Invalid',
                 nickname='12345')

session.add(fake_user)
