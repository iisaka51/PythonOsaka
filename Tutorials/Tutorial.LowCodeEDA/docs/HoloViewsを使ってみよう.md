HoloViewsを使ってみよう
=================

### HoloViews

[HoloViews](http://holoviews.org/index.html]) はデータ分析と可視化を簡単に行うことができるアプリケーション HoloViz で利用されている拡張モジュールで、matplotlibやBokehなどの可視化ライブラリを使いやすくしてくれます。
可視化の作業を簡単にして、データ分析に集中できるようにすることを目指して開発されています。

### インストール

拡張モジュールなので次のようにインストールします。

 condaの場合
```
 $ conda install holoviews
```

 pipの場合
```
 $ pip install holoviews
```


### 準備

ほとんどの場合 NumPy を使用することになるはずなのでインポートしておきましょう。またまた、Jupyter Notebook でHoloViews を利用するためには、`notebook_extension()` を実行しておきます。

 IPython
```
 In [1]: import numpy as np
 In [2]: import holoviews as hv                                             In [3]: hv.notebook_extension()
```

### オンラインドキュメント

HoloViews にはオンラインドキュメントが提供されています。
次のようにインスタンスオブジェクトを生成したときには、
いくつかの方法でオンラインドキュメントを参照することができます。

 IPython
```
 In [4]: obj = hv.Element(None, group='Value', label='Label')
```

- `hv.help(Element)` / `hv.help(e)`：
  - オブジェクトやタイプの説明とパラメーターのドキュメントを表示
- `hv.help(Element、pattern = "group")`：
  - 指定された正規表現（この例では"group"）に一致するヘルプ項目のみを表示します
- `Element(<Shift+TAB>|<TAB>)`
  - IPythonで有効
  - オブジェクトコンストラクターを開いて`<Shift+TAB>`や`<TAB>`を繰り返す
  - 最終的に `hv.help(Element)` の完全な出力が表示されます
- `hv.help(Element,Visualization=True)` / `hv.help(e,Visualization=True)`：
  - 要素または特定のオブジェクトeを視覚化するためのオプションの説明を表示
  - オブジェクト自体のオプションではないことに留意
- `%output info=True`
  - IPython/Jupyter Notebook のセルで有効
  - HoloViewsオブジェクトobjに対して`hv.help(obj, Visualization=True)`を表示
- `%%output info = True`
  - IPython / Jupyter Notebook 全体で有効
  - HoloViewsオブジェクトobjに対して`hv.help(obj, Visualization=True)`を表示

### bokeh をバックエンドにする

HoloViews ではグラフ描画のバックエンドとして、 matplotlib だけでなく bokeh や Plotlyも使用することができます。

描画例をみてみましょう。

### 散布図

散布図の描画には `Points()`クラス使います。


 IPython
```
 In [2]: # %load holoviews_points.py
    ...: import numpy as np
    ...: import pandas as pd
    ...: import holoviews as hv
    ...: import panel as pn
    ...: hv.extension('bokeh', logo=False)
    ...:
    ...: data = np.random.normal(size=[50, 2])
    ...: df = pd.DataFrame(data, columns=['col1', 'col2'])
    ...:
    ...: hv_plot = hv.Points(df).opts(width=600,
    ...:                              title='Sample Scatter Plot')
    ...:
    ...: bokeh_server = pn.Row(hv_plot).show(port=12345)
    ...: bokeh_server.stop()
    ...:
 Launching server at http://localhost:12345
```

すると自動的に bokeh サーバが起動し、ブラウザにグラフを描画してくれます。
このグラフはインタラクティブに拡大縮小、移動などが行なえます。

![](https://gyazo.com/5537264c35d9a06e1a677d6e00743c2b.png)

HoloViews のグラフ描画の手順を説明してみましょう。
まず、`hv.extension()` で bokeh をバックエンドに指定します。
ここでは、ランダムな数値を `numpy.ndarray`オブジェクトで生成してから、データフレームにしています。これを、`Points()` でプロットオブジェクトにしています。
このとき、描画オプションを `opts()` メソッドで与えています。（`width`、`title`)

ダッシュボードを作るため、インポートしておいた `panel` に渡すと、
自動的にバックエンドにしていていた bokeh サーバが起動します。

Jupyter notebook から利用していて、`hv.notebook_extension()`を実行済みのときは、 最後の２行(`bokeh_server`) は不要です。

### グラフを並べる

次のコードは、対数軸の例です。

 IPython
```
 In [2]: # %load holoviews_2curve.py
    ...: import numpy as np
    ...: import pandas as pd
    ...: import holoviews as hv
    ...: import panel as pn
    ...: hv.extension('bokeh', logo=False)
    ...: import bokeh
    ...:
    ...: semilogy = hv.Curve(np.logspace(0, 5),
    ...:                     label='Semi-log y axes')
    ...: loglog = hv.Curve((np.logspace(0, 5), np.logspace(0, 5)),
    ...:                     label='Log-log axes')
    ...:
    ...: hv_plot = semilogy.opts(logy=True) + \
    ...:           loglog.opts(logx=True, logy=True, shared_axes=False)
    ...:
    ...: bokeh_server = pn.Row(hv_plot).show(port=12345)
    ...: bokeh_server.stop()
    ...:
 Launching server at http://localhost:12345
```

オブジェクトを演算子(`+`)でつなぐと、グラフを並べることができます。

![](https://gyazo.com/14b736d79736d2477d88f02aa30e2bd5.png)

### グラフを重ねる
時系列データの例です。

 IPyhton
```
 In [2]: # %load holoviews_curve.py
    ...: import numpy as np
    ...: import pandas as pd
    ...: import holoviews as hv
    ...: import panel as pn
    ...: import bokeh
    ...: from bokeh.sampledata.stocks import GOOG, AAPL
    ...: hv.extension('bokeh', logo=False)
    ...:
    ...: goog_stock = np.array(GOOG['date'], dtype=np.datetime64)
    ...: aapl_stock = np.array(AAPL['date'], dtype=np.datetime64)
    ...:
    ...: goog = hv.Curve((goog_stock, GOOG['adj_close']),
    ...:                 'Date', 'Stock Index', label='Google')
    ...: aapl = hv.Curve((aapl_stock, AAPL['adj_close']),
    ...:                 'Date', 'Stock Index', label='Apple')
    ...:
    ...: hv_plot = (goog * aapl).opts(width=600, legend_position='top_left')
    ...: bokeh_server = pn.Row(hv_plot).show(port=12345)
    ...: bokeh_server.stop()
    ...:
 Launching server at http://localhost:12345
```

オブジェクトを演算子(`*`)でつなぐと、グラフを重ねることができます。

![](https://gyazo.com/8020a0155a7d06548ab377da34b66377.png)

なんのストレスもなく、時系列データを比較できますね。

### ヒートマップ図

 IPython
```
 In [2]: # %load holoviews_heatmap.py
    ...: import numpy as np
    ...: import pandas as pd
    ...: import holoviews as hv
    ...: import panel as pn
    ...: hv.extension('bokeh', logo=False)
    ...: import bokeh
    ...:
    ...: data = [(i, chr(97+j),  i*j) for i in range(5) for j in range(5) if i!=j]
    ...: hv_plot = hv.HeatMap(data).sort()
    ...: hv_plot.opts(xticks=None)
    ...:
    ...: bokeh_server = pn.Row(hv_plot).show(port=12345)
    ...: bokeh_server.stop()
    ...:
 Launching server at http://localhost:12345
```

![](https://gyazo.com/526dce9c4eb4bcd2423ecd34ebe5bd14.png)

### BoxWishker

 IPython
```
 In [2]: # %load holoviews_boxwishker.py
    ...: import numpy as np
    ...: import pandas as pd
    ...: import holoviews as hv
    ...: import panel as pn
    ...: hv.extension('bokeh', logo=False)
    ...: import bokeh
    ...:
    ...: groups = [chr(65+g) for g in np.random.randint(0, 3, 200)]
    ...: boxes = hv.BoxWhisker((groups,
    ...:                        np.random.randint(0, 5, 200),
    ...:                        np.random.randn(200)),
    ...:                       ['Group', 'Category'], 'Value').sort()
    ...:
    ...: boxes.opts(width=600)
    ...:
    ...: bokeh_server = pn.Row(boxes).show(port=12345)
    ...: bokeh_server.stop()
    ...:
 Launching server at http://localhost:12345
```

![](https://gyazo.com/de9456fd9b33af13aebee7a636f70d75.png)


### 動的な描画

Bokeh の特徴のひとつに動的な描画が行えることにあり、HoloViews でも`HoloMap()`を使うことで動的な描画を行うことができます。

 IPython
```
 In [2]: # %load holoviews_holomap.py
    ...: import numpy as np
    ...: import pandas as pd
    ...: import holoviews as hv
    ...: import panel as pn
    ...: hv.extension('bokeh', logo=False)
    ...: import bokeh
    ...:
    ...: hv_plot = hv.HoloMap({i: hv.Curve([1, 2, 3-i], \
    ...:                group='Group', label='Label') for i in range(3)},
    ...:                'Value')
    ...: bokeh_server = pn.Row(hv_plot).show(port=12345)
    ...: bokeh_server.stop()
    ...:
 Launching server at http://localhost:12345
```

これを実行すると、ブラウザにグラフとスライダーが描画されます。
![](https://gyazo.com/65769ad723c9aff5f66fad8ff33392bf.png)
マウスでスライダーを移動させて値(`Values`)を変えると、
それにともなってグラフも変化します。

![](https://gyazo.com/497153a15b43ffee2ef33fa7ea72339e.png)


参考：
- [HoloViz オフィシャルサイト](https://holoviz.org/])
- [HoloViws オフィシャルサイト](https://holoviews.org/])
- [HoloViws Gallery](http://holoviews.org/gallery/index.html])
- [Panel オフィシャルサイト](https://panel.holoviz.org/])
- [Param オフィシャルサイト](https://param.holoviz.org/])



