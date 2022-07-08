from tweetdb import *

query = (Tweet
         .select(Tweet.content, fn.COUNT(Favorite.id).alias('count'))
         .join(User)
         .switch(Tweet)
         .join(Favorite, JOIN.LEFT_OUTER)
         .where(User.username == 'huey')
         .group_by(Tweet.content))

def func(data):
    for d in data:
        print(f'{d.content} favorited {d.count} times')

# func(query)
