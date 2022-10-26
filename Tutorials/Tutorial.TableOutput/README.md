Python チュートリアル：データのテーブル出力
=================

![](https://github.com/iisaka51/PythonOsaka/blob/main/data/images/Python_Logo.png)


## はじめに
データを視覚化するとき、段落やCSVフォーマットよりも、表形式で出力する方が理解が簡単になります。適切に整形されたテーブルは、それぞれのデータについて、ヘッダと値で簡単に理解することができます。
Python では次のモジュールが使用できます。

- [pandas ](https://pandas.pydata.org/)：データフレームを `print()` に渡すだけで端末に表形式で出力される。
  - Markdown, HTMLなどの出力フォーマットの指定は外部モジュールに依存する。
- [tarmtables ](https://github.com/nschloe/termtables)：端末に表示することに特化したモジュール
  - numpy のデータ確認がpandas のように簡単にできるようになる。
- [tabulate ](https://github.com/astanin/python-tabulate)：いろいろな表書式で出力することができる。
  - numpy や pandas との親和性が高く、ndarrayやDataFrameを入力データにできる。
  - pandas も Markdown 出力はこのモジュールで処理している。
  - データの読み込みはできないが、pandas を利用すれば問題はない。
- [pretytable ](https://github.com/jazzband/prettytable)：軽量で簡単に使える。フォーマット変換ツールとしても利用可能。
  - ASCII、HTML、JSON、CSVフォーマットで出力できる。
  - CSV,、JSON、データベース・カーソル、HTMLからデータを読み込める。
　[beatifultable ](https://github.com/pri22296/beautifultable)：きれいなASCII形式の表形式データを端末に簡単に出力できる。
　	１つのセルが複数行をもつようなテーブルも簡単に出力できる

他にも次のようなモジュールがありますが、これらはここでは取り上げません。
- [sqlite-utiils ](https://sqlite-utils.datasette.io/en/stable/)：本来はSQLiteを操作するためのライブラリで、CLIも提供されている
  - CSVファイル読み込んで様々な表形式で出力する機能があるが、このためだけに導入するにはコスト高。
  - CSVファイルをSQLコマンドで検索できるなど、別の機能（こちらが本来の機能）もある
  - 参考: [sqlite-utilsを使ってみよう]
- [rich ](https://github.com/willmcgugan/rich)：TUIアプリケーションを作成するためのフレームワーク。
  - 美しいテーブルを出力できる
  - numpyやpandasとの親和性が低く、データは文字列で与える必要がある。
  - 参考：[TUIアプリケーションフレームワーク Rich を使ってみよう]
- [pythongrid ](https://pythongrid.com/)：表出力が容易なWebフレームワーク。HTMLが前提。
  - 単にデータを端末に出力したいという目的には少し重厚。
- [asciitable ](https://cxc.cfa.harvard.edu/contrib/asciitable/)：さまざまな表形式の読み取りと書き込みを行うことができるフレームワーク。
  - 新規プロジェクトに向いているが、単にデータを端末に出力したいという目的には少し重厚。
- [TableIt ](https://github.com/SuperMaZingCoder/TableIt)：単純に端末に出力するだけなので簡単に使える。
  - パッケージ化されていないため、個々のプロジェクトでコピーして使用する。
- [texttable ](https://github.com/foutaise/texttable/)：表を作成するためにモジュール。
  - 読み込んだデータを、端末に出力したいという目的には設定が煩雑になる。
  - LaTex形式で出力する[latextable ](https://github.com/JAEarly/latextable)はこのモジュールがベースになっている。
- [terminaltables ](https://github.com/Robpol86/terminaltables)：データを端末やコンソールアプリケーションに簡単に描画できる。
  - 複数行の行をサポートしている。

## Pure Python3
Python だけで表出力を記述した例です。
モジュールを使う必要がありませんが、判読性が低くなる欠点があります。

```
 def print_results_table(data, teams_list):
     str_l = max(len(t) for t in teams_list)
     print(" ".join(['{:>{length}s}'.format(t, length = str_l) for t in [" "] + teams_list]))
     for t, row in zip(teams_list, data):
         print(" ".join(['{:>{length}s}'.format(str(x), length = str_l) for x in [t] + row]))

 teams_list = ["Dallas", "Chicago", "Los Angeles"]
 data = [[1, 2, 1],
         [0, 1, 0],
         [2, 4, 1]]

 print_results_table(data, teams_list)
```

 zsh
```
 % python  pure_python.py
             Man Utd  Man City T Hotspur
   Man Utd         1         2         1
  Man City         0         1         0
 T Hotspur         2         4         2
```

## Pandas
Pandas のデータフレームを `print()` するだけです。
jupyter notebook では美しく整形されて出力されます。端末での出力は、内容確認はしやすいのですが境界線は出力することができません。
また、マークダウンなど他の表形式で出力することには対応していません。
 using_pandas.py
```
 import numpy as np
 import pandas as pd

 teams_list = ["Dallas", "Chicago", "Los Angeles"]
 data = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [2, 4, 1]])

 df = pd.DataFrame(data, teams_list, teams_list)
 print(df)
```

 zsh
```
 % python using_pandas.py
              Dallas  Chicago  Los Angeles
 Dallas            1        2            1
 Chicago           0        1            0
 Los Angeles       2        4            1
```

ただし、デフォルトではデータが多い場合、途中が省略されてしまいます。
 using_pandas_readcsv.py
```
 import numpy as np
 import pandas as pd

 df = pd.read_csv('TOYOTA.csv')
 print(df)
```

 zsh
```
 % python using_pandas_from_csv.py
             Date    High     Low    Open   Close      Volume    Adj Close
 0     2015-01-05  7575.0  7416.0  7565.0  7507.0   9515300.0  6402.834473
 1     2015-01-06  7391.0  7300.0  7322.0  7300.0  12387900.0  6226.280273
 2     2015-01-07  7485.0  7255.0  7256.0  7407.0  11465400.0  6317.542969
 3     2015-01-08  7556.0  7495.0  7500.0  7554.0  10054500.0  6442.921387
 4     2015-01-09  7666.0  7561.0  7630.0  7609.0  10425400.0  6489.832520
 ...          ...     ...     ...     ...     ...         ...          ...
 1286  2020-03-09  6587.0  6376.0  6570.0  6495.0   8862700.0  6495.000000
 1287  2020-03-10  6660.0  6266.0  6395.0  6600.0   9822300.0  6600.000000
 1288  2020-03-11  6830.0  6512.0  6630.0  6535.0   8273900.0  6535.000000
 1289  2020-03-12  6449.0  6229.0  6400.0  6309.0   9598800.0  6309.000000
 1290  2020-03-13  6343.0  5771.0  5926.0  6084.0  15841000.0  6084.000000

 [1291 rows x 7 columns]
```

これは、 `pandas.options.display.max_rows` がデフォルトでは60となっているためです。
前述のデータをすべて表示させたい場合（それが’必要かどうかは別にして）、次のようにします。

```
 >>> import pandas as pd
 >>> pd.options.display.max_rows
 60
 >>> pd.options.display.max_rows=1300
 >>> df = pd.read_csv('TOYOTA.csv')
 >>> print(df)
```


## termtables
 `termtables.print()` にデータを与えるだけで、端末にデータを表形式で表示するので、簡単に使用できます。
pandas を利用すると同じことができるので、このモジュールの利用価値は低いかもしれません。


```
 import termtables as tt
 import numpy

 numpy.random.seed(0)
 data = numpy.random.rand(5, 2)

 tt.print(data)
```

![](https://gyazo.com/dafd23c50bd4d564c13f1882631cb030.png)

端末に表示するボーダーが変わる程度ですが、スタイル指定はできます。
一番使えそうなものは markdown です。
ただし、Markdown形式の出力が目的なのであれば、次のtabulateモジュールを使用する方がよいでしょう。

 termtables_demo2.py
```
 import termtables as tt

 header = ["a", "bb", "ccc"]
 data = [
     [1, 2, 3], [613.23236243236, 613.23236243236, 613.23236243236]
 ]

 tt.print(
     data,
     header=header,
     style=tt.styles.markdown,
     padding=(0, 1),
     alignment="lcr"
 )
```

 zsh
```
 % python termtable_dmeo2.py
 | a               |       bb        |             ccc |
 |-----------------|-----------------|-----------------|
 | 1               |        2        |               3 |
 | 613.23236243236 | 613.23236243236 | 613.23236243236 |
```

## tabulate
tabulate は表形式のデータをきれいに画面表示するための拡張ライブラリです。
地味なモジュールですがメールやブログ、Wiki に貼り付けるときにとても便利です。

tabulate の使用例としては次のものがあります。

- 手間をかけずに小さなテーブルを表示する（文字列に変換）：
  - 関数を1回呼び出すだけで、フォーマットはデータ内容によって導出されます。
- 軽量のプレーンテキストマークアップのための表形式データの作成：
  - さらに編集したり何かで変換するのに適した複数の出力形式をサポート
- テキストと数値の混合データを読みやすく表現
  - スマートな列の配置、構成可能な数値のフォーマット、小数点による配置

### インストール
tabulate は拡張モジュールなので次のようにインストールします。
 bash
```
 $ pip install tabulate
```

### tabulate のサポートするデータ型
次の表形式のデータ型がサポートされています。

- リストのリストまたは別の反復可能な反復可能オブジェクト
- リストまたは別の反復可能な辞書（列としてのキー）
- イテラブルの辞書（列としてのキー）
- 2次元NumPy配列
- NumPyレコード配列（列としての名前）
- pandas.DataFrame

### 使用方法
 IPython
```
 import numpy as np
 from tabulate import tabulate

 teams_list = ["Dallas", "Chicago", "Los Angelos"]
 data = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [2, 4, 1]])

 table = tabulate(data, headers=teams_list)
 print(table)
```

 zsh
```
 % python using_tabulate.py
   Dallas    Chicago    Los Angelos
 --------  ---------  -------------
        1          2              1
        0          1              0
        2          4              1
```

### tabulate がサポートする表形式
tabulateがサポートする表形式は、tabulate_formats プロパティーに格納されています。
 `table()` に `tablefmt='github'` ように与えることで出力フォーマットを変更することができます。
 IPython
```
 In [6]: import tabulate
 In [7]: tabulate.tabulate_formats
 Out[7]:
 ['fancy_grid',
  'github',
  'grid',
  'html',
  'jira',
  'latex',
  'latex_booktabs',
  'latex_raw',
  'mediawiki',
  'moinmoin',
  'orgtbl',
  'pipe',
  'plain',
  'presto',
  'psql',
  'rst',
  'simple',
  'textile',
  'tsv',
  'youtrack']
```

Qiitaでは表の書式に github のものを採用しています。
Scapboxでは tsv を指定すると表の記述が楽になります。

 using_tabulate_pandas.py
```
 import numpy as np
 import pandas as pd
 from tabulate import tabulate

 df = pd.read_csv('TOYOTA.csv')
 print(tabulate(df[:10],df.columns, tablefmt='github', showindex=False))
```

 zsh
```
 % python using_tabulate_pandas.py
 | Date       |   High |   Low |   Open |   Close |      Volume |   Adj Close |
 |------------|--------|-------|--------|---------|-------------|-------------|
 | 2015-01-05 |   7575 |  7416 |   7565 |    7507 | 9.5153e+06  |     6402.83 |
 | 2015-01-06 |   7391 |  7300 |   7322 |    7300 | 1.23879e+07 |     6226.28 |
 | 2015-01-07 |   7485 |  7255 |   7256 |    7407 | 1.14654e+07 |     6317.54 |
 | 2015-01-08 |   7556 |  7495 |   7500 |    7554 | 1.00545e+07 |     6442.92 |
 | 2015-01-09 |   7666 |  7561 |   7630 |    7609 | 1.04254e+07 |     6489.83 |
 | 2015-01-13 |   7526 |  7368 |   7440 |    7519 | 1.111e+07   |     6413.07 |
 | 2015-01-14 |   7479 |  7390 |   7428 |    7396 | 1.00273e+07 |     6308.16 |
 | 2015-01-15 |   7548 |  7435 |   7437 |    7526 | 8.9295e+06  |     6419.04 |
```

## prettytable

[PrettyTable ](https://github.com/jazzband/prettytable)は、データをASCII文字で表形式で出力することがための拡張ライブラリです。
機能としては次のものがあります。
- 出力のスタイルを制御
  - 列のパディングの幅、テキストの配置、テーブルの境界線など、テーブル表示のさまざまな制御を行うことができます。
- データを並べ替える
- 出力データの選択：データの列と行を選択することができる
- 複数のデータソースをサポート
  - CSV、JSON、HTML、データベースカーソルからデータを読み取ることができる
- 複数の出力フォーマットをサポート
  - ASCII、CSV、JSON、HTMLで出力することができる

 using_prettytable.py
```
 import numpy as np
 from prettytable import PrettyTable

 teams_list = ["Dallas", "Chicago", "Los Angeles"]
 data = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [2, 4, 1]])

 table = PrettyTable(field_names = teams_list)
 for row in data:
     table.add_row(row)

 print(table)
```

zsh
```
 % python using_prettytable.py
 +--------+---------+-------------+
 | Dallas | Chicago | Los Angeles |
 +--------+---------+-------------+
 |   1    |    2    |      1      |
 |   0    |    1    |      0      |
 |   2    |    4    |      1      |
 +--------+---------+-------------+
```

### CSVファイルからデータを読み込む
次のCSVファイルからデータを読み込んでみましょう。
 CITY.csv
```
 City name,Area,Population,Annual Rainfall
 Adelaide, 1295, 1158259, 600.5
 Brisbane, 5905, 1857594, 1146.4
 Darwin, 112, 120900, 1714.7
 Hobart, 1357, 205556, 619.5
 Melbourne, 1566, 3806092, 646.9
 Perth, 5386, 1554769, 869.4
 Sydney, 2058, 4336374, 1214.8
```

 prettytable_csv.py
```
 from prettytable import from_csv

 with open("CITY.csv") as fp:
     table = from_csv(fp)

 print(table)
```

 zsh
```
 % python prettytable_csv.py
 +-----------+------+------------+-----------------+
 | City name | Area | Population | Annual Rainfall |
 +-----------+------+------------+-----------------+
 |  Adelaide | 1295 |  1158259   |      600.5      |
 |  Brisbane | 5905 |  1857594   |      1146.4     |
 |   Darwin  | 112  |   120900   |      1714.7     |
 |   Hobart  | 1357 |   205556   |      619.5      |
 | Melbourne | 1566 |  3806092   |      646.9      |
 |   Perth   | 5386 |  1554769   |      869.4      |
 |   Sydney  | 2058 |  4336374   |      1214.8     |
 +-----------+------+------------+-----------------+
```


## BeatifulTable
[beatifultable ](https://github.com/pri22296/beautifultable)：きれいなASCII形式の表形式データを端末に簡単に出力できる拡張モジュールです。

次のような特徴があります。

- テーブルのルックアンドフィールの完全なカスタマイズ
- 豊富なテーブル作成の方法を提供
  - 行ごとに追加、列ごとに追加、これらの両方の方法を組み合わせたテーブル作成方法が可能
- カラー出力をサポート：
  - ANSIシーケンスや任意のライブラリを使用したカラー表示ができる
- 複数の出力スタイルをサポート
  - カスタムスタイルを作成することもできる。
- Unicode文字のサポート
- ストリーミングテーブルのサポート
  - データの取得が遅い場合に有益で便利です。

 using_beautifultable.py
```
 import numpy as np
 from beautifultable import BeautifulTable

 teams_list = ["Dallas", "Chicago", "Los Angeles"]
 data = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [2, 4, 1]])

 table = BeautifulTable()
 table.columns.header = teams_list
 for r in range(len(data)):
     table.rows.append(data[r])

 print(table)
```

 zsh
```
 % python using_beautifultable.py
 +--------+---------+-------------+
 | Dallas | Chicago | Los Angeles |
 +--------+---------+-------------+
 |   1    |    2    |      1      |
 +--------+---------+-------------+
 |   0    |    1    |      0      |
 +--------+---------+-------------+
 |   2    |    4    |      1      |
 +--------+---------+-------------+
```

Pandas のデータフレームのようにカラム、行を抜き出すことも簡単にできます。
 usng_beautifultable2.py
```
 import numpy as np
 from beautifultable import BeautifulTable

 teams_list = ["Dallas", "Chicago", "Los Angeles"]
 data = np.array([[1, 2, 1],
                  [0, 1, 0],
                  [2, 4, 1]])

 table = BeautifulTable()
 table.columns.header = teams_list
 for r in range(len(data)):
     table.rows.append(data[r])

 new_table = table.rows[:2]
 print(new_table)

 new_table = table.columns[:2]
 print(new_table)
```

 zsh
```
 % python using_beautifultable2.py
 +--------+---------+-------------+
 | Dallas | Chicago | Los Angeles |
 +--------+---------+-------------+
 |   1    |    2    |      1      |
 +--------+---------+-------------+
 |   0    |    1    |      0      |
 +--------+---------+-------------+
 +--------+---------+
 | Dallas | Chicago |
 +--------+---------+
 |   1    |    2    |
 +--------+---------+
 |   0    |    1    |
 +--------+---------+
 |   2    |    4    |
 +--------+---------+
```


```
 table.columns.alignment['Dallas'] = BeautifulTable.ALIGN_LEFT
 table.columns.alignment['Chicago'] = BeautifulTable.ALIGN_CENTER  # default
 table.columns.alignment['Los Angeles'] = BeautifulTable.ALIGN_RIGHT
```

 zsh
```
 % python using_beautifultable_alignment.py
 +--------+---------+-------------+
 | Dallas | Chicago | Los Angeles |
 +--------+---------+-------------+
 | 1      |    2    |           1 |
 +--------+---------+-------------+
 | 0      |    1    |           0 |
 +--------+---------+-------------+
 | 2      |    4    |           1 |
 +--------+---------+-------------+
```


```
 table.columns.padding_left['Dallas'] = 3
 table.columns.padding_left['Chicago'] = 5
 table.columns.padding_right['Los Angeles'] = 7
```

 zsh
```
 % python using_beautifultable_padding.py
 +----------+-------------+-------------------+
 |   Dallas |     Chicago | Los Angeles       |
 +----------+-------------+-------------------+
 |     1    |        2    |      1            |
 +----------+-------------+-------------------+
 |     0    |        1    |      0            |
 +----------+-------------+-------------------+
 |     2    |        4    |      1            |
 +----------+-------------+-------------------+
```

### スタイル
beautifultable では次のスタイルで出力することができます。
デフォルトのスタイルは `STYLE_DEFAULT` は `STYLE_MYSQL` を指定したときと同じです。これは、MySQLでのテーブル出力フォーマットで表示します
　 `STYLE_DEFAULT` /  `STYLE_MYSQL`
-  `STYLE_NONE`
-  `STYLE_DOTED`
-  `STYLE_SEPARATED`
-  `STYLE_COMPACT`
-  `STYLE_MARKDOWN`
-  `STYLE_RST`
-  `STYLE_BOX`
-  `STYLE_DOUBLED`
-  `SYTLE_BOX_ROUNDED`
-  `STYLE_GRID`

### 色表示

```
 from termcolor import colored

 table.rows.append([
     colored("Dallas", "blue"),
     colored("Chicago", "cyan"),
     colored("Los Angeles", "red")
     ])
```

 using_beautiuletable_paragraph.py
```
 rom beautifultable import BeautifulTable

 table = BeautifulTable(maxwidth=40)
 table.columns.header = ["Heading 1", "Heading 2"]
 table.rows.append(["first Line\nsecond Line", "single line"])
 table.rows.append(["first Line\nsecond Line\nthird Line",
                    "first Line\nsecond Line"])
 table.rows.append(["UTF8エンコーディングをサポートしています",
                    "日本語の表示と折返しもOKです"])

 print(table)
```

 zsh
```
 % python using_beautifultable_paragraph.py
 +----------------------+---------------+
 |      Heading 1       |   Heading 2   |
 +----------------------+---------------+
 |      first Line      |  single line  |
 |     second Line      |               |
 +----------------------+---------------+
 |      first Line      |  first Line   |
 |     second Line      |  second Line  |
 |      third Line      |               |
 +----------------------+---------------+
 | UTF8エンコーディング | 日本語の表示  |
 | をサポートしています | と折返しもOK  |
 |                      |     です      |
 +----------------------+---------------+
```

>補足説明：
> この資料を提供しているサービス ScrapBoxの仕様のため、
> 端末では期待どおりに出力できていますが、
> コピー＆ペーストした code ボックスの中ではずれてしまっています。




## まとめ
データを表形式で出力したいという目的では、次のモジュールの使用を考えるのがよでしょう。

1. Pandas
- データの集計や統計処理が必要になるのであれば、必須でしょう。
2. tabutate
- Pandas との親和性が高く、学習コストが無駄にならない。
3. prettytable
- CSVからJSONなどのフォーマット変換ツールとしても使える。
4. beautifultable
- １つのセルが複数行のテーブルを表現できるのは優秀。
- 端末への出力に限定しているのであれば、検討の余地があります。


## 参考
- [Python 公式ドキュメント - formatメソッド ](https://docs.python.org/3/tutorial/inputoutput.html#the-string-format-method)
　[PyFormat ](https://pyformat.info/)：Python での%演算子、 `str` 型の `.format` についてまとめたサイト
　[Python Courses - formatted output ](https://www.python-course.eu/python3_formatted_output.php)
　[データをtabulateで簡単に表形式で出力してみよう]
　[データをprettytableで簡単に表形式で出力してみよう]
　[データをbeautifultableで簡単に表形式で出力してみよう]


