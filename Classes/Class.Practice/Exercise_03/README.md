# 演習３ 正規表現を使って文字列をパースしてみよう
## 演習３.1
入力された文字列が、次のパターンにマッチするプログラムを作成してみましょう。

 * EX1
  空白文字と英数字だけ（空白文字は)で構成されている文字列の場合に
  `Accept` と表示します
 * EX2
  `a` につづけて`b` がゼロ個以上あるとき `Accept` と表示します
 * EX3
  `a` につづけて`b` が１個以上あるとき `Accept` と表示します
 * EX4
  `a` につづけて３つの`b` がゼロ回以上あるとき `Accept` と表示します
 * EX5
  `a` につづけて２つの`b`か３つの`b` があるとき `Accept` と表示します
 * EX6
  `a` に続けて任意の文字があり、`b` で終わっているとき `Accept` と表示します。
 * EX7
  英小文字`z`を含む[* 単語]が文字列にあるときに `Accept`  と表示します
 * EX8
  `t`が含まれていて、`t`で始まらず、`t`で終わらない単語があるときに、
  `Accept`と表示します。
 * EX9
  `P` で始まる[* 単語]が並んでいるときは `Accept` と表示します。
 * EX10
  時刻が`HH:MM:SS` のフォーマットのときに `Accept` と表示します。
  HHはゼロ埋め２文字の時間、MMはゼロ埋め２文字の分、SSはゼロ埋め２文字の秒

目標時間：EX1〜EX9で15分、EX10は少し難易度が高いので15分

この演習のテストを自動化するためのスニペットです。
`solutions` の第２要素に正規表現パターンを記述します。
第３要素は、`Accept` か `Reject` を指定します。
例えば、`EX0` は、パターンの"対象文字列が英字の大文字以外の文字" にマッチするときに、
`Reject`と表示するというものです。

```
import re

solutions= [
   ['EX0', r'[^A-Z]', 'Reject'],
   ['EX1', r'', 'Accept'],
]

tests = [
  ['test01', 'a'],
  ['test02', 'aa'],
  ['test03', 'aab'],
  ['test04', 'aabb'],
  ['test05', 'abc'],
  ['test06', 'abcabc'],
  ['test07', 'abbabbabb'],
  ['test08', 'abbbabbabbb'],
  ['test09', 'abbbabbabbb'],
  ['test10', 'Python PostgreSQL'],
  ['test11', 'Porker and Zork'],
  ['test12', 'I like zope.'],
  ['test13', 'thank you.'],
  ['test14', r'Big Think!'],
  ['test15', 'I was absent from school.'],
  ['test16', 'The work is near completion.'],
  ['test17', '01:02:03'],
  ['test18', '23:23:23'],
  ['test19', '25:00:00'],
  ['test20', '1:2:3']
]


def exercise(testcase, text, pattern, flag='Accept'):
    result={
        'Accept':['Accept', 'Reject'],
        'Reject':['Reject', 'Accept']
    }
    return result[flag][rv]
    if re.search(pattern,  text):
        return result[flag][0]
    else:
        return result[flag][1]

if __name__ == '__main__':
    import plac
    for id, pattern, flag in solutions:
        print(f'--{id}:"{pattern}" -----')
        for testcase in tests:
            arg = testcase + [pattern, flag]
            x = plac.call(exercise, arg)
            print(f'testcase: {testcase[1:2]}, result: {x}')
```



この演習の目的のひとつにテストの自動化について知ることがあります。

## チャレンジ課題
### 演習の準備

はじめにログジェネレータをインストールしておきます。

```
pip  install   log-generator
```

ログを書き出すディレクトリを work として作成しておきましょう。

そのディレクトリに移動して、
次のファイルコピーして `access_log.conf` として保存します。

```
name: Apache General Access
file: ./access_log
format: "{log_ip} - - [{log_time} +0000] \"{log_method} {log_path} HTTP/1.1\" {log_status} {log_bytes}"
frequency:
  seconds: 5
offset:
  seconds: 0
jitter:
  seconds: 5
amount: 50
fields:
  log_ip:
    type: ip
  log_time:
    type: timestamp
    format: "%d/%b/%Y:%H:%M:%S"
  log_method:
    type: enum
    values: [POST, GET, PUT, PATCH, DELETE]
  log_path:
    type: enum
    values:
      - /auth
      - /alerts
      - /events
      - /playbooks
      - /lists
      - /fieldsets
      - /customers
      - /collectors
      - /parsers
      - /users
  log_status:
    type: enum
    values: [200, 201, 204, 300, 301, 400, 401, 403, 404, 500, 503]
  log_bytes:
    type: integer
    min: 2000
    max: 5000
```

後は、次のコマンドを実行すると、
５０行づつダミーのログ `access_log` を生成してくれます。
適当な行数が出力されたところで `Ctrl+C`(コントロールキーを押しながら`C`キー）を
押下して止めます。

```
 $ log-generator ./access_log.conf
```


## 演習 3.2
ここから正規表現を使って、次のフィールドの値を抜き出してみましょう。

 * IPアドレス
 * リクエストメソッド
 * ステータス

 ヒント
ここで読み出すテキストは access_log.conf で指定したフォーマットでログが記録されます。

```

 format: "{log_ip} - - [{log_time} +0000] \"{log_method} {log_path} HTTP/1.1\" {log_status} {log_bytes}"

```

つまり、第１フィールドはIPアドレスとなることが前提です。
IPアドレスかどうかの有効性を考慮した厳密な正規表現を記述する必要がありません。


