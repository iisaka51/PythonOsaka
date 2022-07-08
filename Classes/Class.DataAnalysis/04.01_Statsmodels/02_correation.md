statsmodels で回帰分析をしてみよう
=================
### 回帰分析について
まず統計用語の説明からはじめます。
statsmodelsは一般的なものとは異なる統計学の専門用語や、名前がクラス、関数、メソッドに使われています。用語を理解することが、入力と出力の意味を理解するはじめの一歩となります。

ある２つの変量[$ x ] と [$ y ] があるとき、それぞを区別せずに対等なものとしてみることを、
#### 相関 (correlation)
要因となる数値([$ x ])と結果となる数値([$ y ])との関係を調べて、それぞれの関係を表す**モデル(model)**(定量的な関係の構造)に当てはめることを**回帰分析**といいます。

[$ x ]のとる値が[$ y ] の値に影響を与える要因となる、あるいは決定するような場合、[$ x ]を **独立変数 (independent variable)**、 [$ y ] を **従属変数 (dependent variable)** と言います。

### 線形回帰と非線形回帰
いま、変数 [$ x] と [$ y] があるとして、これを次のモデルに当てはめるとします。

[$ y = f(x)]

このとき [$ f(x)] は次のような１次関数だとします。

[$ f(x) = a x + b]

モデルは次のように書き換えることができます。

[$ y = ax + b]

このモデルは直線で表現できるものなので、[$ f(x) ] を**線形関数(linear function)**と呼びます。
回帰分析で線形関数をモデルとすることを**線形回帰(linear regression)** といいます。
これに対して、モデルが線形関数で表現できないときは、**非線形回帰(nonlinear regression)** といいます。

### 単回帰と重回帰
変量 [$ x ] が１次元のときを **単回帰(simple regression)**、２次元以上のときを **重回帰(multiple regression)** といいます。重回帰分析の場合は、複数の独立変数の合成変量と従属変数との間での相関を分析することになり、この複数の独立変数の合成変量と従属変数との間での相関係数を**重相関係数(R)(multiple correlation coefficient.)**、重相関係数の二乗を**決定係数(coefficient of determination)** と呼びます。([$ R^2]と表記されるのでR二乗値(R-Square)と呼ばれることもあります）
決定係数は、独立変数の合成変量が従属変数の分散を説明する割合（％）を表していて、決定係数のＦ検定(2つのデータ群のばらつきが等しいか（等分散）を調べること) によって、重回帰分析全体の有意水準を検討します。つまり、意味のある分析なのかを調べます。
重回帰分析に用いた個々の独立変数と他の独立変数の影響を除去した従属変数との間の関係の強さを示すものを **標準化偏回帰係数[$ \beta**（ベータ）] と呼びます。[$ \beta]に関してはｔ検定を行い、２つのグループの平均の差が偶然誤差の範囲内にあるかどうかを調べます。
単回帰分析の場合では、**２変数間の相関係数 [$ \gamma**(ガンマ)] が重相関係数 [$ \beta] と等しくなります。

### 最小二乗法
測定データ[$ x ] と [$ y ]に対して線形回帰分析を行うとき次のモデルを当てはめたいとします。

[$ y = f(x)]

このもっともらしい関数[$ f(x)] を推定するときに、次のように誤差([$ \varepsilon]) を考えます。

[$ y = f(x) + \varepsilon]

[$ f(x)] は線形関数とするので、グラフで表現すると直線になるはずです。
いま仮にモデルを次の式で表すとします。

[$ y = ax + b + \varepsilon]

[$ x_{i} ] に対する[$ y_{i}]はグラフの直線上から推定できる[$ y'_{i}]より、誤差([$ \varepsilon_{i}]) だけずれていると考えると、誤差は次の式で得られます。

[$ \varepsilon_{i} = y_{i} - (ax_{i} + b)]

つまり、誤差の二乗の総和が最小となるような [$ a] と [$ b] を求めればよいことになります。
これを**フィッテイング (Fitting)** といいます。

[$ \sum_{i} \left( y_{i}-(ax_{i}+b)\right) ^{2}]

誤差にはプラスとマイナスの値がありますが、誤差を二乗すると常にプラスになり、相殺を防ぐことができます。つまり、上下の方向を簡単にうまく消すことができるわけです。

誤差の二乗の総和が最小になるようにモデルを推定することを、**最小二乗法(least squares method)** といいます。

最小二乗法で推定できるモデルがもっともらしくあるためには、次の条件が必要になります。

- 誤差に偏りがないこと
- 誤差の分散は既知であること
- 各変量は独立であり、誤差の[共分散 ](https://ja.wikipedia.org/wiki/共分散) が 0 であること
  - データと推定値との間に関係性がないこと
- 誤差は正規分布にしたがうこと

### 最小二乗法を用いたモデルのデータへのフィッティング
statsmodels のドキュメントにある、[最小二乗法を用いたモデルのデータへのフィッティング ](https://www.statsmodels.org/stable/examples/notebooks/generated/chi2_fitting.html) 
について手順を説明してゆきます。
ここで用いられているのは線形回帰分析です。

位置 `x` の測定値 `y` と測定誤差 `y_err` を持つデータポイントがあると仮定します。
詳細は以下の論文を参照してもらうこととにし、この中の表１で提供されているデータを使っています。
[Data analysis recipes: Fitting a model to data, 2010 David W. Hogg (NYU, MPIA), Jo Bovy (NYU), Dustin Lang (Toronto, Princeton)  ](https://arxiv.org/abs/1008.4686)

したがって、モデルは次式となります。

[$ f(x) = ax + b]

この論文の、**加重最小二乗法（Weighted Least Squares:WLS)** によるフィッティングで得られるパラメタと誤差は次のようになっています。

[$ \widetilde a = 2.24 \pm 0.11]
[$ \widetilde b = 34 \pm 18]

はじめにデータを準備します。
 statsmodels_linerfitting_data.py
```
 import numpy as np
 import pandas as pd
 import statsmodels.api as sm
 
 data = """
   x   y y_err
 201 592    61
 244 401    25
  47 583    38
 287 402    15
 203 495    21
  58 173    15
 210 479    27
 202 504    14
 198 510    30
 158 416    16
 165 393    14
 201 442    25
 157 317    52
 131 311    16
 166 400    34
 160 337    31
 186 423    42
 125 334    26
 218 533    16
 146 344    22
 """
 try:
     # for Python 2.x
     from StringIO import StringIO
 except ImportError:
     from io import StringIO
 
 data = pd.read_csv(StringIO(data),
                    delim_whitespace=True).astype(float)
```

 IPython
```
 In [1]: %run statsmodels_linerfitting_data.py                              
 In [2]: data.head()                                                        Out[2]: 
        x      y  y_err
 0  201.0  592.0   61.0
 1  244.0  401.0   25.0
 2   47.0  583.0   38.0
 3  287.0  402.0   15.0
 4  203.0  495.0   21.0
```

このデータを直線を当てはめるには、加重最小二乗法クラス `WLS` を使用します。
注：出力は紙面に収まるよう内容が変わらない範囲で修正しています。
 IPython
```
 In [4]: # %load statsmodels_linerfitting_estimate.py 
    ...: exog = sm.add_constant(data['x']) 
    ...: endog = data['y'] 
    ...: weights = 1. / (data['y_err'] ** 2) 
    ...: wls = sm.WLS(endog, exog, weights) 
    ...: results = wls.fit(cov_type='fixed scale') 
    ...: print(results.summary()) 
    ...:                                                                           
                             WLS Regression Results                        
 ==========================================================================
 Dep. Variable:                      y   R-squared:                   0.400
 Model:                            WLS   Adj. R-squared:              0.367
 Method:                 Least Squares   F-statistic:                 193.5
 Date:                Tue, 07 Apr 2020   Prob (F-statistic):       4.52e-11
 Time:                        05:10:12   Log-Likelihood:            -119.06
 No. Observations:                  20   AIC:                         242.1
 Df Residuals:                      18   BIC:                         244.1
 Df Model:                           1                                     
 Covariance Type:          fixed scale                                      
 ==========================================================================
                  coef    std err          z      P>|z|      [0.025  0.975]
 --------------------------------------------------------------------------
 const        213.2735     14.394     14.817      0.000     185.062 241.485
 x              1.0767      0.077     13.910      0.000       0.925   1.228
 ==========================================================================
 Omnibus:                        0.943   Durbin-Watson:               2.901
 Prob(Omnibus):                  0.624   Jarque-Bera (JB):            0.181
 Skew:                          -0.205   Prob(JB):                    0.914
 Kurtosis:                       3.220   Cond. No.                     575.
 ==========================================================================
 
 Warnings:
 [1] Standard Errors are based on fixed scale
```


 `WLS` クラスの引数はパラメーターは次のように呼び出されます。

```
 sm.WLS(endog, exog, weights)
```

 `endog` は従属変数、 `exog` は独立変数、 `weights` は重みです。
 `exog` は、 `x` を列とし、定数項（切片の初期値）として１を列として追加とした2次元配列である必要があります。
この定数項の列を追加することは、次のモデルに近似させることを意味しています。

[$ y = ax + b]

定数項を与えないと、次のモデルに近似させることを意味します。

[$ y = ax]

また、オプション `cov_type = 'fixed scale'` を使用して、絶対スケールで誤差があると設定しています。
これを与えないと、statsmodelsは重み( `weights` )をデータポイント間の相対加重として扱い、最適なモデル（次式）となるようにそれらを内部的に再スケーリングします。

[$ \frac{ \chi ^2 }{ndf}]　　[$ \chi ^2]= 残差の自乗和、 [$ ndf] = 自由度


> 残差(residual)
> 統計学においては、誤差の推定量をいい、データと予測値との乖離を表します。
>
> 自由度(NDF:number of degree of freedom)
> 統計学においては自由に値を取れるデータの数のことをいいます。
> 基本的にサンプルサイズ[$ n]の標本の自由度は[$ n]になります。
> この標本 に [$ \overline x] という平均値があり、平均値が変わらないようにしたいとき、
> [$ x_{n-1}]の値は自由な値をとれますが、[$ x_{n}] は自由な値をとることができません。
> このときの自由度は [$ n - 1]となります。
> [$ n ] 個のデータの間に、[$ k ] 個の条件があるときの自由度は [$ n - k] となります。

SciPyの最適化ライブラリから  `scipy.optimize.curve_fit` を用いて、 `WLS` でのフィッティングをチェックします。

 IPython
```
 In [6]: # %load statsmodels_linerfitting_check.py 
    ...: from scipy.optimize import curve_fit 
    ...:  
    ...: def f(x, a, b): 
    ...:     return a * x + b 
    ...:  
    ...: xdata = data['x'] 
    ...: ydata = data['y'] 
    ...: p0 = [0, 0] # initial parameter estimate 
    ...: sigma = data['y_err'] 
    ...: popt, pcov = curve_fit(f, xdata, ydata, p0, sigma,
    ...:                        absolute_sigma=True) 
    ...: perr = np.sqrt(np.diag(pcov)) 
    ...: print('a = {0:10.3f} +- {1:10.3f}'.format(popt[0], perr[0])) 
    ...: print('b = {0:10.3f} +- {1:10.3f}'.format(popt[1], perr[1])) 
    ...:                                                                           
 a =      1.077 +-      0.077
 b =    213.273 +-     14.394
```

独自に定義した**目的関数(cost function)** でチェック
 `scipy.optimize.minimize` を使用して独自の目的関数を作成することもできます。
 IPython
```
 In [8]: # %load statsmodels_linerfitting_costfunction.py 
    ...: from scipy.optimize import minimize 
    ...:  
    ...: def chi2(pars): 
    ...:     """Cost function. 
    ...:     """ 
    ...:     y_model = pars[0] * data['x'] + pars[1] 
    ...:     chi = (data['y'] - y_model) / data['y_err'] 
    ...:     return np.sum(chi ** 2) 
    ...:  
    ...: result = minimize(fun=chi2, x0=[0, 0]) 
    ...: popt = result.x 
    ...: print('a = {0:10.3f}'.format(popt[0])) 
    ...: print('b = {0:10.3f}'.format(popt[1])) 
    ...:                                                                           
 a =      1.077
 b =    213.274
```

２つが非常に近い値となっていて、先のWLSのフィッティングがよいものだとわかります。
 curve_fit() の結果
```
  a =      1.077 +-      0.077
  b =    213.273 +-     14.394
```

 独自に定義した目的関数の結果
```
  a =      1.077
  b =    213.274
```

statsmodels のドキュメントでは行っていませんが、ここで推定したモデルとデータをプロットしてみましょう。
 Ipython
```
 In [44]: # %load statsmodels_linerfitting_plot.py 
     ...: import matplotlib.pyplot as plt 
     ...:  
     ...: xp = results.predict(exog) 
     ...:  
     ...: fig, ax = plt.subplots() 
     ...: ax.plot(data['x'].values, data['y'].values, 'o', label="Data") 
     ...: ax.plot(data['x'].values, xp.values,'r', label='WLS') 
     ...: ax.legend(loc="best"); 
     ...:                                                                   
```
![](https://gyazo.com/799894f31e56d3f37e3a6a413f52b812.png)

いかにも線形回帰というような直線が描かれていますね。

### exog と endog
前述の例にあるコードで、 `exog` と  `endog` という見慣れない２つの単語がでてきました。
これは、独立変数と従属変数を表すものです。
統計学の教科書や統計アプリケーションでは色々な表記がされるようです。
(参考: [endog, exog, what’s that?  ](https://www.statsmodels.org/stable/endog_exog.html))

 exog と endogの別表記

| exog | endog |
|:--|:--|
| 外生変数 (exogenous variable) | 内生変数 (endogenous variable) |
| 独立変数(independent variable) | 従属変数(dependent variable) |
| 説明変数 (explanatory variable) | 目的変数 (objective variable) |
| 予測変数 (predictor variable) | 結果変数 (outcome variable) |
| x | y |


### サマリー出力の意味
サマリー出力のパラメタの意味を次に示します。
 sumarryの意味

| パラメータ | 説明 |
|:--|:--|
| R-squared | 決定係数 |
|  | 回帰によって導いたモデルの当てはまりの良さを表現します |
|  | ０〜１の範囲の値で、1に近いほど精度の高いモデルとなります |
| Adj. R-squared | 自由度調整済み決定係数 |
|  | 決定係数は独立変数が増えるほど1に近づく性質があります |
|  | 独立変数が多いときは決定係数ではなくこの値を利用します |
| AIC | 赤池情報量規準（AIC：Akaike’s Information Criterion） |
|  | 有限のモデルセットの中からモデルを選択するための基準 |
|  | 特定のデータセットに対するモデルの品質の相対的な尺度 |
|  | 相対的な値で、小さいほど精度が高くなります |
| BIC | ベイジアン情報基準（BIC:Bayesian information criterion) |
|  | 有限のモデルセットの中からモデルを選択するための基準 |
|  | モデルのパラメーターの数にペナルティ項を導入することで、 |
|  | オーバーフィッティングを防ぎやすくなります |
|  | 時系列のモデル同定と線形回帰に広く使用されます |
| F-statistic | F 統計値 |
|  | モデルまたはモデルの成分の有意性を表す検定統計量 |
| Prob (F-statistic) | F統計値の有意性を表します |
| Log-Likelihood | 対数尤度（たいすうゆうど) |
|  | ある前提条件に従って結果が出現するとき、 |
|  | 逆に観察結果からみて前提条件が「何々であった」と |
|  | 推測するもっともらしさを表す数値 |
| coef | 変動係数(coefficient value) |
|  | 標準偏差を平均値で割った値 |
|  | 単位の異なるデータのばらつきや、平均値に対するデータとばらつきを |
|  | 相対的に評価するときに用います |
| std err | 標準誤差(standard error) |
|  | 推定量の標準偏差でデータから得られる推定量のバラつきを表します |
| t | T統計値 (T Value) |
|  | それぞれの独立変数が従属変数に与える影響の大きさを表します |
|  | 絶対値が大きいほど影響が強いことを意味します |
|  | 一般的に、t値の絶対値が2より小さい場合は |
|  | 統計的にはその独立変数は従属変数に影響しないと考えます |
| p | P統計値 (P Value) |
|  | それぞれの独立変数の係数の有意確率を表します |
|  | 一般的に、有意確率が有意水準以下(5%を下回っている）ならば、 |
|  | その独立変数は従属変数に対して有意性が高いと言われます |
|  | つまり、関係性が強いことになります |
| ［0.025 0.975］ | 95%信頼区間 |
|  | 母平均が95%の確率でその範囲にあるということを表します |
| Omnibus | オムニバス検定値 (Omnibus test) |
|  | グローバル検定(global test)と呼ばれることもあります。 |
|  | ３つ以上のデータ群がある時に全ての群の組み合わせのどれかは不明だが、 |
|  | 少なくともどこか１つに母平均に異なるものがあるかを調べる検定 |
| Prob(Omnibus) | オムニバス検定値の有意性を表す |
| Skew | 歪度 (わいど: skewness) |
|  | 分布が正規分布からどれだけ歪んでいるかを表す統計量 |
|  | 左右対称性の度合いを示しています |
| Kurtosis | 尖度 (せんど) |
|  | 分布が正規分布からどれだけ逸脱しているかを表す統計量 |
|  | 山の尖りと裾の広がりの度合いを示しています |
| Durbin-Watson | ダービン=ワトソン比 (Durbin-Watson ratio) |
|  | 実測値と理論値の差に自己相関があるかないかを判別するための指標 |
|  | 回帰分析では、異なる誤差項間には相関がないことを仮定しているため、 |
|  | この値をチェックするようにします |
| Jarque-Bera (JB) | ジャック＝ベラ検定 (Jarque–Bera test)、JB検定 |
|  | 標本データの尖度と歪度が正規分布に従っているかを判別するための指標 |
| Prob(JB) | JB検定の有意性を表します |
| Cond. No. | 条件数 (condition number) |
|  | 多重共線性(multicollinearity) をチェックする指標 |
|  | 多重共線性が存在すると解析結果が安定性を欠いてしまいます |
|  | ⚫ 分析結果における係数の標準誤差が大きくなる |
|  | ⚫ T統計値が小さくなる |
|  | ⚫ 決定係数が大きな値になる |
|  | ⚫ 回帰係数の符号が本来なるべきものとは逆の符号になる |

### 重回帰分析を用いた推定
statsmodels のドキュメントにある [重回帰分析を用いた推定  ](https://www.statsmodels.org/stable/examples/notebooks/generated/predict.html) について手順を説明してゆきます。
まず、まず0から20までで等間隔の数値を50個生成します。( `x1` )
 Ipython
```
 In [1]: import numpy as np 
    ...: import statsmodels.api as sm 
    ...:  
    ...: nsample = 50 
    ...: sig = 0.25 
    ...:  
    ...: x1 = np.linspace(0, 20, nsample) 
    ...:                                                                    
 In [2]: x1[:5]                                                             Out[2]: array([0.        , 0.40816327, 0.81632653, 1.2244898 , 1.63265306])
 
 In [3]: len(x1)                                                            Out[3]: 50
```

 `x1 ` は１次元配列です。`np.sin(x1) ` は` x1` の各値から  `sin()` を求めた配列、 `x1` の各値から５を減算して二乗した配列、この３つの配列（３変量）を列としてスタックして、
2次元配列( `X` ) を生成して独立変数とします。
 IPython
```
 In [4]: X = np.column_stack((x1, np.sin(x1), (x1-5)**2))                   
 In [5]: X[:3]                                                              Out[5]: 
 array([[ 0.        ,  0.        , 25.        ],
        [ 0.40816327,  0.39692415, 21.0849646 ],
        [ 0.81632653,  0.72863478, 17.5031237 ]])
 In [6]: X.shape                                                            Out[6]: (50, 3)
```

独立変数( `X` ) に定数項(ｙ軸切片の初期値）を追加して 50x4 の２次元配列にします。
 IPython
```
 In [8]: X=sm.add_constant(X)                                               In [9]: X[:3]                                                              Out[9]: 
 array([[ 1.        ,  0.        ,  0.        , 25.        ],
        [ 1.        ,  0.40816327,  0.39692415, 21.0849646 ],
        [ 1.        ,  0.81632653,  0.72863478, 17.5031237 ]])
 In [10]: X.shape                                                           Out[10]: (50, 4)
```

この `X` に 1x4 の一次配列( `beta` ) を乗算して、真のデータ( `y_true` )を得ます。
 IPython
```
 In [16]: beta = [5., 0.5, 0.5, -0.02] 
     ...: y_true = np.dot(X, beta)                                                 
 In [17]: y_true.shape                                                      Out[17]: (50,)
 
 In [18]: y_true[:5]                                                        Out[18]: array([4.5       , 4.98084442, 5.42241818, 5.79747174, 6.08858976])
```

この真のデータ( `y_true` )に乱数を使ってばらつかせたもの計測データ( `y` )とします。
 IPython
```
 In [21]: y = y_true + sig * np.random.normal(size=nsample)                 In [22]: y.shape                                                           Out[22]: (50,)
 
 In [23]: y[:5]                                                             Out[23]: array([4.95491086, 5.00064383, 5.05920143, 5.52842715, 5.9143814 ])
```

この２つのデータ( `X` と `y` )に対して回帰分析を行います。
 `X` は 50x4 の２次元配列で３つの変量と１つの定数項を持っていて、これを変量 `y` との関係を調べるので重回帰分析となります。
注：出力は紙面に収まるよう内容が変わらない範囲で修正しています。
 IPython
```
 In [4]: # %load statsmodels_estimate.py 
    ...: olsmod = sm.OLS(y, X) 
    ...: olsres = olsmod.fit() 
    ...: print(olsres.summary()) 
    ...:                                                                           
                             OLS Regression Results                         
 ==========================================================================
 Dep. Variable:                      y   R-squared:                   0.982
 Model:                            OLS   Adj. R-squared:              0.981
 Method:                 Least Squares   F-statistic:                 846.4
 Date:                Tue, 07 Apr 2020   Prob (F-statistic):       3.11e-40
 Time:                        18:09:03   Log-Likelihood:            -2.1851
 No. Observations:                  50   AIC:                         12.37
 Df Residuals:                      46   BIC:                         20.02
 Df Model:                           3                                 
 Covariance Type:            nonrobust                                         
 ===========================================================================
                  coef    std err          t      P>|t|      [0.025   0.975]
 --------------------------------------------------------------------------
 const          4.9378      0.090     54.971      0.000       4.757   5.119
 x1             0.5015      0.014     36.203      0.000       0.474   0.529
 x2             0.5115      0.054      9.393      0.000       0.402   0.621
 x3            -0.0194      0.001    -15.984      0.000      -0.022  -0.017
 ===========================================================================
 Omnibus:                        0.716   Durbin-Watson:               2.415
 Prob(Omnibus):                  0.699   Jarque-Bera (JB):            0.823
 Skew:                           0.205   Prob(JB):                    0.663
 Kurtosis:                       2.524   Cond. No.                     221.
 ===========================================================================
 
 Warnings:
 [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

もとの独立変数( `X` ) をこのモデルに当てはめてた推定値( `ypred` ) を得ます。
 Ipython
```
 In [26]: ypred = olsres.predict(X)                                         In [27]: ypred.shape                                                       Out[27]: (50,)
 
 In [28]: ypred[:5]                                                         Out[28]: array([4.50622128, 4.94335679, 5.34781753, 5.6976672 , 5.97888622])
```

新しいい独立変数( `Xnew` )を作成し、このモデルに当てはめた推定値( `ynewpred` )を得ます。
 IPython
```
 In [29]: x1n = np.linspace(20.5,25, 10) 
     ...: Xnew = np.column_stack((x1n, np.sin(x1n), (x1n-5)**2)) 
     ...: Xnew = sm.add_constant(Xnew) 
     ...: ynewpred =  olsres.predict(Xnew)                                         
```

はじめに推定した( `ypred` )と、今回推定した( `ynewpred` ) をプロットして比較します。
 IPyhton
```
 In [30]: %matplotlib                                                              
 Using matplotlib backend: MacOSX
 
 In [31]: import matplotlib.pyplot as plt 
     ...:  
     ...: fig, ax = plt.subplots() 
     ...: ax.plot(x1, y, 'o', label="Data") 
     ...: ax.plot(x1, y_true, 'b-', label="True") 
     ...: ax.plot(np.hstack((x1, x1n)), np.hstack((ypred, ynewpred)), 
     ...:         'r', label="OLS prediction") 
     ...: ax.legend(loc="best");                                                   
```

![](https://gyazo.com/7af7c452a4c9b3c4e3adb1e7a91089bb.png)
良い具合にフィッティングできていて、モデルがもっともらしいことがわかります。

これを、計算式を用いると、推定と予測の両方がはるかに簡単になります。
これには、 `statsmodels.formula.api` の `ols` を使用します。
 `ols` の第１引数がモデル式です。
 IPython
```
 In [32]: from statsmodels.formula.api import ols 
     ...:  
     ...: data = {"x1" : x1, "y" : y} 
     ...: res = ols("y ~ x1 + np.sin(x1) + I((x1-5)**2)", data=data).fit()  
 
 In [33]: res.params                                                        Out[33]: 
 Intercept           4.988362
 x1                  0.494574
 np.sin(x1)          0.402507
 I((x1 - 5) ** 2)   -0.019286
 dtype: float64
        
```

得られた  `res` オブジェクトの `predict()` にあたらしい変量を与えるだけで、推定値がが求まります。
 IPython
```
 In [34]: res.predict(exog=dict(x1=x1n))                                    Out[34]: 
 0    10.894985
 1    10.774052
 2    10.561026
 3    10.291878
 4    10.013959
 5     9.774408
 6     9.608607
 7     9.531522
 8     9.534037
 9     9.585186
 dtype: float64
```

### プロパティー
回帰分析(WLS, OLS)が返すオブジェクトには、サマリーで表示されるそれぞれのパラメタに該当するプロパティーがあり、必要なパラメタを直接参照することもできます。

 sumarryと該当するプロパティー

| パラメータ | プロパティ | 意味 |
|:--|:--|:--|
| R-squared | rsquared | 決定係数 |
| Adj. R-squared | rsquared_adj | 自由度調整済み決定係数 |
| AIC | aic | 赤池情報量規準 |
| BIC | bic | ベイジアン情報基準 |
| F-statistic | fvalue | F 統計値 |
| Prob (F-statistic) | f_pvalue | F統計値の有意性を表す |
| Log-Likelihood | llf | 対数尤度（たいすうゆうど) |
| std err | bse | 標準誤差 |
| t | tvalues | T統計値 |
| p | pvalues | P統計値 |


参考：
- [Statsmodels オフィシャルサイト ](https://www.statsmodels.org)
- [Statsmodels - Ordinary Least Squares ](https://www.statsmodels.org/dev/examples/notebooks/generated/ols.html)
- [Sci-Pursuit.com - 最小二乗法の意味と計算方法 - 回帰直線の求め方 ](https://sci-pursuit.com/math/statistics/least-square-method.html)
- [統計学英語 Statistics & English http://www.cottonpot01.com/JpnEng/JpnEngSta120160825.pdf]



