jinja2-cliを使ってみよう
=================

### jinja2-cliついて
テンプレートファイルを書きすすめていくとき、プログラムに頼らずに単独でレンダリングできればテンプレートファイルのデバッグが簡単になります。
 `jinja2-cli` はファイルに定義したデータを読み取ってレンダリングしてくれるものです。

### インストール
インストールは pip で行います。

```
 # Linux or mac
 $ python -m pip install jinja2-cli

 # Windwos
 $ py -3 -m  pip install jinja2-cli
```

データ形式は次のフォーマットをサポートしています。
- JSON：デフォルト
- YAML
- TOML
- XML

"[Jinja2を使ってみよう]" で例示したチャイルド・テンプレートをレンダリングしてみましょう。
まず、データをYAML形式で定義しておきます。

 data.yaml
```
 title: 'This is sample Page'
 body: 'Hello Python!'
```

これを、jinja2コマンドでレンダリングすることができます。

```
 $ jinja2 child.html data.yaml
 <HTML>
     <HEAD>
   <TITLE>This is sample Page</TITLE>
 </HEAD>

   <BODY>

   <p>
   Hello Python!
   </p>

   </BODY>
 </HTML>
```

タイプ量が少ないからという理由でYAML形式でデータを定義していますが、JSON形式であれば次のようになります。

 data.json
```
 {
     "title": "This is sample Page",
     "body": "Hello Python!"
 }
```

JSONではキーワードや値は二重引用符(ダブルクォート： `"` )で囲まないといけないなどの
制約もありますね。

参考：
- [jinja2-cli ソースコード](https://github.com/mattrobenolt/jinja2-cli])
- [JSON オフィシャルサイト](https://www.json.org/json-en.html])
- [YAML オフィシャルサイト　https://yaml.org/]



