Arrowを使って日時処理をしてみよう
=================
## Arrow について
[Arrow](https://arrow.readthedocs.io/en/latest/) は、Pyhton の DateTime オブジェクトの代わりに使用できる日時処理を扱うライブラリです。

このライブラリは、Date/Time APIのデフォルトの実装をオーバーライドするJavaScriptライブラリである [Moment.js](https://github.com/moment/moment) と [requests](https://github.com/psf/requests) にインスパイアされて開発されたことが特徴です。

他にも次のような特徴があります。

 - Python 3.6以上のバージョンをサポート
 - datetime標準ライブラリの完全な実装と効率的な代替品
 - タイムゾーンを認識し（デフォルトでUTCを使用）、タイムゾーンの変換が簡単
 - 日時文字列の自動フォーマットとパース
 - ISO 8601標準の日付と時刻の書式を柔軟にサポート
 - pytz、ZoneInfo、dateutilオブジェクトをサポート
 - マイクロ秒から年までの時間枠に対して、下限(floor)、上限(ceiling)、スパン(span)、範囲(range)を生成することが可能
 - ユーザー独自のArrow由来のデータ型に拡張することができます。
 - PEP 484スタイルの型ヒントをサポート


## インストール
Arrow は pip を使って、次のようにインストールします。

 bash
```
 # Linux or Mac
 $ python -m pip install arrow

 # Windwos
 $ py -3 -m  pip install arrow
```

## Arrow の使用方法

標準ライブラリの datetime を使っているとき、多くの場合は次のように
インポートすることになります。

```
from datetime import datetime, date, time, timezone, tzinfo, timedelta
import calendar
import dateutil
import pytz
```

arrow  を使うと次のようにインポートするだけですみます。

```
import arrow
```


```
In [1]: import arrow

In [2]: x = arrow.now()

In [3]: x
Out[3]: <Arrow [2022-07-11T14:57:35.886643+09:00]>

In [4]: x.datetime
Out[4]: datetime.datetime(2022, 7, 11, 14, 57, 35, 886643, tzinfo=tzlocal())

In [5]: type(x.datetime)
Out[5]: datetime.datetime

In [6]: x.time()
Out[6]: datetime.time(14, 57, 35, 886643)

In [7]: type(x.time())
Out[7]: datetime.time

In [8]: x.year
Out[8]: 2022

In [9]: x.month
Out[9]: 7

In [10]: x.day
Out[10]: 11

```

属性値には次のものがあります。

 - x.year
 - x.month
 - x.day
 - x.hour
 - x.minute
 - x.second
 - x.microsecond


```
In [2]: # %load c01_utc_example.py
   ...: import arrow
   ...:
   ...: utc = arrow.utcnow()
   ...: local = utc.to('local')
   ...:
   ...: print(utc)
   ...: print(local)
   ...:
2022-07-11T03:35:06.033806+00:00
2022-07-11T12:35:06.033806+09:00

In [3]:
```

## ローカル時刻

```
In [2]: # %load c02_local_time.py
   ...: import arrow
   ...:
   ...: local = arrow.now()
   ...: utc = local.to('UTC')
   ...:
   ...: print(local)
   ...: print(utc)
   ...:
2022-07-11T12:38:09.756356+09:00
2022-07-11T03:38:09.756356+00:00

In [3]:
```


```
In [2]: # %load c03_parse_date.py
   ...: import arrow
   ...:
   ...: d1 = arrow.get('2020-05-24 08:10:20', 'YYYY-MM-DD HH:mm:ss')
   ...: print(d1)
   ...:
   ...: d2 = arrow.get(1590307820)
   ...: print(d2)
   ...:
2020-05-24T08:10:20+00:00
2020-05-24T08:10:20+00:00

In [3]:
```


## エポックタイム
**エポックタイム(Epoch Time)** はUnix時刻とも呼ばれ、時刻の値をUTC時刻での1970年1月1日0時0分0秒からの秒単位で返します。

```
In [2]: # %load c04_epoch_time.py
   ...: import arrow
   ...:
   ...: utc = arrow.utcnow()
   ...: print(utc)
   ...:
   ...: epoch_time = utc.timestamp()
   ...: print(epoch_time)
   ...:
   ...: date = arrow.Arrow.fromtimestamp(epoch_time)
   ...: print(date)
   ...:
2022-07-11T04:02:18.570087+00:00
1657512138.570087
2022-07-11T13:02:18.570087+09:00

In [3]:
```

エポックタイムは `.format()`メソッドを使って得ることもできます。
`.format()`メソッドは書式に`X`が与えられるとエポックタイムを返してくれます。


```
In [2]: # %load c05_epoch_time_by_format.py
   ...: import arrow
   ...:
   ...: utc = arrow.utcnow()
   ...:
   ...: epoch_time = utc.format('X')
   ...:
   ...: print(utc)
   ...: print(epoch_time)
   ...:
2022-07-11T04:05:15.357881+00:00
1657512315.357881

In [3]:
```

## format()
`format()`メソッドにフォーマットトークンを与えることで日時文字列をパースしてくれます。


```
In [2]: # %load c06_format.py
   ...: import arrow
   ...:
   ...: now = arrow.now()
   ...:
   ...: year = now.format('YYYY')
   ...: print(f"Year: {year}")
   ...:
   ...: date = now.format('YYYY-MM-DD')
   ...: print(f"Date: {date}")
   ...:
   ...: date_time = now.format('YYYY-MM-DD HH:mm:ss')
   ...: print(f"Date and time: {date_time}")
   ...:
   ...: date_time_zone = now.format('YYYY-MM-DD HH:mm:ss ZZ')
   ...: print(f"Date and time and zone: {date_time_zone}")
   ...:
Year: 2022
Date: 2022-07-11
Date and time: 2022-07-11 13:09:15
Date and time and zone: 2022-07-11 13:09:15 +09:00

In [3]:
```


arrow で使用できるフォーマットトークンには次のものがあります。

| トークン | 意味 | 例 |
|:--|:--|:--|
| YYYY | 年(4桁) | 2020 |
| YY | 年(2桁) | 20, 21 |
| MMMM | 月名 | January, February |
| MMM | 月名(短縮形) | Jan, Feb |
| MM | 月名の数値表記(01-12) | 01, 02 |
| M | 月名の数値表記(1-12) | 1 |
| DDDD | ゼロ埋めした10進数で表記した年中の日にち(001-366) | 001 |
| DDD | 10進数で表記した年中の日にち(1-366) | 1 |
| DD | ゼロ埋めした10進数で表記した月中の日にち(01-31) | 01 |
| D | 10進数で表記した月中の日にち(1-31) | 1 |
| Do | 月中の日にち英語表記(1st,2nd,3rd...30th, 31st) | 1st |
| dddd | 曜日名(Monday, Tuesday...Sunday) | Monday |
| ddd | 曜日名の３文字短縮形(Mon, Tue,...,Sun) | Mon |
| dd | 曜日名の２文字短縮形(Mo, Tu, ..., Su) | Mo |
| d | 曜日名の数値表記(0-6, 0 はSunday) | 1 |
| W | ISO週表記 | 2011-W05-4, 2019-W17 |
| HH | ゼロ埋めした時の２４時間表記 (00-23) | 01 |
| H | 時の24時間表記 (0-23) | 1 |
| hh | ゼロ埋めした時の12時間表記(01-12) | 01 |
| h | 時の12時間表記(1-12) | 1 |
| mm | ゼロ埋めした分(00-59) | 01 |
| m | 分(0-59) | 0 |
| ss | ゼロ埋めした秒(00-59) | 0 |
| s | 秒(1-59) | 0 |
| S | 10分の1秒単位の分数秒 (0,1,..9) | 0 |
| a | AM/PM | AM |
| Z | タイムゾーン(時差の数値表記） | -0900 |
| ZZ | タイムゾーン(時差の時刻表記) | -09:00 |
| ZZZ | タイムゾーン(地域表記） | Asia/Tokyo, Europe/London, GMT |
| X | タイムスタンプの秒表示 | 1234567890.123 |
| x | タイムスタンプのマイクロ秒 | 1234567890123 |

## 組み込みフォーマット

arrow にはよく使用されるフォーマットがあらかじめ定義されています。

```
FORMAT_ATOM = 'YYYY-MM-DD HH:mm:ssZZ'
FORMAT_COOKIE = 'dddd, DD-MMM-YYYY HH:mm:ss ZZZ'
FORMAT_RFC1036 = 'ddd, DD MMM YY HH:mm:ss Z'
FORMAT_RFC1123 = 'ddd, DD MMM YYYY HH:mm:ss Z'
FORMAT_RFC2822 = 'ddd, DD MMM YYYY HH:mm:ss Z'
FORMAT_RFC3339 = 'YYYY-MM-DD HH:mm:ssZZ'
FORMAT_RFC822 = 'ddd, DD MMM YY HH:mm:ss Z'
FORMAT_RFC850 = 'dddd, DD-MMM-YY HH:mm:ss ZZZ'
FORMAT_RSS = 'ddd, DD MMM YYYY HH:mm:ss Z'
FORMAT_W3C = 'YYYY-MM-DD HH:mm:ssZZ'
```

```
In [2]: # %load c07_builtin_formats.py
   ...: import arrow
   ...:
   ...: builtin_formats = {
   ...:     'FORMAT_ATOM': arrow.FORMAT_ATOM,
   ...:     'FORMAT_COOKIE':  arrow.FORMAT_COOKIE,
   ...:     'FORMAT_RFC1036': arrow.FORMAT_RFC1036,
   ...:     'FORMAT_RFC1123': arrow.FORMAT_RFC1123,
   ...:     'FORMAT_RFC2822':  arrow.FORMAT_RFC2822,
   ...:     'FORMAT_RFC3339':  arrow.FORMAT_RFC3339,
   ...:     'FORMAT_RFC822': arrow.FORMAT_RFC822,
   ...:     'FORMAT_RFC850':  arrow.FORMAT_RFC850,
   ...:     'FORMAT_RFC850':  arrow.FORMAT_RFC850,
   ...:     'FORMAT_RSS':  arrow.FORMAT_RSS,
   ...:     'FORMAT_W3C':  arrow.FORMAT_W3C,
   ...: }
   ...:
   ...: dt = arrow.utcnow()
   ...: for name, format in builtin_formats.items():
   ...:     date = dt.format(format)
   ...:     print(f'{name:16}: {date}' )
   ...:
FORMAT_ATOM     : 2022-07-11 23:56:42+00:00
FORMAT_COOKIE   : Monday, 11-Jul-2022 23:56:42 UTC
FORMAT_RFC1036  : Mon, 11 Jul 22 23:56:42 +0000
FORMAT_RFC1123  : Mon, 11 Jul 2022 23:56:42 +0000
FORMAT_RFC2822  : Mon, 11 Jul 2022 23:56:42 +0000
FORMAT_RFC3339  : 2022-07-11 23:56:42+00:00
FORMAT_RFC822   : Mon, 11 Jul 22 23:56:42 +0000
FORMAT_RFC850   : Monday, 11-Jul-22 23:56:42 UTC
FORMAT_RSS      : Mon, 11 Jul 2022 23:56:42 +0000
FORMAT_W3C      : 2022-07-11 23:56:42+00:00

In [3]:
```

## フォーマットトークンのエスケープ
フォーマットトークンは角括弧(`[...]`) でエスケープすることができます。

```
In [2]: # %load c08_escape_format_token.py
   ...: import arrow
   ...:
   ...: fmt = "YYYY-MM-DD h[時] m[分]"
   ...: dt = arrow.get("2018-03-09 8時 40分", fmt)
   ...: dt.format(fmt)
   ...:
   ...: fmt = "YYYY-MM-DD hh:mm [Good Morning.]"
   ...: dt = arrow.get("2018-03-09 08:40 Good Morning.", fmt)
   ...: dt.format(fmt)
   ...:
Out[2]: '2018-03-09 8時 40分'
Out[2]: '2018-03-09 08:40 Good Morning.'

In [3]:
```

## 正規表現
エスケープする文字列には、 正規表現を記述することができます。
次の例は、トークンを区切る空白文字の数に関係なくマッチするように正規表現を使用しています。
これは、ログなどのようにトークン間の空白の数が事前にわからない場合に便利です。

```
In [2]: # %load c09_regular_expressions.py
   ...: import arrow
   ...:
   ...: format = r"ddd[\s+]MMM[\s+]DD[\s+]HH:mm:ss[\s+]YYYY"
   ...: dt1 = arrow.get("Sun May 24 08:20:30 2020", format)
   ...: print(dt1)
   ...:
   ...: dt2 = arrow.get("Sun \tMay 24   08:20:30     2020", format)
   ...: print(dt2)
   ...:
   ...: dt3 = arrow.get("Sun May 24   08:20:30   2020", format)
   ...: print(dt3)
   ...:
2020-05-24T08:20:30+00:00
2020-05-24T08:20:30+00:00
2020-05-24T08:20:30+00:00

In [3]:
```

## 句読点
日付と時刻の書式は、次のリストの中から1つの句読点(Punctuation)で
左右を囲むことができます。

```
, . ; : ? ! " \` ' [ ] { } ( ) < >
```

```
In [2]: # %load c10_punctuation.py
   ...: import arrow
   ...:
   ...: dt1 = arrow.get("Rainy day: 2022-07-12T06:00:00.",
   ...:                 "YYYY-MM-DDTHH:mm:ss")
   ...: print(dt1)
   ...:
   ...: dt2 = arrow.get("(2022-05-24) is 2nd Aniversary!", "YYYY-MM-DD")
   ...: print(dt2)
   ...:
   ...: dt3 = arrow.get("2nd Aniversary is on 2022.05.24.", "YYYY.MM.DD")
   ...: print(dt3)
   ...:
   ...: try:
   ...:     dt4 = arrow.get("It's 2nd Aniversary (2022-05-24)!", "YYYY-MM-DD")
   ...: except:
   ...:     print('例外が発生: 日時文字列に続けて複数の Punctuation がある')
   ...:
2022-07-12T06:00:00+00:00
2022-05-24T00:00:00+00:00
2022-05-24T00:00:00+00:00
例外が発生: 日時文字列に続けて複数の Punctuation がある

In [3]:
```

## 冗長な空白文字
`arrow.get()` に `normalize_whitespace=True` を与えると、冗長な空白文字（スペース、タブ、改行）を自動的に正規化して処理してくれます。


```
In [2]: # %load c11_redundant_whitespace.py
   ...: import arrow
   ...:
   ...: dt1 = arrow.get('\t \n  2022-02-02T22:22:22.222222 \t \n',
   ...:                 normalize_whitespace=True)
   ...: print(dt1)
   ...:
   ...: dt2 = arrow.get('2022-02-02  T \n   22:22:22\t222222',
   ...:                 'YYYY-MM-DD T HH:mm:ss S',
   ...:                 normalize_whitespace=True)
   ...: print(dt2)
   ...:
2022-02-02T22:22:22.222222+00:00
2022-02-02T22:22:22.222222+00:00

In [3]:
```

## タイムゾーン


```
In [2]: # %load c12_timezone.py
   ...: import arrow
   ...:
   ...: utc = arrow.utcnow()
   ...:
   ...: jst = utc.to('Asia/Tokyo')
   ...: tokyo = utc.to('Asia/Tokyo').format('HH:mm:ss')
   ...: newyork = utc.to('America/New_York').format('HH:mm:ss')
   ...: london = (utc.to('Europe/London').format('HH:mm:ss'))
   ...:
   ...: print(jst)
   ...: print(tokyo)
   ...: print(newyork)
   ...: print(london)
   ...:
2022-07-11T13:20:21.337932+09:00
13:20:21
00:20:21
05:20:21

In [3]:
```


## 曜日の取得

```
In [2]: # %load c13_weekday.py
   ...: import arrow
   ...:
   ...: d1 = arrow.get('1962-01-13')
   ...:
   ...: weekday_no = d1.weekday()
   ...: weekday = d1.format('dddd')
   ...:
   ...: print(weekday_no)
   ...: print(weekday)
   ...:
5
Saturday

In [3]: !cal 1 1962
    January 1962
Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6
 7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31


In [4]:
```



## 時刻のシフト


```
In [2]: # %load c14_shift_time.py
   ...: import arrow
   ...:
   ...: now = arrow.now()
   ...: later_5h = now.shift(hours=5).time()
   ...: later_5d = now.shift(days=5).date()
   ...: before_3y = now.shift(years=-3).date()
   ...:
   ...: print(later_5h)
   ...: print(later_5d)
   ...: print(before_3y)
   ...:
18:27:45.891042
2022-07-16
2019-07-11

In [3]:
```

## 夏時間（サマータイム)
日本では運用がないためなじみが薄いですが、サマータイム（DST: Day Light Saving Time）とは、夏の間、時計を進めて夕方の日照時間を長くすることです。春先には1時間進め、秋には標準時まで戻します。


```
In [2]: # %load c15_daylightsaving.py
   ...: import arrow
   ...:
   ...: now = arrow.now()
   ...:
   ...: date_time = now.format("YYYY-MM-DD HH:mm:ss ZZ")
   ...: day_light_saving_Tokyo = now.dst()
   ...: day_light_saving_NY = now.to('America/New_York').dst()
   ...:
   ...: print(date_time)
   ...: print(day_light_saving_Tokyo)
   ...: print(day_light_saving_NY)
   ...:
2022-07-11 13:34:51 +09:00
0:00:00
1:00:00

In [3]:
```

## 日付と時刻のヒューマナイズ
ソーシャルサイトでは、「1時間前」や「5分前」といった用語をよく見かけますが、これは投稿がいつ作成または修正されたかについて、人間に迅速な情報を提供するものです。Arrowには、このような用語を作成するためのヒューマナイズメソッドがあります。
残念ならが日本語には対応できていません。



```
In [2]: # %load c16_humanized_date_time.py
   ...: import arrow
   ...:
   ...: now = arrow.now()
   ...:
   ...: d1 = now.shift(minutes=-15).humanize()
   ...: print(d1)
   ...:
   ...: d2 = now.shift(hours=5).humanize()
   ...: print(d2)
   ...:
   ...:
15 minutes ago
in 5 hours

In [3]:
```

## Arrowによる変換
Arrowでは、文字列から日付と時刻をパースするのは簡単で、`get()`メソッドを使い、有効な日時文字列を与えるだけです。また、Arrowでは、独自のdatetimeクラスの実装と組み込みのdatetimeオブジェクトの間で簡単に変換することができます。

Arrowで文字列をDatetimeに変換する
文字列がすでに ISO 8601 形式 (YYYY-MM-DDTHH:MM:SS.mmmmmm) でフォーマットされている場合は、 `get()`メソッドに直接渡すことができます。

```
In [2]: # %load c17_get.py
   ...: from datetime import datetime
   ...: import arrow
   ...:
   ...: d1 = arrow.get('2020-05-24 08:20:30')
   ...: d2 = arrow.get('2020/05/24 08:20:30')
   ...: d3 = arrow.get(1590308430)
   ...: d4 = arrow.get(datetime(2022, 5, 24, 8, 20, 30))
   ...:
   ...: print(d1)
   ...: print(d2)
   ...: print(d3)
   ...: print(d4)
   ...:
2020-05-24T08:20:30+00:00
2020-05-24T08:20:30+00:00
2020-05-24T08:20:30+00:00
2022-05-24T08:20:30+00:00

In [3]:
```

しかし、実際にはISOの仕様に従った書式の文字列が使われていることは少ないでしょう。

幸いに、正しいArrowフォーマットトークンを使用することで、規則に従わない文字列を解析することができます。これらのトークンはあらかじめ定義されており、文字列を正しくパースするために必要な情報をArrowに与えてくれます。



```
In [2]: # %load c18_get_with_format.py
   ...: import arrow
   ...:
   ...: datetime = arrow.get('May 24 2020 08:20:30',
   ...:                      'MMMM DD YYYY HH:mm:ss')
   ...: print(datetime)
   ...:
2020-05-24T08:20:30+00:00

In [3]:
```

## replace()

Arrow()オブジェクトを`replace()`メソッドで時刻情報を置換することができます。

```
In [2]: # %load c19_replace.py
   ...: import arrow
   ...:
   ...: d1 = arrow.now()
   ...: d2 = d1.replace(year=2020, month=5, day=24)
   ...:
   ...: print(d1)
   ...: print(d2)
   ...:
2022-07-11T15:25:44.135042+09:00
2020-05-24T15:25:44.135042+09:00

In [3]:
```

## range()

与えた開始と終了の日時情報とインターバル間隔でループさせることができます。

```
In [2]: # %load c20_range.py
   ...: import arrow
   ...:
   ...: start = arrow.get(2021, 12, 31, 22, 0)
   ...: end = arrow.get('2022-01-01 02:00')
   ...:
   ...: for r in arrow.Arrow.range('hour', start, end):
   ...:   print(repr(r))
   ...:
<Arrow [2021-12-31T22:00:00+00:00]>
<Arrow [2021-12-31T23:00:00+00:00]>
<Arrow [2022-01-01T00:00:00+00:00]>
<Arrow [2022-01-01T01:00:00+00:00]>
<Arrow [2022-01-01T02:00:00+00:00]>

In [3]:
```

## カスタムクラス

```
In [2]: # %load c21_custom_class.py
   ...: import arrow
   ...:
   ...: class Custom(arrow.Arrow):
   ...:     def till_christmas(self):
   ...:         """
   ...:         ある日付がその年のクリスマスの後に来る場合、
   ...:         次の年のクリスマスとの差を計算
   ...:         """
   ...:         christmas = arrow.Arrow(self.year, 12, 25)
   ...:         if self > christmas:
   ...:               christmas = christmas.shift(years=1)
   ...:
   ...:         return (christmas - self).days
   ...:
   ...: func = arrow.ArrowFactory(Custom)  # create factory function
   ...: x = func.now()
   ...: days = x.till_christmas()
   ...:
   ...: print(f'次のクリスマスまで、あと{days}日')
   ...:
次のクリスマスまで、あと166日

In [3]:
```

## まとめ

Pythonで日付と時刻を扱うためにArrowライブラリを使用するメリットについていくつか説明しました。
Arrowを使用する利点は、次のように公式ドキュメントにまとめられています。

> 感性的で人にやさしいアプローチ。
> 多くの一般的な作成シナリオをサポート。
> より少ないインポートとより少ないコードで日付と時刻を扱うことを支援します。

Arrowは、datetimeライブラリでの問題が、
以下の点で確実に改善されています。

 - 複数のモジュールをインポートすることを低減
 - 1つのデータ型（Arrow）だけで作業することができる
 - タイムゾーンの考慮
 - 最もよく使われる日付と時刻の関数の作成を簡素化すること
 - 様々なタイプ間の簡単な変換
 - 便利なヒューマナイゼーション機能
 - 過去や未来へのシフトが簡単にできる

特に日時文字列をパースする機能は強力でとても応用が効く便利なものであることがわかりました。


## 参考
 - Arrow
   - [Github/Arrow](https://github.com/arrow-py/arrow)
   - [Arrow 公式ドキュメント](https://arrow.readthedocs.io/en/latest/)
 - [Moment.js](https://github.com/moment/moment)
