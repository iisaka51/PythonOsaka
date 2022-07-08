Pythonチュートリアル：日時処理
=================

![](https://gyazo.com/153a339305d78fc4fa4850753e4b1594.png)

## 日時処理について

python で日時処理を行うためのライブラリには、まず 標準ライブラリの datetime があります。
これは、基本中の基本なのですが、使用するにとすぐに気づく煩雑さが問題となります。
こうしたことから、いろいろなライブラリが公開されています。

- [Dateutil ](https://dateutil.readthedocs.io/en/stable/index.html)：datetimeモジュールの拡張機能を提供します。
- [Pendulum ](https://pendulum.eustace.io/)：日時処理やタイムゾーン処理を簡単にするためのライブラリ
- [Delorean ](https://delorean.readthedocs.io/en/latest/)：日時処理やタイムゾーン処理を簡単にするためのライブラリ
- [Zulu ](https://zulu.readthedocs.io/en/latest/)：日時処理やタイムゾーン処理を簡単にするためのライブラリ
- [humanize ](https://github.com/jmoiron/humanize)：数字を人に優しい表現 ("3 minutes ago") にするようなユーティリティ
- [Arrow ](https://github.com/crsmithdev/arrow)：人に優しい日時処理ライブラリ。
- [Maya ](https://github.com/kennethreitz/maya)：人に優しい日時処理ライブラリ。Humanize、pytz、pendulum など、Python でデータタイムを扱う人気のライブラリが含まれている。
- [Freezegun ](https://github.com/spulec/freezegun)：Freezegunは、Pythonコードの中で特定の日時を使ったテストを行うためのライブラリです

これらのライブラリは、日付や時刻の操作を簡単にするという点では共通していますが、それぞれ異なる機能を持っています。時間の操作が得意なものもあれば、解析が得意なものもあります。また、プロジェクトによっては軽量であることやパフォーマンスを重視することもあるでしょう。どれが自分のプロジェクトのニーズに合っているかを判断するのは難しいかもしれません。Mayaの開発者であるKenneth Reitz氏は、「これらのプロジェクトはすべて、お互いに補完し合う仲間です」と語っています。


## Python 標準ライブラリ
- [DateTimeで日時処理をしてみよう](01_Datetime/README.md)

## 日時処理専用の拡張ライブラリ
- [dateutilを使って日時処理をしてみよう](02_Dateutil/README.md)
- [pendulumを使って日時処理をしてみよう](03_Pendulum/README.md)
- [deloreanを使って日時処理をしてみよう](04_Delorean/README.md)
- [zuluを使って日時処理をしてみよう](05_Zulu/README.md)

## 日時処理も行える拡張ライブラリ
- [pandasでの日時処理](06_Pandas_Datetime/README.md)

- [演習1：いろいろなライブラリで日時処理をしてみよう](Exercise_01/README.md)

