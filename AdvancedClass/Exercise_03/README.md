# 演習３ ジェネレータとデコレータを使いこなそう

## 演習3.1

次のコード(exercise31.py) はユーザから入力された数値を超えない範囲で、
０から偶数を表示するものです。


```

def evenNumbers(maxval):
    nums = list()
    for n in range(maxval):
        if n%2 == 0:
            yield n


maxval = int(input('Please input number: '))
for n in evenNumbers(maxval+1):
    print(n)

```

この関数 `evenNumbers()` を`yield`文を使って、
ジェネレータとなるように修正してみましょう。（目標時間：３分)


## 演習3.2
演習:3.1 のコードを`yield`文を使わずに、ジェネレータとなるようにしてみましょう。
（目標時間：３分)

## 演習3.3
次のコード(exercise33.py)は引数として与えられた関数を辞書型オブジェクト`ACTIONS`に保存するものです。


```

ACTIONS = dict()

def register(func):
    ACTIONS[func.__name__] = func
    return func
```

これを利用して次の機能をもつ関数 `greeting()` を作成しましょう。（目標時間：１０分)

 *　`greeting()`は引数`name` で与えられた文字列からメッセージを作成する
 * 英語（`Hello XXX`）もしくはフランス語（ `Bonjour XXX` ）のメッセージを表示する
 * 引数`name`の文字数が偶数なら英語、奇数ならフランス語でメッセージを表示する
 * 英語のメッセージを表示する関数は `greeting_english()` として`ACTIONS`に登録する
 * フランス語のメッセージを表示する関数は`greeting_french()` として`ACTIONS`に登録する


## チャレンジ課題

## 演習3.4

　greeting()の引数`name` はコマンドライン引数で与えることができるようにしてみよう

## 演習3.5

　オプション`--namefile` で与えたファイルから名前を読み出して、
   `greeting()`に渡すようにしてみましょう。
   このときファイルには複数行があっても受け付けるようしましょう

