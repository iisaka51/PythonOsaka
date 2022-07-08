from tweetdb import *

query = (Tweet
         .select()
         .join(User, on=(Tweet.user == User.id))
         .where(User.username == 'huey'))

def func(data):
    for d in data:
        print(d.content)

# func(query)
