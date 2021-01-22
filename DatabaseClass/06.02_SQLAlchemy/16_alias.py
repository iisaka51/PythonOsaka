from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')

all_users = session.query(user_alias, user_alias.name).all()
for row in all_users:
   print(row.user_alias)
