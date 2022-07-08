from tweetdb import *

huey = User.get(User.username == 'huey')

def func(data):
    for d in data:
        print(d.content)

# func(huey.tweets)
# huey.tweets
# huey.tweets.sql()
