for user in session.execute("select * from users"):
    print(user.name)
