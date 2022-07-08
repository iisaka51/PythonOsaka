from tweetdb import *

query = (User
         .select(User.username, fn.COUNT(Favorite.id).alias('count'))
         .join(Tweet, JOIN.LEFT_OUTER)
         .join(Favorite, JOIN.LEFT_OUTER)
         .group_by(User.username))

def func(data):
    for d in data:
        print(f'{d.username} {d.count}')

# func(query)
