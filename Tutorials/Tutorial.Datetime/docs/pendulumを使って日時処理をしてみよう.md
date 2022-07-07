pendulumを使って日時処理をしてみよう
=================
## pendulumについて
多くの場合  `date-util` で日時処理は対応できますが、タイムゾーンをもっとうまく処理しようとすると`pyt` などの助けが必要になります。
pendulum は、これだけで日時処理とタイムゾーン処理が行える便利なモジュールです。

これから新しくコードを書くというのであれば、日時処理は  pendulum がよいでしょう。

### インストール
pendulum は pip で次のようにインストールします。

```
 # Linux or Mac
 $ python -m pip install pendulum

 # Windwos
 $ py -3 -m pip install pendulum
```

### DateTimeオブジェクトの生成
 `pendulum.datetime()` は`datetime.datetime()`の`DateTime`オブジェクトを生成するので、まったく同じように使用することができます。

```
 In [2]: # %load 01_intro.py
    ...: from datetime import datetime
    ...: import pendulum
    ...:
    ...: dt = pendulum.datetime(2020,5,24)
    ...:
    ...: # assert は与えた式が真のときは何も表示しない
    ...:
    ...: assert isinstance(dt, datetime)
    ...: assert dt.timezone.name == 'UTC'
    ...:

```

 `datetime.datetime()` と違い、タイムゾーンの情報もセットされています。
デフォルトのタイムゾーンはUTCになっています。

 `pendulum.datetime()` にキーワード引数`tz`で指定したタイムゾーンの`DateTime`オブジェクトを生成することができます。

```
 In [2]: # %load 02_datetime_tz.py
    ...: import pendulum
    ...:
    ...: dt_tokyo = pendulum.datetime(2020, 5, 24, tz='Asia/Tokyo')
    ...: dt_nyc = pendulum.datetime(2020, 5, 24, tz='America/New_York')
    ...: time_diff = dt_nyc.diff(dt_tokyo).in_hours()
    ...:
    ...: # dt_tokyo
    ...: # dt_nyc
    ...: # time_diff
    ...:

 In [3]: dt_tokyo
 Out[3]: DateTime(2020, 5, 24, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [4]: dt_nyc
 Out[4]: DateTime(2020, 5, 24, 0, 0, 0, tzinfo=Timezone('America/New_York'))

 In [5]: time_diff
 Out[5]: 13

```

 `datetime.now()` と違い `pendulum.now()` ではタイムゾーンが自動的にセットされます。
また、 `today()` 、`yesterday()`、`tommorow()` でタイムゾーンの指定ができます。

```
 In [2]: # %load 03_autoset_tz.py
    ...: from datetime import datetime
    ...: import pendulum
    ...:
    ...: dt_now = datetime.now()
    ...: pt_now = pendulum.now()
    ...:
    ...: today = pendulum.today()
    ...: yesterday = pendulum.yesterday()
    ...: tomorrow = pendulum.tomorrow("America/New_York")
    ...:
    ...: # dt_now
    ...: # pt_now
    ...:
    ...: # today
    ...: # yesterday
    ...: # tommorrow
    ...:

 In [3]: dt_now
 Out[3]: datetime.datetime(2021, 9, 27, 9, 36, 53, 927039)

 In [4]: pt_now
 Out[4]: DateTime(2021, 9, 27, 9, 36, 53, 927647, tzinfo=Timezone('Asia/Tokyo'))

 In [5]: today
 Out[5]: DateTime(2021, 9, 27, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [6]: yesterday
 Out[6]: DateTime(2021, 9, 26, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [7]: tomorrow
 Out[7]: DateTime(2021, 9, 27, 0, 0, 0, tzinfo=Timezone('America/New_York'))

```

タイムゾーンを指定して得られた時刻から、さらにタイムゾーンを指定して時刻を変更することができます。

```
 In [2]: # %load 04_timezone_swap.py
    ...: import pendulum
    ...:
    ...: dt_tokyo = pendulum.datetime(2020, 2, 2, tz='Asia/Tokyo')
    ...:
    ...: dt_nyc1 = dt_tokyo.in_timezone(tz='America/New_York')
    ...: dt_nyc2 = dt_tokyo.in_tz(tz='America/New_York')
    ...:
    ...: # dt_tokyo
    ...: # dt_nyc1
    ...: # dt_nyc2
    ...:

 In [3]: dt_tokyo
 Out[3]: DateTime(2020, 2, 2, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [4]: dt_nyc1
 Out[4]: DateTime(2020, 2, 1, 10, 0, 0, tzinfo=Timezone('America/New_York'))

 In [5]: dt_nyc2
 Out[5]: DateTime(2020, 2, 1, 10, 0, 0, tzinfo=Timezone('America/New_York'))

```


### 日時期間の取得
 `pendulum.duration()` を使うと、`datetime.timedelta()` よりも直感的に期間を求めることができるようになります。

 `DateTime` オブジェクトでの差分を求めると24時間が経過していないのですが、日差が-1となります。


```
 In [2]: # %load 05_datetime_diff.py
    ...: from datetime import *
    ...: import pytz
    ...:
    ...: d1 = datetime(2020, 1, 1, 1, 2, 3, tzinfo=pytz.UTC)
    ...: d2 = datetime(2019, 12, 31, 22, 2, 3, tzinfo=pytz.UTC)
    ...: delta = d2 - d1
    ...:
    ...: v1 = delta.days
    ...: v2 = delta.seconds
    ...: attrs = [attr for attr in dir(delta) if not attr.startswith('__')]
    ...:
    ...: # v1
    ...: # v2
    ...: # attrs
    ...:

 In [3]: v1
 Out[3]: -1

 In [4]: v2
 Out[4]: 75600

 In [5]: attrs
 Out[5]:
 ['days',
  'max',
  'microseconds',
  'min',
  'resolution',
  'seconds',
  'total_seconds']

```

これに対して  pendulum では次のように日差はゼロとなります。

```
 In [2]: # %load 06_pendulum_diff.py
    ...: import pendulum
    ...:
    ...: d1 = pendulum.datetime(2020, 1, 1, 1, 2, 3)
    ...: d2 = pendulum.datetime(2019, 12, 31, 22, 2, 3)
    ...:
    ...: delta = d2 - d1
    ...: v1 = delta.days
    ...: v2 = delta.seconds
    ...: v3 = delta.hours
    ...:
    ...: attrs = [attr for attr in dir(delta) if not attr.startswith('_')]
    ...:
    ...: # v1
    ...: # v2
    ...: # v3
    ...: # attrs
    ...:

 In [3]: v1
 Out[3]: 0

 In [4]: v2
 Out[4]: -10800

 In [5]: v3
 Out[5]: -3

 In [6]: attrs
 Out[6]:
 ['as_interval',
  'as_timedelta',
  'days',
  'end',
  'hours',
  'in_days',
  'in_hours',
  'in_minutes',
  'in_months',
  'in_seconds',
  'in_weeks',
  'in_words',
  'in_years',
  'invert',
  'max',
  'microseconds',
  'min',
  'minutes',
  'months',
  'range',
  'remaining_days',
  'remaining_seconds',
  'resolution',
  'seconds',
  'start',
  'total_days',
  'total_hours',
  'total_minutes',
  'total_seconds',
  'total_weeks',
  'weeks',
  'years']

```

また、pendulum では日差をオブジェクトには seonds だけでなく、hours などの多くの属性が提供されています。


### 日時のシフト
日時差と同じように簡単に指定した単位でシフトした日時情報を取得することができます。


```
 In [2]: # %load 07_shift.py
    ...: import pendulum
    ...:
    ...: dt_tokyo = pendulum.datetime(2020, 5, 24, 8, 20, 0, tz="Asia/Tokyo")
    ...:
    ...: dt1 = dt_tokyo.add(days=1)
    ...: dt2 = dt_tokyo.add(weeks=1)
    ...: dt3 = dt_tokyo.subtract(days=1)
    ...: dt4 = dt_tokyo.subtract(weeks=1)
    ...:
    ...: # dt1
    ...: # ...
    ...: # dt4
    ...:

 In [3]: dt1
 Out[3]: DateTime(2020, 5, 25, 8, 20, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [4]: dt2
 Out[4]: DateTime(2020, 5, 31, 8, 20, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [5]: dt3
 Out[5]: DateTime(2020, 5, 23, 8, 20, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [6]: dt4
 Out[6]: DateTime(2020, 5, 17, 8, 20, 0, tzinfo=Timezone('Asia/Tokyo'))

```

> pendulum.datetime.add(years=0, months=0, weeks=0,
>                       days=0, hours=0, minutes=0, seconds=0, microseconds=0)
> pendulum.datetime.add(years=0, months=0, weeks=0,
>                       days=0, hours=0, minutes=0, seconds=0, microseconds=0)
>
> 可変長の単位（年、月）を加減算するときは、現在の時刻から移動します。


```
 In [2]: # %load 08_duration.py
    ...: import pendulum
    ...:
    ...: it = pendulum.duration(years=2, months=3,
    ...:                        days=1177, seconds=7284, microseconds=1234)
    ...:
    ...: dt01 = it.years
    ...: dt02 = it.months
    ...: dt03 = it.weeks
    ...: dt04 = it.days
    ...: dt05 = it.hours
    ...: dt06 = it.seconds
    ...: dt07 = it.total_weeks()
    ...: dt08 = it.total_days()
    ...: dt09 = it.total_hours()
    ...: dt10 = it.total_minutes()
    ...: dt11 = it.total_seconds()
    ...: dt12 = it.in_weeks()
    ...: dt13 = it.in_days()
    ...: dt14 = it.in_hours()
    ...: dt15 = it.in_minutes()
    ...: dt16 = it.in_seconds()
    ...:
    ...: assert dt01 == 2
    ...: assert dt02 == 3
    ...: assert dt03 == 168
    ...: assert dt04 == 1997
    ...: assert dt05 == 2
    ...: assert dt06 == 7284
    ...: assert dt07 == 285.2977579385483
    ...: assert dt08 == 1997.0843055698379
    ...: assert dt09 == 47930.02333367611
    ...: assert dt10 == 2875801.400020567
    ...: assert dt11 == 172548084.001234
    ...: assert dt12 == 285
    ...: assert dt13 == 1997
    ...: assert dt14 == 47930
    ...: assert dt15 == 2875801
    ...: assert dt16 == 172548084
    ...:
    ...: attrs = [attr for attr in dir(it) if not attr.startswith('_')]
    ...: # attrs
    ...:

 In [3]: attrs
 Out[3]:
 ['as_timedelta',
  'days',
  'hours',
  'in_days',
  'in_hours',
  'in_minutes',
  'in_seconds',
  'in_weeks',
  'in_words',
  'invert',
  'max',
  'microseconds',
  'min',
  'minutes',
  'months',
  'remaining_days',
  'remaining_seconds',
  'resolution',
  'seconds',
  'total_days',
  'total_hours',
  'total_minutes',
  'total_seconds',
  'total_weeks',
  'weeks',
  'years']

```

-  `Duration.weeks` で得られる数値は日数の合計を基準としていて年と月は考慮しない
-  `DUration.days` で得られる数値は、timedeltaと同様に、期間内の日数の合計を表す
  - 年や月が指定されている場合は、近似値を使用する
-  `Duration.remain_days` で得られる数値は、フルウィークに含まれない残りの日数を表す
-  `Duration.seconds` で得られる数値は、互換性のためにtimedeltaクラスのように残りの秒数の全体の値を返す
-  `Duraation.remaing_seconds` で得られる数値は、時と分に含まれない秒数を返す。


### 日時情報文字列の読み取り

 pendulum でも日時情報文字列から`DateTime`オブジェクトを生成できます。

 pendulum_parse.py
```
 import pendulum

 dt = pendulum.parse('2020-02-02T02:02:02')
 print(dt)

 dt = pendulum.parse('2020-02-02T02:02:02', tz='America/New_York')
 print(dt)

 # NOT ISO-8601
 dt = pendulum.parse('1975-05-21 22:00:00')

 try:
     dt = pendulum.parse('31-01-01')
     print(dt)
 except:
     print('pendulum parse error.')

 dt = pendulum.parse('31-01-01', strict=False)
 print(dt)
```

 `strict=False` を与えると `date-util`と同じように読み取ることもできます。

```
 $ python  pendulum_parse.py
 2020-02-02T02:02:02+00:00
 2020-02-02T02:02:02-05:00
 pendulum parse error.
 2031-01-01T00:00:00+00:00
```

- RFC 3339
  - 文字列： `1996-12-19T16:39:57-08:00` → 出力: `1996-12-19T16:39:57-08:00`
  - 文字列： `1990-12-31T23:59:59Z` → 出力: `1990-12-31T23:59:59+00:00`
- ISO 8601
  - 文字列： `20161001T143028+0530` → 出力: `2016-10-01T14:30:28+05:30`
  - 文字列： `20161001T14` → 出力: `2016-10-01T14:00:00+00:00`
- 日付(Date)
  - 文字列： `2012` → 出力: `2012-01-01T00:00:00+00:00`
  - 文字列： `2012-05-03` → 出力: `2012-05-03T00:00:00+00:00`
  - 文字列： `20120503` → 出力: `2012-05-03T00:00:00+00:00`
  - 文字列： `2012-05` → 出力: `2012-05-01T00:00:00+00:00`
- 基準日(Ordinal day)
  - 文字列： `2012-007` → 出力: `2012-01-07T00:00:00+00:00`
  - 文字列： `201200` → 出力: `2012-01-07T00:00:00+00:00`
- 週番号(Week number)
  - 文字列： `2012-W05` → 出力: `2012-01-30T00:00:00+00:00`
  - 文字列： `2012W05` → 出力: `2012-01-30T00:00:00+00:00`
  - 文字列： `2012-W05-5` → 出力: `2012-02-03T00:00:00+00:00`
  - 文字列： `2012W055` → 出力: `2012-02-03T00:00:00+00:00`
- 時刻(Time) - 時刻情報の読み取りだけを行う（年月日はnowから）
  - 文字列： `00:00` → 出力：`2016-12-17T00:00:00+00:00`
  - 文字列： `12:04:23` → 出力：`2016-12-17T12:04:23+00:00`
  - 文字列： `120423` → 出力：`2016-12-17T12:04:23+00:00`
  - 文字列： `12:04:23.45` → 出力：`2016-12-17T12:04:23.450000+00:00`
- インターバル(Interval)
  - 文字列:  `2007-03-01T13:00:00Z/2008-05-11T15:30:00Z`
    - 出力： `2007-03-01T13:00:00+00:00 -> 2008-05-11T15:30:00+00:00`
  - 文字列： `2008-05-11T15:30:00Z/P1Y2M10DT2H30M`
    - 出力： `2008-05-11T15:30:00+00:00 -> 2009-07-21T18:00:00+00:00`
  - 文字列： `P1Y2M10DT2H30M/2008-05-11T15:30:00Z`
    - 出力： `2007-03-01T13:00:00+00:00 -> 2008-05-11T15:30:00+00:00`

 `pendulum.parse()` に `exact=True` を与えると、与えた文字列に応じた`DateTime`オブジェクトが生成されます。


 pendulum_parse_exact.py
```
 import pendulum

 dt = pendulum.parse('2012-05-03')
 print(dt)
 dt = pendulum.parse('2012-05-03', exact=True)
 print(dt)

 dt = pendulum.parse('12:04:23')
 print(dt)
 dt = pendulum.parse('12:04:23', exact=True)
 print(dt)
```

```
 $ python  pendulum_parse_exact.py
 2012-05-03T00:00:00+00:00
 2012-05-03
 2020-03-09T12:04:23+00:00
 12:04:23
```

### 日時情報の文字列への変換
 `DateTime` オブジェクトの `strftime()` メソッドは文字列を返しますが、`pendulum.from_format()` は `DateTime` オブジェクトを生成します。

```
 In [2]: # %load 09_parse.py
    ...: import pendulum
    ...:
    ...: dt = pendulum.datetime(2020, 3, 4, tz='UTC')
    ...: # assert は与えた式が真のときは何も表示しない
    ...:
    ...: dt1 = pendulum.parse('2020/03/04')
    ...: assert dt == dt1
    ...:
    ...: dt2 = pendulum.parse('2020-03-04')
    ...: assert dt == dt2
    ...:
    ...: # dateutil ではOKだけど、pendulum ではエラーになるパターン
    ...: # dt3 = pendulum.parse('2020/Mar/04')
    ...: # dt4 = pendulum.parse('2020-March-04')
    ...: # dt5 = pendulum.parse('04-Mar-2020')
    ...: # dt6 = pendulum.parse('04-March-2020')
    ...: # dt7 = pendulum.parse('04-Mar-20')
    ...: # dt8 = pendulum.parse('04-March-20')
    ...:
    ...: dt2 = pendulum.datetime(2020, 3, 4, 2, 2, 2, tz='UTC')
    ...: dt10 = pendulum.parse('2020-03-04T02:02:02')
    ...: assert dt2 == dt10
    ...:
    ...: dt3 = pendulum.datetime(2020, 3, 4, 2, 2, 2, tz='America/New_York')
    ...: dt11 = pendulum.parse('2020-03-04T02:02:02', tz='America/New_York')
    ...: assert dt3 == dt11
    ...:
    ...: # NOT ISO-8601
    ...: dt12 = pendulum.parse('2020-03-04 02:02:02')
    ...: assert dt2 == dt12
    ...:
    ...: try:
    ...:     dt13 = pendulum.parse('31-01-01')
    ...: except:
    ...:     dt13 = 'pendulum parse error'
    ...:
    ...: assert dt13 == 'pendulum parse error'
    ...:
    ...: dt4 = pendulum.datetime(2031, 1, 1)
    ...: dt14 = pendulum.parse('31-01-01', strict=False)
    ...: assert dt4 == dt14
    ...:

```

多彩なメソッドで日時情報文字列を生成することができます。
デフォルトは  `iso_format()` です。

```
 In [2]: # %load 10_convert_strpy
   ...: import pendulum
   ...:
   ...: dt = pendulum.datetime(2020, 2, 2, 2, 2, 2, tz='Asia/Tokyo')
   ...:
   ...: st1 = dt.isoformat()
   ...: assert st1 == '2020-02-02T02:02:02+09:00'
   ...:
   ...: st2 = dt.to_date_string()
   ...: assert st2 == '2020-02-02'
   ...:
   ...: st3 = dt.to_formatted_date_string()
   ...: assert st3 == 'Feb 02, 2020'
   ...:
   ...: st4 = dt.to_time_string()
   ...: assert st4 == '02:02:02'
   ...:
   ...: st5 = dt.to_datetime_string()
   ...: assert st5 == '2020-02-02 02:02:02'
   ...:
   ...: st6 = dt.to_day_datetime_string()
   ...: assert st6 == 'Sun, Feb 2, 2020 2:02 AM'
   ...:

```

datetime オブジェクトをよく利用されるフォーマットで表示する例です。

```
 In [2]: # %load 11_to_format.py
    ...: import pendulum
    ...:
    ...: dt = pendulum.datetime(2020,5,24,8,20,0, tz='Asia/Tokyo')
    ...:
    ...: ct01 = dt.to_atom_string()
    ...: assert ct01 == '2020-05-24T08:20:00+09:00'
    ...:
    ...: ct02 = dt.to_cookie_string()
    ...: assert ct02 == 'Sunday, 24-May-2020 08:20:00 JST'
    ...:
    ...: ct03 = dt.to_iso8601_string()
    ...: assert ct03 == '2020-05-24T08:20:00+09:00'
    ...:
    ...: ct04 = dt.to_rfc822_string()
    ...: assert ct04 == 'Sun, 24 May 20 08:20:00 +0900'
    ...:
    ...: ct05 = dt.to_rfc850_string()
    ...: assert ct05 == 'Sunday, 24-May-20 08:20:00 JST'
    ...:
    ...: ct06 = dt.to_rfc1036_string()
    ...: assert ct06 == 'Sun, 24 May 20 08:20:00 +0900'
    ...:
    ...: ct07 = dt.to_rfc1123_string()
    ...: assert ct07 == 'Sun, 24 May 2020 08:20:00 +0900'
    ...:
    ...: ct08 = dt.to_rfc2822_string()
    ...: assert ct08 == 'Sun, 24 May 2020 08:20:00 +0900'
    ...:
    ...: ct09 = dt.to_rfc3339_string()
    ...: assert ct09 == '2020-05-24T08:20:00+09:00'
    ...:
    ...: ct10 = dt.to_rss_string()
    ...: assert ct10 == 'Sun, 24 May 2020 08:20:00 +0900'
    ...:
    ...: ct11 = dt.to_w3c_string()
    ...: assert ct11 == '2020-05-24T08:20:00+09:00'
    ...:

```

 pendulum では `datetime` の `strfrime()` メソッドを使うこともできますが、
 `format()` メソッドは判読しやすい指示子を使え、より多彩な文字列変換を行うことができます。

```
 In [2]: # %load 12_strftme.py
    ...: import pendulum
    ...:
    ...: dt = pendulum.datetime(2020, 2, 2, 2, 2, 2, tz='Asia/Tokyo')
    ...: dt_str = 'Sunday 2nd of February 2020 02:02:02 AM'
    ...:
    ...: st1 = dt.strftime('%A %-dnd of %B %Y %I:%M:%S %p')
    ...: assert st1 == dt_str
    ...:
    ...: st2 =  dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
    ...: assert st2 == dt_str
    ...:

```

 pendulum指示子

| 指示子 | 意味 | 例 |
|:--|:--|:--|
| YYYY | 年(4桁) | 2020 |
| YY | 年(2桁) | 20 |
| Q | 期（クォータ:Quator) | 1, 2, 3, 4 |
| Qo | 期（クォータ:Quator) | 1st, 2nd, 3rd, 4th |
| MMMM | 月名 | January |
| MMM | 月名(短縮形) | Jan |
| MM | 月名の数値表記(01-12) | 01 |
| M | 月名の数値表記(1-12) | 1 |
| Mo | 月名の数値の英語表記(1st, 2nd, 3rd...12th) | 1st |
| DDDD | ゼロ埋めした10進数で表記した年中の日にち(001-366) | 001 |
| DDD | 10進数で表記した年中の日にち(1-366) | 1 |
| DD | ゼロ埋めした10進数で表記した月中の日にち(01-31) | 01 |
| D | 10進数で表記した月中の日にち(1-31) | 1 |
| Do | 月中の日にち英語表記(1st,2nd,3rd...30th, 31st) | 1st |
| dddd | 曜日名(Monday, Tuesday...Sunday) | Monday |
| ddd | 曜日名の３文字短縮形(Mon, Tue,...,Sun) | Mon |
| dd | 曜日名の２文字短縮形(Mo, Tu, ..., Su) | Mo |
| d | 曜日名の数値表記(0-6, 0 はSunday) | 1 |
| E | 曜日名のISO数値表記(1-7, 7はSunday) | 1 |
| HH | ゼロ埋めした時の２４時間表記 (00-23) | 01 |
| H | 時の24時間表記 (0-23) | 1 |
| hh | ゼロ埋めした時の12時間表記(01-12) | 01 |
| h | 時の12時間表記(1-12) | 1 |
| mm | ゼロ埋めした分(00-59) | 01 |
| m | 分(0-59) | 0 |
| ss | ゼロ埋めした秒(00-59) | 0 |
| s | 秒(1-59) | 0 |
| S | 10分の1秒単位の分数秒 (0,1,..9) | 0 |
| SS | 100分の1秒単位の分数秒(00,01..99) | 00 |
| SSS | 1000分の1秒単位の分数秒(000,0001...999) | 000 |
| A | AM/PM | AM |
| Z | タイムゾーン(時差の時刻表記) | -09:00 |
| ZZ | タイムゾーン(時差の数値表記） | -0900 |
| z | タイムゾーン(文字列） | Asia/Tokyo |
| zz | タイムゾーン(短縮文字列) | JST |
| X | タイムスタンプの秒表示 | 1234567890.123 |
| x | タイムスタンプのマイクロ秒 | 1234567890123 |

 pendulum ローカル時刻指示子

| 指示子 | 意味 | 例 |
|:--|:--|:--|
| LT | ローカル時刻 | 8:30 PM |
| LTS | ローカル時刻 | 8:30:25 PM |
| L | 月番号/日/年 | 09/04/1986 |
| LL | 月/日/年 | September 4 1986 |
| LLL | 月/日/年 時刻 | September 4 1986 8:30 PM |
| LLLL | 曜日,月/日/年 時刻 | Thursday, September 4 1986 8:30 PM |


## 比較
基本的な演算子を使って簡単な比較ができます。比較はUTCタイムゾーンで行われるため、必ずしも見た目通りにはいかないことには注意してください。

```
 In [2]: # %load 13_comparison.py
    ...: import pendulum
    ...:
    ...: first = pendulum.datetime(2020, 5, 24, 8, 20, 0, 0, tz='Asia/Tokyo')
    ...: second = pendulum.datetime(2020, 5, 23, 19, 20, 0, 0, tz='America/New_Yo
    ...: rk')
    ...:
    ...: st1 = first.to_datetime_string()
    ...: assert st1 ==  '2020-05-24 08:20:00'
    ...: assert first.timezone_name == 'Asia/Tokyo'
    ...:
    ...: st2 = second.to_datetime_string()
    ...: assert st2 == '2020-05-23 19:20:00'
    ...: assert second.timezone_name == 'America/New_York'
    ...:
    ...: c1 = first == second
    ...: assert c1 == True
    ...:
    ...: c2 = first != second
    ...: assert c2 == False
    ...:
    ...: c3 = first > second
    ...: assert c3 == False
    ...:
    ...: c4 = first >= second
    ...: assert c4 == True
    ...:
    ...: c5 = first < second
    ...: assert c5 == False
    ...:
    ...: c6 = first <= second
    ...: assert c6 == True
    ...:
    ...: first = first.on(2020, 1, 1).at(0, 0, 0)
    ...: second = second.on(2020, 1, 1).at(0, 0, 0)
    ...:
    ...: c10 = first == second
    ...: assert c10 == False
    ...:
    ...: c11 = first != second
    ...: assert c11 == True
    ...:
    ...: c12 = first > second
    ...: assert c12 == False
    ...:
    ...: c13 = first >= second
    ...: assert c13 == False
    ...:
    ...: c14 = first < second
    ...: assert c14 == True
    ...:
    ...: c15 = first <= second
    ...: assert c15 == True
    ...:
    ...: # first
    ...: # second
    ...:

 In [3]: first
 Out[3]: DateTime(2020, 1, 1, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))

 In [4]: second
 Out[4]: DateTime(2020, 1, 1, 0, 0, 0, tzinfo=Timezone('America/New_York'))

```

よく使われるケースを処理するために、いくつかのシンプルなヘルパー関数が用意されています。何らかの方法で  `now()` と比較するメソッド（例：`is_today()`）では、インスタンスと同じタイムゾーンで `now()` が生成されます。

```
 In [2]: # %load 14_helper.py
    ...: import pendulum
    ...:
    ...: dt = pendulum.datetime(2020, 7, 20)
    ...: v1 = dt.is_past()
    ...: assert v1 == True
    ...:
    ...: v2 = dt.is_leap_year()
    ...: assert v2 == True
    ...:
    ...: born = pendulum.datetime(1962, 1, 13)
    ...: not_birthday = pendulum.datetime(2020, 10, 2)
    ...: birthday = pendulum.datetime(2021, 1, 13)
    ...: past_birthday = pendulum.now().subtract(years=50)
    ...:
    ...: v3 = born.is_birthday(not_birthday)
    ...: assert v3 == False
    ...:
    ...: v4 = born.is_birthday(birthday)
    ...: assert v4 == True
    ...:
    ...: # Compares to now by default
    ...: v5 = past_birthday.is_birthday()
    ...: assert v5 == True
    ...:

```


## 範囲
期間を指定して反復処理を行う場合は、 `period()` と `range()` メソッドを使用します。

```
 In [2]: # %load 15_range.py
    ...: import pendulum
    ...:
    ...: start = pendulum.datetime(2020, 5, 24)
    ...: end = pendulum.datetime(2020, 10, 2)
    ...: period = pendulum.period(start, end)
    ...:
    ...: dt = pendulum.datetime(2020, 7, 22)
    ...: v1 = dt in period
    ...: assert v1 == True
    ...:
    ...: for dt in period.range('months'):
    ...:     print(dt)
    ...:
 2020-05-24T00:00:00+00:00
 2020-06-24T00:00:00+00:00
 2020-07-24T00:00:00+00:00
 2020-08-24T00:00:00+00:00
 2020-09-24T00:00:00+00:00

```


## 参考
- [pendulum オフィシャルサイト](https://pendulum.eustace.io/])
- [IANA(Internet Assigned Numbers Authority) - TimeZone Database](https://www.iana.org/time-zones])
- [RFC 3339 Date and Time on the Internet: Timestamps](https://tools.ietf.org/html/rfc3339])


