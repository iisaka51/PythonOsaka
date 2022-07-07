DateTimeで日時処理をしてみよう
=================
## Datetime について
Python で日時処理を行う場合h、標準ライブラリの[datetime](https://docs.python.org/ja/3/library/datetime.html)モジュールを使うことになります。

-  `datetime.datetime` : 日時、日付と時刻
-  `datetime.date` : 日付
-  `datetime.time` : 時刻
-  `datetime.timedelta` : 時間差・経過日時

```
 In [2]: # %load 01_intro.py
    ...: import datetime
    ...:
    ...: t = datetime.datetime.now()
    ...:
    ...: # print(t)
    ...:

 In [3]: print(t)
 2021-09-27 07:24:55.979405
```

## エポックタイム
一般にLinux系OSでは日時を内部的に**エポックタイム(Epoch Time)**  (UNIX時刻と呼ばれることもある）というもので管理しています。エポックタイムはプラットフォーム依存ですが、ほとんどの場合、**協定世界時（UTC: Coordinated Universal Time)** の1970年01月01日 00:00:00 から経過した秒数となっています。Pythonでプラットフォームのエポックタイムの起点を知るには `time.gmtime(0)` を調べるとわかります。

```
 In [2]: # %load 02_gmtime.py
    ...: import time
    ...: t1 = time.time()
    ...: t2 = time.gmtime(0)
    ...:
    ...: # t1
    ...: # t2
    ...:

 In [3]: t1
 Out[3]: 1632695262.06526

 In [4]: t2
 Out[4]: time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=1, tm_isdst=0)

```



> **トリビア**
>  2001/09/09 01:46:40 (UTC) はエポックタイムでは 1000000000 となります。
>  2009/02/13 23:31:30 (UTC) はエポックタイムでは 1234567890 となります。
>
>  こんなものを理由にして世界中でパーティーが開かれました。
>   https://www.wired.com/2009/02/unix-lovers-to/

## タイムゾーン
#### 日本標準時 (JST: Japan Standard Time)
エポックタイムとUTC、JSTの関係は次表のようになります。

 EpochTime とUTC, JST

| EpochTime | UTC | JST(UTC+9) |
|:--|:--|:--|
| 0 | 1970/1/1 00:00:00 | 1970/1/1 09:00:00 |
| 1583237398.517091 | 2020-03-03 07:09:58.517150 | 2020-03-03 21:09:58.517150+09:00 |

こうした国ごとの標準時を扱うために、Linux系OSでは**タイムゾーン(Time Zone)** を環境変数 `TZ` に設定できるようになっています。

```
 In [2]: # %load 03_epoch_time.py
    ...: from datetime import datetime, timezone, timedelta
    ...:
    ...: utc_now = datetime.now(timezone.utc)
    ...: timezone_jst = timezone(timedelta(hours=9))
    ...:
    ...: t1 = utc_now.timestamp()
    ...: t2 = utc_now.astimezone(timezone_jst)
    ...:
    ...: # print(utc_now)
    ...: # print(t1)
    ...: # print(t2)
    ...:

 In [3]: print(utc_now)
 2021-09-26 22:31:27.781120+00:00

 In [4]: print(t1)
 1632695487.78112

 In [5]: print(t2)
 2021-09-27 07:31:27.781120+09:00

```

特定のタイムゾーンだけであればUTCとの時刻差を意識してプログラムすればよいのですが、
国際化を意識して各国の標準時やサマータイムなどに対応しようとすると、標準モジュールだけでは煩雑になりすぎます。
拡張モジュール `pytz` をインストールすると、Python でタイムゾーンを簡単に扱えるようになります。

インストールは次のように   `pip` コマンドを使います。
 bash
```
 pip install pytz
```

```
 In [2]: # %load 04_pytz.py
    ...: from datetime import datetime
    ...: import pytz
    ...:
    ...: utc = pytz.utc
    ...: now = datetime.now(utc)  # time.time() と等価
    ...: epoch = now.timestamp()
    ...:
    ...: tz = pytz.timezone('Asia/Tokyo')
    ...: timestamp = datetime.fromtimestamp(epoch, tz)
    ...:
    ...: # print(now)
    ...: # print(epoch)
    ...: # print(timestamp)
    ...:

 In [3]: print(now)
 2021-09-26 22:40:00.072625+00:00

 In [4]: print(epoch)
 1632696000.072625

 In [5]: print(timestamp)
 2021-09-27 07:40:00.072625+09:00

```

## Datetimeオブジェクトを作成
 `datetime.datetime()` に日時を引数で与えると `Datetime`オブジェクトが作成されます。
 `Datetime` オブジェクトにはたくさんのメソッドがあります。このうち `strftime()` メソッドに指示子を与えると、その変換指示に従った文字列を生成して返してくれます。

```
 In [2]: # %load 05_datetime_obj.py
    ...: import datetime
    ...:
    ...: dt = datetime.datetime(2020, 5, 24)
    ...: st = dt.strftime("%Y/%B/%d %A")
    ...:
    ...: # dt
    ...: # st
    ...: # dir(dt)
    ...:

 In [3]: dt
 Out[3]: datetime.datetime(2020, 5, 24, 0, 0)

 In [4]: st
 Out[4]: '2020/May/24 Sunday'

 In [5]: dir(dt)
 Out[5]:
 ['__add__',
  '__class__',
  '__delattr__',
  '__dir__',
  '__doc__',
  '__eq__',
  '__format__',
  '__ge__',
  '__getattribute__',
  '__gt__',
  '__hash__',
  '__init__',
  '__init_subclass__',
  '__le__',
  '__lt__',
  '__ne__',
  '__new__',
  '__radd__',
  '__reduce__',
  '__reduce_ex__',
  '__repr__',
  '__rsub__',
  '__setattr__',
  '__sizeof__',
  '__str__',
  '__sub__',
  '__subclasshook__',
  'astimezone',
  'combine',
  'ctime',
  'date',
  'day',
  'dst',
  'fold',
  'fromisocalendar',
  'fromisoformat',
  'fromordinal',
  'fromtimestamp',
  'hour',
  'isocalendar',
  'isoformat',
  'isoweekday',
  'max',
  'microsecond',
  'min',
  'minute',
  'month',
  'now',
  'replace',
  'resolution',
  'second',
  'strftime',
  'strptime',
  'time',
  'timestamp',
  'timetuple',
  'timetz',
  'today',
  'toordinal',
  'tzinfo',
  'tzname',
  'utcfromtimestamp',
  'utcnow',
  'utcoffset',
  'utctimetuple',
  'weekday',
  'year']

```


この例では、1962年1月13日の日付表示を変えて表示しています。
 `strftime()` メソッドには次の指示子を与えることができます。

 datetime

| 指定子 | 意味 | 例 |
|:--|:--|:--|
| %a | ロケールの曜日名の短縮形 | Sun |
| %A | ロケールの曜日名 | Sunday |
| %w | ロケールの曜日名の数値表記(0-6, 0 はSunday) | 0 |
| %d | ゼロ埋めした10進数で表記した月中の日にち(01-31) | 31 |
| %b | ロケールの月名の短縮形 | Dec |
| %B | ロケールの月名 | December |
| %m | ロケールの月名の数値表記(01-12) | 12 |
| %y | 西暦の短縮表記(2桁) | 20 |
| %Y | 西暦(4桁) | 2020 |
| %H | 時の２４時間表記 (00-23) | 17 |
| %I | 時の１２時間表記(01-12) | 05 |
| %p | AM/PM | PM |
| %M | ゼロ埋めした分(00-59) | 05 |
| %S | ゼロ埋めした秒(00-59) | 08 |
| %f | 10進数で表記をゼロ埋めしたマイクロ秒(000000-999999) | 123456 |
| %z | UTCオフセット( ±HHMM[SS[.ffffff]] の形式) | +0100 |
| %Z | タイムゾーンの名 | JST |
| %j | ゼロ埋めした10進数で表記した年中の日にち(001-366) | 365 |
| %U | ゼロ埋めした10進数で表記した年中の週番号（週始まりは日曜日)(00-53) | 52 |
| %W | ゼロ埋めした10進数で表記した年中の週番号（週始まりは月曜日)(00-53) | 52 |
| %c | ロケールの日時 | (注1) |
| %x | ロケールの日付 | 12/31/20 |
| %X | ロケールの日時 | 21:30:00 |
| %% | 文字％ |  |
注１: Thu Mar 03 17:41:00 2020

## f-StrtingでDateTimeオブジェクトから日時文字列に変換
f-String を使うと、 `strftime()` を呼び出さなくても、DateTimeオブジェクトから日時文字列に変換することができます。

```
 In [2]: # %load 06_datetime_fstring.py
    ...: import datetime
    ...:
    ...: dt = datetime.datetime(2020, 5, 24)
    ...: st = f'{dt:%Y/%B/%d %A}'
    ...:
    ...: # dt
    ...: # st
    ...:

 In [3]: dt
 Out[3]: datetime.datetime(2020, 5, 24, 0, 0)

 In [4]: st
 Out[4]: '2020/May/24 Sunday'

```

### ハンズオン
次のことを調べてみましょう。

- エポックタイムで2,000,000,000 はいつでしょうか。
- その日は今日から何日後でしょうか？

ヒント：エポックタイムの基準点を思い出してみましょう


> トリビア:
> Unix系OSでカレンダー表示のためのコマンド  `cal` には面白い実装がされています。
> まずは、実際に見てみましょう。
>
>$ cal 9 1752
>    September 1752
> Su Mo Tu We Th Fr Sa
>                1 2 14 15 16
> 17 18 19 20 21 22 23
> 24 25 26 27 28 29 30
>
> なにか変ですよね？
> これは、イギリスとその植民地でユリウス暦からグレゴリオ暦に切り替えられたのが、
> 1752年9月ということに由来しています。
> DateTimeにはこうした実装はありません。


参考:
- [Python公式ドキュメント datetime](https://docs.python.org/ja/3/library/datetime.html])
- [pytz オフィシャルサイト](https://pythonhosted.org/pytz/])
