from tweetdb import *

query = (Tweet
         .select(Tweet.content, User.username)
         .join(User, attr='author'))

def func(data):
    for d in data:
        print(f'{d.author.username} -> {d.content}')

# func(query)
# print(query)