# あくまで例として記述しています。 withを使いましょう。
f = None
try:
    f = open("data.txt")
    try:
        data = f.read()
    except:
            print('Read Error')
finally:
    if f:
        f.close()
