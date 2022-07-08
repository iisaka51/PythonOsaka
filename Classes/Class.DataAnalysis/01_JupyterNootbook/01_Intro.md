Jupyter  Notebookを使ってみよう
=================
### Jupter Notebook
Jupyter notebook は 実行可能なプログラム、方程式、視覚化、テキストを含むドキュメントを作成して共有できる、 オープンソースのWebアプリケーションです。
データ分析と変換、数値シミュレーション、統計モデリング、データの視覚化、機械学習などをうまくドキュメント化することができます。

- オープンソースで開発れていて無料で利用できる
- Markdown記法で簡単にドキュメントを整形できる
- 数式をTex形式で入力できる
- プログラムコードを記述できて、実行もでき、その結果をドキュメントに取り込める
- カーネルを切り替えて複数言語に対応
- 強力な補完機能
- １つのファイルにコードとドキュメントを保存できる
- HTML/PDFなど、さまざまな形式に出力できる
- GitHub が notebook に対応しているのでドキュメントの公開がとても簡単
- さまざまな拡張機能: 例: プレゼンテーションを行うRISE

### Jupterlab
JupyterLabは、Jupyterプロジェクトの次世代のWebベースのユーザーインターフェイスです。

- ノートブックと似た感覚で触れることができが、より洗練されたインターフェース
- タブで複数ノートを切り替えられる
- ノートブック、テキスト、CSV、コンソールなど複数のウィンドウ表示が可能
- CSVデータを表形式で表示してくれる
- Google Driveとの統合
- ドラッグ＆ドロップが可能なセル
- ファイルエクスプローラー

![](https://gyazo.com/b85b19940fe2bd217bee28d3d0e52be1.png)

### drow.ioに対応
Jupyterlab から Draw.io の拡張機能を使うことができ、 簡単に作図できるようになります。
![](https://gyazo.com/e04cbdfa5ec16224068be2c52b72bea6.png)



### カーネル
Jupyter / JupyterLab ではカーネルを切り替えることで複数の言語に対応しています。

主なカーネル:
- Bash
- Python
	R
- Ruby
- Perl
- Hashkel
- Go

### notebook の拡張
nbextension というモジュールを使えるようにしています。

Jupyter の Edit メニューから nbextension config を選択すると、 次のような設定画面が表示されます。

![](https://gyazo.com/775f3cf331f5476e151072cf4cfe019c.png)


### 数式との親和性
この資料を記述しているScrapBox 同様に、Markdownのセルに次のようにLatex記法で数式を書くと、数式が整形されて表示されます。
ソース:
> $$e^x=\sum_{i=0}^\infty \frac{1}{i!}x^i$$
[$ e^x=\sum_{i=0}^\infty \frac{1}{i!}x^i]

アルゴリズムや理論を数式でわかりやすく説明できます。
[myscript.com ](https://webdemo.myscript.com/) には手書きで数式を描くと、TeX形式に変換してくれる便利なサービスもあります。
![](https://gyazo.com/f2b710583db42e8e01564e681cdd14bb.png)


また、よく使う数式を備忘録として保存しておくなどの利用方法もあります。

Pythonの数式演算ライブラリ `sympy` を使用すれば、 数式を計算するだけで数式が表示されてとても便利になります。


### ショートカットキー
Jupyter Notebookのショートカットキーを使うと、キーボードから手を話すことなくコードやドキュメントの記述や実行を行えるので作業効率が向上します。

 Jupyter notenookのショートカットキー

| Key | 操作 |
|:--|:--|
| Esc → m  | マークダウンモードに変更 |
| Esc → y  | コードモードに変更 |
| Esc → a | 上にセル追加 |
| Esc → b  | 下にセル追加 |
| Esc → dd  | セル削除 |
| Esc → l  | 行数表示 |
| Ctrl + Enter  | セル実行 |
| Alt + Enter  | セル実行＋下にセル追加 |

### インストールと設定
ここでは、jupyterlab のインストールと設定について説明します。 Jupyter Notebook の場合は、jupyterlab を　jupyter としてください。

 bash
```
 $ pip install jupyterlab jupyter_nbextensions_configurator
```

 bash
```
 $ jupyterlab notebook --generate-config
```

### ノートブックのディレクトリを指定する

```
 # c.NotebookApp.notebook_dir = ''
```

### jupyter のログインでパスワードを強制させる
 bash
```
 $ python -c "from notebook.auth import passwd; print(passwd())"
```

パスワード入力と確認のための再入力後に、表示される文字列を
~/.jupyter/jupyter_notebook_config.py に設定する

```
 # c.NotebookApp.password = ''\
 c.NotebookApp.password = 'sha1:........'
```


## 参考
- [Jupyter プロジェクト オフィシャルサイト ](https://jupyter.org/)
- [Awesome Jupyter ](https://github.com/markusschanta/awesome-jupyter) - Jupyterプ ロジェクト、ライブラリ、リソースの厳選リスト
- [Best-of Jupyter - A ranked list of awesome Jupyter projects ](https://github.com/ml-tooling/best-of-jupyter)
- [19 Best JupyterLab Extensions for Machine Learning ](https://neptune.ai/blog/jupyterlab-extensions-for-machine-learning)


![](https://gyazo.com/a5d11478e77446e0c55e6e19e055d59a.png)



