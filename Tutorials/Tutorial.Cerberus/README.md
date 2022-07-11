データ検証ライブラリCerberusを使ってみよう
=================
![](https://github.com/iisaka51/PythonOsaka/raw/main/Tutorials/Tutorial.Cerberus/images/cerberus_logo.png)
## Cerberus について
Cerberusは、Pythonで実装されたの軽量で拡張性のあるデータ検証ライブラリです。Cerberusは、パワフルでありながらシンプルで軽量なデータ検証機能を提供しています。また、カスタム検証を可能にする拡張性の高い設計になっています。

>ケルベロス
> Cerberus はラテン語表記で、Kérberos はギリシャ語表記です。
> ラテン語読みはケルベルス、英語読みはサーベラス。ギリシャ神話に登場する冥府の入り口を守護する番犬。

この資料では、ソースコードの例示と実行を、Hands-On をすることを考えて IPython を使っています。


```
 % ipython

 Type 'copyright', 'credits' or 'license' for more information
 IPython 7.28.0 -- An enhanced Interactive Python. Type '?' for help.

 In [1]:
```

- IPython の　 `%load` コマンドでソースコードを読み込んで実行させていますす。
- 実行した結果と期待する出力を assert 文を使って記述しています。
- 実行してみて欲しいコードは末尾部分にコメントで記述しています。
- このときにキー入力がすくなくなるような変数にしています。


サンプルコードは [github ](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorial.Cerberus) で公開していますので、自習などでご利用ください。


## インストール

 bash
```
 $ pip install cerberus
```

cerberus には依存関係のある外部モジュールはありません。

## 基本的な使用方法

細かなことは後回しにして、まずどんな具合にデータ検証を行うのかを見てみましょう。
まず。検証スキーマを定義し、それを `Validator` クラスに渡してインスタンスを生成します。
検証したいデータを `Validator` クラスの `validate()` メソッドに渡すとブール値が返ってきます。


```
 In [2]: # %load 01_validate.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'}}
    ...: document = {'name': 'Jack Bauer'}
    ...:
    ...: v = Validator(schema)
    ...: check = v.validate(document)
    ...: assert check == True
    ...:
    ...: # v
    ...:

 In [3]: v
 Out[3]: <cerberus.validator.Validator at 0x10707ee50>

```

 `validate()` メソッドにデータとスキーマを与えて検証することもできます。


```
 In [2]: # %load 02_validate_alternate.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'}}
    ...: document = {'name': 'Jack Bauer'}
    ...:
    ...: v = Validator()
    ...: check = v.validate(document, schema)
    ...: assert check == True
    ...:
    ...: # v.types
    ...:

 In [3]:

```


これは、インスタンスの使用期間中にスキーマが変更される場合に便利です。

検証スキーマの詳細については後述しますが、データのキーがどのようなルールに従うのかを定義した辞書です。ルールに指定できる型は `types` プロパティーで参照できるのが使用できます。


```
 In [3]: v.types
 Out[3]:
 ('binary',
  'boolean',
  'container',
  'date',
  'datetime',
  'dict',
  'float',
  'integer',
  'list',
  'number',
  'set',
  'string')

 In [4]:
```

他の検証ツールとは異なり、Cerberusは検証を行って問題があるときに停止したり、例外を発生させたりしません。ドキュメント全体が常に処理され、検証に失敗した場合は  `False` が返されます。その後、 `errors` プロパティにアクセスして、エラーの原因のリストを取得することができます。
検証に問題がなく成功したときは `True` が返され、 `errors` は空の辞書がセットされます。



```
 In [2]: # %load 03_validate_error.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'}}
    ...: document = {'name': 12345 }
    ...:
    ...: v = Validator()
    ...: check = v.validate(document, schema)
    ...:
    ...: assert check == False
    ...: assert v.errors == {'name': ['must be of string type']}
    ...:

 In [3]:
```

スキーマで定義するルールで制限を与えることもできます。これも詳しくは後述します。
次の例では、 `age` の値は 10 以上でないと検証エラーとなります。


```
 In [2]: # %load 04_validate_complex.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: document = {'name': 'Little Joe', 'age': 5}
    ...:
    ...: v = Validator()
    ...: c  = (v.validate(document, schema), v.errors)
    ...:
    ...: assert c[0] == False
    ...: assert c[1] == {'age': ['min value is 10']}
    ...:
    ...: # v.validation_rules
    ...:

 In [3]:

```


ルールは  `validation_rules` プロパティーのものが使用できます。詳しくは後述します。


```
 In [3]: v.validation_rules
 Out[3]:
 {'allof': {'type': 'list', 'logical': 'allof'},
  'allow_unknown': {'oneof': [{'type': 'boolean'},
    {'type': ['dict', 'string'], 'check_with': 'bulk_schema'}]},
  'allowed': {'type': 'container'},
  'anyof': {'type': 'list', 'logical': 'anyof'},
  'check_with': {'oneof': [{'type': 'callable'},
    {'type': 'list',
     'schema': {'oneof': [{'type': 'callable'},
       {'type': 'string', 'allowed': ()}]}},
    {'type': 'string', 'allowed': ()}]},
  'contains': {'empty': False},
  'dependencies': {'type': ('dict', 'hashable', 'list'),
   'check_with': 'dependencies'},
  'empty': {'type': 'boolean'},
  'excludes': {'type': ('hashable', 'list'), 'schema': {'type': 'hashable'}},
  'forbidden': {'type': 'list'},
  'items': {'type': 'list', 'check_with': 'items'},
  'keysrules': {'type': ['dict', 'string'],
   'check_with': 'bulk_schema',
   'forbidden': ['rename', 'rename_handler']},
  'max': {'nullable': False},
  'maxlength': {'type': 'integer'},
  'meta': {},
  'min': {'nullable': False},
  'minlength': {'type': 'integer'},
  'noneof': {'type': 'list', 'logical': 'noneof'},
  'nullable': {'type': 'boolean'},
  'oneof': {'type': 'list', 'logical': 'oneof'},
  'readonly': {'type': 'boolean'},
  'regex': {'type': 'string'},
  'require_all': {'type': 'boolean'},
  'required': {'type': 'boolean'},
  'schema': {'type': ['dict', 'string'],
   'anyof': [{'check_with': 'schema'}, {'check_with': 'bulk_schema'}]},
  'type': {'type': ['string', 'list'], 'check_with': 'type'},
  'valuesrules': {'type': ['dict', 'string'],
   'check_with': 'bulk_schema',
   'forbidden': ['rename', 'rename_handler']}}

```


ドキュメントがマッピングでない場合には  `DocumentError` が発生します。


```
 In [2]: # %load 05_document_error.py
    ...: from cerberus import Validator, DocumentError
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: document = {'name': 'Little Joe', 'age': 5}
    ...:
    ...: v = Validator()
    ...: doc = f'{document}'
    ...:
    ...: try:
    ...:     c  = (v.validate(doc, schema), v.errors)
    ...: except DocumentError as e:
    ...:     print(e)
    ...:
 '{'name': 'Little Joe', 'age': 5}' is not a document, must be a dict

 In [3]:
```


 `Validator` クラスとそのインスタンスは呼び出し可能(Callable)で、次のような短縮構文が可能です。


```
 In [2]: # %load 06_validate_callable.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: document = {'name': 'David Coverdale', 'age': 70}
    ...:
    ...: v = Validator(schema)
    ...: c = v(document)
    ...: assert c == True
    ...:

 In [3]:

```


スキーマで定義したキーがデータになくてもエラーにはなりませんが。スキーマーで定義していないキーが存在するとエラーになります。


```
 In [2]: # %load 07_validate_keys.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: doc1 = {'name': 'David Coverdale'}
    ...: doc2 = {'name': 'David Coverdale', 'country': 'USA'}
    ...:
    ...: v = Validator(schema)
    ...: c1 = (v.validate(doc1), v.errors)
    ...: assert c1[0] == True
    ...: assert c1[1] == {}
    ...:
    ...: c2 = (v.validate(doc2), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'country': ['unknown field']}
    ...:

 In [3]:

```


## 未知なキーを許可する
デフォルトでは、スキーマで定義されたキーのみが許可されます。 `allow_unknown` プロパティを `True` にセットすると、
これをスキーマで定義されていないキーも受け入れるようになります。


```
 In [2]: # %load 08_unknown_key.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: document = {'name': 'David Coverdale', 'country': 'USA'}
    ...:
    ...: v = Validator(schema)
    ...: assert v.allow_unknown == False
    ...:
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'country': ['unknown field']}
    ...:
    ...: v.allow_unknown = True
    ...:
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == True
    ...:

 In [3]:
```

また、 `allow_unknown` に検証スキーマに設定すると、未知のフィールドはそのスキーマに対して検証されます。


```
 In [2]: # %load 09_unknown_validate.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: v.schema = {}
    ...: v.allow_unknown = {'type': 'string'}
    ...: document = {'an_unknown_field': 'john'}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'an_unknown_field': 1}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'an_unknown_field': ['must be of string type']}
    ...:

 In [3]:
```

 `allow_unknown` プロパティはいつでも元に戻せます。


```
 In [2]: # %load 10_allow_unknown_reset.py
    ...: from cerberus import Validator
    ...:
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: document = {'name': 'David Coverdale', 'country': 'USA'}
    ...:
    ...: v = Validator(schema)
    ...: assert v.allow_unknown == False
    ...:
    ...: v.allow_unknown = True
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: v.allow_unknown = False
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'country': ['unknown field']}
    ...:

 In [3]:

```

 `allow_unknown` をルールとして設定することで、スキーマルールと照合される入れ子のマッピングのバリデータを設定することもできます。


```
 In [2]: # %load 11_allow_unknown_rule.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator()
    ...: assert v.allow_unknown == False
    ...:
    ...: schema = {
    ...:   'name': {'type': 'string'},
    ...:   'a_dict': {
    ...:     'type': 'dict',
    ...:     'allow_unknown': True,  # 注目：この定義でプロパティを上書きする
    ...:     'schema': {
    ...:       'address': {'type': 'string'}
    ...:     }
    ...:   }
    ...: }
    ...:
    ...: document = {'name': 'john',
    ...:             'a_dict': {'an_unknown_field': 'is allowed'}}
    ...: c1 = (v.validate(document, schema), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'name': 'john',
    ...:             'an_unknown_field': 'is not allowed',
    ...:             'a_dict': {'an_unknown_field': 'is allowed'}}
    ...: c2 = (v.validate(document, schema), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'an_unknown_field': ['unknown field']}
    ...:

 In [3]:
```

 `c1` でのバリデーションでは、スキーマで  `a_dict` キーのデータには　 `allow_unknown` が `True` に上書きされるのでエラーにはなりませんが、 `c2` では、スキーマーの `allow_unknown` プロパティは　 `False` のままなので、親ドキュメントの未知なキーはエラになります。


## すべてを要求するスキーマ
デフォルトでは、スキーマで定義されたすべてのキーは必須ではありません。しかし、バリデータの初期化時に  `require_all` を True に設定するか、 `require_all` プロパティを後から `True` に変更すると、スキーマーで定義されているすべてのキーのペアを要求することができます。  `require_all` をルールとして設定し、スキーマルールと照合するサブドキュメント用のバリデータを設定することもできます。



```
 In [2]: # %load 12_require_all.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'min': 10}}
    ...: document = {'name': 'David Coverdale'}
    ...:
    ...: v = Validator(schema)
    ...: assert v.require_all == False
    ...:
    ...: c1 = (v(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: v.require_all = True
    ...:
    ...: c2 = (v(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'age': ['required field']}
    ...:

 In [3]:
```



```
 In [2]: # %load 13_require_all_schema.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator()
    ...: assert v.require_all == False
    ...:
    ...: schema = {
    ...:   'name': {'type': 'string'},
    ...:   'a_dict': {
    ...:     'type': 'dict',
    ...:     'require_all': True,  # 注目：この定義でプロパティを上書きする
    ...:     'schema': {
    ...:       'address': {'type': 'string'}
    ...:     }
    ...:   }
    ...: }
    ...:
    ...: document = {'name': 'john', 'a_dict': {}}
    ...: c1 = (v.validate(document, schema), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'a_dict': [{'address': ['required field']}]}
    ...:
    ...: document = {'a_dict': {'address': 'foobar'}}
    ...: c2 = (v.validate(document, schema), v.errors)
    ...: assert c2[0] == True
    ...:

 In [3]:
```


## 処理済ドキュメントの取得
正規化(Normalize)と強制(coerce)は元のドキュメントのコピーに対して実行され、結果のドキュメントは  `document` プロパティで取得できます。


```
 In [2]: # %load 14_doc_property.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator()
    ...: v.schema = {'amount': {'type': 'integer', 'coerce': int}}
    ...:
    ...: document = {'amount': 1}
    ...: c = v.validate(document)
    ...: assert c == True
    ...: assert v.document == document
    ...:

 In [3]:
```

 `Validator` インスタンスには、 `document` プロパティーのほかに、 ドキュメントを処理したり処理結果を取得したりするための省略可能なメソッドがあります。

### validated() メソッド
ラッパーメソッド  `validated()` があり、検証済みの文書を返します。ドキュメントが認証されなかった場合は  `None` を返します。ただし、キーワード引数  `always_return_document` を  `True` に設定してこのメソッドを呼び出した場合はこの限りではありません。次のような処理をしたいときに便利です。


```
 In [2]: # %load 15_validated.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string'},
    ...:            'age': {'type': 'integer', 'max': 45 }}
    ...:
    ...: documents = [
    ...:   { 'name': 'David', 'age': 70 },
    ...:   { 'name': 'Brian', 'age': 75 },
    ...:   { 'name': 'Roger', 'age': 75 },
    ...:   { 'name': 'Jack', 'age': 51 },
    ...:   { 'name': 'Anthony', 'age': 29 },
    ...:   { 'name': 'Chloe', 'age': 28 },
    ...: ]
    ...:
    ...: v = Validator(schema)
    ...: valid_docs = [x for x in [v.validated(y) for y in documents]
    ...:                     if x is not None]
    ...:
    ...: print(valid_docs)
    ...:
 [{'name': 'Anthony', 'age': 29}, {'name': 'Chloe', 'age': 28}]

 In [3]:
```

強制(coerce)させる呼び出し可能(Callable)オブジェクトまたはメソッドが例外を発生させた場合、その例外はキャッチされ、検証は失敗することに注意してください。

## normalized ()メソッド
 `normalized()` メソッドは、検証を行わずにドキュメントの正規化されたコピーを返します。


```
 In [2]: # %load 16_normalized.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'amount': {'coerce': int}}
    ...: document = {'model': 'consumerism', 'amount': '1'}
    ...:
    ...: v = Validator()
    ...: normalized_document = v.normalized(document, schema)
    ...: assert normalized_document == {'model': 'consumerism', 'amount': 1}
    ...: assert type(normalized_document['amount']) == int
    ...:

 In [3]:
```


## 警告(Warnings)
非推奨事項やトラブルの原因となりそうなものなどの警告(warning)は、Python標準ライブラリのwarningsモジュールを通じて発行されます。logging モジュール  `logging.captureWarnings()` を使って、これらの警告をキャッチするように設定することができます。


## 検証スキーマ
検証スキーマとはマッピングのことで、通常は辞書になります。スキーマのキーは、ターゲット辞書で許可されるキーです。スキーマの値は、対応するターゲットの値と一致しなければならないルールを表します。


```
 In [2]: # %load 20_schema.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string', 'maxlength': 10}}
    ...:
    ...: documents = [
    ...:    {'name': 'Jack Bauer'},
    ...:    {'name': 'David Coverdale'},
    ...:    {'name': 77},
    ...: ]
    ...:
    ...: v = Validator(schema)
    ...:
    ...: valid_docs = [x for x in [v.validated(y) for y in documents]
    ...:                  if x is not None]
    ...:
    ...: c1 = (v.validate(documents[0]), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: c2 = (v.validate(documents[1]), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'name': ['max length is 10']}
    ...:
    ...: c3 = (v.validate(documents[2]), v.errors)
    ...: assert c3[0] == False
    ...: assert c3[1] == {'name': ['must be of string type']}
    ...:
    ...: print(f'Valid_docs: {valid_docs}')
    ...:
 Valid_docs: [{'name': 'Jack Bauer'}]

 In [3]:
```


この例では、 `name` という1つのキーだけを持つターゲット辞書を定義しています。 `{name': 'Jack Bauer'}` のようなものは検証エラーにはなりませんが、 `{'name': 'David Coverdale'}` や `{'name': 77}` のようなものは検証エラーになります。

デフォルトでは、ドキュメントのすべてのキーはオプションで省略可能です。ただし、個々のフィールドに対してルール  `required` を  `True` に設定したり、 `Validator` インスタンスの `require_all` プロパティ を  `True` に設定して、ドキュメントにすべてのスキーマ定義のフィールドが存在していなければ検証エラーとすることもできます。設定に方法の詳細については後述します。


### レジストリ
cerberus モジュールの名前空間には 2 つのデフォルトレジストリがあります。ここにスキーマやルールセットの定義を保存し、検証スキーマで参照することができます。さらに、より多くのレジストリオブジェクトをインスタンス化し、  `Validator` クラスの  `rules_set_registry` や  `schema_registry` にバインドすることができます。初期化時にこれらをキーワード引数として設定することもできます。

レジストリの使用は、次のような場合に特に有効です。

- スキーマが自分自身への参照を含む場合 (スキーマの再帰)
- スキーマには再利用される部分が多く、シリアル化されていることが望ましいとき。


```
 In [2]: # %load 21_schema_registry.py
    ...: from cerberus import schema_registry, Validator
    ...:
    ...: schema_registry.add('non-system user',
    ...:                     {'uid': {'min': 1000, 'max': 0xffff}})
    ...:
    ...: schema = {'sender': {'schema': 'non-system user',
    ...:                      'allow_unknown': True},
    ...:           'receiver': {'schema': 'non-system user',
    ...:                        'allow_unknown': True}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'sender': {'uid': 0}}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'sender': [{'uid': ['min value is 1000']}]}
    ...:
    ...: document = {'sender': {'uid': 1000}}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == True
    ...:
    ...: document = {'sender': {'uid': 1001}}
    ...: c3 = (v.validate(document), v.errors)
    ...: assert c3[0] == True
    ...:

 In [3]:
```


```
 In [2]: # %load 22_rules_set_registry.py
    ...: from cerberus import rules_set_registry, Validator
    ...:
    ...: rules_set_registry.extend((('boolean', {'type': 'boolean'}),
    ...:                            ('booleans', {'valuesrules': 'boolean'})))
    ...: schema = {'foo': 'booleans'}
    ...:
    ...: v = Validator(schema)
    ...: r = v.rules['valuesrules']
    ...:
    ...: c = v.validate({'foo': 1})
    ...: assert c == True
    ...:
    ...: c = v.validate({'foo': True})
    ...: assert c == True
    ...:
    ...: c = v.validate({'foo': {'enable': True}})
    ...: assert c == True
    ...:
    ...: c = v.validate({'foo': {'name': 'Jack'}})
    ...: assert c == False
    ...: assert v.errors == {'foo': [{'name': ['must be of boolean type']}]}
    ...:
    ...: # r
    ...:

 In [3]: r
 Out[3]:
 {'type': ['dict', 'string'],
  'check_with': 'bulk_schema',
  'forbidden': ['rename', 'rename_handler']}

 In [4]:
```

ルール `valuesrules` は全ての値が指定したルールに従うことを制約するものです（詳しくは後述します）
この例では、値には辞書か文字列を与えることができ、値の型はブール値となっていれば検証エラーにはなりません。

### 検証(バリデーション)
 `Validator` クラスに渡されたときや、ドキュメントのフィールドに新しいルールが設定されたときに、バリデーションスキーマ自体が検証されます。無効な検証スキーマに遭遇した場合は SchemaError が発生します。
ただし、そのレベル以下のすべての変更や、レジストリ内の使用済みの定義が変更された場合には、検証がトリガーされないことに注意してください。そのため、検証をトリガーして例外をキャッチすることができます。


```
 In [2]: # %load 23_schema_validation.py
    ...: from cerberus import Validator, SchemaError
    ...:
    ...: schema = {'foo': {'allowed': []}}
    ...: v = Validator(schema)
    ...:
    ...:
    ...: try:
    ...:     v.schema['foo'] = {'allowed': 1}
    ...: except SchemaError as e:
    ...:     print(f'1st: {e}')
    ...:
    ...: v.schema['foo']['allowed'] = 'strings are no valid constraint for allowe
    ...: d'
    ...:
    ...: try:
    ...:     v.schema.validate()
    ...: except SchemaError as e:
    ...:     print(f'2nd: {e}')
    ...:
 1st: {'foo': [{'allowed': ['must be of container type']}]}
 2nd: {'foo': [{'allowed': ['must be of container type']}]}

 In [3]:
```

### シリアル化
cerberus のスキーマは、 `dict` 、 `list` 、 `str` などの純粋なPythonの型で構築されます。ユーザーが定義した検証ルールも、文字列としての名前でスキーマ内で呼び出されます。この定義を文字列で行えるという設計の便利な副次的効果は、スキーマをPyYAMLなどの様々な方法で定義できることです。


```
 In [2]: # %load 24_serialization.py
    ...: import yaml
    ...: from cerberus import Validator
    ...:
    ...: schema_text = '''
    ...: name:
    ...:   type: string
    ...: age:
    ...:   type: integer
    ...:   min: 10
    ...: '''
    ...:
    ...: schema = yaml.load(schema_text, Loader=yaml.SafeLoader)
    ...: document = {'name': 'Little Joe', 'age': 5}
    ...:
    ...: v = Validator(schema)
    ...: c = (v.validate(document), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'age': ['min value is 10']}
    ...:

 In [3]:
```

もちろんYAMLに限定されているわけではなく、JSONなどの好きなシリアライザを使うことができます。ネストされた `dict` を生成できるデコーダがあればよいので、それらを使ってスキーマを定義することができます。

レジストリの入力とダンプには、 `extend()` と  `all()` を使います。

## 検証ルール
 `Validator` インスタンスの  `validation_rules` プロパティーを参照すると検証ルールを知ることができます。
ここでは、そらについて説明してゆくことにします。

### allow_unknown
このルールは、サブドキュメントを検証するための `Validator` インスタンスの `allow_unknown` プロパティを設定することで、マッピングの検証時にスキーマルールと一緒に使用することができます。このルールは、 `purge_unknown` （詳しくは後述します）よりも優先されます。

### allowed
このルールは、許容値の[collections.abc ](https://docs.python.org/ja/3/library/collections.abc.html#module-collections.abc) のContainerを受け取ります。対象の値が許容値に含まれる場合、その値を検証します。ターゲットの値が反復可能である場合、そのすべてのメンバが許容値に含まれていなければなりません。


```
 In [2]: # %load 30_allowed.py
    ...: from cerberus import Validator
    ...:
    ...: schema_list = {'role': {'type': 'list',
    ...:                         'allowed': ['agent', 'client', 'supplier']}}
    ...: schema_string = {'role': {'type': 'string',
    ...:                           'allowed': ['agent', 'client', 'supplier']}}
    ...: schema_integer = {'a_restricted_integer': {'type': 'integer',
    ...:                                            'allowed': [-1, 0, 1]}}
    ...: v = Validator()
    ...:
    ...: v.schema = schema_list
    ...: c1 = (v.validate({'role': ['agent', 'supplier']}), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: c2 = (v.validate({'role': ['intern']}), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'role': ["unallowed values ('intern',)"]}
    ...:
    ...: v.schema = schema_string
    ...: c3 = (v.validate({'role': 'supplier'}), v.errors)
    ...: assert c3[0] == True
    ...:
    ...: c4 = (v.validate({'role': 'intern'}), v.errors)
    ...: assert c4[0] == False
    ...: assert c4[1] == {'role': ['unallowed value intern']}
    ...:
    ...: v.schema = schema_integer
    ...: c5 = (v.validate({'a_restricted_integer': -1}), v.errors)
    ...: assert c5[0] == True
    ...:
    ...: c6 = (v.validate({'a_restricted_integer': 2}), v.errors)
    ...: assert c6[0] == False
    ...: assert c6[1] == {'a_restricted_integer': ['unallowed value 2']}
    ...:

 In [3]:
```

### allof
提供された制約のすべてがそのフィールドを有効にするかどうかを検証します。詳細は *of-rules を参照してください。

### anyof
提供された制約条件のいずれかがそのフィールドを有効にするかどうかを検証します。詳細は *of-rules をご覧ください。

### check_with
関数またはメソッドを呼び出して、フィールドの値を検証します。
この関数は次のスニペットのように実装しなければなりません。


```
 def functionnname(field, value, error):
     if value is invalid:
         error(field, 'error message')

```

error 引数は、呼び出したバリデータの _error メソッドを指します。エラーを送信する方法については、 「Cerberusの拡張」を参照してください。

ここでは、整数が奇数かどうかをテストする例を示します。


```
 def oddity(field, value, error):
     if not value & 1:
         error(field, "Must be an odd number")
```

次のようにしてデータを検証することができます。


 pytohn
```
 In [2]: # %load 40_check_with.py
    ...: from cerberus import Validator
    ...:
    ...: def oddity(field, value, error):
    ...:     if not value & 1:
    ...:         error(field, "Must be an odd number")
    ...:
    ...: schema = {'amount': {'check_with': oddity}}
    ...: v = Validator(schema)
    ...:
    ...: c1 = (v.validate({'amount': 10}), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'amount': ['Must be an odd number']}
    ...:
    ...: c2 = (v.validate({'amount': 9}), v.errors)
    ...: assert c2[0] == True
    ...:

 In [3]:
```

ルールの制約条件が文字列の場合、  `Validator` のインスタンスには、その名前が  `_check_with_` で始まるメソッドを持つ必要があります。上記の関数ベースの例に相当するものとしては、「check_withルールで参照できるメソッド」を参照してください。

制約条件は、シーケンスにすることで連続して呼び出されるようにすることもできます。


```
 schema = {'field': {'check_with': (oddity, 'prime number')}}

```

### contains
このルールは、コンテナオブジェクトに定義されたすべてのアイテムが含まれているかどうかを検証します。


```
 In [2]: # %load 41_contains.py
    ...: from cerberus import Validator
    ...:
    ...: document = {'states': ['peace', 'love', 'inity']}
    ...: schema = {'states': {'contains': 'peace'}}
    ...:
    ...: v = Validator()
    ...:
    ...: c1 = (v.validate(document, schema), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: schema = {'states': {'contains': 'greed'}}
    ...: c2 = (v.validate(document, schema), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'states': ["missing members {'greed'}"]}
    ...:
    ...: schema = {'states': {'contains': ['love', 'inity']}}
    ...: c3 = (v.validate(document, schema), v.errors)
    ...: assert c3[0] == True
    ...:
    ...: schema = {'states': {'contains': ['love', 'respect']}}
    ...: c4 = (v.validate(document, schema), v.errors)
    ...: assert c4[0] == False
    ...: assert c4[1] == {'states': ["missing members {'respect'}"]}
    ...:

 In [3]:
```


### dependencies
このルールでは、定義されたフィールドがドキュメントに存在する場合、ドキュメントで必要とされる単一のフィールド名、一連のフィールド名、またはフィールド名と一連の許容値のマッピングを定義することができます。


```
 In [2]: # %load 42_dependencies.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'field1': {'required': False},
    ...:           'field2': {'required': False,
    ...:                      'dependencies': 'field1'}}
    ...:
    ...: v = Validator()
    ...:
    ...: document = {'field1': 7}
    ...: c1 = v.validate(document, schema)
    ...: assert c1 == True
    ...:
    ...: document = {'field2': 7}
    ...: c2 = v.validate(document, schema)
    ...: assert c2 == False
    ...: assert v.errors == {'field2': ["field 'field1' is required"]}
    ...:

 In [3]:
```

複数のフィールド名が依存関係として定義されている場合、対象となるフィールドが検証されるためには、これらがすべて存在する必要があります。


```
 In [2]: # %load 43_dependencies_multiple.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'field1': {'required': False},
    ...:           'field2': {'required': False},
    ...:           'field3': {'required': False,
    ...:                      'dependencies': ['field1', 'field2']}}
    ...:
    ...: v = Validator()
    ...:
    ...: document = {'field1': 7, 'field2': 11, 'field3': 13}
    ...: c = v.validate(document, schema)
    ...: assert c == True
    ...:
    ...: document = {'field2': 11, 'field3': 13}
    ...: c = v.validate(document, schema)
    ...: assert c == False
    ...: assert v.errors == {'field3': ["field 'field1' is required"]}
    ...:

 In [3]:
```

マッピングが提供されると、すべての依存関係が存在するだけでなく、それらの許容値のいずれかがマッチしなければなりません。



```
 In [2]: # %load 44_dependencies_with_mapping.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'field1': {'required': False},
    ...:           'field2': {'required': True,
    ...:                      'dependencies': {'field1': ['one', 'two']}}}
    ...:
    ...: v = Validator()
    ...:
    ...: document = {'field1': 'one', 'field2': 7}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == True
    ...:
    ...: document = {'field1': 'three', 'field2': 7}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'field2':
    ...:                ["depends on these values: {'field1': ['one', 'two']}"]}
    ...:
    ...: # dependencies のリストを使うのと同じ
    ...: document = {'field2': 7}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'field2':
    ...:                 ["depends on these values: {'field1': ['one', 'two']}"]}
    ...:
    ...:
    ...: # 単一のdependencies を渡すこともできます。
    ...: schema = {'field1': {'required': False},
    ...:           'field2': {'dependencies': {'field1': 'one'}}}
    ...: document = {'field1': 'one', 'field2': 7}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == True
    ...:
    ...: document = {'field1': 'two', 'field2': 7}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'field2':
    ...:                 ["depends on these values: {'field1': 'one'}"]}
    ...:
    ...:

 In [3]:
```

サブドキュメントのフィールドの依存関係をドット表記で宣言することもサポートされています。


```
 In [2]: # %load 45_dependencies_dot_notation.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {
    ...:     'test_field': {'dependencies': ['a_dict.foo', 'a_dict.bar']},
    ...:     'a_dict': {
    ...:         'type': 'dict',
    ...:         'schema': {
    ...:             'foo': {'type': 'string'},
    ...:             'bar': {'type': 'string'}
    ...:         }
    ...:     }
    ...: }
    ...:
    ...: document = {'test_field': 'foobar',
    ...:             'a_dict': {'foo': 'foo'}}
    ...:
    ...: v = Validator()
    ...:
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'test_field': ["field 'a_dict.bar' is required"]}
    ...:

 In [3]:
```

サブドキュメントが処理されると、問題のあるフィールドの検索はそのドキュメントのレベルで始まります。処理されたドキュメントをルートレベルとして扱うためには、宣言はキャレット記号( ` ^ ` で始まる必要があります。2 つのキャレット ( `^^` ) ので始まっていると、特別な意味を持たない１文字のキャレット( `^` ) として解釈されます。

python
```
 In [2]: # %load 46_dependencies_carets.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {
    ...:     'test_field': {},
    ...:     'a_dict': {
    ...:         'type': 'dict',
    ...:         'schema': {
    ...:             'foo': {'type': 'string'},
    ...:             'bar': {'type': 'string',
    ...:                     'dependencies': '^test_field'}
    ...:         }
    ...:     }
    ...: }
    ...:
    ...: v = Validator()
    ...: document = {'a_dict': {'bar': 'bar'}}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'a_dict':
    ...:                 [{'bar': ["field '^test_field' is required"]}]}
    ...:

 In [3]:
```

備考
ドット記法のセマンティクスを拡張したい場合は、 `_lookup_field()` メソッドをオーバーライドしてください。

注意点
このルールの評価では、 `require` ルールで定義された制約は考慮されません。

### empty
このルールが `False` として制約されている場合、反復可能な値が空であれば検証に失敗します。デフォルトでは、フィールドが空であるかどうかはチェックされないため、ルールが定義されていない場合は許可されます。しかし、制約を `True` で定義すると、値が空であるとみなされた場合、そのフィールドに定義されている可能性のあるルール `allowed` 、 `fobidden` 、 `items` 、 `minlength` 、 `maxlength` 、 `regex` 、 `validator` をスキップします。（これ重要）


```
 In [2]: # %load 47_empty.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'type': 'string', 'empty': False}}
    ...: document = {'name': ''}
    ...:
    ...: v = Validator()
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'name': ['empty values not allowed']}
    ...:

 In [3]:
```


### excludes
このルールは除外するフィールドを宣言することができます。


```
 In [2]: # %load 48_excludes.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator()
    ...: schema = {'this_field': {'type': 'dict',
    ...:                          'excludes': 'that_field'},
    ...:           'that_field': {'type': 'dict',
    ...:                          'excludes': 'this_field'}}
    ...:
    ...: c1 = (v.validate({'this_field': {}, 'that_field': {}}, schema), v.errors
    ...: )
    ...: assert c1[0] == False
    ...: assert c1[1] == {'that_field':
    ...:                 ["'this_field' must not be present with 'that_field'"],
    ...:                 'this_field':
    ...:                 ["'that_field' must not be present with 'this_field'"]}
    ...:
    ...: c2 = v.validate({'this_field': {}}, schema)
    ...: assert c2 == True
    ...:
    ...: c3 = v.validate({'that_field': {}}, schema)
    ...: assert c3 == True
    ...:
    ...: c4 = v.validate({}, schema)
    ...: assert c4 == True
    ...:

 In [3]:
```

両方のフィールドを `required` とし、排他的論理和を構築することができます。


```
 In [2]: # %load 49_excludes_exclusive_or.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'this_field': {'type': 'dict',
    ...:                          'excludes': 'that_field',
    ...:                          'required': True},
    ...:           'that_field': {'type': 'dict',
    ...:                          'excludes': 'this_field',
    ...:                          'required': True}
    ...:         }
    ...:
    ...: v = Validator(schema)
    ...: document = {'this_field': {}, 'that_field': {}}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'that_field':
    ...:                  ["'this_field' must not be present with 'that_field'"],
    ...:
    ...:                  'this_field':
    ...:                  ["'that_field' must not be present with 'this_field'"]}
    ...:
    ...:
    ...: document = {'this_field': {}}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == True
    ...:
    ...: document = {'that_field': {}}
    ...: c3 = (v.validate(document), v.errors)
    ...: assert c3[0] == True
    ...:
    ...: document = {}
    ...: c4 = (v.validate(document), v.errors)
    ...: assert c4[0] == False
    ...: assert c4[1] == {'that_field': ['required field'],
    ...:                  'this_field': ['required field']}
    ...:

 In [3]:
```

フィールドをリストで与えて、複数のフィールドを除外することできます。


```
 In [2]: # %load 50_excludes_multiple_fields.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'this_field': {'type': 'dict',
    ...:                          'excludes': ['that_field', 'bazo_field']},
    ...:           'that_field': {'type': 'dict',
    ...:                          'excludes': 'this_field'},
    ...:           'bazo_field': {'type': 'dict'}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'this_field': {}, 'bazo_field': {}}
    ...: c = (v.validate(document), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'this_field':
    ...:   ["'that_field', 'bazo_field' must not be present with 'this_field'"]}
    ...:

 In [3]:
```

### forbidden
このルールは、 `allowed` とは逆に、値が定義された値以外のものであるかどうかを検証します。


```
 In [2]: # %load 51_forbidden.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'user': {'forbidden': ['root', 'admin']}}
    ...: v = Validator(schema)
    ...:
    ...: document = {'user': 'root'}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'user': ['unallowed value root']}
    ...:
    ...: document = {'user': 'jack'}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == True
    ...:

 In [3]:
```

### items
任意の反復可能な項目(iitem)を、インデックスに対応する各項目を検証しなければならない一連の規則に対して検証します。項目は、与えられた反復可能のサイズが定義のものと一致する場合にのみ評価されます。これは正規化の際にも適用され、長さが不一致の場合、値の項目は正規化されません。


```
 In [2]: # %load 52_items.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'list_of_values': {
    ...:              'type': 'list',
    ...:              'items': [{'type': 'string'}, {'type': 'integer'}]}
    ...:           }
    ...: v = Validator(schema)
    ...:
    ...: document = {'list_of_values': ['hello', 100]}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'list_of_values': [100, 'hello']}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'list_of_values':
    ...:                  [{0: ['must be of string type'],
    ...:                    1: ['must be of integer type']}]}
    ...:

 In [3]:
```

### keysrules
このルールは、マッピングのすべてのキーが検証される制約としてルールのセットを受け取ります。


```
 In [2]: # %load 53_keysrules.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'a_dict': {
    ...:               'type': 'dict',
    ...:               'keysrules': {'type': 'string', 'regex': '[a-z]+'}}
    ...:           }
    ...: v = Validator(schema)
    ...:
    ...: document = {'a_dict': {'key': 'value'}}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'a_dict': {'KEY': 'value'}}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'a_dict':
    ...:                  [{'KEY': ["value does not match regex '[a-z]+'"]}]}
    ...:

 In [3]:
```

### meta
これは実際には検証ルールではなく、ルールセットの中のフィールドであり、ドキュメントフィールドのために記述されたアプリケーション固有のデータのために慣習的に使用することができます。


```
 {'id': {'type': 'string', 'regex': r'[A-M]\d{,6}',
         'meta': {'label': 'Inventory Nr.'}}}

```

割り当てられたデータの種類は問いません。

### min、max
比較演算( `__gt__()` と  `__lt__()` )を実装しているクラスのオブジェクトに許される最小値と最大値で検証します。


```
 In [2]: # %load 54_min_max.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'weight': {'min': 10.1, 'max': 10.9}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'weight': 10.3}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'weight': 12}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'weight': ['max value is 10.9']}
    ...:

 In [3]:
```

### minlength、 maxlength
サイズを得る `__len__()` を実装する型に許される最小と最大の長さで検証します。


```
 In [2]: # %load 55_min_max_length.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'numbers': {'minlength': 1, 'maxlength': 3}}
    ...: v = Validator(schema)
    ...:
    ...: document = {'numbers': [256, 2048, 23]}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'numbers': [256, 2048, 23, 2]}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] == {'numbers': ['max length is 3']}
    ...:

 In [3]:
```

### noneof

提供された制約の中にフィールドを検証するものがない場合に検証します。詳細は *of-rules を参照してください。

### nullable
 `True` の場合、フィールドの値は  `None` であることが許可されます。ルールは、定義されているかどうかにかかわらず、すべてのフィールドでチェックされます。ルールの制約のデフォルトは `False` です。


```
 In [2]: # %load 56_nullable.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'a_nullable_integer': {'type': 'integer','nullable': True},
    ...:           'an_integer': {'type': 'integer'}}
    ...: v = Validator(schema)
    ...:
    ...: document = {'a_nullable_integer': 3}
    ...: c1 = v.validate(document)
    ...: assert c1 == True
    ...:
    ...: document = {'a_nullable_integer': None}
    ...: c2 = v.validate(document)
    ...: assert c2 == True
    ...:
    ...: document = {'an_integer': 3}
    ...: c3 = v.validate(document)
    ...: assert c3 == True
    ...:
    ...: document = {'an_integer': None}
    ...: c4 = (v.validate(document), v.errors)
    ...: assert c4[0] == False
    ...: assert c4[1] == {'an_integer': ['null value not allowed']}
    ...:

 In [3]:
```

### *of-rules
これらのルールでは、検証するための異なるセットを定義することができます。ロジックを表す `all` 、 `any` 、 `one` 、 `none` で始まるルール名です。これらのルールに従ってリスト内のセットに対して検証された場合に有効となります。

of-rules

| ルール | 説明 |
|:--|:--|
| allof | すべての制約条件がそのフィールドを有効にするかどうかを検証する |
| anyof | 制約条件のいずれかがフィールドを有効にする場合に有効 |
| noneof | 制約条件のいずれもそのフィールドを有効にしない場合に有効 |
| oneof | 制約条件のうち、正確に1つが適用される場合に有効 |

備考
これらのルールの制約の中で、ルールセットに正規化を使用することはできません。

注意
これらのルールを使用する前に、Cerberusを使用する場合と使用しない場合の問題に対する他の可能な解決策を調べておく必要があります。これらのルールを使用すると、スキーマが複雑になりすぎることがあります。

例えば、フィールドの値が0～10または100～110の数字であることを確認するには、次のようにします。


```
 In [2]: # %load 57_anyof.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'prop1':
    ...:             {'type': 'number',
    ...:              'anyof': [{'min': 0, 'max': 10},
    ...:                        {'min': 100, 'max': 110}]
    ...:             }
    ...:         }
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'prop1': 5}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:
    ...: document = {'prop1': 105}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:
    ...: document = {'prop1': 55}
    ...: c = (v.validate(document), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'prop1': ['no definitions validate',
    ...:                  {'anyof definition 0': ['max value is 10'],
    ...:                   'anyof definition 1': ['min value is 100']}]}
    ...:

 In [3]:
```

 `anyof` ルールは、リスト内の各ルールセットをテストします。したがって、上記のスキーマは2つの別々のスキーマを作ることと同じです。


```
 In [2]: # %load 58_anyof_alternate.py
    ...: from cerberus import Validator
    ...:
    ...: schema1 = {'prop1': {'type': 'number', 'min':   0, 'max':  10}}
    ...: schema2 = {'prop1': {'type': 'number', 'min': 100, 'max': 110}}
    ...:
    ...: v = Validator()
    ...:
    ...: document = {'prop1': 5}
    ...: c = v.validate(document, schema1) or v.validate(document, schema2)
    ...: assert c == True
    ...:
    ...: document = {'prop1': 105}
    ...: c = v.validate(document, schema1) or v.validate(document, schema2)
    ...: assert c == True
    ...:
    ...: document = {'prop1': 55}
    ...: c = v.validate(document, schema1) or v.validate(document, schema2)
    ...: assert c == False
    ...: assert v.errors == {'prop1': ['min value is 100']}
    ...:

 In [3]:
```

### *of-rules の入力を簡単にする
of-ruleをアンダースコアで連結したり、別のルールをルールのあ値(rule-values）のリストで連結したりすることで、入力の手間を省くことができます。


```
 {'foo': {'anyof_regex': ['^ham', 'spam$']}}
 # 上記は次と同じ
 {'foo': {'anyof': [{'regex': '^ham'}, {'regex': 'spam$'}]}}
 # これとも同じ
 # {'foo': {'regex': r'(^ham|spam$)'}}
```

これを使えば、独自のロジックを実装することなく、複数のスキーマに対してドキュメントを検証することができます。


```
 In [2]: # %load 59_of_rules_concatenate.py
    ...: from cerberus import Validator
    ...:
    ...: schemas = [
    ...:     {'department': {'required': True, 'regex': '^CTU$'},
    ...:      'phone': {'nullable': True} },
    ...:     {'department': {'required': True},
    ...:      'phone': {'required': True}}
    ...:   ]
    ...:
    ...: employee_schema = {'employee': {'oneof_schema': schemas,
    ...:                                 'type': 'dict'}}
    ...:
    ...: employee_vldtr = Validator(employee_schema, allow_unknown=True)
    ...:
    ...: employees = [
    ...:   { 'employee': { 'name': 'Jack Bauer',
    ...:                   'department': 'CTU', 'phone': None }},
    ...:   { 'employee': { 'name': "Chloe O'Brian",
    ...:                   'department': 'CTU', 'phone': '001022' }},
    ...:   { 'employee': { 'name': 'Anthony Tony',
    ...:                   'department': 'CTU', 'phone': '001023' }},
    ...:   { 'employee': { 'name': 'Ann Wilson',
    ...:                   'department': 'Heart', 'phone': '002001' }},
    ...:   { 'employee': { 'name': 'Nacy Wilson',
    ...:                   'department': 'Heart', 'phone': None }}
    ...: ]
    ...:
    ...: invalid_employees_phones = []
    ...: for employee in employees:
    ...:     if not employee_vldtr.validate(employee):
    ...:         invalid_employees_phones.append(employee)
    ...:
    ...: from pprint import pprint as print
    ...: print(invalid_employees_phones)
    ...:
 [{'employee': {'department': 'CTU',
                'name': "Chloe O'Brian",
                'phone': '001022'}},
  {'employee': {'department': 'CTU', 'name': 'Anthony Tony', 'phone': '001023'}},
  {'employee': {'department': 'Heart', 'name': 'Nacy Wilson', 'phone': None}}]

 In [3]:
```

### oneof
提供された制約条件のうち、正確に1つが適用されるかどうかを検証します。詳細は *of-rules を参照してください。

### readonly
 `True` の場合、値は読み取り専用になります。このフィールドがターゲット辞書に存在する場合、バリデーションは失敗します。これは、例えば、データストアに送信する前に検証されるべきデータを受信した場合などに便利です。このフィールドはデータストアから提供されるかもしれませんが、書き込み可能であってはなりません。

 `Validator` クラスに引数 `purge_readonly` 与えてインスタンスを作成するか、インスタンスオブジェクトの同名のプロパティを設定することで、このルールが積極的に定義されているすべてのフィールドを削除することができます。
 `default` および `default_setter` と組み合わせて使用することができます。

### regex
フィールドの値が指定した正規表現に一致しない場合、検証エラーになります。これは文字列の値に対してのみテストされます。


```
 In [2]: # %load 60_regex.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {
    ...:     'email': {
    ...:        'type': 'string',
    ...:        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    ...:     }
    ...: }
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'email': 'john@example.com'}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:
    ...: document = {'email': 'john_at_example_dot_com'}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] ==  {'email':
    ...: ["value does not match regex \
    ...: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'"]}
    ...:

 In [3]:
```

すべてのパターンで末尾の  `$ ` が保証されているのは、ユーザーが文字列のマッチング（検索ではなく）のために完全なパターンを書くことを奨励するためです。先頭の  `^` については、実装に一貫性がなく、強制されていません。この不整合は 1.3.x リリースシリーズでは修正されません。正規表現の構文の詳細については、標準ライブラリの [re ](https://docs.python.org/ja/3/library/re.html?highlight=re#module-re) のドキュメントを参照してください。

式の一部として動作フラグを設定できることに注意してください。これは、例えば `re.compile()` 関数にフラグを渡すことと同じです。つまり、制約  `'(?i)holy grail'` は  `re.I` フラグに相当するものを含んでおり、  `'holy grail'` またはその変形を大文字のグリフで含むすべての文字列にマッチします。記載されているライブラリのドキュメントで `(?aiLmsux)` を探すと、そこに記述があります。

### require_all
これは、サブドキュメントのバリデータの `require_all` プロパティを設定するために、マッピングを検証する際のスキーマルールと組み合わせて使用することができます。 `13_require_all_schema.py` の動作をもう一度確認してみてください。

### required
 `True` の場合、そのフィールドは必須です。 `update=True` で `validate()` が呼ばれない限り、このフィールドがないと検証は失敗します。


```
 In [2]: # %load 61_required.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'name': {'required': True, 'type': 'string'},
    ...:             'age': {'type': 'integer'}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'age': 10}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == False
    ...: assert c1[1] == {'name': ['required field']}
    ...:
    ...: c2 = v.validate(document, update=True)
    ...: assert c2 == True
    ...:

 In [3]:
```

備考
ドキュメントのすべてのフィールドを必須(required)として定義する方法は、「すべてを要求するスキーマ」でのサンプルコード `12_require_all.py` を参照してください。

注意
 `required` が True に設定されていても、値が空(empty)の文字列フィールドは検証されます。空の値を受け入れたくない場合は、 `empty` ルールを参照してください。

注意
このルールの評価では、 `dependencies` ルールで定義された制約条件は考慮されません。

### schema (dict)
schemaルールが定義されているフィールドの値としてマッピングがある場合、そのマッピングは制約として提供されているスキーマに対して検証されます。


```
 In [2]: # %load 62_schema_rule_dict.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'a_dict': {'type': 'dict',
    ...:                      'schema': {'address': {'type': 'string'},
    ...:                                 'city': {'type': 'string',
    ...:                                          'required': True}}
    ...:                     }
    ...:         }
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'a_dict': {'address': 'my address', 'city': 'my town'}}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:

 In [3]:
```

マッピングの任意のキーを検証するには  `keysrules` ルール、マッピングの任意の値を検証するには  `valuesrules` ルールを参照してください。

### schema(list)
schema-validationが値として不規則なサイズのシーケンスに遭遇した場合、シーケンスのすべてのアイテムは、スキーマの制約で提供されたルールに対して検証されます。


```
 In [2]: # %load 63_schema_rule_list.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'a_list': {'type': 'list',
    ...:                      'schema': {'type': 'integer'}}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'a_list': [3, 4, 5]}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:

  In [3]:
```

また、リスト型に関するスキーマルールは、辞書のリストを定義して検証するのに適した方法です。


注意点
このルールを使用する際には、例のようにフィールドをリスト型に明示的に制限するタイプルールを併用する必要があります。そうしないと、シーケンスの制約を持つこのルールに対してマッピングを検証したときに、誤った結果が生じる可能性があります。


```
 In [2]: # %load 63_schema_rule_list.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'a_list': {'type': 'list',
    ...:                      'schema': {'type': 'integer'}}}
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'a_list': [3, 4, 5]}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:

 In [3]:
```


### type
キーの値に使用できるデータタイプ。次のいずれかの名前を指定できます。
Cerberus のタイプはValidatorインスタンスの　types プロパティーで参照することができます。


```
 In [3]: v.types
 Out[3]:
 ('binary',
  'boolean',
  'container',
  'date',
  'datetime',
  'dict',
  'float',
  'integer',
  'list',
  'number',
  'set',
  'string')

```

 type

| タイプ  | Python 2 Type  | Python 3 Type |
|:--|:--|:--|
| boolean | bool | bool |
| binary  | bytes, bytearray  | bytes, bytearray |
| date | datetime.date |  datetime.date |
| datetime | datetime.datetime | datetime.datetime |
| dict | collections.Mapping | collections.abc.Mapping |
| float | float | float |
| integer | int, long    | int |
| list     | collections.Sequence, excl. string   | collections.abc.Sequence, excl. string |
| number   | float, int, long, excl. bool     | float, int, excl. bool |
| set  | set  | set |
| string   | basestring()     | str |


このリストを拡張して、カスタムタイプをサポートすることができます。

タイプのリストを使用して、異なる値を許可することができます。

python
```
 In [2]: # %load 64_type.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'quotes': {'type': ['string', 'list']}}
    ...: v = Validator()
    ...:
    ...: document = {'quotes': 'Hello world!'}
    ...: c = v.validate(document, schema)
    ...: assert c == True
    ...:
    ...: document = {'quotes': ['Do not disturb my circles!', 'Heureka!']}
    ...: c = v.validate(document, schema)
    ...: assert c == True
    ...:
    ...: schema = {'quotes': {'type': ['string', 'list'],
    ...:                      'schema': {'type': 'string'}}}
    ...:
    ...: document = {'quotes': 'Hello world!'}
    ...: c = v.validate(document, schema)
    ...: assert c == True
    ...:
    ...: document = {'quotes': [1, 'Heureka!']}
    ...: c = (v.validate(document, schema), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'quotes': [{0: ['must be of string type']}]}
    ...:

 In [3]:
```

備考:
型規則の設定は必須ではありませんが、特に schema のような複雑な規則を使用する場合は、設定しないことをお勧めします。それでも明示的な型を設定したくないと判断した場合、schemaなどのルールは、そのルールを実際に使用できる値（ `dict` や `list` など）にのみ適用されます。また、schemaの場合、Cerberus は  `list` と  `dict` のどちらの型のルールが適切かを判断し、schemaのルールがどのようなものかに応じて推論します。

注意点:
型の検証は、同じフィールドに存在する他のほとんどの型よりも先に実行されることに注意してください（事前に考慮されるのは `nullable` と `readonly` のみ）。型の失敗が発生した場合、そのフィールドに対する後続の検証ルールはスキップされ、他のフィールドの検証が続行されます。これにより、他の（標準またはカスタム）ルールが呼び出されたときに、フィールドの型が正しいと安全に仮定することができます。

### valuesrules
このルールは、マッピングのすべての値が検証される制約としてルールのセットを受け取ります。


```
 In [2]: # %load 65_valuesrules.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'numbers':
    ...:              {'type': 'dict',
    ...:               'valuesrules': {'type': 'integer', 'min': 10}}
    ...: }
    ...:
    ...: v = Validator(schema)
    ...:
    ...: document = {'numbers': {'an integer': 10, 'another integer': 100}}
    ...: c = v.validate(document)
    ...: assert c == True
    ...:
    ...: document = {'numbers': {'an integer': 9}}
    ...: c = (v.validate(document), v.errors)
    ...: assert c[0] == False
    ...: assert c[1] == {'numbers': [{'an integer': ['min value is 10']}]}
    ...:

 In [3]:
```

## 正規化ルール
正規化ルール(Nomalization Rules) はフィールドに適用されます。マッピング用のスキーマでも適用されますし、スキーマ（シーケンス用）、 `allow_unknown` 、 `keysrules` 、 `valuesrules` で一括操作として定義された場合にも適用されます。 `anyof` のようなテスト用バリアントの定義における正規化ルールは処理されません。

正規化は、マッピングの各レベルに対して、深さ優先で、このドキュメントに記載されているとおりに適用されます。

フィールドの名前変更
処理を行う前に名前を変更するフィールドを定義することができます。

### フィールドのリネーム
次の処理を行う前に名前を変更するフィールドを定義できます。



```
 In [2]: # %load 70_renaming_of_fields.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'foo': {'rename': 'bar'}}
    ...: v = Validator(schema)
    ...:
    ...: document = {'foo': 0}
    ...: c = v.normalized(document)
    ...:
    ...: keys = c.keys()
    ...: assert ('foo' in keys) == False
    ...: assert ('bar' in keys) == True
    ...: assert c != document
    ...: assert c == {'bar': 0}
    ...:

 In [3]:
```


callableがフィールドや任意のフィールドの名前を変更できるようにするには、名前変更用のハンドラを定義します。制約が文字列の場合は、カスタム・メソッドを指します。制約が反復可能であれば、値はそのチェーンで処理されます。


```
 In [2]: # %load 71_rename_handler.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator({}, allow_unknown={'rename_handler': int})
    ...:
    ...: document = {'0': 'foo'}
    ...: c1 = v.normalized(document)
    ...:
    ...: keys = c1.keys()
    ...: assert (0 in keys) == True
    ...: assert ('0' in keys) == False
    ...: assert c1 != document
    ...: assert c1 == {0: 'foo'}
    ...:
    ...: even_digits = lambda x: '0' + x if len(x) % 2 else x
    ...: v = Validator({}, allow_unknown={'rename_handler': [str, even_digits]})
    ...:
    ...: document = {1: 'foo'}
    ...: c2 = v.normalized(document)
    ...:
    ...: keys = c2.keys()
    ...: assert (1 in keys) == False
    ...: assert ('1' in keys) == False
    ...: assert ('01' in keys) == True
    ...: assert c2 != document
    ...: assert c2 == {'01': 'foo'}
    ...:

 In [3]:
```


### 未知のフィールドの除去
名前を変更した後、 Validator インスタンスの  `purge_unknown` プロパティが  `True` であれば、 未知のフィールドは除去されます（デフォルトは  `False` ）。このプロパティは、初期化時にキーワード・引数ごとに設定することもできますし、  `allow_unknown` のようにサブドキュメントのルールとして設定することもできます（「未知なキーを許可する」を参照）。既定値は  `False` です。サブドキュメントに  `allow_unknown` ルールが含まれている場合、そのサブドキュメントでは未知のフィールドは除去されません。


```
 In [2]: # %load 72_purge_unknown_fields.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'foo': {'type': 'string'}}
    ...: v = Validator(schema, purge_unknown=True)
    ...:
    ...: c = v.normalized({'bar': 'foo'})
    ...: assert c == {}
    ...:
    ...: c = v.normalized({'foo': 'bar'})
    ...: assert c == {'foo': 'bar'}
    ...:

 In [3]:
```

### デフォルト値
ドキュメント内の欠落しているフィールドのデフォルト値を、 `default` ルールを使って設定することができます。


```
 In [2]: # %load 73_default_values.py
    ...: from cerberus import Validator
    ...:
    ...: schema = {'amount': {'type': 'integer'},
    ...:           'kind': {'type': 'string', 'default': 'purchase'}}
    ...: v = Validator(schema)
    ...:
    ...: c1 = v.normalized({'amount': 1})
    ...: assert c1 == {'amount': 1, 'kind': 'purchase'}
    ...:
    ...: c2 = v.normalized({'amount': 1, 'kind': None})
    ...: assert c2 == {'amount': 1, 'kind': 'purchase'}
    ...:
    ...: c3 = v.normalized({'amount': 1, 'kind': 'other'})
    ...: assert c3 == {'amount': 1, 'kind': 'other'}
    ...:

 In [3]:
```

デフォルト値を動的に設定するために、 `default_setter` にcallable を定義することもできます。この callable は、現在の（サブ）ドキュメントを唯一の引数として呼び出されます。callableは互いに依存することもできますが、解決できない/循環する依存関係がある場合、正規化は失敗します。制約が文字列の場合は、カスタムメソッドを指します。


```
 In [2]: # %load 74_default_setter.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator()
    ...: v.schema = {'a': {'type': 'integer'},
    ...:             'b': {'type': 'integer',
    ...:             'default_setter': lambda doc: doc['a'] + 1}}
    ...:
    ...:
    ...: c1 = v.normalized({'a': 1})
    ...: assert c1 == {'a': 1, 'b': 2}
    ...:
    ...: v.schema = {'a': {'type': 'integer',
    ...:                   'default_setter': lambda doc: doc['not_there']}}
    ...:
    ...: c = v.normalized({})
    ...: assert c == None
    ...: assert v.errors == {'a': ["default value for 'a' cannot be set: Circular
    ...:  dependencies of default setters."]}
    ...:

  In [3]:
```


同じフィールドに `default` と `readonly` の両方を使用することもできます。これにより、手動で値を割り当てることができないフィールドが作成されますが、Cerberusによって自動的にデフォルト値が提供されます。もちろん、 `default_setter` にも同じことが言えます。

### 値の強制
Coercion(強制)は、ドキュメントが検証される前に、 callable（オブジェクトまたはカスタムcoercionメソッドの名前として与えられる）を値に適用することができます。callableの戻り値は、ドキュメント内の新しい値に置き換わります。これは、バリデーションを受ける前に値を変換したり、データから不適切な部分を取り除いたりする（sanitize)のに使用できます。制約がcallableと名前のイテレート可能なものである場合、値はその一連のCoercion Callable を通して処理されます。


```
 In [2]: # %load 75_value_coercion.py
    ...: from cerberus import Validator
    ...:
    ...: v = Validator()
    ...: v.schema = {'amount': {'type': 'integer'}}
    ...: c = v.validate({'amount': '1'})
    ...: assert c == False
    ...:
    ...: v.schema = {'amount': {'type': 'integer', 'coerce': int}}
    ...: c = v.validate({'amount': '1'})
    ...: assert c == True
    ...: assert v.document == {'amount': 1}
    ...:
    ...: to_bool = lambda v: v.lower() in ('true', '1')
    ...: v.schema = {'flag': {'type': 'boolean', 'coerce': (str, to_bool)}}
    ...: c = v.validate({'flag': 'true'})
    ...: assert c == True
    ...: assert v.document == {'flag': True}
    ...:

 In [3]:

```


## エラーとエラー処理

エラーは、Pythonインターフェースを介して評価されたり、エラーハンドラを使ってさまざまな出力形式に処理されます。

### エラーハンドラ
エラーハンドラは、ドキュメントの処理後にバリデータの errors プロパティを通じて異なる出力を返します。エラーハンドラは必須のインターフェイスを定義した  `BaseErrorHandler` をベースにしています。使用するエラーハンドラは、キーワード引数  `error_handler` としてバリデータの初期化時に渡すか、 同じ名前のプロパティをいつでも設定することができます。初期化の際には、インスタンスかクラスのどちらかを指定します。クラスの初期化にキーワード引数を渡すには、 エラーハンドラクラスと引数を含む辞書の 2 つの値のタプルを指定します。

次のようなハンドラが用意されています。

- **BasicErrorHandler**：これは辞書を返すデフォルトのものです。キーはドキュメントのものを参照し、値はエラー・メッセージを含むリストです。ネストされたフィールドのエラーは、これらのリストの最後の項目として辞書に保存されます。

### Python インターフェース
エラーは以下のプロパティを持つ  `ValidationError` として表現されます。

-  `document_path` ：ドキュメント内のパス。フラットな辞書の場合、これは単にタプル内のキーの名前であり、ネストされた辞書の場合は、すべてのトラバースされたキーの名前です。シーケンス内の項目はインデックスで表されます。
-  `schema_path` ：スキーマ内のパスです。
-  `code` ：エラーの一意な識別子です。
-  `rule` ：ルール エラーの発生時に評価されたルールです。
-  `constraint` ：制約。そのルールの制約条件です。
-  `value` ：検証されている値です。
-  `info` ： このタプルには、エラーとともに送信された追加情報が含まれます。ほとんどのエラーでは、これは実際には何もありません。一括して検証する場合 (アイテムや  `keysrules` を使用する場合など) は、このプロパティに個々のエラーがすべて記録されます。追加のロギングを確認するには、ソースコードのルールの実装を参照してください。

ドキュメントを処理した後で、以下の  `Validator` インスタンスのプロパティでエラーにアクセスできます。

-  `_errors` ：このErrorsListインスタンスは、送信されたすべてのエラーを保持します。この属性でエラーを直接操作するつもりはありません。特定のエラー定義を持つエラーが少なくともひとつ、このリストに含まれているかどうかを調べることができます。
-  `document_error_tree` ：ドキュメントに対応するノードを問い合わせることができるディクテーションのようなオブジェクトです。ノードの添え字表記により、指定された ErrorDefinition に一致する特定のエラー、または指定されたキーを持つ子ノードのいずれかをフェッチできます。一致するエラーがそれぞれノード以下で発生していない場合は、代わりに None が返されます。ノードは、ErrorDefinitionまたは子ノードのキーにマッチする可能性のあるin演算子でテストすることもできます。ノードのエラーは、ErrorsListでもあるそのerrorsプロパティに含まれています。ノードのエラーは、そのエラー・プロパティに含まれます。
-  `schema_error_tree` ：使用されているスキーマと同じです。


```
 n [2]: # %load 80_error_handling.py
    ...: from cerberus import Validator
    ...: from cerberus.errors import BAD_TYPE
    ...:
    ...: schema = {'cats': {'type': 'integer'}}
    ...: document = {'cats': 'two'}
    ...:
    ...: v = Validator()
    ...:
    ...: c = v.validate(document, schema)
    ...: assert c == False
    ...: assert BAD_TYPE in v._errors
    ...:
    ...: c = v.document_error_tree['cats'].errors
    ...: assert c == v.schema_error_tree['cats']['type'].errors
    ...:
    ...: assert BAD_TYPE in v.document_error_tree['cats']
    ...:
    ...: c = v.document_error_tree['cats'][BAD_TYPE]
    ...: assert c == v.document_error_tree['cats'].errors[0]
    ...:
    ...: error = v.document_error_tree['cats'].errors[0]
    ...: assert error.document_path == ('cats',)
    ...: assert error.schema_path == ('cats', 'type')
    ...: assert error.rule == 'type'
    ...: assert error.constraint == 'integer'
    ...: assert error.value == 'two'
    ...:

 In [3]:
```


### エラーコード
 `code` プロパティーは、具体的なエラーのコードとして使用される  `ErrorDefinition` を一意に識別します。いくつかのコードは、異なるエラーの共有プロパティをマークするために実際に予約されています。これらは、エラーを処理する際のビットマスクとして役立ちます。次の表はは、予約されたコードの一覧です。

 予約されているエラーコード

| ビット | 16進表記 | 10進表記 | 意味 |
|:--|:--|:--|:--|
| 0110 0000 | 0x60 | 96 | 正規化の際に発生したエラー |
| 1000 0000 | 0x80 | 128 | 子エラーを含んだエラー |
| 1001 0000 | 0x90 | 144 | いずれかの*of-rulesが発したエラー |

次の表は、cerberus.errors モジュールに登録されているエラーコードの一覧です。

 エラーコード一覧

| 10進数 | 16進数 | コード名 | ルール |
|:--|:--|:--|:--|
| 0 | 0x0 | CUSTOM | None |
| 2 | 0x2 | REQUIRED_FIELD | required |
| 3 | 0x3 | UNKNOWN_FIELD | None |
| 4 | 0x4 | DEPENDENCIES_FIELD | dependencies |
| 5  | 0x5 | DEPENDENCIES_FIELD_VALUE  | dependencies |
| 6  | 0x6 | EXCLUDES_FIELD | excludes |
| 34 | 0x22 | EMPTY_NOT_ALLOWED | empty |
| 35 | 0x23 | NOT_NULLABLE | nullable |
| 36 | 0x24 | BAD_TYPE | type |
| 37 | 0x25 | BAD_TYPE_FOR_SCHEMA | schema |
| 38 | 0x26 | ITEMS_LENGTH | items |
| 39 | 0x27 | MIN_LENGTH | minlength |
| 40 | 0x28 | MAX_LENGTH | maxlength |
| 65 | 0x41 | REGEX_MISMATCH   | regex |
| 66 | 0x42     | MIN_VALUE    | min |
| 67 | 0x43     | MAX_VALUE    | max |
| 68 | 0x44     | UNALLOWED_VALUE  | allowed |
| 69 | 0x45     | UNALLOWED_VALUES     | allowed |
| 70  | 0x46     | FORBIDDEN_VALUE |  forbidden |
| 71 | 0x47     | FORBIDDEN_VALUES   |   forbidden |
| 72 | 0x48     | MISSING_MEMBERS  | contains |
| 96 | 0x60     | NORMALIZATION    | None |
| 97 | 0x61     | COERCION_FAILED  | coerce |
| 98 | 0x62     | RENAMING_FAILED  | rename_handler |
| 99 | 0x63     | READONLY_FIELD   | readonly |
| 100 | 0x64     | SETTING_DEFAULT_FAILED   | default_setter |
| 128 | 0x80     | ERROR_GROUP  | None |
| 129 | 0x81     | MAPPING_SCHEMA   | schema |
| 130 | 0x82     | SEQUENCE_SCHEMA  | schema |
| 131 | 0x83     | KEYSRULES    | keysrules |
| 131 | 0x83     | KEYSCHEMA    | keysrules |
| 132 | 0x84     | VALUESRULES  | valuesrules |
| 132 | 0x84     | VALUESCHEMA  | valuesrules |
| 143 | 0x8f     | BAD_ITEMS    | items |
| 144  | x90     | LOGICAL  | None |
| 145 | 0x91     | NONEOF   | noneof |
| 146 | 0x92     | ONEOF    | oneof |
| 147 | 0x93     | ANYOF    | anyof |
| 148 | 0x94     | ALLOF    | allof |


## Cerberusの拡張
 `coerce` や  `check_with` ルールは関数と組み合わせて使うことができますが、  `Validator` クラスをカスタムルール、タイプ、 `check_with` ハンドラ、 `coerce` 、 `default_setter` で簡単に拡張することができます。関数ベースのスタイルは、特殊な用途や一度きりの使用に適していますが、カスタムクラスでの拡張は次のようなメリットがありあす。

- カスタムルールをスキーマの制約条件で定義できる
- 利用可能な型を拡張する
- 追加のコンテクストデータを使用できる
- スキーマはシリアライズ可能

これらのカスタムメソッドへのスキーマ内の参照には、アンダースコアの代わりにスペース文字を使用できます。
 `{'foo': {'check_with': 'is odd'}}` は　 `{'foo': {'check_with': 'is_odd'}}` と同じことになります。


### カスタムルール
今回のユースケースでは、奇数の整数でしか表現できない値があるので、検証スキーマに新しい is_odd ルールのサポートを追加することにしたとします。


```
 schema = {'amount': {'is odd': True, 'type': 'integer'}}
```

これを実現するためには次のスニペットのようなコードになります。


```
 from cerberus import Validator

 class MyValidator(Validator):
     def _validate_is_odd(self, constraint, field, value):
         """ Test the oddity of a value.

         The rule's arguments are validated against this schema:
         {'type': 'boolean'}
         """
         if constraint is True and not bool(value & 1):
             self._error(field, "Must be an odd number")
```

Cerberus Validator クラスをサブクラス化し、カスタム _validate_<rulename> メソッドを追加することで、Cerberus を私たちのニーズに合わせて拡張しました。カスタムルール is_odd がスキーマで利用可能になり、さらに重要なことに、このルールを使ってすべての奇数値を検証することができます。


```
 In [2]: # %load 90_custom_validatr.py
    ...: from cerberus import Validator
    ...:
    ...: class MyValidator(Validator):
    ...:     def _validate_is_odd(self, constraint, field, value):
    ...:         """ Test the oddity of a value.
    ...:
    ...:         The rule's arguments are validated against this schema:
    ...:         {'type': 'boolean'}
    ...:         """
    ...:         if constraint is True and not bool(value & 1):
    ...:             self._error(field, "Must be an odd number")
    ...:
    ...: schema = {'amount': {'is odd': True, 'type': 'integer'}}
    ...:
    ...: v = MyValidator(schema)
    ...: c = v.validate({'amount': 10})
    ...: assert c == False
    ...: assert v.errors == {'amount': ['Must be an odd number']}
    ...:
    ...: c = v.validate({'amount': 9})
    ...: assert c == True
    ...:

 In [3]:
```

スキーマ自体が検証されるように、そのルールのスキーマで与えられた引数を検証するために、ルールの実装メソッドのdocstringでPythonのリテラル表現として制約を提供することができます。docstringにリテラルのみが含まれるか、リテラルがdocstringの一番下に置かれ、その前にThe rule's arguments are validated against this schema.が付けられます。

### カスタムデータタイプ
Cerberusはいくつかの標準的なデータタイプをサポートし、検証します。カスタムバリデータを作成する際には、独自のデータタイプを追加して検証することができます。

types_mapping で指定した型の名前に TypeDefinition を割り当てることで、その場で型を追加することができます。


```
 from decimal import Decimal

 decimal_type = cerberus.TypeDefinition('decimal', (Decimal,), ())

 Validator.types_mapping['decimal'] = decimal_type

```

> 注意
> types_mappingプロパティはmutable型なので、インスタンスの項目を変更すると、そのクラスにも影響を与えます。

Validatorのサブクラスに定義することもできます。



```
 from decimal import Decimal

 decimal_type = cerberus.TypeDefinition('decimal', (Decimal,), ())

 class MyValidator(Validator):
     types_mapping = Validator.types_mapping.copy()
     types_mapping['decimal'] = decimal_type

```

### check_withルールで参照可能なメソッド
検証テストがスキーマの指定された制約に依存しない場合や、 ルールよりも複雑にする必要がある場合は、 ルールではなく値のチェッカとして定義することができます。check_withルールを使うには2つの方法があります。

ひとつは、Validatorを拡張して、先頭に_check_with_をつけたメソッドを作ることです。これにより、任意の設定値や状態を含むバリデータインスタンスのコンテキスト全体にアクセスできます。check_withルールを使ってこのようなメソッドを参照するには、接頭辞なしのメソッド名を文字列制約として渡すだけです。

たとえば、奇数番目のバリデータのメソッドを次のように定義することができます。


```
 class MyValidator(Validator):
     def _check_with_oddity(self, field, value):
         if not value & 1:
             self._error(field, "Must be an odd number")

```

使い方は以下のようになります。


```
 schema = {'amount': {'type': 'integer', 'check_with': 'oddity'}}

```

ルールを使用する2つ目の方法は、スタンドアローンの関数を定義し、それを制約条件として渡すことです。この場合、Validatorを拡張する必要がないという利点があります。この実装についての詳細や例を見るには、ルールのドキュメントを参照してください。

### カスタム強制
強制された結果を返すカスタム・メソッドや、  `rename_handler` としてメソッドを指定するカスタム・メソッドも定義できます。メソッド名の前には  `_normalize_coerce_` を付ける必要があります。


```
 class MyNormalizer(Validator):
     def __init__(self, multiplier, *args, **kwargs):
         super(MyNormalizer, self).__init__(*args, **kwargs)
         self.multiplier = multiplier

     def _normalize_coerce_multiply(self, value):
         return value * self.multiplier
```


```
 In [2]: # %load 91_custom_coercers.py
    ...: from cerberus import Validator
    ...:
    ...: class MyNormalizer(Validator):
    ...:     def __init__(self, multiplier, *args, **kwargs):
    ...:         super(MyNormalizer, self).__init__(*args, **kwargs)
    ...:         self.multiplier = multiplier
    ...:
    ...:     def _normalize_coerce_multiply(self, value):
    ...:         return value * self.multiplier
    ...:
    ...: schema = {'foo': {'coerce': 'multiply'}}
    ...: document = {'foo': 2}
    ...:
    ...: c = MyNormalizer(2).normalized(document, schema)
    ...: assert c == {'foo': 4}
    ...:

 In [3]:
```

### カスタムデフォルトセッター
カスタムリネームハンドラと同様に、カスタムデフォルトセッタを作成することも可能です。


```
 from datetime import datetime

 class MyNormalizer(Validator):
     def _normalize_default_setter_utcnow(self, document):
         return datetime.utcnow()

```


```
 In [2]: # %load 92_custom_default_setters.py
    ...: from cerberus import Validator
    ...: from datetime import datetime
    ...:
    ...: class MyNormalizer(Validator):
    ...:     def _normalize_default_setter_utcnow(self, document):
    ...:         return datetime.utcnow()
    ...:     def _normalize_default_setter_anniversary(self, document):
    ...:         return datetime(2020, 10, 2)
    ...:
    ...: schema = {'creation_date': {'type': 'datetime',
    ...:                             'default_setter': 'anniversary'}}
    ...:
    ...: c = MyNormalizer().normalized({}, schema)
    ...: assert c == {'creation_date': datetime(2020, 10, 2, 0, 0)}
    ...:

 In [3]:
```

よく使用してる特定のルールを上書きするのは良くないかもしれません。

### 設定データの添付とカスタム・バリデータのインスタンス化
 `Validator` やそのサブクラスをインスタンス化する際に、任意の構成値をキーワード引数 (Cerberus では使用しない名前) として渡すことができます。これらの値は、そのインスタンスにアクセスできる、このドキュメントで説明するすべてのハンドラーで使用できます。Cerberusは、処理中に生成される可能性のあるすべての子インスタンスで、このデータが利用可能であることを保証します。カスタマイズされたバリデータの  `__init__()` を実装する際には、すべての位置引数とキーワード引数が親クラスの初期化メソッドにも渡されるようにしなければなりません。以下にパターンの例を示します。


```
 class MyValidator(Validator):
     def __init__(self, *args, **kwargs):
         # インスタンス・プロパティに構成値を割り当てて利便性を高める
         self.additional_context = kwargs.get('additional_context')
         # すべてのデータをベースクラスに渡す
         super(MyValidator, self).__init__(*args, **kwargs)

     # また、ダイナミック・プロパティを定義することで、
     # この例では__init__()が不要になります。
     @property
     def additional_context(self):
         return self._config.get('additional_context', 'bar')

     # 状態を扱う場合のオプションのプロパティセッター
     @additional_context.setter
     def additional_context(self, value):
         self._config["additional_context"] = value

     def _check_with_foo(self, field, value):
         make_use_of(self.additional_context)

```

> 警告
> 上記で説明した以外の状況で _config プロパティにアクセスすることや、ドキュメントの処理中にその内容を変更することは推奨されません。これらのケースはテストされておらず、公式にサポートされる可能性は低いです。


### 関連するValidatorクラスの 属性
カスタムバリデータを書く際に注意すべき、Validatorクラスの属性があります。

#### Validator.document
バリデータは、検証用のフィールドを取得する際に document プロパティにアクセスします。これにより、フィールドの検証をドキュメントの他の部分と関連づけて行うことができます。

#### Validator.schema
同様に、schema プロパティは使用するスキーマを保持します。
この属性は、ある時点でバリデータにスキーマとして渡されたオブジェクトとは異なります。また、その内容も異なる可能性がありますが、 初期の制約を表していることには変わりありません。この属性は、dict と同じインターフェイスを提供します。

#### Validator._error
Validator のエラー・スタッシュにエラーを提出するために受け入れられる署名は3つあります。必要に応じて、与えられた情報は解析されて新しいValidationErrorのインスタンスが作成されます。

### 完全な開示
エラーの内容を後から完全に把握するためには、  `_error()` に 2 つの必須の引数を指定する必要があります。

- エラーが発生したフィールド
-  `ErrorDefinition` のインスタンス

カスタムルールでは、一意の ID を持つ  `ErrorDefinition` としてエラーを定義し、 違反したルールの原因を特定する必要があります。拠出されたエラー定義のリストは、 `errors` を参照してください。ビット7はグループエラーを示し、ビット5は異なるルールセットに対する検証で発生するエラーを示すことに注意してください。

必要に応じて、さらなる引数を情報として提出することができます。人間を対象としたエラーハンドラは、str.format()でメッセージをフォーマットする際に、これらを位置引数として使用します。シリアライズハンドラは、これらの値をリストにしておきます。

### シンプルなカスタムエラー
よりシンプルな方法は、フィールドとメッセージとしての文字列を指定して  `_error()` を呼び出すことです。しかし、結果として生じるエラーには、違反した制約に関する情報は含まれません。これは後方互換性を維持するためのものですが、詳細なエラー処理が必要でない場合にも使用できます。

### 複数のエラー
チャイルドバリデーターを使用する際には、そのエラーをすべて提出すると便利です。
これは ValidationError インスタンスのリストです。

#### Validator._get_child_validator
自分のサブクラスである `Validator ` の別のインスタンスが必要な場合は、` _get_child_validator()`メソッドで  `self` と同じ引数を指定して別のインスタンスを返します。キーワード引数をオーバーライドして指定することもできます。 `document_path` と  `schema_path` (下記参照) のプロパティは子バリデータに継承されるので、  `document_crumb` と  `schema_crumb` というキーワードで単一の値または値のタプルを渡すことで、これらを拡張することができます。

#### Validator.root_document,、.root_schema,、.root_allow_unknown、 .root_require_all
子バリデータ (スキーマを検証するときに使用するもの) は、  `root_document` 、  `root_schema` 、 `root_allow_unknown` および  `root_require_all` プロパティを使って、 第一世代のバリデータが処理しているドキュメントやスキーマ、 未知のフィールドに対する制約にアクセスできます。


#### Validator.document_path、Validator.schema_path
これらのプロパティは、親バリデータが通過したドキュメント内のキーのパスと、スキーマのパスを保持します。これらのプロパティは、エラーが発生したときのベースパスとして使われます。

#### Validator.recent_error
最後に送信されたエラーは、 `recent_error` プロパティでアクセスできます。

#### Validator.mandatory_validations、Validator.priority_validations、Validator._remaining_rules
これらのクラス・プロパティやインスタンス・プロパティは、各フィールドの検証ロジックを調整したい場合に使うことができます。  `mandatory_validations` は、スキーマのフィールドにルールが定義されているかどうかにかかわらず、各フィールドに対して検証されるルールを含むタプルです。  `priority_validations` は、他のルールよりも先に検証される順序付けられたルールのタプルです。 `_remaining_rules` は、これらを考慮して作成されたリストで、次に評価されるべきルールを追跡します。したがって、ルールハンドラで操作して、現在のフィールドに対する残りの検証を変更することができます。できれば、 `_drop_remaining_rules()` を呼んで特定のルールを削除したり、一度にすべてのルールを削除したりしたいところです。

## メッセージの日本語化
カスタムエラーハンドラーを設定することで、エラーメッセージを日本語化することができます。
 `BaasicErrorHandler` を継承した  `JapanseErrorHandler` を作成します。

 cerberus_extend.py
```
 from cerberus.errors import BasicErrorHandler

 class JapaneseErrorHandler(BasicErrorHandler):
     def __init__(self, tree = None):
         super(JapaneseErrorHandler, self).__init__(tree)
         self.messages = {
             0x00: "{0}",
             0x01: "ドキュメントが見つかりません",
             0x02: "必須項目です。",
             0x03: "不明な項目が指定されています。",
             0x04: "'{0}'は必須項目です。",
             0x05: "これらの値に依存します: {constraint}",
             0x06: "{0} はフィールド'{field}'にセットされてる必要があります",
             0x21: "'{0}'はドキュメントではありません。辞書でなければなりません",
             0x22: "必須項目です。",
             0x23: "必須項目です。",
             0x24: "{constraint}型でなければなりません",
             0x25: "辞書型でなければなりません。",
             0x26: "リストの長さは{constraint}なければなりませんが、{0}です",
             0x27: "{constraint}文字以上入力してください。",
             0x28: "{constraint}文字以内で入力してください。",
             0x41: "値が正規表現に一致しません:'{constraint}'",
             0x42: "{constraint}以上の値を入力してください。",
             0x43: "{constraint}以下の値を入力してください。",
             0x44: "{value}は指定できません。",
             0x45: "{0}は指定できません。",
             0x46: "{value}は指定できません。",
             0x47: "{0}は指定できません。",
             0x48: "{0}メンバーが見つかりません",
             0x61: "フィールド'{field}'は強制できません: {0}",
             0x62: "フィールド'{field}'はリネームできません: {0}",
             0x63: "フィールドはリードオンリーです",
             0x64: "フィールド'{field}'にデフォルト値{0}をセットできません",
             0x81: "マッピングがサブスキーマを検証しません: {0}",
             0x82: "ひとつ以上のシーケンス要素が検証されていません: {0}",
             0x83: "マッピングのひとつ以上のキーが検証されていません: {0}",
             0x84: "マッピングのひとつ以上の値が検証されていません: {0}",
             0x81: "マッピングがサブスキーマを検証しません: {0}",
             0x91: "ひとつまたは複数の定義を有効です",
             0x92: "ゼロもしくは複数のルールの検証です",
             0x93: "定義されていない検証です",
             0x94: "1つまたは複数の定義が検証されません"
         }

```

利用するときは `Validator()` の　 `error_handler` 引数にこのクラスを与えます。


```
 v = Validator(schema, error_handler=JapaneseErrorHandler())
```

動作確認をしてみましょう。


```
 In [2]: # %load 93_localization.py
    ...: from cerberus import Validator
    ...: from cerberus_extend import JapaneseErrorHandler
    ...:
    ...: # 参照: 52_items.py
    ...:
    ...: schema = {'list_of_values': {
    ...:              'type': 'list',
    ...:              'items': [{'type': 'string'}, {'type': 'integer'}]}
    ...:           }
    ...: v = Validator(schema, error_handler=JapaneseErrorHandler())
    ...:
    ...: document = {'list_of_values': ['hello', 100]}
    ...: c1 = (v.validate(document), v.errors)
    ...: assert c1[0] == True
    ...:
    ...: document = {'list_of_values': [100, 'hello']}
    ...: c2 = (v.validate(document), v.errors)
    ...: assert c2[0] == False
    ...: assert c2[1] != {'list_of_values':
    ...:                  [{0: ['must be of string type'],
    ...:                    1: ['must be of integer type']}]}
    ...: assert c2[1] == {'list_of_values':
    ...:                  [{0: ['string型でなければなりません'],
    ...:                    1: ['integer型でなければなりません']}]}
    ...:

 In [3]:
```




## 参考
- [Cerberus ドキュメント ](https://docs.python-cerberus.org/en/stable/index.html)
- [Cerberus ソースコード ](https://github.com/pyeve/cerberus)
- [Wikipadia Cerberus ](https://ja.wikipedia.org/wiki/ケルベロス)

#validation


