CLIアプリケーションフレームワークcmdkitを使ってみよう
=================
## cmdkit について

cmdkit は、Python のコマンドラインアプリケーションに必要ないくつかの共通パターンを実装したものです。コンソールアプリケーションの開発するために必要になる手続きを減らすことを目的に開発されています。cmdkit を使って開発されたアプリケーションは、実装が簡単で、メンテナンスが容易で、理解しやすいものになります。

ただし、この資料を作成している時点では、ドキュメントは製作中であることに留意してください。

cmdkit はPython 3.7 以降で動作します。

## インストール
cmdkit は pip でインストールを行います。

 bash
```
 $ pip install cmdkit
 
```

オリジナルは設定ファイルの拡張子でファイルフォーマットを判別します。これをキーワード引数  `ftype="json"` のように与えるバージョンは次のようにインストールすることができます。

 bash
```
 $ git clone https://github.com/iisaka51/CmdKit.git
 $ Cmdkit
 $ git checkout develop
 $ python setup.py install
```

## 機能概要
Applicationクラスは、優れたエントリーポイントのための定型文を提供します。このApplication クラスを継承してアプリケーションを作成します。まず、例を見てみましょう。

 01_demoapp.py
```
 import sys
 from cmdkit.app import Application, ApplicationGroup, exit_status
 from cmdkit.cli import Interface, ArgumentError
 from cmdkit.config import Namespace
 
 APP_NAME = 'demo_simple'
 APP_DESCRIPTION = """\
 Description for demo application.
 """
 
 APP_USAGE = f"""\
 Usage: {APP_NAME} [-h|--help]
 
 {APP_DESCRIPTION}
 """
 
 APP_HELP=f"""\
 {APP_USAGE}
 
 Options:
 -h, --help        show this message and exit.
 """
 
 class DemoApp(Application):
     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
 
     name: str = None
     interface.add_argument('name')
 
     def run(self):
         print(f'Hello {self.name}')
 
 def main() -> int:
     return DemoApp.main(sys.argv[1:2])
 
 if __name__ == '__main__':
     main()
           
```

このコードには、何もオプション解析の処理が書かれていません。 `--help` オプションや引数の解析処理は、Applicationクラスで定義されているものが利用されます。


```
 In [1]: %run 01_demoapp.py
 Usage: demo_simple [-h|--help] name
 
 Description for demo application.
 
 
 
 In [2]: %run 01_demoapp.py --help
 Usage: demo_simple [-h|--help] name
 
 Description for demo application.
 
 
 
 Options:
   -h, --help        show this message and exit.
 
 
 In [3]: %run 01_demoapp.py Python
 Hello Python
 
```


Interfaceクラスは３つの引数を受け取リ、標準ライブラリのargparse.ArgumentParserクラスの動作を変更し、必要に応じていくつかの単純な例外を発生させます。Application クラスはこの例外を捕獲してヘルプメッセージやバージョン情報を表示させます。詳細は後述していますので、心配しないでください。今は大まかに理解するだけで大丈夫です。

ソースコード cmdkit/cli.py での例外の定義

```
 class HelpOption(Exception):
     """Raised by :class: `~Interface` when the help option is passed."""
 
 
 class VersionOption(Exception):
     """Raised by :class: `~Interface` whenever  `` action='version' `` ."""
 
 
 class ArgumentError(Exception):
     """Raised by :class: `~Interface` on bad arguments."""
     
```

ApplicationGroupを使ってコマンドラインアプリケーションを重ねて構築することで、git のサブコマンドのようにCLIを反映したシンプルな構造とモジュールを開発することができます。


Configurationクラスは、読み込みレベルをもたせた複数のファイルから設定を取り込み、環境変数を階層的に展開してマージすることを、基本的に１行できます。


```
 myconf = Configuration.from_local(
                  default = MyAppConfig().__dict__,
                  env = True, prefix='MYAPP',
                  user = str(homedir / '.myapp.yml'),
                  local = str(workdir / 'myapp.yml'))
```

Configuration`クラスを初期化するときに次のキーワード引数を与えることでデフォルト値の設定を柔軟に定義することができます。

-  `default` - デフォルトの設定値の辞書
-  `system` - システムレベルの設定ファイル
-  `user` - ユーザレベルの設定ファイル
-  `local` - カレントディレクトリにある設定ファイル

優先度は `default` で定義したものもが最も低く、 `system` 、 `user` 、 `local` の順に上書きされていきます。
これらをマージするとき、優先順位の低いソースの同じ値を上書きするようなことを避けるために、Namespaceクラスは、標準的なPython dictの動作を拡張して、updateに深さ優先でマージする実装になっています。

設定ファイルは、TOMI、YAML、JSON で記述することができます。cmdkit の 2.6.1 ではファイルの拡張子で判断しています。
タイプを指定できるようにした修正を[プルリクエスト ](https://github.com/glentner/CmdKit/pull/17)して受け入れられたので、次のバージョンではファイル名に制限はなくなるかもしれません。jkkk

## Application クラス
すべてのアプリケーションインターフェイスのための抽象ベースクラスです。
使用する場合は次のようにインポートします。


```
 from cmdkit.app import Application
 
```


Application クラスを派生したクラスを作成して、独自の処理を `run()` メソッドに定義します。クラスメソッドの  `mai()` を呼び出すことでアプリケーションが実行します。

ソースコード cmdkit/app.py から Application クラスを抜粋

```
 class Application(abc.ABC):
 
     interface: cli.Interface = None
     ALLOW_NOARGS: bool = False
 
     shared: Namespace = None
 
     exceptions: Dict[Type[Exception], Callable[[Exception], int]] = dict()
     log_critical: Callable[[str], None] = log.critical
     log_exception: Callable[[str], None] = log.exception
     
     @classmethod
     def handle_help(cls, message: str) -> None:
         print(message)
 
     @classmethod
     def handle_version(cls, *args) -> None:
         print(*args)
 
     @classmethod
     def handle_usage(cls, message: str) -> None:
         print(message)
 
     def __init__(self, **parameters) -> None:
         """Direct initialization sets  `parameters` ."""
         for name, value in parameters.items():
             setattr(self, name, value)
     
     @classmethod
     def from_cmdline(cls, cmdline: List[str] = None) -> Application:
         """Initialize via command line arguments (e.g.,  `sys.argv` )."""
         return cls.from_namespace(cls.interface.parse_args(cmdline))
 
     @classmethod
     def from_namespace(cls, namespace: cli.Namespace) -> Application:
         """Initialize via existing namespace/namedtuple."""
         return cls(**vars(namespace))
 
     @classmethod
     def main(cls, cmdline: List[str] = None) -> int:
         """Entry-point for application."""
 
         try:
             if not cmdline:
                 if hasattr(cls, 'ALLOW_NOARGS') and cls.ALLOW_NOARGS is True:
                     pass
                 else:
                     print(cls.interface.usage_text)
                     return exit_status.usage
 
             with cls.from_cmdline(cmdline) as app:
                 app.run()
 
             return exit_status.success
 
         except cli.HelpOption as help_opt:
             cls.handle_help(*help_opt.args)
             return exit_status.success
 
         except cli.VersionOption as version:
             cls.handle_version(*version.args)
             return exit_status.success
 
         except cli.ArgumentError as error:
             cls.log_critical(error)
             return exit_status.bad_argument
 
         except KeyboardInterrupt:
             cls.log_critical('keyboard-interrupt: going down now!')
             return exit_status.keyboard_interrupt
 
         except Exception as error:
             for exc_type, exc_handler in cls.exceptions.items():
                 if isinstance(error, exc_type):
                     return exc_handler(error)
             cls.log_exception('uncaught exception occurred!')
             raise
 
     @abc.abstractmethod
     def run(self) -> None:
         """Business-logic of the application."""
         raise NotImplementedError()
 
     def __enter__(self) -> Application:
         """Place-holder for context manager."""
         return self
 
     def __exit__(self, *exc) -> None:
         """Release resources."""
         pass
         
```


クラスメソッド `main()` は、Applicationクラスのクラスメソッドである  `from_namespace()` と　 `from_cmdline()` によって初期化されます。

これらのメソッドは : `Interface` クラスのインスタンスオブジェクトがもつメソッドを使ってコマンドライン引数を解析します。直接的な初期化はクラス変数の名前を文字列で取り、単にインスタンスに割り当てられます。
これらはアノテーションの付いた既存のクラスレベルの属性でなければなりません。

デフォルトでは、引数を与えずに実行すると使用例( `APP_USAGE` )が表示されます。
クラス属性として  `ALLOW_NOARGS=True` が定義されていると、引数がない場合でもアプリケーションに処理を渡します。

クラスメソッド `main()` を実行中にcmdkit が想定している例外が発生すると、クラス変数 `log_criticall` にアサインされている関数を呼び出します。これはデフォルトでは、 `log.critical()` になっています。

これ以外の例外は  `exceptions` の辞書を検索してヒットした例外があれば、そこに定義されている関数を呼び出します。
それにも該当しない例外は、クラス変数 `log_exception` にアサインされている関数を呼び出します。このデフォルトは `log.exception` になっているためトレースバックが発生します。

ソースコード cmdkit/app.py の Applicationクラスでの exceptions と log_critical、 log_exception の定義部分を抜粋

```
     exceptions: Dict[Type[Exception], Callable[[Exception], int]] = dict()
     log_critical: Callable[[str], None] = log.critical
     log_exception: Callable[[str], None] = log.exception
```

ソースコードcmdkit/app.py のロギングの定義部分を抜粋

```
 import logging
 # ...
 log = logging.getLogger(__name__)
```

これをみてわかるようにロガーの定義がされているたけなので、実際には必要に応じてロギングを設定する必要が’あります。

ロギング設定の例：

```
 import logging
 # ..
 # 標準出力(コンソール)にログを出力するハンドラを生成する
 log_stderr = logging.StreamHandler(sys.stderr)
 log_stderr.setLevel(logging.WARNING)
 log_stderr.setLevel(logging.CRITICAL)
 
 # ハンドラをロガーに紐づける
 log.addHandler(log_stderr)
```

アプリケーションの終了コードは次のいずれかが返されます。

ソースコード cmdkit/app.py での終了コードの定義

```
 class ExitStatus(NamedTuple):
     """Collection of exit status values."""
     success:            int = 0
     usage:              int = 1
     bad_argument:       int = 2
     bad_config:         int = 3
     keyboard_interrupt: int = 4
     runtime_error:      int = 5
     uncaught_exception: int = 6
 
 # global shared instance
 exit_status = ExitStatus()
     
```

## Interface クラス
Interface クラスは、 `sys.exit` を呼び出す代わりに ArgumentError を発生させる  `argparse.ArgumentParser` の派生クラスです。


```
 Interface(program: str, usage_text: str, help_text: str, **kwargs) -> None:
```

  - **program**：プログラム名、デフォルトは  `os.path.basename(sys.argv[0])` 
  - **usage_text**：使用方法の文字列
  - **help_text**： ヘルプメッセージ

usage_text` と  `help_text` は与えられたそのままの内容で使用されます。

> usage_text` と  `help_text` を自動生成する click や typer といったライブラリと比較すると、cmdkit は手間がかかるように
> 見えるかもしれません。しかし、cmdkit ではヘルプメッセージを自由に定義できるわけです。

argparse で定義されているメソッド利用できます。

使用例：

```
 from cmdkit.cli import Interface
 
 interface = Interface('myapp', 'usage: myapp ...', 'help: ...')
 interface.add_argument('--verbose', action='store_true')
 
```

Interface クラスでのオプション解析の指示については、後ほど詳しく説明します。

## Configurationクラス

ソースコード cmdkit/cli.py には、アプリケーションレベルのパラメータを管理するクラスとインターフェイス パラメータを管理するクラスが定義されています。

- Namespace クラス：深さ優先の更新メソッドを持つ辞書
- Environクラス: Namespace クラスを派生した環境変数を管理する
- Configurationクラス：順番に並べられた  `Namespace` 辞書のコレクション

Namespaceクラスと Environクラスの理解は、Configuration クラスを理解するための助けになります。

### Namesapceクラス
順番に並べられた  `Namespace` 辞書のコレクションです。
- Namespace`のアップデート機能を使って、コンフィギュレーションパラメータを重ねて表示することができます。


```
 Namespace(*args: Union[Iterable, Mapping], **kwargs: Any) -> None
```


```
 In [2]: # %load 02_namespace.py
    ...: from cmdkit.config import Namespace
    ...:
    ...: data = {'a': {'x': 1, 'y': 2}, 'b': 3}
    ...:
    ...: ns = Namespace(data)
    ...:
    ...: v1 = f'{ns}'
    ...: ns.update({'a': {'x': 4, 'z': 5}})
    ...:
    ...: v2 = f'{ns}'
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 Namespace({'a': {'x': 1, 'y': 2}, 'b': 3})
 
 In [4]: print(v2)
 Namespace({'a': {'x': 4, 'y': 2, 'z': 5}, 'b': 3})
 
```


このクラスはYAML、TOML、JSONのフォーマットで記述された構成ファイルに簡単に読み書きすることができます。

読み込み

```
 from_dict(cls, other: Dict[str, Any]) -> Namespace:
```
- from_env(cls, prefix: str = '', defaults: dict = None) -> Namespace:
- from_local(cls, filepath: str, ignore_if_missing: bool = False, **options) -> Namespace:
- from_yaml(cls, path_or_file: Union[str, IO], **options) -> Namespace:
- from_toml(cls, path_or_file: Union[str, IO], **options) -> Namespace:
- from_json(cls, path_or_file: Union[str, IO], **options) -> Namespace:
 

書き込み

```
 to_dict(self) -> Dict[str, Any]:
 to_env(self) -> Environ:
 to_local(self, filepath: str, **options) -> None:
 to_yaml(self, path_or_file: Union[str, IO], encoding: str = 'utf-8', **kwargs) -> None:
 to_toml(self, path_or_file: Union[str, IO], encoding: str = 'utf-8', **kwargs) -> None:
 to_json(self, path_or_file: Union[str, IO], encoding: str = 'utf-8', indent: int = 4, **kwargs) -> None:
 
```

 `from_env()` メソッドは、 `prefix` キーワード引数で与えた文字列で始まる環境変数をフィルタリングしてから処理を行います。


```
 In [1]: import os
 
 In [2]: os.environ['MYAPP_LOGGING_LEVEL']='INFO'
 
 In [3]: %load 03_from_env.py
 
 In [4]: # %load 03_from_env.py
    ...: from cmdkit.config import Namespace
    ...:
    ...: ns  = Namespace.from_env(prefix='MYAPP',
    ...:                    defaults={'MYAPP_LOGGING_LEVEL': 'WARNING', })
    ...: print(ns.items())
    ...:
 dict_items([('MYAPP_LOGGING_LEVEL', 'INFO')])
 
 In [5]: os.environ['MYAPP_LOGGING_MSG']='DEBUG' # 追加
 
 In [6]: %run 03_from_env.py
 dict_items([('MYAPP_LOGGING_LEVEL', 'INFO'), ('MYAPP_LOGGING_MSG', 'DEBUG')])
  
```

prefix が指定されていないと、対象の環境変数をうまく取り込めません。


```
 In [1]: import os
 
 In [2]: os.environ['MYAPP_LOGGING_LEVEL']='INFO'
 
 In [3]: %load 04_from_env_noprefix.py
 
 In [4]: # %load 04_from_env_noprefix.py
    ...: from cmdkit.config import Namespace
    ...:
    ...: ns  = Namespace.from_env(defaults={'MYAPP_LOGGING_LEVEL': 'WARNING', })
    ...: print(ns.items())
    ...:
 dict_items([('MYAPP_LOGGING_LEVEL', 'WARNING')])
 
 In [5]: os.environ['MYAPP_LOGGING_MSG']='DEBUG' # 追加
 
 In [6]: %run 04_from_env_noprefix.py
 dict_items([('MYAPP_LOGGING_LEVEL', 'WARNING')])
 
 
```


構成ファイルの読み書きも簡単になります。


```
 In [1]: !cat config.yaml
 MAIL_SERVER: "smtp.gmail.com"
 MAIL_PORT: 587
 MAIL_USE_TLS: True
 MAIL_USE_SSL: False
 MAIL_USERNAME: None
 MAIL_PASSWORD: None
 MAIL_DEFAULT_SENDER: "admin@example.com"
 # for debug
 MAIL_DEBUG: False
 MAIL_SUPPRESS_SEND: False
 
 In [2]: %load 05_from_yaml.py
 
 In [3]: # %load 05_from_yaml.py
    ...: from cmdkit.config import Namespace
    ...: from pprint import pprint
    ...:
    ...: ns = Namespace.from_yaml('config.yaml')
    ...:
    ...: pprint(ns.items())
    ...: ns.MAIL_DEBUG = True
    ...:
    ...: ns.to_yaml('config.yaml')
    ...:
    ...: #!cat config.yaml
    ...:
 dict_items([('MAIL_SERVER', 'smtp.gmail.com'), ('MAIL_PORT', 587), ('MAIL_USE_TLS', True), ('MAIL_USE_SSL', False), ('MAIL_USERNAME', 'None'), ('MAIL_PASSWORD', 'None'), ('MAIL_DEFAULT_SENDER', 'admin@example.com'), ('MAIL_DEBUG', False), ('MAIL_SUPPRESS_SEND', False)])
 
 In [4]: !cat config.yaml
 MAIL_DEBUG: true
 MAIL_DEFAULT_SENDER: admin@example.com
 MAIL_PASSWORD: None
 MAIL_PORT: 587
 MAIL_SERVER: smtp.gmail.com
 MAIL_SUPPRESS_SEND: false
 MAIL_USERNAME: None
 MAIL_USE_SSL: false
 MAIL_USE_TLS: true
 
 In [５]: %run 05_from_yaml.py
 dict_items([('MAIL_DEBUG', True), ('MAIL_DEFAULT_SENDER', 'admin@example.com'), ('MAIL_PASSWORD', 'None'), ('MAIL_PORT', 587), ('MAIL_SERVER', 'smtp.gmail.com'), ('MAIL_SUPPRESS_SEND', False), ('MAIL_USERNAME', 'None'), ('MAIL_USE_SSL', False), ('MAIL_USE_TLS', True)])
 
```

 `from_local()` は、システム設定、ユーザ設定、ローカル設定といったレベルで構成ファイルを読み込むことができます。


```
 In [2]: # %load 06_from_local.py
    ...: import os
    ...: from cmdkit.config import Configuration
    ...: from pprint import pprint
    ...:
    ...: HOME, CWD = os.getenv('HOME'), os.getcwd()
    ...:
    ...: cfg = Configuration.from_local(
    ...:             default=None, env=True, prefix='MYAPP',
    ...:             system='/etc/myapp.yml',
    ...:             user=f'{HOME}/.myapp.yml',
    ...:             local=f'{CWD}/myapp.yml')
    ...:
    ...: # pprint(cfg)
    ...: # print(cfg)
    ...:
 
 In [3]: pprint(cfg)
 {'MAIL_DEBUG': True,
  'MAIL_DEFAULT_SENDER': 'admin@example.com',
  'MAIL_PASSWORD': 'None',
  'MAIL_PORT': 587,
  'MAIL_SERVER': 'smtp.gmail.com',
  'MAIL_SUPPRESS_SEND': False,
  'MAIL_USERNAME': 'None',
  'MAIL_USE_SSL': False,
  'MAIL_USE_TLS': True}
 
 In [4]: print(cfg)
 Configuration(default=Namespace({}), system=Namespace({}), user=Namespace({}), local=Namespace({'MAIL_DEBUG': True, 'MAIL_DEFAULT_SENDER': 'admin@example.com', 'MAIL_PASSWORD': 'None', 'MAIL_PORT': 587, 'MAIL_SERVER': 'smtp.gmail.com', 'MAIL_SUPPRESS_SEND': False, 'MAIL_USERNAME': 'None', 'MAIL_USE_SSL': False, 'MAIL_USE_TLS': True}), env=Namespace({}))
```

この例の場合では、はじめに  `/etc/myapp.yml` を読み込み、次にユーザホームディレクトリの  `$HOME/.myapp.yml` を読み込んで、実行時のカレントディレクトリの  `myapp.yml` を読み込みます。それぞれのファイルは存在していなくてもOKです。
ファイル名の拡張子は重要で、ファイルフォーマットを判別するために使用されています。

#### whereis 
オプションで  `value` でフィルタリングされた  `leaf` へのパスを検索します。


```
 whereis(self, leaf: str, value: Union[Callable[[T], bool], T] = lambda _: True) 
     -> List[Tuple[str, ...]]:
```



```
 In [2]: # %load 07_whereis.py
    ...: from cmdkit.config import Namespace
    ...:
    ...: data = {'a': {'x': 1, 'y': 2},
    ...:         'b': {'x': 3, 'z': 4} }
    ...:
    ...: ns = Namespace(data)
    ...:
    ...: v1 = f'{ns}'
    ...: v2 = ns.whereis('x')
    ...: v3 = ns.whereis('x', 1)
    ...: v4 = ns.whereis('x', lambda v: v % 3 == 0)
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v4)
    ...:
 
 In [3]: print(v1)
 Namespace({'a': {'x': 1, 'y': 2}, 'b': {'x': 3, 'z': 4}})
 
 In [4]: print(v2)
 [('a',), ('b',)]
 
 In [5]: print(v3)
 [('a',)]
 
 In [6]: print(v4)
 [('b',)]
 
```

### Environクラス
Namespaceクラスを継承したクラスで、 `Namespace.from_env()` で初期化されます。
特別なメソッド  `reduce()` は環境変数をアンダースコアで分割することでデータの構造を再現します。つまり、環境変数名をアンダースコア( `_` )で区切ると、環境変数をネストすることができます。
例えば、Python での辞書型のデータ `{'run: {'echo': True}}` は、 `PREFIX_RUN_ECHO=1` と定義することができます。


```
 In [2]: # %load 10_environ.py
    ...: import os
    ...: from cmdkit.config import Environ
    ...:
    ...: os.environ['MYAPP_A_X'] = '1'
    ...: os.environ['MYAPP_A_Y'] = '2'
    ...: os.environ['MYAPP_B'] = '3'
    ...:
    ...: # env = Environ(prefix='MYAPP')
    ...: env = Environ('MYAPP')
    ...: v1 = env.copy()
    ...:
    ...: v2 = env.reduce()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 {'MYAPP_A_X': '1', 'MYAPP_A_Y': '2', 'MYAPP_B': '3'}
 
 In [4]: print(v2)
 Environ({'a': {'x': 1, 'y': 2}, 'b': 3})
 
```

### Configuration クラス
 `Configuration` クラスは、 `Namespace` クラスオブジェクトを保持します。


```
 In [2]: # %load 20_configuration.py
    ...: from cmdkit.config import Namespace, Configuration
    ...:
    ...: cfg = Configuration(A=Namespace({'x': 1, 'y': 2}),
    ...:                     B=Namespace({'x': 3, 'z': 4}))
    ...:
    ...: v1 = cfg['x'], cfg['y'], cfg['z']
    ...: v2 = cfg.namespaces['A']['x']
    ...:
    ...: # print(cfg)
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(cfg)
 Configuration(A=Namespace({'x': 1, 'y': 2}), B=Namespace({'x': 3, 'z': 4}))
 
 In [4]: print(v1)
 (3, 2, 4)
 
 In [5]: print(v2)
 1
 
```



## オプション解析
Interface クラスは  `argparse.ArgumentParser` クラスを継承しています。そのため、 `add_argument()` などのメソッドを使用してオプションや引数の定義を行うことができます。

## コマンドラインの位置引数

### 引数の型を指定 (type=)
float型とint型の２つの位置引数を受け取るようにしてみましょう。

 ppython
```
 In [1]: %load 30_args_type.py
 
    ...: APP_HELP=f"""\
    ...: {APP_USAGE}
    ...:
    ...: Options:
    ...:   -h, --help        show this message and exit.
    ...: """
    ...:
    ...: class DemoApp(Application):
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     price: float = 0.0
    ...:     lots: int = 0
    ...:
    ...:     interface.add_argument('price', type=float)
    ...:     interface.add_argument('lots', type=int)
    ...:
    ...:     def run(self):
    ...:         print(f'{self.price} x {self.lots}')
    ...:         print(f'price: {type(self.price)}')
    ...:         print(f'lots: {type(self.lots)}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] price lots
 
 Description for demo application.
 
 
 
 In [3]: %run 30_args_type.py 109.58 3
 109.58 x 3
 price: <class 'float'>
 lots: <class 'int'>
 
```

 `add_argument()` メソッドに  `type=` キーワード引数で明示的に型を指定しています。

上記のコードの次の部分です。


```
     price: float = 0.0
     lots: int = 0
 
     interface.add_argument('price', type=float)
     interface.add_argument('lots', type=int)
 
```

クラス変数ではタイプヒントを指定していて冗長に見えるかもしれませんが、 `add_argument()` メソッドは、デフォルトでは引数は文字列(str型)として処理してしまうためです。

### 位置引数の省略
デフォルトでは、引数を省略すると使用例(USAGE_TEXT)が表示されます。これを、引数されたときはデフォルト値で処理するようにしてみましょう。


```
 In [1]: %load 31_noags_default.py
 
    ...:
    ...: {APP_DESCRIPTION}
    ...: """
    ...:
    ...: APP_HELP=f"""\
    ...: {APP_USAGE}
    ...:
    ...: Options:
    ...:   -h, --help        show this message and exit.
    ...: """
    ...:
    ...: class DemoApp(Application):
    ...:     ALLOW_NOARGS = True
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     name: str = None
    ...:     interface.add_argument('name', nargs='?', default='Python')
    ...:
    ...:     def run(self):
    ...:         print(f'Hello {self.name}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:2])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Hello Python
 
 In [3]: %run 31_noags_default.py
 Hello Python
 
 In [4]: %run 03_noags_default.py Osaka
 Hello Osaka
 
```

はじめに cmkkit に位置引数がないことを許すように設定します。これには、Application クラスを継承して定義したDemoAppクラスにクラス変数  `ALLOW_NOARGS = True` を設定します。

次に、 `add_argument()` メソッドに与える引数で制御します。

上記のコードの次の部分です。


```
      name: str = None
      interface.add_argument('name', nargs='?', default='Python')
```

受け取る引数を格納する変数  `name` には、タイプヒントを使った型を明示しておき、その変数名を文字列で `add_argment()` メソッドに与えます。


### ひとつの位置引数が受け入れる個数 (nargs=)
 `nargs=` キーワード引数に与える文字で、位置引数の個数の制御ができます。

-  `?` ：ゼロ（ `0` ）もしくはひとつの位置引数を受け付ける
-  `+` ：ひとつ以上の位置引数を受け付ける
-  `*` ：ゼロ（ `0` ）もしくはひとつ以上の位置引数を受け付ける
- 数値：数値で指定した数だけ位置引数を受け付ける

### 位置引数のデフォルト値を設定 (default=)
 `default=` キーワード引数に、その位置引数のデフォルト値を与えます。

## オプションを設定
 `add_argument()` に与える変数名の指定（つまり第１引数）がダッシュ記号( `-` )で始まっていると、オプション文字列として解析されます。

これまでのコードを `--debug` オプションと `--verbose` オプションを受け取るようにしてみましょう。


```
 In [1]: %load 32_debug_verbose.py
 
    ...: """
    ...:
    ...: class DemoApp(Application):
    ...:     ALLOW_NOARGS = True
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     name: str = 'Python'
    ...:     debug: bool = False
    ...:     verbose: int = 0
    ...:
    ...:     interface.add_argument('name', nargs='?', default=name)
    ...:     interface.add_argument('-D', '--debug',
    ...:                            default=debug, action='store_true')
    ...:     interface.add_argument('-v', '--verbose',
    ...:                            default=verbose, action='count')
    ...:
    ...:     def run(self):
    ...:         print(f'DEBUG: {self.debug}')
    ...:         print(f'VERBSE: {self.verbose}')
    ...:         print(f'Hello {self.name}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 DEBUG: False
 VERBSE: 0
 Hello Python
 
 In [3]: %run 32_debug_verbose.py
 DEBUG: False
 VERBSE: 0
 Hello Python
 
 In [4]: %run 32_debug_verbose.py --debug
 DEBUG: True
 VERBSE: 0
 Hello Python
 
 In [5]: %run 32_debug_verbose.py --verbose Osaka
 DEBUG: False
 VERBSE: 1
 Hello Osaka
 
 In [6]: %run 32_debug_verbose.py --debug -v Osaka
 DEBUG: True
 VERBSE: 1
 Hello Osaka
 
 In [7]: %run 32_debug_verbose.py --debug -vvv Osaka
 DEBUG: True
 VERBSE: 3
 Hello Osaka
 
```

 `add_arguent()` メソッドの第１引数がダッシュ記号( `-` )で始まっていると、オプションとして処理されます。オプションは文字通り省略可能で、指示されたときに何らかの機能をさせるようなときに使用します。
通常、２つのダッシュ記号( `--` )で始まるオプション( `--debug` 、 `--verbose` )はロングオプションと呼ばれます。また、１つのダッシュ記号( `-` )で始まるオプションはショートオプション( `-D` ,  `-v` ) と呼ばれます。
 `add_arguent()` は２つの種類のオプションを定義することができます。

### オプシンをフラグとして扱う
上記のコードのように  `--debug` オプションが指示されたときは、クラス変数  `debug` が  `True` にセットされるようにするためには、 `add_arguent()` に  `action='store_true'` を与えます。


```
     debug: bool = False
     
     interface.add_argument('-D', '--debug',
                            default=debug, action='store_true')
                            
```

- store_true：指示されたときに True をセット
- store_false：指示されたときに False をセット

### オプションが指示された回数をカウント
上記のコードのように `--verbose` オプションが指示された回数をカウントしたいときは、 `add_arguent()` に  `action='count'` を与えます。


```
     verbose: int = 0
 
     interface.add_argument('-v', '--verbose',
                            default=verbose, action='count')
 
```

SSHコマンドの `-v` のように、指定した数が多いほどメッセージが詳細になっていくような処理などで使用されます。


### オプション引数
SSHコマンドの `-l USERNEME` のように引数をとるオプションを実装してみましょう。


```
 In [1]: %load 33_option_args.py
 
    ...:
    ...: APP_HELP=f"""\
    ...: {APP_USAGE}
    ...:
    ...: Options:
    ...:   -U, --username   Set username
    ...:   -h, --help        show this message and exit.
    ...: """
    ...:
    ...: class DemoApp(Application):
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     name: str = 'Python'
    ...:     username: str = os.getlogin()
    ...:
    ...:     interface.add_argument('name', nargs='?', default=name)
    ...:     interface.add_argument('-U', '--username', default=username)
    ...:
    ...:     def run(self):
    ...:         print(f'USER: {self.username}')
    ...:         print(f'Hello {self.name}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] [-U|--user username]  name
 
 Description for demo application.
 
 
 
 In [3]: %run 33_option_args.py Python.Osaka
 USER: goichiiisaka
 Hello Python.Osaka
 
 In [4]: %run 33_option_args.py --user guido Osaka
 USER: guido
 Hello Osaka
 
 In [5]: %run 33_option_args.py Osaka --user guido
 USER: guido
 Hello Osaka
 
```

j実はこれは、オプション引数で最小限の定義をするだけです。


```
     name: str = 'Python'
     username: str = os.getlogin()
 
     interface.add_argument('name', nargs='?', default=name)
     interface.add_argument('-U', '--username', default=username)
 
```

これで、 `--username` （あるいは `-u` )に続く単語がオプションの引数として処理されます。

位置引数とオプションは前後しても問題ありません。

### 相互排他のオプション

こんどは、 `--enable` と  `--disable` のように相互排他となるオプションを設定してみましょう。
これにはいくつかの実装方法があります。まず、 `--enable` と  `--disable` とで、同じクラス変数  `mode` にブール値を格納する方法です。


```
 In [1]: %load 34_mutually_exclusive_manual.py
 
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     debug: bool = False
    ...:     verbose: int = 0
    ...:     mode: bool = True
    ...:
    ...:     interface.add_argument('-D', '--debug',
    ...:                            default=debug, action='store_true')
    ...:     interface.add_argument('-v', '--verbose',
    ...:                            default=verbose, action='count')
    ...:
    ...:     interface.add_argument('--enable', dest='mode',
    ...:                        default=mode, action='store_true')
    ...:     interface.add_argument('--disable', dest='mode',
    ...:                        default=mode, action='store_false')
    ...:
    ...:     def run(self):
    ...:         print(f'DEBUG: {self.debug}')
    ...:         print(f'VERBSE: {self.verbose}')
    ...:         print(f'MODE: {self.mode}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] [name]
 
 Description for demo application.
 
 
 
 In [3]: %run 34_mutually_exclusive_manual.py --debug
 DEBUG: True
 VERBSE: 0
 MODE: True
 
 In [4]: %run 34_mutually_exclusive_manual.py --disable
 DEBUG: False
 VERBSE: 0
 MODE: False
 
 In [5]: %run 34_mutually_exclusive_manual.py --enable
 DEBUG: False
 VERBSE: 0
 MODE: True
 
 In [6]: %run 34_mutually_exclusive_manual.py --enable --disable
 DEBUG: False
 VERBSE: 0
 MODE: False
 
 
```

この場合、 `--enable` と  `--disable` はコマンドラインにいくつあってもエラーにはならずに、最後に指定されたものが保持されます。


通常は、argparse ではこうした場合、 `add_mutually_exclusive_group()` メソッドを用いて、オプションをグループ化します。


```
 In [1]: %load 35_mutually_exclusive.py
 
    ...:     interface.add_argument('-D', '--debug',
    ...:                            default=debug, action='store_true')
    ...:
    ...:     interface.add_argument('-v', '--verbose',
    ...:                            default=verbose, action='count')
    ...:
    ...:     enable: bool = False
    ...:     disable: bool = False
    ...:     group = interface.add_mutually_exclusive_group()
    ...:     group.add_argument('--enable', action='store_true')
    ...:     group.add_argument('--disable', action='store_true')
    ...:
    ...:     def run(self):
    ...:         print(f'DEBUG: {self.debug}')
    ...:         print(f'VERBSE: {self.verbose}')
    ...:         print(f'enable: {self.enable}')
    ...:         print(f'disable: {self.disable}')
    ...:
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] [name]
 
 Description for demo application.
 
 
 
 In [3]: %run 35_mutually_exclusive.py --debug
 DEBUG: True
 VERBSE: 0
 enable: False
 disable: False
 
 In [4]: %run 35_mutually_exclusive.py --disable
 DEBUG: False
 VERBSE: 0
 enable: False
 disable: True
 
 In [5]: %run 35_mutually_exclusive.py --enable
 DEBUG: False
 VERBSE: 0
 enable: True
 disable: False
 
```

 `add_mutually_exclusive_group()` メソッドで作成したグループオブジェクトにも `add_argument()` にメソッドがあり、ここで `dest='変数名'` と与えるとオプションの結果を格納する変数を指定することができます。

 `add_mutually_exclusive_group()` メソッドでグループを作るときに、 `required=True` を与えると、グループのうちどれかひとつは必須となります。つまり、この場合は、 `--enable` /  `--disable` のいずれかを与えられることを要求します。

動作的には問題ないのですが、このままでは相互排他のオプションを同時に与えたときは、
次のように何も出力されないため’ユーザに何が起きたのかを知らせることができません。


```
 
  In [6]: %run 35_mutually_exclusive.py --enable --disable
  
  In [7]:
```

內部的には argparser が  `ArgumentError` の例外を発生させています。


```
 In [7]: DemoApp.interface.parse_args(['--enable', '--disable'])
 ---------------------------------------------------------------------------
 ArgumentError                             Traceback (most recent call last)
 ~/anaconda3/envs/tutorials/lib/python3.9/argparse.py in parse_known_args(self, args, namespace)
    1850             try:
 -> 1851                 namespace, args = self._parse_known_args(args, namespace)
    1852             except ArgumentError:
 (中略)
  ArgumentError: argument --disable: not allowed with argument --enable
  
  During handling of the above exception, another exception occurred:
  
  ArgumentError                             Traceback (most recent call last)
  <ipython-input-8-d62b152479db> in <module>
  ----> 1 DemoApp.interface.parse_args(['--enable', '--disable'])
  (中略)
  ~/anaconda3/envs/tutorials/lib/python3.9/site-packages/cmdkit/cli.py in error(self, message)
       98     # simple raise, no printing
       99     def error(self, message: str) -> None:
  --> 100         raise ArgumentError(message)
  
  ArgumentError: argument --disable: not allowed with argument --enable
```

これを cmdkit が捕獲して  `log.critical()` でメッセージを出力しているのですが、ロギングの設定がまだされていないため
何も出力されないわけです。


```
 import logging
 
 # 標準出力(コンソール)にログを出力するハンドラを生成する
 log_stderr = logging.StreamHandler(sys.stderr)
 log_stderr.setLevel(logging.WARNING)
 log_stderr.setLevel(logging.CRITICAL)
 
 # ハンドラをロガーに紐づける
 log.addHandler(log_stderr)
 
```

ロギングハンドラーについては Python 公式ドキュメントの [logging.handlers --- ロギングハンドラ ](https://docs.python.org/ja/3/library/logging.handlers.html#module-logging.handlers) を参照してください。

 bash
```
 % python 36_mutually_exclusive_with_logging.py --enable
 DEBUG: False
 VERBSE: 0
 enable: True
 disable: False
 % python 36_mutually_exclusive_with_logging.py --disable
 DEBUG: False
 VERBSE: 0
 enable: False
 disable: True
 % python 36_mutually_exclusive_with_logging.py --disable --enable
 argument --enable: not allowed with argument --disable
 
```

Application クラスのクラス変数  `log_critical` が、デフォルトでは’  `log.critical()` に設定されていることを思い出してみましょう。もっとシンプルに `print()` 関数を呼び出すようにすることもできます。
 `print()` 関数に  `file=sys.stderr` を与えると標準エラー出力に書き出すようになります。この引数を `functools.partial()` でまとめることができます。


```
 In [2]: # %load functools_partial_demo.py
    ...: import sys
    ...: import functools
    ...:
    ...: log_critical = functools.partial(print, file=sys.stderr)
    ...:
    ...: log_critical('Hello World.')
    ...: # print('Hello World.', file=sys.stderr)
    ...:
 Hello World.
 
```

 bash
```
 % python 37_mutually_exclusive_with_stderr.py --disable --enable
 argument --enable: not allowed with argument --disable
 
 % python 37_mutually_exclusive_with_stderr.py --disable --enable 2>/dev/null
 %
```

### 選択肢を制限する
位置引数やオプション引数でいくつかの選択肢の中から選ばせたい場合があります。 
通常であれば、こうした場合 argparse では、  `add_argument()` メソッドに  `choices` キーワード引数を渡します。


```
 In [1]: %load 38_choices.py
 
    ...: APP_HELP=f"""\
    ...: {APP_USAGE}
    ...:
    ...: Options:
    ...:   -h, --help        show this message and exit.
    ...: """
    ...:
    ...: class DemoApp(Application):
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     name: str = 'Python'
    ...:     color: str = 'green'
    ...:
    ...:     interface.add_argument('name', nargs='?', default=name)
    ...:     interface.add_argument('-c', '--color', default=color,
    ...:                            choices=['green', 'yellow', 'red'])
    ...:
    ...:     def run(self):
    ...:         print(f'COLOR: {self.color}')
    ...:         print(f'Hello {self.name}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] [-c|--color <green|yellow|red>]  name
 
 Description for demo application.
 
 
 
 In [3]: %run 38_choices.py --color yellow
 COLOR: yellow
 Hello Python
 
 In [4]: %run 38_choices.py --color red
 COLOR: red
 Hello Python
 
```

一見するとうまくいっているように見えますが、これも相互排他オプションと同じで、argparse が発生させる例外が cmdkit によって捕獲され  `log.ceritical()` で出力されるため、ロギング設定がされていないとメッセージが隠されてしまいます。


```
 In [5]: DemoApp.interface.parse_args(['--color'])
 ---------------------------------------------------------------------------
 ArgumentError                             Traceback (most recent call last)
 (中略)
 ArgumentError: argument -c/--color: expected one argument
 
 During handling of the above exception, another exception occurred:
 
 ArgumentError                             Traceback (most recent call last)
 <ipython-input-5-3e71c07867aa> in <module>
 ----> 1 DemoApp.interface.parse_args(['--color'])
 (中略)
 ArgumentError: argument -c/--color: expected one argument
 
 In [6]: DemoApp.interface.parse_args(['--color', 'black'])
 ---------------------------------------------------------------------------
 ArgumentError                             Traceback (most recent call last)
 (中略)
 ArgumentError: argument -c/--color: invalid choice: 'black' (choose from 'green', 'yellow', 'red')
 
 During handling of the above exception, another exception occurred:
 
 ArgumentError                             Traceback (most recent call last)
 (中略)
 ArgumentError: argument -c/--color: invalid choice: 'black' (choose from 'green', 'yellow', 'red')
 
 In [7]: %run 38_choices.py --color
 
 In [8]:
 
 In [8]: %run 38_choices.py --color balck
 
 In [9]:
 
```

ロギング設定を追加して再度実行してみます。

```
 import logging
 
 # 標準出力(コンソール)にログを出力するハンドラを生成する
 log_stderr = logging.StreamHandler(sys.stderr)
 log_stderr.setLevel(logging.WARNING)
 log_stderr.setLevel(logging.CRITICAL)
 
 # ハンドラをロガーに紐づける
 log.addHandler(log_stderr)
 
```

 bash
```
 % python 39_choices_with_logging.py -c green
 COLOR: green
 Hello Python
 % python 39_choices_with_logging.py --color yellow
 COLOR: yellow
 Hello Python
 % python 39_choices_with_logging.py --color yellow red
 COLOR: yellow
 Hello red
 % python 39_choices_with_logging.py --color black
 argument -c/--color: invalid choice: 'black' (choose from 'green', 'yellow', 'red')
 
```

この場合でも、DemoAppクラスのクラス変数 `log_critical` に `print()` を設定することで、ロギング設定をしなくても標準エラー出力に書き出すようにできます。

 bash
```
 % python 40_choices_with_stderr.py
 Usage: demo_simple [-h|--help] [-c|--color <green|yellow|red>]  name
 
 Description for demo application.
 
 
 % python 40_choices_with_stderr.py --color black
 argument -c/--color: invalid choice: 'black' (choose from 'green', 'yellow', 'red')
 
 
```


もうひとつ別の方法でも実装することができます。この場合は、 `add_argument(()` に  `action=` キーワード引数にカスタマイズアクションを与えることで擬似的に処理することができます。

まず、カスタマイズアクションを作成します。
 `--color` があるのに色していがないパターンと、許容する色ではないものが指定された場合はUSAGE_TEXTを表示させて終了しています。



```
 class ChoiceAction(argparse.Action):
     ACCEPTABLE_CHOICES=['green', 'yellow', 'red']
     def __call__(self, parser, namespace, values=None, options_string=None):
         if values is not None and values in ACCEPTABLE_CHOICES:
             setattr(namespace, self.dest, values)
         else:
             print(f"invalid {values} in {self.ACCEPTABLE_CHOICES}")
             print(APP_USAGE)
             sys.exit(exit_status.bad_argument)
                         
```

このアクションを  `add_argument(()` に  `action=` キーワード引数に与えます。


```
     color: str = 'green'
 
     interface.add_argument('-c', '--color', nargs='?', default=color,
                            action=ChoiceAction)
```




```
 In [1]: %load 41_choices_manualy.py
 
    ...: class ChoiceAction(argparse.Action):
    ...:     def __call__(self, parser, namespace, values=None, options_string=None):
    ...:         if values is not None and values in ['green', 'yellow', 'red']:
    ...:             setattr(namespace, self.dest, values)
    ...:         else:
    ...:             print(f"invalid {values} in ('green', 'yellow', 'red')")
    ...:             print(APP_USAGE)
    ...:             sys.exit(0)
    ...:
    ...: class DemoApp(Application):
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     name: str = 'Python'
    ...:     color: str = 'green'
    ...:
    ...:     interface.add_argument('name', nargs='?', default=name)
    ...:     interface.add_argument('-c', '--color', nargs='?', default=color,
    ...:                            action=ChoiceAction)
    ...:
    ...:     def run(self):
    ...:         print(f'COLOR: {self.color}')
    ...:         print(f'Hello {self.name}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] [-c|--color <green|yellow|red>]  name
 
 Description for demo application.
 
 
 
 In [3]: %run 41_choices_manualy.py --color
 invalid None in ('green', 'yellow', 'red')
 Usage: demo_simple [-h|--help] [-c|--color <green|yellow|red>]  name
 
 Description for demo application.
 
 
 
 In [4]: %run 41_choices_manualy.py --color black
 invalid black in ('green', 'yellow', 'red')
 Usage: demo_simple [-h|--help] [-c|--color <green|yellow|red>]  name
 
 Description for demo application.
 
 
 
 In [5]: %run 41_choices_manualy.py --color red
 COLOR: red
 Hello Python
 
```

### FileType オブジェクト
 `argparse.FileType` クラスは  `add_argument()` メソッドの  `type` 引数に渡すことができるオブジェクトを生成します。 
type が FileType オブジェクトである引数はコマンドライン引数を、指定されたモード、バッファーサイズ、エンコーディング、エラー処理でファイルをオープンします。:


```
 In [1]: %load 42_filetype.py
 
    ...: {APP_USAGE}
    ...:
    ...: Options:
    ...:   -h, --help        show this message and exit.
    ...: """
    ...:
    ...: class DemoApp(Application):
    ...:     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)
    ...:
    ...:     infile: argparse.FileType = None
    ...:     outfile: argparse.FileType = None
    ...:
    ...:     interface.add_argument('--infile', type=argparse.FileType('r'))
    ...:     interface.add_argument('--outfile',
    ...:                            type=argparse.FileType('w', encoding='UTF-8')
    ...: )
    ...:
    ...:     def run(self):
    ...:         print(f'infile: {self.infile}')
    ...:         print(f'outile: {self.outfile}')
    ...:
    ...: def main() -> int:
    ...:     return DemoApp.main(sys.argv[1:])
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 Usage: demo_simple [-h|--help] [--infie path] [--outfile path]
 
 Description for demo application.
 
 
 
 In [3]: %run 42_filetype.py --infile a --outfile b
 infile: <_io.TextIOWrapper name='a' mode='r' encoding='UTF-8'>
 outile: <_io.TextIOWrapper name='b' mode='w' encoding='UTF-8'>
 
 
```

## サブコマンドを実装

git のようにサブコマンドをもコンソールアプリケーションを作ってみましょう。
まず、ディレクトリ  `dbmanager` を作成します。ディレクトリ名に制約はないので何でも構いません。

 bash
```
 $ mkdir dbmanager
 
```


はじめに、ロギング設定のモジュール  `logging.py` を作成しておきます。
 dbmanager/dblogging.py
```
 import sys
 import logging
 from cmdkit.app import log
 
 log_stderr = logging.StreamHandler(sys.stderr)
 log_stderr.setLevel(logging.WARNING)
 log_stderr.setLevel(logging.CRITICAL)
 
 log.addHandler(log_stderr)
 
```

ここで、 `initialize.py` と  `dump.py` の２つのコマンドを作成します。


 dbmanager/initialize,py
```
 """Initialize database """
 
 import sys
 from cmdkit.app import Application, exit_status
 from cmdkit.cli import Interface
 from dblogging import log
 
 NAME = 'initialize'
 PROGRAM = 'dbmanager initialize'
 PADDING = ' ' * len(PROGRAM)
 
 USAGE = f"""\
        {PROGRAM} FILE
        {PADDING} [--verbose] [--debug]
        {PADDING} [--help]
 
 """
 
 HELP = f"""\
 {USAGE}
 
 arguments:
 FILE                 Path to file for database
 
 options:
 -v, --verbose        Show info messages.
 -d, --debug          Show debug messages.
 -h, --help           Show this message and exit.
 """
 
 class DBInit(Application):
 
     interface = Interface(PROGRAM, USAGE, HELP)
 
     dbfile: str = ''
     interface.add_argument('dbfile', nargs=1, default=dbfile)
 
     debug: bool = False
     interface.add_argument('-d', '--debug', action='store_true')
 
     verbose: bool = False
     interface.add_argument('-v', '--verbose', action='store_true')
 
     def run(self) -> int:
         print(f'DEBUG: {self.debug}')
         print(f'VERBOSE: {self.verbose}')
         print(f'DB initialize DB: {self.dbfile}')
 
 DBInit.__doc__ = __doc__
 
 if __name__ == '__main__':
     DBInit.main(sys.argv[1:])
     
```

 dbmanager/dump.py
```
 """dump database"""
 
 import ys
 from cmdkit.app import Application, exit_status
 from cmdkit.cli import Interface
 from dblogging import log
 
 NAME = 'dump'
 PROGRAM = 'dbmanager dump'
 PADDING = ' ' * len(PROGRAM)
 
 USAGE = f"""\
        {PROGRAM} DBNAME
        {PADDING} [--verbose] [--debug]
        {PADDING} [--help]
 
 """
 
 HELP = f"""\
 {USAGE}
 
 arguments:
 DBNAME               Name of Database
 options:
 -v, --verbose        Show info messages.
 -d, --debug          Show debug messages.
 -h, --help           Show this message and exit.
 """
 
 class DBDump(Application):
 
     interface = Interface(PROGRAM, USAGE, HELP)
 
     dbname: str = ''
     interface.add_argument('dbname', nargs=1, default=dbname)
 
     debug: bool = False
     interface.add_argument('-d', '--debug', action='store_true')
 
     verbose: bool = False
     interface.add_argument('-v', '--verbose', action='store_true')
 
     def run(self) -> int:
         print(f'DEBUG: {self.debug}')
         print(f'VERBOSE: {self.verbose}')
         print(f'Dumo DB: {self.dbname}')
 
 DBDump.__doc__ = __doc__
 
 if __name__ == '__main__':
     DBDump.main(sys.argv[1:])
     
```

この２つのコマンドを独立していて、それぞれ単独に引数を与えることができます。

 bash
```
 % python dbmanager/initialize.py
        dbmanager initialize FILE
                             [--verbose] [--debug]
                             [--help]
 
 
 % python dbmanager/initialize.py --help
        dbmanager initialize FILE
                             [--verbose] [--debug]
                             [--help]
 
 
 
 arguments:
 FILE                 Path to file for database
 
 options:
 -v, --verbose        Show info messages.
 -d, --debug          Show debug messages.
 -h, --help           Show this message and exit.
 
 % python dbmanager/initialize.py --debug sample
 DEBUG: True
 VERBOSE: False
 DB initialize DB: ['sample']
  
```

 bash
```
 % python dbmanager/dump.py
        dbmanager dump DBNAME
                       [--verbose] [--debug]
                       [--help]
 
 
 % python dbmanager/dump.py --help
        dbmanager dump DBNAME
                       [--verbose] [--debug]
                       [--help]
 
 
 
 arguments:
 DBNAME               Name of Database
 
 options:
 -v, --verbose        Show info messages.
 -d, --debug          Show debug messages.
 -h, --help           Show this message and exit.
 
 % python dbmanager/dump.py sample
 DEBUG: False
 VERBOSE: False
 Dumo DB: ['sample']
 
```

ここに、 `dbmanager/cli.py` を作成して、これらのスクリプトをサブコマンドで呼び出せるようにしてみます。

 dbmanager/c.py
```
 import sys
 from cmdkit.app import Application
 from cmdkit.cli import Interface, ArgumentError
 
 # commands
 from .initialize import DBInit
 from .dump import DBDump
 from .dblogging import log
 
 COMMANDS = {
     'initialize': DBInit,
     'dump': DBDump,
 }
 
 PROGRAM = 'dbmanager'
 
 USAGE = f"""\
 usage: {PROGRAM} <command> [<args>...]
        {PROGRAM} [--help]
 
 database manager.
 """
 
 HELP = f"""\
 {USAGE}\
 
 commands:
 initialize             {DBInit.__doc__}
 dumo                   {DBDump.__doc__}
 
 options:
 -h, --help             Show this message and exit.
 
 Use the -h/--help flag with the above commands to
 learn more about their usage.
 
 """
 
 class CompletedCommand(Exception):
     pass
 
 class DBManager(Application):
     interface = Interface(PROGRAM, USAGE, HELP)
 
     command: str = None
     interface.add_argument('command')
 
     exceptions = {
         CompletedCommand: (lambda exc: int(exc.args[0])),
     }
 
 
     def run(self) -> None:
         try:
             status = COMMANDS[self.command].main(sys.argv[2:])
             raise CompletedCommand(status)
 
         except KeyError as error:
             cmd, = error.args
             raise ArgumentError(f'"{cmd}" is not an available command.')
 
 def main() -> int:
     return DBManager.main(sys.argv[1:2]) 
 
```

 bash
```
 % tree -I __pycache__ dbmanager
 dbmanager
 ├── __init__.py
 ├── cli.py
 ├── dblogging.py
 ├── dump.py
 └── initialize.py
 
```

モジュール  `dbmaager.cli` の `main()` を呼び出すスクリプトを  `dbmanager_cli.py` とします。

 dbmanager_cli.py
```
 import re
 import sys
 from dbmanager.cli import main
 if __name__ == '__main__':
     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
     sys.exit(main())
```



 bash
```
 % python dbmanager_cli.py --help
 usage: dbmanager <command> [<args>...]
        dbmanager [--help]
 
 database manager.
 
 commands:
 initialize             Initialize database
 dump                   dump database
 
 options:
 -h, --help             Show this message and exit.
 
 Use the -h/--help flag with the above commands to
 learn more about their usage.
 
 
 % python dbmanager_cli.py initialize --help
        dbmanager initialize FILE
                             [--verbose] [--debug]
                             [--help]
 
 
 
 arguments:
 FILE                 Path to file for database
 
 options:
 -v, --verbose        Show info messages.
 -d, --debug          Show debug messages.
 -h, --help           Show this message and exit.
 
 % python dbmanager_cli.py dump  --help
        dbmanager dump DBNAME
                       [--verbose] [--debug]
                       [--help]
 
 
 
 arguments:
 DBNAME               Name of Database
 
 options:
 -v, --verbose        Show info messages.
 -d, --debug          Show debug messages.
 -h, --help           Show this message and exit.
 
```



## まとめ
cmdkit は argparse をうまくラッピングしてクラス定義の中で使用できるようにしているため、小規模なスクリプトから、複雑なサブコマンドをもつアプリケーションまで一貫性を保ちながら開発することができます。


## 参考
- cmdkit
  - [ソースコード ](https://github.com/glentner/CmdKit)
  - [ドキュメント ](https://cmdkit.readthedocs.io/en/latest/)
- [Python 公式ドキュメント - argparse チュートリアル ](https://docs.python.org/ja/3/howto/argparse.html)
- [Pythonチュートリアル: オプション解析モジュール]
- [TOML オフィシャルサイト ](https://toml.io/en/)
- [YAML オフィシャルサイト　](https://yaml.org/)
- [JSON オフィシャルサイト ](https://www.json.org/json-en.html)
- [Command Line Interface Guidelines ](https://clig.dev/)


