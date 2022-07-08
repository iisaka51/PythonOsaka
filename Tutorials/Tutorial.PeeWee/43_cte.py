from tweetdb import *

# まずCTEを定義する
# メインのクエリではTweetモデルから直接クエリを行うため、
# Tweetモデルのエイリアスを使用する
Latest = Tweet.alias()
cte = (Latest
       .select(Latest.user, fn.MAX(Latest.timestamp).alias('max_ts'))
       .group_by(Latest.user)
       .cte('latest'))

# 結合述語(predicate)は、timestampとuser_idに基づいてツイートをマッチさる
predicate = ((Tweet.user == cte.c.user_id) &
             (Tweet.timestamp == cte.c.max_ts))

# tweetからのクエリと、predicateを使ったCTEでの結合を行う
query = (Tweet
         .select(Tweet, User)
         .join(cte, on=predicate)
         .join_from(Tweet, User)
         .with_cte(cte))

def func(data):
    for d in data:
        print(f'{d.user.username} -> {d.content}')

# func(query)
# print(query)
