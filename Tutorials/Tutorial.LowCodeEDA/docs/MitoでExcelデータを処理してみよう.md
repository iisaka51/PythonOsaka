MitoでExcelデータを処理してみよう
=================

![](https://gyazo.com/f37bf9cff6c160caaa010dd2898fc9df.png)

## はじめに

Mito は Jupyterlab をベースにしたPythonの拡張モジュールです。
次のような機能を提供しています。

- ポイント＆クリックでCSVやXLSXをインポート
- Excelスタイルのピボットテーブル
- グラフ作成
- フィルタリングとソート
- マージ(ルックアップ)
- エクセル形式の計算式
- 列の要約統計
- ユーザインタフェースでの操作のPythonコードを自動生成

Excelスタイルのピボットテーブは、膨大なデータを集計したり、分析したりできるExcelの機能です。このピボットテーブルを活用すれば、売上分析や勤怠管理などのデータのグラフ化など、面倒な作業が効率化されます。また、関数や数式を使わないのこともあり、Excel初心者にも使いやすい強力な機能で利用しているEXCELユーザも多いものです。
Python でも Pandas の `pivot_table()` 関数を使うと、Excelのピボットテーブル機能と同様の処理が実現できますが、PythonおよびPandasの知識が必要になり、Excelでのマウス操作だけでデータ分析/可視化といった利用方法ではありませんでした。
mito はユーザインタフェースで行った操作に該当するPythonコードを自動生成してくれるため、ExcelになれたPythonの初心者にも利用価値が高い優れたライブラリです。

## インストール

### Jupyterlab をインストール

Mito は　Jupyterlab を使用しているため、
事前にインストールしておく必要があります。

Anaconda Python をインストールしているのであれば、
すでに利用できる環境にあるはずです。


```
 # Linux or MacOS
 $ EXTRA="jupyter-nbextensions-configurator jupyter-contrib-nbextensions"
 $ python -m pip install jupyterlab  ${EXTRA}
```


ノートブックを保存するディレクトリを作成します。

```
 $ mkdir $HOME/notebooks
```

設定ファイルを生成します。

```
 $ jupyterlab --generator-conf
```

必要に応じて jupyter_notebook_config.py の内容を修正します。

デフォルトは次のようになっています。

```
 #c.NotebookApp.port = 8888
 #c.NotebookApp.notebook_dir = ''
 #c.NotebookApp.password = ''
 #c.NotebookApp.open_browser = True
```


### ノートブックのディレクトリを指定する

$HOME と記述できないので先頭で、
athlib モジュールを利用できるようインポートしておきます。

```
 from pathlib import Path
```

```
 c.NotebookApp.notebook_dir = Path.home() / 'notebooks'
```

### jupyter のログインでパスワードを強制させる

```
 $ python -c "from notebook.auth import passwd; print(passwd())"
```

パスワード入力と確認のための再入力後に、表示される文字列を
 `~/.jupyter/jupyter_notebook_config.py`  に設定する

```
 # c.NotebookApp.password = ''
 c.NotebookApp.password = '........'
```

設定ファイルは `$HOME/.jupyter/jupyterlab_notebook_config.py` に配置します。

### Jupyterlab の拡張機能を設定


```
 $ jupyter contrib nbextension install --user
 $ jupyter-labextension install jupyterlab-drawio
```

このあと、 次のようにコマンドを実行して jupyterlab が起動できることを確認してお>きます。

 bash
```
 $ jupyter  lab
```


### Mito のインストール

Mito のインストールは次のように行います。

```
 # Linux or MacOS
 $ python -m pip install mitoinstaller
 $ python -m mitoinstaller install

 # Windwos
 $ py -3 -m pip install mitoinstaller
 $ py -3 -m mitoinstaller install
```


インストールが成功すると Jupyterlab が起動します。
次の内容のセルがあるノートブックが開かれます。


```
 # Run this cell to render a mitosheet
 # See mito's documentation here: https://docs.trymito.io/how-to/creating-a-mitosheet
 # Join our Discord for support here: https://discord.gg/XdJSZyejJU

 import mitosheet
 metosheet.start()
```

このセルを実行すると、mito を使用できるわけですが、初回はメールアドレスを登録するダイアログが表示されます。

![](https://gyazo.com/17018b972bccaae531f503342f0b2d08.png)
メールアドレスを入力すると有料バージョン（月額10USD) の Mito Pro の案内が表示されます。ここは、「No Thanks」をクリックします。

![](https://gyazo.com/19d93f723b620974b19874a8c989aa88.png)

すると次のようなダイアログが表示されます。


![](https://gyazo.com/d453dbb524b9efc23fca9e4b5bf9657e.png)

表示されている内容はつぎのようなものです。

> Mito プライバシーに配慮しています
> お客様の個人情報がコンピュータの外に漏れることがないように配慮しています。
> CCPAに準拠したプライバシーポリシーは[こちら](https://privacy.trymito.io/privacy-policy]) をご覧ください。

ここは「Accept」をクリックすると、mito のツールバーを操作できるようになります。


![](https://gyazo.com/f8823732a8cf96297e3dbe3a6a1f2944.png)

ここに表示されていることは、データを取り込んでいない場合は、datagrameオブジェクトをmitosheet.sheetのセルに渡すか、ツールバーのimport ボタンをクリックしてねということ。

ツールバーの `[IMPORT]`をクリックするとファイルブラウザが表示されるので、読み込みたいファイルを指定します。

![](https://gyazo.com/8a3b4bd78505d2749399d869a2ed5533.png)

ヘッダなどの調整も行えます。

![](https://gyazo.com/e84688cb07097a4f9ba039e47904731d.png)

![](https://gyazo.com/bdc97da5f2877edb5dd762dc7de68f20.png)

データを読み込んだ操作を行うためのコードも自動生成されます。

```
 from mitosheet import *; register_analysis('UUID-1b44f57a-4464-4ade-81b5-d1da6d3ed411')

 # Imported TSLA.xlsx
 import pandas as pd
 sheet_df_dictonary = pd.read_excel('TSLA.xlsx', engine='openpyxl', sheet_name=['Sheet1'], skiprows=0)
 Sheet1 = sheet_df_dictonary['Sheet1']

```

インポートされたデータはシートとして追加されていきます。シートのタブをクリックするとそのデータにアクセスできるようyになります。

## グラフ表示

 `[GRAPH]` をクリックするとグラフの設定メニューが表示されます。 Graph Type を line にして、　`X-axis` に `Date` 、`Y-axis` に `Adj Close` のカラムデータを割り当ててみましょう。すると株価推移のグラフが表示されます。

![](https://gyazo.com/df8b41f80d329869f64113f197360bac.png)

mito のユーザインタフェースで行った操作は、 Python コードとしてその下部のセルに自動生成されています。
次回以降はこのコードを参考や再利用することでマウスを操作することなく処理することができるわけです。


```
 from mitosheet import *; register_analysis('UUID-1b44f57a-4464-4ade-81b5-d1da6d3ed411')

 # Imported TSLA.xlsx
 import pandas as pd
 sheet_df_dictonary = pd.read_excel('TSLA.xlsx', engine='openpyxl', sheet_name=['Sheet1'], skiprows=0)
 Sheet1 = sheet_df_dictonary['Sheet1']

```

mito のツールバーの `[CLEAR]`　をクリックするとグラフが消えて、読み込んだシートの状態に復帰します。

## 列の追加と削除

データ前処理の最も基本的な操作の1つは、属性の追加と削除です。mito のツールバーの `[Add Col]` と `Del Col]` のボタンで列の追加/削除を行うことができます。
まず、列を追加することから始めましょう。`[Add Col]` ボタンをクリックすると、シートに任意の名前のカラムが追加されます。`Adj Close`の列をクリックしてから`[Add Col]`ボタンをクリックしてみましょう。

![](https://gyazo.com/3a44eec4c368a38f0a107fc162866eb2.png)

列の名前は今回の場合 `new-column-7jjx` です。そこをクリックすると名前を変更することができます。

![](https://gyazo.com/ba9fad931a2d6e1b58635d5a0fdb149d.png)

初期状態は追加した列のすべては`0`です。

![](https://gyazo.com/ce964d6ed79f91570f5cb0cb5197eac4.png)

データを追加するには、その列の最初の行をクリックして、Excelと同じように数式を入力すればOKです。試しに1日での始寝と終値の差を求めてみるために、次の式を入力してみてください。

```
 Close-Open
```

入力を終えると行末まで計算結果が充当されます。

![](https://gyazo.com/b51f65bd16c8c19ae476bee59eb0300b.png)

ここまでのPythonコードが自動生成されています。

```
 # Added column new-column-7jjx to Sheet1
 Sheet1.insert(7, 'new-column-7jjx', 0)

 # Renamed new-column-7jjx to Difference in Sheet1
 Sheet1.rename(columns={'new-column-7jjx': 'Difference'}, inplace=True)

 # Set new-column-7jjx in Sheet1 to Close-Open
 Sheet1['Difference'] = Sheet1['Close']-Sheet1['Open']

```



## Excelの関数を使う

シートに追加した新しい列のセル内では、数式を割り当てることができ、通常の**Excelのような関数]を使用することができ、（[API Reference https://docs.trymito.io/how-to/interacting-with-your-data/mito-spreadsheet-formulas**を参照）Mitoは同等のPythonコードを生成します。関数を入力し始めると、選択可能な関数の候補リストが下のメニューに表示されます。

注意しなければいけないことは、`[EXPORT]`で生成したXLSXファイルには、**数式が保存されるわけではありません**。Pythonで計算した結果の値がセルに保存されます。


## データのフィルタリングとソート

データのフィルタリングやソートを行わずにデータ分析することはほとんど考えられません。Mitoを使えと直感的な操作で簡単に処理することができます。
まず、フィルタリングから始めましょう。列の▽マークをクリックすると、設定メニューが表示されます。

![](https://gyazo.com/d5e82a25dc827180672ad52fe48cfede.png)

フィルターに適切なオプションを選択します。この株価のヒストリカルデータの場合は、欠落データがありませんが。データによってはそれらを除外する必要があります。複数のフィルタリング条件を持つには、グループ全体を追加する必要があります

 `[Summary Stats]` をクリックするとその列のデータ可視化してくれます。
1日の株価の比較をしているだけで、過去には株価が低いもおのが多く、ほtんど分散がないグラフになっていますね。

![](https://gyazo.com/43ee1ba6b148cc31900b3ab3087936d1.png)

グラフをスクロールすると統計情報を見ることができます。

![](https://gyazo.com/730e4ac1a52ba639800c40b65672d826.png)

 `Adj Close` が100USD以上のデータを抜き出してみましょう。一旦 `Difference`の列のメニューを閉じて、
 `Adj Close` でfilterを追加します。
すぐに結果が反映された状態のシートになります。

![](https://gyazo.com/d1528ff1a64807a018731170f6712e26.png)

このあとに、先ほどと同じように　`Difference` のグラフを見てみましょおう。

![](https://gyazo.com/49918d011202f9b2b9458931861ca51e.png)

## ピボットレーブルの作成

mito でExcelのようにピボットテーブルを作成することができます。ピボットデーブルとは、未加工の生データからデータを
抽出加工して作成したテーブルで、別シートに作成されます。ピボットテーブルの操作を説明するためには、ここまでの株価データに変えて、もう少し複雑なデータを使ってみましょう。

Excel のチュートリアルを提供している [contextures.com](https://www.contextures.com/) が制約なしで使用することができるサンプルデータをいくつか提供してくれています。この中の架空の食料販売会社の商品販売データの [サンプルデータ](https://www.contextures.com/xlsampledata01.html#food]) を使ってみましょう。

このデータには、8列のデータがあり、そのうち1列は計算が含まれています。食品販売のテーブルには244行のデータがあり、各行には、以下のフィールドがあります。

  - OrderDate (注文日)。注文が行われた日付
  - Region（地域）：注文が発送される地理的な地域
  - City（市区町村）：注文が発送される市区町村
  - Category（カテゴリー）：製品カテゴリー - バー、クッキー、クラッカー、スナック菓子
  - Product（製品）：製品名
  - Quantity（数量）：注文個数
  - UnitPrice（単価）: 1個あたりの製品販売価格
  - TotalPrice（販売額）: 注文の合計金額 - 計算 - 数量 x 単価

ダウンロードした `sampledatafoodsales.zip` を展開すると `sampledatafoodsales.xlsx`が得られます。
mito のツールバー `[IMPORT]`でこのファイルを読み込みます。
このEXCELファイルには3つのシートがあるため、"FoodSales" のシートを選択します。


![](https://gyazo.com/54271bb7988b4eec8802120a6b8cebb6.png)


![](https://gyazo.com/82e860d99f600b40b985ac8078f1c042.png)

ツールバーの　`[PIVOT]` をクリックすると表示されるメニューで次のように設定してみてください。

![](https://gyazo.com/274729d029ae2c2cb3e3eaf085d37950.png)

これは、販売された製品を、西地区、東地区、カテゴリー、製品を抜き出したものです。
このマウスで行った操作に相当する Python コードは下部のセルに自動生成されます。


```
 # Pivoted FoodSales into df2
 unused_columns = FoodSales.columns.difference(set(['Category', 'Product']).union(set(['Region'])).union(set({'Quantity'})))
 tmp_df = FoodSales.drop(unused_columns, axis=1)
 pivot_table = tmp_df.pivot_table(
     index=['Category', 'Product'],
     columns=['Region'],
     values=['Quantity'],
     aggfunc={'Quantity': ['count']}
 )
 pivot_table.set_axis([flatten_column_header(col) for col in pivot_table.keys()], axis=1, inplace=True)
 FoodSales_pivot = pivot_table.reset_index()

```

## グラフ描画
ツールバーの`[GRAPH]`をクリックして表示される設定メニューで次のように設定してみましょう。

  - Data Source： FoodSales.pivot　選択
  - Chart Type：histgram
  - X-axis：Category count EASTと Category count WEST を追加
  - Y-axis：Product


![](https://gyazo.com/368ec66df519f7abf59a829efd640645.png)

製品ごとに西地区と東地区の販売比較を把握することができます。

 `[Setup Graph]` のメニュー下部にある、`[Export]`をクリックすると、
このグラフを表示させるためのPythonコードをクリップボードにコピーすることができます。


```
 import plotly.express as px
 # Construct the graph and style it. Further customize your graph by editing this code.
 # See Plotly Documentation for help: https://plotly.com/python/plotly-express/
 fig = px.histogram(FoodSales_pivot, x=['Quantity count East', 'Quantity count West'], y='Product')
 fig.update_layout(
     title='Quantity count East, Quantity count West, Product histogram',
     barmode='group',
     xaxis=dict(
         rangeslider=dict(
             visible=True,
             thickness=.05
         )
     )
 )
 fig.show(renderer="iframe")

```

## まとめ
mito は 日常的に Excel を使用している Python の初心者にとって非常に便意なツールです。 mito を使っていくなかで、Python および　Pandas、Plotly などの使い方を知ることができ学習の手助けにもなるでしょう。


## 参考
- mito
  - [オフィシャルサイト](https://www.trymito.io/])
  - [ソースコード](https://github.com/mito-ds/monorepo])
  - [公式ドキュメント](https://docs.trymito.io/])
- Jupyterlab
  - [公式ドキュメント](https://jupyterlab.readthedocs.io/en/stable/])
- Microsoft
  - [ピボットテーブルを作成してワークシート データを分析する](https://support.microsoft.com/ja-jp/office/%E3%83%94%E3%83%9C%E3%83%83%E3%83%88%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%82%92%E4%BD%9C%E6%88%90%E3%81%97%E3%81%A6%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B7%E3%83%BC%E3%83%88-%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E5%88%86%E6%9E%90%E3%81%99%E3%82%8B-a9a84538-bfe9-40a9-a8e9-f99134456576#OfficeVersion=macOS])
- [contextures.com](https://www.contextures.com/]) - EXCELのチュートリアルを提供しているサイト
