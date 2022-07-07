演習1：いろいろなライブラリで日時処理をしてみよう
=================

次のデータは、ロンドンのヒースロー空港(LHR)と羽田空港(HND)を就航するANA [NH211 ](https://www.flightradar24.com/data/flights/nh211])便のフライト情報から抜き出した情報です。

 flight_data.py
```
 flight_data = {
     'departure' : ['2021-09-01 11:40', '2021-09-02 12:01', '2021-09-03 11:56'],
     'departure_tz' : ['Asia/Tokyo', 'Asia/Tokyo', 'Asia/Tokyo'],
     'arrival' : ['2021-09-01 15:33', '2021-09-02 15:58', '2021-09-03 15:45'],
     'arrival_tz' : ['Europe/London', 'Europe/London', 'Europe/London'],
 }

```


##  演習 1.1 フライト時間を求めてみよう

#### アドバイス
- Pandas の Series データを list型に変換するためには  `to_list()` メソッドを使用します。
- このデータの場合では、欠損値がないものとして処理して構いません。


### EX1: dateutils を使って求めてみましょう

### EX2: pendulum を使って求めてみましょう


### EX3: delorean を使って求めてみましょう


### EX4: Pandas を使って求めてみましょう

#### アドバイス
Pandas で DataFrame に読み込んで、depature と arraival の日時文字列を時刻に変換するスニペットを用意しています。

```
 In [2]: # %load snippet.py
    ...: import pandas as pd
    ...: from flight_data import flight_data
    ...:
    ...: df = pd.DataFrame(flight_data)
    ...:
    ...: df.loc[:, 'departure'] = pd.to_datetime(df.departure)
    ...: df.loc[:, 'arrival'] = pd.to_datetime(df.arrival)
    ...:

 In [3]: df
 Out[3]:
             departure departure_tz             arrival     arrival_tz
 0 2021-09-01 11:40:00   Asia/Tokyo 2021-09-01 15:33:00  Europe/London
 1 2021-09-02 12:01:00   Asia/Tokyo 2021-09-02 15:58:00  Europe/London
 2 2021-09-03 11:56:00   Asia/Tokyo 2021-09-03 15:45:00  Europe/London

```

これを修正して、フライト時間を  `actual_duration` カラムに格納’してみましょう。

