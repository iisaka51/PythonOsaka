all_users = session.query(User.name, User.fullname)
for name, fullname in all_users:
    print(name, fullname)
