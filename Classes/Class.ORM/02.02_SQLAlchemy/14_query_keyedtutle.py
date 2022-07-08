all_users = session.query(User, User.name).all()
for row in all_users:
   print(row.User, row.name)
