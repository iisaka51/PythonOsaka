Luxで探査的データ分析をしてみよう
=================

![](https://gyazo.com/6e41ac8eba279abb964e928c53275688.png)

# はじめに
効率的なデータ探索のための現在の課題
Python にはデータ分析のためのライブラリが豊富にあります。それらの協力なツールであっても、データ探索の流れを阻害する課題が存在します。特に、頭の中にある疑問から、実用的な洞察を得る可視化処理では、その傾向が顕著になりあす。
おもに次のような障害があげられます。

  - コードとインタラクティブなツールの間の大きなギャップ
  - プロットには多くのコードと事前の設定が必要になること
  - 試行錯誤は退屈で、手間に圧倒されること

データについて推論し考える方法と、そこから洞察を得るために実際にデータに対して行われる必要があることとの間には、非常に大きなギャップが存在します。この資料は、こうしたギャップを補完するため Lux について説明するためのものです。

# Luxについて
[Lux https://pypi.org/project/lux/] は、データを可視化するためのインテリジェントPython ライブラリです。探索的データ解析の可視化処理を自動化する Jjupyterウィジェットを通して視覚的発見が容易になります。
インタラクティブなLuxウィジェットは、ユーザーがデータを素早く参照し、重要なトレンドやパターンを確認できるよう支援してくれます。また、ユーザーがさらに分析するための推奨事項も提供してくれます。さらに、Luxは、あなたがまだ明確な考えを持っていないデータのための可視化も提供してくれます。

Luxには次のような機能があります。

  - Jupyterノートブックへの直接アクセスによるインタラクティブな可視化を提供
  - ユーザーが分析対象を指定することで、コード量を大幅に削減することができる
  - データフレームを自動的に可視化してユーザに推奨する

# インストール

Lux のインストールは次のように行います。


```
 # Linux or MacOS
 $ python -m pip install lux-api

 # Windwos
 $ py -3 -m pip install lux-api
```

Jupyter Notebook の拡張機能を有効にしておきます。

```
 $ jupyter nbextension install --py luxwidget
 $ jupyter nbextension enable --py luxwidget

```

## Jupyterlab の場合
### NodeJS のインストール
使用しているプラットフォームにNodeJSがインストールされていない場合は、次の手順でNodeJSをインストールしておきます。ここでは、nodebrew を使ってNodeJSのバージョン管理をしていますが、nodenev を使っても構いません。

```
 # macOS
 $ brew install nodebrew
 $ mkdir -p $HOME/.nodebrew/src
 $ nodebrew install v18.1.0
 $ nodebrew use v18.1.0
```

PATHを通しておきます。

```
 $ echo 'export PATH=$HOME/.nodebrew/current/bin:$PATH' >> ~/.bash_profile
```

 zsh
```
 $ echo 'export PATH=$HOME/.nodebrew/current/bin:$PATH' >> ~/.zprofile
```


### Jupyterlab の拡張機能を有効化


```
 $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
 $ jupyter labextension install jupyter-matplotlib
 $ jupyter labextension install luxwidget
```

Jupyter のセルで以下を実行してエラーが表示されなければOKです。

```
 import lux
 lux.debug_info()
```

![](https://gyazo.com/a09f6a68c9ae8e02ab6ccf72b5597536.png)

# Luxの使用方法
Lux は Jupyterlab/Jupyter Notebook から利用します。
まずセルに次のコードを入力して実行します。


```
 import lux
 import pandas as pd
```

通常のように　Jupyter Notebook を使うだけです。

![](https://gyazo.com/9375b272eef2e2079564f0fd3c89b641.png)
違いに’気づきましたか？ Toggle Pandas/Lux のボタンが追加されています。これをクリックすると、データセットに存在する量的変数間の関係をプロットしてくれます。複数表示される場合の表示順序は、相関の強いものから弱いものです。


![](https://gyazo.com/750effd21c485ad27ca6247c0232f7ad.png)
データに欠損値などがあるときは黄色い三角のアイコンが表示されます。これをクリックすると下部に情報が表示されます。
すぐ隣のボタン Distribution タブでデータセット中の量的変数のヒストグラムを表示します。表示順序は、大きく歪んでいるものから小さく歪んでいるものです。


![](https://gyazo.com/db6c15d4ffb51b730898a1766cc9fd70.png)
Occurrence タブはデータのカテゴリー属性の棒グラフが表示されます。その順序は、最も偏った分布から均等な分布へと並べられます。


![](https://gyazo.com/4ab2ae03f0fbd4584430f4043c8fbc60.png)

データ要約を知るための `describe()` メソッドを呼び出してみます。
![](https://gyazo.com/0b0cef556fd7f6a39b0ae56b241ad33d.png)

ここでも Toggle Pandas/Lux のボタンが表示されています。クリックすると


![](https://gyazo.com/3f67a69b3b95289be9e70f7095c6ee57.png)
![](https://gyazo.com/9dd4640258b1c63feb0aff14250987f1.png)

例えば、特定の機能または複数の機能をまとめて詳しく知りたいとします。データフレームの`intent`属性を使って、それらの属性に関連するすべての可視化を取得することができます。

 python
```
 df.intent = ['age', 'fare']
 df
```

Luxウィジェットは、意図した機能の可視化を表示するだけではありません。FilterとEnhance を使うことで、より多くの分析のための追加推奨事項を提供します。

![](https://gyazo.com/954e51aedfe3baf08d232bdd8e40b129.png)
Enhance タブは、入力が1つの特徴量の場合、X軸に目的変数を固定し、異なる属性と比較することで推奨の可視化を提供してくれます。`intent`に2つの特徴量を与えたときは、X軸とY軸に目的変数を固定します。`df.intent=['age', 'fare']`としたときでは、X軸が `age` 、Y軸が `fare` で固定されます。

Filter タブは、X軸に意図した変数を固定し、データセットの異なる部分と比較することによって、推奨の可視化を提供してくれます。

# 可視化チャートのエクスポート
Lux は可視化を非常に簡単に共有することができます。プロットを静的なHTMLにエクスポートするには、次のコマンドを使用する必要があります。

 python
```
 df.save_as_html(“Filename.html”)
```


# まとめ
Lux を使うことで、ローコードでデータ分析を行うことができ、退屈で面倒な可視化処理が簡単になります。また、Luxが推奨して可視化するプロットに気付かされることも多く、データ分析の熟練者から初心者まで利用する価値が高いと言えます。注意点としては、Jupyter Notebook の利用が前提であるため、その構築と維持について十分理解しておく必要があります。とわいえ、これは将来的に情報共有や効率化といったリターンが期待できる価値ある投資といえるでしょう。



# 参考
- Lux
  - [PyPI - Lux](https://pypi.org/project/lux/)
  - [公式ドキュメント](https://lux-api.readthedocs.io/en/latest/)


