Seabornを使ってみよう
=================
Seaborn はPythonで利用できるグラフ描画のための拡張モジュールです。Matplotlib をベースに作られているため、散布図や折れ線グラフなどの基本的なグラフ描画は Matplotlib の機能を利用しています。Matplotlib では細かな設定をしないようなグラフでも簡単に見栄えのよい美しいグラフを描画することができるようになります。

### インストール
拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install seaborn
 bash pipの場合
```
 $ pip install seaborn
```

### データセット
実は seaborn はドキュメントに描画例を示すために使用している[サンプルデータ ](https://github.com/mwaskom/seaborn-data)をダウンロードすることができます。データセットの一覧は  `get_dataset_names()` でリストすることができます。
このとき、次のようなメッセージが表示されます。
 IPython
```
 In [19]: seaborn.get_dataset_names()                                              
 /Users/goichiiisaka/anaconda3/envs/py36/lib/python3.6/site-packages/seaborn/utils.py:384: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.
 
 The code that caused this warning is on line 384 of the file /Users/goichiiisaka/anaconda3/envs/py36/lib/python3.6/site-packages/seaborn/utils.py. To get rid of this warning, pass the additional argument 'features="lxml"' to the BeautifulSoup constructor.
 
   gh_list = BeautifulSoup(http)
```

このメッセージは無害なのですが、 `seaborn/utils.py` の 384行目（このときのバージョンでは)を次のように修正するとこのメッセージは表示されなくなります。


```
 gh_list = BeautifulSoup(http,features="lxml")
```

 IPython
```
 In [1]: import seaborn                                                     In [2]: seaborn.get_dataset_names()                                        Out[2]: 
 ['anscombe',
  'attention',
  'brain_networks',
  'car_crashes',
  'diamonds',
  'dots',
  'exercise',
  'flights',
  'fmri',
  'gammas',
  'iris',
  'mpg',
  'planets',
  'tips',
  'titanic']
 
```

データセットのロードには  `load_dataset()` を実行します。
データセット  `iris` を読み込んでみましょう。
 IPython
```
 In [8]: iris = seaborn.load_dataset('iris')                                In [9]: iris.head()                                                        Out[9]: 
    sepal_length  sepal_width  petal_length  petal_width species
 0           5.1          3.5           1.4          0.2  setosa
 1           4.9          3.0           1.4          0.2  setosa
 2           4.7          3.2           1.3          0.2  setosa
 3           4.6          3.1           1.5          0.2  setosa
 4           5.0          3.6           1.4          0.2  setosa
```

アイリス(iris)は、花の色がきれいで鮮やかなアヤメ属の植物で、このデータセットは３種類の
アイリス（[Setosa https://www.fs.fed.us/wildflowers/beauty/iris/Blue_Flag/iris_setosa.shtml]、[Versicolour https://www.fs.fed.us/wildflowers/beauty/iris/Blue_Flag/iris_versicolor.shtml]、[Virginica ](https://www.fs.fed.us/wildflowers/beauty/iris/Blue_Flag/iris_virginica.shtml)）の花びらとがく片の長さで構成されています。

 irisデータセットのカラム名

| カラム名 | 説明 |
|:--|:--|
| sepal_length | ガクの長さ |
| sepal_width | ガクの幅 |
| petal_length | 花弁の長さ |
| petal_width | 花弁の幅 |
| species | 種別 |

このデータを使って seaborn の描画サンプルをみてみましょう。

### 散布図
散布図は  `pairplot()` にデータフレームを渡すだけです。
(紙面の都合で `height=` を与えていますが、なくても問題ありません）
 IPython
```
 In [16]: seaborn.pairplot(iris,height=1.5)                                 Out[16]: <seaborn.axisgrid.PairGrid at 0x1a2636b668>
```

![](https://gyazo.com/41f527108e6ed49fd182974b7586e736.png)
このままでも良いのですが、 `set()` で 描画スタイルをセットしてみましょう。
 IPython
```
 In [17]: seaborn.set()                                                     In [18]: seaborn.pairplot(iris,height=1.5)                                 Out[18]: <seaborn.axisgrid.PairGrid at 0x1a24c7c358>
```
![](https://gyazo.com/1b3a51ad0d0e2955745034bfa91cf595.png)

スタイルが変わって見栄えがするようになりましたね。
アイリスの種別ごとに色を変えてみましょう。
これには、 `pairplot()` に  `hue=カラム名` を与えると、そのカラム別に色を変えて描画してくれます。
 IPython
```
 In [19]: seaborn.pairplot(iris,hue="species", height=1.5)                  Out[19]: <seaborn.axisgrid.PairGrid at 0x1a26647c18>
 
```
![](https://gyazo.com/f82e12eaedac4eeaaa7bd1ef55d2621b.png)

### カラムを特定した散布図
特定の特徴の組み合わせた散布図を描画するときは、 `jointplot()` を使います。
 Ipython
```
 In [20]: seaborn.jointplot('sepal_width', 'petal_length', data=iris)       Out[20]: <seaborn.axisgrid.JointGrid at 0x1a26659c50>
```

![](https://gyazo.com/7eebeeb7a4b375353a929c5d2953153f.png)
 `jointplot()` に  `kind=タイプ` を与えると色々なグラフになります。
- scatter：散布図（デフォルト）
- reg：線形回帰、Regression plots
- resid：残差散布図、残差(resid value)は予測値とデータの乖離を指す統計用語
- kde：等高線
- hex：六角形

線形回帰を行った例です。

 IPython
```
 In [21]: seaborn.jointplot('petal_width', 'petal_length', 
 ...:                        data=iris, kind="reg")  
 Out[21]: <seaborn.axisgrid.JointGrid at 0x1a259be0b8>
```

![](https://gyazo.com/df214fb0fcd6c2cc3fed19106b4c12ae.png)

### 分布図
 `distplot()` を使うと簡単に分布図を描画できます。

 IPython
```
 In [27]: seaborn.distplot(iris['petal_width'])                             Out[27]: <matplotlib.axes._subplots.AxesSubplot at 0x1a2446cbe0>
```

![](https://gyazo.com/053d08de8735b73b0033d890c8ece127.png)

seaborn ではこの他にも多くのグラフタイプがあります。

### The Python Graph Gallery
![](https://gyazo.com/a2b2732ce2fd59614111282405fe822b.png)

このサイトには、matplotlib、seaborn、pandas でグラフ描画のサンプルとそのコードがまとめされています。
目的のグラフを探してコードをスニペットとして利用できるのでとても便利です。

参考：
- [Seaborn オフィシャルサイト ](https://seaborn.pydata.org/)
- [The Python Graph Gallery ](https://python-graph-gallery.com/)
- [matplotlib オフィシャルサイト ](https://matplotlib.org/)



