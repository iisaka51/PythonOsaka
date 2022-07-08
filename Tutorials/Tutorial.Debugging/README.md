Pythonチュートリアル：デバッギング
=================
![](https://gyazo.com/3219db26bd2ab60020ef63cad7aeb1cb.png)

Python プログラムでデバッギング作業の手順や、便利なパッケージについて説明します。

## デバッグについて
コンピュータのプログラム開発においてのデバッグ(Debug)は、バグ（Bug)・欠陥を発見および修正し、動作を仕様通りのものとするための作業で、多くの場合デバッグは面倒で退屈な作業になります。そして、どんなプログラムを開発するときでもデバッグはおそらく避けて通れない作業になります。

無視できないようなバグの発生を確認した場合、デバッグの戦略が必要になります。
それには理由は次のような場合があり単純ではないことも多いためです。

- 発生頻度が低い不具合
- 処理するデータに依存する不具合
- 大量のリクエストを処理したときなどの、性能限界に関連する不具合
- 処理速度が遅すぎるなど性能に関する不具合
- プログラムではなく仕様に問題がある不具合

### デバッグの手順
ある不具合をデバッグするためには、不具合の箇所がフレームワークやプログラムコード以外の少数のコードラインに分離して、できるだけ「修正」→「テスト」→「失敗」のサイクルが短くなるようにします。
そのために重要になることは次の手順です。

1. 確実に失敗させる：毎回コードが失敗するようなテストケースを見つける必要があります。
2.デバッグ対象を明確化：失敗するテストケースを見つけたら、失敗するコードを分離します。
  - どのモジュールか。
  - どの関数か。
  - どのコード行か。
3. テストケースを作成：再現性のある小さなテストを用意する。
4. 1つずつ変更して、失敗したテストケースを再実行します。
5.  デバッガーやログから不具合の原因を理解する。
6.  記録を取りながらデバッグ作業を行う。デバッグ作業はすぐには終わらないことが多いので記録に残す。

### デバッグのテクニック
Pythonプログラムをより良くデバッグするために、様々なテクニックがあります。ここでは、Pythonデバッグのための4つのテクニックを見ていきます。

- 静的解析：構文エラー、インポートの欠落、名前のタイプミスなどを実行前に検出する
- トレースバック：Pythonでプログラムが開発者の想定外の例外が発生したときに実行時のスタックが出力されます。
- コンテキストデバッグ： `print()` などを使って、どこで何が起こっているかを正確に知るための最も単純な方法です。
- ロギング：コンテキストデバッグに似ていますが、より多くの文脈情報を含んでいるので、完全に理解することができます。
- デバッガー：デバッガーpdbを使用する利点は、コマンドライン、インタープリタ、プログラムの中で使用できることです。IDE デバッガー：PyCharm や Visual Studio ほか多くのIDEには、統合されたデバッガ機能が提供されています。

## 静的解析
- [Pythonの静的解析ツール](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/01_StaticAnalyzer)

## トレースバック
- [Pythonのトレースバック](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/02_Traceback)

## コンテキストデバッグ
コンテキストデバッグ(Context Debug)はデバッグライト(Debug write) とも言われるもので、 `print()` などをコードに挿入して変数を確認したりします。

- [Pythonのダンダー(Dunder)](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/03_Dunder)
：２つのアンダースコアで始まる関数/メソッド/属性のこと
- [Inspectモジュールを使ってみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/04_Inspect)
- [Beholdモジュールを使ってみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/05_Behold)
- [watchpointsモジュールを使ってみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/06_Watchpoints)
- [snoopモジュールを使ってみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/07_Snoop)
：これを知るとデバッグライトとしての `print()` は不要になります。

## ロギング
- [Python標準ライブラリloggingでのロギング](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Logging/)

## デバッガー
Python では標準ライブラリに含まれているデバッガ  pdb を利用することができます。他にもこれを拡張した ipdb、 pdb++ などいくつかのデバッグーがあります。

- [Pythonのデバッガーpdbを使ってみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Debugging/08_Pdb)



## 参考
- Python公式ドキュメント
  - [traceback --- スタックトレースの表示または取得 ](https://docs.python.org/ja/3/library/traceback.html)
  - [データモデル ](https://docs.python.org/ja/3/reference/datamodel.html)
  - [inspect --- 活動中のオブジェクトの情報を取得する ](https://docs.python.org/ja/3/library/inspect.html)
  - [pdb --- Python デバッガ  ](https://docs.python.org/ja/3/library/pdb.html)
- [Python のダンダーな名前まとめ ](https://github.com/gh640/python-dunder-names-ja)
- [ipdb ソースコード ](https://github.com/gotcha/ipdb)
- [rpdb オフィシャルサイト ](https://tamentis.com/projects/rpdb/)
- [adhoc-pdb ソースコード　](https://github.com/yehonatanz/adhoc-pdb)
- [pytest-pdb ソースコード ](https://github.com/fschulze/pytest-pdb)
- [Graphvizとdot言語でグラフを描く方法のまとめ ](https://qiita.com/rubytomato@github/items/51779135bc4b77c8c20d)


