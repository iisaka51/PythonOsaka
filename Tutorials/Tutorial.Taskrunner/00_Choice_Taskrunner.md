タスクランナーの選定
=================
##  タスクランナーとは
タスクランナーは、タスクをプログラム処理で自動化してくれるツールのことをいいます
。
いろいろな作業の中で出てくる単純作業を自動化することで次のような利点があります。

- 1. 作業の属人化を防ぐ
- 2. 人為的なミスを防ぐ
- 3. 作業の効率化と平準化ができる
- 4. 事前/事後でレビューができる
- 5. gitなどでバージョン管理を行える


## 代表的なタスクランナー

- Invoke
    - - ドキュメント: http://www.pyinvoke.org/
    - - ソースコード
    - - 記述言語: python
    - - 概要: 登録しているタスクを実行することができるタスクランナー
    - Python の関数としてタスクを定義し、デコレータで登録する
    - 依存関係を定義できる

- Fabric2
    - ドキュメント: http://www.fabfile.org/
    - ソースコード
    - 記述言語: python
    - 概要: 登録しているタスクを実行することができるタスクランナー
    - Python の関数としてタスクを定義し、デコレータで登録する
    - 依存関係を定義できる
    - リモートサーバで実行することができる。

* Doit
    - ドキュメント: https://pydoit.org/
    - ソースコード: https://github.com/pydoit/doit
    - 記述言語: python
    - 概要: マルチコアを有効に使用して並列にタスクを実行できる


- * Pypyr
    - ドキュメント: https://pypyr.io/
    - ソースコード: https://github.com/pypyr/pypyr
    - 記述言語: YAML
    - 概要: タスクをステップとよび、それらをパイプラインと呼ぶYAMLで定義
    - パイプラインにはループや条件分岐、依存関係を定義できる

- Ansible-taskrunner
    - - ドキュメント:
    - - ソースコード: https://github.com/berttejeda/ansible-taskrunner
    - - 記述言語: YAML
    - - 概要: ansibleの上位の自動化レイヤーとして機能するタスクランナー
    - ansible-playbook を想定していて、利用しやすくなる。
    - サーバーやネットワーク機器の構成管理を行う用途に向いている
    - コンパイルほかの開発工程での作業へ適用するにはかえって面倒になる。

- poethepoet
    - - ドキュメント:
    - - ソースコード https://github.com/nat-n/poethepoet
    - - 記述言語: python
    - - 概要: Poetly との相性が良いタスクランナー

- taskipy
      - - ソースコード: https://github.com/illBeRoy/taskipy
    - - 記述言語: TOML
    - - 概要:
    - - 概要: Poetly との相性が良いタスクランナー

## 時間条件によりタスクを実行するもの

- sched - Event Scheduler -  python library
    - - https://docs.python.org/3/library/sched.html
    - 概要：周期的に処理を行わせるためのライブラリ

- timeloop
    - - https://github.com/sankalpjonn/timeloop
      - 概要：周期的に処理を行わせるためのライブラリ
      - デコレータで定義するため既存コードへの提供が楽になる

- croniter
    - - https://github.com/kiorky/croniter
    - 概要：cron 互換の設定で処理を実行するもの

- scheduler-cron
    - - https://github.com/mehrdadmhd/scheduler-py
    - 概要：cron 互換の設定で処理を実行するもの

### 分散システム

- * Celery
    - - ドキュメント: https://docs.celeryproject.org/en/stable/index.html
    - - ソースコード: https://github.com/celery/celery
    - Celeryは、膨大な量のメッセージを処理するための、
    - シンプルで柔軟性と信頼性に優れた分散システムであり、
    - このようなシステムを維持するために必要なツールを運用側に提供します。
    - リアルタイム処理に特化したタスクキューであり、
    - タスクスケジューリングもサポートしています。

- * Dramatiq
    - - ドキュメント: https://dramatiq.io/
    - - ソースコード: https://github.com/Bogdanp/dramatiq
    - Dramatiqは、シンプルさ、信頼性、パフォーマンスを重視した
    - Python3 用のバックグラウンドタスク処理ライブラリです。

以後で、タスクランナーについて個別に説明することにします。


