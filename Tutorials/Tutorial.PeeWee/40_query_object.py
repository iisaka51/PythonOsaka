from tweetdb import *

query = (Tweet
         .select(Tweet.content, User.username)
         .join(User, attr='author'))

def func(data):
    for d in data:
        print(f'{d.username} -> {d.content}')

# func(query.objects())
# print(query.objects())
