Pythonの静的解析ツール
=================

## 静的解析ツールについて
Pythonには多くの静的解析ツールがありますが、概ね次のような分類ができます。

- コードスタイリング解析
- セキュリティリンティング
- エラー検出
- UML図の作成
- 重複コードの検出
- 複雑さの分析
- 使用されていないコードの検出
- 自動フォーマッター

いずれも、 コードを実行することなく、コードを解析することができることができます。静的解析ツールを使っソースコードチェックを行うことで、開発者やプロジェクト、企業には以下のようなメリットがあります。

- 一貫性の確保：誰が作業しても、最終製品は常に同じ信頼できるコードになります。
- 潜在的なバグの回避に役立つ：厳格なルールにより、一般的なミスを犯さないようにします。
- 効率的なコードレビュー：各コードは、慣れ親しんだ同じスタイルと構文を持っています。すべてのチェックに合格していれば、レビューの必要はほとんどありません。
- コードリビジョンの削減：厳密なチェックにより、コードベースを何度も書き直す必要がありません。
- コードの冗長性を減らす：問題に対してある方法で考えているうちに、複雑なコードを書いてしまうことがあります。コードを単純化し、冗長な記述を排除するのに役立つ提案を行います。
- セキュリティ問題の早期の発見を自動化できる
- コードの品質維持の自動化：手順もれや作業ミスをすることない


## Pythonの規約
Pythonには **PEP(Python Enhancement Proposals** と呼ばれるドキュメントが[公開 ](https://www.python.org/dev/peps/%5D)されています。これらのドキュメントの中でコーディングに関する規約やガイドがあります。

- [PEP 7 -- Style Guide for C Code ](https://www.python.org/dev/peps/pep-0007/)：Cコーディングスタイルガイド
- [PEP 8 -- Style Guide for Python Code ](https://www.python.org/dev/peps/pep-0008/)：Python コーディングスタイルガイド
- [PEP 20 -- The Zen of Python ](https://www.python.org/dev/peps/pep-0020/)：Pythonの開発を通して読んで適用するべき考え方
- [PEP 257 -- Docstring Conventions ](https://www.python.org/dev/peps/pep-0257/)：docstring の規約
- [PEP 274 -- Dict Comprehensions ](https://www.python.org/dev/peps/pep-0274/)：dictに適用されるリスト内包表記の美しさについて
- [PEP 328 -- Imports: Multi-Line and Absolute/Relative ](https://www.python.org/dev/peps/pep-0328/)：絶対インポート、相対インポート、複数行のインポートについて
- [PEP 343 -- The "with" Statement ](https://www.python.org/dev/peps/pep-0343/)：ファイルやその他のリソースを扱う際の try/finally ブロックを取り除くのに役立ちます
- [PEP 440 -- Version Identification and Dependency Specification ](https://www.python.org/dev/peps/pep-0440/)：バージョン定義についての規約
- [PEP 498 -- Literal String Interpolation ](https://www.python.org/dev/peps/pep-0498/)：文字列をフォーマットするための素晴らしい構文規約

コーディングスタイルガイド（PEP8)のような規約では、コードを書いてしまってから静的解析ツールで調べて、気づくというようなこともあります。

## リンターとフォーマッター
静的解析ツールには大きく２種類あります。

- リンター(linter)：規約に従っているかどうかをチェックする
- フォーマッター(formatter)：規約に従ってコードを改修する


>Unixでコードをチェックするツールとして lint がよく知られています。このコマンドの名前から転じて、コードをチェック・解析することをリント(lint)、リントを行うプログラムをリンター(linter)と呼ばれるようになりました。



## いろいろなリンター

- [pycodestyle ](https://github.com/PyCQA/pycodestyle)：以前の名前はpep8  だったもので、PythonのコードがPEP8に準拠しているかをチェックするためのリンター。後述の flake8 に取り込まれているため、単独で使用することはないはずです。
- [pyflakes ](https://pypi.org/project/pyflakes/)：Pyflakes には単純な制約があります。それは、スタイルについては決して文句を言わず、偽陽性を出さないことには非常に努力します。論理的なコードの問題や潜在的なエラーに焦点を当てたリンターです。pyflakesは各ファイルのシンタックスツリーを個別に調べるだけです。pylintよりも高速ですが、pyflakesはチェックできる内容がより限定されています。後述の flake8 に取り込まれているため、単独で使用することはないはずです。
- [pylint ](https://pypi.org/project/pylint/) ：Python のコードチェッカーのひとつで、コーディング標準からエラー検出まで多くの機能を持ち、重複したコードや使われていないコードを検出することでリファクタリングを支援してくれるなど、多彩な機能と豊富なオプションを持っています。また、簡単にカスタマイズすることができます。
- [flake8 https://pypi.org/project/flake8/] ： [pyflakes https://github.com/PyCQA/pyflakes],、[pycodestyle  https://github.com/PyCQA/pycodestyle]、 [McCabe ](https://github.com/PyCQA/mccabe) のラッパーです。豊富なサードパティープラグインがある静的解析ツールで、スタイルチェックと pyflakes を組み合わせた機能を持ちます。加えて、プロジェクトごとの強力な設定機能も追加されています。
- [wemake-python-styleguide ](https://github.com/wemake-services/wemake-python-styleguide)：flake8 に機能追加するプラグイン。Flake8と多数のプラグインを一括してインストールできるので便利です。ただし、この資料作成時点では、Flake8の新バージョン4.0.1がリリースされているのですが、追随できていません。
- [Prospector ](https://prospector.landscape.io/en/master)：Pythonコードを解析し、エラー、潜在的な問題、規約違反、複雑さなどの情報を表示する強力な静的解析ツールの一つです。pylint,、flake8、pyflakes、mccabe、vuture、pip9、pep257 を含んだ便利なツールです。柔軟性についてはflake8に劣るものの、依存パッケージがFlake8より少なく管理しやすくなります。mypy や　bandit と連携することができます。多くのリンターを個別に導入すると設定ファイルや実行方法が乱雑になってしまい、混乱してしまいますが、Prospector を導入すると総括して実行してくれます。prospector2 は python2ベースのコードをサポートし続けることを表明したパッケージです。
- [bandit ](https://github.com/PyCQA/bandit)：banditは、Pythonコードの一般的なセキュリティ問題を発見するために設計されたツールです。実際にbandit を使用しない場合でも、このツールのドキュメントは一度目を通しておくことはおすすめします。
- [vulture ](https://github.com/jendrikseipp/vulture)：Python プログラムの中の使われていないコードを検出する。


この資料では説明はしませんが、次の静的解析ツールも利用価値は高いものです。

- [nitpick ](https://wemake-python-stylegui.de/en/latest/pages/usage/integrations/nitpick.html)：言語に依存しない複数のプロジェクトに同じ設定を適用するためのコマンドラインツールとflake8プラグインです。複数のプロジェクトを管理していて、同じ INI/TOML/YAML/JSON のキーや値を何度もコピー/ペーストするのが面倒な場合に便利です。
- [mypy https://mypy.readthedocs.io/en/stable/]：MypyはPython用の静的型チェックツールです。mypy を利用する場合の必要条件は、Python 3の関数アノテーション構文（[PEP484 ](https://www.python.org/dev/peps/pep-0484/)）を使って、コードがアノテーションされていることです。そして、mypyはあなたのコードを型チェックし、共通のバグを見つけることができます。その目的は、動的型付けと静的型付け（型付けモジュールの使用）の利点を組み合わせることです。Pythonには文法として型宣言をすることは不要ですが、型宣言は機械的にテストされたドキュメントとして機能し、静的型付けはコードをより明確にし、エラーを起こさずに修正することを容易にしてくれます。
- [pysa ](https://github.com/facebook/pyre-check)：Facebookがソーシャルネットワークサービス「Instagram」のコードベースにおけるセキュリティバグを収集するために開発した静的解析ツール。ログラムからのデータの流れを追跡し、クロスサイトスクリプティング攻撃、リモートからのコード実行、SQLインジェクションなどにつながるデータパターンがないかを調べることができます。
- [radon ](https://radon.readthedocs.io/en/latest/)：プログラム走査して複雑性や規模を数値化してくれるツールです。単純なコードに比べて複雑なコードの方がバグが存在することが多く、テストを行う湯鮮度を決めるときなどの指標に使うことができます。

## どれを使ったら良いんだ？
多くのリンターがあるため、その選定に悩むことになるはずです。ひとつの選定方針に開発保守が維持されていることに注目してみるとよいかもしれません。
例えば、[PyCQA ](https://github.com/PyCQA)というGitHub Organization は、多くのリンターのレポジトリを管理しています。ここで管理されているものは、その開発保守が維持される可能性が高いと考えられます。

- astroid
- bandit
- doc8
- flake8
- flake8-bugbear
- flake8-commas
- flake8-docstrings
- flake8-import-order
- flake8-json
- isort
- mccabe
- mccabe-console-script mirror
- modernize
- oeuvre
- pep8-naming
- prospector
- pycodestyle
- pydocstyle
- pyflakes
- pylint
- pylint-celery
- pylint-django
- pylint-plugin-utils
- redbaron

これは私見ですが、いまの時点でリンターとしては次の３つの選択肢があると考えています。

- **Pylint**：[Pythonの静的解析ツールPylintを使ってみよう]
- **Flake8**：[Pythonの静的解析ツールFalke8を使ってみよう]
- **Prospector**：[Pythonの静的解析ツールProspectorを使ってみよう]

利用価値のある静的解析ツールとしては次のようになります。

- **bandit**: [Pythonの静的セキュリティー検査ツールbanditを使ってみよう]
- **vulture**：[Pythonの静的解析ツールVultureを使ってみよう]
- **isort**：[Pythonの静的解析ツールisortを使ってみよう]


## 自動フォーマッター
静的解析ツールを使ってソースコードがPEP8のスタイルガイドから逸脱していることを確認したとき、コードを改修する作業も面倒なことです。IDEによっては保存する前に自動フォーマッターでPEP8に準拠したスタイルに書き換えてくれるものもあります。
自動フォーマッターには次のようなものが知られています。

- [autopep8 ](https://github.com/hhatto/autopep8)：PEP 8 スタイルガイドに準拠してコードを変換。
- [pyformat ](https://github.com/myint/pyformat)：PEP 8 スタイルガイドに準拠してコードを変換、未使用のインポートや変数の削除、同じ種類の引用符に変換、docstringを整形
- [isort ](https://github.com/PyCQA/isort)：インポートをチェックして重複排除などの整形を行う
- [add-trailing-comma ](https://github.com/asottile/add-trailing-comma)：リスト/タプル/辞書の定義や呼び出し、複数行の定義をなどで末尾にカンマを追加
- [yapf ](https://github.com/google/yapf)：Googleが開発した非常に複雑な自動フォーマターです。非常に多くの設定オプションがあります。
- [black ](https://github.com/psf/black)：妥協のない Python コードの自動フォーマッターです。

それぞれに設計方針があり、どれがよいと推奨することは難しいのですが、pyformat と isort 、add-trailing-comma、black を使ってみるのがよいかもしれません。
black について補足説明をすると、この自動フォーマッターはカスタマイズできる余地をほとんど与えてくれません。その代わりにコードスタイルについては black にまかせてしまうことで、コード開発に専念できるというメリットがあります。
自動フォーマッターに自由度があるということは、プロジェクトで採用するときにコードスタイルを決定する冗長な議論が必要になるからです。「black がそうフォーマットしたんだから、それで良い」と割り切ることも重要なことです。


## 参考
- [Pylint User Manual  ](https://pylint.pycqa.org/en/latest/index.html)
- [wemake-python-styleguide ドキュメント ](https://wemake-python-stylegui.de/en/latest/index.html)
- [Pythonで開発するなら読んでおくべきPEP一覧](https://scrapbox.io/PythonOsaka/Python%E3%81%A7%E9%96%8B%E7%99%BA%E3%81%99%E3%82%8B%E3%81%AA%E3%82%89%E8%AA%AD%E3%82%93%E3%81%A7%E3%81%8A%E3%81%8F%E3%81%B9%E3%81%8DPEP%E4%B8%80%E8%A6%A7)
