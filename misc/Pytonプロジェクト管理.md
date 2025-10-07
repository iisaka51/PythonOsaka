# Pythonプロジェクト管理

# この資料について

Python でのプロジェクト管理やパッケージ管理については、さまざまな方法があり、
ある意味ではPythonの弱点にもなっています。
この資料はプロジェクトやパッケージを管理するベストプラクティスとしての資料となるものです。

更新日時：2024/12/27

## 導入準備

複数バージョンのPythonを使い分けることができるmise をインストールします。

```
$ curl https://mise.run | sh
$ echo "eval \"\$(/home/goichi/.local/bin/mise activate bash)\"" >> ~/.bashrc
$ exec $SHELL -l
```

次のコマンドを実行するとインストールできるPythonが一覧されます。

```
$ mise ls-remote python 
```

ここで、3.12 をインストールし、デフォルトで使用するようにします。

```
$ mise use -g -y python@3.12
```


pip モジュールを最新にしておきます。

```
$ python -m pip install -U pip
```

## Python 仮想環境を構築する

Python仮想環境を使用すると次のようなメリットがあります。

- プロジェクトごとに環境を分離し、依存関係の競合を防ぐことができまる。
- 仮想環境を他の開発マシンに複製することで、同一の開発環境を簡単に再現できる。
- 仮想環境内でパッケージの追加・削除を行っても、グローバルなPython環境に影響を与えない

次のコマンドで Python 仮想環境を構築します。

```
$ python -m venv $HOME/.venvs/devroot-3.12
```

```
$ echo 'activate_devroot() { source "$HOME/.venvs/devroot-3.12/bin/activate" ; }' >> ~/.bash_profile
```

このPython仮想環境を有効にしたいときは、次のコマンドを実行します。

```
$ activate_devvroot
```

するとシェルプロンプの戦闘に "(仮想環境名)" が付加されます。

この仮想環境を無効にするためには次のコマンドを実行します。

```
$ deactivate
```

シェルプロンプトはもとに元に戻ります。


## PDM のインストール

[pdn](https://pdm.fming.dev/latest/) はPythonのプロジェクト、依存関係のためのツールです。


本来は Python の pip でインストールするのですが、
ここでは、mise でインストールします。

```
$ mise use -g -y pdm
```


```
$ mise list pdm
Tool  Version  Config Source              Requested
pdm   2.22.0   ~/.config/mise/config.toml latest
```

```
$ mise which pdm
/home/goichi/.local/share/mise/installs/pdm/2.22.0/bin/pdm
```


```
$ pdm --help
Usage: pdm [-h] [-V] [-c CONFIG] [-v | -q] [--no-cache] [-I] [--pep582 [SHELL]] [-n]


    ____  ____  __  ___
   / __ \/ __ \/  |/  /
  / /_/ / / / / /|_/ /
 / ____/ /_/ / /  / /
/_/   /_____/_/  /_/

Options:
  -h, --help            Show this help message and exit.
  -V, --version         Show the version and exit
  -c CONFIG, --config CONFIG
                        Specify another config file path [env var: PDM_CONFIG_FILE]
  -v, --verbose         Use `-v` for detailed output and `-vv` for more detailed
  -q, --quiet           Suppress output
  --no-cache            Disable the cache for the current command. [env var:
                        PDM_NO_CACHE]
  -I, --ignore-python   Ignore the Python path saved in .pdm-python. [env var:
                        PDM_IGNORE_SAVED_PYTHON]
  --pep582 [SHELL]      Print the command line to be eval'd by the shell for PEP 582
  -n, --non-interactive
                        Don't show interactive prompts but use defaults. [env var:
                        PDM_NON_INTERACTIVE]

Commands:
  add                   Add package(s) to pyproject.toml and install them
  build                 Build artifacts for distribution
  cache                 Control the caches of PDM
  completion            Generate completion scripts for the given shell
  config                Display the current configuration
  export                Export the locked packages set to other formats
  fix                   Fix the project problems according to the latest version of
                        PDM
  import                Import project metadata from other formats
  info                  Show the project information
  init                  Initialize a pyproject.toml for PDM. Built-in templates: -
                        default: `pdm init`, A simple template with a basic structure.
                        - minimal: `pdm init minimal`, A minimal template with only
                        `pyproject.toml`.
  install               Install dependencies from lock file
  list                  List packages installed in the current working set
  lock                  Resolve and lock dependencies
  outdated              Check for outdated packages and list the latest versions on
                        indexes.
  publish               Build and publish the project to PyPI
  python (py)           Manage installed Python interpreters
  remove                Remove packages from pyproject.toml
  run                   Run commands or scripts with local packages loaded
  search                Search for PyPI packages
  self (plugin)         Manage the PDM program itself (previously known as plugin)
  show                  Show the package information
  sync                  Synchronize the current working set with lock file
  update                Update package(s) in pyproject.toml
  use                   Use the given python version or path as base interpreter. If
                        not found, PDM will try to install one.
  venv                  Virtualenv management
```


### PDM の設定

次のコマンドを実行してpdmを調整しておきます。
```
$ pdm config --global install.cache True
$ pdm config --global pypi.verify_ssl False
$ pdm config --global venv.backend venv
```

はじめの行は、PDM のインストールキャッシュ機能を有効にしてます。

これは、ライブラリの実体を `$HOME/.cache/pdm/packages` 以下にインストールし、`.venv/lib/python<version>/site-packages` 内にはリンクを配置することで、
複数のPython仮想環境でライブラリを追加したときに、ストレージ消費を削減してくれます。


pdm は pyenv などとは異なり、プロジェクトのディレクトリに
Python仮想環境を展開することはしません。
デフォルトでは、`$HOME/.local/share/pdm/venvs` 以下に仮想環境を作成します。
これの良いところは同じバージョンのPythonを使用する別プロジェクトで、
共通して利用できるためディスク消費量が少なくなることです。

pdm では次のpython仮想環境をサポートしています。

- [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html)
- [venv](https://docs.python.org/3/library/venv.html)
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
- [uv](https://github.com/astral-sh/uv)

必要に応じて選択することで既存プロジェクトからの移行の工数も少なくなります。


また、pdm は、デフォルトでは virtualenv で実行します。
venv と virtualenv との違いはは、venv が標準ライブラリであることと、
virtualenv は Python 自身も切り替えることができることです。
ここでは、 mise で Python を切り替えるため、venv に設定しておきます

設定内容は `pdm config` で確認できます。

```
$ pdm config
Site/default configuration
build_isolation = True
cache_dir = /home/goichi/.cache/pdm
check_update = True
global_project.fallback = False
global_project.fallback_verbose = True
global_project.path = /home/goichi/.config/pdm/global-project
global_project.user_site = False
install.cache = False
install.cache_method = symlink
install.parallel = True
log_dir = /home/goichi/.local/state/pdm/log
pypi.ignore_stored_index = False
pypi.json_api = False
pypi.url = https://pypi.org/simple
pypi.verify_ssl = True
python.install_root = /home/goichi/.local/share/pdm/python
python.providers = ['venv', 'path', 'asdf', 'pyenv', 'rye', 'winreg', 'macos']
python.use_pyenv = True
python.use_venv = True
request_timeout = 15
scripts.show_header = False
strategy.inherit_metadata = True
strategy.resolve_max_rounds = 10000
strategy.save = minimum
strategy.update = reuse
theme.error = red
theme.info = blue
theme.primary = cyan
theme.req = bold green
theme.success = green
theme.warning = yellow
use_uv = False
venv.backend = virtualenv
venv.in_project = True
venv.location = /home/goichi/.local/share/pdm/venvs
venv.prompt = {project_name}-{python_version}
venv.with_pip = False

Home configuration (/home/goichi/.config/pdm/config.toml):
install.cache = True
pypi.verify_ssl = False
venv.backend = venv
```

## プロジェクトのディレクトリを作成

プロジェクトのディレクトリを作成して、そのディレクトリへ移動します。

```
$ mkdir sample && cd $_
$ pwd
/home/goichi/sample
```

### プロジェクトで使用する Python仮想環境を構築
ベースとなるPythonを汚さないためと、
他のプロジェクトとの競合を避けるために、
このプロジェクトのためのPython仮想環境を構築します。


```
$  pdm venv create --name sample-dev-3.12 --with-pip 3.12
Virtualenv /home/goichi/.local/share/pdm/venvs/sample-whImP8no-sample-dev-3.12 is created successfully
```

ここで、`--name 仮想環境名` を省略すると、プロジェクトのディレクトリに`.venv` が作成され展開されます。


仮想環境のパスを mise に登録します。

```
$ mise link python@sample-dev /home/goichi/.local/share/pdm/venvs/sample-whImP8no-sample-dev-3.12
$ mise use python@sample-dev
```
これで、このディレクトリに移動すると指定しているpythonに自動的に切り替わるようになります。


### プロジェクトの初期化

`pdm init` コマンドでプロジェクトを初期化します。

```
$ pdm init --python $(mise which python) default
```

実際のメッセージ入力は次のようになります。

```
$ pdm init --python $(mise which python)  default
pyproject.toml already exists, update it now.
INFO: Using the first matched interpreter.
Project name (sample):
Project version (0.1.0):
Do you want to build this project for distribution(such as wheel)?
If yes, it will be installed by default when running `pdm install`. [y/n] (n):
License(SPDX name) (MIT):
Author name ():
Author email ():
Python requires('*' to allow any) (==3.12.*):
Project is initialized successfully
```

README.md や必要なディレクトリが作成されています。

```
$ ls
mise.toml  __pycache__  pyproject.toml  README.md  src  tests
```

### 除外ファイル

Github/GitLab でァイルを管理するときに、管理課のdirectory内でレポジトリに含めたくないファイルがでてくると思います。

例えば、OSが自動で作成する隠しファイルやコーディング作業や、
テストなどで一時的にデータを格納するためのファイルなどです。

こうしたGitの管理に含めたくないファイルやディレクトリを個別に.gitignoreファイル内に指定することで、Gitコマンドを実行時にそれらを無視することができます。

複数の.gitignoreファイルをGitで管理しているディレクトリ内のどこに置くこともできます。

管理しているディレクトリのトップ階層から下の階層の.gitignoreを順に読み込みます。

しかし、ディレクトリごとに.gitignoreを持つと管理が面戸王になるため、通常はプロジェクトのトップディレクトリに１つだけ配置します。

`.gitignore` ファイルのテンプレートは次のように作成します。

```
URL=https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore
$ curl -sL $URL -o .gitignore
```

これをプロジェクトごとに毎回実行するのは手間なので、
`＄HOME/.config/mise/config.toml` に以下を追加しておきます。

```
[tasks.gitignore]
description = "Get gitignores from https://github.com/github/gitignore"
dir = "{{cwd}}"
env = { GITHUB="https://raw.githubusercontent.com/github/gitignore/refs/heads/main/" }
run = "curl -sL $GITHUB/{{arg(name='language', default='Python')}}.gitignore -o .gitignore"
```

以後は、`mise gitginore` でPython用の `.gitignoe` をダウンロードします。
他の言語ように取得したい場合は、`mise gitignore 言語名` と実行するだけです。
詳細は[github/gitignore: A collection of useful .gitignore templates](https://github.com/github/gitignore)を参照してください。


## プロジェクトで使用するライブラリ追加

まず、`pdm add` で追加したいライブラリを登録します。
pip と違いパッケージの依存関係の管理が楽になるだけでなく、
並列でダウンロードするため処理時間が短くなります。

```
$ pdm add typer openpyxl pyyaml
Adding packages to default dependencies: typer, openpyxl, pyyaml
  0:00:01 🔒 Lock successful.
Changes are written to pyproject.toml.
Synchronizing working set with resolved packages: 11 to add, 0 to update, 0 to remove

  ✔ Install typer 0.15.1 successful
  ✔ Install typing-extensions 4.12.2 successful
  ✔ Install shellingham 1.5.4 successful
  ✔ Install mdurl 0.1.2 successful
  ✔ Install et-xmlfile 2.0.0 successful
  ✔ Install click 8.1.7 successful
  ✔ Install markdown-it-py 3.0.0 successful
  ✔ Install rich 13.9.4 successful
  ✔ Install pyyaml 6.0.2 successful
  ✔ Install pygments 2.18.0 successful
  ✔ Install openpyxl 3.1.5 successful
  ✔ Update sample 0.1.0 -> 0.1.0 successful

  0:00:01 🎉 All complete! 11/11
```

テスト時だけに必要なライブラリは次のように登録します。

```
$ pdm add -dG test pytest
INFO: Adding group test to lockfile
Adding packages to test dev-dependencies: pytest
  0:00:01 🔒 Lock successful.
Changes are written to pyproject.toml.
Synchronizing working set with resolved packages: 4 to add, 0 to update, 0 to remove

  ✔ Install iniconfig 2.0.0 successful
  ✔ Install pluggy 1.5.0 successful
  ✔ Install packaging 24.2 successful
  ✔ Install pytest 8.3.4 successful

  0:00:00 🎉 All complete! 4/4
```

追加したライブラリの情報は `pdm.lock` と `pyproject.toml` に記録されます。


```
$ cat pyproject.toml
[project]
name = "sample"
version = "0.1.0"
description = "Sample Project"
authors = [
    {name = "Goichi Yukawa", email = "goichi.yukawa@ark-inc.co.jp"},
]
dependencies = ["typer>=0.15.1", "openpyxl>=3.1.5", "pyyaml>=6.0.2"]
requires-python = ">=3.12"
readme = "README.md"
license = {text = "MIT"}

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"


[tool.pdm]
distribution = true

[dependency-groups]
test = [
    "pytest>=8.3.4",
]
```

登録したライブラリは `pip list` でも参照できますが、
`pdm list` で確認すると整形して表示されます。

```
$ pdm list
╭───────────────────┬─────────┬────────────────────────╮
│ name              │ version │ location               │
├───────────────────┼─────────┼────────────────────────┤
│ click             │ 8.1.7   │                        │
│ et_xmlfile        │ 2.0.0   │                        │
│ iniconfig         │ 2.0.0   │                        │
│ markdown-it-py    │ 3.0.0   │                        │
│ mdurl             │ 0.1.2   │                        │
│ openpyxl          │ 3.1.5   │                        │
│ packaging         │ 24.2    │                        │
│ pluggy            │ 1.5.0   │                        │
│ Pygments          │ 2.18.0  │                        │
│ pytest            │ 8.3.4   │                        │
│ PyYAML            │ 6.0.2   │                        │
│ rich              │ 13.9.4  │                        │
│ sample            │ 0.1.0   │ -e /home/goichi/sample │
│ shellingham       │ 1.5.4   │                        │
│ typer             │ 0.15.1  │                        │
│ typing_extensions │ 4.12.2  │                        │
╰───────────────────┴─────────┴────────────────────────╯
```

依存性解決のために追加されたライブラリは `pdm list --tree` で確認できますｌ。

```
$ pdm list --tree
pytest 8.3.4 [ required: >=8.3.4 ]
├── iniconfig 2.0.0 [ required: Any ]
├── packaging 24.2 [ required: Any ]
└── pluggy 1.5.0 [ required: <2,>=1.5 ]
sample 0.1.0 [ required: This project ]
├── openpyxl 3.1.5 [ required: >=3.1.5 ]
│   └── et-xmlfile 2.0.0 [ required: Any ]
├── pyyaml 6.0.2 [ required: >=6.0.2 ]
└── typer 0.15.1 [ required: >=0.15.1 ]
    ├── click 8.1.7 [ required: >=8.0.0 ]
    ├── rich 13.9.4 [ required: >=10.11.0 ]
    │   ├── markdown-it-py 3.0.0 [ required: >=2.2.0 ]
    │   │   └── mdurl 0.1.2 [ required: ~=0.1 ]
    │   └── pygments 2.18.0 [ required: <3.0.0,>=2.13.0 ]
    ├── shellingham 1.5.4 [ required: >=1.3.0 ]
    └── typing-extensions 4.12.2 [ required: >=3.7.4.3 ]
```

他にも `pdm list --csv` でCSVフォーマットで、`pdm list --json` でJSONフォーマットで出力することができます。



## パッケージのビルドとインストール

まずは簡単なコードを `src/sample/__init__.py` に追加しましょう。

これは、`sample` モジュールに `main()` 関数を追加しています。

```
$ cat src/sample/__init__.py
def main():
    print("Hello Sample")
```

このパッケージをビルドします。

```
$ pdm build
Building sdist...
Built sdist at /home/goichi/sample/dist/sample-0.1.0.tar.gz
Building wheel from sdist...
Built wheel at /home/goichi/sample/dist/sample-0.1.0-py3-none-any.whl
```

```
$ ls dist
sample-0.1.0-py3-none-any.whl  sample-0.1.0.tar.gz
```

生成された sample-0.1.0-py3-none-any.whl は配布パッケージとなります。


python にインストールします。

```
$ pdm install
All packages are synced to date, nothing to do.
  ✔ Update sample 0.1.0 -> 0.1.0 successful

  0:00:00 🎉 All complete! 0/0
```

実行してみます。

```
$ pdm run
WARNING: No command is given, default to the Python REPL.
Python 3.12.8+ (heads/3.12:8e3c2d2, Dec  5 2024, 16:18:04) [GCC 11.5.0 20240719 (Red Hat 11.5.0-2)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from sample import main
>>> main()
Hello Sample
>>>
```

以後、ソースコードを修正したときは、
`pdm update` でパッケージを更新できます。

```
$ pdm update
  0:00:03 🔒 Lock successful.
All packages are synced to date, nothing to do.
  ✔ Update sample 0.1.0 -> 0.1.0 successful

  0:00:00 🎉 All complete! 0/0
```

## バージョン番号の管理

先の `pdm update` の実行例をみてわかるように、
`pyproject.toml` の `version` フィールドを更新していないと
パッケージのバージョンが変わりません。

```
$ sed 3q pyproject.toml
[project]
name = "sample"
version = "0.1.0"
```

パッケージ管理のバックエンドとして、`pdm-backend` を使用しているときは、動的に決定することができます。 この設定は、`pyproject.toml` から `version` フィールドを省き、`project.dynamic.Dynamic` のリストにversionを追加しますｌ。

```
$ sed 3q pyproject.toml
[project]
name = "sample"
dynamic = ["version"]
```

次に、[tool.pdm.version]` テーブルで、バージョン情報の取得方法を指定します。

3つの方法がサポートされています。
- 指定したファイルパスの静的文字列から読み込む
- SCMタグから読み込む (Git, Mercurialがサポート)
- 関数を呼び出してバージョンを読み込む

ここでは、もっとも単純なファイルからバージョンを読み込む方法について説明します。

`pyproject.toml` の [tool.pdm.version]` テーブルを次のようにします。

```
[tool.pdm.version]
source = "file"
path = "src/sammple/__init__.py"
```

指定したファイルには、変数　`__VERSION__`に文字列としてバージョンを定義している必要があります。

```
$ cat  src/sample/__init__.py
__VERSION__ = "0.1.0"

def main():
    print("Hello Sample")
```


## 静的解析ツールでPythonコードを検証する

リンター(linter) と呼ばれる静解析ツールを使うと、
事項する前に構文エラーなどを見つけることができます。
Pythonをサポートしているリンターには多くのがありますが、
主に次のものがよく利用されます。

 - [flake8](https://flake8.pycqa.org/en/latest/index.html#)
 - [pylint](https://pylint.readthedocs.io/en/latest/)
 - [black](https://black.readthedocs.io/en/stable/)
 - [mypy](https://mypy.readthedocs.io/en/stable/index.html)
 - [ruff](https://github.com/astral-sh/ruff?tab=readme-ov-file)
 - [wemake-python-styleguide](https://wemake-python-styleguide.readthedocs.io/en/latest/index.html)

次表はそれぞれの特徴をまとめたものです。


|                            |flake8  | pylint | black | mypy | ruff | wemake-python-styleguide |
| --------------------------| ------ | ------ | ---- | ---- | ------ |
| コード整形                 | ❌     | ❌    | ✅   | ❌  | ✅     | ❌ |
| コーディングスタイルチェック | 🤔     | ✅    | 🤔   | ❌  | ✅     | ❌ |
| バグ検出                   | 🤔     | ✅    | ❌   | ✅  | ✅     | ✅ |
| 複雑すぎるコードを検出       | ❌     | 🤔    | ❌   | ❌  | ✅     | ✅ |
| 厳しいルールがある          | ❌     | 🤔    | ❌   | ❌  | ✅     | ✅ |
| プラグインが使える         | ✅      | ❌    | ❌   | 🤔  | ❌     | ✅ |

ruff と wemake-python-styleguide を使いわけることも検討の価値があります。


## pytest でコードをテストする

pytest を利用するとソースコードを効率的にテストすることができます。

Pythonコードのユニットテストを自動生成するツールもあります。

- [Auger](https://github.com/laffra/auger)  
- [Python-Test-Generator](https://github.com/Pino10/Python-Test-Generator)
- [pyutgenerator - Python UT Generator](https://py-ut-generator.readthedocs.io/en/latest/index.html)
- [Pynguin—PYthoN General UnIt test geNerator](https://pynguin.readthedocs.io/en/latest/)
- [Pynguin](https://www.pynguin.eu/)  


また、豊富なプラグインがあるため、プロジェクトに応じたテストも容易になります。

[Pytest Plugin List](https://docs.pytest.org/en/latest/reference/plugin_list.html)

- [pytest-cov](https://pypi.org/project/pytest-cov/)  
  コードカバレッジを Pytest に組み込む
- [pytest-timeout](https://github.com/pytest-dev/pytest-timeout)  
  ハングアップしているテストを中断させる pytest プラグイン
- [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures)  
  テストを再実行して断続的な失敗を排除するための pytestプラグイン
- [pytest-random-order](https://github.com/pytest-dev/pytest-random-order)  
  テストの順番をランダムにする pytest プラグイン
- [pytest-order](https://github.com/pytest-dev/pytest-order)  
  テストの実行順序をカスタマイズできる pytest プラグイン
- [pytest-incremental](https://pytest-incremental.readthedocs.io/)  
  テストの実行順序を変更したり、テストの選択を解除したりするために、テスト実行の間にプロジェクトの構造やファイル変更を分析するプラグイン。   
   インタラクティブなテスト実行のためのフィードバックをより高速に処理できる。
- [pytest-custom-scheduling](https://pypi.org/project/pytest-custom-scheduling/)  
  グループ化された複数のテストをスケジュールして並列に実行できる
- [pytest-docfiles](https://pypi.org/project/pytest-docfiles/)  
  Markdownに記述したテストケースを実行できる
- [pytest-dotenv](https://pypi.org/project/pytest-dotenv/)  
   python-dotenv を使って `.env` ファイルから環境変数を読み込む。 
   追加の設定は `pytest.ini` などの pytest 設定ファイルで定義できる
- [pytest-envfiles](https://pypi.org/project/pytest-envfiles/)  
  指定したファイルから環境変数を読み込む
- [pytest-reporter](https://github.com/christiansandberg/pytest-reporter)  
  テンプレートから Pytest レポートを生成するプラグイン\。   
  pytest-reporter-html1を利用したり、独自のテンプレートに継承して内容や見た目を調整したり、あるいは独自のテンプレートを作成したりすることができる。
- [pytest-dump2json](https://pypi.org/project/pytest-dump2json/)  
  テスト結果をJSON型式で出力する
- [pytest-durations](https://pypi.org/project/pytest-durations/)  
  テストに要する時間を計測する
- [pytest-examples](https://pypi.org/project/pytest-examples/)  
  Python の docstring や markdown ファイルに記述したコード例をテストする
- [pytest-csv](https://github.com/nicoulaj/pytest-csv)  
  pytestのレポートをCSVファイルに出力する
- [pytest-excel](https://github.com/ssrikanta/pytest-excel)  
  pytestのレポートをExcelファイルに出力する
- [Faker](https://faker.readthedocs.io/en/master/)
  偽のデータを生成してくれるPythonパッケージで、pytestの fixtures も提供さｓれている
- [pytest-fixtures](https://pypi.org/project/pytest-fixtures/)  
  データをファイルから読み込んでテストを行う
- [pytest-takeltest](https://pypi.org/project/pytest-takeltest/  
  )  
  ansibleで設定されたサーバーをテストするためのユニットテストをpythonで書ける
- [pytest-ansible ](https://pypi.org/project/pytest-ansible/)  
  pytestでAnsible関連のタスクやシナリオを効率的に実行し、テストすることができる
- [pytest-ansible-playbook](https://pypi.org/project/pytest-ansible-playbook/)  
  テストケースのセットアップ中に特定のansible playbook を実行できる
- [pytest-ansible-playbook-runner](https://pypi.org/project/pytest-ansible-playbook-runner/)  
  テストケースのセットアップ中に特定の ansible playbooks_ を実行できる
- [pytest-ansible-units](https://pypi.org/project/pytest-ansible-units/)  
  Ansible コレクションの単体テストをpytestを使ってテストができる
- [pytest-examples](https://github.com/pydantic/pytest-examples)  
  MarkdownファイルやPython のdocstringの実行例をpytestを使ってテストができる
- [pytest-securestore](https://pypi.org/project/pytest-securestore/)  
  暗号化されたデータをテストリポジトリに含める方法を提供し、プロジェクトメンバーがテストアカウントデータ(ログイン、パスワード、キー)を共有できるようになる
- [pytest-html](https://pytest-html.readthedocs.io/en/latest/)  
  pytest-htmlはテスト結果のHTMLレポートを生成するpytestのプラグイン
- [pytest-md-report](https://github.com/thombashi/pytest-md-report)  
  pytest 結果のレポートをMarkdown表形式で生成するプラグイン
- [pytest-md](https://pypi.org/project/pytest-md/)  
  pytest 結果の Markdown レポートを生成するプラグイン
- [pytest-emoji](https://github.com/hackebrot/pytest-emoji)  
  pytest 結果の Markdown レポートに絵文字を使えるようにするプラグイン
- [pytest-spec2md](https://github.com/mh7d/pytest-spec2md/tree/main)   
  テストを実行しながら、仕様書としてマークダウンファイルを生成する
- [pytest-markdown-docs](https://github.com/modal-labs/pytest-markdown-docs)  
  マークダウンファイルやdocstringからマークダウンのコードスニペットをテストとして使用できる
- [pytest-black](https://github.com/shopkeep/pytest-black)  
  black でフォーマットチェックをするための pytest プラグイン


### coverage 

プログラムを監視し、コードのどの部分が実行されたかを記録し、ソースを分析して、実行された可能性があったが実行されなかったコードを特定することをコードカバレッジ(Coverage)と呼ばれます。
カバレッジは、コードのどの部分がテストによって実行されていて、どの部分が実行されていないかを示すことができるため、テストの有効性を評価するために使用されます。Python では[Coverage.py](https://coverage.readthedocs.io/en/coverage-5.2.1/)がよく利用されます。

coverageの機能の1つにreportのhtmlの出力の機能があります。

- テストした箇所がわかりやすい
- ドキュメント作成の手間を削減できる

カバレッジレポートはテストフレームワークを使って検証されたコードの割合（%）を示します。 100%ということは、モジュールのすべての行を検証したことを意味します。 これは、次にどんなテストケースを書けばいいのかわからないときに非常に便利です。 カバレッジレポートは、ターミナル経由で生成することができ、ブラウザで見ることができるきれいなHTMLファイルとして見ることができます。


<img src="https://pytest-with-eric.com/images/pytest-code-coverage-report-100-percent.png" alt="Coverage Report" width="500"/>

## ドキュメントの自動生成


```
$ pdm add -dG test mkdocs mkdocs-with-pdf
```

```
$ mkdocs -h
Usage: mkdocs [OPTIONS] COMMAND [ARGS]...

  MkDocs - Project documentation with Markdown.

Options:
  -V, --version         Show the version and exit.
  -q, --quiet           Silence warnings
  -v, --verbose         Enable verbose output
  --color / --no-color  Force enable or disable color and wrapping for the output.
                        Default is auto-detect.
  -h, --help            Show this message and exit.

Commands:
  build      Build the MkDocs documentation.
  get-deps   Show required PyPI packages inferred from plugins in mkdocs.yml.
  gh-deploy  Deploy your documentation to GitHub Pages.
  new        Create a new MkDocs project.
  serve      Run the builtin development server.
```



ドキュメントを作成します。

```
$ mkdocs new .
INFO    -  Writing config file: ./mkdocs.yml
INFO    -  Writing initial docs: ./docs/index.md
```

これで、`docs/iindex.md` が作成されます。

`mkdocs.yml` があるディレクトリで `mkdocs serve` を実行すると、
Webサーバが立ち上がりブラウザでドキュメントを参照することができます。


```
$ mkdocs serve
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.08 seconds
INFO    -  [17:18:20] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [17:18:20] Serving on http://127.0.0.1:8000/
```

ドキュメントとPDFとして出力する
`mkdocs.yml` に一家を追記します。

```
plugin:
  - with-pdf
```


```
$ mkdocs biuld
```

これで、`site/pdf/document.pdf` が作成されます。



## 参考資料
- [mise-en-place](https://mise.jdx.dev/)
- [PDM Official Site](https://pdm-project.org/en/latest/)
- [pdm-project/pdm: A modern Python package and dependency manager supporting the latest PEP standards](https://github.com/pdm-project/pdm?tab=readme-ov-file)
- [Python のプロジェクトマネージャー pdm の紹介 - Qiita](https://qiita.com/iisaka51/items/f500da5968df355f4c8b)
- [Coverage.py — Coverage.py 5.2.1 documentation](https://coverage.readthedocs.io/en/coverage-5.2.1/)
- [MkDocsによるドキュメント作成](https://zenn.dev/mebiusbox/articles/81d977a72cee01)
- [MkDocs](https://www.mkdocs.org/)
- [mkdocs-with-pdf](https://github.com/orzih/mkdocs-with-pdf)
- [jq](https://github.com/jqlang/jq)  
  Cで実装されたJSONパーサー　　
  `mise use -g -y jq` で簡単にインストールできる
- [yq](https://github.com/mikefarah/yq)  
  Pythonで実装されたYAML, JSON, XML をパースできるツール  
  `pdm add -dG test yq`  でテスト時のライブラリとして追加
- [dasel](https://github.com/TomWright/dasel)  
  Goで実装された jq, yq 互換のJSON, YAML, TOML, XML, CSV 相互変換ツール  
  `mise use -g -y dasel` で簡単にインストールできる
- [mkdocstrings](https://github.com/mkdocstrings/mkdocstrings)  
  ソースコードからMkDocsのドキュメントを自動生成する
- [mktestdocs](https://github.com/koaning/mktestdocs?tab=readme-ov-file)  
  Markdownファイル/ドキュメントのコードブロックをpytestで実行する
- [3 Simple Ways To Omit Subfolders From Python Coverage Reports](https://pytest-with-eric.com/coverage/python-coverage-omit-subfolder/)
- [ow To Measure And Improve Test Coverage With Poetry And Pytest](https://pytest-with-eric.com/coverage/poetry-test-coverage/)
- [How To Generate Beautiful & Comprehensive Pytest Code Coverage Reports](https://pytest-with-eric.com/pytest-best-practices/pytest-code-coverage-reports/)