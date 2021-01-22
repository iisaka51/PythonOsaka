all_users =  session.query(User.name).filter(User.fullname=='Ed Jones')
for name, in all_users:
   print(name)
