mako:キャッシュ
=================
 ![](https://gyazo.com/4bdf2b5b1a1690f4ec26052263276df8.png)

## キャッシュ
 `<%page>` 、 `<%def>` 、または `<%block>` タグの `cache` 引数を使用して、任意のテンプレートまたはコンポーネントをキャッシュできます。

```
 <%page cached="True"/>

 テンプレートのテキスト
```

上記のテンプレートは、最初に実行された後、そのコンテンツをキャッシュ内に保存します。キャッシュはデフォルトでメモリ内にスコープされます。 その後、テンプレートの `Template.render()` メソッドを呼び出すと、コンテンツがキャッシュから直接返されます。 `Template` オブジェクト自体がスコープ外になると、対応するキャッシュはテンプレートとともにガベージコレクションされます。

キャッシングシステムでは、キャッシュバックエンドをインストールする必要があります。 これには、Beakerパッケージまたは `dogpile.cache` のいずれか、およびMako統合を特徴とするその他のサードパーティのキャッシュライブラリが含まれます。

デフォルトでは、キャッシングはBeakerを利用しようとします。  `dogpile.cache` を使用するには、`cache_impl`引数を設定する必要があります。

 `<%page>` タグで使用できることに加えて、キャッシングフラグとそのすべてのオプションを `<%def>` タグで使用することもできます。

```
 <%def name="mycomp" cached="True" cache_timeout="60">
     other text
 </%def>
```

同等に、無名または名前付きの `<%block>` タグを使用します。

```
 <%block cached="True" cache_timeout="60">
     other text
 </%block>
```

### キャッシュ引数
Makoには、すべての場合に使用できるタグで使用できる2つのキャッシュ引数があります。 使用可能な残りの引数は、バックエンドに固有です。

2つの一般的なタグの引数は次のとおりです。

-  `cache="True"` ： `<%page>` 、 `<%def>` 、または `<%block>` のキャッシュを有効にする
-  `cache_key` ：キャッシュ内のこのコンテンツを一意に識別するために使用される「キー」
通常、このキーは、呼び出し可能なレンダリングの名前に基づいて自動的に選択されます。
つまり、 `<%page>` で使用される場合は本体、`<%def>` を使用する場合はDefの名前、`<%block>`を使用する場合は明示的または内部的に生成された名前 。 `cache_key`引数を使用すると、固定値またはプログラムで生成された値を使用してキーをオーバーライドできます。

たとえば、呼び出し元のテンプレートのファイル名に基づいて、ページから継承するページをキャッシュするページは次のとおりです。

```
 <%page cached="True" cache_key="${self.filename}"/>

 ${next.body()}

 ## 残りのテンプレート
```

 `Template` または `TemplateLookup` では、次の引数を使用してキャッシュを構成できます。

-  `cache_enabled=False` ：テンプレートのレンダリング時にキャッシュ機能を無効になる。
デフォルトは `True` です。

```
 lookup = TemplateLookup(
                 directories='/path/to/templates',
                 cache_enabled = False
                 )
```

- `cache_impl` ：使用するキャッシュバックエンドの文字列名。これはデフォルトで`'"beaker"`に設定され、Beakerバックエンドが使用されることを示します。

-  `cache_args` ：キャッシュバックエンドによって消費されるキャッシュパラメータの辞書

## バックエンド固有のcache_引数
 `<%page>` 、`<%def>`、および`<%block>`タグは、プレフィックス`cache_`で始まる名前付き引数を受け入れます。次に、これらの引数はパッケージ化され、`cache_`プレフィックスを除いた基になるキャッシュ実装に渡されます。

理解される実際の引数は、バックエンドによって決定されます。

- Beakerキャッシュバックエンドの使用：Beakerが理解できる引数が含まれる
- dogpile.cacheバックエンドの使用：dogpile.cacheによって理解される引数が含まれる

### Beakerキャッシュバックエンドの使用
Beakerを使用する場合、新しい実装では、キャッシュ構成をテンプレートの外部で維持できるように、キャッシュ領域を使用する必要があります。これらの構成は、テンプレート自体の中で参照できる名前付きの「領域」の下にあります。

たとえば、2つのリージョンが必要だとします。 1つは、メモリベースの辞書にコンテンツを保存する短期領域( `"short_term"` )で、60秒後に期限切れになります。もう1つはMemcachedリージョンで、値は5分で期限切れになります。 `TemplateLookup` を構成するには、最初に `beaker.cache.CacheManager` へのハンドルを取得します。


```
 from beaker.cache import CacheManager

 manager = CacheManager(cache_regions={
     'short_term':{
         'type': 'memory',
         'expire': 60
     },
     'long_term':{
         'type': 'ext:memcached',
         'url': '127.0.0.1:11211',
         'expire': 300
     }
 })

 lookup = TemplateLookup(
                 directories=['/path/to/templates'],
                 module_directory='/path/to/modules',
                 cache_impl='beaker',
                 cache_args={
                     'manager':manager
                 }
         )
```

テンプレートは、 `cache_region` 引数を使用して、いずれかのリージョンのいずれかにデータをキャッシュすることを選択できます。
次の例は、 `<%page>` レベルで`short_term`を使用するものです。

```
 <%page cached="True" cache_region="short_term">

 ## ...
```

または、 `<%block>` レベルの `long_term`を使用した例。

```
 <%block name="header" cached="True" cache_region="long_term">
     other text
 </%block>
```

Beakerバックエンドはリージョンなしでも機能します。  `cache_args` 辞書に渡すことができるさまざまな引数があります。これらは、これらのセクションに固有の `<%page>` 、 `<%block>` 、および `<%def>` タグを介してテンプレートでも許可されます。指定された値は、`TemplateLookup`またはテンプレートレベルで指定された値を上書きします。

 `cache_timeout` を除いて、これらの引数は、テンプレート構成レベルにとどまるほうがよいでしょう。テンプレートタグで `cache_XYZ` として指定された各引数は、`cache_args` 辞書で `cache_` プレフィックスなしで指定されます。

-  `cache_timeout` ：キャッシュされたデータを無効にする秒数
このタイムアウト後、コンテンツは次の呼び出しで再生成されます。 cache_argsディクショナリでタイムアウトとして使用できます。
-  `cache_type` ：キャッシュのタイプ
 `'memory'` 、 `'file'` 、 `'dbm'` 、または `'ext:memcached'` （文字列 `'memcached'` は `dogpile.cache`  Makoプラグインでも受け入れられますが、Beaker自体では受け入れられないことに注意してください）。 `cache_args` ディクショナリのタイプとして使用できます。

-  `cache_url` ：用するmemcacheサーバー
memcachedにのみ使用されますが必須です。memcacheサーバーをの単一のIPアドレスもしくはセミコロン（ `;` )で区切られたIPアドレスのリスト。 `cache_args`辞書で`url`として利用できます。

-  `cache_dir` ：データファイルを保存するためのファイルシステムディレクトリ
キャッシュタイプが `'file'` 、`'dbm'` の場合に有効、このオプションが存在しない場合は、`module_directory`の値が使用されます。つまり、コンパイルされたテンプレートモジュールが保存されるディレクトリです。どちらのオプションも使用できない場合、例外が発生します。
 `cache_args` 辞書で `dir` として使用できます。

### dogpile.cacheバックエンドの使用
 `dogpile.cache` は、Beakerの新しい代替品です。近代化されたスリムなインターフェースを提供し、一般的にビーカーよりも使いやすいとされています。`dogpile.cache`には、独自のMakoキャッシュプラグインが含まれています。今時点ではまだ正式にリリースされていません。

### プログラムによるキャッシュアクセス
テンプレート、およびテンプレートから派生した名前空間には、そのテンプレートの `Cache` オブジェクトを返す `cache` というアクセサがあります。このオブジェクトは、基になる`CacheImpl`オブジェクトの上にあるファサードであり、任意の値を取得および配置する機能など、いくつかの非常に基本的な機能を提供します。

```
 <%
     local.cache.set("somekey", type="memory", "somevalue")
 %>
```

上記では、ローカル名前空間に関連付けられたキャッシュにアクセスし、キーをメモリキャッシュ内に配置します。

より一般的には、キャッシュオブジェクトは、キャッシュされたセクションをプログラムで無効にするために使用されます。

```
 template = lookup.get_template('/sometemplate.html')

 # テンプレートの「本体」を無効にする
 template.cache.invalidate_body()

 # 個々の定義を無効にする
 template.cache.invalidate_def('somedef')

 # 任意のキーを無効にする
 template.cache.invalidate('somekey')
```

 `Cache.impl` アトリビュートを使用して、`CacheImpl` 自体の特別なメソッドまたはアトリビュートにアクセスできます。

```
 template.cache.impl.do_something_special()
```

実装固有のメソッドを使用すると、後で別の種類の `CacheImpl` 実装に置き換えられないできないことに注意してください。

### キャッシュプラグイン
キャッシュで使用されるメカニズムは、 `CacheImpl` サブクラスを使用してプラグインできます。 このクラスは、MakoがキャッシングAPIを実装するために必要な基本的なメソッドを実装します。 Makoには、デフォルトの実装を提供する`BeakerCacheImpl`クラスが含まれています。 `CacheImpl`クラスは、Makoが`pkg_resources`エントリポイントを使用して取得し、`Template`または`TemplateLookup`の`cache_impl`引数として指定された名前を使用します。 このエントリポイントは、`mako.cache`という名前の`EntryPoint`グループの下にありインストールすることできます。 また、基本的に同じタスクを実行する便利なインストーラー`register_plugin()`を介して実行時にインストールすることもできます。

ローカル辞書キャッシュを実装するプラグインの例：

```
 from mako.cache import Cacheimpl, register_plugin

 class SimpleCacheImpl(CacheImpl):
     def __init__(self, cache):
         super(SimpleCacheImpl, self).__init__(cache)
         self._cache = {}

     def get_or_create(self, key, creation_function, **kw):
         if key in self._cache:
             return self._cache[key]
         else:
             self._cache[key] = value = creation_function()
             return value

     def set(self, key, value, **kwargs):
         self._cache[key] = value

     def get(self, key, **kwargs):
         return self._cache.get(key)

     def invalidate(self, key, **kwargs):
         self._cache.pop(key, None)

 # optional - register the class locally
 register_plugin("simple", __name__, "SimpleCacheImpl")
```

上記のプラグインをテンプレートで有効にすると、次のようになります。

```
 t = Template("mytemplate",
              file="mytemplate.html",
              cache_impl='simple')
```


### キャッシュプラグインを作成するためのガイドライン
 `CacheImpl` は、テンプレートごとに作成されます。クラスは、親テンプレートのデータのみが永続化されるか、キャッシュメソッドによって返されるようにする必要があります。実際のテンプレートは、`self.cache.template`アトリビュートを介して利用できます。本質的にテンプレートの一意のモジュール名である`self.cache.id`アトリビュートは、テンプレートに固有のキーの一意の名前空間を表すために使用するのに適した値です。

テンプレートは、暗黙的な方法で `CacheImpl.get_or_create()` メソッドのみを使用します。 `CacheImpl.set()`、`CacheImpl.get()`、および`CacheImpl.invalidate()`メソッドは、`Cache`オブジェクトの対応するメソッドへの直接のプログラムアクセスに応答する場合にのみ使用されます。

テンプレート自体がマルチスレッドで使用されている場合、 `CacheImpl` はマルチスレッド方式でアクセスされます。キャッシュの実装がスレッドセーフであることを確認するように注意する必要があります。

Beakerから派生した最小限のロックシステムであるDogpileのようなライブラリを使用すると、複数のスレッドおよびプロセス間で効果を最大化できるスレッドセーフな方法で `CacheImpl.get_or_create()` メソッドを実装できます。 `CacheImpl.get_or_create()`は、テンプレートで使用される主要なメソッドです。

 `**kw` に渡されるすべての引数は、`<%def>`、`<%block>`、または`<%page>`タグ内のパラメーターから直接取得され、引数`cache_timeout`を除いて、文字列として`"cache_"`プレフィックスが差し引かれます。これは、値が整数に変換された名前タイムアウトとしてプラグインに渡されます。 `Template`または`TemplateLookup`の`cache_args`に存在する引数は直接渡されますが、最も具体的なテンプレートタグに存在する引数に置き換えられます。

テンプレートがモジュールファイルを配置するディレクトリは、アクセサ `self.cache.template.module_directory` を使用して取得できます。このディレクトリは、キャッシュ関連の作業ファイルを`_my_cache_work`などのプレフィックスの下に配置して、生成されたモジュールと名前が競合しないようにするのに適した場所です。






