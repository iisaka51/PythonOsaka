inquirerpy で対話型インタフェースを作成してみよう
=================
### inquirerpy について
[inquirerpy https://pypi.org/project/inquirerpy/] は NodeJS での[inquirer.js ](https://github.com/SBoudrias/Inquirer.js/] )に触発されて開発された、会話形アプリケーションを作成するための拡張モジュールです。
類似のモジュールには [python-inquirer https://github.com/magmax/python-inquirer] や、[PyInquirer ](https://github.com/CITGuru/PyInquirer) があります。
python-inquirer は　[node.js https://nodejs.org/ja/] の [inquirer.js ](https://github.com/SBoudrias/Inquirer.js) に触発されてほぼ同じ実装をPython で実現できるように開発されました。
しかし、残念ながら Windows では一部うまく動作しないことが確認されています

これに対して、inquirerpy と PyInquirer は内部的には [prompt_toolkit ](https://python-prompt-toolkit.readthedocs.io/en/master/#) を使用しているため、Windows でも問題なく動作できます。
ただし、PyInquirer は prompt_toolkit の古いバージョン1.0.14に依存していて、IPython などと共存することができなくなっています。inquirerpy はこの問題を解決するとともに、いくつかのバグを修正するために再開発されています。

inquirerpy は Python 3.7 以降で動作します。

### inquirerpy のインストール
inquirerpy はpipコマンドでインストールできます。

 bash
```
 $ pip install inquirerpy
```


### inquirerpy の互換API
inquirerpy は PyInquirer との互換性を考慮して開発されています。
まずは、PyInquirer との互換APIについて説明することにします。

 `prompt()` を使ってユーザから文字列を受け取る簡単な例から見てみましょう。


```
 In [2]: # %load 001_single_input.py
    ...: from InquirerPy import prompt
    ...:
    ...: questions = [
    ...:     {
    ...:         'type': 'input',
    ...:         'name': 'first_name',
    ...:         'message': "What's your first name",
    ...:     }
    ...: ]
    ...:
    ...: answers = prompt(questions)
    ...: print(answers)
    ...: print(answers['first_name'])
    ...:
 ? What's your first name Jack
 {'first_name': 'Jack'}
 Jack
 
```

スクリーンショットは次のようにユーザの入力は色が変わって表示されます。

![](https://gyazo.com/5314bb2517f65baeee96ed85a6dcaf50.png)

 `questions` は質問を記述した辞書のリストです。
 `prompt()` は質問の定義に従ってユーザからの入力を受け取り、辞書オブジェクトとして結果を返します。

リストにある複数の質問は続けて処理されます。


```
 In [2]: # %load 002_multiple_input.py
    ...: from InquirerPy import prompt
    ...:
    ...: questions = [
    ...:     {
    ...:         'type': 'input',
    ...:         'name': 'first_name',
    ...:         'message': "What's your first name",
    ...:     },
    ...:     {
    ...:         'type': 'input',
    ...:         'name': 'last_name',
    ...:         'message': "What's your last name",
    ...:         'when': lambda answers: answers['first_name'] != '',
    ...:     }
    ...: ]
    ...:
    ...: answers = prompt(questions)
    ...: print(answers)
    ...:
 ? What's your first name Jack
 ? What's your last name Bauer
 {'first_name': 'Jack', 'last_name': 'Bauer'}
 
 In [3]: %run 002_multiple_input.py
 ? What's your first name
 {'first_name': '', 'last_name': None}
 
```

質問の辞書に、 `when` で条件が与えられていると、その条件に合致するときだけ、その質問はユーザに問い合わせが行われます。


### 入力補完
ユーザから文字列を受け取るときに、予め登録した文字列に部分合致すると補完文字列をポップアップ表示します。
タブキーを押下すると残りの入力を補完したデータを返します。


```
 In [2]: # %load 03_completion.py
    ...: from InquirerPy import prompt
    ...:
    ...: questions = [
    ...:    {
    ...:        "type": "input",
    ...:        "message": "Which company would you like to apply:",
    ...:        "completer": {
    ...:            "Google": None,
    ...:            "Facebook": None,
    ...:            "Amazon": None,
    ...:            "Netflix": None,
    ...:            "Apple": None,
    ...:            "Microsoft": None,
    ...:        },
    ...:        "multicolumn_complete": True,
    ...:    },
    ...: ]
    ...:
    ...: answers = prompt(questions)
    ...: print(answers)
    ...:
 ? Which company would you like to apply: A
                                            Amazon
                                            Apple
```
![](https://gyazo.com/5cfb4a1efa15a83872002425a961eb92.png)


### transformer, filter, validate
ユーザの入力を加工したり、結果を変換したり、データ検証を行わせることができます。


```
 In [2]: # %load 004_validation.py
    ...: from InquirerPy import prompt
    ...: from InquirerPy.validator import NumberValidator
    ...:
    ...: questions = [
    ...:    {
    ...:        "name": "request salary",
    ...:        "type": "input",
    ...:        "message": "What's your salary expectation(k):",
    ...:        "transformer": lambda result: "%sk" % result,
    ...:        "filter": lambda result: int(result) * 1000,
    ...:        "validate": NumberValidator(),
    ...:    },
    ...: ]
    ...:
    ...: answer = prompt(questions)
    ...: print(answer)
    ...:
 ? What's your salary expectation(k): 2000k
 {'request salary': 2000000}
 
 In [3]: %run 004_validation.py
 ? What's your salary expectation(k): 1500万円
 Input should be number
```

![](https://gyazo.com/b0e286cd6b955b77c9e4c6b40c10e744.png)
![](https://gyazo.com/495cf54dfc802f62ca19c1813000865f.png)
![](https://gyazo.com/fde08f81995ee64f19024c7a2316dcc0.png)

 `transformer` は入力された文字列を加工して画面に出力します。 `filter` は入力されたデータを加工して返します。
 `validate` で与えた検証が失敗すると入力は完了せずに、エラーメッセージを出力して再度入力待ちになります。


## 質問のタイプ
質問を定義する辞書に与えるキー `type` で、質問のタイプを指定します。
次のようなタイプがあります。

-  `list` : リストした候補をカーソルキーで選択する
-  `rawlist` ：数値付きでリストした候補を数値で選択する
-  `expand` ：リストのコンパクト表示、キーアクションで展開表示
-  `checkbox` ：チョイスボックス
-  `confirm` ：ユーザに Yes/No の確認をしブール値を返す
-  `input` ：プロンプトを表示してユーザから文字列を受け取る
-  `password` ： `input` と似ているがユーザの入力は表示されない
-  `fazzy` : 
-  `editor` ：ユーザから複数行の入力を受け取る

## list タイプ
選択肢を表示してユーザに選ばせる基本的なUIです。

プロパティー: `type` ,  `name` ,  `message` ,  `choices` ,  `default` 、
 `[filter]` 、 `[transformer]` 、 `[validate]` 、 `[multiselect]` 、 `[invalid_message]` 

 `filter` で与えた処理がユーザの入力に適用されて返されます。
 `transformer` は返り値には影響は与えませんが、表示文字列を変更します。
 `multiselect` が `True` のときは複数の選択を許します。


```
 In [2]: # %load 005_list_simple.py
    ...: from InquirerPy import prompt
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "list",
    ...:         "message": "Select an action:",
    ...:         "choices": ["Upload", "Download",
    ...:                     {"name": "Exit", "value": None}],
    ...:         "default": None,
    ...:         # "multiselect": True,
    ...:     },
    ...: ]
    ...:
    ...: answer = prompt(questions=questions)
    ...: print(answer)
    ...:
 ? Select an action:
   Upload
   Download
 ❯ Exit
```

![](https://gyazo.com/25f1c79817cdd6c91363fe4f420653f1.png)

カーソルキーで候補を選択します。
マウスクリックでも候補を選択することができます。


```
 ? Select an action: Upload
 {0: 'Upload'}
 
```


 `multiselect` に `True` を与えると、複数選択することができラジオボタンのように動作します。タブキー、スペースキーで候補を選択できます。


### Separator
 `Separator` クラスのインスタンスオブジェクトを与えると、一覧するリストに区切り文字を表示するゆになります。


```
 In [1]: %load 006_list_separator.py
 
    ...: from InquirerPy import prompt
    ...: from InquirerPy.separator import Separator
    ...:
    ...: questions = [
    ...:     {
    ...:         "name": "region",
    ...:         "type": "list",
    ...:         "message": "Select regions:",
    ...:         "choices": [
    ...:             {"name": "Sydney", "value": "ap-southeast-2"},
    ...:             {"name": "Singapore", "value": "ap-southeast-1"},
    ...:             Separator(),
    ...:             "us-east-1",
    ...:             Separator(line='*' * 15),
    ...:             "us-east-2",
    ...:         ],
    ...:         "multiselect": True,
    ...:         "transformer": lambda result: "%s region%s selected"
    ...:         % (len(result), "s" if len(result) > 1 else ""),
    ...:     },
    ...: ]
    ...:
    ...: result = prompt(questions=questions)
    ...: print(result)
    ...:
 ? Select regions:
 ❯ Sydney
   Singapore
   ---------------
   us-east-1
   ***************
   us-east-2
     
 ? Select regions: 2 regions selected
 {'region': ['ap-southeast-2', 'ap-southeast-1']}
  
```

![](https://gyazo.com/a07213a0446061c18fdbae82a5c3f261.png)


## rawlist タイプ
自動的に数字のショートカットを適用させたリストプロンプトです。
各選択肢の前には数字が付加されます。この数字をショートカットキーとして使用して選択肢にジャンプしたり、通常の上下キーバインドで移動したりすることができます。

プロパティー: `type` ,  `name` ,  `message` ,  `choices` ,  `default` 、
 `[filter]` 、 `[transformer]` 、 `[validate]` 、 `[multiselect]` 、 `[invalid_message]` 



```
 In [2]: # %load 007_rawlist.py
    ...: from InquirerPy import prompt
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "rawlist",
    ...:         "choices": [
    ...:             "Apple", "Orange", "Peach", "Cherry",
    ...:             "Melon", "Strawberry", "Grapes",
    ...:         ],
    ...:         "message": "Pick your favourites:",
    ...:         "default": 3,
    ...:         "multiselect": True,
    ...:         "transformer": lambda result: ", ".join(result),
    ...:         "validate": lambda result: len(result) > 1,
    ...:         "invalid_message": "Minimum 2 selections",
    ...:     },
    ...: ]
    ...:
    ...: fruits = prompt(questions)
    ...: print(fruits)
    ...:
 ? Pick your favourites: 3
   1) Apple
   2) Orange
   3) Peach
   4) Cherry
   5) Melon
   6) Strawberry
   7) Grapes
 
 ? Pick your favourites: Peach, Strawberry
 {0: ['Peach', 'Strawberry']}
 
```

![](https://gyazo.com/86089c6e9455e6e20e3bd84f02a87849.png)


## expand タイプ
コンパクト(compact)と拡大(expand)の2種類のUIを持つリストプロンプトです。
はじめはコンパクトな状態で表示されますが、 `h` キーを使って拡大することができます。拡大後は、通常のリストナビゲーションキーが有効になります。

プロパティー: `type` ,  `name` ,  `message` ,  `choices` ,  `default` 、
 `[filter]` 、 `[transformer]` 、 `[validate]` 、 `[multiselect]` 、 `[invalid_message]` 、 `[instruction]` 



```
 In [2]: # %load 008_expand.py
    ...: from InquirerPy.separator import Separator
    ...:
    ...: fruits_choice = [
    ...:         {"key": "a", "name": "Apple", "value": "Apple"},
    ...:         {"key": "c", "name": "Cherry", "value": "Cherry"},
    ...:         {"key": "o", "name": "Orange", "value": "Orange"},
    ...:         {"key": "p", "name": "Peach", "value": "Peach"},
    ...:         {"key": "m", "name": "Melon", "value": "Melon"},
    ...:         {"key": "s", "name": "Strawberry", "value": "Strawberry"},
    ...:         {"key": "g", "name": "Grapes", "value": "Grapes"},
    ...: ]
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "expand",
    ...:         "choices": fruits_choice,
    ...:         "message": "Pick your favourite:",
    ...:         "default": "o",
    ...:         "cycle": False,
    ...:     },
    ...: ]
    ...:
    ...: result = prompt(questions)
    ...: print(result)
    ...:
 ? Pick your favourite: (acopmsgh) o
 ❯ Orange
 
 ? Pick your favourite: (acopmsgh) o
   a) Apple
   c) Cherry
   o) Orange
   p) Peach
   m) Melon
   s) Strawberry
   g) Grapes
   h) Help, list all choices
 
 ? Pick your favourite: Cherry
 {0: 'Cherry'}
 
```

![](https://gyazo.com/b255b57752244f25e009f296007efe78.png)
![](https://gyazo.com/8a313cf28822800d58a1f73ccdbac77d.png)


## checkbox タイプ
チェックボックスを表示するリストプロンプト。

マルチセレクトが可能な他のリストプロンプトでは、最小選択数は常に1です（ユーザが何も選択しない場合、現在のハイライトされた選択肢が選択されます）。チェックボックスプロンプトでは、現在のハイライトされた選択肢は自動的に選択されません。

プロパティー: `type` ,  `name` ,  `message` ,  `choices` ,  `default` 、
 `[filter]` 、 `[transformer]` 、 `[validate]` 、 `[multiselect]` 、 `[invalid_message]` 、 `[instruction]` 

 `choices` で与える各選択肢は、文字列表現を持つ任意の値、または以下のキーで構成される辞書にすることができます。

-  `name` :選択肢の表示名で、ユーザーはこの値を見ることができます。
-  `value` 選択肢の値。名前とは異なる場合がありますが、ユーザーはこの値を見ることはできません。
-  `enabled` : 選択肢が選択された状態にあるかどうかをTrue/Falseで与える

 `choices` で  `{'enabled'：True}` とされた選択肢は、デフォルトでチェックされます。

 pyton
```
 In [2]: # %load 009_checkbox.py
    ...: from InquirerPy import prompt
    ...: from InquirerPy.separator import Separator
    ...:
    ...: region_choice = [
    ...:     Separator(),
    ...:     {"name": "Sydney", "value": "ap-southeast-2", "enabled": False},
    ...:     {"name": "Singapore", "value": "ap-southeast-1", "enabled": True},
    ...:     Separator(),
    ...:     "us-east-1",
    ...:     "us-west-1",
    ...:     Separator(),
    ...: ]
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "checkbox",
    ...:         "message": "Select regions:",
    ...:         "choices": region_choice,
    ...:         "transformer": lambda result: "%s region%s selected"
    ...:         % (len(result), "s" if len(result) > 1 else ""),
    ...:     },
    ...: ]
    ...:
    ...: result = prompt(questions)
    ...: print(result)
    ...:
 ? Select regions:
   ---------------
 ❯ ⬡ Sydney
   ⬢ Singapore
   ---------------
   ⬡ us-east-1
   ⬡ us-west-1
   ---------------
     
 ? Select regions: 2 regions selected
 {0: ['ap-southeast-2', 'ap-southeast-1']}
 
 
```

![](https://gyazo.com/492eb616f6fb1b26fb6205693f82659b.png)

## confirm タイプ
ユーザーの確認を取るためのプロンプトです。

プロパティー: `type` ,  `name` ,  `message` ,  `choices` , `[default, when]` 
 `default` はブール値である必要があります。


```
 In [2]: # %load 010_confirm.py
    ...: from InquirerPy import prompt
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "confirm",
    ...:         "message": "Proceed?",
    ...:         "name": "proceed",
    ...:         "default": True,
    ...:     },
    ...:     {
    ...:         "type": "confirm",
    ...:         "message": "Require 1 on 1?",
    ...:         "when": lambda result: result["proceed"],
    ...:     },
    ...:     {
    ...:         "type": "confirm",
    ...:         "message": "Confirm?",
    ...:         "when": lambda result: result.get(1, False),
    ...:     },
    ...: ]
    ...:
    ...: result = prompt(questions)
    ...: print(result)
    ...:
 ? Proceed? Yes
 ? Require 1 on 1? Yes
 ? Confirm? Yes
 {'proceed': True, 1: True, 2: True}
 
```

![](https://gyazo.com/aada2c5483c297dabe0ae4b845606bcc.png)

この例のように連続した質問では、 `when` で指定した質問の応答がTrueとなるときだけ質問するようにもできます。

## input タイプ
ユーザーにいくつかのテキスト値を入力させる入力プロンプトです。 `Ctrl-Space` もしくは TABキーを押下すると、 `completter` が与えられている場合は、自動コンプリートのポップアップが強制的に表示されます。

プロパティー: `type` ,  `name` ,  `message` ,,  `default` 、
 `[filter]` 、 `[transformer]` 、 `[validate]` 、 `[multiline]` 、 `[invalid_message]` 、

 `message` で与えた文字列をプロンプトとして表示し、ユーザから文字列の入力を受け付けます。
 `default` にはデフォルト値を与えることができます。
 `completer` には補完文字列を登録することができます。
 `filter` で与えた処理がユーザの入力に適用されて返されます。
 `validate` で与えた関数で入力値を検証することができます。
 `multiline` が  `True` のときは複数行の入力を許します。


```
 In [2]: # %load 011_input.py
    ...: from prompt_toolkit.validation import Validator, ValidationError
    ...: from pprint import pprint
    ...: from InquirerPy import prompt
    ...:
    ...: class AgeValidator(Validator):
    ...:     def validate(self, document):
    ...:         if int(document.text) < 18:
    ...:             raise ValidationError(
    ...:                 message='Too yound.',
    ...:                 cursor_position=len(document.text))  # Move cursor to en
    ...: d
    ...:
    ...: questions = [
    ...:   {
    ...:     'type': 'input',
    ...:     'name': 'first_name',
    ...:     'message': "What's your first name ?",
    ...:   },
    ...:   {
    ...:     'type': 'input',
    ...:     'name': 'last_name',
    ...:     'message': "What's your last name ?",
    ...:     'default': lambda ans: 'Bauer' if ans['first_name'] == 'Jack' else '
    ...: ',
    ...:   },
    ...:   {
    ...:     'type': 'input',
    ...:     'name': 'age',
    ...:     'message': "How old are you ?",
    ...:     'validate': AgeValidator()
    ...:   }
    ...: ]
    ...: result = prompt(questions)
    ...: pprint(result)
    ...:
 ? What's your first name ? Jack
 ? What's your last name ? Bauer
 ? How old are you ? 12
 Too yound.
 
```

![](https://gyazo.com/2eba2e0bd3d0cf17ab8160836c34eca2.png)


## passwrd タイプ
ユーザーにパスワードなどの秘密の値を入力させるための入力プロンプトです。inputタイプと似ていますがユーザが入力した文字列は画面には表示されません。



プロパティー: `type` ,  `name` ,  `message` ,   `[default, filter, validate]` 

 `message` で与えた文字列をプロンプトとして表示し、ユーザから文字列の入力を受け付けます。
 `default` にはデフォルト値を与えることができます。
 `filter` で与えた処理がユーザの入力に適用されて返されます。
 `validate` で与えた関数で入力値を検証することができます。


```
 In [2]: # %load 012_password.py
    ...: from InquirerPy import prompt
    ...: from InquirerPy.validator import PasswordValidator
    ...:
    ...: original_password = "P@ssw0rd123"
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "password",
    ...:         "message": "Old password:",
    ...:         "transformer": lambda _: "[hidden]",
    ...:         "validate": lambda text: text == original_password,
    ...:         "invalid_message": "Wrong password",
    ...:     },
    ...:     {
    ...:         "type": "password",
    ...:         "message": "New password:",
    ...:         "name": "new_password",
    ...:         "validate": PasswordValidator(
    ...:             length=8, cap=True, special=True, number=True
    ...:         ),
    ...:         "transformer": lambda _: "[hidden]",
    ...:     },
    ...:     {"type": "confirm", "message": "Confirm?", "default": True},
    ...: ]
    ...:
    ...: result = prompt(questions)
    ...: print(result)
    ...:
    
 ? Old password: ********
 Wrong password
 
 ? Old password: [hidden]
 ? New password:
 
 ? Old password: [hidden]
 ? New password: ***
 Input is not a valid pattern
 
 ? Old password: [hidden]
 ? New password: ***********
 Input is not a valid pattern
 
 ? Old password: [hidden]
 ? New password: [hidden]
 ? Confirm? Yes
 {0: 'P@ssw0rd123', 'new_password': 'Python@Osaka777', 2: True}
 
```


![](https://gyazo.com/5501e88d390684a052f70c6701a534d3.png)
![](https://gyazo.com/89b6f98d12db4198dd71ee880c01db8c.png)

### filepath タイプ
ファイルパスの補完機能があらかじめ組み込まれた入力プロンプト。


```
 In [3]: # %load 013_filepath.py
    ...: from pathlib import Path
    ...: from InquirerPy import prompt
    ...: from InquirerPy.validator import PathValidator
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "filepath",
    ...:         "message": "Enter file to upload:",
    ...:         "name": "location",
    ...:         "default": str(Path('/tmp')),
    ...:         "validate": PathValidator(is_file=True, message="Input is not a
    ...: file"),
    ...:         "only_files": True,
    ...:     },
    ...:     {
    ...:         "type": "filepath",
    ...:         "message": "Enter path to download:",
    ...:         "validate": PathValidator(is_dir=True, message="Input is not a d
    ...: irectory"),
    ...:         "name": "destination",
    ...:         "only_directories": True,
    ...:     },
    ...: ]
    ...:
    ...: result = prompt(questions)
    ...: print(result)
    ...:
 ? Enter file to upload: /tmp/d
                                dummyfile
 
 ?  Enter file to upload: /tmp/junk
 Input is not a file    
 
 ? Enter file to upload: /tmp/dummyfile
 ? Enter path to download: /tmp
 {'location': '/tmp/dummyfile', 'destination': '/tmp'}
                            
```


![](https://gyazo.com/af1a414e6376c675f5f7761a76ebfcb9.png)


### Fuzzy タイプ
入寮文字列のあいまい検索機能を持つリストプロンプトです。選択肢の数が約300kに達するまでは比較的良好な性能を発揮します。


```
 In [@]: # %load 014_fuzzy.py
    ...: from contextlib import ExitStack
    ...: from pathlib import Path
    ...: from InquirerPy import inquirer, prompt
    ...:
    ...: def get_choices(_):
    ...:    p = Path.cwd().joinpath("sample.txt")
    ...:    choices = []
    ...:
    ...:     with ExitStack() as stack:
    ...:         if not p.exists():
    ...:             file = stack.enter_context(p.open("w+"))
    ...:             sample = stack.enter_context(
    ...:                 urllib.request.urlopen(
    ...:                     "https://assets.kazhala.me/InquirerPy/sample.txt"
    ...:                 )
    ...:             )
    ...:             file.write(sample.read().decode())
    ...:             file.seek(0, 0)
    ...:         else:
    ...:             file = stack.enter_context(p.open("r"))
    ...:         for line in file.readlines():
    ...:             choices.append(line[:-1])
    ...:     return choices
    ...:
    ...:
    ...: questions = [
    ...:     {
    ...:         "type": "fuzzy",
    ...:         "message": "Select actions:",
    ...:         "choices": ["hello", "weather", "what", "whoa", "hey", "yo"],
    ...:         "default": "he",
    ...:         "max_height": "70%",
    ...:     },
    ...:     {
    ...:         "type": "fuzzy",
    ...:         "message": "Select preferred words:",
    ...:         "choices": get_choices,
    ...:         "multiselect": True,
    ...:         "validate": lambda result: len(result) > 1,
    ...:         "invalid_message": "minimum 2 selection",
    ...:         "max_height": "70%",
    ...:     },
    ...: ]
    ...:
    ...: result = prompt(questions=questions)
    ...: print(result)
    ...:
 ? Select actions:
 ┌──────────────────────────────────────────────────────────────────────────────┐
 │❯ he  3/6                                                                     │
 │❯ hey                                                                         │
 │  hello                                                                       │
 │  weather                                                                     │
 │                                                                              │
 │                                                                              │
 │                                                                              │
 └──────────────────────────────────────────────────────────────────────────────┘
 
 ? Select actions: hey
 ? Select preferred words: ['AA', 'BA']
 {0: 'hey', 1: ['AA', 'BA']}
 
```

![](https://gyazo.com/d3333818e61e36a9a9d1fd968da413af.png)


### キーバインド
 `keybindings` でキーバインドを定義することができます。
デフォルトのキーバインドは次のように定義されています。


```
 {
     "down": [
         {"key": "down"},
         {"key": "c-n", "filter": ~self._is_vim_edit},
         {"key": "j", "filter": self._is_vim_edit},
     ],
     "up": [
         {"key": "up"},
         {"key": "c-p", "filter": ~self._is_vim_edit},
         {"key": "k", "filter": self._is_vim_edit},
     ],
     "toggle": [
         {"key": "space"},
     ],
     "toggle-down": [
         {"key": Keys.Tab},
     ],
     "toggle-up": [
         {"key": Keys.BackTab},
     ],
     "toggle-all": [
         {"key": "alt-r"},
     ],
     "toggle-all-true": [
         {"key": "alt-a"},
     ],
     "toggle-all-false": [],
 }
```

 `Ctrl+n` でカーソルキーの下キー、 `Ctrl+p` でカーソルキーの上キーと同じ動作になります。
 `prompt()` の引数に `vi_mode=True` を与えるとキーバインドが vi コマンドと同様に、 `j` でカーソルキーの下キー、 `k` でカーソルキーの上キーと同じ動作になります。
変更したい場合は、 `prompt()` にキーワード引数　 `keybinding=` に辞書を与えます。
 `raise_keyboard_interrupt=False` を与えると、キーボードからの  `Ctrl-C` 割り込みを無視するようになります。

 キーバインドの表記方法

| キー | 表記 |
|:--|:--|
| Escape | escape |
| Arrows | left, right, up, down |
| Navigation | home, end, delete, pageup, pagedown, insert |
| Control+lowercase | c-a, c-b ... c-y, c-z |
| Control+uppercase | c-A, c-B ... c-Y, c-Z |
| Control + arrow | c-left, c-right, c-up, c-down |
| Other control keys | c-@, c-\, c-], c-^, c-\_, c-delete |
| Shift + arrow | s-left, s-right, s-up, s-down |
| Other shift keys | s-delete, s-tab |
| F-keys | f1, f2, .... f23, f24 |
| Alt+lowercase | alt-a, alt-b ... alt-y, alt-z |
| Alt+uppercase | alt-A, alt-B ... alt-Y, alt-Z |

 キーバインドでの表記

| Backspace | c-h |
|:--|:--|
| control+space | c-@ |
| Enter | c-m |
| Tab | c-i |

## スタイル
スタイルをカスタマイズする場合、辞書でスタイルを定義して、 `style_from_dict()` に渡したオブジェクトを `prompt()` の `style` キーワードに与えます。
 custom_style.py
```
 from InquirerPy import prompt, style_from_dict
 
 custom_style_1 = style_from_dict({
     "separator": '#cc5454',
     "questionmark": '#673ab7 bold',
     "selected": '#cc5454',  # default
     "pointer": '#673ab7 bold',
     "instruction": '',  # default
    "answer": '#f44336 bold',
     "question": '',
 })
 # ... （中略)
 answers = prompt(questions, style=custom_style_1)
```

## 新しいAPI

inquirerpy では、オリジナルの PyInquirer とは異なる、よりシンプルなAPIを提供しています。
これまで例示したサンプルコードのファイル名に合わせています。

- 互換API： `001_singple_input.py` 
- 新しいAPI： `101_single_input.py` 

PyInquirer との互換APIでは、辞書で定義した質問を `prompt()` に合わえていました。
新しいAPIでは、 `Inquirer()` でマップされる各UIクラスを使用します。

 `site-packages/InquirePy/resolver.py ` からの抜粋


```
 from InquirerPy.prompts.checkbox import CheckboxPrompt
 from InquirerPy.prompts.confirm import ConfirmPrompt
 from InquirerPy.prompts.expand import ExpandPrompt
 from InquirerPy.prompts.filepath import FilePathPrompt
 from InquirerPy.prompts.fuzzy import FuzzyPrompt
 from InquirerPy.prompts.input import InputPrompt
 from InquirerPy.prompts.list import ListPrompt
 from InquirerPy.prompts.rawlist import RawlistPrompt
 from InquirerPy.prompts.secret import SecretPrompt
 
 uestion_mapping = {
     "confirm": ConfirmPrompt,
     "filepath": FilePathPrompt,
     "password": SecretPrompt,
     "input": InputPrompt,
     "list": ListPrompt,
     "checkbox": CheckboxPrompt,
     "rawlist": RawlistPrompt,
     "expand": ExpandPrompt,
     "fuzzy": FuzzyPrompt,
 }
 
 list_prompts = {"list", "checkbox", "rawlist", "expand", "fuzzy"}
```

 互換APIのタイプと新しいAPIのメソッドとの比較

| 互換API | 新しいAPI | UIの説明 |
|:--|:--|:--|
| input | text() | ユーザから文字列を受け取る |
| list | select() | 選択肢を表示してユーザに選ばせる |
| rawlist | rawlist() | 選択肢を番号付きで表示してユーザに番号を選ばせる |
| expand | expand() | 選択肢を始めはコンパクトに表示し、キーアクションで展開して選ばせる |
| checkbox | checkbox() | 選択肢をチェックボックスで表示し、ユーザの選択をリストで返す |
| confirm | confirm() | ユーザにYES/NOの確認を行う |
| password | secret() | input/text() と同じですが、ユーザの入力文字列は表示されない |
| filepath | filepath() | ファイルパスの補完機能があらかじめ組み込まれたUI |
| fuzzy | fuzzy() | ユーザの入力を元にあいまい検索の機能を持つUI |


新しいAPIのクラスをエイリアスでインポートしています。
site-packages/Inquirerpy/inquirer.py から抜粋

python
```
 from InquirerPy.prompts import CheckboxPrompt as checkbox
 from InquirerPy.prompts import ConfirmPrompt as confirm
 from InquirerPy.prompts import ExpandPrompt as expand
 from InquirerPy.prompts import FilePathPrompt as filepath
 from InquirerPy.prompts import FuzzyPrompt as fuzzy
 from InquirerPy.prompts import InputPrompt as text
 from InquirerPy.prompts import ListPrompt as select
 from InquirerPy.prompts import RawlistPrompt as rawlist
 from InquirerPy.prompts import SecretPrompt as secret
```

ユーザから文字列を受け取る簡単な例から見てみましょう。


```
 In [2]: # %load 101_single_input.py
    ...: from InquirerPy import inquirer
    ...:
    ...: name = inquirer.text(message="What's your name: ").execute()
    ...: print(name)
    ...:
 ? What's your name:  Jack
 Jack
 
```

このケースでは、互換APIでは、 `prompt()` に与える辞書の質問のタイプとして  `input` を使用しますが、新しいAPIでは、
 `itext()` メソッドを使用します。名前が異なるので混乱するかもしれませんので、注意してください。

連続する質問は、互換APIでは質問の辞書をリストで与えますが、新しいAPIでは質問は独立しているため、
都度 `Inquirer` クラスのメソッドを呼び出します。


```
 In [2]: # %load 102_multiple_input.py
    ...: from InquirerPy import inquirer
    ...:
    ...: first_name = inquirer.text(
    ...:                       message="What's your first name: ").execute()
    ...: if first_name != '':
    ...:     last_name = inquirer.text(
    ...:                           message="What's your last name: ").execute()
    ...: else:
    ...:     last_name = ''
    ...: print(first_name, last_name)
    ...:
 ? What's your first name:  Jack
 ? What's your last name:  Bauer
 Jack Bauer
 
```


### 入力補完
ユーザから文字列を受け取るときに、予め登録した文字列に部分合致すると補完文字列をポップアップ表示します。
タブキーを押下すると残りの入力を補完したデータを返します。


```
 In [2]: # %load 103_completion.py
    ...: from InquirerPy import inquirer
    ...:
    ...: answer = inquirer.text(
    ...:         message="Which company would you like to apply:",
    ...:         completer={
    ...:             "Google": None,
    ...:             "Facebook": None,
    ...:             "Amazon": None,
    ...:             "Netflix": None,
    ...:             "Apple": None,
    ...:             "Microsoft": None,
    ...:         },
    ...:         multicolumn_complete=True,
    ...:     ).execute()
    ...:
    ...: print(answer)
    ...:
 ? Which company would you like to apply: A
                                            Amazon
                                            Apple
 
 ? Which company would you like to apply: Amazon
 Amazon
                                            
```


### transformer, filter, validate
ユーザの入力を加工したり、結果を変換したり、データ検証を行わせることができます。


```
 In [2]: # %load 104_validation.py
    ...: from InquirerPy import inquirer
    ...: from InquirerPy.validator import NumberValidator
    ...:
    ...: answer = inquirer.text(
    ...:         message="What's your salary expectation(k):",
    ...:         transformer=lambda result: "%sk" % result,
    ...:         filter=lambda result: int(result) * 1000,
    ...:         validate=NumberValidator(),
    ...: ).execute()
    ...:
    ...: print(answer)
    ...:
 ? What's your salary expectation(k): 2000k
 2000000
 
 In [3]: %run 104_validation.py
 ? What's your salary expectation(k): 1500万円
 Input should be number
 
```




## ListPrompt()
選択肢を表示してユーザに選ばせる基本的なUIです。


```
 class ListPrompt(BaseListPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         choices: Union[Callable[[SessionResult], List[Any]], List[Any]],
         default: Any = None,
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         qmark: str = "?",
         pointer: str = INQUIRERPY_POINTER_SEQUENCE,
         instruction: str = "",
         transformer: Callable[[Any], Any] = None,
         filter: Callable[[Any], Any] = None,
         height: Union[int, str] = None,
         max_height: Union[int, str] = None,
         multiselect: bool = False,
         marker: str = INQUIRERPY_POINTER_SEQUENCE,
         validate: Union[Callable[[Any], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         keybindings: Dict[str, List[Dict[str, Any]]] = None,
         show_cursor: bool = True,
     ) -> None:
```



```
 In [2]: # %load 105_list_simple.py
    ...: from InquirerPy import inquirer
    ...: from InquirerPy.separator import Separator
    ...:
    ...: action = inquirer.select(
    ...:        message="Select an action:",
    ...:        choices=["Upload", "Download", {"name": "Exit", "value": None}],
    ...:        default=None,
    ...:        # multiselect=True,
    ...: ).execute()
    ...:
    ...: print(action)
    ...:
 ? Select an action:
   Upload
   Download
 ❯ Exit
 
 ? Select an action: Upload
 Upload
 
```


### Separator
 `Separator` クラスのインスタンスオブジェクトを与えると、一覧するリストに区切り文字を表示するようになります。


```
 In [2]: # %load 106_list_separator.py
    ...: from InquirerPy import inquirer
    ...: from InquirerPy.separator import Separator
    ...:
    ...: region = inquirer.select(
    ...:             message="Select regions:",
    ...:             choices=[
    ...:                 {"name": "Sydney", "value": "ap-southeast-2"},
    ...:                 {"name": "Singapore", "value": "ap-southeast-1"},
    ...:                 Separator(),
    ...:                 "us-east-1",
    ...:                 Separator(line='*' * 15),
    ...:                 "us-east-2",
    ...:             ],
    ...:             multiselect=True,
    ...:             transformer=lambda result: "%s region%s selected"
    ...:             % (len(result), "s" if len(result) > 1 else ""),
    ...:         ).execute()
    ...:
    ...: print(region)
    ...:
 ? Select regions:
 ❯ Sydney
   Singapore
   ---------------
   us-east-1
   ***************
   us-east-2
 
 ? Select regions: 2 regions selected
 ['ap-southeast-2', 'ap-southeast-1']
   
```



## RawlistPrompt()
自動的に数字のショートカットを適用させたリストプロンプトです。
各選択肢の前には数字が付加されます。この数字をショートカットキーとして使用して選択肢にジャンプしたり、通常の上下キーバインドで移動したりすることができます。


```
 class RawlistPrompt(BaseListPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         choices: Union[Callable[[SessionResult], List[Any]], List[Any]],
         default: Any = None,
         separator: str = ")",
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         qmark: str = "?",
         pointer: str = " ",
         instruction: str = "",
         transformer: Callable[[Any], Any] = None,
         filter: Callable[[Any], Any] = None,
         height: Union[int, str] = None,
         max_height: Union[int, str] = None,
         multiselect: bool = False,
         marker: str = INQUIRERPY_POINTER_SEQUENCE,
         validate: Union[Callable[[Any], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         keybindings: Dict[str, List[Dict[str, Any]]] = None,
         show_cursor: bool = True,
     ) -> None:
     
```




```
 In [2]: # %load 107_rawlist.py
    ...: from InquirerPy import inquirer
    ...:
    ...: fruit = inquirer.rawlist(
    ...:     message="Pick your favourites:",
    ...:     choices=[
    ...:         "Apple",
    ...:         "Orange",
    ...:         "Peach",
    ...:         "Cherry",
    ...:         "Melon",
    ...:         "Strawberry",
    ...:         "Grapes",
    ...:     ],
    ...:     default=3,
    ...:     multiselect=True,
    ...:     transformer=lambda result: ", ".join(result),
    ...:     validate=lambda result: len(result) > 1,
    ...:     invalid_message="Minimum 2 selections",
    ...: ).execute()
    ...:
    ...: print(fruit)
    ...:
 ? Pick your favourites: 3
   1) Apple
   2) Orange
  ❯3) Peach
   4) Cherry
   5) Melon
   6) Strawberry
   7) Grapes
 
 Minimum 2 selections
 
 ? Pick your favourites: Apple, Peach
 ['Apple', 'Peach']
 
```


## ExpandPrompt()
コンパクト(compact)と拡張(expand)の2種類のUIを持つリストプロンプトです。
はじめはコンパクトな状態で表示されますが、 `h` キーを使って拡張することができます。展開後は、通常のリストナビゲーションキーが有効になります。


```
 class ExpandPrompt(BaseListPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         choices: Union[Callable[[SessionResult], List[Any]], List[Any]],
         default: Any = "",
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         qmark: str = "?",
         pointer: str = " ",
         separator: str = ")",
         help_msg: str = "Help, list all choices",
         expand_pointer: str = INQUIRERPY_POINTER_SEQUENCE,
         instruction: str = "",
         transformer: Callable[[Any], Any] = None,
         filter: Callable[[Any], Any] = None,
         height: Union[int, str] = None,
         max_height: Union[int, str] = None,
         multiselect: bool = False,
         marker: str = INQUIRERPY_POINTER_SEQUENCE,
         validate: Union[Callable[[Any], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         keybindings: Dict[str, List[Dict[str, Any]]] = None,
         show_cursor: bool = True,
     ) -> None:
 
```




```
 In [2]: # %load 108_exapnd.py
    ...: from InquirerPy import inquirer
    ...:
    ...: fruits_choice = [
    ...:         {"key": "a", "name": "Apple", "value": "Apple"},
    ...:         {"key": "c", "name": "Cherry", "value": "Cherry"},
    ...:         {"key": "o", "name": "Orange", "value": "Orange"},
    ...:         {"key": "p", "name": "Peach", "value": "Peach"},
    ...:         {"key": "m", "name": "Melon", "value": "Melon"},
    ...:         {"key": "s", "name": "Strawberry", "value": "Strawberry"},
    ...:         {"key": "g", "name": "Grapes", "value": "Grapes"},
    ...:     ]
    ...:
    ...: fruit = inquirer.expand(
    ...:         message="Pick your favourite:",
    ...:         choices=fruits_choice,
    ...:         default="o"
    ...:     ).execute()
    ...:
    ...: print(fruit)
    ...:
 ? Pick your favourite: (acopmsgh) o
 ❯ Orange
 
 ? Pick your favourite: (acopmsgh) a
   a) Apple
   c) Cherry
   o) Orange
   p) Peach
   m) Melon
   s) Strawberry
   g) Grapes
   h) Help, list all choices
 
 ? Pick your favourite: Apple
 Apple
 
```


## CheckboxPrompt()
チェックボックスを表示するリストプロンプト。

マルチセレクトが可能な他のリストプロンプトでは、最小選択数は常に1です（ユーザが何も選択しない場合、現在のハイライトされた選択肢が選択されます）。チェックボックスプロンプトでは、現在のハイライトされた選択肢は自動的に選択されません。


```
 class CheckboxPrompt(BaseListPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         choices: Union[Callable[[SessionResult], List[Any]], List[Any]],
         default: Any = None,
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         qmark: str = "?",
         pointer: str = INQUIRERPY_POINTER_SEQUENCE,
         enabled_symbol: str = INQUIRERPY_FILL_HEX_SEQUENCE,
         disabled_symbol: str = INQUIRERPY_EMPTY_HEX_SEQUENCE,
         instruction: str = "",
         transformer: Callable[[Any], Any] = None,
         filter: Callable[[Any], Any] = None,
         height: Union[int, str] = None,
         max_height: Union[int, str] = None,
         validate: Union[Callable[[Any], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         keybindings: Dict[str, List[Dict[str, Any]]] = None,
         show_cursor: bool = True,
     ) -> None:
     
```


```
 In [2]: # %load 109_checkbox.py
    ...: from InquirerPy import inquirer
    ...: from InquirerPy.separator import Separator
    ...:
    ...: region_choice = [
    ...:     Separator(),
    ...:     {"name": "Sydney", "value": "ap-southeast-2", "enabled": False},
    ...:     {"name": "Singapore", "value": "ap-southeast-1", "enabled": True},
    ...:     Separator(),
    ...:     "us-east-1",
    ...:     "us-west-1",
    ...:     Separator(),
    ...: ]
    ...:
    ...: regions = inquirer.checkbox(
    ...:     message="Select regions:",
    ...:     choices=region_choice,
    ...:     cycle=False,
    ...:     transformer=lambda result: "%s region%s selected"
    ...:     % (len(result), "s" if len(result) > 1 else ""),
    ...: ).execute()
    ...: print(regions)
    ...:
 ? Select regions:
   ---------------
 ❯ ⬡ Sydney
   ⬢ Singapore
   ---------------
   ⬡ us-east-1
   ⬡ us-west-1
   ---------------
   
 ? Select regions: 2 regions selected
 ['ap-southeast-2', 'ap-southeast-1']
   
```

## ConfirmPrompt()
ユーザーの確認を取るためのプロンプトです。


```
 class ConfirmPrompt(BaseSimplePrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         style: InquirerPyStyle = None,
         default: Union[bool, Callable[[Dict[str, Any]], bool]] = False,
         qmark: str = "?",
         transformer: Callable[[bool], Any] = None,
         filter: Callable[[bool], Any] = None,
         **kwargs
     ) -> None:
     
```



```
 In [2]: # %load 110_confirm.py
    ...: from InquirerPy import inquirer
    ...:
    ...: proceed, service, confirm = False, False, False
    ...: proceed = inquirer.confirm(message="Proceed?", default=True).execute()
    ...: if proceed:
    ...:     service = inquirer.confirm(message="Require 1 on 1?").execute()
    ...: if service:
    ...:     confirm = inquirer.confirm(message="Confirm?").execute()
    ...:
    ...: print(f'proceed:{proceed}, service:{service}, confirm:{confirm}')
    ...:
 ? Proceed? Yes
 ? Require 1 on 1? Yes
 ? Confirm? No
 proceed:True, service:True, confirm:False
 
```


## InputPromot()
ユーザーにいくつかのテキスト値を入力させる入力プロンプトです。 `Ctrl-Space` もしくは TABキーを押下すると、 `completter` が与えられている場合は、自動コンプリートのポップアップが強制的に表示されます。


```
 class InputPrompt(BaseSimplePrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         default: Union[str, Callable[[SessionResult], str]] = "",
         qmark: str = "?",
         completer: Union[Dict[str, Optional[str]], Completer] = None,
         multicolumn_complete: bool = False,
         multiline: bool = False,
         validate: Union[Callable[[str], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         transformer: Callable[[str], Any] = None,
         filter: Callable[[str], Any] = None,
         **kwargs,
     ) -> None:
 
```



```
 In [2]: # %load 111_input.py
    ...: from prompt_toolkit.validation import Validator, ValidationError
    ...: from InquirerPy import inquirer
    ...:
    ...: class AgeValidator(Validator):
    ...:     def validate(self, document):
    ...:         if int(document.text) < 18:
    ...:             raise ValidationError(
    ...:                 message='Too yound.',
    ...:                 cursor_position=len(document.text))  # Move cursor to en
    ...: d
    ...:
    ...: first_name = inquirer.text(message="Waht's your first name?").execute()
    ...:
    ...: default_name = 'Bauer' if first_name == 'Jack' else ''
    ...: last_name = inquirer.text(message="What's your last name?",
    ...:                         default=default_name).execute()
    ...: age = inquirer.text(message="How old are you?",
    ...:                         validate=AgeValidator()).execute()
    ...:
    ...:
    ...: print(f'first_name: {first_name}, last_name: {last_name}, age: {age}')
    ...:
 ? Waht's your first name? Jack
 ? What's your last name? Bauer
 ? How old are you? 11
 Too yound.
 
 ? Waht's your first name? Jack
 ? What's your last name? Bauer
 ? How old are you? 19
 first_name: Jack, last_name: Bauer, age: 19
 
```

## SecretPrompt()
ユーザーにパスワードなどの秘密の値を入力させるための入力プロンプトです。inputタイプと似ていますがユーザが入力した文字列は画面には表示されません。


```
 class SecretPrompt(InputPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         style: InquirerPyStyle = None,
         default: Union[str, Callable[[SessionResult], str]] = "",
         qmark: str = "?",
         vi_mode: bool = False,
         validate: Union[Validator, Callable[[str], bool]] = None,
         invalid_message: str = "Invalid input",
         transformer: Callable[[str], Any] = None,
         filter: Callable[[str], Any] = None,
         **kwargs
     ) -> None:
     
```



```
 In [2]: # %load 112_password.py
    ...: from InquirerPy import inquirer
    ...: from InquirerPy.validator import PasswordValidator
    ...:
    ...: original_password = "P@ssw0rd123"
    ...:
    ...: old_password = inquirer.secret(
    ...:     message="Old password:",
    ...:     transformer=lambda _: "[hidden]",
    ...:     validate=lambda text: text == original_password,
    ...:     invalid_message="Wrong password",
    ...: ).execute()
    ...:
    ...: new_password = inquirer.secret(
    ...:     message="New password:",
    ...:     validate=PasswordValidator(length=8, cap=True, special=True, number=
    ...: True),
    ...:     transformer=lambda _: "[hidden]",
    ...: ).execute()
    ...:
    ...: confirm = inquirer.confirm(message="Confirm?", default=True).execute()
    ...:
    ...: msg = f'old_password: {old_password}, '
    ...: msg += f'new_password: {new_password}, '
    ...: msg += f'confirm: {confirm}'
    ...: print(f'{msg}')
    ...:
 ? Old password: *******
 Wrong password
 
 ? Old password: [hidden]
 ? New password: ***
 Input is not a valid pattern
 
 ? Old password: [hidden]
 ? New password: [hidden]
 ? Confirm? Yes
 old_password: P@ssw0rd123, new_password: Python@Osaka123, confirm: True
 
```


### FilePathPrompt()

python
```
 class FuzzyPrompt(BaseComplexPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         choices: Union[Callable[[SessionResult], List[Any]], List[Any]],
         default: Union[str, Callable[[SessionResult], str]] = "",
         pointer: str = INQUIRERPY_POINTER_SEQUENCE,
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         qmark: str = "?",
         transformer: Callable[[Any], Any] = None,
         filter: Callable[[Any], Any] = None,
         instruction: str = "",
         multiselect: bool = False,
         prompt: str = INQUIRERPY_POINTER_SEQUENCE,
         marker: str = INQUIRERPY_POINTER_SEQUENCE,
         border: bool = True,
         info: bool = True,
         height: Union[str, int] = None,
         max_height: Union[str, int] = None,
         validate: Union[Callable[[Any], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         keybindings: Dict[str, List[Dict[str, Any]]] = None,
     ) -> None:
```


 113_filepath.py
```
 from pathlib import Path
 from InquirerPy import inquirer
 from InquirerPy.validator import PathValidator
 
 src_path = inquirer.filepath(
     message="Enter file to upload:",
     default=str(Path('/tmp')),
     validate=PathValidator(is_file=True, message="Input is not a file"),
     only_files=True,
 ).execute()
 
 dest_path = inquirer.filepath(
     message="Enter path to download:",
     validate=PathValidator(is_dir=True, message="Input is not a directory"),
     only_directories=True,
 ).execute()
 
 print(f'src_path: {src_path}, dest_path: {dest_path}')
```


### FuzzyPrompt()
入寮文字列のあいまい検索機能を持つリストプロンプトです。選択肢の数が約300kに達するまでは比較的良好な性能を発揮します。


```
 class FuzzyPrompt(BaseComplexPrompt):
     def __init__(
         self,
         message: Union[str, Callable[[SessionResult], str]],
         choices: Union[Callable[[SessionResult], List[Any]], List[Any]],
         default: Union[str, Callable[[SessionResult], str]] = "",
         pointer: str = INQUIRERPY_POINTER_SEQUENCE,
         style: InquirerPyStyle = None,
         vi_mode: bool = False,
         qmark: str = "?",
         transformer: Callable[[Any], Any] = None,
         filter: Callable[[Any], Any] = None,
         instruction: str = "",
         multiselect: bool = False,
         prompt: str = INQUIRERPY_POINTER_SEQUENCE,
         marker: str = INQUIRERPY_POINTER_SEQUENCE,
         border: bool = True,
         info: bool = True,
         height: Union[str, int] = None,
         max_height: Union[str, int] = None,
         validate: Union[Callable[[Any], bool], Validator] = None,
         invalid_message: str = "Invalid input",
         keybindings: Dict[str, List[Dict[str, Any]]] = None,
     ) -> None:
 
```



```
 In [2]: # %load 114_fuzzy.py
    ...: from contextlib import ExitStack
    ...: from pathlib import Path
    ...:
    ...: from InquirerPy import inquirer, prompt
    ...:
    ...: _WORDFILE_ = 'sample.txt'
    ...: def get_choices(_):
    ...:     p = Path.cwd().joinpath(_WORDFILE_)
    ...:     choices = []
    ...:
    ...:     with ExitStack() as stack:
    ...:         if not p.exists():
    ...:             raise Exception('%s: wordfile missing!', _WORDFILE_)
    ...:         else:
    ...:             file = stack.enter_context(p.open("r"))
    ...:         for line in file.readlines():
    ...:             choices.append(line[:-1])
    ...:     return choices
    ...:
    ...: action = inquirer.fuzzy(
    ...:     message="Select actions:",
    ...:     choices=["hello", "weather", "what", "whoa", "hey", "yo"],
    ...:     default="he",
    ...:     max_height="70%",
    ...: ).execute()
    ...:
    ...: words = inquirer.fuzzy(
    ...:     message="Select preferred words:",
    ...:     choices=get_choices,
    ...:     multiselect=True,
    ...:     validate=lambda result: len(result) > 1,
    ...:     invalid_message="minimum 2 selections",
    ...:     max_height="70%",
    ...: ).execute()
    ...:
    ...: print(f'action: {action}, words: {words}')
    ...:
 ? Select actions:
 ┌──────────────────────────────────────────────────────────────────────────────┐
 │❯ he  3/6                                                                     │
 │❯ hey                                                                         │
 │  hello                                                                       │
 │  weather                                                                     │
 │                                                                              │
 │                                                                              │
 │                                                                              │
 └──────────────────────────────────────────────────────────────────────────────┘
 
 ? Select actions: hey
 ? Select preferred words:
 ┌──────────────────────────────────────────────────────────────────────────────┐
 │❯   100000/100000 (0)                                                         │
 │❯ AA                                                                          │
 │  AAH                                                                         │
 │  AAHED                                                                       │
 │  AAHING                                                                      │
 │  AAHS                                                                        │
 │  AAL                                                                         │
 │  AALII                                                                       │
 │  AALIIS                                                                      │
 
 ? Select actions: hey
 ? Select preferred words: ['AA', 'AAH']
 action: hey, words: ['AA', 'AAH']
 
 
```


## PyInquirer との非互換について

InquierPy と PyInquirer とで互換性のないものについて説明します。

#### editorプロンプト
inquirerpy は今時点では、editorプロンプトをサポートしていません。

#### checkboxプロンプトのAPI
CheckBoxPrompt()のパラメタ名が異なっています。

 CheckboxPrompt()のパラメタ

| PyInquirer | InquirerPy |
|:--|:--|
| pointer_sign | pointer |
| selected_sign | enabled_symbol |
| unselected_sign | disabled_symbol |

#### Syle

PyInquirerのスタイルのキーのうち次のものは名前が変わっています。


 style のキー

| PyInquirer | InquirerPy |
|:--|:--|
| selected | pointer |

色やスタイルなどのカスタマイズはprompt_toolkit のスタイルを利用して行います。

## まとめ

 `editor` など複数行入力などのインタフェースを使いたい場合は prompt_toolkit を使うことになるでしょう。
それでも、基本的な会話形インタフェースを構築するには十分な機能が提供されていて、個人的には見た目(Look&Feel) もシンプルで好感が持てます。

余談ですが、InquirerPy を使って[Emberblast　](https://github.com/felipemeriga/Emberblast)というクラシカルなRPGを作った人もいますね。

## 参考
- [inquirerpy ソースコード ](https://github.com/kazhala/InquirerPy)
- [inquirerpy ドキュメント ](https://github.com/kazhala/InquirerPy/wiki)
- [FELIPE RAMOS ON BUILDING A PYTHON RPG GAME ](https://x-team.com/blog/interview-felipe-ramos-da-silva/)
- [Emberblast  ](https://github.com/felipemeriga/Emberblast)



