dateutilを使って日時処理をしてみよう
=================
## date-utilについて
dateutilモジュールは、Pythonで提供されている標準のdatetimeモジュールを強力に拡張します。
例えば、次のような日時関連の処理は出くわすことが多いのに、datetime だけでの実装はなかなか面倒なものです。

- 1ヶ月後の日付
- 次の月曜日の日付
- 今月の最終金曜日の日付
- ISO-8601形式の日付文字列との相互変換

`dateuti` は、こうした面倒な処理に対応することができるので、広く使われています。
dateutil は次のような機能があります。

- 相対的なデルタの計算（来月、来年、来週の月曜日、今月の最終週など）
- 2つの与えられた日付および/またはdatetimeオブジェクト間の相対的なデルタの計算
- iCalendar仕様のスーパーセットを使用した、非常に柔軟な再帰規則に基づく日付の計算。RFC文字列の解析もサポート
- ほぼすべての文字列形式での日付の汎用的な解析。
- さまざまなタイムゾーンの実装
  - tzfileフォーマットファイル ( `/etc/localtime, /usr/share/zoneinfo` など)
  - TZ 環境文字列 (すべての既知のフォーマット)
  - iCalendar フォーマットファイル
  - 与えられた範囲のローカルマシンのタイムゾーン
  - 固定オフセットのタイムゾーン
  - UTC タイムゾーン
  - Windows レジストリベースのタイムゾーンに対するタイムゾーン (tzinfo)
- Olsonのデータベースに基づく、内部の最新の世界のタイムゾーン情報。
- 西洋式、正教会式、ユリウス式のアルゴリズムによる、任意の年のイースターサンデーの日付の計算


## インストール
拡張モジュールなので次のようにインストールします。

 condaの場合
```
 $ conda install python-dateutil
```

 pipの場合
```
 # Linux or Mac
 $ python -m  pip install python-dateutil

 # Windwos
 $ py -3 -m pip install python-dateutil
```

## 相対デルタ（日時差分)の取得
 `dateutil` の `relativedelta()` と簡単に日時の差分(相対デルタ)を取得できます。

```
 relativedelta(datetime1, datetime2)
```

- `datetime1` , `datetime2` : DateTime オブジェクト
- `datetime1 - datetime2` の結果が返されます

例えば、2020年05月24が、エポックタイムから何日経過しているか調べてみましょう。
エポックタイムの起点は1970年01月01日 00:00:00 でしたよね。

```
 In [2]: # %load 02_relativedelta.py
    ...: from datetime import *
    ...: from dateutil.relativedelta import *
    ...:
    ...: dt = date(2020,5,24)
    ...: epoch = date(1970,1,1)
    ...: diff = relativedelta(dt, epoch)
    ...:
    ...: # dt
    ...: # epoch
    ...: # diff
    ...:

 In [3]: dt
 Out[3]: datetime.date(2020, 5, 24)

 In [4]: epoch
 Out[4]: datetime.date(1970, 1, 1)

 In [5]: diff
 Out[5]: relativedelta(years=+50, months=+4, days=+23)

```

2020年05月24日は、1970年01月01日から50年と4ヶ月と23日経過しているのがわかります。

## 絶対日時を置き換えた日時の取得
 `relativedelta()` のもうひとつの呼び出し方は、絶対日時をキーワード引数で与えるものです。このとき、キーワードは単数形であることに注意してください。
この呼び出し方をすると、当月の１日は何曜日か、といった基準で日時情報を取得できるようになります。

```
 relativedelta(year=x,month=y,hour=z...)
```
- 絶対日時をキーワード引数で与えます
 - year, month, day, hour, minute, second, microsecond
- 相対日時の計算せずに元の日時情報と置き換えます。

2020年の元旦は何曜日か？　その年の２月の月末は何曜日か？を求める場合は、次のようにします。

```
 In [2]: # %load 03_relativedelta_absolute.py
    ...: from datetime import *
    ...: from dateutil.relativedelta import *
    ...:
    ...: dt = date(2020,7,20)
    ...:
    ...: date1 = dt + relativedelta(month=1, day=1)
    ...: v1 = date1.weekday()
    ...: v2 = date1.strftime('%A')
    ...:
    ...: date2 = dt + relativedelta(month=2, day=31)
    ...: v3 = date2.weekday()
    ...: v4 = date2.strftime('%A')
    ...:
    ...: # date1
    ...: # v1
    ...: # v2
    ...: # date2
    ...: # v3
    ...: # v4
    ...:

 In [3]: date1
 Out[3]: datetime.date(2020, 1, 1)

 In [4]: v1
 Out[4]: 2

 In [5]: v2
 Out[5]: 'Wednesday'

 In [6]: date2
 Out[6]: datetime.date(2020, 2, 29)

 In [7]: v1
 Out[7]: 2

 In [8]: v2
 Out[8]: 'Wednesday'

```

閏年(Leap Year) の対応もキチンとできています。

## 相対デルタ(日時差)の取得
 `relativedelta()` の別の呼び出し方は、相対日時をキーワード引数で与えるものです。このとき、キーワードは複数形であることに注意してください。
この呼び出し方をすると、年、月、日などの基準で相対した日時の情報を取得できるようになります。

```
 relativedelta(years=x,months=y,hours=z...)
```

- 相対情報をキーワード引数で与えます
 - years, months, days, hours, minutes, seconds, microseconds
- 相対日時の計算した結果を返します。

```
 In [2]: # %load 04_relativedelta_relative.py
    ...: from datetime import *
    ...: from dateutil.relativedelta import *
    ...:
    ...: dt = date(2020,7,20)
    ...:
    ...: date1 = dt + relativedelta(months=+1)
    ...: date2 = dt + relativedelta(months=+1, weeks=+1)
    ...: date3 = dt + relativedelta(months=+1, weeks=+1, hours=+10)
    ...: date4 = dt + relativedelta(years=+1, months=+1)
    ...:
    ...:
    ...: # Bad usage: can you say what's wrong?
    ...: date5 = dt + relativedelta(year=1, month=1)
    ...:
    ...: # date1
    ...: # ...
    ...: # date5
    ...:

 In [3]: date1
 Out[3]: datetime.date(2020, 8, 20)

 In [4]: date2
 Out[4]: datetime.date(2020, 8, 27)

 In [5]: date3
 Out[5]: datetime.datetime(2020, 8, 27, 10, 0)

 In [6]: date4
 Out[6]: datetime.date(2021, 8, 20)

 In [7]: date5
 Out[7]: datetime.date(1, 1, 20)

```

## 次の該当曜日の日時
 `dateutil.relativedelta` には、曜日基準で相対デルタを計算するためのオブジェクトがあります。( `SU`, `FR` など）
 `relativedelta()` の`weekday=FR(-1)` のように曜日を指定することができます。
この呼び出し方をすると、指定した相対曜日の日時情報を取得することができます。
相対指定、絶対指定のいずれの呼び出し方にも使用することができます。

```
relativedelta(weekday=x)
```

- `weekday` : 曜日オブジェクトを与える
- 曜日の基準で相対させた日時情報が返されます。

 `FR` のように曜日オブジェクトに何も与えない場合は、単純に「次の金曜日」ということになります。同様に、`FR(2)` は次の次の金曜日（２週先の金曜日）、`FR(-1)` は直前の金曜日という意味です。また、`relativedelta()` の `weekday` には `calendar`モジュールの曜日オブジェクトも与えることができます。

例を見てみましょう。

```
 In [2]: # %load 05_relativedelta_weehday.py
    ...: from datetime import *
    ...: from dateutil.relativedelta import *
    ...: import calendar
    ...:
    ...: dt = date(2020,5,24)
    ...:
    ...: # 次の金曜日
    ...: date1 = dt + relativedelta(weekday=FR)
    ...:
    ...: # 次の次の金曜日
    ...: date2 = dt + relativedelta(weekday=FR(2))
    ...:
    ...: # 前の金曜日
    ...: date3 = dt + relativedelta(weekday=FR(-1))
    ...:
    ...: # 次の金曜日
    ...: date4 = dt + relativedelta(weekday=calendar.FRIDAY)
    ...:
    ...: # 今月の前の金曜日
    ...: date5 = dt + relativedelta(day=31, weekday=FR(-1))
    ...:
    ...: # 先月の直近の金曜日
    ...: date6 = dt + relativedelta(months=-1, day=31, weekday=FR(-1))
    ...:
    ...: # date1
    ...: # ...
    ...: # date6
    ...: # !cal -3 5 2020
    ...:

 In [3]: date1
 Out[3]: datetime.date(2020, 5, 29)

 In [4]: date2
 Out[4]: datetime.date(2020, 6, 5)

 In [5]: date3
 Out[5]: datetime.date(2020, 5, 22)

 In [6]: date4
 Out[6]: datetime.date(2020, 5, 29)

 In [7]: date5
 Out[7]: datetime.date(2020, 5, 29)

 In [8]: date6
 Out[8]: datetime.date(2020, 4, 24)

 In [9]: !cal -3 5 2020
                             2020
        April                  May                   June
 Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
           1  2  3  4                  1  2      1  2  3  4  5  6
  5  6  7  8  9 10 11   3  4  5  6  7  8  9   7  8  9 10 11 12 13
 12 13 14 15 16 17 18  10 11 12 13 14 15 16  14 15 16 17 18 19 20
 19 20 21 22 23 24 25  17 18 19 20 21 22 23  21 22 23 24 25 26 27
 26 27 28 29 30        24 25 26 27 28 29 30  28 29 30
                       31

```


## 年度内での経過日数の日時情報を取得

 `relativedelta()` の`yearday=256` のように1月1日からの経過日数を指示することができます。`yearday=1` を与えたときは、１月１日の情報が返されます。

```
 relativedelta(yearday=x)
```
- `yearday`: １月１日からの経過日数を与える（1 〜365、閏年では1〜366)
- 曜日の基準で相対させた日時情報が返されます。


```
 In [2]: # %load 06_relativedelta_yearday.py
    ...: from datetime import *
    ...: from dateutil.relativedelta import *
    ...:
    ...: # 2021年の256日目
    ...: date1 = date(2021, 1, 1) + relativedelta(yearday=256)
    ...:
    ...: # 2020年の256日目
    ...: date2 = date(2020, 1, 1) + relativedelta(yearday=256)
    ...:
    ...: # date1
    ...: # date2
    ...:

 In [3]: date1
 Out[3]: datetime.date(2021, 9, 13)

 In [4]: date2
 Out[4]: datetime.date(2020, 9, 12)

```

きちんと閏年の処理ができています。

### 日時文字列の変換
 `relativedelta()` に与える日付情報は`DateTime`型を与えます。ここで困ったことに、日付の文字列には国別など慣例的に多くのスタイルがあります。
例えば次のようなものがあります。（あくまで一例です)

- 2020/01/31
- 2020-01-31
- 31-01-2020
- 31-Jan-2020

こうした違いがあるため[ISO-8601](https://ja.wikipedia.org/wiki/ISO_8601])という国際規格が定義されています。

ISO-8601に従った日時文字列は次のようなものです。
- UTC時刻: 末尾にZが付加される    `2020-03-04T19:00Z`
- UTC以外の日時：UTCとの時刻差を付加      `2020-03-04T10:00+09:00`

 `dateutil.parser` を使用すると、ISO-8601日時文字列を含め、多数ある規格外の日時情報の文字列もうまく`DateTime`型に変換してくれます。

```
 In [2]: # %load 07_dateutil_parse.py
    ...: from datetime import datetime
    ...: import dateutil.parser
    ...:
    ...: dt = datetime(2020, 3, 4, 0, 0)
    ...:
    ...: # assert は与えた式が真のときは何も表示しない
    ...:
    ...: dt1 = dateutil.parser.parse('2020/03/04')
    ...: assert dt == dt1
    ...:
    ...: dt2 = dateutil.parser.parse('2020-03-04')
    ...: assert dt == dt2
    ...:
    ...: dt3 = dateutil.parser.parse('2020/Mar/04')
    ...: assert dt == dt3
    ...:
    ...: dt4 = dateutil.parser.parse('2020-March-04')
    ...: assert dt == dt4
    ...:
    ...: dt5 = dateutil.parser.parse('04-Mar-2020')
    ...: assert dt == dt5
    ...:
    ...: dt6 = dateutil.parser.parse('04-March-2020')
    ...: assert dt == dt6
    ...:
    ...: dt7 = dateutil.parser.parse('04-Mar-20')
    ...: assert dt == dt7
    ...:
    ...: dt8 = dateutil.parser.parse('04-March-20')
    ...: assert dt == dt8
    ...:

```

しかし、  `04/05/06` (`04-05-06`) のような場合は、`年/月/日`や `月/日/年`、 `日/月/年` の区別がつきません。
これを区別させるために、 `yearfirst` や`dayfirst` のフラグを指示できます。
 `date-util` のデフォルトでは `月/日/年` が優先変換になります。

 dateutil での形式優先度

| yearfirst | dayfirst | 形式優先度 |
|:--|:--|:--|
| False | False | 月/日/年　＞　日/月/年　＞　年/月/日 |
| True | False | 年/月/日　＞　月/日/年　＞　日/月/年 |
| False | True | 日/月/年　＞　月/日/年　＞　年/月/日 |
| True | True | 年/月/日　＞　日/月/年　＞　月/日/年 |


## rrule
rruleは、iCalendar RFCに記載されている再帰規則を、完全かつ軽量に、そして非常に高速に実装したもので、結果のキャッシュもサポートしています。

```
 In [2]: # %load 30_rrule.py
    ...: from dateutil.rrule import rrule, MONTHLY
    ...: from datetime import datetime
    ...:
    ...: start_date = datetime(2020, 5, 24, 8, 20)
    ...: period = list(rrule(freq=MONTHLY, count=4, dtstart=start_date))
    ...:
    ...: for dt in period:
    ...:     print(dt)
    ...:
 2020-05-24 08:20:00
 2020-06-24 08:20:00
 2020-07-24 08:20:00
 2020-08-24 08:20:00

```




## 参考
- [dateutil ドキュメント](https://dateutil.readthedocs.io/en/stable/index.html])
- [dateutil ソースコード](https://github.com/dateutil/dateutil])
