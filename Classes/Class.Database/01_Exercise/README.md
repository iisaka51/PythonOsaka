演習１：実際にデータを操作してみよう
=================

## 演習1.1: TinyDB
演習としてTinyDBを使ってタスク管理を行うための小さなコンソールアプリケーションを作成してみましょう。

はじめに、次のコードはタスク管理のためのモデルクラスのスニペットです。

 tinydb_task.py
```
 from tinydb_base import DatabaseBase
 
 class TaskDB(DatabaseBase):
 
     def __init__(self,
         file='tasks.json',
         table='tasks',
         requiredKeys='title:str,description:str,done:bool'):
         super().__init__(file=file,
                          table=table,
                          requiredKeys=requiredKeys)
 
         self.db = self.createObj().db
         self.tbl = self.createObj().tbl
 
     def _create_task(self, title='', descripton='', done=False):
         task = {'titile': title, 'decription': description, 'done': done}
         return task
 
     def add(self, title, description):
         return task_id
 
     def get(self, task_id=None):
         return None
 
     def remove(self, task_id=None):
         return task_id
 
     def update(self, title, description, task_id=None):
         return task_id
 
     def done(self, task_id=None):
         return task_id
 
     def list(self):
         return self.tbl.all()
```

データベースには `title` 、 `description` 、 `done` のカラムを持っています。
初期データは次のものです。

 task_data.py
```
 tasks = [
       {
           'title': 'Buy Beer',
           'description': 'IPA 6 bottles',
           'done': False
       },
       {
           'title': 'Buy groceries',
           'description': 'Beef, Tofu, Sting Onion',
           'done': False
       }
 ]
```

データベースに初期データをインストールするためのサンプルです。

 tinydb_init.py
```
 from tinydb_task import *
 from task_data import task_data
 
 db = TaskDB()
 
 for t in task_data:
     db.tbl.insert(t)
 
 db.tbl.all()
```


ここで演習として作成するアプリケーションでは click と click-shell を使っていますので、次の準備を行ってください。
 bash
```
 $ pip install click-shell
```

次のコードはタスク管理アプリケーションのスニペットです。
 task_manager.py
```
 import click
 from click_shell import shell
 from task_model import *
 
 db = TaskDB()
 
 @shell(prompt='task> ', intro='Starting task manager...')
 def app():
     pass
 
 @app.command()
 @click.argument('title', nargs=1)
 @click.argument('description', nargs=1)
 def add(title, description):
     task_id = db.add(title, description)
     click.echo(f'id: {task_id} added')
 
 @app.command()
 @click.argument('task_id', type=int, nargs=1)
 @click.argument('title', nargs=1)
 @click.argument('description', nargs=1)
 def update(task_id, task):
     task_id = db.update(title, decription, task_id)
     click.echo(f'id: {task_id} updated')
 
 @app.command()
 @click.argument('task_id', type=int, nargs=1)
 def remove(task_id):
     db.remove(task_id)
     click.echo(f'id: {task_id} removed')
 
 @app.command()
 @click.argument('task_id', type=int, nargs=1)
 def get(task_id):
     task = db.get(task_id)
     click.echo(f'id: {task_id} {task}')
 
 @app.command()
 @click.argument('task_id', type=int, nargs=1)
 def done(task_id):
     task_id = db.update(task_id)
     click.echo(f'id: {task_id} set done flag.')
 
 @app.command()
 def listall():
     for task_id, task in enumerate(db.list()):
         click.echo(f'id: {task_id} {task}')
 
 if __name__ == '__main__':
     app()
 
```

 bash
```
 % python tinytask_manager.py --help
 Usage: task_manager.py [OPTIONS] COMMAND [ARGS]...
 
 Options:
   --help  Show this message and exit.
 
 Commands:
 　add
   done
   get
   listall
   remove
 
 % python tinytask_manager.py listall
 id:1 {'title': 'Buy Beer', 'description': 'IPA 6 bottles', 'done': False}
 id:2 {'title': 'Buy groceries', 'description': 'Beef, Tofu, Sting Onion', 'done': False}
 
 % python tinytask_manager.py
 Starting task manager...
 task> listall
 id:1 {'title': 'Buy Beer', 'description': 'IPA 6 bottles', 'done': False}
 id:2 {'title': 'Buy groceries', 'description': 'Beef, Tofu, Sting Onion', 'done': False}
 task> exit
 %
```

この段階では’ listall コマンドだけが使用できます。 `tinydb_task.py` を修正して、他のコマンドについても動作するようにしてみましょう。

#### ヒント
- 例外が発生したときの処理を忘れないようにしましょう。


## 演習1.2： ZODB チャレンジ課題
前述のタスク管理アプリケーション `task_manager.py` を ZODB を使って実装してみましょう。
実は、モデルクラスのインポートを変えるだけで対応可能です。

TinyDBのモデルクラス
python
```
 from tinydb_task import *
```
ZODBのモデルクラス
python
```
 from tinydb_task import *
```

ZODBでのモデルクラスのスニペットです。
 zodb_task.py
```
 import ZODB
 from persistent import Persistent
 from BTrees.OOBTree import BTree
 import transaction
 
 class Task(Persistent):
     def setTask(self, task):
         self.task = task
     def getTask(self):
         return self.task
     def compose(self, title='', description='', done=False):
         task = {'titile': title, 'decription': description, 'done': done}
         self.task = task
 
 class TaskDB():
     def __init__(self, file='tasks.fs'):
         self.open(file)
         self.root = self.connection.root
         if 'db' not in self.root._root:
             self.root.db = BTree()
         if 'tasks' not in self.root.db:
             self.root.db['tasks'] = list()
         self.tasks = self.root.db['tasks']
 
     def commit(self):
         return transaction.commit()
 
     def open(self, file):
         self.db = ZODB.DB(file)
         self.connection = self.db.open()
         return self.connection
 
     def close(self):
         return self.connection.close()
 
     def add(self):
         pass
 
     def get(self):
         pass
 
     def remove(self):
         pass
 
     def update(self):
         pass
 
     def done(self):
         pass
 
     def list(self):
         print(self.tasks)
         return list(map(lambda x: x.getTask(), self.tasks))
```

データベースに初期データを設定するサンプルです。
 zodb_init.py
```
 from zodb_task import *
 from task_data import task_data
 import transaction
 
 db = TaskDB()
 
 for t in task_data:
     task = Task()
     task.setTask(t)
     db.tasks.append(task)
 
 transaction.commit()
 db.connection.close()
```


#### ヒント
- Persistentクラスの派生クラスを作成します。
- トランザクションを考慮する必要があります。


## 参考資料
- [AirPort Data ](https://github.com/mihi-tr/Airport-Data)


