all_users = session.query(User).order_by(User.id)

for user in all_users:
    print(user.fullname)
