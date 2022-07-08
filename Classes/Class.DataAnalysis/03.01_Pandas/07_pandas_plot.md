pandasでデータをプロットしてみよう
=================
### plot()メソッド
Pandas の  `Series` オブジェクトや `DataFrame` オブジェクトには  `plot()` メソッドがあります。 `plot()` メソッドが返すものは `matplotlib.axes` オブジェクトで、これからわかるようにmatplotlibがベースになっていて、より簡単に可視化（グラフ描画）してくれます。
ただし、描画できるのはデータフレームにある数値データだけです。

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
    ...: baseurl = 'https://raw.githubusercontent.com/mwaskom/seaborn-data' 
    ...: url = baseurl + '/master/iris.csv' 
    ...: df = pd.read_csv(url) 
    ...: 
                                                                       
 In [3]: df.head()                                                          Out[3]: 
    SepalLength  SepalWidth  PetalLength  PetalWidth         Name
 0          5.1         3.5          1.4         0.2  Iris-setosa
 1          4.9         3.0          1.4         0.2  Iris-setosa
 2          4.7         3.2          1.3         0.2  Iris-setosa
 3          4.6         3.1          1.5         0.2  Iris-setosa
 4          5.0         3.6          1.4         0.2  Iris-setosa
 
 In [4]: %matplotlib                                                        Using matplotlib backend: MacOSX
 
 In [5]: df.plot()                                                          Out[5]: <matplotlib.axes._subplots.AxesSubplot at 0x11db2e080>
 
```

![](https://gyazo.com/9aa84276f94db67c42dc339d055baafd.png)

Jupyter notebook では次のマジックコマンドをセルで実行しておくと、
それ以降で、 `plot()` メソッドが実行されるとグラフがノートブック内に表示されます。
Python
```
 %matplotlib inline
```


### 個別データをプロット
 `plot()` メソッドに  `subplots=True` を与えると、データごとにグラフ描画します。
 IPython
```
 In [6]: df.plot(subplots=True)                                                    
 Out[6]: 
 array([<matplotlib.axes._subplots.AxesSubplot object at 0x11ffa9898>,
        <matplotlib.axes._subplots.AxesSubplot object at 0x1216a5e10>,
        <matplotlib.axes._subplots.AxesSubplot object at 0x1216e22b0>,
        <matplotlib.axes._subplots.AxesSubplot object at 0x11f5e9710>],
       dtype=object)
```

![](https://gyazo.com/2ff3b9d7468c883614561c8bb9791168.png)

 `plot()` メソッドに  `layout=` を与えると、データごとにグラフ描画のレイアウトを変更することができます。
 IPython
```
 In [8]: df.plot(subplots=True,layout=(2,2))                                Out[8]: 
 array([[<matplotlib.axes._subplots.AxesSubplot object at 0x11f9b0ef0>,
         <matplotlib.axes._subplots.AxesSubplot object at 0x120a23710>],
        [<matplotlib.axes._subplots.AxesSubplot object at 0x120a55860>,
         <matplotlib.axes._subplots.AxesSubplot object at 0x123fcdcc0>]],
       dtype=object)
```

![](https://gyazo.com/201e8cbc0ff6a066f928ca5e85b89e16.png)


 `plot()` メソッドに、 `kind=` でグラフの種類を与えることができます。

-  `line` ： 折れ線グラフ（line plot）
-  `bar` : 垂直棒グラフ（vertical bar plot）
-  `barh` ：水平棒グラフ（horizontal bar plot）
-  `box` ：箱ひげ図（boxplot）
-  `hist` ：ヒストグラム（histogram）、 `stacked=True` で積み上げグラフ
-  `kde` 、 `density` ：カーネル密度推定（Kernel Density Estimation plot）
-  `area` ：面グラフ（area plot）
-  `scatter` ：散布図（scatter plot）
-  `hexbin` ：hexbin plot
-  `pie` ：円グラフ（pie plot）

### 画像を保存する
 `plot()` で描画する画像を保存したいときは、次のように行います。
 IPython
```
 In [2]: # %load pandas_csv_readfromurl.py  
    ...: import pandas as pd 
    ...:  
    ...: baseurl = 'https://github.com/pandas-dev/pandas/raw/master/pandas' 
    ...: url = baseurl + '/tests/data/iris.csv' 
    ...: df = pd.read_csv(url) 
    ...:                                                                           
 In [3]: df.plot().get_figure().savefig('./iris.png')                       
```


### 画像の保存についての余談
matplotlib.ax オブジェクトの  `get_figure()` の実装は、次のように単に [figureプロパティーを返す ](https://github.com/matplotlib/matplotlib/blob/2108af1b75fc9100d7ca081d83cf17d8653591ea/lib/matplotlib/artist.py#L682-L684) だけです。

```
 def get_figure(self):
     """Return the  `.Figure` instance the artist belongs to."""
     return self.figure
```
このため、画像の保存は `get_figure()` メソッドを使わずにできると思うかもしれません。事実、今のバージョンでは次のようにして保存することができます。

```
 df.plot().figure.savefig('./iris.png') 
```

これは、よくないと考えています。
理由は、 `get_figure()` メソッドを作っている意味を考えると、将来何らかの変更があったときにこのメソッドで対応するという意図があるはずだからです。
今時点で、「できるから」という考えでコードを書いてしまうと、
将来 matplotlib のバージョンアップに対応できなくなる潜在的な不具合を埋め込むことになるかもしれません。




