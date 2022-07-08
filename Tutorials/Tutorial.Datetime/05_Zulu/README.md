zuluを使って日時処理をしてみよう
=================
## zulu について
Zuluは、Pyhton の DateTime オブジェクトの代わりに使用できる日時処理を扱うライブラリです。

次のような特徴があります。

- Python ネイティブの datetime オブジェクトを簡単に置き換えることができます。
- すべての datetime オブジェクトを UTC に変換して保存します。
- デフォルトでは、ISO8601 フォーマットの文字列および POSIX タイムスタンプを解析します。
- 文字列出力のフォーマット時やネイティブの datetime オブジェクトへのキャスト時にのみタイムゾーンが適用されます。
- Python 3.6以降で動作します

> 資料の表記について
> この資料にあるサンプルコードにコメントで記述した出力例は、読みやすいように内容を変えない範囲で編集しています。


## インストール
zulu は pip を使って、次のようにインストールします。

 bash
```
 # Linux or Mac
 $ python -m pip install zulu

 # Windwos
 $ py -3 -m  pip install zulu
```


## Zulu の使用方法
Zuluの主な型はzulu.Zuluで、ネイティブのdatetimeオブジェクトの代替となるものですが（datetime.datetimeを継承しています）、内部的にはUTCタイムゾーンのみを扱います。


```
 In [2]: # %load 01_now.py
    ...: import zulu
    ...:
    ...: dt = zulu.now()
    ...: print("Today date and time is:", dt)
    ...:
 Today date and time is: 2021-09-26T00:18:04.173085+00:00

```

時刻情報の tzinfo の値が  `+00:00` となっているため、內部的にUTCで表現されていることがわかります。

zulu は datetime オブジェクトを代替するものとして機能します。

```
 In [2]: # %load 02_intro.py
    ...: from datetime import datetime
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...: # <Zulu [2020-05-24T08:20:00.137493+00:00]>
    ...:
    ...: v1 = isinstance(dt, zulu.Zulu)
    ...: assert v1 == True
    ...:
    ...: v2 = isinstance(dt, datetime)
    ...: assert v2 == True
    ...:
```

datetime の属性値も保持しています。

```
 In [2]: # %load 03_attributes.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: assert dt.year == 2020
    ...: assert dt.month == 5
    ...: assert dt.day == 24
    ...: assert dt.hour == 8
    ...: assert dt.minute == 20
    ...: assert dt.second == 00
    ...: assert dt.microsecond == 137493
    ...: assert dt.tzname() == '+00:00'
    ...:
    ...: # assert は与えた式が真のときは何も出力しない
    ...:

```

## 基本的なデータアクセス
datetimeのすべての属性とメソッドに加え、いくつかの新しい属性とメソッドが利用できます。
まず、datetime のメソッドをみてみましょう。

 04_methods.py
```
 import zulu

 dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

 dt.utcoffset()
 # datetime.timedelta(0)

 dt.dst()
 # datetime.timedelta(0)

 dt.isoformat()
 # '2020-05-24T08:20:00.137493+00:00'

 dt.weekday()
 # 6

 dt.isoweekday()
 # 7

 dt.isocalendar()
 # datetime.IsoCalendarDate(year=2020, week=21, weekday=7)

 dt.ctime()
 # 'Sun May 24 08:20:00 2020'

 dt.toordinal()
 # 737569

 dt.timetuple()
 # time.struct_time(tm_year=2020, tm_mon=5, tm_mday=24,
 #                  tm_hour=8, tm_min=20, tm_sec=0,
 #                  tm_wday=6, tm_yday=145, tm_isdst=-1)

 dt.utctimetuple()
 # time.struct_time(tm_year=2020, tm_mon=5, tm_mday=24,
 #                  tm_hour=8, tm_min=20, tm_sec=0,
 #                  tm_wday=6, tm_yday=145, tm_isdst=0)

 dt.timestamp()
 # 1590308400.137493

 dt.date()
 # datetime.date(2020, 5, 24)

 dt.time()
 # datetime.time(8, 20, 0, 137493)

 dt.timetz()
 # datetime.time(8, 20, 0, 137493,
 #               tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))
```


新しいメソッドには次のものがあります。

```
 In [2]: # %load 05_new_methods.py
    ...: import zulu
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: dt.naive
    ...: # datetime.datetime(2020, 5, 24, 8, 20, 0, 137493)
    ...:
    ...: dt.datetime
    ...: # datetime.datetime(2020, 5, 24, 8, 20, 0, 137493,
    ...: #          tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))
    ...:
    ...: dt.is_leap_year()
    ...: # True
    ...:
    ...: dt.days_in_month()
    ...: # 31
    ...:
    ...: dt.datetuple()
    ...: # Date(year=2020, month=5, day=24)
    ...:
    ...: dt.datetimetuple()
    ...: # DateTime(year=2020, month=5, day=24,
    ...: #          hour=8, second=20, minute=0, microsecond=137493,
    ...: #          tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))
    ...:
 Out[2]: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493)
 Out[2]: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493, tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))
 Out[2]: True
 Out[2]: 31
 Out[2]: Date(year=2020, month=5, day=24)
 Out[2]: DateTime(year=2020, month=5, day=24, hour=8, second=20, minute=0, microsecond=137493, tzinfo=datetime.timezone(datetime.timedelta(0), '+00:00'))

```

## 構文解析と書式設定
デフォルトでは、 `zulu.parse()` は、ISO8601形式の文字列またはPOSIXタイムスタンプのいずれかを探しますが、文字列の中に明確なタイムゾーンが見つからない場合は、UTCタイムゾーンを仮定します。

```
 In [2]: # %load 06_parsing_and_formating.py
    ...: import zulu
    ...:
    ...:  zulu.parse('2020-05-24T08:20:00+0900')
    ...: # <Zulu [2020-05-23T23:20:00+00:00]>
    ...:
    ...: zulu.parse('2020-05-24T08:20:00+0900', zulu.ISO8601)
    ...: # <Zulu [2020-05-23T23:20:00+00:00]>
    ...:
    ...: zulu.parse('2020-05-24')
    ...: # <Zulu [2020-05-24T00:00:00+00:00]>
    ...:
    ...: zulu.parse('2020-05-24 08:20')
    ...: # <Zulu [2020-05-24T08:20:00+00:00]>
    ...:
    ...: zulu.parse(1590308400.0)
    ...: # <Zulu [2020-05-24T08:20:00+00:00]>
    ...:
    ...: zulu.parse(1590308400.0, zulu.TIMESTAMP)
    ...: # <Zulu [2020-05-24T08:20:00+00:00]>
    ...:
    ...:
 Out[2]: <Zulu [2020-05-24T08:20:00.137493+00:00]>
 Out[2]: <Zulu [2020-05-23T23:20:00+00:00]>
 Out[2]: <Zulu [2020-05-23T23:20:00+00:00]>
 Out[2]: <Zulu [2020-05-24T00:00:00+00:00]>
 Out[2]: <Zulu [2020-05-24T08:20:00+00:00]>
 Out[2]: <Zulu [2020-05-24T08:20:00+00:00]>
 Out[2]: <Zulu [2020-05-24T08:20:00+00:00]>

```

 `zulu.parse()` には複数のフォーマットを与えることができます。それらはすべて評価されます。

```
 In [2]: # %load 07_multiple_fomatting.py
    ...: import zulu
    ...:
    ...: zulu.parse('3/2/1992', ['ISO8601', 'MM/dd/YYYY'])
    ...: # <Zulu [1992-03-02T00:00:00+00:00]>
    ...:
    ...: try:
    ...:     zulu.parse('3/2/1992', 'ISO8601')
    ...: except zulu.ParseError as e:
    ...:     print(e)
    ...:
    ...: # Value "3/2/1992" does not match any format in
    ...: # ["ISO8601" (Unable to parse date string '3/2/1992')]
    ...:
    ...:
 Out[2]: <Zulu [1992-03-02T00:00:00+00:00]>
 Value "3/2/1992" does not match any format in ["ISO8601" (Unable to parse date string '3/2/1992')]

```

 `zulu.parse()` は、特別なフォーマットキーワードに対応しています。

default_tzを設定することで、他のタイムゾーンを素朴なデータタイムに置き換えることができます。

```
 In [2]: # %load 08_timezone.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: zulu.parse('2020-05-24', default_tz='US/Eastern')
    ...: # <Zulu [2020-05-24T04:00:00+00:00]>
    ...:
    ...: zulu.parse('2020-05-24', default_tz='Asia/Tokyo')
    ...: # <Zulu [2020-05-23T15:00:00+00:00]>
    ...:
    ...: zulu.parse('2020-05-24', default_tz='local')
    ...: # <Zulu [2020-05-23T15:00:00+00:00]>
    ...:
 Out[2]: <Zulu [2020-05-24T04:00:00+00:00]>
 Out[2]: <Zulu [2020-05-23T15:00:00+00:00]>
 Out[2]: <Zulu [2020-05-23T15:00:00+00:00]>

```


入力にデフォルトのタイムゾーンが設定されている場合は無視されます。

```
 In [2]: # %load 09_input_timezone.py
    ...: import zulu
    ...:
    ...: zulu.parse('2020-05-24T08:20:00+0900')
    ...: # <Zulu [2020-05-23T23:20:00+00:00]>
    ...:
    ...:
    ...: zulu.parse('2020-05-24T08:20:00+0900', default_tz='Asia/Tokyo')
    ...: # <Zulu [2020-05-23T23:20:00+00:00]>
    ...:
 Out[2]: <Zulu [2020-05-23T23:20:00+00:00]>
 Out[2]: <Zulu [2020-05-23T23:20:00+00:00]>

```

Zuluの文字列解析/フォーマットは、strftime/strptime指示子とUnicodeの日付パターンの両方をサポートしています。

```
 In [2]: # %load 10_formatting_directive.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00+0900')
    ...:
    ...: dt.format('%Y-%m-%d %H:%M:%S%z')
    ...: # '2020-05-23 23:20:00+0000'
    ...:
    ...: dt.format('YYYY-MM-dd HH:mm:ssZ')
    ...: # '2020-05-23 23:20:00+0000'
    ...:
    ...: dt.format('%Y-%m-%d %H:%M:%S%z', tz='US/Eastern')
    ...: # '2020-05-23 19:20:00-0400'
    ...:
    ...: dt.format('%Y-%m-%d %H:%M:%S%z', tz='local')
    ...: # '2020-05-24 08:20:00+0900'
    ...:
    ...: zulu.parse('2020-05-24 08:20:00+0900', '%Y-%m-%d %H:%M:%S%z')
    ...: # <Zulu [2020-05-23T23:20:00+00:00]>
    ...:
    ...:
 Out[2]: '2020-05-23 23:20:00+0000'
 Out[2]: '2020-05-23 23:20:00+0000'
 Out[2]: '2020-05-23 19:20:00-0400'
 Out[2]: '2020-05-24 08:20:00+0900'
 Out[2]: <Zulu [2020-05-23T23:20:00+00:00]>

```

 `zulu.parser.format_datetime()` をネイティブのデータタイムで使うこともできます。


```
 In [2]: # %load 11_format_datetime.py
    ...: from datetime import datetime
    ...: from zulu import Zulu
    ...: from zulu.parser import UTC, format_datetime
    ...:
    ...: native = datetime(2020, 5, 24, 8, 20, 00, 137493, tzinfo=UTC)
    ...:
    ...: format_datetime(native, '%Y-%m-%d %H:%M:%S%z')
    ...: # '2020-05-24 08:20:00+0000'
    ...:
    ...: format_datetime(native, 'YYYY-MM-dd HH:mm:ssZ')
    ...: # '2020-05-24 08:20:00+0000'
    ...:
    ...: dt = Zulu.fromdatetime(native)
    ...: format_datetime(dt, 'YYYY-MM-dd HH:mm:ssZ')
    ...: # '2020-05-24 08:20:00+0000'
    ...:
 Out[2]: '2020-05-24 08:20:00+0000'
 Out[2]: '2020-05-24 08:20:00+0000'
 Out[2]: '2020-05-24 08:20:00+0000'
```

## キーワード パースフォーマット
以下のキーワードは、フォーマット指令またはパターンの代わりに、zulu.parseに与えることができます。

```
 In [2]: # %load 12_keyword_format.py
    ...: import zulu
    ...:
    ...: zulu.parse(1590308400, 'timestamp')
    ...: # <Zulu [2020-05-24T08:20:00+00:00]>
    ...:
 Out[2]: <Zulu [2020-05-24T08:20:00+00:00]>
```

 キーワードパースフォーマット

| Keyword | Description | Sample Input |
|:--|:--|:--|
| ISO8601 | Parse ISO8601 string | 2020-05-24 08:24:00-0400 |
|  |  | 2020-05-24 08:24:00 |
|  |  | 2020-05-24 |
|  |  | 2020-05 |
| timestamp | Parse POSIX timestamp | 1590308400 |
|  |  | 1590308400.137493 |


## フォーマットトークン
Zuluは、2つの異なるスタイルの文字列解析/フォーマットトークンをサポートします。

- すべてのPython strptime/strftime指示子
- Unicode 日付パターンのサブセット

どちらのスタイルも解析時に使用できます。

```
 In [2]: # %load 13_format_token.py
    ...: import zulu
    ...:
    ...: dt1 = zulu.parse('05/24/20 08:20:00 +0900', '%m/%d/%y %H:%M:%S %z')
    ...: dt2 = zulu.parse('05/24/20 08:20:00 +0900', 'MM/dd/YY HH:mm:ss Z')
    ...:
    ...: v1 = dt1.format('%m/%d/%y %H:%M:%S %z')
    ...: v2 = dt1.format('MM/dd/YY HH:mm:ss Z')
    ...:
    ...:
    ...: # dt1           # OUT: <Zulu [2020-05-23T23:20:00+00:00]>
    ...: # dt2           # OUT: <Zulu [2020-05-23T23:20:00+00:00]>
    ...:
    ...: # v1            # OUT: '05/23/20 23:20:00 +0000'
    ...: # v2            # OUT: '05/23/20 23:20:00 +0000'
    ...:

 In [3]: dt1
 Out[3]: <Zulu [2020-05-23T23:20:00+00:00]>

 In [4]: dt2
 Out[4]: <Zulu [2020-05-23T23:20:00+00:00]>

 In [5]: v1
 Out[5]: '05/23/20 23:20:00 +0000'

 In [6]: v2
 Out[6]: '05/23/20 23:20:00 +0000'
```


## フォーマットディレクティブ
Python の標準ライブラリ datetime での  [strftime() と strptime() の振る舞い](https://docs.python.org/ja/3.9/library/datetime.html#strftime-and-strptime-behavior])のすべてのディレクティブがサポートされています。

[日付パターン](http://www.unicode.org/reports/tr35/tr35-19.html#Date_Field_Symbol_Table])  からのパターンのサブセットが解析用にサポートされており、  `_all_ ` パターンがフォーマット用にサポートされています。

 フォーマットディレクティブ

| 属性 | スタイル | 表記パターン | 例 |
|:--|:--|:--|:--|
| Year | 西暦(4桁) | YYYY | 2000, 2001, 2002 … 2015, 2016 |
| Year | 西暦(2桁) | YY | 00, 01, 02 … 15, 16 |
| Month | 月名（フルネーム) | MMMM | January, February, March |
| Month | 月名（省略形) | MMM | Jan, Feb, Mar … Nov, Dec |
| Month | ゼロ埋めした10進数で表記した月番号 | MM | 01, 02, 03 … 11, 12 |
| Month | 10進数で表記した月番号 | M | 1, 2, 3 … 11, 12 |
| Day of Month | ゼロ埋めした10進数で表記した月中の日にち | dd | 01, 02, 03 … 30, 31 |
| Day of Month | 10進数で表記した月中の日にち | d | 1, 2, 3 … 30, 31 |
| Day of Year | ゼロ埋めした10進数で表記した年中の日にち | DDD | 001, 002, 003 … 054, 055 … 364, 365 |
| Day of Year | ゼロ埋めした10進数で表記した年中の日にち | DD | 01, 02, 03 … 54, 55 … 364, 365 |
| Day of Year | 10進数で表記した年中の日にち | D | 1, 2, 3 … 54, 55 … 364, 365 |
| Weekday | 曜日名(フルネーム) | EEEE | Sunday, Monday, Tuesday … Friday, Saturday |
| Weekday | 曜日名(省略形) | EEE | Sun, Mon, Tue … Fri, Sat |
| Weekday | 曜日名(省略形) | EE | Sun, Mon, Tue … Fri, Sat |
| Weekday | 曜日名(省略形) | E | Sun, Mon, Tue … Fri, Sat |
| Weekday | 曜日名(省略形) | eee | Sun, Mon, Tue … Fri, Sat |
| Weekday | ゼロ埋めした曜日番号 | ee | 01, 02, 03 … 06, 07 |
| Weekday | 曜日番号 | e | 1, 2, 3 … 6, 7 |
| Hour | ゼロ埋めした時の24時間表記 | HH | 00, 01, 02 … 22, 23 |
| Hour | 時の24時間表記 | H | 0, 1, 2 … 22, 23 |
| Hour | ゼロ埋めした時の12時間表記 | hh | 00, 01, 02 … 11, 12 |
| Hour | 時の12時間表記 | h | 0, 1, 2, … 11, 12 |
| AM / PM | 大文字のAM/PM | a | AM, PM |
| Minute | ゼロ埋した分 | mm | 00, 01, 02 … 58, 59 |
| Minute | 分 | m | 0, 1, 2 … 58, 59 |
| Second | ゼロ埋めした秒 | ss | 00, 01, 02 … 58, 59 |
| Second | 秒 | s | 0, 1, 2 … 58, 59 |
| Microsecond | ゼロ埋めしたマイクロ秒 | SSSSSS | 000000, 000001 … 999998, 999999 |
| Microsecond | マイクロ秒 | SSSSS | 00000, 00001 … 99998, 99999 |
| Microsecond | ゼロ埋めしたマイクロ秒（5桁) | SSSS | 0000, 0001 … 9998, 9999 |
| Microsecond | ゼロ埋めしたマイクロ秒（3桁) | SSS | 000, 001 … 998, 999 |
| Microsecond | ゼロ埋めしたマイクロ秒（2桁) | SS | 00, 01 … 98, 99 |
| Microsecond | ゼロ埋めしたマイクロ秒（1桁) | S | 0, 1 … 8, 9 |
| Timezone | UTCオフセット(セパレーターなし） | Z | -1100, -1000 … +0000 … +1100, +1200 |

## 人に優しい表記
 `time_from()` と `time_to()` メソッドを使って、2つのZuluオブジェクトを人に優しい表記にすることができます。

```
 In [2]: # %load 14_human_readble.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: dt
    ...: # <Zulu [2020-05-24T08:20:00.137493+00:00]>
    ...:
    ...: dt.time_from(dt.end_of_day())
    ...: # '16 hours ago'
    ...:
    ...: dt.time_to(dt.end_of_day())
    ...: # 'in 16 hours'
    ...:
    ...: dt.time_from(dt.start_of_day())
    ...: # 'in 8 hours'
    ...:
    ...: dt.time_to(dt.start_of_day())
    ...: # '8 hours ago'
    ...:
    ...: zulu.now()
    ...: # <Zulu [2021-09-25T07:12:26.937079+00:00]>
    ...:
    ...: dt.time_from_now()
    ...: # '1 year ago'
    ...:
    ...: dt.time_to_now()
    ...: # 'in 1 year'
    ...:
 Out[2]: <Zulu [2020-05-24T08:20:00.137493+00:00]>
 Out[2]: '16 hours ago'
 Out[2]: 'in 16 hours'
 Out[2]: 'in 8 hours'
 Out[2]: '8 hours ago'
 Out[2]: <Zulu [2021-09-25T07:14:54.310773+00:00]>
 Out[2]: '1 year ago'
 Out[2]: 'in 1 year'

```

## タイムゾーンの取り扱い

UTC 以外のタイムゾーンは、Zulu インスタンス内では表現できません。他のタイムゾーンは、Zuluオブジェクトをネイティブのデータタイムに変換する時( `Zulu.astimezone()` 経由)、または、文字列のフォーマットを行う時(`Zulu.format()`経由)にのみ適用されます。Zuluは、tzinfoオブジェクトとIANAタイムゾーンデータベース文字列名(Olsonデータベースとしても知られています)の両方を理解します。

```
 In [2]: # %load 15_tzinfo.py
    ...: from datetime import datetime
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+09:00')
    ...: local = dt.astimezone()
    ...: # same as doing dt.astimezone('local')
    ...: # datetime.datetime(2016, 7, 25, 15, 33, 18, 137493,
    ...: #                   tzinfo=tzlocal())
    ...:
    ...: jst1 = dt.astimezone('Asia/Tokyo')
    ...:
    ...: import pytz
    ...: jst2 = dt.astimezone(pytz.timezone('Asia/Tokyo'))
    ...:
    ...: # jst1
    ...: # OUT: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493,
    ...: #                        tzinfo=tzfile('/usr/share/zoneinfo/Asia/Tokyo')
    ...: )
    ...:
    ...: # jst2
    ...: # OUT: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493,
    ...: #                        tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>
    ...: )
    ...:

 In [3]: jst1
 Out[3]: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493, tzinfo=tzfile('/usr/share/zoneinfo/Asia/Tokyo'))

 In [4]: jst2
 Out[4]: datetime.datetime(2020, 5, 24, 8, 20, 0, 137493, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)

```


## シフト、置き換え、コピー
Zuluでは、シフト法を使ってtimedeltaオブジェクトを簡単に適用することができます。

```
 In [2]: # %load 16_shift.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: shifted = dt.shift(hours=-5, minutes=10)
    ...: # <Zulu [2020-05-24T03:30:00.137493+00:00]>
    ...:
    ...: assert shifted is not dt
    ...: # assert は与えた式が真のときは何も表示しない
    ...:

```

そして、 `add()` 、`subtract()`メソッドでを使った例です。

```
 In [2]: # %load 17_add_subtract.py
    ...: from datetime import timedelta
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: shifted = dt.subtract(hours=5).add(minutes=10)
    ...: # <Zulu [2020-05-24T03:30:00.137493+00:00]>
    ...:
    ...: shifted = dt.subtract(timedelta(hours=5))
    ...: # <Zulu [2020-05-24T03:30:00.137493+00:00]>
    ...:
    ...: # First argument to subtract() can also be another datetime object
    ...: delta = dt.subtract(shifted)
    ...: # <Delta [5:00:00]>
    ...:
    ...: shifted = dt.add(timedelta(minutes=10))
    ...: # <Zulu [2020-05-24T03:30:00.137493+00:00]>
    ...:

```

 `replace()` で datetime オブジェクトの属性値を変更できます。

```
 In [2]: # %load 18_replace.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: replaced = dt.replace(hour=14, minute=43)
    ...: # <Zulu [2020-05-24T14:43:18.137493+00:00]>
    ...:

```

また、 `copy()` でコピーをとることもできます。

```
 In [2]: # %load 19_copy.py
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: copied = dt.copy()
    ...: # <Zulu [2020-05-24T08:20:00.137493+00:00]>
    ...:
    ...: assert copied is not dt
    ...: assert copied == dt
    ...:

```


## span、range、star、end
 `span()` で時間軸をまたいだ期間を取得できます。

```
 In [2]: # %load 20_span.py
    ...: from zulu import Zulu
    ...:
    ...: dt = Zulu(2020, 5, 20, 8, 20, 00, 137493)
    ...:
    ...: t1 = dt.span('century')
    ...: # (<Zulu [2000-01-01T00:00:00+00:00]>,
    ...: #  <Zulu [2099-12-31T23:59:59.999999+00:00]>)
    ...:
    ...: t2 = dt.span('decade')
    ...: # (<Zulu [2020-01-01T00:00:00+00:00]>,
    ...: #  <Zulu [2029-12-31T23:59:59.999999+00:00]>)
    ...:
    ...: t3 = dt.span('year')
    ...: # (<Zulu [2020-01-01T00:00:00+00:00]>,
    ...: #  <Zulu [2020-12-31T23:59:59.999999+00:00]>)
    ...:
    ...: t4 = dt.span('month')
    ...: # (<Zulu [2020-05-01T00:00:00+00:00]>,
    ...: #  <Zulu [2020-05-31T23:59:59.999999+00:00]>)
    ...:
    ...: t5 = dt.span('week')
    ...: # (<Zulu [2020-05-18T00:00:00+00:00]>,
    ...: #  <Zulu [2020-05-24T23:59:59.999999+00:00]>)
    ...:
    ...: t6 = dt.span('day')
    ...: # (<Zulu [2020-05-20T00:00:00+00:00]>,
    ...: #  <Zulu [2020-05-20T23:59:59.999999+00:00]>)
    ...:
    ...: t7 = dt.span('hour')
    ...: # (<Zulu [2020-05-20T08:00:00+00:00]>,
    ...: #  <Zulu [2020-05-20T08:59:59.999999+00:00]>)
    ...:
    ...: t8 = dt.span('minute')
    ...: # (<Zulu [2020-05-20T08:20:00+00:00]>,
    ...: #  <Zulu [2020-05-20T08:20:59.999999+00:00]>)
    ...:
    ...: t9 = dt.span('second')
    ...: # (<Zulu [2020-05-20T08:20:00+00:00]>,
    ...: #  <Zulu [2020-05-20T08:20:00.999999+00:00]>)
    ...:
    ...: t10 = dt.span('century', count=3)
    ...: # (<Zulu [2000-01-01T00:00:00+00:00]>,
    ...: #  <Zulu [2299-12-31T23:59:59.999999+00:00]>)
    ...:
    ...: t11 = dt.span('decade', count=3)
    ...: # (<Zulu [2020-01-01T00:00:00+00:00]>,
    ...: #  <Zulu [2049-12-31T23:59:59.999999+00:00]>)
    ...:

```

時間枠の開始は  `start()` で、終了は`end()`で取得することができます。

```
 In [2]: # %load 21_start_end.py
    ...: from datetime import datetime
    ...: import zulu
    ...:
    ...: dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')
    ...:
    ...: t1 = dt.start_of('day')  # OR dt.start_of_day()
    ...: # <Zulu [2020-05-24T00:00:00+00:00]>
    ...:
    ...: t2 = dt.end_of('day')  # OR dt.end_of_day()
    ...: # <Zulu [2020-05-24T23:59:59.999999+00:00]>
    ...:
    ...: t3 = dt.end_of('year', count=3)  # OR dt.end_of_year()
    ...: # <Zulu [2022-12-31T23:59:59.999999+00:00]>
    ...:

```

サポートされている時間軸(time frame)は、 `century` 、`decade`、`year`、`month`、`week`、`day`、`hour`、`minute`、`second`です。これらは、 `start_of(frame)`、`end_of(frame)` 、`start_of_<frame>()`、`end_of_<frame>.()`で使用することができます。

期間(time span)の範囲を `span_range()` で取得できます。

```
 In [2]: # %load 22_span_range.py
    ...: import zulu
    ...:
    ...: start = zulu.Zulu(2020, 5, 20, 8, 20)
    ...: end = zulu.Zulu(2020, 10, 2, 11, 00)
    ...:
    ...: for span in zulu.span_range('month', start, end):
    ...:     print(span)
    ...:
 (<Zulu [2020-05-01T00:00:00+00:00]>, <Zulu [2020-05-31T23:59:59.999999+00:00]>)
 (<Zulu [2020-06-01T00:00:00+00:00]>, <Zulu [2020-06-30T23:59:59.999999+00:00]>)
 (<Zulu [2020-07-01T00:00:00+00:00]>, <Zulu [2020-07-31T23:59:59.999999+00:00]>)
 (<Zulu [2020-08-01T00:00:00+00:00]>, <Zulu [2020-08-31T23:59:59.999999+00:00]>)
 (<Zulu [2020-09-01T00:00:00+00:00]>, <Zulu [2020-09-30T23:59:59.999999+00:00]>)
```

datetime の  `range()` を使用すると、データタイムの範囲を反復処理することができます。

```
 In [2]: # %load 23_range.py
    ...: import zulu
    ...:
    ...: start = zulu.Zulu(2020, 5, 20, 8, 20)
    ...: end = zulu.Zulu(2020, 10, 2, 11, 00)
    ...:
    ...: for dt in zulu.range('month', start, end):
    ...:     print(dt)
    ...:
 2020-05-20T08:20:00+00:00
 2020-06-20T08:20:00+00:00
 2020-07-20T08:20:00+00:00
 2020-08-20T08:20:00+00:00

```

 `range()` と `span_range()` でサポートされている時間軸(time frame)は、
 `century` 、 `decade`、 `year`、 `month`、 `week`、 `day`、 `hour`、 `minute`、 `second` です。

## タイムデルタ(timedelta)
zuluは、datetime オブジェクトの代替としての機能だけでなく、timedelta オブジェクトも代替する機能が提供されています。

```
 In [2]: # %load 24_timedelta.py
    ...: import zulu
    ...:
    ...: delta = zulu.parse_delta('1w 3d 2h 32m')
    ...: # <Delta [10 days, 2:32:00]>
    ...:
    ...: assert isinstance(delta, zulu.Delta)
    ...:
    ...: from datetime import timedelta
    ...: assert isinstance(delta, timedelta)
    ...:
    ...: t1 = zulu.parse_delta('2:04:13:02.266')
    ...: # <Delta [2 days, 4:13:02.266000]>
    ...:
    ...: t2 = zulu.parse_delta('2 days, 5 hours, 34 minutes, 56 seconds')
    ...: # <Delta [2 days, 5:34:56]>
    ...:

```

zulu.parse_deltaが解析できる他のフォーマットは以下の通りです。

-  `32m`
-  `2h32m`
-  `3d2h32m`
-  `1w3d2h32m`
-  `1w 3d 2h 32m`
-  `1 w 3 d 2 h 32 m`
-  `4:13`
-  `4:13:02`
-  `4:13:02.266`
-  `2:04:13:02.266`
-  `2 days,  4:13:02`
-  `2 days,  4:13:02.266`
-  `5hr34m56s`
-  `5 hours, 34 minutes, 56 seconds`
-  `5 hrs, 34 mins, 56 secs`
-  `2 days, 5 hours, 34 minutes, 56 seconds`
-  `1.2 m`
-  `1.2 min`
-  `1.2 mins`
-  `1.2 minute`
-  `1.2 minutes`
-  `172 hours`
-  `172 hr`
-  `172 h`
-  `172 hrs`
-  `172 hour`
-  `1.24 days`
-  `5 d`
-  `5 day`
-  `5 days`
-  `5.6 wk`
-  `5.6 week`
-  `5.6 weeks`

 `Zulu.time_to()` /`Zulu.time_from()` と同様に、Deltaオブジェクトは`Delta.format()`メソッドで人に優しい出力にすることができます。

```
 In [2]: # %load 25_time_tofrom.py
    ...: import zulu
    ...:
    ...: delta = zulu.parse_delta('2h 32m')
    ...: # <Delta [2:32:00]>
    ...:
    ...: t1 = delta.format()
    ...: assert t1 == '3 hours'
    ...:
    ...: t2 = delta.format(add_direction=True)
    ...: assert t2 == 'in 3 hours'
    ...:
    ...: t3 = zulu.parse_delta('-2h 32m').format(add_direction=True)
    ...: assert t3 == '3 hours ago'
    ...:
    ...: t4 = delta.format(granularity='day')
    ...: assert t4 == '1 day'
    ...:
    ...: t5 = delta.format(locale='de')
    ...: assert t5 == '3 Stunden'
    ...:
    ...: t6 = delta.format(locale='fr', add_direction=True)
    ...: assert t6 == 'dans 3 heures'
    ...:
    ...: t7 = delta.format(threshold=0)
    ...: assert t7 == '0 years'
    ...:
    ...: t8 = delta.format(threshold=0.1)
    ...: assert t8 == '0 days'
    ...:
    ...: t9 = delta.format(threshold=0.2)
    ...: assert t9 == '3 hours'
    ...:
    ...: t10 = delta.format(threshold=5)
    ...: assert t10 == '152 minutes'
    ...:
    ...: t11 = delta.format(threshold=155)
    ...: assert t11 == '9120 seconds'
    ...:
    ...: t12 = delta.format(threshold=155, granularity='minute')
    ...: assert t12 == '152 minutes'
    ...:
    ...: t13 = delta.format(format='long')
    ...: assert t13 == '3 hours'
    ...:
    ...: t14 = delta.format(format='short')
    ...: assert t14 == '3 hr'
    ...:
    ...: t15 = delta.format(format='narrow')
    ...: assert t15 == '3h'
    ...:

```



## ユーティリティー関数

### zulu.to_seconds()
マイクロ秒から週単位までの時間単位を簡単に秒単位に変換します。

```
 In [2]: # %load 26_to_seconds.py
    ...: import zulu
    ...:
    ...: t1 = zulu.to_seconds(seconds=5, minutes=2, hours=3, days=2, weeks=1)
    ...: assert t1 == 788525.0
    ...:
    ...: t2 = zulu.to_seconds(milliseconds=25300, seconds=5, minutes=2)
    ...: assert t2 == 150.3
    ...:

```

### zulu.Timer()
タイマーオブジェクトは、経過時間を記録したり、タイマーとして使用することができます。

```
 In [2]: # %load 27_timer.py
    ...: import zulu
    ...:
    ...: timer = zulu.Timer()
    ...: v1 = timer.start()
    ...: # <zulu.timer.Timer at 0x7fdb0e0b6180>
    ...:
    ...: v2 = timer.started()
    ...: assert v2 == True
    ...:
    ...: v3 = timer.stopped()
    ...: assert v3 == False
    ...:
    ...: v4 = timer.elapsed()
    ...: # 0.0001289844512939453
    ...:
    ...: v5 = timer.stop()
    ...: # <zulu.timer.Timer at 0x7fb17f63b300>
    ...:
    ...: v6 = timer.elapsed()
    ...: # 0.0001499652862548828
    ...:

```

コードブロックの継続時間を把握するためのコンテキストマネージャーとして使用できます。

タイマーとしての利用方法は次のとおりです。

```
 In [2]: # %load 28_timer_context_manager.py
    ...: import zulu
    ...: import time
    ...:
    ...: timer = zulu.Timer()
    ...:
    ...: with timer:
    ...:     time.sleep(1)
    ...:
    ...: # これは次と同じこと
    ...: with zulu.Timer() as timer:
    ...:     time.sleep(1)
    ...:
    ...: v1 = timer.elapsed()
    ...: # 1.0052082538604736
    ...:
    ...: # 複数回使用して持続時間を蓄積できる
    ...: with timer:
    ...:     time.sleep(2)
    ...:
    ...: v2 = timer.elapsed()
    ...: # 3.0064713954925537
    ...:
    ...: # タイマーのリセット
    ...: v3 = timer.reset()
    ...: # <zulu.timer.Timer at 0x7fa53c185140>
    ...:
    ...: v4 = timer.started()
    ...: assert v4 == False
    ...:
    ...: v5 = timer.elapsed()
    ...: # 0
    ...:

```

カウントダウンタイマーとしての使用方法は次のようになります。

```
 In [2]: # %load 29_count_down_timer.py
    ...: import zulu
    ...: import time
    ...:
    ...: # 最大15秒のつタイマー
    ...: timer = zulu.Timer(timeout=15)
    ...: v1 = timer.start()
    ...: # <zulu.timer.Timer at 0x7fa8c0b8bf80>
    ...:
    ...: v2 = timer.done()
    ...: assert v2 == False
    ...:
    ...: v3 = timer.remaining()
    ...: # 14.999913930892944
    ...:
    ...: time.sleep(5)
    ...:
    ...: v4 = timer.remaining()
    ...: # 9.99487590789795
    ...:
    ...: time.sleep(10)
    ...:
    ...: v5 = timer.done()
    ...: assert v5 == True
    ...:
    ...: v6 = timer.remaining()
    ...: # -0.009467124938964844
    ...:
    ...: v7 = timer.start()
    ...: # <zulu.timer.Timer at 0x7fa8c0b8bf80>
    ...:
    ...: v8 = timer.done()
    ...: assert v8 == False
    ...:
```


## 参考
- [zulu ドキュメント](https://zulu.readthedocs.io/en/latest/])
- [zulu ソースコード](https://github.com/dgilland/zulu])
