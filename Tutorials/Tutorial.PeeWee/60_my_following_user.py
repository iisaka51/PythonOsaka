from tweepeedb import *

charlie = User.get(User.username == 'charlie')
query = (User
         .select()
         .join(Relationship, on=Relationship.to_user)
         .where(Relationship.from_user == charlie))

