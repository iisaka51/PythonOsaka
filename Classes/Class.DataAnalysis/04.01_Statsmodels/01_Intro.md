statsmodels を使ってみよう
=================
### statsmodelsについて
statsmodelsは、異なる多くの統計モデルの推定、および統計的検定と統計データの分析のためのクラスと関数を提供する拡張モジュールです。 
統計処理や線形回帰分析や時系列データ分析を簡単に行えるようになります。

### インストール
拡張モジュールなので次のようにインストールします。
 bash condaの場合
```
 $ conda install statsmodels
 bash pipの場合
```
 $ pip install statsmodels
```

### データセット
statsmodels には学習用の [データセット ](https://www.statsmodels.org/devel/datasets/index.html) が付属しています。

- American National Election Survey 1996
- Breast Cancer Data
- Bill Greene’s credit scoring data.
- Smoking and lung cancer in eight cities in China.
- Mauna Loa Weekly Atmospheric CO2 Data
- First 100 days of the US House of Representatives 1995
- World Copper Market 1951-1975 Dataset
- US Capital Punishment dataset.
- El Nino - Sea Surface Temperatures
- Engel (1857) food expenditure data
- Affairs dataset
- World Bank Fertility Data
- Grunfeld (1950) Investment Data
- Transplant Survival Data
- (West) German interest and inflation rate 1972-1998
- Longley dataset
- United States Macroeconomic data
- Travel Mode Choice
- Nile River flows at Ashwan 1871-1970
- RAND Health Insurance Experiment Data
- Taxation Powers Vote for the Scottish Parliament 1997
- Spector and Mazzeo (1980) - Program Effectiveness Data
- Stack loss data
- Star98 Educational Dataset
- Statewide Crime Data 2009
- U.S. Strike Duration Data
- Yearly sunspots data 1700-2008

この他に次のデータも読み込むことができます。
- 出版社の [Stata Press社 https://www.stata-press.com/] が公開している[データセット ](https://www.stata-press.com/data/)
- 統計分析用アプリケーション `R` がサンプルとして配布している [Rデータセット ](https://vincentarelbundock.github.io/Rdatasets/datasets.html)

### データセットを読み込む方法

例えば、"pector and Mazzeo (1980) - Program Effectiveness Data(個別指導システムプログラム(PSI)の有効性に関する実験データ)" を例にとってみます。

データフレームに格納する方がいろいろ便利なので、pandas と併せてインポートします。
データは  `statsmodels.datasets` としてサブモジュールとして格納されています。

次のように読み込みます。
 IPython
```
 In [2]: # %load statsmodels_spector.py 
    ...: import pandas as pd 
    ...: import statsmodels.api as sm 
    ...:  
    ...: spector = sm.datasets.spector.load_pandas() 
    ...:                                                                    
```

読み込んだデータは  `sepctor.data` にデータフレームとして格納されています。
 IPython
```
 In [3]: spector.data.head()                                                     Out[3]: 
     GPA  TUCE  PSI  GRADE
 0  2.66  20.0  0.0    0.0
 1  2.89  22.0  0.0    0.0
 2  3.28  24.0  0.0    0.0
 3  2.92  12.0  0.0    0.0
 4  4.00  21.0  0.0    1.0
```

### Rデータセットを読み込む

Rデータセットを読み込むためには、次のように `get_rdataset()` を使います。
 IPython
```
 In [2]: # %load statsmodels_rdatasets.py 
    ...: import numpy as np 
    ...: import statsmodels.api as sm 
    ...: guerry = sm.datasets.get_rdataset("Guerry", "HistData")
    ...: querry.data.head().T
           
 Out[2]: 
                           0       1        2             3             4
    dept                   1       2        3             4             5
    Region                 E       N        C             E             E
    Department           Ain   Aisne   Allier  Basses-Alpes  Hautes-Alpes
    Crime_pers         28870   26226    26747         12935         17488
    Crime_prop         15890    5521     7925          7289          8174
    Literacy              37      51       13            46            69
    Donations           5098    8901    10973          2733          6962
    Infants            33120   14572    17044         23018         23076
    Suicides           35039   12831   114121         14238         16171
    MainCity           2:Med   2:Med    2:Med          1:Sm          1:Sm
    Wealth                73      22       61            76            83
    Commerce              58      10       66            49            65
    Clergy                11      82       68             5            10
    Crime_parents         71       4       46            70            22
    Infanticide           60      82       42            12            23
    Donation_clergy       69      36       76            37            64
    Lottery               41      38       66            80            79
    Desertion             55      82       16            32            35
    Instruction           46      24       85            29             7
    Prostitutes           13     327       34             2             1
    Distance         218.372  65.945  161.927       351.399        320.28
    Area                5762    7369     7340          6925          5549
    Pop1831           346.03     513   298.26         155.9         129.1
   
```

他のデータセットと同じように  `.data` にデータフレームとして格納されます。

### 統計分析
統計処理は SciPy や NumPy でも処理することができますが、statsmodels は統計に特化していて、より使いやすくなっています。もちろん、統計学の知識が必要にはなりますが...

statsmodels を使って線形回帰分析した例です。
見てわかるように、分析そのものは１行で済んでしまいます。
注：出力は紙面に収まるよう内容が変わらない範囲で修正しています。
 IPython
```
    ...: import statsmodels.formula.api as smf 
    ...: results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', 
    ...:                   data=guerry).fit() 
    ...: results.summary() 
    ...:                                                                           
 Out[2]: 
 <class 'statsmodels.iolib.summary.Summary'>
 """
                             OLS Regression Results                        
 ==========================================================================
 Dep. Variable:                Lottery   R-squared:                   0.348
 Model:                            OLS   Adj. R-squared:              0.333
 Method:                 Least Squares   F-statistic:                 22.20
 Date:                Thu, 02 Apr 2020   Prob (F-statistic):       1.90e-08
 Time:                        16:48:44   Log-Likelihood:            -379.82
 No. Observations:                  86   AIC:                         765.6
 Df Residuals:                      83   BIC:                         773.0
 Df Model:                           2                                     
 Covariance Type:            nonrobust                                     
 ==========================================================================
            　　　   coef    std err        t       P>|t|  [0.025　　 0.975]
 --------------------------------------------------------------------------
 Intercept     　246.4341    35.233     6.995   　  0.000  176.358   316.510
 Literacy       　-0.4889     0.128    -3.832      0.000    -0.743    -0.235
 np.log(Pop1831) -31.3114    5.977     -5.239      0.000   -43.199   -19.424
 ==========================================================================
 Omnibus:                        3.713   Durbin-Watson:               2.019
 Prob(Omnibus):                  0.156   Jarque-Bera (JB):            3.394
 Skew:                          -0.487   Prob(JB):                    0.183
 Kurtosis:                       3.003   Cond. No.                     702.
 ==========================================================================
 
 Warnings:
 [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
 """
```

次からは、分析についてもう少し詳しく説明していきます。

参考：
- [Statsmodels オフィシャルサイト ](https://www.statsmodels.org)



