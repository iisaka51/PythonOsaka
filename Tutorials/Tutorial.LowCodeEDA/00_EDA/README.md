Pythonによる探査的データ分析：入門編
=================

# はじめに
この資料は、Python で探索的データ分析を行うときのポイントについてまとめたものです。


# 探査的データ分析

探索的データ分析（EDA: Exploratory Data Analysis）は、データを分析し、モデル化に進む前に、データセットが持つパターンや視覚的な洞察などを見出すアプローチです。1977年にJohn W. Tukeyという米国の統計学者が初めて使用した言葉です。 通常は、次のステップを複数回繰り返すことになります。

  - データを調査する
  - データを加工し、可視化することで仮説をたてて分析する
  - データセットに対する新たな理解や、仮説に対する新たな視点を得て、以前の仮説を洗練させる

それと重要なことは入手あるいは収集するデータについて事前に考察することは、将的に多くの時間とストレスを軽減してくれることになります。

  - このデータはどのように収集されたのか、どこから得られたのか？
  - なぜこのデータに興味があるのか？
  - 興味のあるターゲット変数は何か？
  - このデータの入手もとは信頼できるのか（評判の良いか）？
  - モデルを作成するのに十分なデータがあるか？
  - 他の人がこのデータセットで同様の分析/モデリングプロジェクトを行ったことがあるか？彼らの結論から学びたいのか、それとも新しいプロジェクトを立ち上げたいのか？
  - そのデータセットの説明はあるか？それは完全なものか？
  - このデータを使用した場合、サイズやライセンス、料金などの追加的な課題や問題が予想されるか？

次からはPandasのDetaFrameにあるデータをどのような手順で調査するのかをみていきましょう。次のライブラリをインストールしておきます。

 bash
```
 $ python -m pip install pandas matplotlib palmerpenguins
```

palmerpenguins はサンプルデータで、 `load_penguins` で読み出せるDataFrameには次のカラムを持っています。

  - species
  - island
  - bill_length_mm
  - bill_depth_mm
  - flipper_length_mm
  - body
  - mass_g
  - sex
  - year

参考：[palmerpenguins   ](https://allisonhorst.github.io/palmerpenguins/index.html)




## データ構造と分布

データ構造と分布を調べるときは、 `.shape` 属性と `.info()` メソッドを呼び出します。


```
 In [2]: # %load c01_describe.py
    ...: import pandas as pd
    ...: from palmerpenguins import load_penguins
    ...:
    ...: df = load_penguins()
    ...:
    ...: df.shape
    ...: df.info()
    ...:
 Out[2]: (344, 8)
 <class 'pandas.core.frame.DataFrame'>
 RangeIndex: 344 entries, 0 to 343
 Data columns (total 8 columns):
  #   Column             Non-Null Count  Dtype
 ---  ------             --------------  -----
  0   species            344 non-null    object
  1   island             344 non-null    object
  2   bill_length_mm     342 non-null    float64
  3   bill_depth_mm      342 non-null    float64
  4   flipper_length_mm  342 non-null    float64
  5   body_mass_g        342 non-null    float64
  6   sex                333 non-null    object
  7   year               344 non-null    int64
 dtypes: float64(4), int64(1), object(3)
 memory usage: 21.6+ KB
 
 In [3]:
 
```

### データ構造の考察ポイント
データ構造では次のような項目について考察します。

  - サンプル数はいくつあるか？
  - 特徴量はいくつあるか?
  - それぞれの特徴量のデータ型は何か?
  - データセットの特徴量について既知の情報から、データ型は妥当か?
  - 欠損値やヌル値はあるか？
  - このデータセットが使用するメモリはどれくらいか？これが後で問題になる可能性ないか？

そして、変数の分布を見るには、次のようになります。基本的な統計量の要約は  `.describe()` で得ることができます。可視化のためには、いくつかコードを実行する必要があります。　これらのコードの慣れていないと理解しずらい上に、分布を知るという本来の目的を実現するために、追加でプロット関連の設定を行う必要があります。


```
 In [2]: # %load c02_plot_hist.py
    ...: # %matplotlib
    ...: import pandas as pd
    ...: from matplotlib import pyplot as plt
    ...: from palmerpenguins import load_penguins
    ...:
    ...: df = load_penguins()
    ...:
    ...: df.describe()
    ...:
    ...: df.hist(figsize=(15,15))
    ...: # 9個以上の変数がある場合は、figsizeを大きく設定
    ...: plt.tight_layout()
    ...: plt.show()
    ...:
 Out[2]:
        bill_length_mm  bill_depth_mm  ...  body_mass_g         year
 count      342.000000     342.000000  ...   342.000000   344.000000
 mean        43.921930      17.151170  ...  4201.754386  2008.029070
 std          5.459584       1.974793  ...   801.954536     0.818356
 min         32.100000      13.100000  ...  2700.000000  2007.000000
 25%         39.225000      15.600000  ...  3550.000000  2007.000000
 50%         44.450000      17.300000  ...  4050.000000  2008.000000
 75%         48.500000      18.700000  ...  4750.000000  2009.000000
 max         59.600000      21.500000  ...  6300.000000  2009.000000
 
 [8 rows x 5 columns]
 Out[2]:
 array([[<AxesSubplot:title={'center':'bill_length_mm'}>,
         <AxesSubplot:title={'center':'bill_depth_mm'}>],
        [<AxesSubplot:title={'center':'flipper_length_mm'}>,
         <AxesSubplot:title={'center':'body_mass_g'}>],
        [<AxesSubplot:title={'center':'year'}>, <AxesSubplot:>]],
       dtype=object)
 
 In [3]:
 
```

![](https://gyazo.com/23d9b321b7a47593e51a9596a9965019.png)
### 分布の考察ポイント
分布では次のような考察を行います。

  - 最大/最小値は、変数に対して妥当な値か？誤差のような値はあるか
  - 各変数の平均値は？ 平均値は、データセット全体について何かを示唆しているか
  - 各変数の分布はどうなっていますか
  - 外れ値があるように見えるか
  - 変数が何を意味するのか、ヒストグラムがそれらの値や広がりの意味を考える。
  - 想定外のことがあるか？


# データクリーニング
データ分析では、データの信頼性が非常に重要です。信頼性の高いデータセットには、次の5つの重要な特徴があります。

  - 妥当性
  - 統一性
  - 一貫性
  - 正確性
  - 完全性

データクリーニングは、欠損値の処理とカテゴリ特徴の数値への変換を行います。これにより、分析で使用できる信頼性の高いデータセットになるわけです。

# 重複値と欠損値
重複値があるかを調べるためには次のコードを実行します。


```
 In [2]: # %load c03_duplicated.py
    ...: import pandas as pd
    ...:
    ...: s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
    ...: df = pd.DataFrame(s)
    ...:
    ...: df.duplicated().sum()
    ...:
 Out[2]: 1
 
 In [3]:
 
```

このコードを実行した結果、0より大きい値が表示されると重複値(重風した行）があることになります。重複値を削除したいときは、次のコードを実行します。


```
 In [2]: # %load c04_deduplicated.py
    ...: import pandas as pd
    ...:
    ...: s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
    ...: df = pd.DataFrame(s)
    ...:
    ...: df.drop_duplicates(inplace=True)
    ...: df.duplicated().sum()
    ...:
 Out[2]: 0
 
 In [3]:
 
```

欠損値を調べるときは `.isna()` を呼び出します。


```
 In [2]: # %load c05_na_val.py
    ...: import pandas as pd
    ...:
    ...: s = pd.Series([0,1,2,3,None,5,6,9,10,13,40])
    ...: df = pd.DataFrame(s)
    ...: df.isna()
    ...:
    ...: from palmerpenguins import load_penguins
    ...: df = load_penguins()
    ...:
    ...: null = df.isna().sum()/len(df)
    ...: null[null > 0].sort_values()
    ...:
 Out[2]:
         0
 0   False
 1   False
 2   False
 3   False
 4    True
 5   False
 6   False
 7   False
 8   False
 9   False
 10  False
 Out[2]:
 bill_length_mm       0.005814
 bill_depth_mm        0.005814
 flipper_length_mm    0.005814
 body_mass_g          0.005814
 sex                  0.031977
 dtype: float64
 
 In [3]:
 
```

## 欠損値と重複値の考察ポイント
欠損値と重複値では、次の項目について考察を行います。

  - 欠損値（NaN, NULLなどゼロ以外のもの）は、データの記録方法の結果か？
  - 分析に大きな影響を与えることなく、欠損値の行を削除できるか？
  - 変数の分布を見て、その変数の平均値または中央値で欠損値を埋めることは正当化できるか？
  - もしデータが時系列データであれば、補間で欠損値を埋めることができるか？
  - ある変数の欠損値があまりに多ければ、その変数をデータセットから取り除くべきか検討する

欠損値と重複値には注意を払う必要があります。データを加工するよりも、行を削除した方が良い場合もあります。重要なことは、悪いデータを分析しても、意味のある結果を得ることはできないことに留意してください。

# 外れ値
データセットの**外れ値（Outliers）**を可視化するためには箱ひげ図を作成します。もし変数がほぼ同じスケールであれば、Pandasの  `df.boxplot()` メソッドを使用するだけです。これはデータセット内のすべての連続変数について、同じグラフ上に箱ひげ図を作成します。


```
 In [2]: # %load c06_outliers.py
    ...: import pandas as pd
    ...: from matplotlib import pyplot as plt
    ...:
    ...: s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
    ...: df = pd.DataFrame(s)
    ...:
    ...: df.boxplot()
    ...: plt.tight_layout()
    ...: plt.show()
    ...:
 Out[2]: <AxesSubplot:>
 
 In [3]:
 
```


![](https://gyazo.com/4f2ad7462e1e90282a0c90f1f7f6f0aa.png)




もし、スケールが異なる変数があれば、ループの中でサブプロットを使ってプロットすることができます。
参考: [Stack Overflow - pandas boxplots as subplots with individual y-axis ](https://stackoverflow.com/questions/49690316/pandas-boxplots-as-subplots-with-individual-y-axis)


```
 In [2]: # %load c07_multi_val_outliers.py
    ...: import random
    ...: import pandas as pd
    ...: import matplotlib.pyplot as plt
    ...:
    ...: df = pd.DataFrame(data={'A': random.sample(range(60, 100), 10),
    ...:                         'B': random.sample(range(20, 40), 10),
    ...:                         'C': random.sample(range(2000, 3010), 10),
    ...:                         'type': list(3*'A')+list(3*'B')+list(4*'C')})
    ...:
    ...: fig, axes = plt.subplots(2,2)
    ...:
    ...: for i,el in enumerate(list(df.columns.values)[:-1]):
    ...:     a = df.boxplot(el, by="type", ax=axes.flatten()[i])
    ...:
    ...: fig.delaxes(axes[1,1])
    ...: plt.tight_layout()
    ...:
    ...: plt.show()
    ...:
 
 In [3]:
 
```


![](https://gyazo.com/c845d0ac113bdc72c6add020edb536b1.png)
## 外れ値の考察ポイント
外れ値では次の項目について考察します。

  - データの各変数に外れ値があるか？（箱ひげ図では黒丸で表示される）
  - なぜ外れ値があるのかを考える
  - 外れ値は実際のデータを表しているか？（つまり、誤差ではないのか）
  - 外れ値のデータを除外すべきか？　 そうでない場合、値をwinsorize（外れ値を外れ値以外の最大値・最小値で置き換える）するべきか？

外れ値への対応は少し厄介です。外れ値を識別したとしても、他にいくつかのモデルを試すまでそれらをそのままにしておきく方が良い場合があります。モデルの精度が低いと分かっ時点で、外れ値を持つ変数（複数可）をwinsorizeすべきかどうか再度検討するべきでしょう。単純に外れ値を除去するよりも、データサイズが少ない場合はほかのカラムの情報を有効活用できることがあります。

# 相関関係/関係性
連続変数の相関関係(Correlations)の行列を作るためには、 `.corr()` メソッドを使用します。


```
 In [2]: # %load c08_Correlations.py
    ...: # %matplotlib
    ...: import pandas as pd
    ...: from matplotlib import pyplot as plt
    ...: from palmerpenguins import load_penguins
    ...:
    ...: df = load_penguins()
    ...:
    ...: df.corr()
    ...:
 Out[2]:
                    bill_length_mm  bill_depth_mm  ...  body_mass_g      year
 bill_length_mm           1.000000      -0.235053  ...     0.595110  0.054545
 bill_depth_mm           -0.235053       1.000000  ...    -0.471916 -0.060354
 flipper_length_mm        0.656181      -0.583851  ...     0.871202  0.169675
 body_mass_g              0.595110      -0.471916  ...     1.000000  0.042209
 year                     0.054545      -0.060354  ...     0.042209  1.000000
 
 [5 rows x 5 columns]
 
 In [3]:
 
```

## 相関関係での考察ポイント
データの相関関係では次の項目について考察を行います。

  - どの変数が、ターゲット変数と最も相関しているか？
  - 多重共線性(multicollinearity: 相関係数が > 0.8 となる2つの特徴) はあるか？　これはモデルにどのように影響するか？
  - 同じ情報を表現する変数があるか？　そのうちひとつは削除できるか？


# 特徴量
特徴量について調査することは、特徴量エンジニアリング(Feature Engineering)と呼ばれることがあります。これは、今あるデータの特徴量からドメイン知識などを生かして新しくデータの特徴量を追加する作業のことをいいます。
特徴量エンジニアリングでよく使われる手法には次のようなものがあります。

## 変数変換
最も一般的な変換はワンホットエンコーディング(one-hot-encoding) で、カテゴリ変数を数値（具体的にはバイナリ）変数に変換する。これは、機械学習モデルが「オブジェクト」データ型を扱えないために必要になります。Pandas では `get_dummies()` メソッドを使って簡単に処理することができます。


```
 In [2]: import pandas as pd
    ...: from palmerpenguins import load_penguins
    ...:
    ...: df = load_penguins()
    ...:
    ...: new_df = pd.get_dummies(df,drop_first=True)
    ...:
 
 In [3]: df
 Out[3]:
        species     island  bill_length_mm  ...  body_mass_g     sex  year
 0       Adelie  Torgersen            39.1  ...       3750.0    male  2007
 1       Adelie  Torgersen            39.5  ...       3800.0  female  2007
 2       Adelie  Torgersen            40.3  ...       3250.0  female  2007
 3       Adelie  Torgersen             NaN  ...          NaN     NaN  2007
 4       Adelie  Torgersen            36.7  ...       3450.0  female  2007
 ..         ...        ...             ...  ...          ...     ...   ...
 339  Chinstrap      Dream            55.8  ...       4000.0    male  2009
 340  Chinstrap      Dream            43.5  ...       3400.0  female  2009
 341  Chinstrap      Dream            49.6  ...       3775.0    male  2009
 342  Chinstrap      Dream            50.8  ...       4100.0    male  2009
 343  Chinstrap      Dream            50.2  ...       3775.0  female  2009
 
 [344 rows x 8 columns]
 
 In [4]: new_df
 Out[4]:
      bill_length_mm  bill_depth_mm  ...  island_Torgersen  sex_male
 0              39.1           18.7  ...                 1         1
 1              39.5           17.4  ...                 1         0
 2              40.3           18.0  ...                 1         0
 3               NaN            NaN  ...                 1         0
 4              36.7           19.3  ...                 1         0
 ..              ...            ...  ...               ...       ...
 339            55.8           19.8  ...                 0         1
 340            43.5           18.1  ...                 0         0
 341            49.6           18.2  ...                 0         1
 342            50.8           19.0  ...                 0         1
 343            50.2           18.7  ...                 0         0
 
 [344 rows x 10 columns]
 
 In [5]:
 
```

場合によっては、変数が正規分布に従うように変換したい場合があります。これには、NumPuの  `np.log()` 、 `np.sqrt()` 、box-cox変換、その他の正規分布に合うようにデータを変換する関数を試すことができます。

## 新しい特徴量の追加
新しく特徴量を追加することは、それだけで[書籍 ](https://www.packtpub.com/product/hands-on-exploratory-data-analysis-with-python/9781789537253) になるほど非常に難しく、慎重に行う必要がありあす。それに、多くのプロジェクトに適用できるような画一的なコードがあるわけでもありません。
通常は、次のようなケースでは特徴量を追加したくなります。

  - ある結果とある特徴の関係が、もう一つの特徴に依存していると思われる場合
    - 相互作用変数を作成する
  - 線形関係を作りたい
    - 二次関数以上の関数を作る
  - データセットにない変数や情報が考えられる 
    - ある変数の関数を使ってその変数を作成する


## 望ましい分析環境
Jupyterlab をプラットフォームにしておくと、分析するためのコード、データを可視化したプロット図、とそこから得られた知見をメモや考察内容を容易に管理することができるため、効率的な分析が行えるためおすすめです。


# まとめ

データを分析するためには、どのような手順と方法があるのかについて基本的な知識について知ることができたはずです。実際に多くのデータをご自分で分析することのきっかけになれば幸いです。


# 参考
- Pandas
  - [Pandas オフィシャルサイト ](https://pandas.pydata.org/)
- NumPy
  - [NumPy オフィシャルサイト ](https://numpy.org/)
- Qiita
  - [特徴量エンジニアリングおさらいメモ ](https://qiita.com/takahashi_yukou/items/2b6d7776634ef55cec58)
- 書籍
  - [Packt - Hands-On Exploratory Data Analysis with Python ](https://www.packtpub.com/product/hands-on-exploratory-data-analysis-with-python/9781789537253)
- PythonOsaka
  - [Jupyter  Notebookを使ってみよう]
  - [Jupyter Notebook が使えるクラウドサービス]


