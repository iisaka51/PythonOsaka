from tweetdb import *

Owner = User.alias()
query = (Favorite
         .select(Favorite, Tweet.content, User.username, Owner.username)
         .join(Owner)   # Join favorite -> user (owner of favorite).
         .switch(Favorite)
         .join(Tweet)   # Join favorite -> tweet
         .join(User))   # Join tweet -> user

def func(data):
    for d in data:
        print(f'{d.user.username} liked ', end='')
        print(f'{d.tweet.content} by {d.tweet.user.username}')

# func(query)
# print(query)
