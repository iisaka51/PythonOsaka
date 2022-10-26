Pythonチュートリアル：Webスクレイピングでのブロック回避
=================
![](https://github.com/iisaka51/PythonOsaka/blob/main/data/images/Python_Logo.png)

# はじめに
この資料は、なぜWebスクレイピングでブロックされないための方法について説明しています。

# スクレイピングでのブロック回避
ブロックされずにスクレイピングするために、守るべきWebスクレイピングの方法には次のようなものがあります。

  -  `robots.txt` を尊重する
  - スクレイパーを遅くしてWebサイトを優しく扱う
  - 同じアクセスパターンを繰り返さない
  - プロキシを利用してアクセスする
  - リアルなユーザーエージェントを使用する
  - 単純なリクエストヘッダの使用を避ける
  - HTTPリクエストヘッダをリクエストごとにローテーションする。
  - ヘッドレスブラウザを使用する。 (Puppeteer、Selenium、Playwright、etc...)
  - ハニーポットの罠に注意する
  - ウェブサイトのレイアウトが変更されていないか確認する
  - ログインの背後にあるデータのスクレイピングを避ける
  - CAPTCHA突破サービスを使用する
  - ウェブサイトがブロックまたは禁止しているかどうかを調べる

これは、Webサイトがスクレイピングを検知する方法を理解することにも通じます。
では、説明してゆきましょう。

# robots.txt を尊重する
ほとんどのWebサイトでは  `robot.txt` ファイルを提示していています。このファイルには、スクレイピングの頻度、サイトのどのページでスクレイピングが許可/禁止されているかなど、守って欲しい具体的なルールが記述されています。そのため、Webスクレイピングを行う場合は、 `robot.txt` ファイルのルールに従うことが望ましく、ルールに違反するという理由でブロックされることにもなります。

Webサイトをどのように運営するかはサイト管理者の権限であり自由なため、Webサイトによっては、Google にだけスクレイピングを許可しているようなところもあります。

 `robot.txt` ファイルは、通常、 Webサイトのドキュメントルートディレクトリに存在しています。
他の場所にある場合でも、 `robots.txt` に移動先の情報が提示されています。
例えば、Google では次のようになっています。

 bash
```
  $ curl -s http://google.com/robots.txt
  <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
  <TITLE>301 Moved</TITLE></HEAD><BODY>
  <H1>301 Moved</H1>
  The document has moved
  <A HREF="https://www.google.com/robots.txt">here</A>.
  </BODY></HTML>
```

 bash
```
  $ curl -s http://www.google.com/robots.txt
  User-agent: *
  Disallow: /search
  Allow: /search/about
  Allow: /search/static
  Allow: /search/howsearchworks
  Disallow: /sdch
  Disallow: /groups
  Disallow: /index.html?
  （中略)
  Disallow: /local/place/rap/
  Disallow: /local/tab/
  Disallow: /localservices/*
  Allow: /finance
  Allow: /js/
  Disallow: /nonprofits/account/
  Disallow: /fbx

  # AdsBot
  User-agent: AdsBot-Google
  Disallow: /maps/api/js/
  Allow: /maps/api/js
  Disallow: /maps/api/place/js/
  Disallow: /maps/api/staticmap
  Disallow: /maps/api/streetview

  # Crawlers of certain social media sites are allowed to access page markup when google.com/imgres* links are shared. To learn more, please contact images-robots-allowlist@google.com.
  User-agent: Twitterbot
  Allow: /imgres

  User-agent: facebookexternalhit
  Allow: /imgres

  Sitemap: https://www.google.com/sitemap.xml

```

 `robots.txt` が次のようになっていると、このサイトはスクレイピングされることを拒否していることを意味しています。

 robots.txt
```
 code: robotss.txt
 User-agent: *
 Disallow: /
```

実際のところは、ほとんどのサイトは間違いなくGoogleやYahooなどの検索サイトに掲載されることを望んでいるため、スクレイパーへのアクセスを許可しています。

 `robots.txt` で `Disabllow` とされているページもスクレイピングしようとすることは可能です。その場合、アンチスクレイピングツールが導入されているWebサイトでは、スクレイピングがブロックされることがあります。これらのツールは、人間ではないと推定される特徴や規則性を見つけようとします。スクレイパーによるアクセスには次のような特徴があります。

  - 人間よりも速く、多くのページにアクセスしている。
  - 同じアクセスパターンが連続する。
  - 同じIPアドレスからのリクエストが短時間に多すぎる。
  - 高いダウンロード率
  - 不明なブラウザからアクセスしている。
  - 非常に古いブラウザのUser-Agent文字列を使用している。

これらのポイントを押さえれば、Webサイトがスクレイピングをブロックするために使用している中級程度のアンチスクレイピングであればクリアできるようになります。

# スクレイパーを遅くしてWebサイトを優しく扱う
クレイピングに限らずWebサイトにアクセスを行うと、サーバ側はこちらのIPアドレスとアクセスしたページは見えています。サイトは、ユーザ何をしているか、データを収集しているか、どのページに滞留しているかを知ることができるわけです。これらの情報は、広告収入を得ているようなサイトでは非常に重要になるので、ユーザーのパターンを収集しています。
1日24時間、毎秒1回のリクエストを送信するスクレイパーを検出するのは簡単です。人間がWebサイトへそんなアクセスすることは不可能なので、このような明白なパターンは簡単にスクレイパーのアクセスだと検出することができます。ブロックされないようにするために、ランダムな遅延（例えば、2〜10秒のランダム間隔）を使用するようにします。リ
クエストの応答がどんどん遅くなっているのを把握したときは、Webサイトのサーバーに負担をかけないように、もっとゆっくりリクエストを送るようにしてください。

丁寧なスクレイパーは、サイトの `robots.txt` のルールに従います。 `robots.txt` には、 `Crawl-delay:` という行が設定されていることがあり、サイトにリクエストを送る間に何秒待てば、サーバーへの負荷の問題を引き起こすことはないかが示されています。この時間だけ遅延した間隔でアクセスすることが理想的です。

# 同じアクセスパターンを繰り返さない
一般的に人間は気まぐれでランダムなアクションでサイトをアクセスするため、反復的な
処理を繰り返すことはほとんどありません。

スクレイパーはプログラムに従って動作するため、必然的に同じアクセスパターンになり
がちです。インテリジェントなアンチクローリングを取り入れているサイトは、スクレイ
パーのアクセスパターンを見つけることによって簡単に検出することができ、Webスクレイピングをブロックすることができます。通常、次のような情報はWebサイト側で監視されています。

  - 訪問したページ
  - 訪問したページの順番
  - HTTP Referrerと前回訪問したページのクロスマッチング
  - ウェブサイトへのリクエスト数
  - ウェブサイトへのリクエストの頻度

これの情報から、次にようなパターンはスクレイパーだと認識されることになります。

  - 同じ秒数間隔でアクセスしている。
  - 検索結果の全ページを巡回し、各結果のリンクへ順に移動している
  - 表示(あるいはインデックス)の順序で全てのファイルをダウンロードしている

人間であればこんなアクセスの仕方はしません(できません)。ページ上のランダムなクリック、マウスの動き、ランダムなアクションを取り入れることで、スパイダーを人間のように見せることができます。

# プロキシを利用してアクセスする

前述したように、Webサイトへのアクセスはサーバー側で把握され記録されています。
そして、Webサイトがスクレイパーを検出する方法の基本は、IPアドレスを調べることです。 大量のリクエストが特定のIPアドレスからのものであれば、ブロックされる可能性が非常に高くなります。ブロックされなくても特定に時間内のアクセスが多くなるとビジ
ーページを表示するようなサイトもあります。
いくつかの異なるIPアドレスを使用することでこれを避けることができます。
プロキシ(PROXY)からリクエストを送信すると、ターゲットのWebサイトは元のIPがどこの
ものかを知ることができず、検出が難しくなります。

発信者のIPアドレスを変更できる方法はいくつかあります。

  - TORブラウザ
  - VPN
  - 無料プロキシサービス
  - 共有プロキシサービス
    - 多くのユーザーによって共有されている最も安価なプロキシです。ただしブロックされる可能性も高い。
  - プライベートプロキシ
    - 通常は自分だけが使用するプロキシで、頻度を低くすればブロックされる可能性は低くなります。
  - データセンタープロキシ
    - IPアドレスと高速なプロキシ、大規模なIPアドレスプールの数が必要な場合に使用されます。住宅用ロキシよりも安価ですが、簡単に検出される可能性があります。

また、様々な商用プロバイダーがIPアドレスの自動ローテーションのサービスを提供しています。

![](https://gyazo.com/9dfa5c09ccc727486a130ef99aa9f71c.png)
[. プロキシプールを自動ローテーションの概要(FreeProxtListから引用)]

すべてのリクエストを同じIPアドレスで送信しないようにするには、ScraperAPIなどのIPローテーションサービスや他のプロキシサービスを使用して、リクエストを一連の異なるIPアドレスにルーティングすることが可能です。これによって、大半のWebサイトを問題なくスクレイピングできるようになります。

要に応じて使用できるIPアドレスのプールを作成し、各リクエストごとににランダムに
選択して使用するようにします。ただし、検索を行いその結果を参照するなどの一連のリ
クエストでは同一のIPアドレスである必要があります。


より高度なプロキシブラックリストを使用しているサイトでは、住宅用またはモバイル用プロキシを使用してみる必要があるかもしれません。実際￥￥のところ、世界のIPアドレスの数は有限で固定されており、インターネットにアクセス
する人々の大半は、 インターネットサービスプロバイダによって与えられたひとつのIPアドレスを使っています。したがって、1万のIPアドレスを持っていることは1万人のユーザからのアクセスと同じことなので、疑われることなく通常のインターネットユーザーと同じようにWebサイトにアクセスすることができます。IPアドレスでのブロックはサイトにとって最も一般的な方法になるため、もしブロックされた場合は、まず最初に試してみる対処方法です。

# リアルなユーザーエージェントを使用する
ユーザーエージェント(User-Agent)は、HTTPヘッダーの特殊なタイプで、アクセスしているWebサイトに、使用しているブラウザの情報をサーバに知らせます。Webサイトによっては、ユーザーエージェントを調べ、主要なブラウザに属さないユーザーエージェントからのリクエストをブロックすることがあります。ほとんどのスクレイパーは、ユーザーエージェントをわざわざ設定しないため、ユーザーエージェントが見つからないかどうかをチェックすれば、簡単に検出することができます。

例えば、次のコードはPythonのスクレイピングのためのライブライ requests が送出しているリクエストヘッダを知るためのものです。


```
 In [2]: # %load c01_headers_of_requests.py
    ...: import requests
    ...: from pprint import pprint
    ...:
    ...: response = requests.get('http://httpbin.org/headers')
    ...: pprint(response.json())
    ...:
 {'headers': {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate',
              'Host': 'httpbin.org',
              'User-Agent': 'python-requests/2.28.1',
              'X-Amzn-Trace-Id': 'Root=1-62de2fbf-3dfd0f200170ab5a0530e751'}}

 In [3]:

```

 `X-Amzn-Trace-Id:` は無視してください。これは、HTTPBinサービスが使用しているAmazon Load Balancer が生成しているものです。

この例にあるように、'User-Agent' に  `'python'` ,  `'java'` ,  `'curl'` などがあるときは、 スクレイパーからのアクセスだと簡単に識別することができます。

例えばWebサーバーの代表的な Nginx では設定ファイルで簡単に閲覧禁止としたり、別ページにリダイレクトさせることができます。server セクションの中であればどの設定ファイルでも構いません。

 nginxの設定　閲覧禁止
```
 if ($http_user_agent ~* "java|curl|python") {
     return 403;
 }

```

 nginxの設定　リダイレクト
```
 if ($http_user_agent ~* "java|curl|python") {
     return 301 https://yoursite.com;
 }
```

オープンソース [p0f ](https://salsa.debian.org/pkg-security-team/p0f)は、ユーザーエージェントが偽造されているかどうかを見分けることができます。

スクレイパーには、一般的なリアルなユーザエージェントを設定することを忘れないでください。Google Chrome、Safari、Firefoxなどが新しくアップデートされるたびに、ユーザーエージェントが全く異なるため、何年もユーザーエージェントを変更せずにいると、スクレイパーが怪しまれることになります。使用するユーザーエージェントは比較的最新のものにすることを忘れないようにすることが大切です。また、1つのユーザーエージェントからサイトへのリクエストが突然急増しないように、いくつかの異なるユーザーエージェントをローテーションで使用することも重要です。同じユーザエージェントからのアクセスは簡単に検知されてしまいます。

# 単純なリクエストヘッダの使用を避ける
物のウェブブラウザは、多くのヘッダを設定しており、注意深いウェブサイトはそのどれかをチェックして、あなたのウェブスクレイパーをブロックすることができます。スクレイパーを本物のブラウザのように見せるには、ブラウザで  `https://httpbin.org/anything` をアクセスて表示されるヘッダ情報をコピーするようにします。これらの情報は、アクセスで使用したブラウザが使っているヘッダになります。
次の値が設定されていると、リクエストが本物のブラウザから来たように見えるので、スクレイパーがブロックされることがほとんどなくなります。

  -  `"Accept"`
  -  `"Accept-Encoding"`
  -  `"Accept-Language"`
  -  `"Upgrade-Insecure-Requests"`

[scrapinghelper ](https://github.com/iisaka51/scrapinghelper) は、収集されたリアルなユーザエージェントを10000エントリ保持していて、これを利用しながらアクセスすることができるようになっています。また、ヘッダ情報も初期化時に自動的に設定してくれます。


```
 In [1]: # %load examples/check_headers.py
    ...: import scrapinghelper as sch
    ...: from pprint import pprint
    ...:
    ...: scraper = sch.Scraper()
    ...: response = scraper.request('http://httpbin.org/headers')
    ...:
    ...: pprint(response.json())
 {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en',
              'Host': 'httpbin.org',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) '
                            'AppleWebKit/600.1.4 (KHTML, like Gecko) '
                            'Mobile/12B440',
              'X-Amzn-Trace-Id': 'Root=1-62de3626-07daf491262b96356486884d'}}

 In [2]: scraper.get_random_user_agent()
 Out[2]: 'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36'

 In [3]: scraper.get_random_user_agent()
 Out[3]: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/'

 In [4]: scraper.get_random_user_agent()
 Out[4]: 'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36'

 In [5]:
```

# リファラーを設定する

httpリクエストヘッダの `"Referer:"` は、どのサイトから来たかを知らせるものです。一般的には、初回のアクセスには Googleから来たように見えるように設定すると良いでしょう。

 HTTPリクエストヘッダ（部分）
```
 "Referer": "https://www.google.com/"

```

[similarweb.com ](https://www.similarweb.com) のようなサービスを使うと、 任意のサイトへの最も一般的なリファラーを調べることもできます。多くの場合、これは Youtube などのソーシャルメディア・サイトになるかもしれません。
リファラーを設定したヘッダをもつアクセスは、多くのトラフィックが来ることを期待しているサイトからのトラフィックであるように見えるため、リクエストがさらに本物らしく見えるようになります。

# HTTPリクエストヘッダをリクエストごとにローテーションする
同じHTTPリクエストヘッダを使ってアクセスすることは、つまり同じブラウザでアクセスしていることになるため、リクエストをするたびに変更してアクセスすることが重要です。これは特にユーザエージェントについて注意するべきです。
IPアドレスとヘッダをローテーションしながらアクセスすることで、一般的なWebサイトからブラックされることはほんとどなくなるはずです。

次のコードは、requests を使ったユーザエージェントのローテーションを行う例です。


```
 In [2]: # %load c03_random_user_agent_for_requests.py
    ...: import random
    ...: import requests
    ...: from pprint import pprint
    ...:
    ...: url = 'http://httpbin.org/headers'
    ...: user_agent_list = [
    ...:  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; WOW
    ...: 64; Trident/5.0; BOIE9;ENUS)',
    ...:  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; WOW
    ...: 64; Trident/5.0; BOIE9;ENUS)',
    ...:  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-u
    ...: s) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.
    ...: 4 Safari/531.21.10',
    ...:  'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML,
    ...:  like Gecko) Chrome/13.0.782.112 Safari/535.1',
    ...:  'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; Sony Xper
    ...: ia Tablet Z - 4.2.2 - API 17 - 1920x1200 Build/JDQ39E) A
    ...: ppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari
    ...: /534.30',
    ...:  'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900P Buil
    ...: d/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Samsung
    ...: Browser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
    ...: ]
    ...:
    ...: headers = {
    ...:     'Accept': 'text/html,application/xhtml+xml,applicati
    ...: on/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application
    ...: /signed-exchange;v=b3;q=0.9',
    ...:     'Accept-Encoding': 'gzip, deflate, br',
    ...:     'Accept-Language': 'en',
    ...:     'Host': 'httpbin.org',
    ...:     'Upgrade-Insecure-Requests': '1',
    ...: }
       ...:
       ...: for n in range(1, 5):
       ...:     user_agent = random.choice(user_agent_list)
       ...:     headers['User-Agent'] = user_agent
       ...:     response = requests.get(url, headers=headers)
       ...:     print(f'Request: #{n}')
       ...:     pprint(response.json())
       ...:
    Request: #1
    {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'en',
                 'Host': 'httpbin.org',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900P '
                               'Build/LRX21V) AppleWebKit/537.36 (KHTML, like '
                               'Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 '
                               'Mobile Safari/537.36',
                 'X-Amzn-Trace-Id': 'Root=1-62df43eb-70b9c05659d72409702e3b4f'}}
    Request: #2
    {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'en',
                 'Host': 'httpbin.org',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 '
                               '(KHTML, like Gecko) Chrome/13.0.782.112 '
                               'Safari/535.1',
                 'X-Amzn-Trace-Id': 'Root=1-62df43ec-189f818e284dece133c49ac9'}}
    Request: #3
    {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'en',
                 'Host': 'httpbin.org',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 '
                               '(KHTML, like Gecko) Chrome/13.0.782.112 '
                               'Safari/535.1',
                 'X-Amzn-Trace-Id': 'Root=1-62df43ec-0618cd00015478463a1be740'}}
    Request: #4
    {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept-Language': 'en',
                 'Host': 'httpbin.org',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900P '
                               'Build/LRX21V) AppleWebKit/537.36 (KHTML, like '
                               'Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 '
                               'Mobile Safari/537.36',
                 'X-Amzn-Trace-Id': 'Root=1-62df43ed-5ce0fab719bbfe0e3d8660da'}}

    In [3]:

```

scrapinghelper を使うともっと簡単に記述することができます。


```
 In [2]: # %load c04_random_user_agent_for_scrapinghelper.py
    ...: import scrapinghelper as sch
    ...: from pprint import pprint
    ...:
    ...: url = 'http://httpbin.org/headers'
    ...:
    ...: scraper = sch.Scraper()
    ...:
    ...: for n in range(1, 5):
    ...:     response = scraper.request(url, user_agent='random')
    ...:
    ...:     print(f'Request: #{n}')
    ...:     pprint(response.json())
    ...:
 Request: #1
 {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en',
              'Host': 'httpbin.org',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; D6503 '
                            'Build/23.0.1.A.0.167) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/37.0.2062.117 Mobile '
                            'Safari/537.36 OPR/24.0.1565.82529',
              'X-Amzn-Trace-Id': 'Root=1-62df4714-6c11bc6b280264b52cd4a96b'}}
 Request: #2
 {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en',
              'Host': 'httpbin.org',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; D6503 '
                            'Build/23.0.1.A.0.167) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/37.0.2062.117 Mobile '
                            'Safari/537.36 OPR/24.0.1565.82529',
              'X-Amzn-Trace-Id': 'Root=1-62df4721-6b0c8a665ae67a014a96c0d8'}}
 Request: #3
 {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en',
              'Host': 'httpbin.org',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; D6503 '
                            'Build/23.0.1.A.0.167) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/37.0.2062.117 Mobile '
                            'Safari/537.36 OPR/24.0.1565.82529',
              'X-Amzn-Trace-Id': 'Root=1-62df472d-2ce9683e4500fb5d33c78e1c'}}
 Request: #4
 {'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'en',
              'Host': 'httpbin.org',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; D6503 '
                            'Build/23.0.1.A.0.167) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/37.0.2062.117 Mobile '
                            'Safari/537.36 OPR/24.0.1565.82529',
              'X-Amzn-Trace-Id': 'Root=1-62df473a-7cc923f823ecc5e179614909'}}

 In [3]:

```

scrapinghelper の  `request()` メソッドは  `requests.get()` のパラメタも受け取ることができますが、これとは別に `user_agent='random'` を与えると、自動的にランダムにユーザエージェントを置き換えてくれます。また、アクセスのときにデフォルトで2〜10秒間のランダムなスリープを入れながらアクセスをします。

# ハニーポットの罠に注意する
ハニーポット(honeypot)とは、ハッカーをおびき寄せ、情報を得ようとするハッキングの試みを検知するために設置されたシステムのことです。通常は、実際のシステムの動作を模倣するアプリケーションです。
スクレイパーを検知するためのハニーポットリンクの中には、 CSSのスタイルが  `display:none` であったり、ページの背景色に溶け込むように色を偽装しているものがあります。多くは、通常のユーザーには見えないリンクですが、ウェブスクレイパーには見えるようになっています。

リンクをたどるときは、常に次のことに注意を払うようにしましょう。

  -  `'nofollow'` の属性があるリンクは辿らない
  - リンクが適切に表示されているかをチェックする

この検知は、明らかに容易ではなく、適切に行うには相当量のプログラミング作業が必要です。そのため、この手法は、サーバー側、ボットやスクレイパー側のいずれにおいても、広く使用されるには至っていません。

# ウェブサイトのレイアウトが変更されていないか確認する
Webサイトの中には、ページによってレイアウト微妙に異なるものがあり、スクレイパーにとっては厄介な存在となります。

例えば、Web サイトによっては、1～20 ページには、あるレイアウトで表示し、残りのページでは別のレイアウトで表示するといったことがあります。こうしたサイトをスクレイピングするときは、単純な方法ではうまく処理できません。
XPathsやCSSセレクタを使用してデータをスクレイピングするようにします。サイトがそうなっていない場合は、
レイアウトがどのように異なるかをページソースで確認し、それらのページを異なる方法でスクレイピングする必要があります。

# ログインの背後にあるデータをスクレイピングしないようにする
ログインは基本的にWebページにアクセスするための許可を得ることです。ページがログインによって保護されている場合、スクレイパーはページを見るためのリクエストごとに何らかの情報またはクッキーを一緒に送信する必要があります。そのため、
ターゲットのWebサイトは、同じアドレスから来るリクエストを簡単に確認することができることになります。その結果、アカウント削除されたり、ブロックされる可能性が非常に高くなります。

しかし、認証が必要なページでも、人間のブラウザ操作を模倣することで、必要なデータを取得することはできます。


# CAPTCHA突破サービスを使用する
多くのWebサイトでは、Webスクレイピング対策が施されています。大規模にWebサイトをスクレイピングしていると、やがてWebサイトがブロックされて、Webページではなく、キャプチャーページが表示されることもあります。
CAPTCHA(キャプチャ)はCompletely Automated Public Turing test to tell Computers and Humans Apart 略称で、画像やテキストを利用してWebサイトにアクセスしているものが人間かどうかを識別する仕組みです。CAPTCHAを使用しているウェブサイトをスクレイピングする必要がある場合は、Captcha突破サービス(Captcha Solving Services)を利用する方が良いでしょう。Captcha突破サービスは比較的安価なので、大規模なスクレイピングを行う場合に有効です。

CAPTCHA突破サービスには次のようなものがあります。

  - [DeathByCaptcha ](https://www.deathbycaptcha.com/)
  - [2Captcha ](https://2captcha.com/)
  - [Anticaptcha ](https://anti-captcha.com/)
  - [EndCaptcha ](https://www.endcaptcha.com/)
  - [BypassCaptch ](http://bypasscaptcha.com/)
  - [CaptchaSniper ](https://www.captchasniper.com/)
  - [CaptchaTronix](http://www.captchatronix.com/)
  - [BestCaptchaSolver ](https://bestcaptchasolver.com/)
  - [AZCaptc ](https://azcaptcha.com/)
  - [ImageTyperz](http://www.imagetyperz.com/)
  - [AntiCaptcha ](https://anti-captcha.com/)

# ウェブサイトがブロックまたは禁止しているかどうかを調べる
サイトにアクセスして次のような兆候があらわれたときは、通常はブロックまたは禁止されているサインだと考えられます。

  - CAPTCHAページの表示
  - なコンテンツ配信の異常な遅延
  - HTTP 404、301、または 50x エラーの頻繁な応答

以下ののHTTPステータスコードが頻繁に表示される場合も、ブロックの兆候となります。

  - 301 Moved Temporarily: 一時的に移動されました
  - 401 Unauthorized: 認証されていません
  - 403 Forbidden: 禁止
  - 404 Not Found: 見つかりません
  - 408 Request Timeout: リクエストタイムアウト
  - 429 Too Many Requests: リクエストが多すぎる
  - 503 Service Unavailable: サービスが利用できません

408や503などが多発するような場合、アンチスクレイパーによるものではなく、単純にサ
ーバーがアクセス負荷に耐えられなくなっていることもあります。

# まとめ

ここで紹介していることは、あくまでも基本的なことだということを理解しておいてください。スクレイパーをブロックするための方法をWebサイト側の視点が考えてみることをおすすめします。



#Webスクレイピング


