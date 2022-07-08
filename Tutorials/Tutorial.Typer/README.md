オプション解析モジュールTyperを使いこなそう 
=================
### Typer について
TyperはFastAPIマイクロフレームワークの作者が Click を利用したオプション解析処理をしてくれる拡張モジュールです。
Click がデコレータでオプション解析処理の指示を与えるのに対して、Typer は変数のタイプヒントを利用して定義するため、より簡潔な記述となるのが特徴です。
そのため、Python 3.6 以降が必要になります。

typer は拡張モジュールなのでインストールする必要があります。
 pip
```
 $ pip install typer
```

### typerの実装方法
typer を組み込んだコマンドの実装には次の２つの方法があります。

#### typer.run() から呼び出す方法
この例ではオプションや引数の定義はしていないので、単純に  `hello_world()` を呼び出しても動作します。
 helloworld1.py
```
 import typer
 
 def hello_world():
     typer.echo('Hello World')
 
 if __name__ == "__main__":
     typer.run(hello_world)
```

#### アプリケーションインスタンスに登録して呼び出す方法
詳しくは後述しますが、サブコマンドを持たせたいときは、複数のファイルにまたがるような場合に使用します。
 helloworld2.py
```
 import typer
 
 app = typer.Typer()
 
 @app.command("hello")
 def hello_world():
     typer.echo('Hello World')
 
 if __name__ == "__main__":
     app()
```

 bash
```
 % python helloworld2.py --help
 Usage: helloworld2.py [OPTIONS]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
```

両方とも出力は同じになります。
typer はデフォルトで入力補完のオプション  `--install-completion` と  `--show-completion` を表示します。これを表示させたくない場合は、アプリケーションインスタンスを生成するときに次のようにします。

 helloworld3.py
```
 import typer
 
 app = typer.Typer(add_completion=False)
 
 @app.command("hello")
 def hello_world():
     typer.echo('Hello World')
 
 if __name__ == "__main__":
     app()
```

 bash
```
 % python helloworld3.py --help
 Usage: helloworld3.py [OPTIONS]
 
 Options:
   --help  Show this message and exit.
```

### typer.echo()
 `typer.echo()` はpythonの  `print()` と同じように与えた文字列を表示します。 `print()` との大きな違いは、 `err=True` を与えると標準エラー出力へ出力されることです。

 echo.py
```
 import typer
 
 def cmd():
    typer.echo("This message oputput to stdout.")
    typer.echo("This message oputput to stderr.", err=True)
     
 if __name__ == '__main__':
     cmd()
```

 zsh
```
 % python echo.py
 This message oputput to stdout.
 This message oputput to stderr.
 
 % python echo.py 2>/dev/null
 This message oputput to stdout.
```

### typer.style()
 `typer.echo()` は、 `typer.style()` と共に使うことで、カラーなど文字の装飾が簡単になります。
> typer.sytle(text, fg, bg, bold, dim, underline, blink, reverse, reset)
>    text:  任意の文字列
>    fg: 前景色/文字の色 ('red', 'green', 'yellow'など)
>    bg: 背景色
>    bold: ボールド表示
>    dim:  薄暗く表示する
>    underline: アンダーライン表示
>    blink: 点滅表示
>    reverse:  前景色、背景色の反転
>    reset: 設定のリセット、False にすると設定を引き継ぐ

 style.py
```
 import typer
 
 def cmd():
     typer.echo(typer.style('Hello World.',
                            fg='green', bg='red', reset=False))
     typer.echo(typer.style('Hello Again.'))
 
 if __name__ == '__main__':
     cmd()
```

### typer.launch()
 `typer.launch()` は引数に与えたURLやファイル・タイプに応じたアプリケーションを起動します。

次の例はブラウザでURLをオープンします。
 launch.py
```
 import typer
 
 def open_google():
     typer.echo("Opening Google...")
     typer.launch("https://www.google.com")
 
 if __name__ == "__main__":
     typer.run(open_google)
```

また、 `locate=True` が与えられているとファイルブラウザが起動してファイルの場所を示すこともできます。
次のようにすると設定ファイルをオープンするような処理になります。
 launch2.py
```
 from pathlib import Path
 import typer
 
 APP_NAME = "typer_tutorial"
 
 def main():
     app_dir = typer.get_app_dir(APP_NAME)
     app_dir_path = Path(app_dir)
     app_dir_path.mkdir(parents=True, exist_ok=True)
     config_path: Path = Path(app_dir) / "config.json"
     if not config_path.is_file():
         config_path.write_text('{"version": "1.0.0"}')
     config_file_str = str(config_path)
     typer.echo("Opening config directory")
     typer.launch(config_file_str, locate=True)
 
 if __name__ == "__main__":
     typer.run(main)
```


> XCodeがインストールされているMacでは、
> Xcode がファイルをオープンします。

### オプション解析
 `typer.Option()` の例です。
次の例は、ユーザからの文字列入力を受け付けて、 `--count` オプションで与えた数値だけ繰り返すものです。
 greeting.py
```
 import typer
 
 def hello(count: int = typer.Option(1, '-C', '--count',
 　　　　　　　　　　　　　　　　　　　　　　help='Number of greetings.'),
            name: str = typer.Option(..., prompt='Your Name: ',
                                     help='The person to greet.'),
          ):
     """COUNTで与えた回数だけHelloする"""
     for x in range(count):
         typer.echo(f'Hello {name}')
 
 if __name__ == '__main__':
     typer.run(hello)
```

 `typer.Option()` は引数の変数名をオプション文字列として解析します。
この例では、 `--count` オプションを `-C` としても受け付けることができ、オプション引数のデフォルト値を１に設定しています。

ユーザがコマンドラインで `--name` オプションを与えない場合は、 `prompt` で指示した文字列を表示して入力待ちとなります。
 `typer.Option()` の第１引数にはデフォルト値を与えることができ、
ここに ３つのピリオド（ `...` ） を与えると必須オプションということになります。


 bash
```
 $ python greeting.py --help
 Usage: greeting.py [OPTIONS]
 
  COUNTで与えた回数だけHelloする
 
 Options:
  -C, --count INTEGER         Number of greetings.  [default: 1]
  --name TEXT                 The person to greet.  [required]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                              Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                              Show completion for the specified shell, to
                              copy it or customize the installation.
 
  --help                      Show this message and exit.
  
 $ python greeting.py --name David
 Hello David
 
 $ python greeting.py -C 2
 Your Name: Freddie
 Hello Freddie
 Hello Freddie
```

関数に記述した docstrings がヘルプ表示のときに使用されます。


#### パスワード入力の処理をしたい
 `typer.Option()` で  `hide_input=True` とすると入力中の文字のエコー表示をしなくなります。また、 `confirmation_prompt=True` にしておくと２度入力を求めて同じ場合にだけ、ユーザが入力した文字がセットされます。

 optpassword.py
```
 import typer
 
 def cmd(password: str = typer.Option(...,
                                prompt='Password',
                                hide_input=True,
                                confirmation_prompt=True)
 ):
     typer.echo( password )
 
 if __name__ == '__main__':
     typer.run(cmd)
```


#### オプションをフラグとして処理したい
 `typer.option()` でタイプヒントを行う変数を  `bool` 型 としておくと、そのオプションはフラグとして解析されます。
 optflag.py
```
 import typer
 
 def cmd(debug: bool = typer.Option(False,hidden=True
                             help='DEBUG mode'),
         force: bool = typer.Option(False, '--force',
                             help='Force option')
 ):
     typer.echo( f'debug: {debug}')
     typer.echo( f'force: {force}')
 
 if __name__ == '__main__':
     typer.run(cmd)
```

 bash
```
 % python optflag.py --help
 Usage: optflag.py [OPTIONS]
 
 Options:
   --force               Force option  [default: False]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
   
   % python optflag.py --debug
   debug: True
   force: False
   
   % python optflag.py --no-debug
   debug: False
   force: False
   
   % python optflag.py --force
   debug: False
   force: True
   
   % python optflag.py --no-force
   Usage: optflag.py [OPTIONS]
   Try 'optflag.py --help' for help.
   
   Error: no such option: --no-force
```

 `typer.Option()` に  `hidden=True` を与えると、そのオプションはヘルプメッセージに表示されなくなります。
 `typer.Option()` はデフォルトで引数の名前をオプション文字列とします。
上記の `debug` の場合では、 `--debug` と  `--no-debug` が有効となり、明示的にオプション文字列を与えると `--no-オプション` のオプションは受けつなくなります。


### フラグオプションの文字列を変更したい
フラグオプションを `--accept` と  `--reject` というような組み合わせにしたいときは、オプション文字列の定義でスラッシュ( `/` ) で区切って定義しておきます。

 option_alterante.py
```
 from typing import Optional
 import typer
 
 def main(accept: Optional[bool] = typer.Option(None, "--accept/--reject")):
     if accept is None:
         typer.echo("I don't know what you want yet")
     elif accept:
         typer.echo("Accepting!")
     else:
         typer.echo("Rejecting!")
 
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python option_alternate.py --help
 Usage: option_alternate.py [OPTIONS]
 
 Options:
   --accept / --reject
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
   
 % python option_alternate.py --accept
 Accepting!
 
 % python option_alternate.py --reject
 Rejecting!
 
 % python option_alternate.py
 I don't know what you want yet
```

#### オプションのプレフィックスを変更したい
通常は、コマンドラインのオプションはひとつ、もしくは２つのマイナス記号( `-` ) で始まるものですが、次のようにスラッシュ記号( `/` )で区切ってオプションを記述することで別の文字をオプションとすることができるようになります。

 option_prefix.py
```
 import typer
 
 def cmd(writable: bool = typer.Option(False, '+w/-w')):
     typer.echo( f'writable: {writable}' )
 
 if __name__ == '__main__':
     typer.run(cmd)
```

 bash
```
 % python option_prefix.py --help
 Usage: option_prefix.py [OPTIONS]
 
 Options:
   +w / -w               [default: False]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
   
 % python option_prefix.py
 writable: False
 
 % python option_prefix.py -w
 writable: False
 
 % python option_prefix.py +w
 writable: True
```

### フラグオプションを与えたときだけFalseとして扱わせたい
フラグオプションを与えたときだけFalse となるようにするためには次のように定義します。
 option_false.py
```
 import typer
 
 def main(in_prodaction: bool = typer.Option(True, " /--demo", " /-d")):
     if in_prodaction:
         typer.echo("Running in production")
     else:
         typer.echo("Running demo")
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python option_false.py --help
 Usage: option_false.py [OPTIONS]
 
 Options:
    / -d, --demo         [default: True]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python option_false.py --demo
 Running demo
 
 % python option_false.py -d
 Running demo
 
 % python option_false.py
 Running in production
```

オプション文字列を指定する箇所で、スラッシュ( `/` ) の前の空白文字は意味があります。この空白文字がないと、 `/--demo` 、 `/-d` がオプション文字列となってしまいます。

#### オプション引数の数を指定する
オプション引数を数を指定する場合、typer では次のようにタイプヒントでタプルあるいはリストで、その要素の型を与えるだけです。この例では、 `int` 型を２つ与えているため２つのオプション引数を受け取ります。


```
 import typer
 from typing import Tuple
 
 def cmd(position: Tuple[int, int] = typer.Option(..., '-P', 
 　　　　　　　　　　　　　　　　　　　　　　　　help="Geometory: x y")):
     typer.echo( position )
 
 if __name__ == '__main__':
     typer.run(cmd)
```


 bash
```
 $ python optmultiargs.py -P 1
 Error: -P option requires 2 arguments
 $ python optmultiargs.py -P 1 2
 (1, 2)
 $ python optmultiargs.py -P 1 2 3
 Usage: optmultiargs.py [OPTIONS]
 Try 'optmultiargs.py --help' for help.
 
 Error: Got unexpected extra argument (3)
```

#### 同じオプションを複数回指定することを許す
オプションは複数回指定することができるようになります。デフォルトでは、同じオプションが複数回与えられた場合は、最後に与えられたオプションが有効になります。
 multiopt.py
```
 import typer
 from typing import List
 
 def cmd(name: List[str] = typer.Option(..., '-N', '--name', help="Name...")):
     typer.echo( name )
 
 if __name__ == '__main__':
     typer.run(cmd)
```

 bash
```
 $ python　multiopts.py -N Beer -N Wine
 ('Beer', 'Wine')
```


#### オプションが指定された回数を知りたい
 `tyer.Option()` で  `count=True` を設定すると、そのオプションが指定された回数がセットされます。
 option_count.py
```
 import typer
 
 def cmd(verbose: int = typer.Option(0, '-v', '--verbose', 
                                     count=True,
                                     help="Verbosly Mode")):
     typer.echo(f'verbose level: {verbose}')
 
 if __name__ == '__main__':
     typer.run(cmd)
```

 bash
```
 $ python option_count.py
 verbose level: 0
 
 $ python option_count.py -v
 verbose level: 1
 
 $ python option_count.py -v -v
 verbose level: 2
 
 $ python click_optcount.py -vvvv
 verbose level: 4
```



### コマンド引数を処理したい
 `typer.Argument()` はコマンド引数を処理することができます。
 arguments.py
```
 from typing import List
 import typer
 
 def copy(src: List[str] = typer.Argument(...),
          dst: str = typer.Argument(...)
 ):
     """Move file SRC to DST."""
     for filename in src:
         typer.echo(f'move {filename} to folder {dst}')
 
 if __name__ == '__main__':
     typer.run(copy)
```

コマンド引数を可変長にしたいときは、タイプヒントでタプルもしくはリストで指示します。 `typer.Argument()` の第１引数にはデフォルト値を与えることができ、ここに ３つのピリオド（ `...` ） を与えた引数は必須ということになります。

 bash
```
 % python arguments.py
 Usage: arguments.py [OPTIONS] SRC... DST
 Try 'argument.py --help' for help.
 
 Error: Missing argument 'SRC...'.
 
 % python arguments.py --help
 Usage: argument.py [OPTIONS] SRC... DST
 
   Move file SRC to DST.
 
 Arguments:
   SRC...  [required]
   DST     [required]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 % python arguments.py a b c d
 move a to folder d
 move b to folder d
 move c to folder d
```

typer はタイプヒントの対象となる変数名や型からをヘルプメッセージを生成します。
コマンド引数のタイプヒントで  `name: str` としていると、ヘルプメッセージでは　 `NAME` として表示されます。
 `typer.Argument()` や　 `typer.Option()` にキーワード引数  `metavar=` に表示する文字列を与えることで変更することができます。

 argument_metavar.py
```
 from typing import List
 import typer
 
 def copy(src: List[str] = typer.Argument(..., metavar='SOURCES'),
          dst: str = typer.Argument(..., metavar='DESTINATION')
 ):
     """Move file SOURCES to DESTINATION."""
     for filename in src:
         typer.echo(f'move {filename} to folder {dst}')
 
 if __name__ == '__main__':
     typer.run(copy)
```

 bash
```
 % python  artument_metavar.py --help
 Usage: artument_metavar.py [OPTIONS] SOURCES DESTNESTION
 
   Move file SOURCES to DESTINATION.
 
 Arguments:
   SOURCES      [required]
   DESTNESTION  [required]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
```

### 終了処理
コマンドでの処理中に意図的に終了したいようなときがあります。こうしたときは、typer では  `typer.Exit()` や  `typer.Abort()` の例外を発行します。
 `typer.Abort()` は”Aborted!" と表示することを除いて、両者は同じ働きです。
 terminate.py
```
 import typer
 
 def abort_cmd():
     raise typer.Abort()
 
 def exit_cmd():
     raise typer.Exit()
 
 action = {
     'exit': exit_cmd,
     'abort': abort_cmd,
 }
 
 def cmd(subcmd: str = typer.Argument(...)):
     if subcmd in action.keys():
         typer.echo(f'subcmd: {subcmd}')
         action[subcmd]()
     else:
         typer.echo(f'Unknown subcommand: {subcmd}')
 
 if __name__ == '__main__':
     typer.run(cmd)
```

 bash
```
 % python terminate.py --help
 Usage: terminate.py [OPTIONS] SUBCMD
 
 Arguments:
   SUBCMD  [required]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python terminate.py exit
 subcmd: exit
 
 % python terminate.py abort
 subcmd: abort
 Aborted!
```


#### パラメタを限定させたい
typer でコマンド引数やオプション引数に与えることができる文字列を限定させたいときは、Python 標準モジュール  `enum.Enum` クラスを継承したクラスを定義してタイプヒントの型として与えます。
 choice.py
```
 from enum import Enum
 import typer
 
 class HashType(str, Enum):
     md5 = "md5"
     sha1 = "sha1"
     sha256 = "sha256"
 
 def main(hash_type: HashType = HashType.md5):
     typer.echo(f"Hash Type: {hash_type.value}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python choice.py --help
 Usage: choice.py [OPTIONS]
 
 Options:
   --hash-type [md5|sha1|sha256]  [default: md5]
   --install-completion           Install completion for the current shell.
   --show-completion              Show completion for the current shell, to
                                  copy it or customize the installation.
 
   --help                         Show this message and exit.
 
 % python choice.py --hash-type sha256
 Hash Type: sha256
 
 % python choice.py --hash-type sha
 Usage: choice.py [OPTIONS]
 Try 'choice.py --help' for help.
 
 Error: Invalid value for '--hash-type': invalid choice: sha. (choose from md5, sha1, sha256)
```

#### パラメタの数値範囲を指定したい
 `typer.Option` や  `typer.Argument()` には、 `min` と  `max` で受け入れる数値範囲を指定することができます。コマンド引数やオプション引数が、期待している数値範囲にあるかチェックしてくれます。 
 validate_range.py
```
 import typer
 
 def main(
     id: int = typer.Argument(..., min=0, max=1000),
     age: int = typer.Option(20, min=18),
     score: float = typer.Option(0, max=100, clamp=True),
 ):
     typer.echo(f"ID is {id}")
     typer.echo(f"--age is {age}")
     typer.echo(f"--score is {score}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 `clamp=True` が与えられていれば、指定した数値を超えた場合は補正されます。

 bash
```
 $ python validate_range.py --help
 Usage: validate_range.py [OPTIONS] ID
 
 Arguments:
   ID  [required]
 
 Options:
   --age INTEGER RANGE   [default: 20]
   --score FLOAT RANGE   [default: 0]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 $ python validate_range.py 5 --score 200
 ID is 5
 --age is 20
 --score is 100
```

#### パラメタとしてUUIDを扱いたい
#### UUID（Universally Unique Identifier)
UUIDをコマンド引数やオプション引数のパラメタとして使用したいときは次のように、Python 標準モジュールの  `uuid.UUID` をタイプヒントで与えます。
 myuuid.py
```
 from uuid import UUID
 
 import typer
 
 def main(user_id: UUID):
     typer.echo(f"USER_ID is {user_id}")
     typer.echo(f"UUID version is: {user_id.version}")
 
 if __name__ == "__main__":
     typer.run(main)
```

typer はユーザが与えた文字列がUUIDとして妥当かチェックしてくれます。
 bash
```
 % python myuuid.py --help
 Usage: myuuid.py [OPTIONS] USER_ID
 
 Arguments:
   USER_ID  [required]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python uuid.py e6501a90-2a30-45aa-9a6f-bb2013264341
 USER_ID is e6501a90-2a30-45aa-9a6f-bb2013264341
 UUID version is: 4
 
 % python uuid.py e6501a90-2a30-45aa-9a6f-bb201
 Usage: uuid.py [OPTIONS] USER_ID
 Try 'uuid.py --help' for help.
 
 Error: Invalid value for 'USER_ID': e6501a90-2a30-45aa-9a6f-bb201 is not a valid UUID value
```

### パラメタに日時文字列を指定したい
typer でコマンド引数やオプション引数に日時文字列を指定したいとぃは、Python 標準モジュール  `datetime.datetime` をタイプヒントの型として与えます。
 mydatetime.py
```
 from datetime import datetime
 import typer
 
 def main(start: datetime = typer.Option(...),
          end: datetime = typer.Argument(
                                f'{datetime.today():%Y-%m-%d}'),
 ):
     typer.echo(f'start: {start}')
     typer.echo(f'  end: {end}')
 
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python mydatetime.py --help
 Usage: datetime.py [OPTIONS]
                                [END]:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d
                                %H:%M:%S]
 
 Arguments:
   [END]:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                   [default: 2020-12-02]
 
 Options:
   --start [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                   [required]
   --install-completion            Install completion for the current shell.
   --show-completion               Show completion for the current shell, to
                                   copy it or customize the installation.
 
   --help                          Show this message and exit.
   
 % python mydatetime.py --start '2000-10-02' '2020-12-02'
 start: 2000-10-02 00:00:00
   end: 2020-12-02 00:00:00
 
 % python mydatetime.py --start '2000-10-02'
 start: 2000-10-02 00:00:00
   end: 2020-12-02 00:00:00
 
 % python mydatetime.py --start '2000-15-33'
 Usage: datetime.py [OPTIONS] [END]:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d
                          %H:%M:%S]
 
 Error: Invalid value for '--start': invalid datetime format: 2000-15-33. (choose from %Y-%m-%d, %Y-%m-%dT%H:%M:%S, %Y-%m-%d %H:%M:%S)
```

デフォルトでは次の３つの日付指定を受け付けます。

-  `%Y-%m-%d` 
-  `%Y-%m-%dT%H:%M:%S` 
-  `%Y-%m-%d %H:%M:%S` 

日付指定のフォーマットを追加や変更したい場合は  `formats=` にリストで与えます。
 mydatetime_custom.py
```
 rom datetime import datetime
 import typer
 
 def main(
     launch_date: datetime = typer.Argument(..., formats=["%Y/%m/%d"])
 ):
     typer.echo(f"Launch will be at: {launch_date}")
 
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python mydatetime_custom.py --help
 Usage: mydatetime_custom.py [OPTIONS] LAUNCH_DATE:[%Y/%m/%d]
 
 Arguments:
   LAUNCH_DATE:[%Y/%m/%d]  [required]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python mydatetime_custom.py 2020/12/25
 Launch will be at: 2020-12-25 00:00:00
 
 % python mydatetime_custom.py 2020-12-25
 Usage: mydatetime_custom.py [OPTIONS] LAUNCH_DATE:[%Y/%m/%d]
 
 Error: Invalid value for 'LAUNCH_DATE:[%Y/%m/%d]': invalid datetime format: 2020-12-25. (choose from %Y/%m/%d)
```


#### パラメタを環境変数でも指定できるようにしたい
 `typer.Argument()` や  `typer.Option()` に　 `envvar=環境変数名` を与えると、環境変数に設定されている文字列を引数として変数にセットします。 
 argument_envvar.p
```
 from pathlib import Path
 import typer
 
 def cmd(name: str = typer.Argument('anonymous',
                                     envvar='USERNAME',
                                     show_envvar=False),
         config: Path = typer.Option('config.ini',
                                      envvar='CONFIG_FILE')
 ):
     if config.is_file():
         text = config.read_text()
         typer.echo(f"Config file contents: {text}")
     else:
         typer.echo(f"Config file missing: {config.name}")
 
     typer.echo(f"Hello: {name}")
 
 if __name__ == '__main__':
     typer.run(cmd)
```

 bash
```
 % python argument_envvar.py --help
 Usage: artument_envvar.py [OPTIONS] [NAME]
 
 Arguments:
   [NAME]  [default: anonymous]
 
 Options:
   --config PATH         [env var: CONFIG_FILE; default: config.ini]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 % python argument_envvar.py Jack
 Config file missing: config.ini
 Hello: Jack
 
 % python artument_envvar.py --config=data.txt Jack
 Config file contents: Python Osaka
 
 Hello: Jack
 
 % export CONFIG_FILE=data.json
 % python artument_envvar.py Jack
 Config file missing: data.json
 Hello: Jack
 
 % export USERNAME=David 
 % python artument_envvar.py Jack
 Config file missing: config.json
 Hello: Jack
```

 `typer.Argument()` に  `show_envvar=False` を与えるとヘルプメッセージに環境変数名を表示しなくなります。

#### パラメタをファイル名として扱いたい
コマンドでファイルを処理したいときなどファイル名をパラメタとして受け取りますが、typer では次のようにタイプヒントの型に `typer.FileText` を与えます。

 argument_file.py
```
 import typer
 
 def cmd(srcfile: typer.FileText = typer.Argument(...)):
     lines = srcfile.readlines()
     for line in lines:
         typer.echo( line[:-1] )
 
 if __name__ == '__main__':
     typer.run(cmd)
```

typer は、 `FileText` 型の引数に指定された文字列をファイル名として扱い、オープンをしたファイルオブジェクトを変数にセットします。ファイルの存在などのチェックまではしません。

 bash
```
 % python argument_file.py --help
 Usage: argument_file.py [OPTIONS] SRCFILE
 
 Arguments:
   SRCFILE  [required]
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % echo "Python Osaka" > data.txt
 
 % python argument_file.py data.txt

 
 % python argument_file.py data.json
 Usage: argument_file.py [OPTIONS] SRCFILE
 Try 'argument_file.py --help' for help.
 
 Error: Invalid value for 'SRCFILE': Could not open file: data.json: No such file or directory
```

ファイルの存在をチェックしたいようなときは、Python 標準モジュールの  `pathlib.Path` をタイプヒントの型として与えます。

 mypathlib.py
```
 from pathlib import Path
 from typing import Optional
 import typer
 
 def main(config: Optional[Path] = typer.Option(None)):
     if config is None:
         typer.echo("No config file")
         raise typer.Abort()
     if config.is_file():
         text = config.read_text()
         typer.echo(f"Config file contents: {text}")
     elif config.is_dir():
         typer.echo("Config is a directory, will use all its config files")
     elif not config.exists():
         typer.echo("The config doesn't exist")
 
 if __name__ == "__main__":
     typer.run(main)
```

bash
```
 % python mypathlib.py --help
 Usage: mypathlib.py [OPTIONS]
 
 Options:
   --config PATH
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python mypathlib.py --config data.txt
 Config file contents: Python Osaka
 
 % python mypathlib.py --config ./data.txt
 Config file contents: Python Osaka
 
 % python mypathlib.py --config data.json
 The config doesn't exist
```

 `typer.Option()` に次のキーワード引数で与えた内容でファイルをチェックします。

-  `exists` : True でファイル/ディレクトリの存在有無をチェック
-  `file_okay` : Trueでファイルとして操作可能かチェック
-  `dir_okay` : Trueでディレクトリとして操作可能かチェック
-  `writable` : Trueで書き込み可能かチェック
-  `readable` : Trueで読み込み可能かチェック
-  `resolve_path` :Trueでファイルパスは絶対パスとして評価します。シンボリックリンクが解決されます。

 mypathlib_check.py
```
 from pathlib import Path
 import typer
 
 def main(
     config: Path = typer.Option(
         ...,
         exists=True,
         file_okay=True,
         dir_okay=False,
         writable=False,
         readable=True,
         resolve_path=True,
     )
 ):
     text = config.read_text()
     typer.echo(f"Config file contents: {text}")
 
 if __name__ == "__main__":
     typer.run(main)
```

#### オプション解析時にコールバック関数を与えたい
 `typer.Option()` や  `typer.Argument()` に キーワード引数 `callback` に関数を与えると、その関数を呼び出してくれます。

 option_callback1.py
```
 from typing import Optional
 import typer
 
 __version__ = "0.1.0"
 
 def version_callback(value: bool):
     if value:
         typer.echo(f"Awesome CLI Version: {__version__}")
         raise typer.Exit()
 
 def name_callback(name: str):
     if name != "Freddie":
         raise typer.BadParameter("Only Freddie is allowed")
 
 def main(
     name: str = typer.Option(..., callback=name_callback),
     version: Optional[bool] = typer.Option(
         None, "--version", 
         callback=version_callback
     ),
 ):
     typer.echo(f"Hello {name}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python option_callback1.py --help
 Usage: option_callback1.py [OPTIONS]
 
 Options:
   --name TEXT           [required]
   --version
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python option_callback1.py --version
 Awesome CLI Version: 0.1.0
```

これは、うまく動作しているように見えます。
このスクリプトではコールバック関数 `name_callback()` は処理中に終了する場合があり、また、 `--version` オプションの定義の前にあるため、２つのオプションを同時に与えられるとうまく動作しません。

 bash
```
 % python  option_callback1.py --name Jack --version
 Usage: option_callback1.py [OPTIONS]
 
 Error: Invalid value for '--name': Only Freddie is allowed
```

こうしたときは、 `is_eager=True` を与えると、他のオプションより優先度が高くなります。

 option_callback2.py
```
 from typing import Optional
 import typer
 
 __version__ = "0.1.0"
 
 def version_callback(value: bool):
     if value:
         typer.echo(f"Awesome CLI Version: {__version__}")
         raise typer.Exit()
 
 def name_callback(name: str):
     if name != "Freddie":
         raise typer.BadParameter("Only Freddie is allowed")
 
 def main(
     name: str = typer.Option(..., callback=name_callback),
     version: Optional[bool] = typer.Option(
         None, "--version", 
         callback=version_callback,
         is_eager=True
     ),
 ):
     typer.echo(f"Hello {name}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python  option_callback2.py --name Jack --version
 Awesome CLI Version: 0.1.0
```

### 入力補完
Linux系プラットフォームや Bash on Windows では、シェルとして Bash や Zsh を使用することができます。
これらのシェルではタブキーによるコマンドラインの入力補完が行えるようになっています。
typer も入力補完をサポートしていて、これまでのサンプルスクリプトでもデフォルトオプションとして表示される  `--install-completion` と  `--show-completion` は何度も目にしてきました。

 choice.py
```
 from enum import Enum
 import typer
 
 class HashType(str, Enum):
     md5 = "md5"
     sha1 = "sha1"
     sha256 = "sha256"
 
 def main(hash_type: HashType = HashType.md5):
     typer.echo(f"Hash Type: {hash_type.value}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 bash
```
 % python choice.py --help
 Usage: choice.py [OPTIONS]
 
 Options:
   --hash-type [md5|sha1|sha256]  [default: md5]
   --install-completion           Install completion for the current shell.
   --show-completion              Show completion for the current shell, to
                                  copy it or customize the installation.
 
   --help                         Show this message and exit.
```

 bash
```
 $ python choice.py --install-completion
 bash completion installed in /Users/goichiiisaka/.bash_completions/choice.py.sh
 Completion will take effect once you restart the terminal
 
```

 zsh
```
 % python choice.py --install-completion
 zsh completion installed in /Users/goichiiisaka/.zfunc/_choice.py
 Completion will take effect once you restart the terminal
```

Bash では  `bash-completion` 、Zsh では　 `zsh-completion` のパッケージがシステムにインストールされている必要があります。
ここでは プラットフォームが Mac で シェルは zsh を使っているものとして説明します。
次のように $HOME/.zshrc を定義しておけば動作するようになります。
 $HOME/.zshrc
```
 if type brew &>/dev/null; then
   FPATH=$(brew --prefix)/share/zsh-completions:$FPATH
   FPATH=$HOME/.zfunc:$FPATH
   autoload -Uz compinit
   compinit
 fi
```

#### シェルのリセット
 bash or zsh
```
 $ exec $SHELL -l
```

対象のスクリプト(この場合は  `choice.py` ) がpython スクリプトとして実行権限があれば、 `---install-completion` を実行することで単独で入力補完ができるようになります。

あるいは、 typer コマンドに続けてコマンドを入力します。
この場合は、 `--install-completion` を実行しなくても構いません。

typer コマンドはインストールする必要があります。
 pip
```
 $ pip install typer-cli
```

次のようにコマンドラインを入力して、オプションプレフィックスの `--` の後に
タブキーを１度押下します。便宜上  `[TAB]` として表記します。
 zsh
```
 % typer choice.py run --[TAB]
```

すると typer は次のように入力補完をしてくれます。
 zsh
```
 % typer choice.py run --hash-type 
```

ここでもう一度タブキーを押下すると選択候補が表示されます。
 zsh
```
 % typer choice.py run --hash-type [TAB]
 md5     sha1    sha256
```

選択候補を指定するため  `m` を入力したあとにタブキーを押下するとオプション引数が入力補完されます。
 zsh
```
 % typer choice.py run --hash-type m[TAB]
 md5     sha1    sha256
```

 zsh
```
 % typer choice.py run --hash-type md5 
 md5     sha1    sha256
```

### コールバック関数を使った入力補完
typer はパラメタの入力補完にコールバック関数を与えて処理することができます。
この場合は、キーワード引数  `autocompletion` を使用します。

 autocompletion1.py
```
 import typer
 
 def complete_name():
     return ["Camila", "Carlos", "Sebastian"]
 
 def main(
    name: str = typer.Option("World",
                      autocompletion=complete_name,
                      help="The name to say hi to."
    )
 ):
     typer.echo(f"Hello {name}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 zsh
```
 % typer autocompletion1.py run --help
 Usage: typer run [OPTIONS]
 
   Run the provided Typer app.
 
 Options:
   --name TEXT  The name to say hi to.  [default: World]
   --help       Show this message and exit.
```

次のようにコマンドラインを入力します。
 zsh
```
 % typer autocompletion1.py run --[TAB][TAB]
```

typer は次のようにコマンドラインを補完します。
 zsh
```
 % typer autocompletion1.py run --name 
 David    Freddie  Jack
```

Dに続けてタブキーを入力します。
 zsh
```
 % typer autocompletion1.py run --name D[TAB]
```

typer は次のようにコマンドラインを補完します。
 zsh
```
 % typer autocompletion1.py run --name David 
 David    Freddie  Jack
```

選択候補が表示されたときにタブキーを押下するたびに、選択候補が変わっていきます。
カーソルキーや `Ctl+f` ,  `Ctl+b` などのキー操作でも選択することができます。

### パラメタの選択候補にヘルプメッセージをつけたい

入力補完させるパラメタの選択候補にヘルプメッセージをつけたいような場合は、
 `(パラメタ, メッセージ)` のタプルを要素とするリストを与えます。

 autocompletion2.py
```
 import typer
 
 valid_completion_items = [
     ("Brian", "The guitarist."),
     ("Freddie", "The vocalist."),
     ("John", "The bass guitarist."),
     ("Roger", "The drummer."),
 ]
 
 def complete_name(incomplete: str):
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)
             
 def main(
     name: str = typer.Option("World",
                       autocompletion=complete_name,
                       help="The name to say hi to."
     )
 ):
     typer.echo(f"Hello {name}")
 
 if __name__ == "__main__":
     typer.run(main)
```

これまでと同様にオプションに続けてタブキーを２度押下すると選択候補が表示されます。
 zsh
```
 % typer autocompletion2.py run --name[TAB][TAB]
 Brian    -- The guitarist.
 Freddie  -- The vocalist.
 John     -- The bass guitarist.
 Roger    -- The drummer.
```

これも、選択候補が表示されたときにタブキーを押下するたびに、選択候補が変わっていきます。
カーソルキーや `Ctl+n` ,  `Ctl+p` などのキー操作でも選択することができます。

> Bash ではパラメタの選択候補にヘルプメッセージをつけることができません。
> 対応可能なシェル： zsh, fish, PowerShell 

### 他のパラメタの選択を参照したい
これまでは選択候補を持つパラメタが１つ、もしくは１度だけでした。
次の例は `--name` オプションは複数与えることができます。

 autocompletion3.py
```
 from typing import List
 import typer
 
 valid_completion_items = [
     ("Brian", "The guitarist."),
     ("Freddie", "The vocalist."),
     ("John", "The bass guitarist."),
     ("Roger", "The drummer."),
 ]
 
 def complete_name(ctx: typer.Context, incomplete: str):
     names = ctx.params.get("name") or []
     for name, help_text in valid_completion_items:
         if name.startswith(incomplete) and name not in names:
             yield (name, help_text)
 def main(
     name: List[str] = typer.Option(["World"],
                             autocompletion=complete_name,
                             help="The name to say hi to."
     )
 ):
     for n in name:
         typer.echo(f"Hello {n}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 zsh
```
 % typer  autocompletion3.py run --name Brian --name [TAB]
 Freddie  -- The vocalist.
 John     -- The bass guitarist.
 Roger    -- The drummer.
```

この例でのポイントは、コールバック関数で `ctx.params.get("name")` を使って既に選択されたものを取得していることです。
これにより、選択済みのものが除かれた選択候補が表示されます。

### コマンドラインの状態を参照したい
コールバック関数で引数に  `args: List[str]` と受けておくと、
補完する前のマンドラインを参照することができます。

 autocompletion4.py
```
 from typing import List
 import typer
 
 valid_completion_items = [
     ("Brian", "The guitarist."),
     ("Freddie", "The vocalist."),
     ("John", "The bass guitarist."),
     ("Roger", "The drummer."),
 ]
 
 def complete_name(args: List[str], incomplete: str):
     typer.echo(f"{args}", err=True)
     for name, help_text in valid_completion_items:
         if name.startswith(incomplete):
             yield (name, help_text)
 
 def main(
     name: str = typer.Option("World",
                       autocompletion=complete_name,
                       help="The name to say hi to."
     )
 ):
     typer.echo(f"Hello {name}")
 
 if __name__ == "__main__":
     typer.run(main)
```

 zs
```
 % typer  autocompletion4.py run --name
 ['autocompletion4.py', 'run', '--name']
                                                       typer  autocompletion4.py run --name
 Brian    -- The guitarist.
 Freddie  -- The vocalist.
 John     -- The bass guitarist.
 Roger    -- The drummer.
```

### サブコマンド処理
 `typer.Typer()` アプリケーションインスタン( `app` )を生成して、 `@app.command()` で関数をデコレートすると、git などのようなサブコマンドを持つアプリケーションを作ることができます。
 subcommand.py
```
 import typer
 
 app = typer.Typer()
 
 @app.command()
 def initdb(dbname: str):
     typer.echo(f'Initialized the database {dbname}')
 
 @app.command()
 def dropdb(force: bool = typer.Option(False, '--force',
                                       help='drop db anyway'),
            dbname: str = typer.Argument(...)
 ):
     typer.echo(f'Force Flag: {force}')
     typer.echo(f'Droped the database: {dbname}')
 
 
 if __name__ == "__main__":
     app()
```

 bash
```
 % python subcommand.py --help
 Usage: subcommand.py [OPTIONS] COMMAND [ARGS]...
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 Commands:
   dropdb
   initdb
 
 % python subcommand.py initdb --help
 Usage: subcommand.py initdb [OPTIONS] DBNAME
 
 Arguments:
   DBNAME  [required]
 
 Options:
   --help  Show this message and exit.
   
 % python subcommand.py dropdb --help
 Usage: subcommand.py dropdb [OPTIONS] DBNAME
 
 Arguments:
   DBNAME  [required]
 
 Options:
   --force  drop db anyway  [default: False]
   --help   Show this message and exit.
 
 % python subcommand.py initdb mydb
 Initialized the database mydb
 
 % python subcommand.py dropdb mydb
 Force Flag: False
 Droped the database: mydb
 
 % python subcommand.py dropdb --force mydb
 Force Flag: True
 Droped the database: mydb
```

サブコマンドの右側はすべてそのサブコマンドの関数に渡されるコマンドラインとなります。

### サブコマンドのヘルプ表示
コマンド全体のヘルプメッセージはアプリケーションインスタンスの生成時に `typer.Typer()` に  `help` 引数で与えます。
各サブコマンドとなる関数をデコレートするときの `@app.command()` に `help` 引数で与えるか、省略された場合は関数の docstrings が使用されます。
サブコマンド名はデフォルトでは関数名が使用されますが、別名にしたいときは
 `@app.command()` に文字列として与えます。

 subcommand2.py
```
 import typer
 
 app = typer.Typer(help='Database manager')
 
 @app.command(help='Initializing DATABASE')
 def initdb(dbname: str):
     """
     initializing database.
     """
     typer.echo(f'Initialized the database {dbname}')
 
 @app.command("dropdb")
 def delete_db(force: bool = typer.Option(False, '--force',
                            help='drop db anyway'),
            dbname: str = typer.Argument(...)
 ):
     """
     Drop database.
     """
     typer.echo(f'Force Flag: {force}')
     typer.echo(f'Droped the database: {dbname}')
```

 zsh
```
 % python subcommand2.py --help
 Usage: subcommand2.py [OPTIONS] COMMAND [ARGS]...
 
   Database manager
 
 Options:
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 Commands:
   dropdb  Drop database.
   initdb  Initializing DATABASE.
```

### サブコマンド共通のパラメタを処理したい
 `typer.Typer()` で生成するアプリケーションインスタンスはサブコマンドをもたせることができますが、コマンドラインは各サブコマンドの関数に渡されるため、このままではコマンド全体のオプションなどを処理することできません。
そうしたときに、 `@app.callback()` を使用します。

次の例ではグロール変数  `state` に  `verbose` フラグを保持していて、
各サブコマンドをこの値を参照するようにしています。

 subcommand3.py
```
 import typer
 
 state = {'verbose': False }
 app = typer.Typer(help='Database manager')
 
 @app.command(help='Initializing DATABASE')
 def initdb(dbname: str):
     """
     Initializing database.
     """
     if state["verbose"]:
        typer.echo("running initializing database")
     typer.echo(f'Initialized the database {dbname}')
     typer.echo(f'Force Flag: {force}')
     if state["verbose"]:
        typer.echo("running drop database")
     typer.echo(f'Droped the database: {dbname}')
 
 @app.callback()
 def main(verbose: bool = typer.Option(False, '--verbose')):
     if verbose:
         typer.echo("Will write verbose output")
         state["verbose"] = True
 
 if __name__ == "__main__":
     app()
```

 zsh
```
 % python subcommand3.py --help
 Usage: subcommand3.py [OPTIONS] COMMAND [ARGS]...
 
   Database manager
 
 Options:
   --verbose             [default: False]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 Commands:
   dropdb  Drop database.
   initdb  Initializing DATABASE
 
 % python subcommand3.py initdb mydb
 Initialized the database mydb
 
 % python subcommand3.py --verbose initdb mydb
 Will write verbose output
 running initializing database
 Initialized the database mydb
```

 `@app.callback()` はコマンドラインのサブコマンドより前にあるパラメタをデコレートした関数に渡します。

同様のことは `typer.Typer()` でアプリケーションインスタンス生成時に `callback` 引数でコールバック関数を与えることができます。
ただし、 `@app.callback()` は生成時に与えたコールバック関数の指示を上書きします。

コールバック関数の定義で  `ctx: typer.Context` で受けおくと、
 `ctx.invoked_subcommand` で実行するサブコマンドを知ることができます。
引数は変数ですので、 `ctx` でなくても構いません。

 subcommand4.py
```
 import typer
 
 state = {'verbose': False }
 
 def app_callback(
 　　　　　ctx: typer.Context,
 　　　　　verbose: bool = typer.Option(False, '--verbose')):
     typer.echo(f"Running a command {ctx.invoked_subcommand}")
     if verbose:
         typer.echo("Will write verbose output")
         state["verbose"] = True
 
 app = typer.Typer(help='Database manager',
                   callback=app_callback)
 
 @app.command(help='Initializing DATABASE')
 def initdb(dbname: str):
     """
     Initializing database.
     """
     if state["verbose"]:
        typer.echo("running initializing database")
     typer.echo(f'Initialized the database {dbname}')
 @app.command("dropdb")
 def delete_db(force: bool = typer.Option(False, '--force',
                            help='drop db anyway'),
            dbname: str = typer.Argument(...)
 ):
     """
     Drop database.
     """
     typer.echo(f'Force Flag: {force}')
     if state["verbose"]:
        typer.echo("running drop database")
     typer.echo(f'Droped the database: {dbname}')
 
 if __name__ == "__main__":
     app()
```

 zsh
```
 % python subcommand4.py --help
 Usage: subcommand4.py [OPTIONS] COMMAND [ARGS]...
 
   Database manager
 
 Options:
   --verbose             [default: False]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 Commands:
   dropdb  Drop database.
   initdb  Initializing DATABASE
 
 % python subcommand4.py initdb mydb
 Running a command initdb
 Initialized the database mydb
 
 % python subcommand4.py --verbose initdb mydb
 Running a command initdb
 Will write verbose output
 running initializing database
 Initialized the database mydb
```

ヘルプメッセージを表示するためにコールバック関数を使用することもできます。

 subcommand.py
```
 import typer
 
 app = typer.Typer()
 
 @app.callback()
 def callback():
     """
     Manage users CLI app.
 
     Use it with the create command.
 
     A new user with the given NAME will be created.
     """
 
 @app.command()
 def create(name: str):
     typer.echo(f"Creating user: {name}")
  
  @app.command()
  def delete(name: str):
      typer.echo(f"Deleting user: {name}")
 
 if __name__ == "__main__":
     app()
 
```

デフォルトではコールバック関数はサブコマンドが実行される直前に呼び出されます。このときサブコマンドが与えられていないとヘルプメッセージが表示されます。
 `--version` のようなオプションは、サブコマンドを取る必要がありません。
こうしたときは、 `@app.command()` に　 `invoke_without_command=True` を与えておきます。
 `ctx.invoked_subcommand` が  `None` のときはサブコマンドではなく、メインコマンドが実行されていることになります。

 subcommand6.py
```
 import os
 import typer
 
 __MYPROG__ = os.path.basename(__file__)
 __VERSION__ = '1.0'
 
 app = typer.Typer()
 
 @app.command()
 def initdb(dbname: str):
     typer.echo(f'Initialized the database {dbname}')
 
 @app.command()
 def dropdb(force: bool = typer.Option(False, '--force',
                            help='drop db anyway'),
            dbname: str = typer.Argument(...)
 ):
     typer.echo(f'Force Flag: {force}')
     typer.echo(f'Droped the database: {dbname}')
     
 @app.callback(invoke_without_command=True)
 def print_version(ctx: typer.Context,
           version: bool = typer.Option(False, '--version')
 ):
     if version:
         typer.echo(f'{__MYPROG__} - Version: {__VERSION__}')
         raise typer.Exit()
     if ctx.invoked_subcommand is None:
         typer.echo('This is main command')
 
 if __name__ == "__main__":
     app()
```

 zsh
```
 % python subcommand6.py --help
 Usage: subcommand6.py [OPTIONS] COMMAND [ARGS]...
 
 Options:
   --version             [default: False]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 Commands:
   dropdb
   initdb
 
 % python subcommand6.py --version
 subcommand6.py - Version: 1.0
 
 % python subcommand6.py
 This is main command
 
 % python subcommand6.py initdb mydb
 Initialized the database mydb
```

### コマンドラインの文字列をそのまま受け取りたい
コマンドのオプションや引数として登録したパラメタの他に、コマンドラインの文字列をそのまま受け取ることもできます。
 context.py
```
 import typer
 
 app = typer.Typer()
 
 @app.command(
     context_settings={'allow_extra_args': True, 
                       'ignore_unknown_options': True}
 )
 def main(version: bool = typer.Option(False, '--version'),
          unkown_args: typer.Context = typer.Option(None)
 ):
     typer.echo(f'Got known arg version: {version}')
     for unknown_arg in unkown_args.args:
         typer.echo(f'Got unknown arg: {unknown_arg}')
 
 if __name__ == "__main__":
     app()
```

 zsh
```
 % python context.py --help
 Usage: context.py [OPTIONS]
 
 Options:
   --version             [default: False]
   --install-completion  Install completion for the current shell.
   --show-completion     Show completion for the current shell, to copy it or
                         customize the installation.
 
   --help                Show this message and exit.
 
 % python context.py --version --name Jack
 Got known arg version: True
 Got unknown arg: --name
 Got unknown arg: Jack
```

#### 処理中にプログレスバーを表示させたい
少し時間がかかるような処理などで、 `typer.progressbar()` を使うとプログレスバーを表示してくれます。
 progressbar.py
```
 import time
 import typer
 
 def count_something(count):
     for num in range(count):
         yield num
 
 def main(count: int = typer.Option(100,
                             '--count', min=10, max=500)
 ):
     total = 0
     with typer.progressbar(count_something(count),
                           length=count,
                           label="Processing") as progress:
         for value in progress:
             # Fake processing time
             time.sleep(0.01)
             total += 1
     typer.echo(f"Processed {total} things.")
 
 if __name__ == "__main__":
     typer.run(main)
```


### アプリケーションのテスト
 `typer.testing.CliRunner` を使うと、関数をコマンドラインスクリプトとして実行してくれます。
 `CliRunner.invoke()` メソッドは、アプリケーションインスタンスを実行して、出力をバイトデータとバイナリデータの両方として取り込みます。
返り値は、キャプチャされた出力データ、終了コード、およびオプションの例外が添付された `Result` オブジェクトとなります。

前述した  `greeting.py` をテストしてみます。
もとのコードではテストを実行することができないので、次のように修正します。
 greeting2.py
```
 import typer
 
 app = typer.Typer()
 
 @app.command()
 def hello(count: int = typer.Option(1, '-C', '--count',
                                    help='Number of greetings.'),
            name: str = typer.Option(..., prompt='Your Name',
                                     help='The person to greet.'),
          ):
     """COUNTで与えた回数だけHelloする"""
     for x in range(count):
         typer.echo(f'Hello {name}')
 
 if __name__ == '__main__':
     app()
```

これをテストするためのコードは次のようになります。
 test_greeting.py
```
 from typer.testing import CliRunner
 from greeting2 import app
 
 runner = CliRunner()
 
 def test_app():
   result = runner.invoke(app, ['--name', 'Peter'])
   assert result.exit_code == 0
   assert result.output == 'Hello Peter\n'
 
   result = runner.invoke(app, ['--name', 'Jack', '-C', '2'])
   assert result.exit_code == 0
   assert result.output == 'Hello Jack\nHello Jack\n'
 
 if __name__ == '__main__':
     test_app()
 
```


 `invoke()` メソッドの第１引数にテストしたい関数名、第２引数にコマンドラインオプションをリストで与えます。テストする関数をコマンドスクリプトとして実行した結果は、 `Result` オブジェクトにセットされて戻されます。

-  `exception` : 例外が発生したときにセットされる例外情報
-  `exit_code` ：終了コード
-  `stdout` : 標準出力をテキストとして取り込んだ文字列
-  `stdout_bytes` : 標準出力をバイナリとして取り込んだデータ
-  `stderr` : 標準エラー出力をテキストとして取り込んだ文字列
-  `stderr_bytes` ：標準エラー出力をバイナリとして取り込んだデータ
-  `output` : 標準出力と同じ

### pytest

pytestはPythonのテストフレームワークで、テストに失敗した原因がわかりやすく、よく利用されているものです。

 conda
```
 $ conda install pytest
 pip
```
 $ pip install pytest
```

pytest はカレントディレクトリにある `test_` で始まるファイルを検出し、自動的にテストします。


 zsh
```
 % pytest
 ============================= test session starts ==============================
 platform darwin -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
 rootdir: /Users/goichiiisaka/Projects/Python.Osaka/Typer_tutorial
 collected 1 item
 
 test_greeting.py .                                                       [100%]
 
 ============================== 1 passed in 0.08s ===============================
```

参考：
　[typerオフィシャルサイト ](https://typer.tiangolo.com/)
　[pytest オフィシャルサイト ](https://docs.pytest.org/en/stable/)


