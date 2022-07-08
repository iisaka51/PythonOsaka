演習１：既存のデータをデータベース化してみよう
=================

## 事前準備としてのタイプヒント
Pythonの一般的な型はそのまま使えます。


```
 from datafiles import *

 class GenericType_demo(Modle):
 	id: int
 	name: str
 	value: float
 	data: dict
```

標準モジュールの typing を使うとタイプヒントの表現が広がります。

```
 from datafiles import *
 from typing import Union, Optional

 class Type_demo(Modle):
     id: int
     name: Optoonal[str] = None
     value: Union[ int, str, flot ]

```

Opional を使うと省略可能となり、 `None` などを設定することができます。
Union を使うと、列挙したいずれかの型を受け入れるものとして動作します。
ここで、改めて注意するべきことは、タイプヒントはあくまでヒントであって、言語レベルで型の強制まではできないということです。

Python 3.9 から組み込みの `list` と `dict` のタイプヒントがリスト表記( `[...]` )をサポートするようになったため、 `typing.List` と  `typing.Dict` は非推奨になりました。

## テストデータ
ここに次のようなデータがあります。
これをデータベース化してみましょう。

 move_data.py
```
 actor = [
     { 'name': 'Robert de Niro', 'birthday': '1943-08-17',
       'imdb': 'https://www.imdb.com/name/nm0000134/',
       'movies': [
         { 'title': 'Taxi Driver', 'year': 1976 },
         { 'title': 'The Deer Hunter', 'year': 1978 },
         { 'title': 'Falling in Love', 'year': 1984 },
         { 'title': 'The Intern', 'year': 2015 }
       ]
     },
     { 'name': 'Ann Hathaway', 'birthday': '1982-11-12',
       'imdb': 'https://www.imdb.com/name/nm0004266/',
       'movies': [
         { 'title': 'The Intern', 'year': 2015 },
         { 'title': 'The Dark Knight Rises', 'year': 2012 },
         { 'title': 'Les Misé rables', 'year': 2012 },
         { 'title': 'The Devil Wears Prada', 'year': 2006 }
       ]
     },
     { 'name': 'Clint Eastwood', 'birthday': '1930-05-31',
       'imdb': 'https://www.imdb.com/name/nm0000142/',
       'movies': [
         { 'title': 'Gran Torino', 'year': 2008 },
         { 'title': 'Million Dollar Baby', 'year': 2004 },
         { 'title': 'The Bridges of Madison County', 'year': 1995 }
       ]
     },
     { 'name': 'Meryl Streep', 'birthday': '1949-06-22',
       'imdb': 'https://www.imdb.com/name/nm0000658/',
       'movies': [
         { 'title': 'Falling in Love', 'year': 1984 },
         { 'title': 'The Bridges of Madison County', 'year': 1995 },
         { 'title': 'The Devil Wears Prada', 'year': 2006 },
         { 'title': 'Mamma Mia! Here We Go Again', 'year': 2018 }
       ]
     },
     { 'name': 'Morgan Freeman', 'birthday': '1937-06-01',
       'imdb': 'https://www.imdb.com/name/nm0000151/',
       'movies': [
         { 'title': 'Invictus', 'year': 2009 },
         { 'title': 'The Shawshank Redemption', 'year': 1994 },
         { 'title': 'The Bridges of Madison County', 'year': 1995 }
       ]
     },
     { 'name': 'Dennis Quaid', 'birthday': '1954-04-09',
       'imdb': 'https://www.imdb.com/name/nm0000598/',
       'movies': [
         { 'title': 'Freequency', 'year': 2009 },
         { 'title': 'The Rookie', 'year': 2002 }
       ]
     },
     { 'name': 'Kevin Costner', 'birthday': '1955-01-18',
       'imdb': 'https://www.imdb.com/name/nm0000126/',
       'movies': [
         { 'title': 'The Postman', 'year': 1997 },
         { 'title': 'Field of Drems', 'year': 1989 }
       ]
     },
     { 'name': 'Amy Modigan', 'birthday': '1950-09-11',
       'imdb': 'https://www.imdb.com/name/nm0000126/',
       'movies': [
         { 'title': 'Field of Drems', 'year': 1989 },
         { 'title': 'Gone Baby Gone', 'year': 2007 }
       ]
     },
     { 'name': 'Silvester Stallone', 'birthday': '1946-07-06',
       'imdb': 'https://www.imdb.com/name/nm0000230/',
       'movies': [
         { 'title': 'Creed II', 'year': 2018 },
         { 'title': 'Creed', 'year': 2015 },
         { 'title': 'Rocky Balboa', 'year': 2007 },
         { 'title': 'Rocky V', 'year': 1990 },
         { 'title': 'Rocky IV', 'year': 1985 },
         { 'title': 'Rocky III', 'year': 1982 },
         { 'title': 'Rocky II', 'year': 1979 },
         { 'title': 'Rocky', 'year': 1976 }
       ]
     }
 ]
```


## 演習1.1 datafiles を使ってデータベース化してみよう
### アドバイス
- データベース化することが目的なので、美しくなくても大丈夫。
- なによりも経験が’大事です。
- データをよく見ると重複したデータがあることがわかりますよね。
- 重複したデータを含むカラムを別テーブルにして、リレーションシップを設定することも一つの方法です。
- まずモデルクラスを作るところからはじめてみましょう。
- 雛形として次のスクリプトを用意しています。適宜修正して完成させてみましょう。

 exercise_01_hint.py
```
 from datafiles import *
 from dataclasses import dataclass
 from datetime import datetime

 """
 Ther's more than one way to do it.
     -- Larry Wall
 """

 data_dir = 'moviedb'
 data_filepattern = data_dir + '/{self.id}.json'

 @dataclass
 class Movie(Model):
     pass

 @datafile(data_filepattern)
 class Actor(Model):
     pass

 if __name__ == '__main__':
     from pathlib import Path
     from movie_data import actors

     data_path = Path(data_dir)
     data_path.mkdir(exist_ok=True)

     for num, actor in enumerate(actors):
         d = dict(id=num)
         try:
             actor = d | actor      # python 3.9
         except:
             actor = dict(d, **actor)
         # この行以降を修正する必要がある
         print(actor)

```
