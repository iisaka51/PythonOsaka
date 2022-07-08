from tweetdb import *

# 最初にサブクエリを定義
# 外側のクエリではTweetモデルから直接クエリを行うため、
# Tweetモデルのエイリアスを使用する
Latest = Tweet.alias()
latest_query = (Latest
                .select(Latest.user,
                        fn.MAX(Latest.timestamp).alias('max_ts'))
                .group_by(Latest.user)
                .alias('latest_query'))

# 結合述語(predicate)は、timestampとuser_idに基づいてツイートをマッチさせる
predicate = ((Tweet.user == latest_query.c.user_id) &
             (Tweet.timestamp == latest_query.c.max_ts))

# tweet からのクエリと predicate 使ったサブクエリの結合を行う
query = (Tweet
         .select(Tweet, User)
         .join(latest_query, on=predicate)
         .join_from(Tweet, User))

def func(data):
    for d in data:
        print(f'{d.user.username} -> {d.content}')

# func(query)
# print(query)
