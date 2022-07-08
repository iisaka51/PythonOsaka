pshellモジュールを使って外部コマンドを呼び出してみよう
=================
## pshellモジュールについて

Linuxなどでよく利用されるシェルのひとつに bash コマンドがあります。bash コマンドはコンソール端末での基本的なユーザインタフェースを提供します。 bash コマンドはスクリプトを作成することもでこますが、一般に、数行以上のスクリプトを書くたには適していないと言われています。自動テストや自動文書化がサポートされておらず、バグが発生しやすい文法や、デバッグツールがないために echo によるデバッグライトが多様されたりするため保守性が低くなります。

一方、Pythonは非常に堅牢な言語です。しかし、bashでは1行で実行できる操作でも、Pythonでos、shutil、subprocessなどを使って書く必要があったりするなど不釣り合いな量のコードが必要になります。

pshell は、伝統的に bash スクリプトで行われていたすべてのタスクを実行するための、統一された、堅牢でコンパクトな Python API を提供することで、両方の世界の長所を手に入れています。

pshell はsubprocess の代替モジュールではありません。また、対話型シェルでもありません。しかし、お気に入りの python/ipython/jupyter 端末から使用することができます。

pshell は次のような機能があります。

- すべてのアクションは、ロギングモジュールを使って記録されます。これは、テストやデバッグに非常に有効です。pshell を起動する前に、logging モジュールを初期化し、logoglevel を INFO または DEBUG に設定することを強くお勧めします。
- すべてのファイルパスには、bash 形式の環境変数を含めることができ、これらはその場で解決されます。環境変数の解決に失敗すると、 `EnvironmentError` 例外 が発生します。これで、恐ろしい  `rm -rf $MISSPELLED/*` から逃れることができます。
- コアライブラリの関数は、ラップされ、強化、洗練されています、ときにはより健全なデフォルトの動作に変更されます。
- shutil や glob など、pathlib をサポートしていない標準ライブラリ関数をラップする際にも、pathlib を完全にサポートしています。

pshell モジュールは Python 3.6以降で動作します。
必要な外部モジュールは、 psutil 5.6 以降を利用していま。
Python 3.6 の場合のみ、 contextvars backport 2.0 以降が必要です。

## インストール

pshell モジュールは pip コマンドでインストールを行います。

 bash
```
 $ pip install pshell
 
```

## pshell の使用方法

subprocess を使って外部コマンドを実行する場合、次のようなコードになります。


```
 n [2]: # %load 01_intro_subprocess.py
    ...: import pshell as sh
    ...: import subprocess
    ...: import shlex
    ...:
    ...: cmd = 'ls /tmp'
    ...: v1 = subprocess.call(shlex.split(cmd))
    ...: # print(v1)
    ...:
 FirstBootAfterUpdate		current_time.txt
 FirstBootCleanupHandled		error.txt
 _MEIubHlfI			fseventsd-uuid
 com.apple.launchd.9WKFMCb6kv	kjnsdfBSDFBo2pnwvpd
 com.apple.launchd.dx5ZAvQMdp	powerlog
 com.brave.Browser.Sparkle.pid	sdfvSDFVGver27zv93
 com.google.Keystone		some_logfile.log
 
 In [3]: print(v1)
 0
 
```

これを pshell を使って記述すると、次のようになります。


```
 In [2]: # %load 02_intro_pshell.py
    ...: import pshell as sh
    ...:
    ...: v1 = sh.call('ls /tmp')
    ...: # print(v1)
    ...:
 FirstBootAfterUpdate		current_time.txt
 FirstBootCleanupHandled		error.txt
 _MEIubHlfI			fseventsd-uuid
 com.apple.launchd.9WKFMCb6kv	kjnsdfBSDFBo2pnwvpd
 com.apple.launchd.dx5ZAvQMdp	powerlog
 com.brave.Browser.Sparkle.pid	sdfvSDFVGver27zv93
 com.google.Keystone		some_logfile.log
 
 In [3]: print(v1)
 0
 
```

コマンドラインをそのまま記述できるため、読みやすくなっているのがわかりますよね。

それでは、これ以降 psehll の機能を説明してゆきましょう。

## 環境変数
Pyhon スクリプトで環境変数を扱うとき、以外に面倒な手続きが必要になりますが、pshell では統一的で直感的なAPIを使って柔軟に記述することできるようになります。

### source()
bashコマンドの `source  bash_file` をエミュレートします。コマンドの標準出力がある場合は、標準エラーにリダイレクトされます。取得した変数は  `os.environment` に追加され、その後に起動されるサブプロセスに公開されます。
#### この関数は Windows では動作しません
スクリプトは常にbashで実行されます。これは、Ubuntuやその派生機種で実行する場合も同様で、/bin/shは実際にはdashです。スクリプトはbash の errexit, pipefail, nounsetを設定されてから実行されます。


```
 source(bash_file: Union[str, pathlib.Path], *, stderr: <class 'IO'> = None) -> None
```

- **bash_file**：bashファイルへのパス。環境変数を含むことができます。
- **stderr**：標準エラーのファイルハンドルです。 `sys.stderr` (標準エラー出力）の場合は省略できます。OSレベルのファイル記述子によってバックアップされなければならない  `subprocess.call()` の同じパラメータとは異なり、これは例えば `io.StringIO` のような疑似ストリームにすることができます。

### putenv()
環境変数を設定します。新しい変数は、現在のプロセスとそこからフォークされたすべてのサブプロセスに  現在のプロセスとそこからフォークされたすべてのサブプロセスに公開されます。
 `os.putenv()` とは異なり、このメソッドは環境変数を設定値に解決し、現在のプロセスからすぐに見えるようになります。


```
 putenv(key: str, value: Union[str, pathlib.Path, None]) → None
```

- **key**：環境変数名
- **value**：環境変数へ設定する値。値を設定する場合は文字列、変数を削除する場合は  `None` を与えます。
  - 設定する値には、  `` ${FOO}.${BAR} `` のように、他の変数を参照することができます。
  -  `pathlib.Path` オブジェクトは透過的に文字列に変換されます。

### oerride_env()
環境変数を上書きしするコンテキストマネージャー。コンテキストが終了すると環境変数を元の値に戻します。


```
 override_env(key: str, value: Union[str, pathlib.Path, None]) → Iterator[None]
```


- **key**：環境変数名
- **value**：環境変数へ設定する値。値を設定する場合は文字列、変数を削除する場合は  `None` を与えます。
  - 設定する値には、  `` ${FOO}.${BAR} `` のように、他の変数を参照することができます。
  -  `pathlib.Path` オブジェクトは透過的に文字列に変換されます。


```
 In [2]: # %load 03_override_env.py
    ...: import os
    ...: import pshell as sh
    ...:
    ...: sh.putenv('X', 'foo')
    ...: v1 = os.environ['X']
    ...:
    ...: with sh.override_env('X', 'bar'):
    ...:     v2 = os.environ['X']
    ...:
    ...: v3 = os.environ['X']
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: print(v1)
 foo
 
 In [4]: print(v2)
 bar
 
 In [5]: print(v3)
 foo
 
```

### resolve_env()
対象となる文字列または  `pathlib.Path` に含まれるすべての環境変数を解決します。


```
 resolve_env(vaname)
```

- **varname**：文字列もしくは環境変数を含む可能性がある `pathlib.Path` オブジェクト

このコマンドは常にbashの構文である  `$VARNAME` または  `${VARNAME}` を使用します。これはWindowsでも同じです。Windowsのネイティブシンタックスである  `%VARNAME%` はサポートされていません。
 `os.path.expandvars` とは異なり、未定義の変数は空の文字列に置き換えられるのではなく、例外が発生します。



## ファイル操作
pshell モジュールはディレクトリの作成/削除などといった操作を行うヘルパー関数が提供されています。

- **remove() **：ファイルやディレクトリを削除する
- **chdir() **：ディレクトリを移動する
- **pushd() **：指定したディレクトリに移動するコンテキストマネージャ。コンテキストが終了すると元のディレクトリに戻る
- **move() **：ファイルやディレクトリを移動する
- **copy() **：ファイルをコピーする
- **backup() **：ファイルをコピーする
- **symlink() **；シンボリックリンクを作成する
- **exists() **：ファイルやディレクトリが存在するか確認する
- **lexists() **：
- **mkdir() **：ディレクトリを作成する
- **owner() **：ファイルを所有しているユーザのユーザ名を返す
- **open()**：ファイルをオープンする

### remove()
ァイルやディレクトリを削除します。

```
 remove(path: Union[str, pathlib.Path], *, recursive: bool = False, force: bool = True, 
 ignore_readonly: bool = False, rename_on_fail: bool = False)
```


- **path**: 対象のファイルやディレクトリのパス
- **recursive**: True の場合、ディレクトリを再帰的に処理する
- **force**: True の場合、対象が存在しないときに OSError 例外を発行しない
- **ignore_readonly**: True の場合、読み取り専用フラグが設定されたファイルやディレクトリも削除する
- **rename_on_fail**: Trueの場合、削除に失敗しても OSError 例外を発生させない
  - これは通常次のケースで起こります。
    - ユーザーがファイルやディレクトリの削除に十分な権限を持っていない場合
    - NFSロックの場合
  - こうした場合では、ファイル名は <path>.DELETEME.<timestamp> に変更されます
  - リネームにも失敗した場合は、OSErrorを発生させます。

次の例外が発生することがあります。
- **FileNotFoundError**: force が False の場合で、path が存在しないとき
- **OSError**:
        - - rename_on_fail が False の場合は、path が削除できなかったとき
        - - rename_on_fail が True の場合は、path の削除やファイル名変更のいずれかが失敗したとき
### chdir()
指定したディレクトリへ移動します。


```
 chdir(path: Union[str, pathlib.Path]) -> None
```

- **path**：ディレクトリパス

### pushd()
指定したディレクトリに移動するコンテキストマネージャです。コンテキストから離れるときには、元のディレクトリに戻されます。


```
 pushd(path: Union[str, pathlib.Path]) -> Iterator[NoneType]
```

- **path**：ディレクトリパス

### move()
ファイルやディレクトリ(src)を別の場所(dst)に再帰的に移動します。移動先がディレクトリまたはディレクトリへのシンボリックリンクの場合、srcはそのディレクトリ内に移動します。
ディレクトリは移動先のディレクトリに存在しているとエラーになります。
移動先のディレクトリが既に存在していても、それがディレクトリでない場合は、
 `os.rename()` のセマンティクスによっては、上書きされる可能性があります。


```
 move(src: Union[str, pathlib.Path], dst: Union[str, pathlib.Path]) -> None
```

- **src**：ファイルやディレクトリのパス
- **dst**：ファイルやディレクトリのパス

### copy()
ファイルやディレクトリを再帰的にコピーします。src が通常のファイルで、dst がディレクトリの場合、src と同じ basename のファイルが指定されたディレクトリに作成（または上書き）されます。パーミッションビットや最終更新日もコピーされます。シンボリックリンクは維持されます。ユーザーとグループは破棄されます。


```
 copy(src: Union[str, pathlib.Path], dst: Union[str, pathlib.Path], *, ignore=None) -> None
```

- **src**：ファイルやディレクトリのパス
- **dst**：ファイルやディレクトリのパス
- **ignore**：ディレクトリをコピーするときにのみ有効で、対象としないファイルやディレクトリを指示
  - カレントディレクトリに相対的なディレクトリ名やファイル名のシーケンス

この関数は、srcがディレクトリの場合、bashとは若干動作が異なります。  bash ではdstが存在するかどうかで動作が変わります。

 check_bash_copy.sh
```
 mkdir /tmp/work
 cd /tmp/work
 
 mkdir foo
 touch foo/hello.txt
 echo "---- 1st copy..."
 cp -r foo bar
 find .
 
 echo "---- 2nd copy..."
 cp -r foo bar
 find .
 
 cd /tmp
 rm -rf /tmp/work
 
```

cp コマンドを２回実行しています。初回は対象のディレクトリが存在していませんが、２回目では初回の結果でディレクトリが存在することに注目してください。

 bash
```
 $ bash check_bash_copy.sh
 ---- 1st copy...
 .
 ./foo
 ./foo/hello.txt
 ./bar
 ./bar/hello.txt
 ---- 2nd copy...
 .
 ./foo
 ./foo/hello.txt
 ./bar
 ./bar/foo
 ./bar/foo/hello.txt
 ./bar/hello.txt
```



```
 In [2]: # %load 04_copy.py
    ...: import pshell as sh
    ...:
    ...: sh.mkdir('/tmp/work/foo')
    ...: with sh.pushd('/tmp/work'):
    ...:     sh.call('touch foo/hello.txt')
    ...:     print('--- 1st copy ')
    ...:     sh.copy('foo', 'bar')
    ...:     sh.call('find . ')
    ...:     print('--- 2nd copy ')
    ...:     sh.copy('foo', 'bar')
    ...:     sh.call('find . ')
    ...:
    ...: sh.remove('/tmp/work', recursive=True)
    ...:
 --- 1st copy
 .
 ./foo
 ./foo/hello.txt
 ./bar
 import pshell as sh
 ./bar/hello.txt
 --- 2nd copy
 ---------------------------------------------------------------------------
 FileExistsError                           Traceback (most recent call last)
 (中略)
 FileExistsError: [Errno 17] File exists: 'bar'
 
```

この関数は、代わりに常に完全なデスティネーションパスを要求します。2回目の  `copy('foo', 'bar')` の呼び出しでは、  `bar` がすでに存在しているために `FileExistsError` 例外が発生します。これは  `` bar `` が既に存在しているからです。

### backup()


```
 backup(path, *, suffix=None, force=False, action='copy')
```

- **path**：バックアップするファイルまたはディレクトリです。文字列または  `pathlib.Path` オブジェクトを指定
- **suffix**：バックアップファイルの接尾辞を指定。デフォルト： .YYYYMMDD-HHMMSS
- **force**：ファイルが存在しない場合は何もしません（例外を発生しません）
- **action**：copy あるいは move を指定

path が存在していないときで、 `force=False` の場合に  `FileNotFoundError` の例外が発生します。

- 戻り値：リネームされたパス、またはバックアップが行われなかった場合には None が返されます。
  - pathが  `pathlib.Path` オブジェクトであれば、戻り値も  `pathlib.Path` オブジェクトになります。


### symlink()
srcを指すdstという名前のシンボリックリンクを作成します。
この機能は、POSIX互換のファイルシステムであるUnixでのみ動作します。


```
 symlink(src: Union[str, pathlib.Path], dst: Union[str, pathlib.Path], *, 
 force: bool = False, abspath: bool = False) -> None
```

- **force**： trueの場合、前のdstが存在し、それが異なるシンボリックリンクのとき削除する
  - 同じシンボリックリンクであれば、競合状態を防ぐために置き換えない
- **abspath**： False の場合、可能な限り最短の相対リンクを構築する
  - True の場合は、絶対パスを使用してリンクを生成します。
  - これは，src と dst が絶対パスか相対パスか，また現在の作業状況に関わらず現在のディレクトリに関係なく行われます。


```
 In [11]: # %load 05_symlink.py
     ...: import pshell as sh
     ...:
     ...: sh.mkdir('/tmp/work')
     ...: sh.symlink('/tmp/work/foo', '/tmp/work/bar')
     ...: sh.call('ls -l /tmp/work')
     ...: sh.remove('/tmp/work', recursive=True)
     ...:
     ...: sh.mkdir('/tmp/work')
     ...: sh.symlink('/tmp/work/foo', '/tmp/work/bar', abspath=True)
     ...: sh.call('ls -l /tmp/work')
     ...: sh.remove('/tmp/work', recursive=True)
     ...:
 total 0
 lrwxr-xr-x  1 goichiiisaka  wheel  3 Sep 16 15:15 bar -> foo
 total 0
 lrwxr-xr-x  1 goichiiisaka  wheel  13 Sep 16 15:15 bar -> /tmp/work/foo
 
```

### exists()
 `os.path.exists` のラッパー関数で、環境変数の自動解決やロギングを行います。

```
 exists(path: Union[str, pathlib.Path]) -> bool
```

- **path**: ファイルやディレクトリのパス

path が実在するパスかオープンしているファイル記述子を参照している場合 True を返します。壊れたシンボリックリンクについては False を返します。一部のプラットフォームでは、たとえ path が物理的に存在していたとしても、要求されたファイルに対する  `os.stat()` の実行権がなければこの関数が False を返すことがあります。

### lexists()
 `os.path.lexists` のラッパー関数で、環境変数の自動解決やロギングを行います。

```
 exists(path: Union[str, pathlib.Path]) -> bool
```

- **path**: ファイルやディレクトリのパス

path で与えたファイルやディレクトリが存在するときは  `True` を返し、それ以外は `False` を返します。

path が実在するパスなら  `True` を返します。壊れたシンボリックリンクについては  `True` を返します。  `os.lstat()` がない環境では  `os.exists()` と等価です。


### mkdir()
ディレクトリを作成します。
この関数は、複数プロセスが同じディレクトリを同時に作成しようとするような、並列処理環境でも安心して使用できます。


```
 mkdir(path: Union[str, pathlib.Path], *, parents: bool = True, force: bool = True) -> None
```

- **path**： 作成されるディレクトリパス
- **parents**：  `True` の場合、必要に応じて親ディレクトリも作成
- **force**： `True` の場合、path が存在するときは何もしない


### owner()
ファイルを所有しているユーザのユーザ名を返します。
この機能はWindowsでは使用できません。


```
 owner(fname: Union[str, pathlib.Path]) -> str
```

- **fname**： ファイルやディレクトリのパス

### open()
指定したファイルをオープンします。環境変数の自動解決やロギングや、透過的な圧縮をサポートしています。

```
 pshell_open(file: Union[str, pathlib.Path, int, BinaryIO], mode: str = 'r', *, encoding: str = None, errors: str = None, compression: Union[str, bool] = 'auto', **kwargs) -> <class 'IO'>
 
```

- **file**：オープンされるファイルまたはラップされるファイルディスクリプターへのパス。
圧縮方式が 'gzip'，'bzip2'，'lzma' に設定されている場合，file はバイナリのファイルハンドルを与えます。
- **mode**：組み込み関数の  `open` と同じです。明示的に'b'が指定されていない限り、常にデフォ>ルトはテキストモードになります。この点は `gzip.open` ,  `bz2.open` ,  `lzma.open` がバイナリモードをデフォルトとするのとは異なります。
- **encoding**： テキストモードの時の文字エンコーディングです。組み込み関数の `open` とは異なります。プラットフォームに依存せず、常にデフォルトで utf-8 を使用します。
- **errors**：組み込み関数の  `open` と同様ですが、デフォルトでは  `strict` ではなく  `replace` を使用します。
- **compression**： 以下のいずれかです。
  - False - 圧縮しない組み込み関数  `open()` を使用）
  - gzip - gzipで圧縮（関数  `gzip.open()` を使用）
  - bzip2 -  bzip2 で圧縮 (関数 `bz2.open()` を使用)

### concatenate()
ファイルを連結します。Python では、 `cat  file1 file2 ... filen > output_fname` の動作に相当します。


```
 concatenate(input_fnames: Sequence[Union[str, pathlib.Path]], output_fname: Union[str, pathlib.Path], mode: str = 'w', **kwargs) -> None
```

- **input_fnames**：入力ファイルのパスもしくは複数の入力ファイルのパスのシーケンス
- **output_fname**： 出力テキストファイルへのパス
- **mode**： 出力ファイルを開く際のモードを指定（例：'w'または'ab'） `'b'` が明示的に宣言されていない限り、デフォルトではテキストモードになります。
- **kwargs**： `pshell.open` の全ての呼び出しにそのまま渡されます。
  - 特に、この関数は、圧縮されたファイルを検査して、透過的に処理することができます。
  - 透過的に圧縮ファイルを扱うことができます．
  -  `compression='auto'` （デフォルト）の場合は、異なる入力ファイルは異なる圧縮アルゴリズムを使用できます。

### ロギング
pshell は、すべてのコマンドを標準エラー出力またはログファイルに記録するためにロギングを使用します。デフォルトではpshellのロガーを使用しますが、別のロガーを使用するように設定することもできます。


```
 In [2]: # %load 06_logging.py
    ...: import logging
    ...: import pshell as sh
    ...:
    ...: logging.basicConfig(
    ...:     level=logging.INFO,
    ...:     format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(messag
    ...: e)s'
    ...:     )
    ...:
    ...: with sh.open("hello.txt", "w") as fh:
    ...:     fh.write("Hello world!")
    ...:
 2021-09-16 16:17:40,528 INFO [log.py:56] Opening 'hello.txt' for write
 
```

### set_global_logger()
pshellのグローバルロガーを設定します。このロガーは、context_logger が定義されていない限り、すべての pshell 関数で使用されます。

```
 set_global_logger(logger: Union[logging.Logger, str, None]) -> Optional[logging.Logger]
```

- **logger**：ロガー

- 戻り値：設定前のロガー

### contex_logger


```
 context_logge r= <ContextVar name='context_logger' default=None>
```

ContextVarはマルチスレッドや非同期コードで使用される、コンテキストローカルなloggerです。これは、新しいスレッドを作成するときには継承されません。None に設定すると、代わりにglobal logger を使用します。

### get_logger()


```
 get_logger() -> logging.Logger
```

- context_loggerが設定されていれば、それを返します。
- それ以外の場合、もし  `set_global_logger()` が呼ばれていれば、global logger を返します。
- それ以外の場合は、pshell  logger を返します。

## pshell logger

 `logging.Logger` で同じ名前の関数をラッパーしたヘルパー関数が提供されています。
それぞれの戻り値は  `get_logger()` と同じです。


```
 log.debug(msg, *args, **kwargs) → None
```


```
 log.info(msg, *args, **kwargs) → None
```


```
 log.warning(msg, *args, **kwargs)
```


```
 log.error(msg, *args, **kwargs) → None
```


```
 log.critical(msg, *args, **kwargs) → None
```




## call() : 外部コマンドを実行する 
pshell の  `call()` は、外部コマンドの実行して、終了するまで待ちます。これは、subprocess の  `call()` と同じように機能します。


```
 pshell.call(cmd: Union[str, List[str]], *, stdout: IO = None, stdin: IO = None, stderr: IO = None, obfuscate_pwd: str = None, shell: bool = True, timeout: Union[int, float] = None) → int
```

- **cmd** - 実行されるコマンド（strまたはリスト）。 `shell=True` の場合は、strでなければなりません。
- **stdout** - 標準出力ファイルのハンドルです。 `sys.stdout` の場合は省略します。OSレベルのファイル記述子によってバックアップされなければならない `subprocess.call()` のための同じパラメータとは異なり、これは例えば `io.StringIO` のような疑似ストリームにすることができます。
- **stdin** - 標準入力ファイルハンドルです。入力がない場合は省略されます。
- **stderr** - 標準的なエラーファイルのハンドルです。sys.stderrの場合は省略してください。OSレベルのファイル記述子によってバックアップされなければならない  `subprocess.call()` の `stderr` パラメータとは異なり、これは例えば  `io.StringIO` のような疑似ストリームにすることができます。
- **obfuscate_pwd** - 設定された場合、ターゲットのパスワードを検索し、ログに記録する前に XXXX に置き換えます。
- **shell** - これに `True` を与えると、シェルの中で起動します。これは  `subprocess.call()` での `shell` パラメータといくつかの点で異なります。
  - デフォルトは、 `False` ではなく `True` です。
  - LinuxおよびMacOSXでは、errexit、nounset、pipefailなどのまともな設定を行います。
  - Linux と MacOSX では、常に bash であることが保証されています。これは  `subprocess.call()` とは異なり、Ubuntu では dash が、RedHat では bash が起動します。WindowsではCMDです。
- **timeout** - 制限時間内に戻らなかった場合、コマンドを終了します。

> シェルインジェクション
> 信頼されていないソースからの無害化(sanitizing)されていない入力を組み込んだシェルコマンドを実行すると、
> 任意のコマンドが実行されることになり、セキュリティ上の重大な欠陥 となりえるシェルインジェクション(Shell injection)に
> 対して脆弱になります。

 `stdout` にファイルオブジェクトを与えると、コマンドの標準出力をファイルへ出力することができます。また、 `stdin` にファイルオブジェクトを与えると、ファイルの内容をコマンドの標準入力に割り当てて実行します。


```
 In [2]: # %load 10_stdout_stdin.py
    ...: import pshell as sh
    ...:
    ...: with open('sample.txt') as infp:
    ...:     with open('/tmp/cmdout.txt', 'w') as outfp:
    ...:         v1 = sh.call('cat', stdout=outfp, stdin=infp)
    ...:
    ...: # print(v1)
    ...: # !cat /tmp/cmdout.txt
    ...:
 
 In [3]: print(v1)
 0
 
 In [4]: !cat sample.txt
 Hello World

 Think Big!
 EXIT
 
 In [5]: !cat /tmp/cmdout.txt
 Hello World

 Think Big!
 EXIT
 
```

同様に、 `stderr` にファイルオブジェクトを与えると、コマンドの標準エラー出力を格納することができます。


```
 In [2]: # %load 11_stderr.py
    ...: import pshell as sh
    ...:
    ...: with open('/tmp/cmderr.txt', 'w') as errfp:
    ...:     v1 = sh.call('ls /tmp/junk', stderr=errfp)
    ...:
    ...: # print(v1)
    ...: # !cat /tmp/cmderr.txt
    ...:
 
 In [3]: print(v1)
 1
 
 In [4]: !cat /tmp/cmderr.txt
 ls: /tmp/junk: No such file or directory
 
```

 `stdout` と  `stderr` に与えたオブジェクトは `write()` メソッドがあるものとして処理されます。どうように、 `stdin` に与えたオブジェクトは、 `read()` メソッドがあるものとして処理されます。
そのため、ファイル名やファイルパスを直接文字列で与えることはできません。

### メモリへの一時格納
StringIOを使うことメモリへ一時的に格納することもできます。


```
 In [2]: # %load 12_stringio.py
    ...: import pshell as sh
    ...: from io import StringIO
    ...:
    ...: outbuf = StringIO()
    ...:
    ...: v1 = sh.call('ls -1 /etc/', stdout=outbuf)
    ...: v2 = outbuf.getvalue().splitlines()[:5]
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 0
 
 In [4]: print(v2)
 ['afpovertcp.cfg', 'afpovertcp.cfg~orig', 'aliases', 'aliases.db', 'apache2']
 
```

### タイムアウト

 `timeout` に秒数を指定すると、実行したコマンドが指定した秒数で終了しないときは、強制終了させます。


```
 In [2]: # %load 13_timeout.py
    ...: import pshell as sh
    ...: from subprocess import TimeoutExpired
    ...:
    ...: try:
    ...:     sh.call('sleep 10', timeout=5)
    ...: except TimeoutExpired as e:
    ...:     print(f'Timeoout: {e}')
    ...: except:
    ...:     print('unknown')
    ...: print('done')
    ...:
 Timeoout: Command '['bash', '-c', 'set -o errexit; set -o nounset; set -o pipefail; sleep 10']' timed out after 5 seconds
 done
 
```

## check_call()


```
 check_call(cmd: Union[str, List[str]], *, stdout: IO = None, stdin: IO = None, stderr: IO = None, obfuscate_pwd: str = None, shell: bool = True, timeout: Union[int, float] = None) → None
```

サブプロセスで別のコマンドを実行し、終了するのを待ちます。 `call()` と違い、終了コードがゼロでない場合には、 `CalledProcessError` 例外を発生させます。

- 引数は  `call()` と同じです。
- 戻り値：　ありません


```
 In [2]: # %load 14_check_call.py
    ...: import pshell as sh
    ...: from subprocess import CalledProcessError
    ...:
    ...: try:
    ...:     sh.check_call('ls /tmp/missing_file')
    ...: except CalledProcessError as e:
    ...:     print(f'Error: {e}')
    ...:
 ls: /tmp/missing_file: No such file or directory
 Error: Command '['bash', '-c', 'set -o errexit; set -o nounset; set -o pipefail; ls /tmp/missing_file']' returned non-zero exit status 1.
 
```

### check_output()
サブプロセスで別のプログラムを実行し、終了するのを待ち、その標準出力を返します。終了コードがゼロでない場合には、
 `CalledProcessError` 例外を発生させます。


```
 check_output(cmd: Union[str, List[str]], *, stdin: IO = None, stderr: IO = None, obfuscate_pwd: str = None, shell: bool = True, timeout: Union[int, float] = None, decode: bool = True, encoding: str = 'utf-8', errors: str = 'replace')
```

多くの引数は `call()` と同じです。
- **decode**：True の場合、生の出力を UTF-8 にデコードし、str オブジェクトを返します。
Falseの場合は、生のバイトオブジェクトを返します。デフォルトでは、UTF-8にデコードします。
これは、常に生の出力を返す  `subprocess.check_output()` とは異なります。
- **encoding**： 生のバイト出力のエンコーディング。 `decode=False` の場合は無視されます。
- **errors**：  `'replace'` 、 `'ignore'` 、 `'strict'` のいずれか。( `bytes.decode()` を参照)
 `decode=False` の場合は無視されます。なお、デフォルトは  `replace` ですが、 `bytes.decode()` のデフォルトは `strict` です。


```
 In [2]: # %load 15_check_output.py
    ...: import pshell as sh
    ...:
    ...: v1 = sh.check_output('cat sample.txt')
    ...: v2 = sh.check_output('cat sample.txt', decode=False)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 Hello World

 Think Big!
 EXIT
 
 
 In [4]: print(v2)
 b'Hello World\nPython Osaka\nThink Big!\nEXIT\n'
 
```

## real_fh()
io モジュールは、ファイルハンドルを偽装するために使用できるファイルライクオブジェクトを提供します。とりわけ、これらは nosetests や py.test によって標準出力/標準エラー出力をキャプチャするために広く使用されています。

ほとんどの場合、これは透過的に行われます。しかし、subprocess モジュールのような例外があり、それは実際のファイル記述子の下にあるファイルハンドルを必要とします。

このコンテキストマネージャはこのようなケースを透過的に検出し、ioモジュールの疑似ファイルハンドラを実際のPOSIXベースのファイルハンドルに自動的に変換します。


```
 real_fh(fh: Optional[IO]) -> None
```

- **fh**：書き込み用にオープンされ、POSIXファイル記述子によってバックアップされたファイルハンドル
例：open()によって返されるもの、またはsys.stdoutもしくはsys.stderrのデフォルト値
 `io.StringIO` 、 `io.BytesIO` 、 または  `sys.stdout` と  `sys.stderr` をモックするために nosetestsで使われるスタブのような疑似ファイルハンドルです。


```
 In [2]: # %load 16_real_fh.py
    ...: import subprocess
    ...: import pshell as sh
    ...: import io
    ...: import shlex
    ...:
    ...: buf = io.StringIO()
    ...:
    ...: cmd = 'ls /tmp/missing_file'
    ...: sh.call(cmd, stderr=buf)
    ...:
    ...: with sh.real_fh(buf) as real_buf:
    ...:     subprocess.call(shlex.split(cmd), stderr=real_buf)
    ...:
 
```

## パイプ処理
bashコマンドでのパイプ処理は、コマンドをパイプ記号( `|` )でコマンドを繋いで、あるコマンドの出力を別のコマンドへの入力として実行するものです。 pshell モジュールではコマンドラインをそのまま `call()` 、 `check_call()` 、 `check_output()` にわたすだけです。


```
 In [2]: # %load 17_pipe.py
    ...: import pshell as sh
    ...:
    ...: v1 = sh.check_output('ls -l /etc/ | wc -l')
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
      114
 
 
 In [4]: !ls -l /etc/ | wc -l
      114
 
```

## まとめ
シェルスクリプトではデバッグしづらくなるものが、pshell を使うことでロギングや他の多くの  Python モジュールと連携することができ、保守性が高まります。

## 参考
- [pshell ソースコード ](https://github.com/crusaderky/pshell)
- [pshell ドキュメント ](https://pshell.readthedocs.io/en/latest/)
- [Shell Injection ](https://en.wikipedia.org/wiki/Code_injection#Shell_injection)


