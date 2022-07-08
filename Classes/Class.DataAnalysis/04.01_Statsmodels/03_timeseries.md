statsmodelsで時系列データ分析をしてみよう
=================
### 時系列データ分析
時系列データは、その名前が示すように、一定の時間間隔で収集されたデータポイントのコレクションです。これらを分析して長期的な傾向を判断し、将来の予測を行ったりします。時系列データ分析が通常の回帰分析と比べて、難しくなる理由には次の2つがあります。

#### 時間に依存している
時系列データは時間に依存していて、収集されたデータが独立しているという回帰モデルの基本的な仮定は成り立ちません。
#### なんらかの季節性が存在することがある
ほとんどの時系列データには、増加または減少する傾向に加えて、何らかの季節性 (seasonality) の傾向、つまり特定の時間枠で固有の変動があります。たとえば、エアコンの売り上げを時系列で確認すると、夏の売り上げは増える傾向があります。

時系列データにはそれぞれ固有の特性があるため、その分析にはさまざまなステップがあります。

#### 株価データは予測できるのか
ここでは、Yahoo Finance から S&P500(^GSPC)の過去５０年分のデータをダウンロードして、
時系列データ分析などを行ってみます。
まず、データをダウンロードしましょう。
 ipython
```
 In [2]: # %load statsmodels_datareader.py  
    ...: from datetime import datetime 
    ...: import pandas as pd 　
    ...: import pandas_datareader as pdr 
    ...:  
    ...: start=datetime(1970, 1, 1) 
    ...: end=datetime(2020, 1, 1) 
    ...: stock_data = pdr.DataReader("^GSPC", 'yahoo', start, end) 
    ...:  
    ...: stock_data.to_csv('SP500.csv') 
    ...:                                                                    
 
 In [3]: %load statsmodels_stock.py                                         In [4]: # %load statsmodels_stock.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...: import statsmodels.api as sm 
    ...: import matplotlib.pyplot as plt 
    ...:  
    ...: stock_data = pd.read_csv('SP500.csv', 
    ...:                           index_col='Date', parse_dates=True) 
    ...: stock_data = stock_data.sort_index() 
    ...:                                                                           
 
 In [5]: %matplotlib osx                                                    In [6]: stock_data['Close'].plot(figsize=(8, 4))                           Out[6]: <matplotlib.axes._subplots.AxesSubplot at 0x1a1ac00240>
```

IPythonのセルに、マジックコマンド  `%matplotlib` を使って使用しているプラットフォームに応じたデバイスを指定します。

#### Jupyter Notebookの場合
 IPython
```
 %matplotlib inline
```

#### IPython をMac で動作させている場合
 IPython
```
 %matplotlib osx
```

#### IPython を Windows で動作させている場合
 IPython
```
 %matplotlib qt
```

#### IPython に判断を任せる場合
 IPython
```
 %matplotlib
```

終値をプロットしてみます。

```
 stock_data['Close'].plot(figsize=(8, 4))
```

![](https://gyazo.com/d0966cc4377a88d2f1186fe86b362f5b.png)

最初に注目すべきことは、2002年と2008年の市場暴落を除いて、長期的には下降するより上昇する傾向があることが観察できます。これは、この時系列データが非定常であることを意味しています。
> 時系列データの定常性(STATIONARITY)
> 時間によらず期待値、自己共分散が一定であるような時系列データの性質のこと。
> わかりやすく言い換えると、時系列データが定常であれば、平均に回帰します。

まずは、現在の値[$ t ]から以前の値[$ t -1 ]を引いて、差分 [$ d(t)]を求めることから分析してみましょう。
 IPython
```
 In [6]: stock_data['First Difference'] = stock_data['Close'] - \ 
    ...:                                  stock_data['Close'].shift()       In [7]: stock_data['First Difference'].plot(figsize=(8, 4))                Out[7]: <matplotlib.axes._subplots.AxesSubplot at 0x1a2816d860>
 
```


![](https://gyazo.com/ec89fb3c7ddb073359f307bffd84e2a4.png)

このプロットではデータの変動の振幅を知ることができます。
ここで、注目する点は、初期には変動幅は非常に小さく、時間とともに着実に増加していることです。 これは、データが非定常であるだけでなく、指数関数的に増加していることを示しています。 
最近の変動の大きさは、1990年以前の変化を見えなくしてしまっているので、オリジナルの時系列データに対数変換を適用しましょう。

 IPython
```
 stock_data['Natural Log'] = stock_data['Close'].apply(lambda x: np.log(x))
    ...:                                                                    In [9]: stock_data['Natural Log'].plot(figsize=(8, 4))                     Out[9]: <matplotlib.axes._subplots.AxesSubplot at 0x1a2814b4e0>
```

![](https://gyazo.com/e06ae78708d5980d01b3bc7afb799cc8.png)

時間の経過に伴う分散を分析すると、対数変換の効果を視覚的に確認することができます。

 IPython
```
 In [2]: # %load statsmodels_stock.py 
    ...: import numpy as np 
    ...: import pandas as pd 
    ...: import statsmodels.api as sm 
    ...: import matplotlib.pyplot as plt 
    ...:  
    ...: stock_data = pd.read_csv('SP500.csv', 
    ...:                           index_col='Date', parse_dates=True) 
    ...: stock_data = stock_data.sort_index() 
    ...:                                                                           
 In [3]: stock_data['Natural Log'] = \
                         stock_data['Close'].apply(lambda x: np.log(x))
    ...:                                                                    In [4]: stock_data['Logged First Difference'] = \
         stock_data['Natural Log'] - stock_data['Natural Log'].shift()      In [5]: %matplotlib osx                                                    In [6]: stock_data['Logged First Difference'].plot(figsize=(8,4))          Out[6]: <matplotlib.axes._subplots.AxesSubplot at 0x1a1ddd4f60>
```
![](https://gyazo.com/bfec2c432d76605500b0b55fe5c3c5f6.png)
これで、S＆P 500インデックスの毎日の変化の定常時系列モデルができました。
次に、いくつかのラグ変数 `f(t-1)` 、 `f(t-2)` などを作成し、それらの `f(t)` との関係を調べています。時系列データには、多くの場合ある種の**季節性 (seasonality)** が見られることがあります。この、「**季節的な影響 ("seasonal" effects)**」を探すために、1日と2日のラグ(lag)、および週ごとと月ごとのラグを調べます。

 IPython
```
 In [7]: stock_data['Lag_1'] = \
    ...:         stock_data['Logged First Difference'].shift() 
    ...: stock_data['Lag_2'] = \
    ...:         stock_data['Logged First Difference'].shift(2) 
    ...: stock_data['Lag_5'] = \
    ...:          stock_data['Logged First Difference'].shift(5) 
    ...: stock_data['Lag_30'] = \
    ...:           stock_data['Logged First Difference'].shift(30)    
 
 In [8]: import seaborn as sb
 In [9]: sb.jointplot('Logged First Difference', 'Lag 1', \
 ...:                  stock_data, kind='reg', height=6)
 Output[9]: <seaborn.axisgrid.JointGrid at 0x1a237fb5f8>
```


![](https://gyazo.com/e8395b0820917f978a28cf11f45f757e.png)

このプロットを観察するときは、どのくらい密に集まっているかと両軸の分布にの注目します。この例では、両軸の分布はおおむね正規分布となっています。これは、ある日から次の日までの値の変化の間にほとんど相関関係がないことを表していて、ある日のインデックス値を知っていても、翌日にどうなるかは推測できないことになります。つまり、上がるか下がるかはコイントスで表裏がでるのと変わらないということです。

上記で作成した他のラグの値（これを**遅延変数**といいます）も同様の結果を示しています。 試していない他のラグステップとの関係がある可能性がありますが、可能なすべてのラグ値を手動でテストすることは現実的ではありません。 `statsmodels` にはこれを体系的に実行できる関数が提供されています。

 IPython
```
 In [23]: from statsmodels.tsa.stattools import acf 
     ...: from statsmodels.tsa.stattools import pacf 
     ...:  
     ...: lag_correlations = \
     ...:    acf(stock_data['Logged First Difference'].iloc[1:],　fft=False) 
     ...: lag_partial_correlations = \
     ...:    pacf(stock_data['Logged First Difference'].iloc[1:]) 
```

#### 自動相関関数(ACT:Auto-Correlation Function)
これらの結果をプロットすると、有意な相関があるかどうかを確認できます。

 IPython
```
 In [25]: fig, ax = plt.subplots(figsize=(8,4))                             In [26]: ax.plot(lag_correlations, marker='o', linestyle='--')             Out[26]: [<matplotlib.lines.Line2D at 0x1a22690a90>]
 
```


![](https://gyazo.com/b4c75680387d2b4caaa371a62b02318f.png)

自己相関(ACF)と偏自己相関(PACF)の結果は互いに非常に近いことが確認できます。これは、時刻 `t` の値と `t` の前の任意の時点の値との間に最大40ステップ遅れの有意な（> 0.2）相関がないことになります。つまり、この結果は、S&P500インデックスの時系列データがランダムウォークだということを表しています。

時系列データ分析のもう1つの手法は、**分解(decompose)**です。これは、時系列をトレンド、季節、残差の要素に分解して観察する手法です。  `statsmodels` には、これを行うことができる関数が提供されています。

 IPython
```
 In [27]: from statsmodels.tsa.seasonal import seasonal_decompose 
     ...:  
     ...: decomposition = seasonal_decompose(stock_data['Natural Log'],
     ...:                     model='additive', period=30) 
     ...: fig = plt.figure() 
     ...: fig = decomposition.plot()  
```

![](https://gyazo.com/8e4c6a8b75cdc3e52622bcac8ae5a399.png)

S&P500インデックスには周期が存在しないため、季節要素（seasonal_decompose)の視覚化はそれほど意味がありません。
S&P500インデックスはランダムウォークであり、遅延変数はそれほど影響を与えていないように観察できます。

次に、**自己回帰和分移動平均モデル(ARIMAモデル)** をいくつか当てはめて、得られる結果を確認することができます。 
簡単な移動平均モデルから始めましょう。

 IPython
```
 In [28]: model = sm.tsa.ARIMA(stock_data['Natural Log'].iloc[1:], 
     ..:                        order=(1, 0, 0))
     ...: results = model.fit(disp=-1) 
     ...: stock_data['Forecast'] = results.fittedvalues 
     ...: stock_data[['Natural Log', 'Forecast']].plot(figsize=(8,4))       Out[28]: <matplotlib.axes._subplots.AxesSubplot at 0x1a26077240>       
```


![](https://gyazo.com/10e940d02fb9e02f923244552dbe043b.png)
一見するとうまくプロットできているように見えますが、対数変換されたデータと予測値には
差がないため重なっています。
対数差分変換されたデータでみてみましょう。
IPython
```
 In [30]: model = sm.tsa.ARIMA(
     ...:                stock_data['Logged First Difference'].iloc[1:], 
     ...:                order=(1, 0, 0)) 
     ...: results = model.fit(disp=-1) 
     ...: stock_data['Forecast'] = results.fittedvalues 
     ...: stock_data[['Logged First Difference', 'Forecast']].plot(figsize=(8,4)) 
     ...:  
```

![](https://gyazo.com/009c57b074ced21a2a709acd490d05bd.png)

予測値の変化が平坦に見えるのは、実際の変化と比べてはるかに小さいためです。
ズームアップして比較してみましょう。

 IPython
```
 In [39]: stock_data[['Logged First Difference',
     ...:        'Forecast']].iloc[12000:12200, :].plot(figsize=(8,4))                                               
```

![](https://gyazo.com/52414e70ce32f1191a4b012eb64ccf80.png)

実は、ランダムウォークな時系列データの単純移動平均モデルは、有効的ではありません。
それは、前日の情報だけで翌日に何が起こるかを正確に予測することはできないからです。

それに、この程度の分析で簡単に予測できるのであれば、皆が実行しているはずですよね。
ただ、長期的な上昇傾向は観察できたので、買ったら売らない（Buy and Hold)でいるか、ETF(Exchange Traded Fund：上場投資信託)で定期的に定額分買い増すことを続けていれば、利益が出やすくなっていると考えられます。
あくまで過去５０年の観察と仮定と憶測です、未来を予測するものではありませんが...


参考:
- [statsmodels オフィシャルサイト ](https://www.statsmodels.org/stable/index.html)
- [Duke大学 Statistical forecasting: notes on regression and time series analysis http://people.duke.edu/~rnau/411home.htm]



