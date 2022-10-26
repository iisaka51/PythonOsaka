Pythonチュートリアル：日時処理
=================

![](https://github.com/iisaka51/PythonOsaka/blob/main/data/images/Python_Logo.png)

## 日時処理について

python で日時処理を行うためのライブラリには、まず 標準ライブラリの datetime があります。
これは、基本中の基本なのですが、使用するにとすぐに気づく煩雑さが問題となります。

 - time、datetime、dateutil、calendar、pytzなど、外部モジュールが多すぎる
 - datetime、date、time、timedelta、tzinfoなど、多くのデータ型から選択する必要が
ある
 - 異なるタイムゾーンを扱う経験が不足しているユーザには難しい
 - タイムスタンプとタイムゾーン変換の方法が非効率的
 - ヒューマナイゼーション(例：日付を人間が読める形式に変換)やISO 8601のパースな>どの機能が劣る。

datetime だけで処理できないことが多く、外部モジュールに依存することが多くなります。
例えば、datetime 型からエポックタイム(Unix時間）に変換したいときは、次のようなコードになります。

```
import time
import datetime

date = datetime.date(2022,2,2)
unixtime = time.mktime(date.timetuple())
```

これはコードの一貫性がなくなるためスマートとは言えず、また読みづらくなってしまいます。


こうしたことから、日時処理を行うためのライブラリがいろいろ開発されています。

- [Dateutil ](https://dateutil.readthedocs.io/en/stable/index.html)：datetimeモジュールの拡張機能を提供します。
- [Pendulum ](https://pendulum.eustace.io/)：日時処理やタイムゾーン処理を簡単にするためのライブラリ
- [Delorean ](https://delorean.readthedocs.io/en/latest/)：日時処理やタイムゾーン処理を簡単にするためのライブラリ
- [Zulu ](https://zulu.readthedocs.io/en/latest/)：日時処理やタイムゾーン処理を簡単にするためのライブラリ
- [humanize ](https://github.com/jmoiron/humanize)：数字を人に優しい表現 ("3 minutes ago") にするようなユーティリティ
- [Arrow ](https://github.com/crsmithdev/arrow)：人に優しい日時処理ライブラリ。
- [Maya ](https://github.com/kennethreitz/maya)：人に優しい日時処理ライブラリ。Humanize、pytz、pendulum など、Python でデータタイムを扱う人気のライブラリが含まれている。
- [Freezegun ](https://github.com/spulec/freezegun)：Freezegunは、Pythonコードの中で特定の日時を使ったテストを行うためのライブラリです

これらのライブラリは、日付や時刻の操作を簡単にするという点では共通していますが、それぞれ異なる機能を持っています。時間の操作が得意なものもあれば、解析が得意なものもあります。また、プロジェクトによっては軽量であることやパフォーマンスを重視することもあるでしょう。どれが自分のプロジェクトのニーズに合っているかを判断するのは難しいかもしれません。Mayaの開発者であるKenneth Reitz氏は、「これらのプロジェクトはすべて、お互いに補完し合う仲間です」と語っています。

それとともに、標準ライブラリの datetime は、積極的に他にライブラリに置き換えを
検討する必要があるということも覚えておくとよいでしょう。


## Python 標準ライブラリ
- [DateTimeで日時処理をしてみよう](01_Datetime/)

## 日時処理専用の拡張ライブラリ
- [dateutilを使って日時処理をしてみよう](02_Dateutil/)
- [pendulumを使って日時処理をしてみよう](03_Pendulum/)
- [deloreanを使って日時処理をしてみよう](04_Delorean/)
- [zuluを使って日時処理をしてみよう](05_Zulu/)
- [Arrowを使って日時処理をしてみよう](06_Arrow/)
- [Mayaを使って日時処理をしてみよう](07_Maya/)

## 日時処理も行える拡張ライブラリ
- [pandasでの日時処理](08_Pandas_Datetime/)

## テストで日時処理をうまう処理できるライブラリ
- [Freezegunでの日時処理](09_Freezegun/)

- [演習1：いろいろなライブラリで日時処理をしてみよう](Exercise_01/README.md)

