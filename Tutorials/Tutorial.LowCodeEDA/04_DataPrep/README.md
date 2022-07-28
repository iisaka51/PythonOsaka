DataPrepで探査的データ分析をしてみよう
=================
![](https://gyazo.com/d7a8e07643b2b549cea8c9f36f726680.png)
# DataPrep について
DataPrepは、データを準備(prepare)するために開発されたPythonパッケージです。このパッケージには、主に以下の3つのAPIが含まれています。

  - データ探索( dataprep.eda )
  - データクリーニング( dataprep.clean )
  - データ収集( dataprep.connector )

DataPrepパッケージは、高速にデータ探索を行うことができるように設計されていて、PandasやDaskのDataFrameオブジェクトとうまく連携して動作します。


## インストール
dataprep  は次のようにインストールします。

 bash
```
 $ python -m pip install dataprep
```

macOS の場合は、pip でインストールすると SciPy をビルドしようとして失敗します。[MacでPython実行環境を整えるベストプラクティス ](https://www.notion.so/Mac-Python-116e3ee2718f4f77b40901104d53d318) を参考に Anaconda Python を利用するようにしてください。



## 学習用データセット
DataPrep には学習用のデータセットが内包されています。ヘルパー関数  `load_dataset()` にデータセット名を与えるとDataFrameで返してくれます。データセットのリストを得るためには、 `get_dataset_names()` を呼び出します。


```
 In [2]: # %load c00_datasets.py
    ...: from dataprep.datasets import get_dataset_names
    ...:
    ...: get_dataset_names()
    ...:
 Out[2]:
 ['house_prices_test',
  'adult',
  'countries',
  'patient_info',
  'waste_hauler',
  'iris',
  'titanic',
  'house_prices_train',
  'covid19',
  'wine-quality-red']
 
 In [3]:
 
```

たとえば、Kaggleの[Titanic Machine Learning from Disaster ](https://www.kaggle.com/c/titanic) のデータセットを使用する場合は、次のようになります。


```
 In [2]: # %load c01_titanic.py
    ...: from dataprep.datasets import load_dataset
    ...: from dataprep.eda import create_report
    ...:
    ...: df = load_dataset("titanic")
    ...: df.head()
    ...: df.to_save('titanic.csv')
    ...:
 Out[2]:
    PassengerId  Survived  Pclass  ...     Fare Cabin  Embarked
 0            1         0       3  ...   7.2500   NaN         S
 1            2         1       1  ...  71.2833   C85         C
 2            3         1       3  ...   7.9250   NaN         S
 3            4         1       1  ...  53.1000  C123         S
 4            5         0       3  ...   8.0500   NaN         S
 
 [5 rows x 12 columns]
 
 In [3]:
```

このデータセットは次の属性で構成されています。

  - pclass： 旅客クラス（1＝1等、2＝2等、3＝3等）。裕福さの目安となる
  - name： 乗客の名前
  - sex： 性別（male＝男性、female＝女性）
  - age： 年齢。一部の乳児は小数値
  - sibsp： タイタニック号に同乗している兄弟（Siblings）や配偶者（Spouses）の数
  - parch： タイタニック号に同乗している親（Parents）や子供（Children）の数
  - ticket： チケット番号
  - fare： 旅客運賃
  - cabin： 客室番号
  - embarked： 出港地（C＝Cherbourg、Q＝Queenstown、S＝Southampton）
  - boat： 救命ボート番号
  - body： 遺体収容時の識別番号
  - home.dest： 自宅または目的地
  - survived：生存状況（0＝死亡、1＝生存）。通常はこの数値が目的変数として使われる


## DataPrep によるデータ探査
DataPrepは、1行のコードでインタラクティブなプロファイルレポートを作成することができます。
このレポートオブジェクトは、ノートブックから分離されたHTMLオブジェクトなので、様々な探索の選択肢があることになります。



```
 create_report(df).show_browser()
```

デフォルトのブラウザが開き各種の分析結果をプロットと共にがインタラクティブレポートが表示されます。
[DataPrep での分析サンプル　](https://docs.dataprep.ai/_downloads/1a61c6aebb3ecbe9dc9742bd6ca78ddb/titanic_dp.html)

![](https://gyazo.com/cdfac825959f4a65b8dbba81b7607a40.png)
[# Overview] タブからは、我々のデータセットからすべての概要情報を見ることができます。ここから知ることのできる情報には、欠損データ数およびパーセンテージ、重複データ、変数データ・タイプ、各変数の詳細情報などです。

![](https://gyazo.com/8d810501016e0b5e303fcd42ad4d29c4.png)

[# Variables] タブは、データセット内の各変数の詳細な情報を知ることができます。これには、ユニーク、欠損データ、分位数、統計量の概要、分布、正規性など、必要な情報はほとんどすべて利用可能です。


![](https://gyazo.com/d9efa377f58ea7a6fb7a248fa3db6bc9.png)
[# Interactions] タブは、2つの数値変数から散布図を作成してくれます。X軸とY軸を自分で設定できるので、どのように可視化するかをコントロールすることができます。

![](https://gyazo.com/765d112298c7e6710fb16612448379a0.png)
[# Correlations] タブは、数値間の統計的相関関係をヒートマップにプロットしてくれます。今のバージョンでは、Pearson、Spearman、KendallTauの3つの相関計算を行うことができます。

![](https://gyazo.com/d14d5a576da6c541270b042d6f483d6d.png)

[# Missing Values] タブは、欠損値に関するすべての詳細情報を知ることができます。欠損値情報を完全に調査するために、棒グラフ（Bar Chart)、スペクトラム(Spectrum)、ヒートマップ(Heat Map)、デンドログラム（Dendorogram) からプロット種別を選択することができます。


## DataPrep によるクリーニング
DataPrep にはDataFrameのクリーニングとバリデーションを行うためのAPIが提供されています。例えば、以下のようなAPIがあります。

  - [Column Headers ](https://docs.dataprep.ai/user_guide/clean/clean_headers.html)
  - [Country Names ](https://docs.dataprep.ai/user_guide/clean/clean_country.html)
  - [DataTime ](https://docs.dataprep.ai/user_guide/clean/clean_date.html)
  - [Duplicate Values ](https://docs.dataprep.ai/user_guide/clean/clean_duplication.html)
  - [Email Address ](https://docs.dataprep.ai/user_guide/clean/clean_email.html)

APIは140以上あるためこの資料で全てを取り上げることができませんが、詳細は[公式ドキュメント　](https://docs.dataprep.ai/index.html) を参照してください。

先ほどの Titanic データセットを使ってクリーニングAPIの Columns  Headers を試してみましょう。


```
 In [2]: # %load c02_cleaning_columnheaders.py
    ...: from dataprep.datasets import load_dataset
    ...: from dataprep.clean import clean_headers
    ...:
    ...: df = load_dataset("titanic")
    ...:
    ...: df.columns
    ...: clean_headers(df, case = 'const').columns
    ...: clean_headers(df, case = 'camel').columns
    ...:
 Out[2]:
 Index(['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
        'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'],
       dtype='object')
 Column Headers Cleaning Report:
 	12 values cleaned (100.0%)
 Out[2]:
 Index(['PASSENGER_ID', 'SURVIVED', 'PCLASS', 'NAME', 'SEX', 'AGE', 'SIB_SP',
        'PARCH', 'TICKET', 'FARE', 'CABIN', 'EMBARKED'],
       dtype='object')
 Column Headers Cleaning Report:
 	12 values cleaned (100.0%)
 Out[2]:
 Index(['passengerId', 'survived', 'pclass', 'name', 'sex', 'age', 'sibSp',
        'parch', 'ticket', 'fare', 'cabin', 'embarked'],
       dtype='object')
 
 In [3]:
 
```

 `clean_headers()` に  `case=const` を与えるとカラム名(カラムヘッダ）が大文字になり、アンダーライン( `_` )で単語の区切られます。また、 `case=camel` を与えるとカラム名は小文字になり、複数の単語でが含まれる場合は単語の頭を大文字でっくぐるようになります。

もし、完全にクリーニングされたDataFrameが欲しいときは、DataPrepの  `clean_df()` を利用することができます。このAPIは、推論されたデータ型とクリーニングされたDataFrameを返します。


```
 In [2]: # %load c03_cleaning_df.py
    ...: from dataprep.datasets import load_dataset
    ...: from dataprep.clean import clean_df
    ...:
    ...: df = load_dataset("titanic")
    ...: inferred_dtypes, cleaned_df = clean_df(df)
    ...:
 Data Type Detection Report:
 	These data types are supported by DataPrep to clean: []
 Column Headers Cleaning Report:
 	12 values cleaned (100.0%)
 Downcast Memory Report:
 	Memory reducted from 334337 to 296915. New size: (88.81%)
 
 In [3]: inferred_dtypes
 Out[3]:
             semantic_data_type atomic_data_type
 PassengerId            integer          integer
 Survived               integer          integer
 Pclass                 integer          integer
 Name                    string           string
 Sex                     string           string
 Age                   floating         floating
 SibSp                  integer          integer
 Parch                  integer          integer
 Ticket                  string           string
 Fare                  floating         floating
 Cabin                   string           string
 Embarked                string           string
 
 In [4]: cleaned_df
 Out[4]:
      passenger_id  survived  pclass  ...       fare cabin  embarked
 0               1         0       3  ...       7.25  <NA>         S
 1               2         1       1  ...  71.283302   C85         C
 2               3         1       3  ...      7.925  <NA>         S
 3               4         1       1  ...  53.099998  C123         S
 4               5         0       3  ...       8.05  <NA>         S
 ..            ...       ...     ...  ...        ...   ...       ...
 886           887         0       2  ...       13.0  <NA>         S
 887           888         1       1  ...       30.0   B42         S
 888           889         0       3  ...  23.450001  <NA>         S
 889           890         1       1  ...       30.0  C148         C
 890           891         0       3  ...       7.75  <NA>         Q
 
 [891 rows x 12 columns]
 
 In [5]:
 
```

DataPrepのクリーニングAPIには、その数だけでなく受け入れる パラメータもたくさんあります。詳細は[公式ドキュメント　](https://docs.dataprep.ai/index.html) を参照してください。

## DataPrepによるデータ収集
DataPrep のCollection APIは、データベースやWeb APIからデータを収集するためのAPIです。MySQLやPostgreSQLなどのデータベースにアクセスできるのであれば、DataPrep APIで接続できますが、DataPrep connect APIを使ってアクセスすることも可能です。
### データベースへのアクセス
Postgres、Mysql, SQLServerなどのデータベースからPythonの DataFrame（pandas、dask、modin、arrow、polars）へ最速かつ最もメモリ効率の良い方法でデータをロードできるよう、現在のバージョンは [Connector-x ](https://github.com/sfu-db/connector-x)  をバックエンドで使用するようになっています。

 bash
```
 $ python -m pip install -U connectorx
```

データベースへアクセスするために必要なことは、次の1行のコードを実行するだけです。


```
 from dataprep.connector import read_sql
 read_sql("postgresql://username:password@server:port/database", "SELECT * FROM lineitem")
```



### パブリックAPIへのアクセス
Webからデータを収集する場合は、若干のコードが必要になりますが、すべてが簡略化されます。例として [Finnhub ](https://finnhub.io/) の公開APIへアクセスしてみます。
Finnhub は株価や為替、および暗号化資産のレートを提供しているサービスです。Finnhub APIを利用するためには、Finnhubの[アカウントを作成 ](https://finnhub.io/register)し、APIキーを取得する必要があります。フリープランは米国株だけで、1分間あたり最大60APIの利用までという制限があります。

Finnhubに登録すると、自動的にFinnhub Dashboardにリダイレクトされ、APIキーを確認することができます。このAPIキーは、Connectorを使用してFinnhubのデータにアクセスするために使用します。

APIキーを取得できたら次のようなコードで接続を初期化します。GitHubなどでコードを管理する場合では、不用意にAPIキーが公開されてしまうようなことに注意してください。次のようにAPIキーを環境変数から読み取るとよいでしょう。


```
 In [2]: # %load c04_init_connect.py
    ...: import os
    ...: from dataprep.connector import connect, info
    ...:
    ...: auth_token = os.environ.get('FINNHUB_APIKEY', default=None)
    ...: dc = connect('finnhub', _auth={"access_token":auth_token})
    ...:
    ...: dc
    ...:
 Out[2]: <dataprep.connector.connector.Connector at 0x10f2b12a0>
 
 In [3]:
```

### Connector の機能
Connectorには、Finnhubからダウンロードしたデータを調べるめに実行できるいくつかの機能があります。
#### コネクタ情報
 `info()` メソッドは、コネクタの使用に関する情報とガイドラインを提供します。次の4 つの情報があります。

  -  `Table` ー アクセスするテーブル
  -  `Parameters` ー メソッドを呼び出すために使用できるパラメータを特定
  -  `Examples` ー　コネクタ クラスのメソッドを呼び出す方法を示す
  -  `Schema` ー  応答の属性の名前とデータ型


```
 In [3]: info('finnhub')
 /Users/goichiiisaka/anaconda3/envs/EDA_dataprep/lib/python3.10/site-packages/dataprep/utils.py:70: FutureWarning: this method is deprecated in favour of  `Styler.to_html()` 
   return styled_df.render()
 
 In [4]:
 
```

![](https://gyazo.com/ef43a001974d403c80bf7effb87acf68.png)
基本的な使い方を表示される銃砲にしたがってアクセスすることができます。
例として為替関連のニュースを取得する場合は次のようになります。


```
 In [13]: df = await dc.query('general_news', category='currency')
 
 In [14]: df
 Out[14]:
     category  ...                                                url
 0   business  ...  https://www.cnbc.com/2022/04/25/cramers-lightn...
 1   top news  ...  https://www.bloomberg.com/news/audio/2022-04-2...
 2   top news  ...  https://www.marketwatch.com/story/it-looks-lik...
 3   top news  ...  https://www.bloomberg.com/news/features/2022-0...
 4   top news  ...  https://www.bloomberg.com/news/articles/2022-0...
 ..       ...  ...                                                ...
 94  top news  ...  https://www.cnbc.com/2022/04/25/recruiters-are...
 95  top news  ...  https://www.bloomberg.com/news/articles/2022-0...
 96  top news  ...  https://www.marketwatch.com/story/does-employe...
 97  top news  ...  https://www.bloomberg.com/news/articles/2022-0...
 98  top news  ...  https://www.marketwatch.com/story/ecb-official...
 
 [99 rows x 9 columns]
 
 In [15]:
 
```

# デモ動画
[](https://www.youtube.com/watch?v=nSkQy3ew3EI)

# 参考
- DataPrep
  - [オフィシャルサイト ](https://dataprep.ai/)
  - [ソースコード ](https://github.com/sfu-db/dataprep#connector)
  - [公式ドキュメント ](https://docs.dataprep.ai/index.html)
  - [PyPI - dataprep ](https://pypi.org/project/dataprep/)


#EDA


