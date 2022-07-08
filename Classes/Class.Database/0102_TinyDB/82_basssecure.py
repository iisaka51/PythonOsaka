from tinydb_base.cryptography import DatabaseBaseSercure

class Diary(DatabaseBaseSercure):

    def __init__(self,
        file: str ='diary.json',
        table: str ='diary',
        requiredKeys: str ='title,content',
        salt: str ='salt'):
        super().__init__(file=file,
                         table=table,
                         requiredKeys=requiredKeys,
                         salt=salt)

diary = Diary(salt='this_is_my_salt')
diary.create({'title': '2021-08-08', 'content': "Open Lion's Gate"},
             'myp@ssw0rd')
# diary.readAll('myp@ssw0rd')
