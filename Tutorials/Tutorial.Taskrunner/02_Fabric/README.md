タスクランナーFabric2を使ってみよう
=================
## Fabric2 について
Fabric はタスクランナー invoke をSSHライブラリでラッピングした Python2 (Python2.5-2.7) で実装された、アプリケーションのデプロイメント(展開)や、システム管理でのSSHの使用を合理化するためのライブラリおよびコマンドラインツールです。複数のサーバーを非常に簡単にリモート管理できます。
Fabric2は Fabric を Python3 に対応させるため、ゼロから再構築されたバージョンです。そのため、Fabric2 はFabric との互換性を失っています。
PYPIでは Fabric を Python3に移植したバージョンも出ていますが、Fabric2 を利用することをお勧めします。

Fabirc2 では認証処理とシェルコマンドの実行をサポートするツールで、バックエンドには[Paramiko http://www.paramiko.org/]と[Invoke ](https://www.pyinvoke.org/) が使用されています。 

### Invoke と Fabric2
両方ともタスクランナーの機能を提供しますが、Invoke と Fabric2 の大きな違いは、SSHを経由してタスクを実行するかどうでかです。
自ノードであってもSSHを経由してタスクを実行することもありえます。
SSHを経由しない場合では、基本的にはタスクのすべて処理を invoke で完結させることができます。
Invoke では `Conetext` オブジェクトを使用して、 `run()` APIでタスクを実行します。 


```
 from invoke import task
 
 @task
 def do_something(c):
     with c.cd("some-directory"):
         c.run("ls")
```

Fabric2 では、多くの場合対象ホストへの接続を行う `Connection` オブジェクトを生成したうえで、 `run()` メソッドでタスクを実行します。


```
 from fabric.connection import Connection
 
 connection = Connection("username@remote_host")
 print(connection.run("ls"))
```

### Fabric2 と Ansible 
Pythonで実装された関連するツールには Ansible があります。
Fabric2 と Ansible との相違点と類似点のリストは次のとおりです。

　Ansible の学習コストは Fabric よりも高くなります。
　	Ansible を理解するにはPythonに加えてさらなる努力と時間が必要です
　	FabricではPythonの知識があれば、比較的簡単に目的を達成することができます。
　Ansibleは Fabric2 より強力で多機能です。
　	Ansible は多層インフラストラクチャをモデル化のための複雑なセマンティクスを提供します。
　	Anisbe は基本的に同じ操作を何度繰り返しても同じ結果が得られる(冪等性)を保証します。
　記述するコードのタイプが異なります。
  - FabricにはAnsibleより基本的なAPIがあり、Pythonで記述します。
  - AnsibleはYAMLフォーマットで記述します。加えて、各種のモジュールを利用して構成定義の豊富さを補強します。
　AnsibleとFabricはどちらも、SSHを介してタスクを実行します。
  - Fabricはリモートマシンに対して単純なコマンドラインステートメントを実行します。
  - Ansibleはモジュールをリモートマシンにプッシュしてから、そのモジュールをリモートで実行します。

両者の最大の違いは、機能と複雑さです。
数ノード程度に対してタスクを実行するのであれば、Ansible は必要以上の重厚なツールとなってしまうかもしれません。

## fabric2 のインストール
fabric2 は拡張モジュールなのでインストールする必要があります。

 zsh
```
 % pip install fabric2
```

## Fabric2 の利用方法
今、web.example.com にユーザ名 webapp のアカウントがあるときで、
パスワード認証をすることなくログインできる状態であれば、
次のコマンド実行することができます。

 fabric_sample.py
```
 from fabric2 import Connection
 
 result = Connection('web.example.com', user='webapp').run('uname -s', hide=True)
 msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
 print(msg.format(result))
```

 zsh
```
 % python fabric_sample.py
 Ran 'uname -s' on web.example.com, got stdout:
 Linux
 
```

 `Connection` クラス、は対象ホストへSSH接続を行い、 `run()` メソッドなどのFabricのAPIを提供します。  `Connection` オブジェクトを作成するためには、少なくともアクセス可能なリモートシステムのホスト名が必要であり、ユーザー名やポート番号を引数で与えることができます。これらは、キーワード引数で明示的に指定することができます。

```
 Connection(host='web.example.com', user='webapp', port=2202)
```

あるいは、 `[user@]host[:port]` 文字列をhost引数に詰め込むことによって接続することができます。この方法は簡単ですが、あいまいさが発生する場合はキーワード引数を使うようにしてください。

```
 Connection('webapp@web.example.com:2202')
```

 `Connection` オブジェクトのメソッド（ `run()` など）は通常、 `invoke.runners.Result` （またはそのサブクラス）のインスタンスを返します。これには、接続情報、要求された内容、リモートアクションの発生中に発生した内容、最終結果が格納されています。

 `Connection` クラスのコンストラクタに `connect_kwargs` 引数を使用することで、秘密鍵やタイムアウトなどの多くの低レベルのSSH接続のパラメタをバックエンドのSSHに直接指定できます。

### 自動応答によるスーパーユーザー権限
リモートシステムのスーパーユーザーとして実行する必要があれば、 `run()` メソッドを介して `sudo` プログラムを呼び出すことができます。
リモートシステムがパスワード不要でsudo実行ができるように構成されていない場合は、以下のように端末からパスワードプロンプトに応答します。
リモート疑似端末(pseudo terminal)を要求する必要があるので、 `pty=True` を与えることに注意してください。

 fabric2_sudo.py
```
 from fabric2 import Connection
 c = Connection('webapp@web.example.com')
 c.run('sudo id', pty=True)
```

 zsh
```
 % python fabric_sudo.py
 [sudo] password for webapp:
 uid=0(root) gid=0(root) groups=0(root)
```

毎回手作業でパスワードを与えることは、つまらなってしまいます。 ありがたいことに、Invokeの強力なコマンド実行機能には、事前定義された入力を使用してプログラム出力に自動応答する機能が含まれています。 これをsudoに使用することができます。

 fabric2_sudo_auto.py
```
 import os
 from invoke import Responder
 from fabric2 import Connection
 
 user = 'webapp'
 password = os.environ.get('SUDO_PASSWORD')
 
 c = Connection('webapp@web.example.com')
 sudopass = Responder(
     pattern=rf'\[sudo\] password for {user}:',
     response=f'{password}\n',
 )
 c.run('sudo whoami', pty=True, watchers=[sudopass])
```

 zsh
```
 % python fabric_sudo_auto.py
 [sudo] password for webapp:
 root
```

このコードが実行されたときに、ユーザーは何も入力する必要はありません。
環境変数  `SUDO_PASSWORD` で設定したパスワード文字列が `password` にセットされて、リモートプログラムに自動的に送信されます。

> セキュリティーに関する注意点：
> 安直にパスワードなどをコードに記述することは、避けるようにしましょう。

### sudoヘルパー
ここでは `Watcher` / `Responder` の使用はうまく機能しますが、毎回設定する必要のある多くの処理項目(ボイラープレート: boilerplate ) があります。特に、実際のユースケースでは、パスワード認証の失敗や不正を検出するためにより多くの処理が必要になるためです。
> ボイラープレート(boilerplate):
> プログラミング言語での意味は、仕様上省略不能で、かつほとんど変更を加えることなく、
> 多くの場所に組み込む必要があるソースコードのことを言います。

これを支援するために、Invokeはボイラープレートのほとんどを処理する `Context.sudo()` メソッドを提供します（ `Connection` クラスは `Context` クラスをサブクラス化するため、このメソッドを自由に使用することができます。）。sudo は、ユーザーが指示しないことは何もしません。
ユーザーが行う必要があるのは、構成ファイルや環境変数、または端末からプロンプトで入力されるなどにより、 `sudo.password` の値をセットし、 `Connection.sudo()` が行う残り処理を確認することだけです。 
次のコードは、getpass モジュールでユーザからパスワードを取得して、 `Connection` クラスのコンストラクタに `config` 引数で与えています。

 fabric2_sudo_getpass.py
```
 import getpass
 from fabric2 import Connection, Config
 
 sudo_pass = getpass.getpass("What's your sudo password?")
 config = Config(overrides={'sudo': {'password': sudo_pass}})
 c = Connection('webapp@web.example.com', config=config)
 c.sudo('whoami', hide='stderr')
```

 zsh
```
 % python fabric_sudo_getpass.py
 What's your sudo password?
 root
```

この例では、実行時にsudoパスワードを事前に入力しました。 実際の状況では、構成システムを介してパスワード文字列を与えることもできます。理想的には、シークレット管理システムを使用するようにします。

### ファイル転送
シェルコマンドの実行に加えて、SSH接続の他の一般的な使用法はファイル転送です。  `Connection.put()` と `Connection.get()` は、この機能を実現を実現します。
 fabric_put_get.py
```
 from fabric2 import Connection
 
 conn = Connection('webapp@web.example.com')
 
 # result = conn.put(local='./dummy.txt', remote='/tmp/')
 result = conn.put('./dummy.txt', remote='/tmp/')
 print("Uploaded {0.local} to {0.remote}".format(result))
 
 # result = conn.get(remote='/tmp/dummy.txt', local='./junk.txt')
 result = conn.get('/tmp/dummy.txt', local='./junk.txt')
 print("Download {0.local} to {0.remote}".format(result))
```

 `put()` と `get()` メソッドは通常、引数の評価については、 `cp` コマンドや `scp` 、 `sftp` の使用方法に従います。たとえば、この例では、 `remote` 引数にファイルパス指定には、ディレクトリだけを与えることができます。

### 複数のアクション
ワンライナーは良い例ですが、必ずしも現実的なユースケースではありません。通常、何かの処理行うためには複数の手順が必要になります。最も基本的なレベルでは、 `Connection` クラスのメソッドを複数回呼び出すことで、複数のアクションを実行することができます。

 fabric_multiple_action.py
```
 from fabric2 import Connection
 c = Connection('webapp@web.example.com')
 c.put('dummy.txt', '/tmp')
 c.run('cat /tmp/dummy.txt')
```

このようなコードのブロックを、呼び出し元からの `Connection` オブジェクトを引数として受け取る関数にして、再利用をしやすくすることができます。（必ずしも、そうする必要はありませんが...）

 fabric_multiple_action_function.py
```
 from fabric2 import Connection
 
 def upload_and_cat(c, filename, remote_dir='/tmp'):
     c.put(filename, remote_dir)
     c.run(f'cat {remote_dir}/{filename}')
 
 
 c = Connection('webapp@web.example.com')
 upload_and_cat(c, 'dummy.txt')
```

### 複数のサーバーへ接続
実際のユースケースの多くでは、複数のサーバーで処理が実行されます。 簡単なアプローチは、接続するシステムのホスト名のリストやタプル、または `map()` を介した `Connection` オブジェクトを反復処理することです。
 fabric_multiple_server.py
```
 from fabric2 import Connection
 
 for host in ('webapp@web1', 'webapp@web2'):
     result = Connection(host).run('uname -s')
     print("{}: {}".format(host, result.stdout.strip()))
```

この方法はうまく機能しますが、ユースケースがより複雑になるにつれて、ホストのコレクションを単一のオブジェクトと考えると便利な場合があります。 1つ以上の  `Connection` オブジェクトをラップした、同様のAPIを提供する `Group` クラスを使用します。
具体的には、 `SerialGroup` クラスや `ThreadingGroup` クラスなどのサブクラスの1つを使用する必要があります。

 `SerialGroup` クラスを使用した前の例は、次のようになります。
 fabric_server_group.py
```
 from fabric2 import SerialGroup as Group
 
 conn = Group('webapp@web1', 'webapp@web2')
 results = con.run('uname -s')
 
 for connection, result in results.items():
     print("{0.host}: {1.stdout}".format(connection, result))
```

 `Connection` クラスのメソッドが単一の `Result` オブジェクト（例： `fabric.runners.Result` ）を返す場合では、 `SerialGroup` クラスのメソッドは `GroupResult` オブジェクトを返します。これは、個々の接続ごとの結果と実行全体に関するメタデータへのアクセスできるようにした `dict` 型のようなオブジェクトです。

グループ内の個々の接続でエラーが発生すると、 `GroupResult` は `GroupException` 例外を発生します。 したがって、 `SerialGroup` クラスのメソッドの動作は個別の `Connection` クラスのメソッドの動作に似ており、成功した場合は値を返し、失敗した場合は例外を発生させます。

すべてをまとめる
最後に、最も現実的な使用例を説明しましょう。例えば、コマンドやファイル転送のバンドルがあり、それを複数のサーバーに適用したい場合です。 この処理を行うためには、複数の `Group` クラスのメソッド呼び出して使用することができます。

 fabric2_pool.py
```
 from fabric2 import SerialGroup as Group
 
 pool = Group('webapp@web1', 'webapp@web2')
 pool.put('dummy.txt', '/tmp')
 pool.run('cat /tmp/dummy.txt')
 
```

実はこのコードは期待どおりには動作しません。 `SerialGroup` およびベースクラスの `Group` クラスは、 `get()` メソッドは使用できるものの、 `put()` メソッドが提供されていないためです。

> この機能は、Fabric1.xのAPIで提供されていました。

また、この方法では、ロジックが必要になるとすぐに不十分になってしまいます。たとえば、 `/tmp` が空のときには、前述のサンプルコードで例示した  `upload_and_cat()` 関数だけを実行したい場合などです。 この種のチェックを実行するには、サーバーごとに実行する必要があります。
こうした場合では、 `Connection` オブジェクトのイテラブルを使用することです。ただし、これにより、 `Group` クラスを使用する利点が少なくなってしまうことには留意が必要です。

 fabric2_multiple_server2.py
```
 from fabric2 import Connection
 
 servers = ('webapp@web1', 'webapp@web2')
 
 for host in servers:
     c = Connection(host)
     if c.run('test -f /tmp/dummy.txt', warn=True).failed:
         c.put('dummy.txt', '/tmp')
         c.run('cat /tmp/dummy.txt')
```

当然のことながら、 `upload_and_cat()` を使うこともできます。
 fabric2_multiple_server3.py
```
 from fabric2 import Connection
 
 servers = ('webapp@web1', 'webapp@web2')
 
 def upload_and_cat(c, filename, remote_dir='/tmp'):
     if c.run(ｆ'test -f {remote_dir}/{filename}', warn=True).failed:
         c.put(filename, remote_dir)
         c.run(f'cat {remote_dir}/{filename}')
 
 for host in servers:
     c = Connection(host)
     upload_and_cat(c, 'dummy.txt')
```

この方法での欠点は、実行結果を確認することが煩雑になることです。 `Group.run()` メソッドでは、タスクの実行結果が `Result` オブジェクトに集約されますが、 `Connection` オブジェクトのイテラブルを使用した場合は、自分で処理する必要があります。

## fab2コマンドラインツール
任意のサーバーでアプリケーションをデプロイする場合や、システム管理のためのタスクを実行する場合など、コマンドラインからfabricコードを実行すると便利なことが多くなります。Fabricライブラリを含むコードは、通常の Invokeタスクを使用することができますが、別の方法として、Fabric独自の `fab2` コマンドがあります。

 `fab2` コマンドは、ネットワーク指向ツールとも言えるもので、Invokeのコマンドラインインタフェースの機能に、ホスト選択などの機能でラップし、すべてのタスクでホストを指定しなくても、さまざまなサーバーでタスクをすばやく実行できるようにします。

 fabfile.py
```
 from fabric2 import Connection, task
 
 @task(name='remote')
 def remote_exectutor(c, cmd):
     c.run(cmd)
```

zsh
```
 % fab2 --list
 Available tasks:
 
   remote
 
 (jupyter) goichiiisaka@GoichiMacBook Fabric2_tutorial % fab2 --help remote
 Usage: fab2 [--core-opts] remote [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -c STRING, --cmd=STRING
 
```


invole がデフォルトで読み込むファイルが  `task.py` ですが、
 `fab2` コマンドはカレントディレクトリにある  `fabfile.py` を読み込みます。
このファイル名を変更したい場合は、 `--connection` オプションで次のように与えます。
 `fab2` がモジュールとして読み込むため、拡張子( `.py` )が不要だということに注意してください。
 zsh
```
 % mv fabfile.py fabtask.py
 % fab2 --collection fabtask --list
 Available tasks:
 
   remote
```

>残念なことですが、 fab2 のタスクでは  `put()` メソッドを使用することができません。


### Fabric2 から Invoke のタスクを利用する
ドキュメントには具体的な例示はされていないのですが、
Fabric2の `Connection` クラスは、Invoke の  `Context` クラスのサブクラスです。
このため、invoke の `Context` オブジェクトとして `Connetion` オブジェクトを与えることができます。


```
 from fabric import Connection
 from fabric.tasks import task
 
 @task
 def sub_task(c):
     with c.cd("/path/to/somewhere"):
         c.run("ls")
 
 @task
 def main_task(c):
     con = Connection("username@remote_host")
     print(sub_task(con))
```



 config.py
```
 import pydantic
 from typing import Optional
 
 class BaseSettings(pydantic.BaseSettings):
     class Config:
         env_prefix = ""
         env_file = ".env"
         env_file_encoding = "utf-8"
         use_enum_values = True
 
 class FabricSettings(BaseSettings):
     FABRIC_TASK_HOST: str = "localhost"
     FABRIC_TASK_USER: str = "webapp"
     FABRIC_TASK_SSH_KEYFILE: str = "/var/webapp/.ssh/id_rsa"
     FABRIC_TASK_SUDO_SCRET_KEY: Optional[str] = None
     FABRIC_TASK_SUDO_PASSWORD: Optional[str] = None
     FABRIC_TASK_DEBUG: bool = False
 
 class InvalidConfigException(Exception):
     """Invalid Config - something is wrong with the configuration,
        and it should not be accepted, as some task will not work with it.
     """
     pass
```


 fabric_task.py
```
 from config import FabricSettings, InvaidConfigException
 
 class FabricTask(object):
     def __init__(self, conf=None):
         if conf is not None:
             self.conf = conf
         else:
             self.conf = FabricBaseSettings().dict()
             self.init_app()
             
     def init_app(self):
         for key in self.conf.keys():
             val = self.conf.get(key, None)
             if val is None:
                 raise  InvalidConfigException("Invalid configuration.")
     
         self.targethost = self._getcv("HOST")
         self.fabric_key = self._getcv("SUDO_SCRET_KEY")
         self.sudo_password = self._getcv("SUDO_PASSWORD")
         self.fabconf = Config(overrides={
               　　　　　　　"sudo": {"password": self.sudo_password},
                            "user": self._getcv("USER"),
                            "key_filename": self._getcv("SSH_KEYFILE")
                         })
         def _getcv(self, key, default=None):
             key = 'FABRIC_TASK_' + key
             return self.conf.get(key, default)
     
         def runner(self, function, *args, **kwargs):
             """ Task runner - set your task along with args and kwargs
     
             :param function: The function for some tasks
             :type function: callable
             """
     
             with Connection(self.targethost, config=self.fabconf) as c:
                 return function(c, *args, **kwargs)
                 
```

 tasks.py
```
 import os
 import tempfile
 from patchwork import files
 
 basedir = os.path.abspath(os.path.dirname(__file__))
 command = f"{basedir}/scripts/manage_pubkey.sh"
 
 def install_publickey(c, userid, homedir, pubkey):
    """Install to Register Public Key
    :param c: Flask_Fabric Connnext within to execute commands.
    :param homedir: directory path of homedir
    :param userid: directory path of homedir
    :param pubkey: string of ssh public key
    """
    dummyfile = tempfile.mkstemp()[1]
    files.append(c, f"{dummyfile}", pubkey)
    cmd = f'{command} install {userid} {homedir} {dummyfile}'
    rv = c.sudo(f"{cmd}", pty=True, warn=True, hide="stderr")
    logger.debug(f'TASK: {cmd} return_code={rv.return_code}')
    c.run(f"rm -f {dummyfile}")
 
    return rv.return_code
```

 app.py
```
 from tasks import check_publickey
 
 tasks = FabricTask()
 rv = task.runner(install_publickey, user.userid, user.homedir, pubkey)
```





