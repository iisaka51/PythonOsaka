Pythonチュートリアル：Pythonによる探査的データ分析
=================
![](https://gyazo.com/153a339305d78fc4fa4850753e4b1594.png)

# はじめに
この資料は、Python で探索的データ分析を行うときに便利に使用できる支援ツールにつ>いてまとめたものです。

# 探査的データ分析
- [Pythonによる探査的データ分析：入門編]


# 探査的データ分析の支援ツール

pandasのデータフレームを使ったデータ探索は、一つ一つの分析をゼロからコーディングする必要があるため、非常に手間がかかるものでした。データをより良く理解するためには多くの時間が必要になり、デバッグなどの気力を奪う作業が必要なこともあります。幸いにも、Python には多くの自動可視化を行うことができる支援ツールがあり、それらを使用することでEDAを行うための時間を大幅に削減することができます。
ここでは、次のパッケージについて紹介します。

- ローコードタイプ (Low Code)
  - [skimpy](https://github.com/aeturrell/skimpy)
  - [snapedautility](https://pypi.org/project/snapedautility/)
  - [Pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)
  - [Sweetviz](https://github.com/fbdesignpro/sweetviz)
  - [Lux](https://pypi.org/project/lux/)
  - [DataPrep](https://github.com/sfu-db/dataprep)

- ノーコード/ゼロコードタイプ(No Code/Zero Code)
  - [Pandas_UI](https://github.com/arunnbaba/pandas_ui)
  - [PandasGUI](https://pypi.org/project/pandasgui/)
  - [Autoviz](https://pypi.org/project/autoviz/)
  - [D-Tale](https://pypi.org/project/dtale/)
  - [Ba,boolib](https://pypi.org/project/bamboolib/)
  - [Visidata](https://pypi.org/project/visidata/)
  - [Mito](https://www.trymito.io/)
  - [ScatterText](https://github.com/JasonKessler/scattertext)
  - [OpenRefine](https://openrefine.org/)

- 可視化ツールタイプ
  - [HoloViz](https://holoviz.org/tutorial/)

- クラウドサービス
  - Google - [Cloud Dataprep by Trifacta](https://cloud.google.com/dataprep?hl=ja)
    - GCP 管理コンソールからの Dataprep のフローやレシピの作成は無料で利用できますが、フローを実行する際には Dataflow ジョブを使ってデータ処理を行うため、Dataflow の利用料金がかかります。




これらのツールは簡単な操作でデータを可視化することができる機能を持っていて、ローコードツール(Low Code Tool)と呼ばれたりもします。



## skimpy
[skimpy](https://github.com/aeturrell/skimpy)は、データの要約を表示する `.describe()`の拡張版を提供する軽量なPythonパッケージです。データレポートは非常にシンプルですが、必要な情報はほぼすべて含まれています。このライブラリのレポートは他のツールほど完全ではありませんが、要約として時々使うには十分なものです。


### インストール
skimpy  は次のようにインストールします。

```bash
 $ python -m pip install skimpy
```


### 使用方法
skimpy の使用方法は簡単です。`skim()` にデータフレームを与えるだけです。

```python
 In [2]: # %load c01_skimpy_demo.py
    ...: from skimpy import skim, generate_test_data
    ...:
    ...: df = generate_test_data()
    ...: skim(df)
    ...:
    ...: # df.describe()
    ...:
 ╭─────────────────────────────── skimpy summary ───────────────────────────────╮
 │          Data Summary                Data Types                              │
 │ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓ ┏━━━━━━━━━━━━━┳━━━━━━━┓                       │
 │ ┃ dataframe         ┃ Values ┃ ┃ Column Type ┃ Count ┃                       │
 │ ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩ ┡━━━━━━━━━━━━━╇━━━━━━━┩                       │
 │ │ Number of rows    │ 1000   │ │ float64     │ 3     │                       │
 │ │ Number of columns │ 10     │ │ category    │ 2     │                       │
 │ └───────────────────┴────────┘ │ datetime64  │ 2     │                       │
 │                                │ int64       │ 1     │                       │
 │                                │ bool        │ 1     │                       │
 │                                │ string      │ 1     │                       │
 │                                └─────────────┴───────┘                       │
 │        Categories                                                            │
 │ ┏━━━━━━━━━━━━━━━━━━━━━━━┓                                                    │
 │ ┃ Categorical Variables ┃                                                    │
 │ ┡━━━━━━━━━━━━━━━━━━━━━━━┩                                                    │
 │ │ class                 │                                                    │
 │ │ location              │                                                    │
 │ └───────────────────────┘                                                    │
 │                                   number                                     │
 │ ┏━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━┓  │
 │ ┃       ┃ missi ┃ comp ┃ mean  ┃ sd   ┃ p0   ┃ p25   ┃ p75  ┃ p100 ┃ hist ┃  │
 │ ┃       ┃ ng    ┃ lete ┃       ┃      ┃      ┃       ┃      ┃      ┃      ┃  │
 │ ┃       ┃       ┃      ┃       ┃      ┃      ┃       ┃      ┃      ┃      ┃  │
 │ ┃       ┃       ┃ rate ┃       ┃      ┃      ┃       ┃      ┃      ┃      ┃  │
 │ ┡━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━┩  │
 │ │ lengt │     0 │    1 │   0.5 │ 0.36 │ 1.6e │  0.13 │ 0.86 │    1 │ █▃▃▃ │  │
 │ │ h     │       │      │       │      │  -06 │       │      │      │  ▄█  │  │
 │ │ width │     0 │    1 │     2 │  1.9 │ 0.00 │   0.6 │    3 │   14 │ █▃▁  │  │
 │ │       │       │      │       │      │   21 │       │      │      │      │  │
 │ │ depth │     0 │    1 │    10 │  3.2 │    2 │     8 │   12 │   20 │ ▁▄█▆ │  │
 │ │       │       │      │       │      │      │       │      │      │  ▃▁  │  │
 │ │ rnd   │   120 │ 0.88 │ -0.02 │    1 │ -2.8 │ -0.74 │ 0.66 │  3.7 │ ▁▄█▅ │  │
 │ │       │       │      │       │      │      │       │      │      │  ▁   │  │
 │ └───────┴───────┴──────┴───────┴──────┴──────┴───────┴──────┴──────┴──────┘  │
 │                                  category                                    │
 │ ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓  │
 │ ┃              ┃ missing     ┃ complete rate      ┃ ordered    ┃ unique   ┃  │
 │ ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩  │
 │ │ class        │           0 │                  1 │ False      │        2 │  │
 │ │ location     │           1 │                  1 │ False      │        5 │  │
 │ └──────────────┴─────────────┴────────────────────┴────────────┴──────────┘  │
 │                                  datetime                                    │
 │ ┏━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓  │
 │ ┃            ┃ missing ┃ complete   ┃ first      ┃ last       ┃ frequency ┃  │
 │ ┃            ┃         ┃ rate       ┃            ┃            ┃           ┃  │
 │ ┡━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩  │
 │ │ date       │       0 │          1 │ 2018-01-31 │ 2101-04-30 │ M         │  │
 │ │ date_no_fr │       3 │          1 │ 1992-01-05 │ 2023-03-04 │ None      │  │
 │ │ eq         │         │            │            │            │           │  │
 │ └────────────┴─────────┴────────────┴────────────┴────────────┴───────────┘  │
 │                                   string                                     │
 │ ┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓  │
 │ ┃        ┃ missing   ┃ complete rate    ┃ words per row    ┃ total words  ┃  │
 │ ┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩  │
 │ │ text   │         6 │             0.99 │              5.8 │         5800 │  │
 │ └────────┴───────────┴──────────────────┴──────────────────┴──────────────┘  │
 │                                    bool                                      │
 │ ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓  │
 │ ┃                      ┃ true       ┃ true rate           ┃ hist          ┃  │
 │ ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩  │
 │ │ booly_col            │        520 │                0.52 │    █    █     │  │
 │ └──────────────────────┴────────────┴─────────────────────┴───────────────┘  │
 ╰──────────────────────────────────── End ─────────────────────────────────────╯

 In [3]: df.describe()
 Out[3]:
             length        width        depth         rnd
 count  1000.000000  1000.000000  1000.000000  882.000000
 mean      0.501619     2.036549    10.024000   -0.019771
 std       0.359707     1.928640     3.208382    1.001654
 min       0.000002     0.002057     2.000000   -2.808934
 25%       0.134014     0.602987     8.000000   -0.735467
 50%       0.497570     1.467916    10.000000   -0.000774
 75%       0.860224     2.952881    12.000000    0.663878
 max       0.999999    13.908001    20.000000    3.716621

 In [4]:

```


## snapedautility
[snapedautility](https://pypi.org/project/snapedautility/) はデータセット全体を素早く分析し、視覚化された詳細なレポートを提供します。特徴量の迅速な分析、観測値からの外れ値の検出、その他のデータの特徴づけの作業を支援してくれます。

- `plot_histograms`　ー　数値、カテゴリ、テキスト特徴量の分布をプロットする
- `plot_corr`　ー　数値データ型（ピアソン相関），カテゴリデータ型（不確定係数），カテゴリ-数値データ型（相関比）に対して，すべてのデータ型に対してシームレスに相関プロットを作成する．
- `detect_outliers`　ー　データ上の他の観測値から逸脱している外れ値を示すバイオリンプロットを生成する


### インストール
snapedautility は次のようにインストールします。

```bash
 $ python -m pip install snaoedautility altair_viewer
```

altair_viewer はバックエンドの 可視化ライブラリAltair を表示させるためのもので、 IPython など Jupyter Notebook/Jupyterlab の環境でない場合に使用します。altair_viewer があれば作図を確認できるため、snapedautility は軽量であることが特徴のひとつになっています。

Jupyterlab の環境では次の拡張機能を有効にしておきます。

```bash
 $ python -m install vega
 $ jupyter labextension install @jupyterlab/vega5-extension
```


## plot_histograms で分布を調べる

```python
 In [2]: # %load c01_histgram.py
    ...: import pandas as pd
    ...: import altair as alt
    ...: from palmerpenguins import load_penguins
    ...: from snapedautility.plot_histograms import plot_histograms
    ...:
    ...: alt.renderers.enable('altair_viewer') # for IPython
    ...: # alt.renderers.enable('notebook')      # for Jupyterlab
    ...:
    ...: df = load_penguins()
    ...: chart = plot_histograms(df,
    ...:            ["bill_length_mm", "bill_depth_mm", 'species'],
    ...:            100, 100)
    ...: chart.show()
    ...:
 Out[2]: RendererRegistry.enable('altair_viewer')
 Displaying chart at http://localhost:18906/

 In [3]:
```

![](https://gyazo.com/827b7c7a619503f875bad3f1c46bc4a1.png)

## plot_corr で相関を調べる

```python
 In [2]: # %load c02_plot_coor.py
    ...: import pandas as pd
    ...: import altair as alt
    ...: from palmerpenguins import load_penguins
    ...: from snapedautility.plot_corr import plot_corr
    ...:
    ...: alt.renderers.enable('altair_viewer') # for IPython
    ...: # alt.renderers.enable('notebook')      # for Jupyterlab
    ...:
    ...: df = load_penguins()
    ...: chart = plot_corr(df,
    ...:            ["bill_length_mm", "bill_depth_mm", 'species'],
    ...:            100, 100)
    ...: chart.show()
    ...:
 Out[2]: RendererRegistry.enable('altair_viewer')
 Displaying chart at http://localhost:23611/

 In [3]:

```
![](https://gyazo.com/d0c24c5841ebe561f7deb78a8d756366.png)
## detect_outliers で外れ値を調べる

```python
 In [2]: # %load c03_detect_outlier.py
    ...: import pandas as pd
    ...: import altair as alt
    ...: from snapedautility.detect_outliers import detect_outliers
    ...:
    ...:
    ...: alt.renderers.enable('altair_viewer') # for IPython
    ...: # alt.renderers.enable('notebook')      # for Jupyterlab
    ...:
    ...: s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
    ...: data, chart = detect_outliers(s)
    ...:
    ...: chart.show()
    ...:
 Out[2]: RendererRegistry.enable('altair_viewer')
 Displaying chart at http://localhost:16094/

 In [3]: data
 Out[3]: [-8.0, 20.0]

 In [4]:

```


![](https://gyazo.com/414711a4766d4a3f391eaf9af26ddb7f.png)

# Pandas-Profiling
![](https://gyazo.com/a522e368c83e3fe54da7c08d5a67f866.png)

[Pandas-profiling](https://github.com/pandas-profiling/pandas-profiling) は、2016年から開発されているオープンソースのPythonモジュールで、わずか数行のコードで探索的データ分析を迅速に行うことができます。また、こ生成するレポートは、プログラミングを知らない人にも見せることができるインタラクティブなWeb形式のものです。pandas-profiling が出力するのはHTMLオブジェクトひとつだけです。ただし、そこには、より具体的で個別のデータ探索を行う前に知っておくべき情報がほとんど含まれていて、広範囲に構造化されたHTMLファイルで、JupyterlabやWebページに簡単に取り込むことができ共有も簡単です。

  - [Pandas-Profilingで探査的データ分析をしてみよう]()


## Sweetviz
![](https://gyazo.com/26524c0d359a737bea8b61ee34c21e46.png)
[Sweetviz](https://github.com/fbdesignpro/sweetviz) は、たった2行のコードで探索的データ分析(EDA）を始めるための美しく高密度な可視化レポートを作成するオープンソースのPythonライブラリです。出力は、完全に自己完結したHTMLアプリケーションになっています。
レポートは、目標値を素早く視覚化し、データセットを比較することもできます。ターゲットの特性、トレーニングデータとテストデータの比較、その他のデータ特性評価タスクの迅速な分析に役立つものとなっています。

Sweetviz では次の3種類のレポートを作成することができ、それぞれに対応した関数を呼び出します。

  - `analyze()` ー　与えたデータフレームに対してのEDAレポートを作成
  - `compare()` ー　2つの与えたデータフレームを比較したレポートを作成
  - `compare_intra()` ー　同じデータフレームの2つのサブセットを比較する（例：男性 vs 女性）

- [Sweetvizで探査的データ分析をしてみよう]()


## Lux
![](https://gyazo.com/6e41ac8eba279abb964e928c53275688.png)

[Lux](https://pypi.org/project/lux/) は、データを可視化するためのインテリジェントPython ライブラリです。探索的データ解析の可視化処理を自動化する Jjupyterウィジェットを通して視覚的発見が容易になります。

  - [Luxで探査的データ分析をしてみよう]()


## DataPrep
![](https://gyazo.com/d7a8e07643b2b549cea8c9f36f726680.png)
[DataPrep](https://github.com/sfu-db/dataprep)は、データを準備(prepare)するために2020年から開発が始まった　Pythonパッケージです。このパッケージには、主に以下の3つのAPIが含まれています。

  - データ探索( dataprep.eda )
  - データクリーニング( dataprep.clean )
  - データ収集( dataprep.connector )

DataPrepパッケージは、高速にデータ探索を行うことができるように設計されていて、PandasやDaskのDataFrameオブジェクトとうまく連携して動作します。データ探査ではHTMLオブジェクトを返すため、ブラウザやJupyterlab などで分析したり、情報を共有することができます。EDAでの計算処理をDaskで行っているため Pandas-Profileing と比較して5〜10倍高速で、メモリに乗り切らないような大規模データセットについても処理することができます。

- [DAtaPrep での分析サンプル https://docs.dataprep.ai/_downloads/1a61c6aebb3ecbe9dc9742bd6ca78ddb/titanic_dp.html]
- [DataPrepで探査的データ分析をしてみよう]()


## Pandas_UI
[Pandas_ui](https://github.com/arunnbaba/pandas_ui0 は、Jupyterlab と連携して、Pandas のユーザインタフェースを提供するパッケージです。
ソフトウェア構造としては非常にシンプルで、[pandas](https://pandas.pydata.org/)、[NumPy](https://numpy.org/)、[plotly](https://plotly.com/)、[ipywidgets](https://github.com/jupyter-widgets/ipywidgets)、[pandas_profiling](https://github.com/pandas-profiling/pandas-profiling)、[qgrid](https://github.com/quantopian/qgrid) などの優れたPythonライブラリの能力を利用して、ユーザーがPandas の操作や可視化のための操作をノーコードで実現することができます。

Pandas_uiの主な特徴と利点には次のようになります。

- データフレームに対して指定された操作を自動的に実行
  - コーディング時間を90％削減します
  - Pythonコードを生成して再利用が可能
- データフレームに対して独自の Python コードを適用できる
- 方法ではなく、やりたいことに集中できる
  - とにかく使いやすい
  - 使い方をネットで調べるようなことは不要
- Jupyter notebook との連携
  - 既存のノートへのシームレスな統合
- 最小限の学習コストで素早く使いこなせるようになる
- クラウドサービスではないため、すべてのデータは安全なまま

pandas_uiは、簡単な操作でデータを絞り込んで探索し、データを簡単に可視化することができるようになります。
Pandas_uiは、Pandas のデータフレームに対して指定された操作を自動的に実行し、同時にPythonコードを生成します。

  - [Pandas_uiを使ってデータを可視化しよう]()

# PandasGUI
[PandasGUI](https://pypi.org/project/pandasgui/) は、Pandas にグラフィカルユーザインタフェース(GUI) を提供するアプリケーションとライブラリで、マウスをクリックするだけでpandasのデータフレームにアクセスしたり、操作することができます。

次のような機能をもっています。

  - データフレームとシリーズの表示と並べ替え（マルチインデックス対応）
  - インタラクティブなグラフ描画
  - フィルタリング（クエリ式を使用することもOK)
  - １クリックでの統計概要
  - データ編集、コピー/ペースト
  - ドラッグ＆ドロップによるCSVファイルの読み込み
  - 検索ツールバー
  - Jupyter notebook / Jupyterlab との連携


PandasGUIには既にいくつかのサンプルデータセットが付属しています。Titanicデータセットを使ってみましょう。
コードは簡単です。

```python
 import pandas as pd
 from pandasgui import show
 from pandasgui.datasets import titanic

 gui = show(titanic)
```

PandasGUIのアプリケーションが起動して、初めの画面ではデータフレームの内容が表示されます。

![](https://gyazo.com/779246b609f1d3b3decd6bd0d0f92531.png)


![](https://gyazo.com/579faa30f3ef2c3264bef3d1ede0ef86.png)


    - [PandasGUIで探査的データ分析をしてみよう]()


## AutoViz
![](https://gyazo.com/169d1fc3235b9c3bde269e8aa9dc6d48.png)

小さなデータセットの可視化は簡単でそれほど問題になることはありませんが、数百の変数を持つ大規模なデータセットでは、データセットから強調すべき最良の特徴量を決定することはほぼ不可能です。データ分析を行う環境によっては、標準的でない可視化ライブラリを使用しなければならず、洞察を得るための最適な可視化を行うにはかなりのコーディングが必要となることが多いものです。
[Autoviz](https://pypi.org/project/autoviz/) は、データ可視化のための作業を行うときに発生する、こうしたさまざまな課題の多くに対処することができます。AutoViz は、pandasのDataFrameオブジェクトや、CSVファイルのいずれかを与える、たった1行のコードで実現することができます。

  - [AutoVizで探査的データ分析をしてみよう]()

# D-Table
![](https://gyazo.com/2fd4c1042c129e327d96fd9125a511d7.png)

Python自体の学習コストは低いものの、こうしたライブラリの学習は難しく、初心者にとっては使い方を覚えるのに時間がかかることがあります。経験豊かなPythonユーザーであっても、いくつかの作業は繰り返し行われることがあり、時間を浪費してしまうことになりがちです。こんなときに役立つのが [D-Tale](https://github.com/man-group/dtale)です。
D-Taleは探索的データ分析やデータクリーニングといったタスクの最適化を支援してくれます。時間を節約することで、コードの洗練や機械学習モデルのチューニングなど、より重要なタスクに集中することができます。

  - [D-Taleで探査的データ分析をしてみよう]()

# Bamboolib
[Bamboolib](https://pypi.org/project/bamboolib/)　は、Jupyter NotebookやJupyterLabで誰でもPythonを扱えるようにするためのpandas DataFramesのGUIです。2021年にDatabricks社がローコード/ノーコード開発企業の8080 Labsを買収したことで、一部の機能は有料化されましたが、ローカルコンピュータやBinder経由のOpen Dataでbamboolibを利用する場合は、無料で利用することができます。Databricks は 2020 年には Redash を買収しており、Redash による使いやすいダッシュボードおよび視覚化機能と、8080 Labs による bamboolib の統合によ、りデータサイエンティストを含む多くのユーザーがデータと AI を利活用しやすいプラットフォームを提供しています。

Bamboolib には次のような’特徴があります。

  - Pythonのコードを書き出す直感的なGUI
  - 一般的な変換や可視化をサポート
  - データ探索のためのベストプラクティス分析を提供する
  - シンプルなPythonプラグインによって任意にカスタマイズ可能
  - 内部・外部のあらゆるPythonライブラリを統合可能

bamboolib の主な利点には次のものがあります。

  - コードを書かずに誰でもPythonでデータ解析が可能
  - コードが書ける人でもbamboolibを使うことで、自分でコードを書くより早く簡単にできるようになる
  - 導入時間やトレーニングコストを削減できます。



# Visidata
![](https://gyazo.com/078c880aa72f2511d84c186b22d0d34f.png)

[Visidata](https://pypi.org/project/visidata/) は、コンピュータの端末でデータセットを素早く開き、探索し、要約し、分析することができる、無料のオープンソースツールです。VisiDataは、CSV/JSON/YAML/XMLファイル、Excelスプレッドシート、SQLデータベース、その他多くのデータソースをサポートしています。 Windows では [WSL](（Windows Subsystem for Linux） https://docs.microsoft.com/en-us/windows/wsl/) の環境が必要になります。

### インストール
visidata は次のようにインストールします。
```bash
 $ python -m pip install visidata
```

## 使用方法
vd コマンドが使用できるようになるので、引数にデータセットのファイル名を与えるだけです。

```bash
 $ vd titanic.csv
```

![](https://gyazo.com/e72005a1f9d571223bb9203c6a737728.png)

そうです、visidata はグラフィカルな環境ではなくあえてターミナル上でのデータ分析を目指しています。補助的なツールといえばそれまでですが、多くの機能をもっているため慣れるとコードを書く手間を省くことができます。
visidata のカーソルを移動するには、キーボードの `h`/`j`/`k`/`l` で左/下/上/右に移動させることができます。もちろんキーボードのカーソルキーでもOKです。

現在開いているシートを閉じるときは、`q` キーを押下します。visidata を終了するときは、`gq` を押下します。

操作はキーボードとマウスが使用できます。詳細は[キー操作の一覧](https://jsvine.github.io/visidata-cheat-sheet/en/) を参照してみてください。



# Mito
![](https://gyazo.com/52c5b4817376a77c63383cd7264b6925.png)

[Mito](https://www.trymito.io/) は Jupyterlab をベースにしたEDAアプリケーションです。次のような機能を提供しています。

  - ポイント＆クリックでCSVやXLSXをインポート
  - Excelスタイルのピボットテーブル
  - グラフ作成
  - フィルタリングとソート
  - マージ(ルックアップ)
  - エクセル形式の計算式
  - 列の要約統計
  - ユーザインタフェースでの操作のPythonコードを自動生成

Excelスタイルのピボットテーブは、膨大なデータを集計したり、分析したりできるExcelの機能です。このピボットテーブルを活用すれば、売上分析や勤怠管理などのデータのグラフ化など、面倒な作業が効率化されます。また、関数や数式を使わないのこともあり、Excel初心者にも使いやすい強力な機能で利用しているEXCELユーザも多いものです。
Python でも Pandas の `pivot_table()` 関数を使うと、Excelのピボットテーブル機能と同様の処理が実現できますが、PythonおよびPandasの知識が必要になり、Excelでのマウス操作だけでデータ分析/可視化といった利用方法ではありませんでした。
mito はユーザインタフェースで行った操作に該当するPythonコードを自動生成してくれるため、ExcelになれたPythonの初心者にも利用価値が高い優れたライブラリです。

  - [MitoでExcel データを処理してみよう]()


## ScatterText
[ScatterText](https://github.com/JasonKessler/scattertext) は、これまで紹介してきたEDAツールとは少し異なり文字列を対象にしています。scattertext はコーパスから特徴的な用語を見つけ出し、それをインタラクティブなHTML散布図に表示するツールです。

### インストール
scattertext は次のようにインストールします。

```bash
 $ python -m pip install scattertext
```


### 使用方法
次のコードはScattertextを使用して、2012年のアメリカの政治大会で使用された用語を視覚化するものです。

```python
 In [2]: # %load c01_demo.py
    ...: import scattertext as st
    ...:
    ...: df = st.SampleCorpora.ConventionData2012.get_data().assign(
    ...:         parse=lambda df: df.text.apply(st.whitespace_nlp_with_sentences)
    ...:
    ...:      )
    ...:
    ...: corpus = st.CorpusFromParsedDocuments(
    ...:     df, category_col='party', parsed_col='parse'
    ...: ).build().get_unigram_corpus().compact(st.AssociationCompactor(2000))
    ...:
    ...: html = st.produce_scattertext_explorer(
    ...:     corpus,
    ...:     category='democrat',
    ...:     category_name='Democratic',
    ...:     not_category_name='Republican',
    ...:     minimum_term_frequency=0,
    ...:     pmi_threshold_coefficient=0,
    ...:     width_in_pixels=1000,
    ...:     metadata=corpus.get_df()['speaker'],
    ...:     transform=st.Scalers.dense_rank
    ...: )
    ...: open('./demo_compact.html', 'w').write(html)
    ...:
 Out[2]: 1655720

 In [3]:

```

![](https://gyazo.com/9cdbeb6aec8996986c0da88acdc22dad.png)


最も政党に関連する2,000のユニグラム（Unigram: 任意の文字列が1文字だけ続いた文字列）が散布図に点として表示されます。X軸とY軸は、それぞれ共和党と民主党のスピーカーによって使用された頻度を表しています。

  - [Scattetext 2017 PyData Talk https://github.com/JasonKessler/Scattertext-PyData]


# Holoviz
![](https://gyazo.com/40a323195cca6965ca69c95f34425440.png)

[HoloViz](https://holoviz.org/) は、EDAのためのツールというわけではないのですが、可視化をより簡単に、より正確に、より強力にすることができます。 EDAで得た知見や洞察をプレゼンテーションするときに役立ちます。
HoloViz は次のPythonパッケージで構成されています。

  - Panel ー　プロットライブラリからアプリやダッシュボードを作る
  - HivPlot ー データからインタラクティブなプロットを素早く生成する
  - HoloViews ー　全てのデータを瞬時に可視化する
  - GeoView ー　地理データ用にHoloViewsを拡張する
  - Datashader  ー　最大のデータセットもレンダリングする
  - Param ー　宣言型のユーザ設定可能オブジェクトを作る
  - Colorcet ー 知覚的に均一なコロマップを作る
![](https://gyazo.com/2f09d7ead2e7b53f45efed6e9cf3ac1a.png)

  - [HoloViewsを使ってみよう]()


## OpenRefine
[OpenRefine](https://openrefine.org/)（以前はGoogle Refineとして知られていました）は、乱雑なデータのクリーニング、あるフォーマットを別のフォーマットへの変換、ウェブサービスや外部データとの拡張を行う強力なツールです。OpenRefineは、ローカルのコンピュータ上で小さなサーバを動作させ、それをウェブブラウザを使ってそのサーバと対話することで機能します。つまり、OpenRefineは、共有やコラボレーションをしたいと思うまで、データは常にローカルのコンピュータ上にあり非公開の状態にあります。



# まとめ

データを分析するための、すべてのデータセットとユーザに適した画一的な手法やツールは残連ながら存在しません。どのようなツールがEDAプロセスを快適で効率良いものにするかは、データとプロジェクトによって異なるためです。


## 余談
これはまったくの私見ですが、DataPrep と D-Tale, Visidata が好きです。理由は単に可視化だけでなくデータクリーニングなどでも重宝するからです。可視化そのものは HoloViz が秀逸。

# 参考
- snapedautility
  - [Pypi - snapedautility](https://pypi.org/project/snapedautility/)
  - [ソースコード](https://github.com/UBC-MDS/snapedautility]
  - [公式ドキュメント](https://snapedautility.readthedocs.io/en/latest/]
- Pandas-profilint
  - [PyPI - Pandas-profiling](https://github.com/pandas-profiling/pandas-profiling]
- DataPrep
  - [ソースコード]( https://github.com/sfu-db/dataprep]
- Sweetviz
  - [ソースコード](https://github.com/fbdesignpro/sweetviz]
- Lux
  - [PyPI - Lux](https://pypi.org/project/lux/]


- Visidata
  - [オフィシャルサイト](https://www.visidata.org/]
  - [PyPI - visidata](https://pypi.org/project/visidata/]
  - [公式ドキュメント](https://www.visidata.org/docs/]
  - [デモ動画](https://www.youtube.com/watch?v=N1CBDTgGtOU]

- Altair
  - [オフィシャルサイト](https://altair-viz.github.io/]
  - [PyPI - altair](https://pypi.org/project/altair/]

- OpenRefine
  - [オフィシャルサイト](https://openrefine.org/]
  - [公式ドキュメント](https://docs.openrefine.org/]
  - 書籍 Packt - [Using OpenRefine](https://www.packtpub.com/product/using-openrefine/9781783289080]

- PyViz.org
  - [PyViz.org](https://pyviz.org/dashboarding/index.html] Pythonでの可視化ツール/ライブラリを整理しているサイト

- Laggle
  - [Lean Pandas Tutorials](https://www.kaggle.com/learn/pandas]
- DataSchool
  - [100 pandas tricks to save you time and energy](https://www.dataschool.io/python-pandas-tips-and-tricks/]
- Klipfolio
  - [The Starter Guide to Data Visualizations](https://www.kaggle.com/learn/pandas]
- Qiita
  - [特徴量エンジニアリングおさらいメモ](https://qiita.com/takahashi_yukou/items/2b6d7776634ef55cec58]
- Python@Osaka
  - [学習に使えるデータソース]()


