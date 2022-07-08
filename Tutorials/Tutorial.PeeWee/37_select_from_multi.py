from tweetdb import *

query = Tweet.select(Tweet.content, User.username).join(User).dicts()

def func(data):
    for d in data:
        print(d)

# func(query)
# print(query)
