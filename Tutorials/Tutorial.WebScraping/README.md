Pythonチュートリアル：Webスクレイピング
=================
![](https://gyazo.com/153a339305d78fc4fa4850753e4b1594.png)

# はじめに
ビッグデータやデータ分析などデータを扱う処理を行う場合では、大量のデータを取得する工程も重要になります。単純にCSV形式やEXCELファイルで配布されている情報であれば簡単なのですが、場合によってはWebページからデータを収集する必要があり、Webスクレイピングのテクニックが使われるようになりました。
Webスクレイピングでは、、クローラー、スクレイパー、スパイダーなど同じ意味で使われる言葉があります。この資料では以降、スクレイピングを行うプログラムをスクレイパーと表現するようにします。
スクレイパーは人間よりもはるかに速く、より深くデータを取得することができるため、行儀の悪い(サイト側から見ればタチの悪い)スクレイパーは、サイトのパフォーマンスに何らかの影響を与える可能性があります。このため、Webスクレイピングをブロックするような対策をとっているサイトもあります。
ここで、Webスクレイピングは、スクレイピング対象のサイトに有害な影響を与えることがないよう、責任を持って実行されなければならない作業であることを理解する必要があります。
ブロックしたいWebサイトへのスクレイピングの是非はともかく、ほとんど全ての個人や会社がWebスクレイピングによって得られたデータの恩恵を受けていることは事実です。
この資料は、なぜWebスクレイピングが重要なのかということと、スクレイピングの方法について簡単に説明しています。

# Webスクレイピングについて
Webスクレイピングとは、スクレイパーを使ってWebページにアクセスして、そこから使えるデータに変換して書き出すことです。ところで、なぜデータをスクレイピングする必要があるのでしょうか？例えば、あなたが持っている書籍をメルカリで販売したいときを考えてみましょう。おそらくは類似サイトなどもアクセスして販売価格の相場を知りたくなるはずです。力技を使うのであれば、ブラウザでアクセスしてそれらのリストをコピーして、Excelスプレッドシートに貼り付 ける作業を根気強く突ける必要があり、それは何時間もかかることがあるかもしれません。しかも、その作業がために販売機会を逃してしまうかもしれません。しかし、Webスクレイピングツールを使用すれば、このプロセスを自動化することができます。データを収集したら、CSV、JSON、またはXMLファイルとしてダウンロードすることができます。もう、手作業で大量のデータを収集する必要がないわけです。

# Webスクレイピングの適用事例
Webスクレイピングの適用事例には非常に多くのものがあります。いくつかの例を挙げてみます。

  - 価格モニタリング
  - マーケティングと潜在顧客の獲得
  - 店舗出店の最適化
  - ニュースおよびソーシャル・メディア
  - 不動産

スクレイピングで自動化できる作業には次のようなものがあります。

#### 価格モニタリング
もしあなたがオンラインショップの領域で働いているのであれば、マーケティングとして価格モニタリングを行って商品戦略を向上させたいと考えるかもしれません。Webスクレイピングは、次ののようなサイトから価格、在庫レベル、レビューを収集することができます。

  - Amazon
  - eBay
  - 楽天
  - メルカリ
  - その他eコマースストア

これらのデータを使って、競合他社と商品を比較し、オンラインショップを改善することができます。

### マーケティングと潜在顧客の獲得
売上を伸ばすには、商談率や契約率が高い潜在顧客の獲得することが重要です。これは「リードジェネレーション」と言われることもあります。しかし、潜在顧客の獲得し育成することは面倒な作業です。
。Webスクレイピングを使えば、会社の詳細、住所、ソーシャルメディアのアカウントを収集し、マーケティングの質を改善し、潜在顧客を獲得することができます。

### 店舗出店の最適化
もしあなたが店舗を出店したいすると、場所をどこにするか迷うかもしれません。Webスクレイピングは、一般に公開されているリソースから、次のような位置情報を収集することができます。

  - 学校
  - 病院
  - 美容院
  - コンビニ
  - スーパー
  - ホテル
  - レストラン
  - 倉庫

これらのデータセットを分析して、どのような要因が店舗経営に影響するかを推定して、最適な出店場所を決定することができます。

### ニュースとソーシャルメディア
ソーシャルメディアは、マーケティング担当者にとって貴重なツールです。ソーシャルメディアの公開情報を抽出すると、フォロワーが何に興味を持っているかパターンを知ることができます。

この情報は、次のようなことに利用できます。

  - ソーシャルメディアコンテンツの最適化
  - SEOの更新
  - 競合他社の監視
  - ターゲット顧客の特定

> 余談：YouTuber がよく見られているネタを分析するためにCloudWorksへ案件を出しているのを見たことがあります。

### 不動産
不動産は、扱う対象が高額になることから、Webスクレイピングが利用されている領域の一つです。次のような情報をスクレイピングも可能です。

  - 不動産業者
  - 販売(賃貸)価格の相場
  - 路面価格
  - 建築物の用途制限
  - 競売物件

Webスクレイピングツールは、多くのプロセスを自動化することができるようになります。

# Python のスクレイピングライブラリ
スクレイピングでよく使用されるPythonのライブラリには次のようなものがあります。

  - urllib: URLの解析
  - requests: Webサイトへのアクセスとデータ取得
  - BeautifulSoup: タグ解析とデータ抽出
  - lxml: タグ解析とデータ抽出
  - json: JSON形式のデータの読み書き
  - selenium: ヘッドレスブラウザを使ったWebサイトへのアクセスとデータ取得
  - pyppeteer: ヘッドレスブラウザを使ったWebサイトへのアクセスとデータ取得
  - request-html: オールインワン
  - scrapinghelper (request-htmlをベースにリパッケージ：私製 ^o^)

それぞれ特徴や役割があるのですが、おすすめは request-html です。この拡張ライブラリは、ヘッドレスブラウザを使ってWebサイトへのアクセスしデータ取得することができます。このライブラリは非常にシンプルで内部的には urllib、requests、pyppeteer、 lxml を呼び出しているだけなのですが、 このライブラリをおすすめする理由には、次の通りです。

  - 統一的なAPIの提供
  - 非同期I/Oをサポート
  - ヘッドレスブラウザのダウンロードと設定を自動的に処理

scrapinghelper は私が request-html をベースに、より簡単に使えるようにしたものです。( 宣伝 (^^)v )

# インストール

 bash
```
 # Linux or Mac
 $ python -m pip install scrapinghelper

 # Windows
 $ py -3 -m pip install scrapinghelper
```

scrapinghelper は request-html と numpy、padnas、loguru に依存しているため、これらのパッケージも合わせてインストールされます。


# スクレイピングのハンズオン
 `https://www.socks-proxy.net/` は公開プロキシをリストしているページです。
このサイトかプロキシの情報を抽出してCSVファイルにしてみましょう。

この処理は次のように数行のコードですみます。


```
 In [1]: # %load c01_get_stocks_list.py
    ...: import pandas as pd
    ...: from scrapinghelper import Scraper
    ...:
    ...: url = 'https://www.socks-proxy.net/'
    ...:
    ...: scraper = Scraper()
    ...: response = scraper.request(url)
    ...: proxy_list = scraper.get_texts(response.html)
    ...: df = pd.DataFrame(proxy_list[1:], columns=proxy_list[0])
    ...:
    ...: df.to_csv('socks_proxy_list.csv')

 In [2]: df.head()
 Out[2]:
        IP Address   Port Code             Country Version  Anonymity Https Last Checked
 0   46.101.37.189   7497   GB      United Kingdom  Socks4  Anonymous   Yes   4 mins ago
 1   64.124.191.98  32688   US       United States  Socks4  Anonymous   Yes   4 mins ago
 2     31.135.91.9   4145   RU  Russian Federation  Socks4  Anonymous   Yes   4 mins ago
 3    170.84.71.45   5678   BR              Brazil  Socks4  Anonymous   Yes   4 mins ago
 4  176.119.227.65   5678   KZ          Kazakhstan  Socks4  Anonymous   Yes   4 mins ago

 In [3]:

```

この `scraper.get_texts()` が何をしているのかを説明します。


```
 proxy_list = scraper.get_texts(response.html)

```

この行は次のコードと同じことをしています。


```
 proxy_list = [ x.text.split('\n')
               for x in response.html.find('table')[0].find('tr') ]

```

 `get_texts()` は与えられ request_html.HTML オブジェクトの  `find()` メソッドを使って　 `table` タグ(HTMLの表）を検出します。その結果の最初の要素に対して、続けて  `find()` メソッドで  `tr` (HTMLの表の行) を検出します。結果はリストで返されるので、各要素（つまり各行）を改行文字( `\n` )で分割したリストにします。
もう少し詳しく説明することにしましょう。

Scraper クラスを初期化して、 `request()` メソッドにURLを与えてを呼び出します。


```
 scraper = Scraper()
 response = scraper.request(url)

```

 `scraper.request()` は requests_html の  `get()` メソッドを呼び出して、URLで指定したページの内容(request_html.HTMLオブジェクト)を取得し、 `render()` を呼び出してJavaScript を実行した結果を返します。

この response.html は request_html.HTML オブジェクトで, `find()` メソッドがあるので、これを呼び出しているわけです。
 `.find()` メソッドにはセレクタを与えます。単純にはHTMLタグで構いません。

この場合  `table` では3つの結果が返され、その最初のエントリについて、つづけて  `tr` を検出しています。
結果的に今回は問題ありませんが、複数検出された結果の最初のエントリ以外を処理したいときは明示的に特定した要素を指定する必要があります。


# 要素を特定する方法
要素を特定する方法は、CSSセレクタとXPATHの2つがあります。一般的に XPATHの方が複雑になりやすいので、CSSセレクタを使用するようにして問題ありません。呼び出す関数が異なることに注意してください。

  - CSSセレクタ： `response.html.find()` に与える
  - XPATH： `resposen.html.xpath()` に与える

ところで、CSSセレクタをどうやって知ればよいのでしょう？

Chrome ブラウザで該当ページを開いているときに、ブラウザ内でマウス右クリックにより表示メニューから　<Inspect> を選択します。
![](https://gyazo.com/7c21bebf2288fe4cfc4dd4476e12b21a.png)
すると次のようにウィンドが分割されます。

![](https://gyazo.com/66e8f3ccba10ac62e2b7365d49cb255c.png)
縦三点リーダー( `︙` ) をクリックすると、<dock side> のメニューにアイコンがならんでいます。これを選択すると分割方法が変わります。
![](https://gyazo.com/9bfb175f2f933fc74b6ff79db769c057.png)


左から、別ウィンド、左に配置、下に配置、右に配置、です。

セレクトモードにして、表示されている内容をクリックすると該当するCSS要素を知ることができます。

![](https://gyazo.com/087bb883fb0ff5a1178be2716d4fb2b4.png)


セレクトモードで表のヘッダの  `IPAddress` をダブルクリックしてみてください。

![](https://gyazo.com/a4721a162734a17c27a6c2cefbe61e7b.png)


この要素は  `<td>` で、親要素が、 `<tr>` 、さらに遡れば `<table class="table table-striped table-bordered">` になっていることがわかりま>す。この `<table>` 要素をマウスで選択して、マウス右ボタンメニューから
 `<Copy> -> <Copy Selector>` を選択すると、そのCSSセレクタがクリップボードにコピーされます。
XPATHが必要な場合は、 `<Copy> -> <Copy XPATH>` を選択します。


この例の場合は、次の内容になります。

 `#list > div > div.table-responsive > div > table`

これを与えると特定要素を選択することができます。


```
 selector = [
    "#list > div > div.table-responsive > div > table",
    "tr",
 ]

 scraper.get_texts(response.html, selector)

```

# Yahooジャパンのニュースのリンクを取得
こんどは、Yahooジャパンのニュースのリンクを取得してみましょう。
![](https://gyazo.com/d50d434b89e9c59a288a66980a3ebce2.png)

まず、news.yahoo.co.jp がスクレイピングを許可しているかどうかを確認します。

 bash
```
 $ curl -s https://news.yahoo.co.jp/robots.txt
 User-agent: *
 Disallow: /comment/plugin/
 Disallow: /comment/violation
 Disallow: /profile/violation
 Disallow: /polls/widgets/
 Disallow: /articles/*/comments
 Disallow: /articles/*/order
 Sitemap: https://news.yahoo.co.jp/sitemaps.xml
 Sitemap: https://news.yahoo.co.jp/sitemaps/article.xml
 Sitemap: https://news.yahoo.co.jp/sitemaps/byline.xml:jjjjjjjj
```

基本的なニュースの一覧についてはダメとはいわれていません。
これで安心してスクレイピングできます。

HTMLではリンクはaタグを使って表現されています。

例えば次のような記述されます。

 HTML
```
 <a href="https://google.com">Google</a>
```

scrapinghelper の  `get_links()` メソッドを使うと、ページ内のすべてのaタグを取得することができます。


```
 In [2]: # %load c02_get_yahoo_news.py
    ...: from scrapinghelper import Scraper
    ...:
    ...: url = 'https://news.yahoo.co.jp'
    ...:
    ...: scraper = Scraper()
    ...: response = scraper.request(url)
    ...:
    ...: news_links = scraper.get_links(response.html)
    ...:

 In [3]: news_links[:2]
 Out[3]:
 [TAG_LINK(text='「男性のがん予防にも」HPVワクチンが注目されている理由', link=https://rdr.yahoo.co.jp/v1/label=L21lbXBmL21oZC91aGQvcGMvOTM4NzMvMTI1MTA0LzEwMTE0NjUvMQ/p=mempf/d=mempf_redirect_api_log/tk=8dec6df6-7d6e-4085-b834-5afb49ed6c82/ru=aHR0cHM6Ly9zZGdzLnlhaG9vLmNvLmpwL29yaWdpbmFscy8xMjAuaHRtbD9jcHRfbj1VSEQmY3B0X209dWhkJmNwdF9zPWFsbA/),
  TAG_LINK(text='ジューシーで果汁たっぷり、各地のおいしい桃を味わおう', link=https://rdr.yahoo.co.jp/v1/label=L21lbXBmL21oZC91aGQvcGMvOTM4NzMvMTI1MTA0LzEwMTE0NjUvMg/p=mempf/d=mempf_redirect_api_log/tk=8dec6df6-7d6e-4085-b834-5afb49ed6c82/ru=aHR0cHM6Ly95ZWxsbWFya2V0LnlhaG9vLmNvLmpwL3NwZWNpYWxsaXN0L3NlYXNvbi9wZWFjaC8/)]

 In [4]: len(news_links)
 Out[4]: 130

```

すべてのリンクを取得するため期待通りに取得できていません。また、ニュース以外のものも結果に混入しています。


```
 In [5]: news_links[-5:]
 Out[5]:
 [TAG_LINK(text='運営方針', link=https://news.yahoo.co.jp/info/news-operation-policy),
  TAG_LINK(text='著作権', link=https://support.yahoo-net.jp/PccNews/s/article/H000006460),
  TAG_LINK(text='特定商取引法の表示', link=/info/commercial-transactions),
  TAG_LINK(text='ご意見・ご要望', link=https://support.yahoo-net.jp/voc/s/news),
  TAG_LINK(text='ヘルプ・お問い合わせ', link=https://support.yahoo-net.jp/PccNews/s/)]

 In [6]:

```

 `get_links()` では次のパラメタを受け取ることができます。

  -  `startswith` : URLのbasename がこの文字列で始まっていなければ無視する。
  -  `endswith` : URLのbasename がこの文字列で終わっていなければ無視する。
  -  `containing` : デコードされたURL にこの文字列で入っていなければ無視する。

これらは文字列もしくは文字列のリストで与えることができます。
URLの basename はURLクラスでパースされて設定されます。


```
 In [1]: from scrapinghelper import URL

 In [2]: url = URL('http://www.example.com/sample?src=git&encode=jp')

 In [3]: url.is_valid
 Out[3]: True

 In [4]: url.attrs
 Out[4]:
 {'url': 'http://www.example.com/sample?src=git&encode=jp',
  'is_valid': True,
  'scheme': 'http',
  'netloc': 'www.example.com',
  'username': None,
  'password': None,
  'hostname': 'www.example.com',
  'port': None,
  'path': '/sample',
  'params': '',
  'query': 'src=git&encode=jp',
  'fragment': '',
  'basename': 'sample'}

 In [5]:

```

日本語などのようにURLに適さない文字列はエンコードして使用します。デコードされたURLというのは元の文字列に変換したもののことです。
例を見る方が理解が速いでしょう。


```
 In [1]: from scrapinghelper import URL

 In [2]: url = URL('http://www.example.com/データ.txt')

 In [3]: url
 Out[3]: http://www.example.com/%E3%83%87%E3%83%BC%E3%82%BF.txt

 In [4]: url.decode()
 Out[4]: 'http://www.example.com/データ.txt'

 In [5]:

```

さて、 Yahooニュースでトップにならぶリンクには"pickup" の文字列があるので、これを利用すると期待通りにニュースのリンクだけを抜き出せます。


```
 In [1]: # %load c03_get_pickup_news.py
    ...: from scrapinghelper import Scraper
    ...:
    ...: url = 'https://news.yahoo.co.jp'
    ...:
    ...: scraper = Scraper()
    ...: response = scraper.request(url)
    ...:
    ...: news_links = scraper.get_links(response.html, containing="pickup")

 In [2]: len(news_links)
 Out[2]: 9

 In [3]: news_links[:2]
 Out[3]:
 [TAG_LINK(text='西日本-東北 局地的に激しい雷雨', link=https://news.yahoo.co.jp/pickup/6433808),
  TAG_LINK(text='「GX担当相」に萩生田氏を任命', link=https://news.yahoo.co.jp/pickup/6433807)]

 In [4]:

```

この結果をCSVにするときは、次のようにします。


```
 In [4]: import pandas as pd

 In [5]: df = pd.DataFrame(news_links, columns=['title', 'link'])

 In [6]: df
 Out[6]:
               title                      link
 0  西日本-東北 局地的に激しい雷雨  https://news.yahoo.co...
 1   「GX担当相」に萩生田氏を任命  https://news.yahoo.co...
 2  双方に得 政治と旧統一教会の関係  https://news.yahoo.co...
 3  夏休みに学童での感染増 都が警戒  https://news.yahoo.co...
 4  独ルフトハンザで欠航 日本便遅れ  https://news.yahoo.co...
 5    カーリング・吉田知那美が結婚  https://news.yahoo.co...
 6   瀬戸康史 母親の応募で人生激変  https://news.yahoo.co...
 7  香川照之 エキストラ役で映画主演  https://news.yahoo.co...
 8   瀬戸康史 母親の応募で人生激変  https://news.yahoo.co...

 In [7]: df.to_csv('news.csv')

 In [8]:

```

# JavaScript で動的に処理されるページの場合

[国税庁法人番号公表サイト ](https://www.houjin-bangou.nta.go.jp/download/zenken/) には、公表されている全ての法人の月末時点の最新情報を全国又は所在地（各都道府県及び国外の単位）で分類されまとめられています。例えば京都府の法人番号のCSV形式UNICODEのデータを取得したいとします。ブラウザでは単純に近畿の行の京都府のカラムにあるリンクをクリックすればOKなのですが、これをスクレイピングするとなると少しテクニックが必要になります。
次のコードはページソースを抜粋です。

 HTML
```
 <td>
   <dl class="mb00">
     <dt class="mb05">京都府</dt>
     <dd>
       <ol class="listNone mb00">
           <li><a href="#" onclick="return doDownload(16654);">zip 5MB</a></li>
       </ol>
     </dd>
   </dl>
 </td>
```

このリンクはHTMLの  `a` タグで記述はされていますが、リンクがなくJavaScriptの関数にファイルIDを与えて処理しているためです。

 HTML
```
     <script type="text/javascript">
         function doDownload(fileNo) {
             $("#selDlFileNo").val(fileNo);
             $("#appForm").submit();
             return false;
         }
     </script>
```

このサイトのように、JavaScriptによる動的な処理が必要な場合はヘッドレスブラウザを使ってスクレイピングする必要があります。

そして、このページはフォームになっていてJavaScriptがトークンキーをPOSTで送信するようになっています。次のコードはページソースのフォーム定義の抜粋です。（内容が変わらない範囲で、改行など整形しています）

 HTML
```
 <form id="appForm"
       action="/download/zenken/index.html"
       method="post">
   <div>
     <input type="hidden"
            name="jp.go.nta.houjin_bangou.framework.web.common.CNSFWTokenProcessor.request.token"
            value="a652db1b-b7a4-4076-b614-d53417016a4d">
     </div>
     <input type="hidden" name="event" id="event" value="download">
     <input type="hidden" name="selDlFileNo" id="selDlFileNo">
     <div class="inBox21">
       <h2 class="title" id="csv-sjis">CSV形式・Shift_JIS</h2>
       <p class="txtS">
         令和4年6月30日更新
       </p>

```

 ` <input type="hidden"` の部分で、 `name` の値がトークンキーで　 `value` がトークンです。
POST時につぎの辞書をデータとしいて与える必要があります。
（今時点では単に変数にしています）


```
 {
      f'{TOKEN_KEY}　:　{TOEKN}',
      "event" : 'download',
      f'"selDlFileNo": {FILEID}'.
  }
```

ここでページソースからトークンを人が読んでスクレイパーのコードにハードコーディングすると、トークンが変わったときにうまう処理できなくなってしまいます。スクレイパーでトークンを取得する方が望ましいでしょう。APIの設計をする側の尾視点で考えると、トークンキーの変更は常識的にはほとんどないはずです。トークンキーはハードコーディングしてもよいでしょう。


```
 class DatasetError(BaseException):
     pass

 class CNScrapper(object):

     _BASE_URL = 'https://www.houjin-bangou.nta.go.jp/download'
     _INDEX_URL = f'{_BASE_URL}/zenken/'
     _DOWNLOAD_URL = f'{_BASE_URL}/zenken/index.html'
     _TOKEN_KEY = ( 'jp.go.nta.houjin_bangou.framework.web.common'
                    '.CNSFWTokenProcessor.request.token' )
     _CSV_UNICODE_TABLE_XPATH = '//*[@id="appForm"]/div[2]/div[2]/table/tbody'
     _CSV_UNICODE_TABLE_SELECTOR = '#appForm > div.inBox21 > div:nth-child(7) > table'
     _ATTACHFILE_PREFIX="attachment; filename*=utf-8'jp'"

     def __init__(self):
         from scrapinghelper import Scraper

         self.scraper = Scraper()
         self.response = self.scraper.request(self._INDEX_URL)
         self.fileids = self.gathering_fileids(self.response.html)
         self.token = self.response.html.find(f'input[name="{self._TOKEN_KEY}"]',
                                              first=True)
         try:
             self.post_form = {
                f'{self._TOKEN_KEY}': f'{self.token.attrs["value"]}',
                "event" : 'download',
             }
         except AttributeError:
             raise DatasetError('Could not get token') from None

```

ファイルIDは  `table` タグ中の  `a` タグの  `onclick` 属性で指定されているJacaScriptの関数呼び出しの形でコードされているます。　 `a` タグを取得してあと、 `onclick` 毒性の値を加工すると得られます。


```
     def gathering_fileids(self, html):
         fileid_cache = dict()
         # htmltable =  html.xpath(self._CSV_UNICODE_TABLE_XPATH, first=True)
         htmltable =  html.find(self._CSV_UNICODE_TABLE_SELECTOR, first=True)
         if htmltable is not None:
             atags = htmltable.find('a')
         else:
             atags = []
         for entry in atags:
             for e in entry.element.iterancestors():
                 if e.tag == 'dl':
                     dt = e.find('dt')
                     if dt is not None:
                        for ee in e.iterdescendants():
                             if ee is not None and ee.tag == 'a':
                                 fileid = ( ee.get('onclick')
                                            .replace('return doDownload(','')
                                            .replace(');', ''))
                                 fileid_cache[dt.text] = fileid
         return fileid_cache

```


ダウンロードの処理は次のようなコードになります。


```
     def download(self, prefecture='all'):
         prefecture = self.name_normalized(prefecture)
         try:
             assert prefecture in self.fileids.keys()
             self.post_form['selDlFileNo'] = f'{self.fileids[prefecture]}'
             response = self.scraper.session.post( url=self._DOWNLOAD_URL,
                                           data=self.post_form)

         except AssertionError:
             raise DatasetError('id not available') from None

         except HTTPError as err:
             raise DatasetError(err)

         # print(response.headers)
         self.filename = self._get_filename(response.headers)
         with open(self.filename, 'wb') as save:
                 save.write(response.content)
         return self.filename

```


POST送信した応答ヘッダの  `"Content-Disposition"` にファイル名が記述されています。


```
     def _get_filename(self, headers):
             try:
                 c = headers['Content-Disposition']
                 filename =c.replace(self._ATTACHFILE_PREFIX, '')
             except:
                 filename = None
             return filename

```

ダウンロードしたファイルはCSVファイルをZIPで圧縮したファイルなので、データにアクセスするためには次のような処理が必要になります。


```
     def load_data(self, filepath):
         df = None
         with ZipFile(filepath, 'r') as zipobj:
             for innerfile in zipobj.namelist():
                 if innerfile.endswith('csv'):
                     csvfile = zipobj.extract(innerfile)
                     df = pd.read_csv(csvfile)
                     os.unlink(csvfile)
         return df

```

完全なソースコードを　[GitHub corporate-numbers ](https://github.com/iisaka51/corporate_numbers/) で公開しています。

# まとめ
実際のスクレイピングではより複雑な例が多くあります。例えばログインの向こう側にあるデータなどです。注意するべき点としては、Webサーバに負荷をかけないように丁寧に処理することを心がけるべきです。



#Webスクレイピング


