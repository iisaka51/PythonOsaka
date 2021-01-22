all_users =  session.query(User.name).filter_by(fullname='Ed Jones')
for name, in all_users:
   print(name)
