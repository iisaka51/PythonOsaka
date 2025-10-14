# Git/GitLab

最終更新日: 2025/02/14

## Omnibus GitLab

Omnibus GitLabはChefのOmnibusプロジェクトをカスタマイズしてフォークしたもので、  
CookbookやレシピのようなChefのコンポーネントを使い、ユーザーのコンピュータ上で
GitLabを設定するタスクを実行します。  
GitLab.comのOmnibus GitLabリポジトリは、Omnibus GitLabに
必要なすべてのコンポーネントをホストしています。
これらには、設定やプロジェクトメタデータのようなパッケージのビルドに必要なOmnibusの部分と、
インストール後にユーザーのコンピュータで使用されるChef関連のコンポーネントが含まれます。

Chef, Matthermost, Container Container Registory を含んだオープンソースで、
GitHub/CircleCI/Slack/Docker Hub/Datadogをまとめたようなものです。


- [Omnibus-gitlab](https://gitlab.com/gitlab-org/omnibus-gitlab)
- [Omnibus GitLab architecture and components](https://docs.gitlab.co.jp/omnibus/architecture/)
- [Omnibus GitLabアーキテクチャとコンポーネント](https://gitlab-docs.creationline.com/omnibus/architecture/)
- [Installing GitLab with Omnibus packages](https://docs.gitlab.co.jp/omnibus/installation/)
- [Upgrading GitLab](https://docs.gitlab.com/ee/update/)
- [hutchgrant/gitlab-docker-local](https://github.com/hutchgrant/gitlab-docker-local)


## インストール

- [GitLab をインストールしよう! (omnibus package)](https://qiita.com/masakura/items/0a0f00dfdddc8ce27f29)
- [Docker ComposeでGitLabを起動](https://qiita.com/str416yb/items/2932052a6ead78c167e4)
- [Ｗindows で ＷSL2 (Ubuntu) ＋ docker compose 環境構築](https://footloose-engineer.com/wsl2-ubuntu-docker-compose-setup/)
- [WSLでdockerのインストールからdocker-composeまで動かす](https://qiita.com/tettsu__/items/85c96850d187e4386c24)
- [Docker Compose を使用して Docker コンテナで GitLab を実行する](https://ja.linux-console.net/?p=20587)
- [docker-composeによる GitLabの実行と運用](https://qiita.com/Mr-K/items/e0d8f905946703767954)
- [Dockerを用いたGitLabサーバのオンプレミス構築](https://e-penguiner.com/gitlab-with-docker-onpremise/)
- [docker-compose でGitlabとGitlab-Runner構築](https://qiita.com/hakuchan/items/977764d99bf7a1463063)
- [オンプレサーバーで研究室・社内用のGitLab環境を構築する](https://qiita.com/hmkc1220/items/fdc9630078a2428b5a6b)
- [[WSL2対応]gitlabをdocker composeで動かす(gitlab container registry, gitlab pagesあり)](https://qiita.com/KO_YAmajun/items/b4e894f72697348e3beb)
- [WindowsでGitLabを構築(Docker)](https://gup.monster/entry/2020/04/13/023005)
- [WindowsでのDockerを使用したGitLabとGitLab Runnerの構築手順](https://developers-trash.com/archives/1536)
- [GitLabとGitLab runnerをDockerでセットアップ](https://qiita.com/ronkabu/items/9643e578c1e3b8ee3043)
- [Windows環境でGitLab for Dockerを立ち上げてみる](https://qiita.com/YoshijiGates/items/0ae87483bbf1c1904b8b)
- [Windows＋Docker(Compose)でGitlabをローカルに立ち上げた時の話](https://qiita.com/beeeegle/items/b8d8da113f272f61af44)
- [Docker(Docker-Compose)でGitlabを構築](https://qiita.com/piityan1126/items/c76c46ae2047a4259a9e)
- [Gitlab(17.2) docker compose で立ち上げる方法](https://qiita.com/KO_YAmajun/items/1a511a3378a67358bb04)
- [ポートを振り分けてRedmine/Gitlabを1つのマシンで構築](https://qiita.com/loverboy/items/094c2de0f8c3e7e9a2b3)
- [【Gitlab】gitlab-runnerを構築してCI/CDを動かす](https://qiita.com/rittan_girla/items/00827de6d098eff5db3b)


## ログイン認証をキャッシュさせる

GitLab へアクセスするとき毎回パスワードを聞かれるのが面倒なときは、
次のように背っていしておくと１時間はパスワードをキャッシュしてくれます。

```
$ git config --global credential.helper 'cache --timeout=3600'
```

認証情報をファイルに格納したいときは次のようにします。

```
$ git config --global credential.helper store 
```

## 設定しておくと便利なエイリアス

次の設定を `~/.gitconfig` あるいは、レポジトリ内の `.git/config` 記述しておくと、
キータイプが少し楽になります。
シェルのエイリアスとは違い、ブランチ名などはタブキー補完ができるので便利です。

```
[alias]
  st = status
  co = checkout
  br = branch
  ft = fetch
  ll = log --oneline
  graphall = log --graph --all --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
```

## 経験からGit/GitLabで注意しとくべき項目

- `main` ブランチに直接コミットしない  
   本番環境で使用される認識でいること
   `develop` ブランチなどを作成しておき、
   `develop` をクローンしてから各自さらにブランチを作成するようにする

- コミットメッセージの変更は近く的面倒  
  冷静になってtypoに気をつけて行う
  直前のコミットメッセージの変更は比較的楽だけど...
- 小まめにコミット  
  あれやこれやと作業をしないこと
- 機能でまとめられるものは `rebase` する
  粒度が細かいとレビューが面倒になるため
- ブランチを積極的に使う  
  特定の機能、バグ修正、テストごとにブランチを使用
- `push` は慎重に  
  意図しないものをコミットしてしまったり、バグを含んでしまうことがあるため

`push` していない場合
```
$ git reset --hard <previous_commit_hash>
```

`push` 済みのコミットを取り消す場合

```
$ git revert <bad_commit_hash>
$ git commit -m "Revert changes from <bad_commit_hash>"
$ git push origin <BRANCH_NAME>
```

- マージコンフリクトが発生することがある　　
　マージされたブランチ間のコードの違いを自動的に解決できない場合に発生

```
$ git merge feature/new-feature
$ git add .
$ git commit -m "fix: resolve merge confilices"
$ git push origin <HRANCH_NAME>
```


## コミットテンプレートの使用

コミットメッセージにプレフィックス(prefix)と呼ばれる定型キーワードで始めるようにしておくと
次のようなメリットがあります。

- 機能をプレフィックスレベルで分割して作るようになる
- コミットが見やすくなる
- レビューしやすくなる
- コミットログを検索しやすくなる


機能をプレフィックスレベルで分割して開発を進めるようになり、
作業の進め方が良い方向に誘導されます。

例えば:

-「まずはライブラリを入れて (chore)」
- 「次にA機能のためのテスト書いて (test)」
- 「次にA機能を作って (feat)」
- 「最後にスタイル調整して (style)」

といったように、プレフィックスを意識しながら順序立てて機能を作成するようになり、
一つのコミットに詰め込みすぎたり、分割しすぎたりすることがなくなります。

プロジェクトディレクトリ(`$PROJECT_DIR`)  に
次のような `.commit_template` を作成します。

```


# 以下はフォーマットのサンプルです。コミット時に消しましょう。
# コメントは`#`ではじまる
# ==================== Format ====================
# type: Subject
#
# message body...
# コミットメッセージの1行目はサブジェクト、サブジェクトには絵文字を含んでもOK
# 2行目は空行
# 3行目以降にメッセージを記述
#
# ==== Prefix/Type ====
# :fix: バグ修正
# :hotfix: クリティカルなバグ修正
# :add: 新規機能・新規ファイル追加
# :feat: feature
# :update: バグではない機能修正
# :change: 仕様変更による機能修正
# :docs: ドキュメントのみ修正
# :disable: 無効化
# :remove(delete): ファイル削除、コードの一部を取り除く
# :rename: ファイル名の変更
# :upgrade: バージョンアップ
# :revert: 修正取り消し
# :style: 空白、セミコロン、行、コーディングフォーマットなどの修正
# :refactor(clean,improve): リファクタリング
# :test: テスト追加や間違っていたテストの修正
# :chore: ビルドツールやライブラリで自動生成されたものをコミットするとき
#
# ==== Emojis ====
# 🐛  :bug: バグ修正
# 👍  :+1: 機能改善
# ✨  :sparkles: 部分的な機能追加
# 🎨  :art: デザイン変更のみ
# 💢  :anger: コンフリクト
# 🚧  :construction: WIP
# 📝  :memo: 文言修正
# ♻️  :recycle: リファクタリング
# 🔥  :fire: 不要な機能・使われなくなった機能の削除
# 💚  :green_heart: テストやCIの修正・改善
# 👕  :shirt: Lintエラーの修正やコードスタイルの修正
# 🚀  :rocket: パフォーマンス改善
# 🆙  :up: 依存パッケージなどのアップデート
# 👮  :cop: セキュリティ関連の改善
# ⚙   :gear: config変更
# 📚  :books: ドキュメント
#
# 絵文字一覧：https://gitmoji.dev/
```

`git commit` 実行時にこのテンプレートを使用するように設定します。

```
$ cd <PROJECT_DIR>
$ git config commit.template .commit_template
```

この設定が不要な場合は、`--unset` オプションを与えて実行します。

```
$ cd <PROJECT_DIR>
$ git config --unset commit.template .commit_template
```

## コミットヘルパー
Go で実装したTUIツール [gum](https://github.com/charmbracelet/gum/tree/main) を使用すると
プレフィックスや絵文字いを簡単に選べるのでコミットが少し楽になります。

```
#!/usr/bin/bash

GUMCMD=$(which gum 2>/dev/null)
test -z "${GUMCMD}"  && {
   echo "gum: missing. you should install gum." >&2
   echo "I.E.) mise use -g -y gum" >&2
   exit 1
}

TYPE=$( echo $(gum choose \
 "fix: バグ修正" \
 "hotfix: クリティカルなバグ修正" \
 "add: 新規機能・新規ファイル追加" \
 "feat: feature" \
 "update: バグではない機能修正" \
 "change: 仕様変更による機能修正" \
 "docs: ドキュメントのみ修正" \
 "disable: 無効化" \
 "remove: コードの一部を取り除く" \
 "delete: ファイル削除" \
 "rename: ファイル名の変更" \
 "upgrade: バージョンアップ" \
 "revert: 修正取り消し" \
 "style: 空白、セミコロン、行、コーディングフォーマットなどの修正" \
 "refactor: リファクタリングのための修正 (グ修正や新機能の追加なし）" \
 "test: テスト追加や間違っていたテストの修正" \
 "build: ビルドシステムや外部依存関係に影響を与える変更" \
 "chore: その他、CI設定ファイルやスクリプトの変更" \
 ) | cut -d: -f1
)

EMOJI=$( echo $(gum choose \
"🔖  :bookmark: バージョンタグ" \
"🐛  :bug: バグ修正" \
"👍  :+1: 機能改善" \
"✨  :sparkles: 部分的な機能追加" \
"🎨  :art: デザイン変更のみ" \
"💢  :anger: コンフリクト" \
"🚧  :construction: 作業中(WIP: Work In progress)" \
"♻️   :recycle: リファクタリング" \
"🗑️  :wastebasket: 不要な機能・使われなくなった機能の削除" \
"💚  :green_heart: テストやCIの修正・改善" \
"👕  :shirt: Lintエラーの修正やコードスタイルの修正" \
"🚀  :rocket: パフォーマンス改善" \
"🆙  :up: 依存パッケージなどのアップデート" \
"👮  :cop: セキュリティ関連の改善" \
"⚙   :gear: config変更" \
"📚  :books: ドキュメント" \
"📝  :memo: 文言修正" \
 ) | cut -d: -f1
)

SCOPE=$(gum input --placeholder "scope")
test -n "${SCOPE}" && SCOPE="(${SCOPE})"

SUMMARY=$(gum input --value "${TYPE}${SCOPE}: ${EMOJI}" --placeholder "Summary of this change")
DESCRIPTION=$(gum write --placeholder "Details of this change")

# Commit these changes if user confirms
gum confirm "Commit changes?" && git commit -n -m "${SUMMARY}" -m "${DESCRIPTION}"
```

## pre-commit

[pre-commit](https://pre-commit.com/) をインストールそしておきます。

```
$ pdm add -dG dev pre-commit
```

`.pre-commit-config.yml` をレポジトリのベースディレクトリに配置します。
次の例にある `exclude:` は対象としないディレクトリを正規表現で記述するもので、
プロジェクト毎にことなることに留意してください。

```
exclude: "^ark/apif/collections/.*$"
repos:
- repo: https://github.com/sco1/brie-commit
  rev: v1.1.0
  hooks:
    - id: brie-commit
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v2.3.0
  hooks:
    - id: check-yaml
    - id: end-of-file-fixer
    - id: trailing-whitespace
    - id: mixed-line-ending
    - id: check-added-large-files
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.9.3
  hooks:
    - id: ruff
      files: .py$
- repo: https://github.com/JangasCodingplace/commit-prefix-pre-commit
  rev: v0.0.1-beta
  hooks:
  - id: commit-prefix
    stages: [ commit-msg ]
```

コミットする前に`pre-commit run` コマンドで登録した項目をチェックできるようになります。

```
$ git status
On branch feature_aipf_ark-gyukawa
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .pre-commit-config.yaml
        modified:   README.md

$ pre-commit run
🧀🧀🧀...................................................................Passed
Check Yaml...............................................................Passed
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
Mixed line ending........................................................Passed
Check for added large files..............................................Passed
ruff.................................................(no files to check)Skipped
```

### Hooks を利用する

Git`のhooksを利用すると、コマンドラインからよびださなくても
`git commit` をしたときに自動的に呼び出されます。
`pre-commit run` が終了ステータスがゼロ以外の場合、`git commit` は中断します。

```
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## GitLab/Git 関連ツール

- [auto-gitlab-backup](https://github.com/sund/auto-gitlab-backup)
- [git-chglog/git-chglog: CHANGELOG generator implemented in Go (Golang).](https://github.com/git-chglog/git-chglog )
- [extrawurst/gitui: Blazing 💥 fast terminal-ui for git written in rust 🦀](https://github.com/extrawurst/gitui )  
  GitUIは、ターミナル上でgit GUIの快適さを提供します
- [GitLab.org / cli · GitLab](https://gitlab.com/gitlab-org/cli#demo )  
  GLabはオープンソースのGitLab CLIツールで、ウィンドウやブラウザのタブを切り替えることなく、GitLabをあなたのターミナルで作業することができる。
- [gitleaks/gitleaks-action: Protect your secrets using Gitleaks-Action](https://github.com/gitleaks/gitleaks-action )  
  Gitleaks は、git リポジトリ内のパスワード、API キー、トークンなどのハードコードされた秘密を検出・防止するための SAST ツールです。 Gitleaks は、コード内の過去または現在の秘密を検出するための使いやすいオールインワンのソリューションです。 Gitleaks-ActionをGitHubのワークフローで有効にすると、秘密が漏えいした際にすぐにアラートを受け取ることができます。 デモはこちら（.gif）とこちら（.png）、v2 の新機能はこちらをご覧ください。 また、Gitleaks-Action の組織・企業向け設定方法について詳しく説明したブログもぜひご覧ください。

### シェルプロンプト

[starship](https://starship.rs/) を利用すると、
Git のブウランチや使用しているPythonなどのコマンドバージョンの把握が容易になります。
実行例:

```
❯ pwd
/home/goichi/ansible-dev

~/ansible-dev is 📦 v0.1.0 via 🐍 v3.12.8
❯ cd path/to/projectroot/

projectroot on  main via 🐍 v3.12.8
❯ source venvs/ansible-dev/bin/activate

projectroot on  main via 🐍 v3.9.21 (ansible-dev)
❯
```


`mise` が利用できる環境であれば次のコマンドでインストールできます。

```
$ mise use -g -y starship
$ echo 'eval "$(starship init bash)"' >> ~/.bashrc
```

あるいは、

```
$ curl -sS https://starship.rs/install.sh > startship.sh
$ mkdir ~/bin; sh starship.sh   --bin-dir=~/bin
$ echo 'eval "$(starship init bash)"' >> ~/.bashrc
```



### Python

- [python-gitlab](https://github.com/python-gitlab/python-gitlab)  
  python-gitlab is a Python package providing access to the GitLab server API.
- [GITLABにアクセスしてPipelineの一覧を取得、操作するアプリを作成](https://qiita.com/neetstar/items/adee609e028dd04cd2bd)
- [オンプレ版 GitLab で GitLab Pages する](https://qiita.com/hykisk/items/ebff2f7cd2e8100a6bbe)
- [python-gitlabでGitLabのパイプライン状況を一覧表示するHTMLをGitLab Pagesにデプロイする](https://qiita.com/dyamaguc/items/4e78b49cfff202141920)

## Ansible

GitLab CI/CD パイプラインで ansible を実行するメリット。  

Ansibleのプレイブックを定期的に実行するためには、Ansible Tower(OSS: AWX)のようなツールを
使用することができます。しかし、これはインフラストラクチャはさらに複雑なものにしてしまいます。

通常は、Ansible プレイブック、ロール、インベントリ、プラグインは
バージョン管理されている必要があります。
バージョン管理システムとしてGitLabを使用することで、
「誰がプレイブックにアクセスできるか」という機能はすでにカバーされていることになります。
GitLab CI/CD の機能を加えることで、「いつ、どのように何かを実行するか」という機能も
カバーされ、障害通知とステータスレポートもカバーされることになります。

- [ansible-gitlab-runner](https://github.com/riemers/ansible-gitlab-runner)  
  公式GitLab Runner（haroldbからのフォーク）を更新してインストールするAnsibleのロール
- [Ansibleの自動テストをGitlab CIでCIしてみる](https://qiita.com/konono/items/06159e6fc9beb01b5647)
- [How to run an ansible playbook using GitLab CI/CD?](https://medium.com/geekculture/how-to-run-an-ansible-playbook-using-gitlab-ci-cd-2135f76d7f1e)
- [GitLab CI template for Ansible](https://to-be-continuous.gitlab.io/doc/ref/ansible/)
- [GitLab CI/CD pipelines running ansible](https://der-jd.de/blog/2021/01/02/Using-ansible-with-gitlab-ci/)

## Bash


- [Shell Scripting GITLAB API](https://qiita.com/neetstar/items/db8f5f8ab72e368682d2)

## チュートリアルと小技

- [サル先生のGit入門〜バージョン管理を使いこなそう〜【プロジェクト管理ツールBacklog】](https://backlog.com/ja/git-tutorial/ )
- [注目！ GitLabのマージリクエストと、GitHubのプルリクエストの違い (同じではありません)](https://qiita.com/Hurry_Fox/items/ce4d99449ee9097feabd)
- [【GitLab】GitLab-Runnerを試用してみた](https://qiita.com/fy406/items/f3c4644fa280023d37e4)
- [GitLab Tips](https://qiita.com/nanbuwks/items/deff40bdc162679835d3)
- [GitLab Container Registryの容量削減](https://qiita.com/ntrlmt/items/09acbfe6d0f6a326ba9f)
- [GitlLabアップグレード　16.10.0-->17.0.2-->17.1.1](https://qiita.com/taro373/items/b79e9ad37c1c3119d5d2)
- [GitLabのタブを開きすぎて見分けづらいのでfaviconを変える拡張機能を作った](https://qiita.com/SogoK/items/31f74b517dc3c6884c04)
- [GitLab に Network Load Balancer を導入](https://qiita.com/kooohei/items/ddb69d37147e8952d0ee)
- [【Ansible】GitLab RunnerでAnsible実行環境のコンテナイメージを使いたい～第1章：GitLabの構築～](https://qiita.com/masa2223/items/081302acf9b6f63413b5)
- [Gitlab Runnerのインストールと初期設定](https://qiita.com/ryosuke-horie/items/438974ec5796b9b0f390)
- [GitLab CI/CDパイプラインで生成されたファイルをGitLabのリポジトリーにコミット(Push)し直す方法](https://qiita.com/ynott/items/8cb3b3995cb41ca78437)
- [オンプレ版GitLabでGitLab Pagesを実行するまで](https://qiita.com/np_hsgw/items/26ac2ff9883b654ab1d3)
- [gitlabのコンテナレジストリ](https://qiita.com/infra_buld/items/cc4acfe70ec22b5ba82a)
- [GitLab に Let's Encrypt で SSL を設定](https://qiita.com/kooohei/items/f7b7829243f766b6b0c1)
- [GitLab Omnibusロゴ差し替えスクリプト](https://qiita.com/hiconyan/items/7c5cdc6965c7eb44f1b5)
- [備忘録：GitLab Runnerの登録手順](https://qiita.com/hisato_imanishi/items/28bbe6f05f8e62d1ef62)


## トラブルシューティング
- [【GitLab】オンプレ+Proxy環境のGitLab Runnerが急に動かなくなった話](https://qiita.com/ForestMountain1234/items/1836891ac91fd433bfb9)
- [GitLab Runnerが署名の鍵の期限切れでアップデートできなかったのを解消した話](https://qiita.com/ynott/items/0780a60f004270a15776)
- [GitLabが署名の鍵の期限切れでアップデートできなかったのを解消した話](https://qiita.com/ynott/items/930558bdb5456746f40c)
