# 演習５ クラス継承を使いこうなそう

## 演習5.1
pow() の機能を実現するメソッド `pow()` を持つクラス`POW`を定義してみましょう。


```
pow（x、n）
    pow() は２つの引数 x と n を受けとり、"x の n 乗" の結果を返す
```


* インスタンス作成時に２つの値(`x`,  `y`) を指定できるようにします

```
 	 obj=POW(2,2`
```

* メソッド`pow()`に値を指定でき、その値を保持できるようにします


```
  obj.pow(2,3); obj.pow()
```

* 呼び出し可能オブジェクトをサポートしましょう

```
 	obj(2,3)
    obj(2,4).pow()
```

* `pow(0, 負数)` のときは "cannot negative power" を表示しよう
* `POW`クラスを含むモジュール `POW` を作成しよう

## 演習5.2

メソッド `getString()` と `capString()` を持つクラス`StrKeeper`を作成しよう

*  `getString()` はユーザーの入力した文字列を返し、それをリストとして保持します
*  `capString()` は保持している文字列のリスト要素を大文字に変換したリストを返します
*  `StrKeeper`クラスを含むモジュール `StrKeeper` を作成しよう
 	ヒント: ユーザーの入力を処理する関数は`input()`です

## 演習5.3
矩形の面積を計算するメソッド`area()`を持つクラス`Rectangle`を作成しよう

* `StrKeep`クラスを継承して、ユーザからの入力を処理できるようにします
* インスタンス作成時に縦横の値(`length`と`width`)を受けることもできるようにします
* インスタンス作成時に引数が指定されなければユーザからの入力値で処理します
　	ヒント: `__init__()`メソッドが実行されるかどうかは...

## 演習5.4
円の面積を計算するメソッド`area()`を持つクラス`Circle`を作成しよう

 *　`StrKeep`クラスを継承して、ユーザからの入力を処理できるようにします
 *　インスタンス作成時に半径`radius`の値を受けることもできるようにします
 *　πの値として`3.141592653589793` を保持するアトリビュート `pi`を持ちます
 *　アトリビュート `pi` は外部から書き換えられないようにします
　	ヒント: プロパティーを利用すると...

## チャレンジ課題
### 演習5.5

* `StrKeeper`クラスを継承して、ユーザが入力した文字列を数値チェックして返す
  `validate()` メソッドを持つ`Validator`クラスを作成しよう

```
validate(val, valstr, prompt, retry, positive)
    val: 検証する値
    valsttr: val を表す文字列
    prompt:  val が None のときユーザから入力待ちで表示するプロンプトメッセージ
    positive:   True にすると負数は再度ユーザから入力待ちになる

    利用例:
      length = obj.validate(length, 'Length', 'Please input length',
                            retry=3, postive=True)
```

 * ユーザ入力文字列を`float()`で変換できなければ，再度入力待ちになるようにしよう
 *  `positive=True` のとき`retry`で指定した回数を超えると
    '{valstr} must be set positive value'  を表示しValueErrorとしましょう
 *  `positive=False` のとき`retry`で指定した回数を超えると
    'Too many retries'  を表示しValueErrorとしましょう

## 演習5.6

 * `Validator`クラスを継承して、`Rectangle`クラスで数値チェックをするように修正しよう

## 演習5.7

* `Validator`クラスを継承して、`Circle`クラスで数値チェックをするように修正しよう

