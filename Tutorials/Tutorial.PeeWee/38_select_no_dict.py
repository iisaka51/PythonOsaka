from tweetdb import *

query = Tweet.select(Tweet.content, User.username).join(User)

def func(data):
    for d in data:
        print(f'{d.user.username} -> {d.content}')

# func(query)
# print(query)
