deloreanを使って日時処理をしてみよう
=================
![](images/delorean_logo.png)


## delorean について

Deloreanは、Pythonで datetime を扱う際に生じる面倒な手続きを簡単にしてくれるライブラリです。タイミングが非常にデリケートな問題であることを理解した上で、Deloreanは datetime生成や、シフトなどの操作を、より明確でトラブルの少ないソリューションを提供することを設計方針にされています。

delorean とは、映画 [Backto the future](https://www.imdb.com/title/tt0088763/?ref_=fn_al_tt_1])  に登場する[車](https://www.imdb.com/title/tt0088763/mediaviewer/rm670349313/])の名前です。映画ではタイムトラベルが多く扱われているため、datetimeを扱うモジュールとしてDeloreanと名付けられています。

Delorean は内部的には [pytz](https://pypi.org/project/pytz/]) と [dateutil](https://pypi.org/project/python-dateutil/]) を用いています。

## インストール

delorean のインストールは pip で行います。

```
 # linux or mac
 $ python -m pip install delorean

 # Windows
 $ py -3 -m pip install delorean

```

## delorean のないとき.../あるとき...
もしdeloreanがなくて、旧来の方法を使うのであれば次のようなコードになります。

```
 In [2]: # %load 01_no_flux_capacitor.py
    ...: from datetime import datetime
    ...: import pytz
    ...:
    ...: jst = pytz.timezone('Asia/Tokyo')
    ...: d = datetime.now(pytz.utc)
    ...: d = jst.normalize(d.astimezone(jst))
    ...:
    ...: # print(d)
    ...:

 In [3]: print(d)
 2021-09-05 10:55:17.800485+09:00

```

これを delorean を使って記述すると次のようになります。

```
 In [2]: # %load 02_use_delorean.py
    ...: from delorean import Delorean
    ...:
    ...: d = Delorean()
    ...: d = d.shift('Asia/Tokyo')
    ...:
    ...: # print(d)
    ...:

 In [3]: print(d)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 11, 1, 2, 762193), timezone='Asia/Tokyo')

```

delorean を使うととてもシンプルに記述できることがわかりますよね。

それでは、delorean の使い方を説明してゆきましょう。

> **UTC(Coordinated Universal Time / 協定世界時)** 、**JST(Japan Standard Time / 日本標準時)**
> UTCはセシウム原子を利用したセシウム原子時計を基本にした、現在世界で標準となっている時間
> JSTはUTCを9時間後退させた時間で UTC-9 を表記されることもある。


## 時間の作り方
deloreanで時間を作ることは、とても簡単です。
まずは、Delorean クラスをインポートしてインスタンスオブジェクトを生成します。

```
 In [2]: # %load 03_make_datetime_step1.py
    ...: from delorean import Delorean
    ...:
    ...: d = Delorean()
    ...:
    ...: # print(d)
    ...:

 In [3]: print(d)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 2, 11, 24, 864037), timezone='UTC')

```

これだけで、現在の日付とUTCタイムゾーンを使って、datetime オブジェクトを作成したことになります。
このオブジェクトはUTCタイムゾーンですが、これを他のタイムゾーンに標準化する場合は次にように記述します。

```
 In [5]: # %load 03_make_datetime_step2.py
    ...: d = d.shift("Asia/Tokyo")
    ...:
    ...: # print(d)
    ...: # print(d.datetime)
    ...: # print(d.date)
    ...: # print(d.native)
    ...: # print(d.epoch)
    ...:

 In [6]: print(d)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 11, 11, 24, 864037), timezone='Asia/Tokyo')

 In [7]: print(d.datetime)
 2021-09-05 11:11:24.864037+09:00

 In [8]: print(d.date)
 2021-09-05

 In [9]: print(d.naive)
 2021-09-05 02:21:54.506110

 In [10]: print(d.epoch)
 1630840284.864037

```

 `shift()` メソッドを呼び出すだけで、タイムゾーンの変更され、ローカライズされた datetime オブジェクトや日付を簡単に返すことができます。

[**　タイムゾーン]
タイムゾーンについは pytz モジュールを使っています。

```
 In [2]: # %load 04_pytz.py
   ...: import pytz
   ...: from pprint import pprint
   ...:
   ...: v1 = pytz.common_timezones
   ...: v2 = [zone for zone in pytz.common_timezones if 'Tokyo' in zone]
   ...:
   ...: # pprint(v1)
   ...: # print(v2)
   ...:

 In [3]: pprint(v1)
 ['Africa/Abidjan',
  'Africa/Accra',
  'Africa/Addis_Ababa',
  (中略)
  'US/Mountain',
  'US/Pacific',
  'UTC']

 In [4]: print(v2)
 ['Asia/Tokyo']

```

また、Unixのタイムスタンプを使ってDeloreanオブジェクトを作成することもできます。

```
 In [2]: # %load 05_from_epoch.py
    ...: from delorean import epoch
    ...:
    ...: d = epoch(1630807884.864037).shift("Asia/Tokyo")
    ...:
    ...: # print(d)
    ...:

 In [3]: print(d)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 11, 11, 24, 864037), timezone='Asia/Tokyo')

```

ご覧のように、deloreanはDeloreanオブジェクトを返します。このオブジェクトを適切なタイムゾーンにシフトすることで、先ほどの元のdatetimeオブジェクトを取り戻すことができます。

>注意
>Deloreanオブジェクトを比較する場合、エポック時間が比較のために内部で使用されます。これにより、異なるタイムゾーンのDeloreanオブジェクトを比較する際に、最も正確に比較することができます。

Deloreanはローカライズされたデータタイムを受け入れることができます。つまり、以前にローカライズされたデータタイムオブジェクトがあった場合、デロリアンはこれらの値を受け入れ、関連するタイムゾーンとデータタイム情報をDeloreanオブジェクトに設定します。

> 注意
>ローカライズされたdatetimeオブジェクトにタイムゾーンを渡した場合、datetimeオブジェクトにはタイムゾーン情報が既に関連付けられているため、タイムゾーンは無視されます。

```
 In [2]: # %load 06_from_localized_datetime.py
    ...: from delorean import Delorean
    ...: from pytz import timezone
    ...: from datetime import datetime
    ...:
    ...: tz = timezone("Asia/Tokyo")
    ...: dt = tz.localize(datetime.utcnow())
    ...: d1 = Delorean(datetime=dt)
    ...:
    ...: d2 = Delorean(datetime=dt, timezone="Asia/Tokyo")
    ...:
    ...: # print(dt)
    ...: # print(d1)
    ...: # print(d2)
    ...:

 In [3]: print(dt)
 2021-09-05 02:34:59.267580+09:00

 In [4]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 2, 34, 59, 267580), timezone='Asia/Tokyo')

 In [5]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 2, 34, 59, 267580), timezone='Asia/Tokyo')

```

## 時間の演算
delorean は timedelta 演算もできます。timedelta 演算 はDeloreanオブジェクトに加算したり、Deloreanオブジェクトから減算したりすることができます。また、Delorean オブジェクトから別のDelorean オブジェクトを減算して、それらの間の時刻差(timedelta)を得ることもできます。

```
 In [2]: # %load 07_timedelta.py
    ...: from delorean import Delorean
    ...: from datetime import datetime, timedelta
    ...:
    ...: d1 = Delorean()
    ...: d1s = f'{d1}'
    ...: d1 += timedelta(hours=2)
    ...: d2 = d1 - timedelta(hours=2)
    ...: d3 = d1 + timedelta(hours=2)
    ...: d4 = d2 - d1
    ...:
    ...: # print(d1s)
    ...: # print(d1)
    ...: # print(d2)
    ...: # print(d3)
    ...: # print(d4)
    ...:

 In [3]: print(d1s)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 2, 43, 55, 788580), timezone='UTC')

 In [4]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 4, 43, 55, 788580), timezone='UTC')

 In [5]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 2, 43, 55, 788580), timezone='UTC')

 In [6]: print(d3)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 6, 43, 55, 788580), timezone='UTC')

 In [7]: print(d4)
 -1 day, 22:00:00

```

Delorean オブジェクトは、UTCで同じ時間を表している場合は、等しいとみなされます。

```
 In [2]: # %load 08_obj_omparison.py
    ...: from delorean import Delorean
    ...: from datetime import datetime, timedelta
    ...:
    ...: # JST = UTC+9
    ...: d1 = Delorean(datetime(2021, 9, 5, 9), timezone='Asia/Tokyo')
    ...: d2 = Delorean(datetime(2021, 9, 5), timezone='UTC')
    ...:
    ...: v = d1 == d2
    ...:
    ...: # print(d1)
    ...: # print(d2)
    ...: # print(v)
    ...:

 In [3]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 9, 0), timezone='Asia/Tokyo')

 In [4]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 0, 0), timezone='UTC')

 In [5]: print(v)
 True

```

## 自然言語
Deloreanクラスは、特定の日付を他の日付と比較して取得する方法を数多く提供していますが、来年や次の木曜日のような単純なものを取得するのは非常に面倒です。

delorean はこのような動作のためにいくつかの便利な機能を提供しています。
例えば、今日から次の火曜日を取得したい場合は、 `next_tuesday()` を呼び出します。

```
 In [2]: # %load 09_next_tuesday.py
    ...: from delorean import Delorean
    ...:
    ...: d1 = Delorean()
    ...: d2 = d1.next_tuesday()
    ...:
    ...: # print(d1)
    ...: # print(d2)
    ...:

 In [3]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 3, 36, 55, 945364), timezone='UTC')

 In [4]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 9, 7, 3, 36, 55, 945364), timezone='UTC')

```

先週の火曜日であれ、2つ前の火曜日の午前0時であれ、そのままの表記です。

```
 In [2]: # %load 10_last_tuesday.py
    ...: from delorean import Delorean
    ...:
    ...: d = Delorean()
    ...: d1 = d.last_tuesday()
    ...: d2 = d.last_tuesday(2).midnight
    ...:
    ...: # print(d1)
    ...: # print(d2)
    ...:

 In [3]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 8, 31, 3, 41, 16, 615875), timezone='UTC')

 In [4]: print(d2)
 2021-08-24 00:00:00+00:00

 In [5]: !cal -3
     August 2021          September 2021         October 2021
 Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
  1  2  3  4  5  6  7            1  2  3  4                  1  2
  8  9 10 11 12 13 14   5  6  7  8  9 10 11   3  4  5  6  7  8  9
 15 16 17 18 19 20 21  12 13 14 15 16 17 18  10 11 12 13 14 15 16
 22 23 24 25 26 27 28  19 20 21 22 23 24 25  17 18 19 20 21 22 23
 29 30 31              26 27 28 29 30        24 25 26 27 28 29 30
                                             31
```

## 時刻を指定してオブジェクトを生成
Deloreanオブジェクトの  `replace()` メソッドを使えば、datetimeの `replace()` メソッドのように、時、分、秒、年などをs指定してDelorean オブジェクトを生成したり、置き換えたりすることができます。

```
 In [2]: # %load 11_replace.py
    ...: from delorean import Delorean
    ...: from datetime import datetime
    ...:
    ...: d1 = Delorean(datetime(2021, 5, 24, 12, 15), timezone='Asia/Tokyo')
    ...: d2 = d1.replace(hour=8)
    ...:
    ...: # print(d1)
    ...: # print(d2)
    ...:

 In [3]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 5, 24, 12, 15), timezone='Asia/Tokyo')

 In [4]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 5, 24, 8, 15), timezone='Asia/Tokyo')

```

## 切り捨て
多くの場合では、datetimeオブジェクトに含まれるミリ秒や秒数を気にすることはありません。例えば、同じ分(minutes)に発生した日付を検索するのは面倒なことです。比較を行う前に、ゼロを気にしない単位に置き換えるという面倒な作業を行わなければなりません。

Deloreanには、ミリ秒、秒、分、時間などの異なる単位の時間を簡単に切り詰めることができるメソッドが用意されています。

```
 In [2]: # %load 12_truncation.py
    ...: from delorean import Delorean
    ...:
    ...: d1 = Delorean()
    ...: d2 = d1.truncate('second')
    ...: d3 = d1.truncate('hour')
    ...:
    ...: # print(d1)
    ...: # print(d2)
    ...: # print(d3)
    ...:

 In [3]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 4, 0), timezone='UTC')

 In [4]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 4, 0), timezone='UTC')

 In [5]: print(d3)
 Delorean(datetime=datetime.datetime(2021, 9, 5, 4, 0), timezone='UTC')

```

また、deloreanは月や年のレベルでも切り捨てることができます。

```
 In [2]: # %load 13_truncation_other.py
    ...: from delorean import Delorean
    ...: from datetime import datetime
    ...:
    ...: d1 = Delorean(datetime=datetime(2021, 5, 24, 8, 30, 00, 555555),
    ...:               timezone="Asia/Tokyo")
    ...: d2 = d1.truncate('month')
    ...: d3 = d1.truncate('year')
    ...:
    ...: # print(d1)
    ...: # print(d2)
    ...: # print(d3)
    ...:

 In [3]: print(d1)
 Delorean(datetime=datetime.datetime(2021, 1, 1, 0, 0), timezone='Asia/Tokyo')

 In [4]: print(d2)
 Delorean(datetime=datetime.datetime(2021, 1, 1, 0, 0), timezone='Asia/Tokyo')

 In [5]: print(d3)
 Delorean(datetime=datetime.datetime(2021, 1, 1, 0, 0), timezone='Asia/Tokyo')

```

## 文字列解析
もう一つの問題は、日付を表す文字列の扱いです。Deloreanは、様々なAPIから取得したすべての日付文字列を解析することができます。

```
 In [2]: # %load 14_string_parse.py
    ...: from delorean import parse
    ...:
    ...: d = parse("2021/05/24 08:30:00 -0700")
    ...:
    ...: # print(d)
    ...:

 In [3]: print(d)
 Delorean(datetime=datetime.datetime(2021, 5, 24, 8, 30), timezone=pytz.FixedOffset(-420))

```

上記のように、渡された文字列にオフセットデータがある場合、deloreanは結果のオブジェクトをUTCに変換しますが、タイムゾーンの情報が渡されない場合は、UTCとして扱われます。

### 曖昧なケース
例えば、パースに渡された文字列が少し曖昧な場合があるかもしれません。 `"2021-05-06"` と渡された場合、これは2021年5月06日なのか、それとも2021年6月5日なのかが明確ではありません。

Delorean は  `dayfirst=True` 、`yearfirst=True` を前提としているため、以下のような優先順位になります。

 `dayfirst=True` 、`yearfirst=True`の場合。(YY：西暦年、MM: 月、DD: 日)

- 1. YY-MM-DD
- 2. DD-MM-YY
- 3. MM-DD-YY

例えば、デフォルトでは、Delorean は  `"'2021-05-06"` を2021年5月6日 と返します。

```
 In [2]: # %load 15_parse_default.py
    ...: from delorean import parse
    ...:
    ...: d = parse("2021-05-06")
    ...:
    ...: # print(d)
    ...:

 In [3]: print(d)
 Delorean(datetime=datetime.datetime(2021, 6, 5, 0, 0), timezone='UTC')

```

以下は、キーワード引数  `dayfirst` と`yearfirst`の残りの組み合わせの優先順位です。

 `dayfirst=False` 、`yearfirst=False`の場合。

- 1. MM-DD-YY
- 2. DD-MM-YY
- 3. YY-MM-DD

 `dayfirst=True` 、`yearfirst=False`の場合。

- 1. DD-MM-YY
- 2. MM-DD-YY
- 3. YY-MM-DD

 `dayfirst=False` 、`yearfirst=True`の場合。

- 1. YY-MM-DD
- 2. MM-DD-YY
- 3. DD-MM-YY


## ストップ
delorean は指定した間隔でオブジェクトを生成させることができます。

```
 In [2]: # %load 16_stops.py
    ...: from delorean import stops, HOURLY
    ...:
    ...: for stop in stops(freq=HOURLY, count=10):
    ...:     print(stop)
    ...:
 Delorean(datetime=datetime.datetime(2021, 9, 5, 4, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 5, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 6, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 7, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 8, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 9, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 10, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 11, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 12, 35, 23), timezone='UTC')
 Delorean(datetime=datetime.datetime(2021, 9, 5, 13, 35, 23), timezone='UTC')

```

 `stops()` は Delorean オブジェクトを生成するジェネレータです。
これを使うことで、毎日、毎時、などの構成が可能になります。次の10週間は毎週火曜日に、次の3ヶ月は1時間おきに、というようなことに使うことができます。

## より複雑に
これができるようになると、タイムゾーンを指定したり、反復の開始日と終了日を指定したりすることができます。

```
 In [2]: # %load 17_stops_begine_end.py
    ...: from delorean import stops, MONTHLY
    ...: from datetime import datetime
    ...:
    ...: d1 = datetime(2021, 5, 24)
    ...: d2 = datetime(2022, 5, 24)
    ...:
    ...: for stop in stops(freq=MONTHLY, count=20, timezone="Asia/Tokyo",
    ...:                   start=d1, stop=d2):
    ...:     print(stop)
    ...:
 Delorean(datetime=datetime.datetime(2021, 5, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 6, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 7, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 8, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 9, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 10, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 11, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 12, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 1, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 2, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 3, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 4, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 5, 24, 0, 0), timezone='Asia/Tokyo')

```

この例で、 `count` で返す数を20としているのに、12で終わっていることに注目してください。`end`で指定した時刻で終了していることが確認できます。
 `stops()` には、次の制約があります。

- 引数の  `start` と `stop` には datetime の値しか受け付けません。
-  `start` または `timezone` の値が指定されていない場合、`start` はローカライズされたUTCオブジェクトとして処理されます。
-  `timezone` が指定された場合は、UTCを正しいタイムゾーンに正規化します。

キーワード引数  `stop` しか設定されている場合は、上記の注意制約を逸脱すると次のようなエラーが発生します。

```
 In [2]: # %load 18_stops_error.py
    ...: from delorean import stops, MONTHLY
    ...: from datetime import datetime
    ...:
    ...: d1 = datetime(2021, 5, 24)
    ...: d2 = datetime(2022, 5, 24)
    ...:
    ...: for stop in stops(freq=MONTHLY, timezone="Asia/Tokyo", stop=d2):
    ...:     print(stop)
    ...:
 ---------------------------------------------------------------------------
 ValueError                                Traceback (most recent call last)
 <ipython-input-2-4d966e7165d3> in <module>
       6 d2 = datetime(2022, 5, 24)
       7
 ----> 8 for stop in stops(freq=MONTHLY, timezone="Asia/Tokyo", stop=d2):
       9     print(stop)
 (中略)
 ValueError: RRULE UNTIL values must be specified in UTC when DTSTART is timezone-aware

```

こうしたケースでは、まずは  `start` と`count`を指定して返されるオブジェクトの範囲を制限することができます。

```
 In [2]: # %load 19_stops_good.py
    ...: from delorean import stops, MONTHLY
    ...: from datetime import datetime
    ...:
    ...: d1 = datetime(2021, 5, 24)
    ...: d2 = datetime(2022, 5, 24)
    ...:
    ...: for stop in stops(freq=MONTHLY, count=13, timezone="Asia/Tokyo", start=d
    ...: 1):
    ...:     print(stop)
    ...:
 Delorean(datetime=datetime.datetime(2021, 5, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 6, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 7, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 8, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 9, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 10, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 11, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 12, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 1, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 2, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 3, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 4, 24, 0, 0), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 5, 24, 0, 0), timezone='Asia/Tokyo')

```

あるいは、どちらも使用せず、 `count` を使用して返される値の範囲だけで制限することもできます。
この場合、現在の時刻がstart に使用されて、制限できるのは個数だけになります。

```
 In [2]: # %load 20_stops_count_only.py
    ...: from delorean import stops, MONTHLY
    ...: from datetime import datetime
    ...:
    ...: for stop in stops(freq=MONTHLY, count=5, timezone="Asia/Tokyo"):
    ...:     print(stop)
    ...:
 Delorean(datetime=datetime.datetime(2021, 9, 5, 14, 9, 41), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 10, 5, 14, 9, 41), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 11, 5, 14, 9, 41), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2021, 12, 5, 14, 9, 41), timezone='Asia/Tokyo')
 Delorean(datetime=datetime.datetime(2022, 1, 5, 14, 9, 41), timezone='Asia/Tokyo')
```

## まとめ
delorean は名前のとおり時間(datetimeオブジェクト)を自由に操作することができます。処理したい目的の処理を簡単にコードできるので、非常に利用価値が高いものです。




## 参考
- [delorean ソースコード](https://github.com/myusuf3/delorean])
- [delorean 公式ドキュメント](https://delorean.readthedocs.io/en/latest/])


#datetime


