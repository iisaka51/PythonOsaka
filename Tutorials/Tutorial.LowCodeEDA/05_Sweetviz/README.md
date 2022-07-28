Sweetvizで探査的データ分析をしてみよう
=================
![](https://gyazo.com/26524c0d359a737bea8b61ee34c21e46.png)

# はじめに
この使用は探索的データ分析(EDA）の支援ツール Sweetviz についてまとめたものです。

# Sweetvizについて
Sweetvizは、たった2行のコードで探索的データ分析(EDA）を始めるための美しく高密度な可視化レポートを作成するオープンソースのPythonライブラリです。出力は、完全に自己完結したHTMLアプリケーションになっています。
レポートは、目標値を素早く視覚化し、データセットを比較することもできます。ターゲットの特性、トレーニングデータとテストデータの比較、その他のデータ特性評価タスクの迅速な分析に役立つものとなっています。

Sweetviz では次の3種類のレポートを作成することができ、それぞれに対応した関数を呼び出します。

  -  `analyze()` ー　与えたデータフレームに対してのEDAレポートを作成
  -  `compare()` ー　2つの与えたデータフレームを比較したレポートを作成
  -  `compare_intra()` ー　同じデータフレームの2つのサブセットを比較する（例：男性 vs 女性）

## Analyze()


```
 In [2]: # %load c01_analyze.py
    ...: import sweetviz as sv
    ...: import pandas as pd
    ...:
    ...: train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')
    ...:
    ...: report = sv.analyze([train_df,'Train'],
    ...:                     target_feat='Survived')
    ...:
    ...: report.show_html(filepath='Titanic_EDA.html',
    ...:                  layout='vertical', scale=1.0)
    ...: # or
    ...: # report.show_notebook()
    ...:
 Feature: SibSp                               |▌| [ 54%]   00:03 -> (00:03 left)/Users/goichiiisaka/anaconda3/envs/EDA/lib/python3.1/site-packages/sweetviz/utils.py:34: FutureWarning: The series.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
   clamped_series = clamped_series.append(other_series, ignore_index=False)
   (以下略）
   
```

このコードを実行すると指定したファイル名のレポートがカレントディレクトリに作成され、ブラウザが開いてレポートを表示します。


![](https://gyazo.com/07f1bb13b7b1226f4a91ca7ad55f91ae.png)
ページトップにある [# Associations] をクリックすると、アソシエーション分析（association analysis）の結果が表示されます。これは、データの中から統計的なパターンや意味のある関連性を抽出したものです。


![](https://gyazo.com/62b6c09001eb70fb5629e7a37e36054e.png)

ここで、表示される正方形のマークは `0` から `1` までのカテゴリ的な関連性（不確実性係数と相関比）を表しています。
丸形のマークは- `1` から `1` までの対称的な数値相関を表しています。
データの属性をクリックすると、その詳細なレポートが表示されます。


![](https://gyazo.com/e46896eed9113a9e759c2370aa7e0c68.png)
 `show_html()` に  `layout='wide` （デフォルト）を与えると展開されるのではなく、右側のスペースに詳細情報が配置されます。

HTML形式で保存されたレポートはブラウザがあれば内容を参照できるため、メール送付した相手側に特別なアプリケーションは不要です。

## compare_intra()
データセットを2つの部分集団に分割することで、データから洞察を得ることがあります。 `compare_intra()` はこのような目的のときに使用します。この関数は、データフレームとブール値のSeriesオブジェクトを与えます。さらに結果のデータセットに (true, false) の名前をつけるための明示的な  `names` 引数も与えることができます。内部的には、この関数は結果の各グループを表すために2つの別々のデータフレームを作成することに注意してください。


```
 In [5]: # %load c02_compare_intra.py
    ...: import sweetviz as sv
    ...: import pandas as pd
    ...:
    ...: train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')
    ...:
    ...: report = sv.compare_intra(train_df,
    ...:                           train_df["Sex"] == "male",
    ...:                           ["Male", "Female"])
    ...:
    ...: report.show_html(filepath='Titanic_Comp_Intra.html',
    ...:                  layout='vertical', scale=1.0)
    ...: # or
    ...: # report.show_notebook()
 Feature: SibSp                               |▌| [ 54%]   00:03 -> (00:03 left)/Users/goichiiisaka/anaconda3/envs/EDA/lib/python3.1/site-packages/sweetviz/utils.py:34: FutureWarning: The series.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
   clamped_series = clamped_series.append(other_series, ignore_index=False)
 (以下略)
 
```


![](https://gyazo.com/ccd8faa4448761363935d91d73eb4b6e.png)

![](https://gyazo.com/7b0d71ca6c4d3f04e499b4d6f561e654.png)


## compare()
Sweetvizz の特徴のひとつにデータセットの比較部分析ができることがあります。これは、 `compare()` 関数を呼び出すだけです。パラメータは  `analyze()` と同じですが、比較対象のデータフレームを表す2番目のパラメータが挿入されています。ベースとなるデータフレームと比較されるデータフレームを区別するために、 `[dataframe, "name"]` という形式のパラメータを使用することが推奨されています。



```
 In [2]: # %load c01_sweetviz_demo.py
    ...: import sweetviz as sv
    ...: import pandas as pd
    ...:
    ...: train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')
    ...: test_df = pd.read_csv('http://cooltiming.com/SV/test.csv')
    ...:
    ...: report = sv.compare([train_df,'Train'],
    ...:                     [test_df,'Test'],
    ...:                     target_feat='Survived')
    ...:
    ...: report.show_html(layout='vertical', scale=1.0)
    ...: # or
    ...: # report.show_notebook()
    ...:
 Feature: SibSp                               |▌| [ 54%]   00:04 -> (00:04 left)/Users/goichiiisaka/anaconda3/envs/EDA/lib/python3.1/site-packages/sweetviz/utils.py:34: FutureWarning: The series.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
   (以下略）
   
```


![](https://gyazo.com/baccd3430575243b8df3552883a21711.png)
属性別に表示されるので、クリックすると詳細な情報が表示されまう。

![](https://gyazo.com/b539ca3ed3bcdce21749a53598f48d76.png)

## デフォルトのカスタマイズ：設定ファイル
Sweetvizz はINIファイルに記述された設定情報を読み込むことできます。レポートを作成する前にこれを呼び出すことで、任意の設定をオーバーライドすることができます。

 config.ini
```
 [General]
 use_cjk_font = 1
 
 [Layout]
 show_logo = 0
 
 Output_Defaults]
 html_layout = widescreen
 html_scale = 1.0
 notebook_layout = vertical
 notebook_scale = 0.9
 notebook_width = 100%%
 notebook_height = 700
```

この設定ファイルでパーセント記号( `%` )を記述するため2つ記述していることに注意してください。これはINIフォーマットの仕様で `%` にはマクロ展開の意味があるためです。
設定ファイルを読み込むためには、はじめに次の1行を呼び出しておくだけです。


```
 sv.config_parser.read('config.ini')
```

これ以降は、 `show_html()` や  `show_notebook()` のたびに引数を与える必要が’なくなります。


```
 n [2]: # %load c04_config.py
    ...: import sweetviz as sv
    ...: import pandas as pd
    ...:
    ...: train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')
    ...:
    ...: sv.config_parser.read('config.ini')
    ...: report = sv.analyze([train_df,'Train'],
    ...:                     target_feat='Survived')
    ...:
    ...: # or
    ...: # report.show_notebook()
    ...:
 Out[2]: ['config.ini']
 Feature: SibSp                               |▌| [ 54%]   00:03 -> (00:03 left)/Users/goichiiisaka/anaconda3/envs/EDA/lib/python3.1/site-packages/sweetviz/utils.py:34: FutureWarning: The series.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
 (以下略）
   
```



# まとめ

SweetvizはEDAに注力したツールです。データセットの欠損などにも柔軟で簡単にレポートを作成することができるため、ベン席に集中することができます。また、分析プロセスの後半、例えば特徴量の生成中に、新しい特徴量がどのように作用するかを素早く概観するのときにも有益なツールとなります。



# 参考
- Sweetviz
  - [PyPI - serrtviz ](https://pypi.org/project/sweetviz/)
  - [ソースコード ](https://github.com/fbdesignpro/sweetviz)
  - [Powerful EDA (Exploratory Data Analysis) in just two lines of code using Sweetviz ](https://towardsdatascience.com/powerful-eda-exploratory-data-analysis-in-just-two-lines-of-code-using-sweetviz-6c943d32f34) ー　開発者による解説記事
- PythonOsaka
  - [学習に使えるデータソース]

#EDA


