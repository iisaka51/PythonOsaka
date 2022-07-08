pandasでの日時処理
=================
Pandas では時系列処理ができることもあり、日時処理をするためのメソッドが提供されています。
また、Pandasには DataFrame と Series という２種類のデータ型があり、それぞれ日時処理のためのメソッドが提供されています。


## 日時の文字列をdatetime型に変換

次のコードは、日時データのリストを Pandas の Series型データにしているものです。

```
 In [2]: # %load 01_series_datetime.py
    ...: import pandas as pd
    ...:
    ...: data = pd.Series(['2021-09-01','2021-09-02','2021-09-03'])
    ...: pdt = pd.to_datetime(data)
    ...:
    ...: # data
    ...: # pdt
    ...:

 In [3]: data
 Out[3]:
 0    2021-09-01
 1    2021-09-02
 2    2021-09-03
 dtype: object

 In [4]: pdt
 Out[4]:
 0   2021-09-01
 1   2021-09-02
 2   2021-09-03
 dtype: datetime64[ns]
```

 `data` をみると、Series の dtype型 は object ですが、それぞれの要素は str 型です。 `to_datetime()`関数にわたすことで、NumPy の `datetime64型 に変換されます。これは、datetime でいうところの Timestamp型です。

 `to_datetime()` 関数にキーワード引数 `format=` を与えると、与える日時文字列のフォーマットを指示することができます。

 format引数

| 記 | 説明 | 例 |
|:--|:--|:--|
| %Y | 4桁の年数 | 2020,2021… |
| %y | 2桁の年数 | 20 21... |
| %m | 2桁の月 01〜12 | 01, 09, 12... |
| %d | 2桁の日付 01〜31 | 01, 25, 31... |
| %H | 24時間表記の時間  00〜23  | 00, 12, 21.. |
| %I | 12時間表記の時間  01〜12 | 01, 09, 12.. |
| %M | 2桁の分 00〜59 | 00, 05, 38, 59.. |
| %S | 秒 00〜61 | 00, 15, 39, 60, 61.. |
|  |  | 60,61は00,01と同じ |
| %w | 整数表記された曜日 0(日曜)〜6(土曜)  | 1(月曜), 2(火曜), 6(土曜) |
| %U | 週番号 00〜53 日曜が週の始めとしてカウントされる。年を通しての週の番号 | 00, 03, 04, ...53 |
| %W | 週番号 00〜53 月曜が週の始めとしてカウントされる、年を通しての週の番号 | 00, 03, 04, ...53 |
| %z | UTC タイムゾーンからのオフセット +HHMMまたは-HHMMの形 | +0800, -0925,… |

 `"2021-09-05"` を例に考えてみると、じつはプログラム的に言えば非常に曖昧な文字列となります。
それは、2021年09月05日なのか、2021年05月09日なのかが、この文字列からは判別できません。日本でこの日時文字列をみると多くお人が2021年05月09日と判読lするかもしれませんが、’それは慣習であってプログラム上の仕様や定義ではないからです。こうしたときに、 `format=` キーワード引数を指定して期待通りに解析させることができます。

```
 n [2]: # %load 02_to_datetime.py
    ...: import pandas as pd
    ...:
    ...: t1 = pd.to_datetime('2021-09-05')
    ...: t2 = pd.to_datetime('2021/09/05')
    ...: t3 = pd.to_datetime('2021,09,05')
    ...: t4 = pd.to_datetime('2021-09-05', format='%Y-%d-%m')
    ...:
    ...: # print(t1)
    ...: # ...
    ...: # print(t4)
    ...:

 In [3]: print(t1)
 2021-09-05 00:00:00

 In [4]: print(t2)
 2021-09-05 00:00:00

 In [5]: print(t3)
 2021-05-01 00:00:00

 In [6]: print(t4)
 2021-05-09 00:00:00

```

Sieres 型なのでリストで文字列データを受け付けることが多くあります。

```
 In [2]: # %load 03_to_datetime_list.py
    ...: import pandas as pd
    ...:
    ...: d1 = pd.Series(['2021-09-01', '2021-09-02', '2021-09-03', '2021-09-04'])
    ...:
    ...: t1 = pd.to_datetime(d1, format='%Y-%m-%d')
    ...:
    ...: # print(t1)
    ...:

 In [3]: print(t1)
 0   2021-09-01
 1   2021-09-02
 2   2021-09-03
 3   2021-09-04
 dtype: datetime64[ns]

```

実際には DataFrame や Series のデータには欠損値としてNaN要素(Not a number)が含まれることもあります。この場合はどうでしょうか？　まず、試してみましょう。欠損値として NumPy の nan を入寮に与えておきます。

```
 n [2]: # %load 04_to_datetime_naT.py
    ...: import pandas as pd
    ...: import numpy as np
    ...:
    ...: d1 = pd.Series(['2021-09-01', np.nan, '2021-09-03', '2021-09-04'])
    ...: t1 = pd.to_datetime(d1, format='%Y-%m-%d')
    ...:
    ...: # print(t1)
    ...:

 In [3]: print(t1)
 0   2021-09-01
 1          NaT
 2   2021-09-03
 3   2021-09-04
 dtype: datetime64[ns]

```

NaT(Not a Time) としてうまく処理されています。

 `to_datetime()` メソッドで datetime64型に変換されたデータは、年(year), 月(month), 日(day) などの日時を表す属性をもっているため直接アクセスすることができます。

```
 n [2]: # %load 05_to_datetime_attr.py
    ...: import pandas as pd
    ...:
    ...: d1 = pd.Series(['2021-09-01', '2021-09-02', '2021-09-03', '2021-09-04'])
    ...:
    ...: t1 = pd.to_datetime(d1, format='%Y-%m-%d')
    ...: v1 = f'{t1[3].month}月{t1[3].day}日'
    ...:
    ...: # print(t1)
    ...: # print(v1)
    ...:

 In [3]: print(t1)
 0   2021-09-01
 1   2021-09-02
 2   2021-09-03
 3   2021-09-04
 dtype: datetime64[ns]

 In [4]: print(v1)
 9月4日

```

DataFrame から列や行を抽出されたデータは Series 型になります。確かめてみましょう。
次にCSVファイrうはGoogleを親会社Alphabet社([GOOG](https://finance.yahoo.com/quote/GOOG/history/]))の2021年08月の株価のヒストリカルデータです。

```
 % head GOOG.csv
 Date, Open, High, Low, Close, Adj Close, Volume
 Aug 31 2021, 2917.69, 2922.24, 2900.00, 2909.24, 2909.24, 1337800
 Aug 30 2021, 2894.09, 2929.79, 2892.00, 2909.39, 2909.39,  845800
 Aug 27 2021, 2842.25, 2900.22, 2840.40, 2891.01, 2891.01, 1228100
 Aug 26 2021, 2852.37, 2862.70, 2841.83, 2842.46, 2842.46,  746100
 Aug 25 2021, 2857.66, 2866.26, 2848.79, 2859.00, 2859.00,  641900
 Aug 24 2021, 2830.87, 2860.15, 2827.07, 2847.97, 2847.97,  756300
 (以降略)

```

このCSVファイルを読み込んで Date フィールドを抽出してみましょう。

```
 In [2]: # %load 06_dataframe.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('GOOG.csv')
    ...: ts = df['Date']
    ...: tss = pd.to_datetime(ts)
    ...: t1 = f'{tss[2].year}年{tss[2].month}月{tss[2].day}日'
    ...:
    ...: # print(df.head())
    ...: # print(ts.head())
    ...: # print(tss.head())
    ...: # print(t1)
    ...: # type(ts)
    ...:

 In [3]: print(df.head())
           Date     Open     High      Low    Close   Adj Close   Volume
 0  Aug 31 2021  2917.69  2922.24  2900.00  2909.24     2909.24  1337800
 1  Aug 30 2021  2894.09  2929.79  2892.00  2909.39     2909.39   845800
 2  Aug 27 2021  2842.25  2900.22  2840.40  2891.01     2891.01  1228100
 3  Aug 26 2021  2852.37  2862.70  2841.83  2842.46     2842.46   746100
 4  Aug 25 2021  2857.66  2866.26  2848.79  2859.00     2859.00   641900

 In [4]: print(ts.head())
 0    Aug 31 2021
 1    Aug 30 2021
 2    Aug 27 2021
 3    Aug 26 2021
 4    Aug 25 2021
 Name: Date, dtype: object

 In [5]: print(tss.head())
 0   2021-08-31
 1   2021-08-30
 2   2021-08-27
 3   2021-08-26
 4   2021-08-25
 Name: Date, dtype: datetime64[ns]

 In [6]: print(t1)
 2021年8月27日

 In [7]: type(ts)
 Out[7]: pandas.core.series.Series

```



 `to_datetime()` メソッドは文字列を読み取り NumPy の dateime64型、あるいは datetime の Timestamp 型のオブジェクトとして返します。

```
 In [2]: # %load 10_create_datetime.py
    ...: import pandas as pd
    ...:
    ...: now = pd.to_datetime('today')
    ...:
    ...: # print(now)
    ...:

 In [3]: print(now)
 2021-09-05 15:31:40.205029

```

```
 In [5]: # %load 11_localized_tz.py
    ...: pdt_tokyo = now.tz_localize('Asia/Tokyo')
    ...: pdt_london = pdt_tokyo.astimezone('Europe/London')
    ...:
    ...: # pdt_tokyo
    ...: # pdt_london
    ...:

 In [6]: pdt_tokyo
 Out[6]: Timestamp('2021-09-06 16:44:58.995500+0900', tz='Asia/Tokyo')

 In [7]: pdt_london
 Out[7]: Timestamp('2021-09-06 08:44:58.995500+0100', tz='Europe/London')

```


```
 In [9]: # %load 12_time_difference_bad.py
    ...: # this will occure TypeError
    ...: pdt_diff = pdt_tokyo - pdt_london
    ...:
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-9-4949cb46da6c> in <module>
       1 # %load 03_time_difference_bad.py
       2 # this will occure TypeError
 ----> 3 pdt_diff = pdt_tokyo - pdt_london

 ~/anaconda3/envs/py39/lib/python3.9/site-packages/pandas/_libs/tslibs/timestamps.pyx in pandas._libs.tslibs.timestamps._Timestamp.__sub__()

 TypeError: Timestamp subtraction must have the same timezones or no timezones

```

現在の日付と時刻（タイムゾーン情報なし）は、 `pd.to_datetime('today')` を使って生成され、`.tz_localize()`メソッドを使って `"Asia/Tokyo"` にローカライズされ、`pdt_tokyo` として保存されます。ロンドンの日時は、`astimezone('Euprope/London')`メソッドを使って生成されて、`pdt_london`として保存されます。ここで、両方の変数の出力に、UTCとの時差とタイムゾーン(TZ)が表示されていることに注目してください。Pandas の 日時処理では、Delorean とは異なり、タイムゾーンを認識する2つの変数の差を簡単に引く方法がないため、`TypeError`の例外が発生します。

```
 In [11]: # %load 13_time_difference_not_good.py
     ...: pdt_diff = pdt_tokyo.to_pydatetime() - pdt_london.to_pydatetime()
     ...:
     ...: # pdt_diff
     ...:

 In [12]: pdt_diff
 Out[12]: datetime.timedelta(0)

```

このエラーを軽減するために、 `.to_pydatetime()` メソッドを使ってpandasの表現をdatetimeオブジェクトに変換することができますが、この場合は時差はゼロになります。不思議に見えますが、重要なのことは2つの異なる地理的な場所で同じ時間を過ごしても、それぞれのローカル時間が違うだけでその時差はゼロになるということです。

2つのタイムゾーンの差を計算するには、 `.tz_localize(None)` を使って、タイムゾーンを意識した表現からタイムゾーンを意識しない表現に変換する必要があります。これは、8時間の差があります。

```
 In [14]: # %load 14_time_difference_good.py
     ...: pdt_diff = pdt_tokyo.tz_localize(None) - pdt_london.tz_localize(None)
     ...: diff_time = pdt_diff.total_seconds() / 3600
     ...:
     ...: # pdt_diff
     ...: # diff_time
     ...:

 In [15]: pdt_diff
 Out[15]: Timedelta('0 days 08:00:00')

 In [16]: diff_time
 Out[16]: 8.0

```

