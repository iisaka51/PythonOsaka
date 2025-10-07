# Python ドキュメント関連

## はじめに

Microsoft の Word を含め、ドキュメント作成のためツールには多くのものが存在しています。
ここでは、Python で実装されたドキュメントツールについてまとめています。


## Python の docstring 

Python では、関数やクラス、モジュールなどに Pythonドキュメンテーション文字列 (docstring)と呼ばれるドキュメントを記述することができます。

docstringの例： pathlib ライブラリのPathクラスから抜粋

```
class Path(PurePath):
    """PurePath subclass that can make system calls.

    Path represents a filesystem path but unlike PurePath, also offers
    methods to do system calls on path objects. Depending on your system,
    instantiating a Path will return either a PosixPath or a WindowsPath
    object. You can also instantiate a PosixPath or WindowsPath directly,
    but cannot instantiate a WindowsPath on a POSIX system or vice versa.
    """
    __slots__ = ()

    def stat(self, *, follow_symlinks=True):
        """
        Return the result of the stat() system call on this path, like
        os.stat() does.
        """
        return os.stat(self, follow_symlinks=follow_symlinks)
```

組み込み関数 `help()` はこの docstring を読み取り表示してくれます。

```
$ ppython -c 'from pathlib import Path; help(Path)'
Help on class Path in module pathlib:

class Path(PurePath)
 |  Path(*args, **kwargs)
 |
 |  PurePath subclass that can make system calls.
 |
 |  Path represents a filesystem path but unlike PurePath, also offers
 |  methods to do system calls on path objects. Depending on your system,
 |  instantiating a Path will return either a PosixPath or a WindowsPath
 |  object. You can also instantiate a PosixPath or WindowsPath directly,
 |  but cannot instantiate a WindowsPath on a POSIX system or vice versa.
 |
 |  Method resolution order:
 |      Path
 |      PurePath
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  __enter__(self)
```

標準ツール pydoc を使ってファイルを指定しても同じことができます。
また、pydoc はインストールされているライブラリ全体のナビゲートする
Webサーバーを立ち上げることもでき、ブラウザで参照することができます。

VSCode のPython拡張を利用したり、
Jupyter などであれば、`nbextentions`で `hinterland` を有効化していると、関数を呼び出す際に表示してくれるようになります。

その場限りの使い捨てコードでは書く必要はありませんが、
ソースコードに適切な docstring を記述しておくことで、
開発や保守での機能確認が容易になります。

Pythonドキュメンテーション文字列 (docstring)について，その意味と取り決めは、
[PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/) としてまとめられています。


PEP-257 でのポイント

  1行は72文字までとする。
- import文はコメントの直後に記述する。
- 概要のみの1行、詳細な説明の複数行を記述する。
- 1行目は概要のみ簡潔に記述する。
- 複数行の場合は、空行を挟んで説明を記述する。
- docstringと対象定義の間に空行を挟まない。
- モジュールの場合は、公開するクラス、関数などについて1行の説明を付けて一覧化する。
- クラスの場合は、何をするクラスなのかの概要、外部に公開するメソッドやインスタンス変数などを記述する。
- クラスの場合は、冒頭ではdocstringとの間に空行を挟む。
- 関数の場合は、何をするのかの概要、パラメータ、戻り値、発生する例外などについて記述する。

## docstring を使ったテスト
[doctest](https://docs.python.org/ja/3/library/doctest.html) を使用すると、docstring 中の実行例をチェックしてくれます。


今ここに、`fibo.py` があるとします。

```
def fibo(n):
    """
    >>> fibo(8)
    34
    >>> fibo(9)
    55
    """
    if n == 0 or n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

if __name__ == '__main__':
    v = fibo(10)
    print(v)
```

doctest を呼び出せばテストをしてくれます。

```
$ python -m doctest -v fibo.py
```

テストの結果機体通りだった場合は終了コード０が返されます。


## docstring のスタイル

docstringのスタイルは、プロジェクトや使用するツールに応じてさまざまなスタイルがあります。

 - reStructuredTextスタイル
 - Googleスタイル
 - NumPyスタイル

同じプロジェクトで複数のスタイルが混在するのは良くないため、
事前に決定しておくべき事項です。


### reStructuredTextスタイル
[reStructuredText](https://docutils.sourceforge.io/rst.html) は読み易く、見たままのものが得られる、プレーンテキストのマークアップ文法およびパーサシステムです。 reStructuredText を reST と略して呼ぶこともあります。
[sphinx](https://www.sphinx-doc.org/ja/master/)は reStructredText で記述したテキストから、プログラムドキュメントを作成しいたり、シンプルな web ページを作るときに便利なツールです。もともと、Python のドキュメンテーション用に作られました、
今では、Python や Numpy などほか幅広い言語のプロジェクトでドキュメント作成を容易にするツールとして利用されています。
sphinx はdocstringを構文解析することでドキュメントの自動生成を行うことができます。

特定のキーワードを用います。

| キーワード | 説明 |
|-----------|------|
| param, parameter, arg, argument, key, keyword	| 引数の説明 |
| type	| 引数の型|
| raises, raise, except, exception	| 例外処理の説明 |
| var, ivar, cvar	| 変数の説明 |
| vartype	| 変数の型 |
| returns, return	| 戻り値の説明 |
| rtype	| 戻り値の型 |


記述例

```
def func(arg1, arg2):
    """概要
    
    詳細説明
    
    :param int 引数(arg1)の名前: 引数(arg1)の説明
    :param 引数(arg2)の名前: 引数(arg2)の説明
    :type 引数(arg2)の名前: 引数(arg2)の型
    :return: 戻り値の説明
    :rtype: 戻り値の型
    :raises 例外の名前: 例外の定義
    """
    value = arg1 + arg2
    return value
```

### Googleスタイル
Google がプログラム言語ごとに規定したスタイルガイドで、
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) の [3.8 Comment and Docstring](https://google.github.io/styleguide/pyguide.html) で規定されています。

セクションごとに記述します。

| セクション | 内容 |
|-----------|------|
| Attributes	| クラスの属性の説明 |
| Args	| 引数の説明 |
| Returns	| retrun文での戻り値の説明 |
| Yieds	| yeild文での戻り値の説明 |
| Raises	| 例外処理の説明 |
| Examples	| クラスや関数の実行例 |
| Note	| 自由記載 |
| Todo	Todoリストを記載 |


記述例

```
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

### Numpy スタイル

Numpy プロジェクトで規定された[スタイルガイド](https://numpydoc.readthedocs.io/en/latest/format.html#)


| セクション	| 内容 |
|--------------|------|
| Attributes	| クラスの属性の説明 |
| Parameters	| 引数の説明 |
| Returns	| return文での戻り値の説明 |
| Yields	| yeild文での戻り値の説明 |
| Raises	| 例外処理の説明 |
| Examples	| クラスや関数の実行例 |
| Notes | 自由記載 |
| See Also	| 関連して参照 |


[記述例](https://numpydoc.readthedocs.io/en/latest/example.html#)　から抜粋

```
def foo(var1, var2, *args, long_var_name="hi", only_seldom_used_keyword=0, **kwargs):
    r"""Summarize the function in one line.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    *args : iterable
        Other arguments.
    long_var_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.
    type_without_description

    Other Parameters
    ----------------
    only_seldom_used_keyword : int, optional
        Infrequently used parameters can be described under this optional
        section to prevent cluttering the Parameters section.
    **kwargs : dict
        Other infrequently used keyword arguments. Note that all keyword
        arguments appearing after the first parameter specified under the
        Other Parameters section, should also be described under this
        section.

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    numpy.array : Relationship (optional).
    numpy.ndarray : Relationship (optional), which could be fairly long, in
                    which case the line wraps here.
    numpy.dot, numpy.linalg.norm, numpy.eye

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a Greek symbol like :math:`\omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a = [1, 2, 3]
    >>> print([x + 3 for x in a])
    [4, 5, 6]
    >>> print("a\nb")
    a
    b
    """
    # After closing class docstring, there should be one blank line to
    # separate following codes (according to PEP257).
    # But for function, method and module, there should be no blank lines
    # after closing the docstring.
```


## docstring の自動生成

VSCode で、関数宣言の直下で３重引用符(`"""`)を入力すると`Generate docstring` という入力支援が表示されるのでそのままリターンキーを押下することでdocstringが自動的に挿入されます。

他にも、[autoDocstring ](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)　などの拡張機能を使うこともできます。

## reStructredText と Markdown 
どちらも学習コストは少なく利用を始めればすぐになれるものですが、
プログラマーの視点からMarkdownとreStructuredTextのどちらを使用すればよいのか検討してみます。

- Markdown  
 プログラムのドキュメンテーションやソースコードへのテキスト入力に使う技術を考えるとき、GitHub がデフォルトのマークアップ限度として採用していることから、多くのプロジェクトで利用されているため、真っ先に頭に浮かぶのはMarkdown になるでしょう。

- reStructuredText  
 の最初のリリースは2002年にさかのぼり、実はMarkdownよりも古い。 問題は、Pythonコミュニティの一部に限定され、その生涯のほとんどを比較的無名のまま過ごしてきたことだ。 Pythonのコアなドキュメントはかなり長い間reSTで書かれてきましたが、Sphinxがリリースされた後、初めて外部で本格的に使われるようになりました。 GitHubはページやWikiのためにreSTをサポートし、Linuxカーネル、OpenCV、LLVM/Clangを含むいくつかの主要なプロジェクトは、デフォルトでドキュメントにreSTを使っています。 私にとって、reSTはMarkdownに対して3つの主要な側面で際立っています。 より機能が充実している。 より標準化され、統一されている。 拡張機能のサポートが組み込まれている。

どちらを選ぶべきかは、結局のところプロジェクトに依存することです。
個人的には機能が少ない Markdown の方が文章を書くことに専念できると考えています。


## ドキュメント作成ツール

sphinx が広く使用されているのですが、このツールは reStructuredText で記述しデフォルトではMarkdownを扱うことができません。sphinx-markdown-parser を追加すれば処理できますが、PDFで出力での出力したいときなどで設定が手間になります。

ここでは、直接 Markdown を処理でき、PDFでの出力の設定などが簡単にできる MkDocs について説明します。

```
$ pdm -dG test mkdoc smkdocs-with-pdf mkdocs-kroki-plugin mkdocs-marmaid2-plugin
```

Python の pdoc ライブラリは docstring を読み取りドキュメントを生成してくれます。
この出力を mkdocs に取り込みたいときは、mkdocs-pdoc-plugin を追加しておきます。

```
$ pdm add -dG test git+https://github.com/spirali/mkdocs-pdoc-plugin
```

Ansible のロール/プレイブックを取り込みたいときは、次のプラグインも追加しておきます。

```
$ pdm -dG test  mkdocs-ansible-collection mkdocs-ansible 
```

```
$ mkdocs -h
Usage: mkdocs [OPTIONS] COMMAND [ARGS]...

  MkDocs - Project documentation with Markdown.

Options:
  -V, --version         Show the version and exit.
  -q, --quiet           Silence warnings
  -v, --verbose         Enable verbose output
  --color / --no-color  Force enable or disable color and wrapping for the output.
                        Default is auto-detect.
  -h, --help            Show this message and exit.

Commands:
  build      Build the MkDocs documentation.
  get-deps   Show required PyPI packages inferred from plugins in mkdocs.yml.
  gh-deploy  Deploy your documentation to GitHub Pages.
  new        Create a new MkDocs project.
  serve      Run the builtin development server.

```

プロジェクトのディレクトリで mkdocs を初期設定をします。

```
$ mkdocs new .
INFO    -  Writing config file: ./mkdocs.yml
INFO    -  Writing initial docs: ./docs/index.md
```

これで、`docs/index.md` と mkdocs.yml が生成されます。

生成された `docs/index.md` は次の内容が書き出されます。

```
# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
```

Makrdownとしてリンクを記述すれば、別のファイルに繊維します。


`mkdocs.yml` はmkdocs の設定ファイルで、はじめはサイト名を定義する設定しかありません。

```
site_name: My Docs
```

このファイルにセクションとして以下を定義してゆきます。

| セクション	       | 説明 |
|---------------------|-------------------------------------------|
| site_name           | サイト名　このセクションは必須 |
| site_url            | 外部公開するときのURL |
| repo_url            | 指定したリポジトリへのリンクが表示される |
| nav	              | ドキュメントのレイアウトを定義する |
| theme	              | サイトの見た目などに関わるテーマを定義する |
| markdown_extensions | Markdown拡張機能を定義します |
| plugins             | サイト構築時に使用するプラグインを定義する |
|



詳細は [mkdocs configuration](https://www.mkdocs.org/user-guide/configuration/) を
参照してください。



### ドキュメントの生成

`mkdocs build` でドキュメントを生成します。

```
$ mkdocs build
WARNING -  Config value 'packages': Unrecognised configuration name: packages
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /home/goichi/sample/site
INFO    -  Documentation built in 0.04 seconds
```


`site` 以下にHTMLファイルほかが自動的に生成されます。

```
$ tree site
site
├── 404.html
├── css
│   ├── base.css
│   ├── bootstrap.min.css
│   ├── bootstrap.min.css.map
│   ├── brands.min.css
│   ├── fontawesome.min.css
│   ├── solid.min.css
│   └── v4-font-face.min.css
├── img
│   ├── favicon.ico
│   └── grid.png
├── index.html
├── js
│   ├── base.js
│   ├── bootstrap.bundle.min.js
│   ├── bootstrap.bundle.min.js.map
│   └── darkmode.js
├── pdf
│   └── document.pdf
├── sitemap.xml
├── sitemap.xml.gz
└── webfonts
    ├── fa-brands-400.ttf
    ├── fa-brands-400.woff2
    ├── fa-regular-400.ttf
    ├── fa-regular-400.woff2
    ├── fa-solid-900.ttf
    ├── fa-solid-900.woff2
    ├── fa-v4compatibility.ttf
    └── fa-v4compatibility.woff2

5 directories, 26 files
```

### Webサーバーの起動

`mkdocs serve` は、mkdocs build を実行してから、
Webサーバーが立ち上げます。
表示されたURLを開くとブラウザで参照することができます。　

```
$ mkdocs serve
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.10 seconds
INFO    -  [13:09:20] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [13:09:20] Serving on http://127.0.0.1:8000/
```


### テーマをカスタマイズ

mkdocs はドキュメントの外観を簡単に変更することができます。

まず、人気のあるテーマは[MkDocs Themes · mkdocs/mkdocs Wiki](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes)で参照できます。

公開されていて利用可能なテーマの一覧は[mkdocs/catalog: :trophy: A list of awesome MkDocs projects and plugins.](https://github.com/mkdocs/catalog#-theming)　を参照してみてください。

テーマを塚します。

```
$ pdm add -gD test mkdocs-simple-blog
```
`mkdocs.yml` に `tehme` を追記してビルドしなおします。

```
site_name: My Docs
plugins:
  - with-pdf
theme:
  name: simple-blog
```

### ダイアグラム

mkdocs-marmaid2-plugin を追加しているため、 [marmaid](https://mermaid.js.org/) で作図してドキュメントで取り込むことができます。

`mkdocs.yml` の`plugins` のセクションを次のように定義します。

```
plugins:
  - mermaid2:
      search: 11.4.1
```

これにより `https://unpkg.com/mermaid@10.4.0/dist/mermaid.esm.min.mjs` を参照するHTMLが生成されます。

外部にアクセスさせたくない場合は次のように、 mermaid.esm.min.msj をダウンロードしてローカルに配置します。

```
$ mkdir  docs/javascript
$ pushd docs/javascript
$ curl -sLO https://unpkg.com/mermaid@10.4.0/dist/mermaid.esm.min.mjs
$ popd
```

この場合の `mkdocs.yml` は次のように定義します。
```
plugins:
  - mermaid2:
      javascript: javascript/mermaid.min.js
```

[kroki](https://kroki.io/) で作図することもできます。
ただし、kroki は Webサービスなため作図データといえ外に出したくない場合は、
kroki のコンテナーをDocks/Podman で起動して利用します。


- [yuzutech/kroki - Docker Image | Docker Hub](https://hub.docker.com/r/yuzutech/kroki)
- [yuzutech/kroki-mermaid - Docker Image | Docker Hub](https://hub.docker.com/r/yuzutech/kroki-mermaid)


```
$ podman run -d yuzutech/kroki-mermaid
```

`ServerUrl を次のように定義します。
`
```
plugins:
  - with-pdf:
  - mermaid2:
      javascript: javascript/mermaid.esm.min.mjs
  - kroki:
      ServerUrl: http://localhost:8000
```



### PDFで出力

`mkdocs.yml` に次の行を設定します。

```
site_name: My Docs
plugins:
  - with-pdf
```

この後は、`mkdocs build` を実行すると、
PDFファイルも生成されるようになります。

```
$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /home/goichi/sample/site
INFO    -  Number headings up to level 3.
INFO    -  Generate a table of contents up to heading level 2.
INFO    -  Generate a cover page with "default_cover.html.j2".
INFO    -  Converting <img> alignment(workaround).
INFO    -  Rendering for PDF.
INFO    -  Output a PDF to "/home/goichi/sample/site/pdf/document.pdf".
INFO    -  Converting 1 articles to PDF took 0.7s
INFO    -  Documentation built in 0.76 seconds
```

mdocs-with-pdf はmermaid はうまく処理してくれないため、
mkdocs-kroki-plugin を経由させるとうまくいきます。


```
plugins:
  - with-pdf:
  - mermaid2:
      javascript: javascript/mermaid.esm.min.mjs
  - kroki:
      FencePrefix: ''
      FileTypeOverrides:
        mermaid: png
```
### Markdown 拡張機能

mkdocs ではいくつかの[Markdown拡張機能](https://squidfunk.github.io/mkdocs-material/setup/extensions/)があります。

 - 目次([toc](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#table-of-contents))
 - 強調されたテキストブロック([admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/))
 - 脚注([footnotes](https://squidfunk.github.io/mkdocs-material/reference/footnotes/))
 - HTML属性拡張([attr_list](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown/#attribute-lists))
 - コードハイライト([pymdownx.superfences](https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#superfences))
 - アイコンや絵文字([pymdownx.emoji](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/)) の挿入
 - タグ([tags](https://squidfunk.github.io/mkdocs-material/setup/setting-up-tags/)) をページに設定。タグ検索などで使用。


### 便利なプラグイン

mkdocs で利用可能なプラグインをまとめている[A list of awesome MkDocs projects and plugins](https://github.com/mkdocs/catalog) からいくつかリストします。

- [search](https://squidfunk.github.io/mkdocs-material/plugins/search/)   
  ドキュメントを検索できるようにする
- [copyright](https://squidfunk.github.io/mkdocs-material/setup/setting-up-the-footer/#copyright-notice)  
  フッターにコピーライトを表示する
- [mkdocs-git-revision-date-localized-plugin](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin)  
  ページの作成日と更新日を表示する
- [mkdocstrings](https://github.com/mkdocstrings/mkdocstrings)  
  ソースコードからの自動ドキュメンテーションを行う
- [mkdocstrings-python](https://github.com/mkdocstrings/python)  
  Pythonソースコードからの自動ドキュメンテーションを行う
- [inari](https://github.com/tkamenoko/inari)  
  Python docstring を Markdown で記述できるようにする
- [mkdocs-coverage](https://github.com/pawamoy/mkdocs-coverage)  
  Coverageのレポートをドキュメントに取り込む
- [ansible-mkdocs](https://pypi.org/project/ansible-mkdocs/)  
  ロール/プレイブックからドキュメントを生成する
- [mkdocs-table-reader-plugin](https://github.com/timvink/mkdocs-table-reader-plugin)  
  CSV, Excelなどの表形式フォーマットファイルから表を自動生成する
- [markdown-captions](https://github.com/Evidlo/markdown_captions)  
  図のキャプションを作成
- [mkdocs-macros-plugin](https://github.com/fralau/mkdocs-macros-plugin)  
  ドキュメント中にユーザ定義変数が使えるようになる
- [mkdocs-awesome-pages-plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin)  
  ページタイトルとその順序の設定が簡単になる
- [mkdocs-include-markdown-plugin](https://github.com/mondeja/mkdocs-include-markdown-plugin)  
  別のMarkdown を取り込める
- [mdx_include](https://github.com/neurobin/mdx_include)  
  ローカル/リモートのファイルを任意の位置を抜き出してドキュメントに取り込む
- [markdown-exec](https://github.com/pawamoy/markdown-exec)  
  コマンドの実行結果をドキュメントに取り込む
- [mkdocs-no-sitemap-plugin](https://github.com/leonardehrenfried/mkdocs-no-sitemap-plugin)  
  サイトマップを生成しない
- [mkdocs-bootstrap-tables-plugin](https://github.com/byrnereese/mkdocs-bootstrap-tables-plugin?tab=readme-ov-file)  
  Markdownの表形式の出力をBootstrapのTableクラスで拡張して表を美しくする
- [mkdocs-import-statement-plugin](https://github.com/Rj40x40/mkdocs-import-statement-plugin)  
  Markdown にイメージやファイルをインポートできるようにする
  画像の取り込みが簡単になる。
- [mkdocs-mermaid2-plugin](https://github.com/fralau/mkdocs-mermaid2-plugin)  
  mermaid での作図をドキュメントに取り込む
- [mkdocs-kroki-plugin](https://github.com/AVATEAM-IT-SYSTEMHAUS/mkdocs-kroki-plugin)  
  kroki での作図をドキュメントに取り込む
- [mkdocs-plotly-plugin](https://github.com/haoda-li/mkdocs-plotly-plugin)  
  lotlyのjson構文を使ってデータからインタラクティブなチャートを作成する

## Markitdown

[Markitdown](()ttps://github.com/microsoft/markitdown)はMicrosfotがリリースしているMarkdown変換ツールです。
Office文書だけでなく、PDF、画像、音声、HTML、CSV、JSON、XMLといったものをMarkdownに変換することができます。
OpenAI GPT-4などのLLMと連携することで、画像の説明生成やテキスト抽出といった高度な機能も提供します。

Python から呼び出して利用することもできます。

```
from markitdown import MarkItDown

markitdown = MarkItDown()
result = markitdown.convert("sample.xlsx")
print(result.text_content)
```








## 参考資料

- [reStructuredText](https://docutils.sourceforge.io/rst.html)
- [https://docutils.sourceforge.io/rst.html](https://docutils.sourceforge.io/index.html)
- [sphinx](https://www.sphinx-doc.org/ja/master/) 美しいドキュメントを簡単に生成することができるドキュメンテーションツール
  - [Sphinx-User.JP](https://sphinx-users.jp/) Sphinxの日本ユーザ会
  - [sphinx-markdown-parse](https://github.com/clayrisser/sphinx-markdown-parser)
- [mkdocs](https://www.mkdocs.org/) Markdown から美しいドキュメントを簡単に生成することができるドキュメンテーションツール
- [mdutils](https://mdutils.readthedocs.io/en/latest/examples/Example_Python.html)
- [inari](https://github.com/tkamenoko/inari) Markdown で記述した docstring をパース 
- [microsfot/Markitdown](https://github.com/microsoft/markitdown)
- [autoDocstring - Python Docstring Generator - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [Awesome MkDocs](https://github.com/mkdocs/catalog?tab=readme-ov-file)
- [mkdocs-pdoc=-plugin](https://github.com/spirali/mkdocs-pdoc-plugin/)
- [mkdocs-with-pdfの使い方](https://try0.github.io/mkdocs-example/example-site/site/mkdocs-with-pdf.html)
- [kroki - Creates diagrams from textual descriptions!](https://kroki.io/)
- [mkdocs-kroki-plugin](https://github.com/AVATEAM-IT-SYSTEMHAUS/mkdocs-kroki-plugin)