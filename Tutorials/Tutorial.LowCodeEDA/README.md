# Deep Learning

 * pycaret

## はじめに
この資料は、Python で探索的データ分析を

## 探査的データ分析と支援ツール

探索的データ分析（EDA: Exploratory Data Analysis）は、データを分析し、モデル化に進む前に、データセットが持つパターンや視覚的な洞察などを見出すアプローチです。データをより良く理解するためにEDAを行うには多くの時間を費やすことになります。

幸いに、Python には多くの自動可視化を行うことができる支援ツールがあり、それらを使用することでEDAを行うための時間を大幅に削減することができます。


 * ローコードタイプ (Low Code)
  * [skimpy](https://pypi.org/project/skimpy/)
  * [snapedautility](https://pypi.org/project/snapedautility/)
  * [Pandas-profiling](https://github.com/pandas-profiling/pandas-profiling/)
  * [QuickDA](https://github.com/ismael-araujo/Testing-Libraries/tree/main/QuickEDA)
  * [Sweetviz](https://github.com/fbdesignpro/sweetviz)
  * [DataPrep](https://github.com/sfu-db/dataprep)

 * ノーコード/ゼロコードタイプ (No Code/Zero Code)
  * [PandasGUI](https://pypi.org/project/pandasgui/)
  * [Pandas_UI](https://pypi.org/project/pandasgui://github.com/arunnbaba/pandas_ui)
  * [AutoViz](https://github.com/AutoViML/AutoViz)
  * [D-Tale](https://github.com/man-group/dtale)
  * [Bamboolib](https://bamboolib.8080labs.com/)
  * [Lux](https://github.com/lux-org/lux)
  * [Dora](https://github.com/NathanEpstein/Dora)
  * [Visidata](https://www.visidata.org/))
  * [Mito](https://www.trymito.io/)
  * [ScatterText](https://github.com/JasonKessler/scattertext)

  * [OpenRefine](https://openrefine.org/)

  https://towardsdatascience.com/comparing-five-most-popular-eda-tools-dccdef05aa4c

  https://towardsdatascience.com/autoviz-a-new-tool-for-automated-visualization-ec9c1744a6ad

  https://www.analyticsvidhya.com/blog/2021/04/top-python-libraries-to-automate-exploratory-data-analysis-in-2021/

  https://www.malicksarr.com/top-10-exploratory-data-analysis-eda-libraries/

  * Databricks acquires 8080labs(Bamboolib)
    - https://medium.com/analytics-vidhya/mlops-how-to-do-eda-without-writing-a-single-line-of-python-code-634d95a02367


EDAには、統計的検定、様々な種類のプロットを用いたデータの可視化など、多くのステップが含まれます。以下に、EDAのステップのいくつかを説明します。

 * データの品質チェック
  describe()、info()、dtypes()などのpandasライブラリ関数を使用して行うことができる。これは、いくつかの特徴、そのデータ型、重複する値、欠落値などを見つけるために使用されます。
 * 統計的検定
   Pearson相関、Spearman相関、Kendall検定など、いくつかの統計検定は特徴量間の相関を得るために行われます。Pythonのstatsライブラリを使って実装することができる。
 * 定量的テスト
   数値特徴量の広がりや、カテゴリ特徴量のカウントを求めるために、定量的検定を行う。Pythonのpandasライブラリの関数を用いて実装することができる。
 * 可視化
   特徴の可視化は、データを理解するために非常に重要である。棒グラフや円グラフのようなグラフィカルな手法は、カテゴリ特徴を理解するために使用され、散布図やヒストグラムは数値的特徴に使用されます。


 * Pandas-Profiling
   - https://github.com/pandas-profiling/pandas-profiling/
   Pandas-Profiling は、EDAプロセスを自動化し、詳細なレポートを作成するオープンソースのPythonライブラリです。Pandasプロファイリングは、驚くほど高速で数秒でレポートを作成するため、大規模なデータセットでも容易に利用することができます。
     * データセットの概要
     * 変数の特性
     * 変数の相互作用
     * 変数の相関
     * 欠測値
     * サンプルデータ
     * 可視化: ヒストグラム/散布図/ヒートマップ

 * Sweetviz
   - https://github.com/fbdesignpro/sweetviz
   Sweetvizは、高密度プロットの助けを借りてデータを探索しながらレポートを生成する、オープンソースのPython自動可視化ライブラリです。EDAを自動化するだけでなく、データセットの比較やそこから推論を導き出すためにも使用されます。2つのデータセットの比較は、一方をトレーニング、もう一方をテストとして扱うことで行うことができます。
     * データセットの概要
     * 変数の特性
     * カテゴリの関連性
     * 数値的な関連性
     * 数値特徴の最頻値、最小値、最大値

 * Autoviz
   - https://github.com/AutoViML/AutoViz
   Autovizは、オープンソースのPython自動可視化ライブラリで、主に異なるタイプのプロットを生成することによって、データの関係を可視化することに重点を置いています。

     * データセットの概要
     * 連続変数の一組の散布図
     * カテゴリ変数の分布
     * 連続変数のヒートマップ
     * 各カテゴリ変数による平均的な数値変数

 * D-Tale
   - https://github.com/man-group/dtale
   D-Taleは、オープンソースのPython自動可視化ライブラリです。最も優れた自動データ可視化ライブラリの1つです。D-Taleは、データの詳細なEDAを取得するのに役立ちます。また、レポート中の各プロットや分析に対して、コードエクスポートと呼ぶPythonコードの生成機能も持っています。

     * データセットの概要
     * カスタムフィルター
     * 分布、相関、チャート、ヒートマップ
     * データ型、欠損値、範囲の強調表示
     * テキスト分析
     * Pythonコードの生成
     * Plotly との連携

 * Bamboolib
   - https://bamboolib.8080labs.com/
   BambooLib は Jupyter 用の拡張機能
   Bamboolibを使うと、簡単なpandasのデータ変換をポイント＆クリックのインターフェースで行うことができます。例えば、あるカラムのヘッダー名を変更するようなときにも、コードを書く必要がなくなります。


 * BitRook
   - https://www.bitrook.com/
   BitRookは、EDAという課題に対する現代的なアプローチです。他のツールの優れた部分をパッケージ化し、コーディングの経験を必要としないデスクトップアプリケーションにまとめたものです。EDA作業終了後、クリーニングや標準化も可能です。

     * データの概要
     * データの種類を自動で検出
     * データの分布
     * 記述統計
     * 分位数統計
     * 欠損値グラフ
     * 相関関係
     * Pythonコードの生成

利点
    * ノーコードEDA
   * ローコードでデータクリーニング
   * AIを使用してデータのクリーニングを支援
   * PIIデータを特定
   * Predictive Power Scoreを自動計算します。


 * DataPrep
   - https://dataprep.ai/
DataPrepは、DataPrepのplot機能で指定できる可視化機能を幅広く提供しています。最も注目すべきビジュアライゼーションには、棒グラフ、ヒストグラム、円グラフ、箱ひげ図、ジオプロットなどがあり、さまざまな数値分布、カテゴリー分布、地理的分布を表現することをサポートします。DataPrepのビジュアライゼーションは、Bokehを使用しており、インタラクティブな表現が可能です。DataPrepのビジュアライゼーションのもう一つの特筆すべき点は、ビジュアライゼーションと一緒に表示されるインサイトノートです。これらのインサイトは、分布の要約を提供し、ユーザーが余分な計算を実行する必要をなくします。さらに、DataPrepでは、デフォルトのビジュアライゼーションをユーザーが設計要件に合わせて簡単にフォーマットおよびカスタマイズすることができます。

   内部ではDaskを使用し、分散クラスタ上でスケーリングすることにより、より高速なデータ解析を提供します。これにより、計算の高速化を通じて、より大きなデータセットに対応する能力が向上します。DataPrepのもう一つの特徴として、複数のデータフレーム間の比較も抜きん出ています。plot_diff関数は、2つ以上のデータフレームをリスト引数に取り、特徴を並べてプロットすることで、比較を容易にすることができます。
DataPrepは、2つ以上のデータフレームを分析・比較するユーザーにとって理想的なツールでしょう。DataPrepは、複数のデータフレームを扱う拡張機能とDask実装による高速化により、ビッグデータを扱うのに最も適したツールです。


 * QuickDA
   https://github.com/ismael-araujo/Testing-Libraries/tree/main/QuickEDA
   QuickDAは使いやすく直感的なローコードライブラリで、数行のコードでデータクリーニング、データ探索、データ可視化を実行することができます。実際、私たちはほとんどの時間、たった1行のコードを使うことになります。QuickDaがどれほど強力かを示すために、私はちょっとしたプロジェクトを作りました。ノートブックはこちらでご覧になれます。
   https://medium.com/towards-data-science/save-hours-of-work-doing-a-complete-eda-with-a-few-lines-of-code-45de2e60f257
   QuickDA — Low-code Python library for Quick Exploratory Data Analysis
   https://medium.com/analytics-vidhya/quickda-low-code-python-library-for-quick-exploratory-data-analysis-b4b1c3af369d




 * Lux
   - https://lux-api.readthedocs.io/en/latest/
   - https://github.com/lux-org/lux
   - https://medium.com/@amrkmrc/lux-the-next-level-of-eda-sophistication-fca6cfbf25d4

   Luxは、可視化とデータ分析プロセスを自動化することで、迅速かつ容易にデータ探索を行うことができるPythonライブラリです。Jupyterノートブックにデータフレームを出力するだけで、Luxはデータセットの興味深い傾向やパターンを強調する一連のビジュアライゼーションを推奨します。ビジュアライゼーションはインタラクティブなウィジェットで表示され、ユーザーは大量のビジュアライゼーションのコレクションを素早く閲覧し、データの意味を理解することができます。




  * Dora
  Dora は、探索的データ解析の困難で不便な部分を自動化するために設計された Python ライブラリです。このライブラリには、データのクリーニング、特徴の選択と抽出、データの可視化、モデル検証のためのデータの分割、データのバージョン変換のためのヘルパー関数が含まれています。このライブラリは、pandas、scikit-learn、matplotlibなどの一般的なPythonデータ解析ツールに追加して使用するもので、有用であることが意図されています。



このライブラリは、この記事で紹介する他のライブラリほど直感的ではなく、使用するためにはコードを書く方法を知っている必要があります。このライブラリは、すべてのEDAプロジェクトで使用される、追加の反復的な関数のようなものと考えることができます。Doraはあなたのためにこれらの関数を書きました。あなたがしなければならないのは、それらを呼び出して結果を分析することだけです。



   Dora の主な機能
       * データ読み込みとコンフィギュレーション
       * クリーニング
       * 特徴の選択と抽出
       * 可視化
       * モデル検証
       * データのバージョン管理



   * Visidata
     VisiDataは、表形式データのための対話型マルチツールです。スプレッドシートのわかりやすさ、ターミナルの効率、Pythonのパワーを組み合わせて、数百万行を簡単に扱える軽量なユーティリティです。
このライブラリは、ターミナル上でEDAを行いたい場合に最適です。ターミナル上でデータを分析するのは、通常はあまり利用されませんが、
それを必要とするプロジェクトがあるのであれば、Visidataを使うことを検討してみてください。



  Visidataの主な機能です。
       * コンテンツの編集
       * データのグループ化、記述統計
       * シート、行、列の作成
       * データセットの結合
       * テキストベースでのグラフの描画
       * VisiDataセッションの保存と再生方法



  * ScatterText
  自然言語処理（NLP）プロジェクトでEDAを行いたい場合、Scattertextを使うとよいでしょう。これは、コーパス内の用語を検索して区別し、インタラクティブなHTML散布図に表示するツールです。様々な点は、他のラベルや点と重ならないように選択的にラベル付けされた用語に関連しています。



このライブラリもまた、完全なEDAシステムではないので、使用するにはコードの書き方を知っている必要があります。完全なEDAプラットフォームではないものの、Scattertext内の可視化により、NLPプロジェクトに文脈を与えることができます。それらは、クリーンで、理解しやすく、うまく表現され、インタラクティブで、あなたが持っているデータをよりよく提示することができます。



Scattertextの主な特徴
Scattertext をテキスト分析ライブラリとして使用：特徴的な用語とその関連付けを見つける
用語の関連付けやフレーズの関連付けを可視化する
エンパスのトピックとカテゴリの可視化
モラルファウンデーション2.0辞書の表示
コーパスの特性による用語の順序付け
ドキュメントベースの散布図
CohenのdやHedgeのrを使って効果量を視覚化する



== DeepLearning
 * pycaret

   https://towardsdatascience.com/announcing-pycaret-an-open-source-low-code-machine-learning-library-in-python-4a1f1aad8d46
   https://towardsdatascience.com/introduction-to-regression-in-python-with-pycaret-d6150b540fc4
   https://towardsdatascience.com/introduction-to-anomaly-detection-in-python-with-pycaret-2fecd7144f87
   https://towardsdatascience.com/announcing-pycarets-new-time-series-module-b6e724d4636c

== BLOG
 * Data Frame EDA Packages Comparison: Pandas Profiling, Sweetviz, and PandasGUI
   - https://towardsdatascience.com/data-frame-eda-packages-comparison-pandas-profiling-sweetviz-and-pandasgui-bbab4841943b
 * Exploratory Data Analysis with 1 line of Python code
   - https://towardsdatascience.com/exploratory-data-analysis-with-1-line-of-python-code-5fe25387c84b
 * 4 Libraries that can perform EDA in one line of python code
   - https://towardsdatascience.com/4-libraries-that-can-perform-eda-in-one-line-of-python-code-b13938a06ae

 * How to Do a Ton of Analysis in Python in the Blink of An Eye.
   - https://towardsdatascience.com/how-to-do-a-ton-of-analysis-in-the-blink-of-an-eye-16fa9affce06

== Cloud
 * How to use Jupyter on a Google Cloud VM
   - https://medium.com/towards-data-science/how-to-use-jupyter-on-a-google-cloud-vm-5ba1b473f4c2


   Python | Titanic Data EDA using Seaborn
   https://www.geeksforgeeks.org/python-titanic-data-eda-using-seaborn/
