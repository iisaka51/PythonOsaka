#テストで Freezegun を使ってみよう

## Freezegun について
[Freezegun](https://github.com/spulec/freezegun)は、Pythonのコードで特定の日付時刻を使ったテストを行うためのライブラリです。freeze_time デコレータを使用すると、テストケースに特定の日時を設定することができ、 datetime.datetime.now() や datetime.datetime.utcnow() などのすべての呼び出しは、指定した日時を返すようになります。

タイムゾーンをまたがるテストを行うには、デコレータに tz_offset 引数を渡します。freeze_time デコレータは、 @freeze_time('April 4, 2017') のような日常で使用されるような平易な形式の日付も扱えます。

