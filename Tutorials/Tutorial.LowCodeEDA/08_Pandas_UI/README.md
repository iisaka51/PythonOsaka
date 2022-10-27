Pandas_uiを使ってデータを可視化しよう
=================
## Pandas_ui について
[Pandas_ui ](https://github.com/arunnbaba/pandas_ui) は、Arunn Thangavel氏がbamboolib が商業サービスに移行したときに、そのサービスにインスピレーションを得てオープンソースとして開発したものです。
ソフトウェア構造としては非常にシンプルで、[pandas https://pandas.pydata.org/]、[NumPy https://numpy.org/]、[plotly https://plotly.com/]、[ipywidgets https://github.com/jupyter-widgets/ipywidgets]、[pandas_profiling https://github.com/pandas-profiling/pandas-profiling]、[qgrid ](https://github.com/quantopian/qgrid)などの優れたPythonライブラリの能力を利用して、ユーザーがPandas の操作や可視化のための効率的な方法を提供する拡張モジュールです。

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

## Pandas_ui の対象者
簡単に使えるツールですが高機能でもあるため、初心者ユーザーから上級ユーザーまで使用することができるツールです。 Pandas_uiは、データサイエンティストやデータアナリストがデータ前処理にかかる時間を短縮するように設計されています。
Python と Pandas の初心者には強くお勧めします。

## インストール
pandas_ui は次の手順でインストールします。

 zsh
```
 % git clone https://github.com/iisaka51/pandas_ui.git
 % cd pandas_ui
 % python setup.py install
```

これで qgrid などの依存関係のあるモジュールも一緒にインストールされます。
Jupyter notebook に関連モジュールを有効にするために、以下を実行します。

 zsh
```
 % jupyter nbextension enable --py qgrid
 % jupyter nbextension enable --py widgetsnbextension
```

Jupyter notebook を開いて、コードセルに次のコードを入力して実行します。
  python
```
 from pandas_ui import *
 pandas_ui('csv_file_path_here')
```

これで指定したCSVファイルのデータを検証できるようになります。
![](images/sp500_csv.png)


このあとデータフレームを参照するためには次のコードで処理できます。


```
 get_df()        # データフレームの取得
 get_meltdf()    # Meltデータフレームの取得（もしあれば）
 get_pivotdf()   # Pivotデータフレームの取得（もしあれば）
```

Meltデータフレームは Pandas の [melt()関数 ](https://pandas.pydata.org/docs/reference/api/pandas.melt.html) で処理したデータフレームです。
 `melt()` 関数は次のようなことが出来ます。

- データの列を id_vars, variable, value の3つの集合に分ける。
- id_vars に指定した列はそのまま
- values_vars に指定した列名はデータとして扱われ、variable列に格納される
- variable列の名前はvar_nameで変更する
- value_vars に入っていたデータが、value列に格納され、アンピボットされる
- value列の名前はvalue_nameで変更する

Pivotデータフレームは Pandas の [pivot()関数 ](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html) で処理したデータフレームです。
インデックスラベル、カラムラベル、データ部分の3つを個別に指定して新たなDataFrameを作成してくれます

## 具体的に見てみよう
はじめに、次のコードをセルに入力して実行してTITANICの乗客リストを取得します。

```
 import pandas as pd

 train_df = pd.read_csv('http://cooltiming.com/SV/train.csv')
 train_df.to_csv('titanic.csv')
```

このデータセットでは次のフィールドがあります。
- PassengerId：乗客者ID
- pclass： 旅客クラス /  1＝1等、2＝2等、3＝3等
- name： 乗客の名前
- sex： 性別/ male＝男性、female＝女性
- age： 年齢。一部の乳児は小数値
- sibsp： タイタニック号に同乗している兄弟（Siblings）や配偶者（Spouses）の数
- parch： タイタニック号に同乗している親（Parents）や子供（Children）の数
- ticket： チケット番号
- fare： 旅客運賃
- cabin： 客室番号
- embarked： 出港地 /  C＝Cherbourg、Q＝Queenstown、S＝Southampton
- boat： 救命ボート番号
- body： 遺体収容時の識別番号
- home.dest： 自宅または目的地
- survived：生存状況 / 0＝死亡、1＝生存

pandas_ui に読み込ませるためには次の２行を実行するだけです。

```
 import pandas_ui import *
 pandas_ui('titanic.csv')
```

これによりデータフレームにインタラクティブに参照できるようになります。
![](images/titanic_csv.png)

### PandasProfile
出力されたUIの  `PandasProfiling` をクリックします。
![](images/pandasprofile.png)
 `Get_Profile` をクリックすると、データフレームをパースして基本的なデータ分析を処理してくれます。
![](images/profile_overview.png)

![](images/profile_variable.png)
![](images/profile_iteractions.png)

![](images/profile_correlations.png)

![](images/profile_missing_values.png)
![](images/profile_sample_first_rows.png)
![](images/profile_sample_last_rows.png)

#### Varialbles
ヒストグラムチャートが表示されます。
![](images/variables.png)


### Pandas の操作
多くのPandasの処理が数回クリックするだけで行えます。

- **Set/Update variables** ボタンをクリック
- **Column :** のプルダウンメニューから  `Passengerid` を選択（このメニューはデータ依存です）
- **Operation:** のプラダンメニューから  `Update table value` を選択
- **Column:** を  `Passengerid` 、**Condaition** を  `<` 、 **Selected** を  `10`
- **Execute** をクリック
![](images/pandas_operation_exec.png)



Pandasのカラムを探索し、操作を実行することもできます。
- **Column :** のプルダウンメニューから  `Passengerid` を選択（このメニューはデータ依存です）
- **Select** ボタンをクリック

![](images/pandas_operation_columns.png)

### データフレームに Python コードを適用
pandas_ui から pandas のデータフレームに対して Python コードを適用することができます。
 `df` は pandas_ui が内部で保持しているデータフレームのことです。

- **Add Python Code** をクリック
![](images/add_python_code.png)

### Pandas_ui で操作したデータフレームを取り出す
pandas_ui で操作したデータフレームを取り出したい場合は、
次の関数を実行します。

-  `get_df()` ：pandas_ui からデータフレームを取り出す
-  `get_meltdf()` ：pandas_ui で melt()関数を処理した場合、そのデータフレームを取り出す
-  `get_pivotdf()` ：pandas_ui で pivot()関数を処理した場合、そのデータフレームを取り出す

### 履歴
Pandas_ui の最も強力な機能の1つは履歴(History)です。これにより、生成されたpython-pandasコードでアクションを元に戻したり、再実行したり、後で再利用するためにコードを保存できます。

- **DataFrame**タブにある、**History**ボタンをクリック

![](images/history.png)

### データの探索
手間をかけずに強力なデータ可視化することができ、後で再利用するためにコードをコピーできます。

- Pandas_ui の出力から **Explore** をクリック
- **Figure Type** のプルダウンメニューから  `scatter` を選択して **Choose** ボタンをクリック
- **scatt_x** を  `Passengerid` **scatt_y** を  `Age` にセット
- **Plot** をクリック

![](images/explore.png)

これで散布図とそれを表示させるために Python コードが表示されます。
表示のためにはバックエンドで 可視化モジュール Plotly が使われているため、拡大/縮小/移動などのインタラクティブな操作や画像としてセーブすることができます。

![](images/plot_scatter.png)

３D散布図を表示してみます。

- **Figure Type** のプルダウンメニューから  `scatter_3d` を選択して **Choose** ボタンをクリック
- **scatt_x** を  `Passengerid` **scatt_y** を  `Age` **scatt_z** を  `Fare` にセット
- **scatt3_color** を  `Pclass` にセット
- **Plot** をクリック
![](images/explore_3dscatter_setting.png)

![](images/explore_3dscatter.png)

### サポートしているグラフの種類
pandas_ui でサポートしているグラフは次のとおりです。

- scatter：散布図
- box：箱ひげ図
- violin：ヴァイオリン図
- histogram：ヒストグラム
- strip：ストリップ図
- density_heatmap：密度ヒートマップ
- density_contour：密度分布図
- area：面グラフ
- scatter_3d：３D散布図
- line_3d：3D折れ線グラフ
- scatter_matrix：散布図行列
- parallel_coordinates：平行座標
- parallel_categories：カテゴリを指定した並行座標

### pandas_ui とplotyの位置づけ
pandas_ui はバックエンドで[Plotly ](https://plotly.com/) を使うことデータフレームを可視化しています。直接 plotly を利用する方が多彩な可視化を行うことができますが、データ分析では色々な視点でデータを観察や評価考察を行うため、可視化についても何度も種類を変えて再描画する場合が多くなりがちなことに注目するべきでしょう。大事なことは、データの分析と考察であって、どれだけ美しい可視化ができるかに時間を費やすことではないはずです。 pandas_ui では2回から数回程度のクリック操作でデータフレームを操作、加工、可視化することができます。
そのため、分析を進めたあと、プレゼンテーションする段階で plotly を使用する方がよいでしょう。
ここでは、plotly オフィシャルサイトからグラフとそのコードを例示しておきます。

#### scatter：散布図

```
 import plotly.express as px
 fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
 fig.show()
```
![](images/example_scatter.png)
#### box：箱ひげ図

```
 import plotly.express as px
 df = px.data.tips()
 fig = px.box(df, y="total_bill")
 fig.show()
```
![](images/example_box.png)
#### violin：ヴァイオリン図

```
 import plotly.express as px

 df = px.data.tips()
 fig = px.violin(df, y="total_bill")
 fig.show()
```
![](images/example_violin.png)
#### histogram：ヒストグラム

```
 import plotly.express as px
 df = px.data.tips()
 fig = px.histogram(df, x="total_bill")
 fig.show()
```
![](images/example_histgram.png)

#### strip：ストリップ図

```
 import plotly.express as px
 df = px.data.tips()
 fig = px.strip(df, x="total_bill", y="day")
 fig.show()
```
![](images/example_strip.png)

#### density_heatmap：密度ヒートマップ

```
 import plotly.express as px
 fig = px.imshow([[1, 20, 30],
                  [20, 1, 60],
                  [30, 60, 1]])
 fig.show()
```
![](images/example_heatmap.png)

#### density_contour：密度分布図

```
 import plotly.express as px
 df = px.data.tips()

 fig = px.density_contour(df, x="total_bill", y="tip")
 fig.show()
```
![](images/example_densty_contour.png)


#### area：面グラフ

```
 import plotly.express as px
 df = px.data.gapminder()
 fig = px.area(df, x="year", y="pop", color="continent",
 	      line_group="country")
 fig.show()
```
![](images/example_area.png)

#### scatter_3d：３D散布図

```
 import plotly.express as px
 df = px.data.iris()
 fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
               color='species')
 fig.show()
```
![](images/example_scatter3d.png)

#### line_3d：3D折れ線グラフ

```
 import plotly.express as px
 import plotly.express as px
 df = px.data.gapminder().query("country=='Brazil'")
 fig = px.line_3d(df, x="gdpPercap", y="pop", z="year")
 fig.show()
```
![](images/example_line3d.png)
#### scatter_matrix：散布図行列

```
 import plotly.express as px
 df = px.data.iris()
 fig = px.scatter_matrix(df)
 fig.show()
```
![](images/example_scatter_matrix.png)

#### parallel_coordinates：平行座標

```
 import plotly.express as px
 df = px.data.iris()
 fig = px.parallel_coordinates(df, color="species_id", labels={"species_id": "Species",
                 "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                 "petal_width": "Petal Width", "petal_length": "Petal Length", },
                              color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)
 fig.show()
```
![](images/example_parallel_coordinates.png)

#### parallel_categories：カテゴリを指定した並行座標

```
 import plotly.express as px

 df = px.data.tips()
 fig = px.parallel_categories(df)

 fig.show()
```
![](images/example_parallel_categories.png)


## まとめ

Pandas のデータフレームからダッシュボードで可視化するためツールはいつくかありますが、
Pandas の操作をUIから行えて、Python コードを実行してデータフレームに適用することができるこのツールの利便性は非常に高いと考えています。
個人的にはソフトウェアがシンプル過ぎて力技で記述されているのが少し残念ですが、オープンソースであるので、利用者がアイデアやコードを改版して皆で育てていくものだと理解しています。

### 参考
- [pandas_ui ソースコード ](https://github.com/arunnbaba/pandas_ui)



