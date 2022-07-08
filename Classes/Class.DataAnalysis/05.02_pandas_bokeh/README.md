pandas-bokehを使ってみよう
=================
### bokehについて
bokeh はインタラクティブなグラフを描画できる拡張モジュールです。

 boke_sample.py
```
 from bokeh.plotting import figure, output_file, show
 
 x = [1, 2, 3, 4, 5]
 y = [6, 7, 2, 4, 5]
 
 output_file("lines.html")
 p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
 p.line(x, y, legend_label="Temp.", line_width=2)
 show(p)
```


 Ipython
```
 In [2]: # %load bokeh_sample.py 
    ...: from bokeh.plotting import figure, output_file, show 
    ...:  
    ...: x = [1, 2, 3, 4, 5] 
    ...: y = [6, 7, 2, 4, 5] 
    ...:  
    ...: output_file("lines.html") 
    ...:  
    ...: p = figure(title="simple line example", 
    ...:            x_axis_label='x', y_axis_label='y') 
    ...: p.line(x, y, legend_label="Temp.", line_width=2) 
    ...: show(p) 
```
まず、 `figure()` でグラフ領域をつくり、そこに `line()` を引き、 `show()` で描画するという手順でグラフを描画します。

![](https://gyazo.com/616fbecf578159a535a73839b0e0a413.png)

Bokeh では次のようなインタラクティブな描画機能が提供されています。

- ズームイン/ズームアウト可能
- 凡例をクリックすると、個々の線をオン/オフが可能（非表示にできる）
- プロットされた線のホバーツール（マウスでなぞるとデータ値を参照できる）
- スライドバーで変数を変化させた動的なグラフの描画


### インストール
拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install bokeh
 bash pipの場合
```
 $ pip install bokeh
```

### bokeh のサンプルデータセット
bokeh にはサンプル用のデータセットがあります。
利用するためにはあらかじめダウンロードしておく必要があります。
 IPython
```
 In [1]: import bokeh                                                       In [2]: bokeh.sampledata.download()                                               
 Creating /Users/goichiiisaka/.bokeh directory
 Creating /Users/goichiiisaka/.bokeh/data directory
 Using data directory: /Users/goichiiisaka/.bokeh/data
 Downloading: CGM.csv (1589982 bytes)
    1589982 [100.00%]
 Downloading: US_Counties.zip (3171836 bytes)
    3171836 [100.00%]
 Unpacking: US_Counties.csv
 Downloading: us_cities.json (713565 bytes)
     713565 [100.00%]
 Downloading: unemployment09.csv (253301 bytes)
     253301 [100.00%]
 Downloading: AAPL.csv (166698 bytes)
     166698 [100.00%]
 Downloading: FB.csv (9706 bytes)
       9706 [100.00%]
 Downloading: GOOG.csv (113894 bytes)
     113894 [100.00%]
 Downloading: IBM.csv (165625 bytes)
     165625 [100.00%]
 Downloading: MSFT.csv (161614 bytes)
     161614 [100.00%]
 Downloading: WPP2012_SA_DB03_POPULATION_QUINQUENNIAL.zip (4816256 bytes)
    4816256 [100.00%]
 Unpacking: WPP2012_SA_DB03_POPULATION_QUINQUENNIAL.csv
 Downloading: gapminder_fertility.csv (64346 bytes)
      64346 [100.00%]
 Downloading: gapminder_population.csv (94509 bytes)
      94509 [100.00%]
 Downloading: gapminder_life_expectancy.csv (73243 bytes)
      73243 [100.00%]
 Downloading: gapminder_regions.csv (7781 bytes)
       7781 [100.00%]
 Downloading: world_cities.zip (645274 bytes)
     645274 [100.00%]
 Unpacking: world_cities.csv
 Downloading: airports.json (6373 bytes)
       6373 [100.00%]
 Downloading: movies.db.zip (5053420 bytes)
    5053420 [100.00%]
 Unpacking: movies.db
 Downloading: airports.csv (203190 bytes)
     203190 [100.00%]
 Downloading: routes.csv (377280 bytes)
     377280 [100.00%]
 Downloading: haarcascade_frontalface_default.xml (930127 bytes)
     930127 [100.00%]
 
```

Linux系プラットフォームでは、 `$HOME/.bokeh/data/` 以下に保存されています。
 bash
```
 $ ls $HOME/.bokeh/data
 AAPL.csv
 CGM.csv
 FB.csv
 GOOG.csv
 IBM.csv
 MSFT.csv
 US_Counties.csv
 WPP2012_SA_DB03_POPULATION_QUINQUENNIAL.csv
 airports.csv
 airports.json
 gapminder_fertility.csv
 gapminder_life_expectancy.csv
 gapminder_population.csv
 gapminder_regions.csv
 haarcascade_frontalface_default.xml
 movies.db
 routes.csv
 unemployment09.csv
 us_cities.json
 world_cities.csv
```

### pandas-bokehについて

pandas がデータフレームから `plot()` メソッドを呼び出すだけで簡単にグラフを描画できるのに比べると、bokeh を単独で使った場合は、それなりにコードを記述しないと目的のグラフを描画できません。
この不満を解消するものが、pandas-bokeh です。このモジュールはpandasのデータフレームから簡単に bokeh をバックエンドとしたグラフを描画できるようになります。


### インストール
拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install pandas-bokeh
 bash pipの場合
```
 $ pip install pandas-bokeh
```


### pandas-bokeh の利用準備

次のようにモジュールをロードしておきます。
 IPython
```
 import pandas as pd
 import pandas_bokeh
```

Jupyter Notebook を使用している場合は、次のように出力先をノートブックしておきます。

```
  pandas_bokeh.output_notebook()
```

次のようにすると出力先をファイルにすることができます。
それ以降でプロットしたときにブラウザに表示されます。

```
  pandas_bokeh.output_file("output.html")
```


### pandas-bokeh でプロット
"[pandasでデータをプロットしてみよう]"でプロットしたグラフを pandas-bokeh を使って描画してみましょう。

 pandas_csv_readfromurl.py
```
 import pandas as pd
 
 baseurl = 'https://raw.githubusercontent.com/mwaskom/seaborn-data'
 url = baseurl + '/master/iris.csv'
 df = pd.read_csv(url)
```

 IPython
```
 In [2]: # %load pandas_csv_readfromurl.py 
    ...: import pandas as pd 
    ...:  
    ...: baseurl = 'https://github.com/pandas-dev/pandas/raw/master/pandas' 
    ...: url = baseurl + '/tests/data/iris.csv' 
    ...: df = pd.read_csv(url) 
    ...:                                                                           
 In [3]: import pandas_bokeh                                                In [4]: df.plot_bokeh()         
```

データフレームオブジェクトの `plot()` メソッドに変えて  `plot_bokeh()` メソッドを呼び出すだけです。

![](https://gyazo.com/ec36175fa802652a73852a818a3c2fde.png)

### バックエンドを pandas-bokeh に切り替える

次のようにバックエンドを pandas-bokeh に切り替えておくと、以後はデータフレームの `plot()` メソッドを `pands_bokeh()` に書き換える必要がありません。
 IPython
```
 import pandas as pd
 import pandas_bokeh
 pd.set_option('plotting.backend', 'pandas_bokeh')
```

### プロットタイプ
pandas-bokeh では次のタイプのグラフを描画できます。
 `plot_bokeh(kind="line")` と実行すると、lineplot を描画します。
これは、 `plot_bokeh.line()` と呼び出すことと同じです。

 pandas-bokeh の描画タイプの一覧

| ドキュメント表記 | method | kind | 説明 |
|:--|:--|:--|:--|
| lineplot | line() | line | 折れ線グラフ |
| pointplot | point() | point | ドット |
| stepplot | step() | step | ステップ図 |
| scatterplot | scatter() | scatter | 散布図 |
| barplot | bar() | bar | 棒グラフ |
| barplot | barh() | barh | 積み上げ棒グラフ |
| histogram | hist() | hist | ヒストグラム |
| areaplot | area() | area | 面グラフ |
| pieplot | pie() | pie | 円グラフ |
| mapplot | map() | map | 地図 |

pandas-boken の[ドキュメントに例示 ](https://github.com/PatrikHlobil/Pandas-Bokeh) されているグラフ描画のサンプルをみてみましょう。

### lineplot - ライングラフ

乱数を使って作成したダミーデータを折れ線グラフでプロットしてみます。
 bokeh_line.py 
```
 import numpy as np
 import pandas as pd
 import pandas_bokeh
 
 np.random.seed(42)
 df = pd.DataFrame({"Google": np.random.randn(1000)+0.2,
                    "Apple": np.random.randn(1000)+0.17},
                    index=pd.date_range('1/1/2000', periods=1000))
 df = df.cumsum()
 df = df + 50
 df.plot_bokeh(kind="line")
 
```

 IPython
```
 In [2]: # %load bokeh_line.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: np.random.seed(42) 
    ...: df = pd.DataFrame({"Google": np.random.randn(1000)+0.2, 
    ...:                    "Apple": np.random.randn(1000)+0.17}, 
    ...:                    index=pd.date_range('1/1/2000', periods=1000)) 
    ...: df = df.cumsum() 
    ...: df = df + 50 
    ...: df.plot_bokeh(kind="line") 
    ...:                                                                    
```

![](https://gyazo.com/05069b5acbcadbe3e471bd021559d963.png)
この資料ではキャプチャーした画像となっていますが、
ブラウザで表示されるグラフでは右側のメニューをマウスで操作したり、
カーソルをプロットされるラインに重ねてそのポイントでの値を見ることができます。

### lineplot - 時系列グラフ
乱数を使って作成したダミーデータを使って時系列グラフをプロットしてみます。

 bokeh_line_timeseries.py
```
 import numpy as np
 import pandas as pd
 import pandas_bokeh
 
 ts = pd.Series(np.random.randn(1000),
                index=pd.date_range('1/1/2000', periods=1000))
 df = pd.DataFrame(np.random.randn(1000, 4),
                index=ts.index, columns=list('ABCD'))
 
 df = df.cumsum()
 df.plot_bokeh(rangetool=True)
```


 IPython
```
 In [2]: # %load bokeh_line_timeseries.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: ts = pd.Series(np.random.randn(1000), 
    ...:                index=pd.date_range('1/1/2000', periods=1000)) 
    ...: df = pd.DataFrame(np.random.randn(1000, 4), 
    ...:                index=ts.index, columns=list('ABCD')) 
    ...:  
    ...: df = df.cumsum() 
    ...: df.plot_bokeh(rangetool=True) 
    ...:                                                                           
 Out[2]: Column(id='1202', ...)
```


![](https://gyazo.com/b7e3c8ad2f9fab118c56a5785042c2f4.png)


### pointplot - ポイントグラフ
lineplot とよく似ていますが、ラインの代わりにポイントをマーカーで印ていきます。

 bokeh_point.py
```
 import numpy as np
 import pandas as pd
 import pandas_bokeh
 
 x = np.arange(-3, 3, 0.1)
 y2 = x**2
 y3 = x**3
 df = pd.DataFrame({"x": x, "Parabula": y2, "Cube": y3})
 df.plot_bokeh.point(
     x="x",
     xticks=range(-3, 4),
     size=5,
     colormap=["#009933", "#ff3399"],
     title="Pointplot (Parabula vs. Cube)",
     marker="x")
```


 IPython
```
 In [2]: # %load bokeh_point.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: x = np.arange(-3, 3, 0.1) 
    ...: y2 = x**2 
    ...: y3 = x**3 
    ...: df = pd.DataFrame({"x": x, "Parabula": y2, "Cube": y3}) 
    ...: df.plot_bokeh.point( 
    ...:     x="x", 
    ...:     xticks=range(-3, 4), 
    ...:     size=5, 
    ...:     colormap=["#009933", "#ff3399"], 
    ...:     title="Pointplot (Parabula vs. Cube)", 
    ...:     marker="x") 
    ...:                                                                           
 Out[2]: Figure(id='1001', ...)
```
![](https://gyazo.com/e808ca14d4c9942e2290020ee612244b.png)
pointplot ではマーカー（ポイントの形状)には次のものが指定できます
- circle
- square
- triangle
- asterisk
- circle_x
- square_x
- inverted_triangle
 x
- circle_cross
- square_cross
- diamond
- cross

### stepplot ステップ図

 bokeh_stepplot.py
```
 import numpy as np
 import pandas as pd
 import pandas_bokeh
 
 
 x = np.arange(-3, 3, 1)
 y2 = x**2
 y3 = x**3
 df = pd.DataFrame({"x": x, "Parabula": y2, "Cube": y3})
 df.plot_bokeh.step(
     x="x",
     xticks=range(-1, 1),
     colormap=["#009933", "#ff3399"],
     title="Stepplot (Parabula vs. Cube)",
     figsize=(800,300)
     )
 df.plot_bokeh.step(
     x="x",
     xticks=range(-1, 1),
     colormap=["#009933", "#ff3399"],
     title="Stepplot (Parabula vs. Cube)",
     mode="after",
     figsize=(800,300)
     )
```

 IPython
```
 In [1]: %load bokeh_stepplot.py                                               ...: import pandas_bokeh 
    ...:  
    ...: x = np.arange(-3, 3, 1) 
    ...: y2 = x**2 
    ...: y3 = x**3 
    ...: df = pd.DataFrame({"x": x, "Parabula": y2, "Cube": y3}) 
    ...: df.plot_bokeh.step( 
    ...:     x="x", 
    ...:     xticks=range(-1, 1), 
    ...:     colormap=["#009933", "#ff3399"], 
    ...:     title="Stepplot (Parabula vs. Cube)", 
    ...:     figsize=(800,300) 
    ...:     ) 
    ...:  
    ...: df.plot_bokeh.step( 
    ...:     x="x", 
    ...:     xticks=range(-1, 1), 
    ...:     colormap=["#009933", "#ff3399"], 
    ...:     title="Stepplot (Parabula vs. Cube)", 
    ...:     mode="after", 
    ...:     figsize=(800,300) 
    ...:     ) 
    ...:                                                                           
 Out[2]: Figure(id='1178', ...)
```

![](https://gyazo.com/8e293d1d041d41049e322bda5ba53f5a.png)


### scatterplot 散布図
散布図の例です。

 bokeh_scatter.py
```
 import pandas as pd
 import pandas_bokeh
 
 df = pd.read_csv(
     r"https://raw.githubusercontent.com/PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/iris/iris.csv"
 )
 df = df.sample(frac=1)
 
 # Create Bokeh-Table with DataFrame:
 from bokeh.models.widgets import DataTable, TableColumn
 from bokeh.models import ColumnDataSource
 
 data_table = DataTable(
     columns=[TableColumn(field=Ci, title=Ci) for Ci in df.columns],
     source=ColumnDataSource(df),
     height=300,
 )
 
 # Create Scatterplot:
 p_scatter = df.plot_bokeh.scatter(
     x="petal length (cm)",
     y="sepal width (cm)",
     category="species",
     title="Iris DataSet Visualization",
 )
 
```

 IPython
```
 In [2]: # %load bokeh_scatter.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...: 
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/' 
    ...: url = gitjuburl + baseurl + 'iris/iris.csv' 
    ...:  
    ...: df = pd.read_csv(url) 
    ...: df = df.sample(frac=1) 
    ...:  
    ...: #Change one value to clearly see the effect of the size keyword 
    ...: df.loc[13, "sepal length (cm)"] = 15 
    ...:  
    ...: #Make scatterplot: 
    ...: p_scatter = df.plot_bokeh.scatter( 
    ...:     x="petal length (cm)", 
    ...:     y="sepal width (cm)", 
    ...:     category="species", 
    ...:     title="Iris DataSet Visualization with Size Keyword", 
    ...:     size="sepal length (cm)") 
    ...: 
```
![](https://gyazo.com/f9853d889fa816b45dcdbcc164d5d2e0.png)

### データを表示させる
bokeh の  `DataTable` を使うと、データを表形式で表示します。
グラフは `plot_bokeh()` を呼び出すときに  `show_figure=False` としておき、
 `plot_grid()` でDataTableのオブジェクトと合わせて表示します。
 bokeh_scatter_with_table.py
```
 import pandas as pd
 import pandas_bokeh
 
 df = pd.read_csv(
     r"https://raw.githubusercontent.com/PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/iris/iris.csv"
 )
 df = df.sample(frac=1)
 
 # Create Bokeh-Table with DataFrame:
 from bokeh.models.widgets import DataTable, TableColumn
 from bokeh.models import ColumnDataSource
 
 data_table = DataTable(
     columns=[TableColumn(field=Ci, title=Ci) for Ci in df.columns],
     source=ColumnDataSource(df),
     height=300,
 )
 
 # Create Scatterplot:
 p_scatter = df.plot_bokeh.scatter(
     x="petal length (cm)",
     y="sepal width (cm)",
     category="species",
     title="Iris DataSet Visualization",
     show_figure=False,
 )
 
 # Combine Table and Scatterplot via grid layout:
 pandas_bokeh.plot_grid([[data_table, p_scatter]], plot_width=400, plot_height=350)
 
```
![](https://gyazo.com/e50efd118f5e4f9d3d6e835d37e5d613.png)


### barplot 棒グラフ
棒グラフの例です。

 bokeh_bar.py
```
 import pandas as pd
 import pandas_bokeh
 
 data = {
     'fruits':
     ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries'],
         '2015': [2, 1, 4, 3, 2, 4],
         '2016': [5, 3, 3, 2, 4, 6],
         '2017': [3, 2, 4, 4, 5, 3]
 }
 df = pd.DataFrame(data).set_index("fruits")
 p_bar = df.plot_bokeh.bar(
     ylabel="Price per Unit [€ ]",
     title="Fruit prices per Year",
     alpha=0.6)
```


 IPython
```
 In [2]: # %load bokeh_bar.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: data = { 
    ...:     'fruits': 
    ...:     ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries'], 
    ...:     '2015': [2, 1, 4, 3, 2, 4], 
    ...:     '2016': [5, 3, 3, 2, 4, 6], 
    ...:     '2017': [3, 2, 4, 4, 5, 3] 
    ...: } 
    ...: df = pd.DataFrame(data).set_index("fruits") 
    ...:  
    ...: p_bar = df.plot_bokeh.bar( 
    ...:     ylabel="Price per Unit [€]", 
    ...:     title="Fruit prices per Year", 
    ...:     alpha=0.6) 
    ...:   
```

![](https://gyazo.com/d46f54d7ed40eb0f6e86103c2305b96a.png)

### StackedBar　積み上げ棒グラフ
barplot に `stacked=True` を与えると、積み上げ棒グラフになります。

 bokeh_stackedbar.py
```
 import pandas as pd
 import pandas_bokeh
 
 data = {
     'fruits':
     ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries'],
     '2015': [2, 1, 4, 3, 2, 4],
     '2016': [5, 3, 3, 2, 4, 6],
     '2017': [3, 2, 4, 4, 5, 3]
 }
 df = pd.DataFrame(data).set_index("fruits")
 
 p_stacked_bar = df.plot_bokeh.bar(
     ylabel="Price per Unit [€ ]",
     title="Fruit prices per Year",
     stacked=True,
     alpha=0.6)
```


 bokeh_stackedbar.py
```
 In [2]: # %load bokeh_stackedbar.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: data = { 
    ...:     'fruits': 
    ...:     ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries'], 
    ...:     '2015': [2, 1, 4, 3, 2, 4], 
    ...:     '2016': [5, 3, 3, 2, 4, 6], 
    ...:     '2017': [3, 2, 4, 4, 5, 3] 
    ...: } 
    ...: df = pd.DataFrame(data).set_index("fruits") 
    ...:  
    ...: p_stacked_bar = df.plot_bokeh.bar( 
    ...:     ylabel="Price per Unit [€]", 
    ...:     title="Fruit prices per Year", 
    ...:     stacked=True, 
    ...:     alpha=0.6) 
    ...:                                                                    
```

![](https://gyazo.com/53b8a663c4812fdfbe58b799951afbb9.png)


### histogram
ヒストグラムの例です。

 bokeoh_histgram_data.py
```
 import numpy as np
 import pandas as pd
 import pandas_bokeh
 
 df_hist = pd.DataFrame({
     'a': np.random.randn(1000) + 1,
     'b': np.random.randn(1000),
     'c': np.random.randn(1000) - 1
     },
     columns=['a', 'b', 'c'])
     
```

 bokeh_histgram_default.py
```
 #Top-on-Top Histogram (Default):
 df_hist.plot_bokeh.hist(
     bins=np.linspace(-5, 5, 41),
     vertical_xlabel=True,
     hovertool=False,
     title="Normal distributions (Top-on-Top)",
     line_color="black")
```


```
 In [2]: # %load bokeh_histgram_data.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: df_hist = pd.DataFrame({ 
    ...:     'a': np.random.randn(1000) + 1, 
    ...:     'b': np.random.randn(1000), 
    ...:     'c': np.random.randn(1000) - 1 
    ...:     }, 
    ...:     columns=['a', 'b', 'c']) 
    ...: 
    
 In [4]: # %load bokeh_histgram_default.py 
   ...: #Top-on-Top Histogram (Default): 
   ...: df_hist.plot_bokeh.hist( 
   ...:     bins=np.linspace(-5, 5, 41), 
   ...:     vertical_xlabel=True, 
   ...:     hovertool=False, 
   ...:     title="Normal distributions (Top-on-Top)", 
   ...:     line_color="black") 
   ...:                                                                           
 Out[4]: Figure(id='1001', ...)       
```


![](https://gyazo.com/8574f023c153a0715b2fc46406d2a1f9.png)

 `plot_bokeh(kind="hist")` としても  `plot_bokeh.hist()` を呼び出すことと同じです。
 `histogram_type="stacked"` を与えると、積み上げヒストグラムになります。

 bokeh_histgram_stacked.py
```
 #Stacked histogram:
 df_hist.plot_bokeh.hist(
     bins=np.linspace(-5, 5, 41),
     histogram_type="stacked",
     vertical_xlabel=True,
     hovertool=False,
     title="Normal distributions (Stacked)",
     line_color="black")
```

 IPython
```
 In [6]: # %load bokeh_histgram_stacked.py 
    ...: #Stacked histogram: 
    ...: df_hist.plot_bokeh.hist( 
    ...:     bins=np.linspace(-5, 5, 41), 
    ...:     histogram_type="stacked", 
    ...:     vertical_xlabel=True, 
    ...:     hovertool=False, 
    ...:     title="Normal distributions (Stacked)", 
    ...:     line_color="black") 
    ...:                                                                           
 Out[6]: Figure(id='1215', ...)
```

![](https://gyazo.com/9f7fdb53b348ad0f13a3a375c4a6a194.png)

 `histogram_type="sidebyside"` を与えるとデータごとにずらして描画します。

 bokeh_histgram_sidebyside.py
```
 #Side-by-Side Histogram
 # multiple bars share bin side-by-side
 # and also accessible via kind="hist":
 df_hist.plot_bokeh(
     kind="hist",
     bins=np.linspace(-5, 5, 41),
     histogram_type="sidebyside",
     vertical_xlabel=True,
     hovertool=False,
     title="Normal distributions (Side-by-Side)",
     line_color="black")
     
```

 IPythokn
```
 In [8]: # %load bokeh_histgram_sidebyside.py 
    ...: #Side-by-Side Histogram 
    ...: # multiple bars share bin side-by-side 
    ...: # and also accessible via kind="hist": 
    ...: df_hist.plot_bokeh( 
    ...:     kind="hist", 
    ...:     bins=np.linspace(-5, 5, 41), 
    ...:     histogram_type="sidebyside", 
    ...:     vertical_xlabel=True, 
    ...:     hovertool=False, 
    ...:     title="Normal distributions (Side-by-Side)", 
    ...:     line_color="black") 
    ...:                                                                           
 Out[8]: Figure(id='1429', ...)
```
![](https://gyazo.com/9c683814650ee37ac1c423e1c94333d2.png)

### areaplot - 面グラフ
 bokeh_area.py
```
 import pandas as pd
 import pandas_bokeh
 
 githuburl = 'https://raw.githubusercontent.com/'
 baseurl = 'PatrikHlobil/Pandas-Bokeh/master/'
 url = githuburl + baseurl + 'docs/Testdata/energy/energy.csv'
 
 df_energy = pd.read_csv(url, parse_dates=["Year"])
 df_energy.head()
 df_energy.plot_bokeh.area(
     x="Year",
     stacked=True,
     legend="top_left",
     colormap=["brown", "orange", "black", "grey", "blue", "green"],
     title="Worldwide energy consumption split by energy source",
     ylabel="Million tonnes oil equivalent",
     ylim=(0, 16000))
     
```

 IPython
```
 In [2]: # %load bokeh_area.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/' 
    ...: url = githuburl + baseurl + 'energy/energy.csv' 
    ...:  
    ...: df_energy = pd.read_csv(url, parse_dates=["Year"]) 
    ...: df_energy.head() 
    ...:  
    ...: df_energy.plot_bokeh.area( 
    ...:     x="Year", 
    ...:     stacked=True, 
    ...:     legend="top_left", 
    ...:     colormap=["brown", "orange", "black", "grey", "blue", "green"], 
    ...:     title="Worldwide energy consumption split by energy source", 
    ...:     ylabel="Million tonnes oil equivalent", 
    ...:     ylim=(0, 16000)) 
    ...:
```
![](https://gyazo.com/662b2c41930f878979bcf482cdb560d0.png)
 `stacked=True` を与えると、積み上げ面グラフになり各要素の割合の変化を観察することができます。

 bokeh_area2.py
```
 import pandas as pd
 import pandas_bokeh
 
 githuburl = 'https://raw.githubusercontent.com/'
 baseurl = 'PatrikHlobil/Pandas-Bokeh/master/'
 url = githuburl + baseurl + 'docs/Testdata/energy/energy.csv'
 
 df_energy = pd.read_csv(url, parse_dates=["Year"])
 df_energy.head()
 
 df_energy.plot_bokeh.area(
     x="Year",
     stacked=True,
     normed=100,
     legend="bottom_left",
     colormap=["brown", "orange", "black", "grey", "blue", "green"],
     title="Worldwide energy consumption split by energy source",
     ylabel="Million tonnes oil equivalent")
```

 IPython
```
 In [2]: # %load bokeh_area2.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/' 
    ...: url = githuburl + baseurl + 'energy/energy.csv' 
    ...:  
    ...: df_energy = pd.read_csv(url, parse_dates=["Year"]) 
    ...: df_energy.head() 
    ...:  
    ...: df_energy.plot_bokeh.area( 
    ...:     x="Year", 
    ...:     stacked=True, 
    ...:     normed=100, 
    ...:     legend="bottom_left", 
    ...:     colormap=["brown", "orange", "black", "grey", "blue", "green"], 
    ...:     title="Worldwide energy consumption split by energy source", 
    ...:     ylabel="Million tonnes oil equivalent") 
    ...:                                                                   
```

![](https://gyazo.com/764c78bb1c04768d16d88276f5dfbe10.png)

### pieplot　円グラフ
円グラフの例です。
引数  `x` に与えたカラム別に円グラフば描画され、凡例（legend) に表示されます。
 bokeh_pie.py
```
 import pandas as pd
 import pandas_bokeh
 
 githuburl = 'https://raw.githubusercontent.com/'
 baseurl = 'PatrikHlobil/Pandas-Bokeh/master/'
 url = githuburl + baseurl + 'docs/Testdata/Bundestagswahl/Bundestagswahl.csv'
 
 df_pie = pd.read_csv(url)
 df_pie.plot_bokeh.pie(
     x="Partei",
     y="2017",
     colormap=["blue", "red", "yellow", "green", "purple", "orange", "grey"],
     title="Results of German Bundestag Election 2017",
     )
```

 IPython
```
 In [2]: # %load bokeh_pie.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/' 
    ...: url = githuburl + baseurl + 'Bundestagswahl/Bundestagswahl.csv' 
    ...:  
    ...: df_pie = pd.read_csv(url) 
    ...:  
    ...: df_pie.plot_bokeh.pie( 
    ...:     x="Partei", 
    ...:     y="2017", 
    ...:     legend_field="Partei",
    ...:     colormap=["blue", "red", "yellow", "green", "purple", "orange", "grey"
    ...: ], 
    ...:     title="Results of German Bundestag Election 2017", 
    ...:     ) 
    ...:                                                                           
 Out[2]: Figure(id='1036', ...)
 
 In [3]: df_pie                                                             Out[3]: 
       Partei  2002  2005  2009  2013  2017
 0    CDU/CSU  38.5  35.2  33.8  41.5  32.9
 1        SPD  38.5  34.2  23.0  25.7  20.5
 2        FDP   7.4   9.8  14.6   4.8  10.7
 3     Grünen   8.6   8.1  10.7   8.4   8.9
 4  Linke/PDS   4.0   8.7  11.9   8.6   9.2
 5        AfD   0.0   0.0   0.0   0.0  12.6
 6   Sonstige   3.0   4.0   6.0  11.0   5.0
 
```

![](https://gyazo.com/3f35ac704abae5bd911c42da7f3c036c.png)

引数  `y` を複数のカラムを与えると、１つのグラフに複数の円グラフがネストされて描画されます。
引数 `y` を省略すると、与えたデータフレームのすべてのカラムのデータを描画します。

 bokeh_pie_multi.py
```
 import pandas as pd
 import pandas_bokeh
 
 githuburl = 'https://raw.githubusercontent.com/'
 baseurl = 'PatrikHlobil/Pandas-Bokeh/master/'
 url = githuburl + baseurl + 'docs/Testdata/Bundestagswahl/Bundestagswahl.csv'
 
 df_pie = pd.read_csv(url)
 df_pie.plot_bokeh.pie(
     x="Partei",
     colormap=["blue", "red", "yellow", "green", "purple", "orange", "grey"],
     title="Results of German Bundestag Elections [2002-2017]",
     line_color="grey")
```

 IPython
```
 In [2]: # %load bokeh_pie_multi.py 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/' 
    ...: url = githuburl + baseurl + 'Bundestagswahl/Bundestagswahl.csv' 
    ...:  
    ...: df_pie = pd.read_csv(url) 
    ...:  
    ...: df_pie.plot_bokeh.pie( 
    ...:     x="Partei", 
    ...:     colormap=["blue", "red", "yellow", "green", "purple", "orange", "grey"
    ...: ], 
    ...:     title="Results of German Bundestag Elections [2002-2017]", 
    ...:     line_color="grey") 
    ...:                                                                           
```

![](https://gyazo.com/96d304a5c2ee212139a186e44f0d1b61.png)



### mapplot
GeoPandas がインストールされていると、pandas-bokeh は mapplot で地図データをベースにデータを重ねて描画することができます。

 bokeh_map.py
```
 import pandas as pd
 import pandas_bokeh
 
 githuburl = 'https://raw.githubusercontent.com/'
 baseurl = r'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/populated%20places/'
 url = githuburl + baseurl + 'populated_places.csv'
 df_map = pd.read_csv(url)
 df_map["size"] = df_map["pop_max"] / 1000000
 df_map.plot_bokeh.map(
     x="longitude",
     y="latitude",
     hovertool_string="""<h2> @{name} </h2>
 
                         <h3> Population: @{pop_max} </h3>""",
     tile_provider="STAMEN_TERRAIN_RETINA",
     size="size",
     figsize=(900, 600),
         title="World cities with more than 1.000.000 inhabitants")
 
 Ipython
```
 In [2]: # %load bokeh_map 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = r'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/populated%20pla
    ...: ces/' 
    ...: url = githuburl + baseurl + 'populated_places.csv' 
    ...: df_map = pd.read_csv(url) 
    ...:  
    ...: df_map["size"] = df_map["pop_max"] / 1000000 
    ...: df_map.plot_bokeh.map( 
    ...:     x="longitude", 
    ...:     y="latitude", 
    ...:     hovertool_string="""<h2> @{name} </h2> 
    ...:  
    ...:                         <h3> Population: @{pop_max} </h3>""", 
    ...:     tile_provider="STAMEN_TERRAIN_RETINA", 
    ...:     size="size", 
    ...:     figsize=(900, 600), 
    ...:     title="World cities with more than 1.000.000 inhabitants") 
   
```

![](https://gyazo.com/29a4fb2af5874688d891290308d77b00.png)

 IPython
```
 In [1]: # %load bokeh_map.py 
    ...: import geopandas as gpd 
    ...: import pandas as pd 
    ...: import pandas_bokeh 
    ...:  
    ...: githuburl = 'https://raw.githubusercontent.com/' 
    ...: baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/states/' 
    ...: url = githuburl + baseurl + 'states.geojson' 
    ...:  
    ...: df_states = gpd.read_file(url) 
    ...: df_states.plot_bokeh(simplify_shapes=10000)                               
```


![](https://gyazo.com/2a6f695bf3b91bbb33f5c7e177bf3091.png)


### 既知の問題
Bokeh のバージョンが 2.0 になり、pandas-bokeh が一部うまく処理できないところがありました。

#### legend キーワードが legend_label に変わった
この修正により pandas-bokeh 0.4.2では、プロットとしたときにワーニングメッセージが表示されました。


```
 BokehDeprecationWarning: 'legend' keyword is deprecated, use explicit 'legend_label', 'legend_field', or 'legend_group' keywords instead
 BokehDeprecationWarning: 'legend' keyword is deprecated, use explicit 'legend_label', 'legend_field', or 'legend_group' keywords instead
```

pandas-bokeh のバージョン 0.5.0 でうまく処理できるようになっています。


参考:
　[Bokeh オフィシャルサイト ](https://bokeh.org/)
　[Python-Bokeh ソースコード ](https://github.com/PatrikHlobil/Pandas-Bokeh)
- [geoplot: geospatial data visualization ](https://residentmario.github.io/geoplot/index.html)


