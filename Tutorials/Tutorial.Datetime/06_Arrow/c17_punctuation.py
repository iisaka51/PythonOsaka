import arrow

dt1 = arrow.get("Rainy day: 2022-07-12T06:00:00.",
                "YYYY-MM-DDTHH:mm:ss")
print(dt1)

dt2 = arrow.get("(2022-05-24) is 2nd Aniversary!", "YYYY-MM-DD")
print(dt2)

dt3 = arrow.get("2nd Aniversary is on 2022.05.24.", "YYYY.MM.DD")
print(dt3)

try:
    dt4 = arrow.get("It's 2nd Aniversary (2022-05-24)!", "YYYY-MM-DD")
except:
    print('例外が発生: 日時文字列に続けて複数の Punctuation がある')
