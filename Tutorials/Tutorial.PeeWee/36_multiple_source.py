from tweetdb import *

query = Tweet.select()

def func(data):
    for d in data:
        print(f'{d.user.username} -> {d.content}')

# func(query)
