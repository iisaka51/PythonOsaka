PythonでGoogleTrendsのデータを取得してみよう
=================
![](https://gyazo.com/64bc8e6765529236aec0b615d41fbf6a.png)

## pytrends について
[Google Trends ](https://trends.google.com/) は、Google Searchでの検索クエリのトレンドを分析するサービスです。

pytrends は、この Google Trends にアクセスしてデータを抽出するためのPython で実装された拡張ライブラリです。Pytrendsを使用することで、Google Trendsで利用可能なほぼすべてのデータを抽出することができます。

この資料作成時点では、pytrends のバージョンは4.8.0 で、以下のAPIメソッドが提供されています。

  -  `interest_over_time()` `: Google Trends の Interest Over Time セクションに示されているように、キーワードが最も検索された時間帯の履歴データをインデックス付きで返します。
  -  `get_historical_interest()` `: Google TrendsのInterest Over Timeセクションに表示されている、キーワードが最も検索された時間ごとの履歴データを、インデックス付きで返します。Googleに複数回リクエストを送信し、それぞれ1週間分のデータを取得する。1時間ごとのデータを取得するには、この方法しかないように思われる。
  -  `interest_by_region()` ：Google TrendsのInterest by Regionにあるように、そのキーワードが最も検索されている地域のデータを返します。
  -  `related_topics()` : Google TrendsのRelated Topicsに表示されている、指定したキーワードに関連するキーワードのデータを返します。
  -  `related_queries()` ：Google Trendsの「関連クエリ」に表示されている、提供されたキーワードに関連するキーワードのデータを返す。
  -  `trending_searches()` : Google TrendsのTrending Searchesに表示されている最新のトレンド検索のデータを返す。
  -  `top_charts()` : Google TrendsのTop Chartsセクションに表示されている、指定したトピックのデータを返します。



## インストール

まず、次のようにインストールしておきます。


 bash
```
 # Linux or MacOS
 $ python -m pip install pytrends seaborn IPython
 #
 # Windows
 $ py -3 -m pip install pytrends seaborn IPython

```


## 使用方法

はじめに、pytrendsをインポートしておきます。


```
 In [2]: # %load c01_initialize.py
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...: seaborn.set_style("darkgrid")
    ...:

 In [3]:

```

この例では、IPython は例示のために利用しています。seaborn も可視化のために使用していますが、単純な設定を行っているだけです。pytrends を使うことについての依存性があるわけではありません。


次に  `TrendReq` クラスのインスタンスオブジェクトを作成します。


```
 In [4]: # %load c02_create_instance.py
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:

 In [5]:

```


キーワード引数  `hl` はGoogle Trendsにアクセスするための言語指定(Host Languagues)>、 `tz` はタイムゾーンオフセットで、UTCからの時差を分で表現した数値を与えます。日本標準時（JST)の場合は  `tz=540` です。
ここに例示した値がデフォルト値になっていま>す。

その他にも、リクエストに失敗した場合の再試行回数を示すretriesや、タイムアウト時>間を指定する timeout などを渡すことができます。

次にペイロード(payload) を作成します。このペイロードとは、Google Trends で調べようとする検索キーワードから作られるものです。



```
 In [6]: # %load c03_build_payload.py
    ...: kw_list = ["Python", "Java"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:

 In [7]:
```

 `interest_over_time()` メソッドを使用して、キーワードに対する検索回数をデータフレームとして取得することができます。



```
 In [8]: # %load c04_interrest_over_time.py
    ...: iot = pt.interest_over_time()
    ...:
    ...: # iot
    ...:

 In [9]: iot
 Out[9]:
             Python  Java  isPartial
 date
 2004-01-01       7    94      False
 2004-02-01       7    97      False
 2004-03-01       7   100      False
 2004-04-01       7    92      False
 2004-05-01       6    92      False
 ...            ...   ...        ...
 2021-11-01      18    13      False
 2021-12-01      17    14      False
 2022-01-01      17    13      False
 2022-02-01      19    14      False
 2022-03-01      19    14       True

 [219 rows x 3 columns]

 In [10]:

```



値の範囲は0（ほとんど検索されない）から100（最大検索可能数）になっています。

 `build_payload()` メソッドは、キーワードリスト以外にいくつかのパラメータを受け取
ります。

  -  `cat` : カテゴリ ID を指定します。検索クエリが複数の意味を持つ場合、カテゴリを設
定することで混乱を取り除くことができます。カテゴリIDのリストはこのページで確認す
るか、単純に  `.categories()` メソッドを呼び出して取得することができます。
  -  `geo` : US、FR、ES、DZなど、特定の国の検索を取得するための2文字の国の略語を与え>ます。
  -  `timeframe` 。抽出したいデータの時間範囲を与えます。'all' は Google で公開されて
  - いる初期からのすべてのデータを意味し、特定の日付や、'today 6-m' は最新の6ヶ月分>のデータ、'today 3-d' は最新の3日分のデータ、というようにマイナスパターンを渡す>ことができる。デフォルト値は'today 5-y'で、これは過去5年分のデータを意味しています。


検索キーワード  `Python` と  `Java` の相対的な差を時系列でプロットしてみましょう。
 `%matplotlib` としているのは、プロットを表示させるためのIPython のマジックコマンドです。


```
 In [12]: %matplotlib
 Using matplotlib backend: MacOSX

 In [13]: # %load c05_plot.py
     ...: iot.plot(figsize=(10,6))
     ...:
 Out[13]: <AxesSubplot:xlabel='date'>

 In [14]:

```

![](https://gyazo.com/d3b6d7ee8f7e82fa8687786ee6972b47.png)



 `get_historical_interest()` メソッドを使用すると、指定した開始と終了で日時で1時間ごとに集計されたデータを取得することもできます。当然のことですが、このメソッドは短期間でのデータは、長期的なトレンドの傾向を示すものではないことに留意してください。


```
 In [2]: # %load c07_get_historial_interest.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:
    ...: kw_list = ["Python", "Java"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:
    ...: data = pt.get_historical_interest( kw_list,
    ...:              year_start=2022, month_start=2, day_start=1, hour_start=0,
    ...:              year_end=2022, month_end=2, day_end=28, hour_end=23,
    ...:          )
    ...:
    ...: # %matplotlib
    ...: # data.plot(figsize=(10,6))
    ...:

 In [3]: %matplotlib
 Using matplotlib backend: MacOSX

 In [4]: data.plot(figsize=(10,6))
 Out[4]: <AxesSubplot:xlabel='date'>

 In [5]: data
 Out[5]:
                      Python  Java  isPartial
 date
 2022-02-01 00:00:00      60    44      False
 2022-02-01 01:00:00      55    36      False
 2022-02-01 02:00:00      63    46      False
 2022-02-01 03:00:00      76    44      False
 2022-02-01 04:00:00      78    57      False
 ...                     ...   ...        ...
 2022-02-28 19:00:00      60    44      False
 2022-02-28 20:00:00      61    39      False
 2022-02-28 21:00:00      61    41      False
 2022-02-28 22:00:00      65    42      False
 2022-02-28 23:00:00      60    37      False

 [675 rows x 3 columns]

 In [6]:
```



![](https://gyazo.com/4ff44609cd6821bccbf80a16758f214b.png)
今回、先頭部分で　次の2行が追加されています。


```
 import warnings
 warnings.simplefilter(action='ignore', category=FutureWarning)
```

これは、DataFrameオブジェクトの `append()` のメソッドを　pytrends が使用しているため、Pandas で出力される次の `FutureWaring` メッセージを出力させないようにするためのものです。



```
 site-packages/pytrends/request.py:589: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
   df = df.append(week_df)
```


 `get_historical_interest()` メソッドは、長期間の時間枠を指定するとデータが膨大になってしまうことに注意してください。場合によってはGoogleにIPブロックされる可能性があります。

## 地域別関心度を取得
特定のキーワードの地域別関心度を取得してみましょう。


```
 In [2]: # %load c08_interest_by_region.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:
    ...: kw_list = ["Python", "Java"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:
    ...: data = pt.interest_by_region( "COUNTRY",
    ...:          inc_low_vol=False, inc_geo_code=True
    ...:          )
    ...:
    ...: # data
    ...: # data.filter(items=['Japan', 'United States'], axis='index')
    ...:

 In [3]: data
 Out[3]:
                geoCode  Python  Java
 geoName
 Afghanistan         AF       0     0
 Albania             AL       0     0
 Algeria             DZ       0     0
 American Samoa      AS       0     0
 Andorra             AD       0     0
 ...                ...     ...   ...
 Western Sahara      EH       0     0
 Yemen               YE       0     0
 Zambia              ZM       0     0
 Zimbabwe            ZW       0     0
 Åland Islands       AX       0     0

 [250 rows x 3 columns]

 In [4]: data.filter(items=['Japan', 'United States'], axis='index')
 Out[4]:
               geoCode  Python  Java
 geoName
 Japan              JP      33    67
 United States      US      42    58

 In [5]:
```



 `interest_by_region()` メソッドに  `"COUNTRY"` を渡して、国別の関心度を取得しています。他の値として、都市レベルのデータには  `'CITY'` 、メトロレベルのデータには  `'DMA'` 、地域レベルのデータには  `'REGION'` を指定することができます。

 `inc_low_vol=True` を与えると、検索ボリュームの少ない国のデータも含めるようになります。 `inc_geo_code=True` を与えると、各国のジオコードを含めることができます。

検索キーワードとしての関心度では、日本は米国に比べて Python の関心度が低いいことが見て取れます。

検索キーワード Python で関心度で国別にソートしてみましょう。
要素の値に応じてソートするにはDataFrameオブジェクトの `sort_values()` メソッドを使います。


```
 In [2]: # %load c09_sort_values.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:
    ...: kw_list = ["Python", "Java"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:
    ...: data = pt.interest_by_region( "COUNTRY",
    ...:          inc_low_vol=False, inc_geo_code=True
    ...:          )
    ...:
    ...: # data[kw_list].sort_values('Python', ascending=False).head(10)
    ...:
    ...: # %matplotlib
    ...: # data[kw_list].sort_values('Python', ascending=False).head(10).plot.bar
    ...: ()
    ...:
    ...: # data[kw_list].sort_values('Java', ascending=False).head(10)
    ...:

 In [3]: data[kw_list].sort_values('Python', ascending=False).head(10)
 Out[3]:
                 Python  Java
 geoName
 Israel              49    51
 Taiwan              46    54
 Australia           46    54
 South Korea         45    55
 United Kingdom      45    55
 Russia              43    57
 New Zealand         43    57
 Singapore           42    58
 Canada              42    58
 United States       42    58

 In [4]: %matplotlib
 Using matplotlib backend: MacOSX

 In [5]: data[kw_list].sort_values('Python', ascending=False).head(10).plot.bar()
    ...:
 Out[5]: <AxesSubplot:xlabel='geoName'>

 In [6]:
```

 `sort_values()` メソッドの第一引数(キーワードで与えるときは  `by` ) にソートをする列のラベルを与えます。


![](https://gyazo.com/93f5cb691dfc4f32ba97ea7057b33dda.png)


ちなみに、Java でソートすると次のような結果になります。


```
 In [6]: data[kw_list].sort_values('Java', ascending=False).head(10)
 Out[6]:
              Python  Java
 geoName
 Indonesia         9    91
 Bangladesh       11    89
 Mexico           13    87
 Peru             14    86
 Nigeria          15    85
 Sri Lanka        16    84
 Turkey           16    84
 Brazil           16    84
 Vietnam          17    83
 Philippines      18    82

 In [7]:
```


Python をキーとしてソートしたときでは科学立国として知られる国が並ぶのに対して、Java をキーとしてでソートするとオフショア開発を受託している国々が並ぶのも興味深いですね。



## 関連トピックとクエリ

Googleトレンドは、**クエリ(queries)** と **トピックス(topics)** に分類されています。

  - クエリ　ー 　検索クエリそのもの
  - トピックス ー 　分類済みの話題

これらがさらに、**人気**(top) と **注目(rising)** に分類されます。

  - 人気　ー　検索ボリュームが多いもの
  - 注目 ー は検索ボリュームの上昇率が高いもの

関数を使い方は次のようになります。

キーワード + 人気

```
 d = pytrends.related_queries()
 result = df["keyword"]["top"]
```

キーワード + 注目

```
 d = pytrends.related_queries()1
 result = df["keyword"]["rising"]
```

トピック + 人気

```
 df = pytrends.related_topics()
 result = =df["keyword"]["top"]
```

トピック + 注目

```
 d = pytrends.related_topics()
 result = =df["keyword"]["rising"]
```

実際に呼び出しは次のようになります。



```
 In [2]: # %load c10_related_topics.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:
    ...: kw_list = ["Python"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:
    ...: data = pt.related_topics()
    ...:
    ...: # type(data)
    ...: # data
    ...:
 In [3]: type(data)
  Out[3]: dict

```

この場合、ペイロードの作成時に複数の検索キーワードを与えていると、うまく処理できません。また、辞書オブジェクトが返されることに注意してください。



```
 In [4]: data['Python']['top']
 Out[4]:
     value formattedValue  ...           topic_title            topic_type
 0     100            100  ...                Python  Programming language
 1       9              9  ...                  List    Abstract data type
 2       8              8  ...                String      Computer science
 3       8              8  ...         Computer file                 Topic
 4       6              6  ...               Pythons                 Snake
 5       4              4  ...     Associative array                 Topic
 6       4              4  ...          Monty Python         Comedy troupe
 7       4              4  ...                  Data                 Topic
 8       4              4  ...              Function           Mathematics
 9       3              3  ...          Installation     Computer programs
 10      3              3  ...  Array data structure                 Topic
 11      3              3  ...           Ball python              Reptiles
 12      3              3  ...              Tutorial                 Topic
 13      2              2  ...                pandas              Software
 14      2              2  ...              Variable      Computer science
 15      2              2  ...    Scripting language                 Topic
 16      2              2  ...  Computer programming                 Topic
 17      2              2  ...                 Class  Computer programming
 18      2              2  ...                Object      Computer science
 19      2              2  ...               Command             Computing
 20      2              2  ...                 NumPy              Software
 21      2              2  ...             Directory             Computing
 22      2              2  ...                  JSON           File format
 23      2              2  ...                 Linux      Operating system
 24      2              2  ...              Printing       Visual art form

 [25 rows x 7 columns]

 In [5]:
```

同様に、 `related_queries()` メソッドを使用すると検索クエリを抽出することができます。



```
 In [2]: # %load c11_related_queries.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:
    ...: kw_list = ["Python"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:
    ...: data = pt.related_queries()
    ...:
    ...: # type(data)
    ...: # data['Python']['top']
    ...:

 In [3]: type(data)
 Out[3]: dict

 In [4]: data['Python']['top']
 Out[4]:
                 query  value
 0          python for    100
 1         python list     92
 2       python string     73
 3         python with     63
 4        monty python     52
 5           python if     39
 6      install python     39
 7         python code     38
 8     python function     35
 9      python windows     32
 10       python array     29
 11    python download     29
 12       python print     28
 13  python dictionary     26
 14        ball python     26
 15             pandas     26
 16      pandas python     25
 17    python tutorial     25
 18        python loop     23
 19     what is python     23
 20       python class     22
 21      python script     22
 22         python set     21
 23      python import     21
 24      online python     21

 In [5]:
```


 `suggestions()` メソッドを使用すると｀keyword`引数に与えた検索キーワードに対する検索クエリの候補がリストで返されます。


```
 In [2]: # %load c12_suggestions.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...:
    ...: kw_list = ["Python"]
    ...: pt.build_payload(kw_list, timeframe="all")
    ...:
    ...: data = pt.suggestions("python")
    ...:
    ...: # type(data)
    ...: # data
    ...:

 In [3]: type(data)
 Out[3]: list

 In [4]: data
 Out[4]:
 [{'mid': '/m/05z1_', 'title': 'Python', 'type': 'Programming language'},
  {'mid': '/m/05tb5', 'title': 'Python family', 'type': 'Snake'},
  {'mid': '/m/0cv6_m', 'title': 'Pythons', 'type': 'Snake'},
  {'mid': '/m/02_2hl', 'title': 'Python', 'type': 'Film'},
  {'mid': '/m/02rg562', 'title': 'Python', 'type': 'Efteling'}]

 In [5]:

```


## トレンド検索
Google Trends の特徴のひとつには、各地域の現在のトレンド検索を抽出する機能があります。


```
 In [2]: # %load c13_trendinng_search.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...: data = pt.trending_searches(pn='japan')
    ...:
    ...: # type(data)
    ...: # data[:10]
    ...:

 In [3]: type(data)
 Out[3]: pandas.core.frame.DataFrame

 In [4]: data[:10]
 Out[4]:
             0
 0    ドライブマイカー
 1        日経平均
 2        井上咲楽
 3      ウィルスミス
 4  ボヘミアンラプソディ
 5        噴火浅根
 6      SOPHIA
 7       高松宮記念
 8   ヴィーナスフォート
 9      パンサラッサ

 In [5]:
```

ちなみに米国での関心事はこんな具合です。


```
 In [5]: usa = pt.trending_searches(pn='united_states')

 In [6]: usa[:10]
 Out[6]:
                     0
 0          Will Smith
 1         Oscars 2022
 2                CODA
 3       USA vs Panama
 4       Ariana DeBose
 5         Regina Hall
 6       Billie Eilish
 7       Jesse Plemons
 8           Al Pacino
 9  Honduras vs Mexico

 In [7]:
```

 `realtime_trending_searches()` メソッドを使うと今最新の検索トレンドを取得することができます。



```
 In [2]: # %load c14_realtime_trendinng_search.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...: data = pt.realtime_trending_searches(pn='JP')
    ...:
    ...: # data[:10]
    ...:

 In [3]: data[:10]
 Out[3]:
                                                title                                        entityNames
 0  Will Smith, Academy Awards, Academy Award for ...  [Will Smith, Academy Awards, Academy Award for...
 1  Remi Hirano, Tetsuko Kuroyanagi, Makoto Wada, ...  [Remi Hirano, Tetsuko Kuroyanagi, Makoto Wada,...
 2                 Omega SA, Swatch, Shosuke Tanihara               [Omega SA, Swatch, Shosuke Tanihara]
 3  Academy Awards, Academy Award for Best Directi...  [Academy Awards, Academy Award for Best Direct...
 4  Kristen Stewart, Academy Awards, Jessica Chastain  [Kristen Stewart, Academy Awards, Jessica Chas...
 5  Meihan National Highway, Gokadani Interchange,...  [Meihan National Highway, Gokadani Interchange...
 6  Academy Awards, Volodymyr Zelenskyy, Sean Penn...  [Academy Awards, Volodymyr Zelenskyy, Sean Pen...
 7  BIGBANG, G-Dragon, Taeyang, Daesung, YG Entert...  [BIGBANG, G-Dragon, Taeyang, Daesung, YG Enter...
 8                                   Fuji TV, Viking!                                 [Fuji TV, Viking!]
 9  Asadora, Ryoko Moriyama, Rina Kawaei, Louis Ar...  [Asadora, Ryoko Moriyama, Rina Kawaei, Louis A...

 In [4]:

```


## top_charts - Year in Search: 検索で振り返る
 `top_charts()` メソッドを使用すると、数値で指定した年の検索キーワードを取得することができます。現在の年と同じ数値の場合は何も返さないので注意してください。



```
 In [2]: # %load c15_top_charts.py
    ...: import warnings
    ...: warnings.simplefilter(action='ignore', category=FutureWarning)
    ...: from pytrends.request import TrendReq
    ...: import seaborn
    ...:
    ...: seaborn.set_style("darkgrid")
    ...:
    ...: pt = TrendReq(hl='en-US', tz=360)
    ...: data = pt.top_charts(2021,geo='JP')
    ...:
    ...: # data[:10]
    ...:

 In [3]: data[:10]
 Out[3]:
            title exploreQuery
 0   東京2020オリンピック       オリンピック
 1           大谷翔平        大谷 翔平
 2     東京リベンジャー ズ
 3   モンスターハンターライズ     モンハン ライズ
 4           呪術廻戦       呪術 廻 戦
 5  ウマ娘 プリティーダービー         ウマ 娘
 6  新型コロナウイルスワクチン     コロナ ワクチン
 7           小松菜奈        小松菜 奈
 8           夏目三久       夏目 三 久
 9          小山田圭吾       小山田 圭吾

 In [4]:
```

## まとめ
pytrends を使用すると簡単に Google Trands へアクセスして結果を得ることができます。IPythonやJupyterlab の環境と合わせて使用するとブラウザで処理するより速く目的を達することができるようになるでしょう。


## 参考
- pytrends
  - [PyPI - pytrends ](https://pypi.org/project/pytrends/)
  - [ソースコード ](https://github.com/GeneralMills/pytrends)
- [GeoNames.org ](https://www.geonames.org/)
- [Wikipedia - UTC Offset - ](https://en.wikipedia.org/wiki/UTC_offset)
- [Wikipedia -日本標準時  ](https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E6%A8%99%E6%BA%96%E6%99%82)

