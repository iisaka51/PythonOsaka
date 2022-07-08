import sys
from tinydb_base import DatabaseBase
from tinydb_base.exporter import jsonExport
from tinydb_base.exporter import ymalExport as yamlExport

class MyDB(DatabaseBase):
    def __init__(self,
        file: str ='mydb.json',
        table: str ='tasks',
        requiredKeys: str ='title:str,data:int'):
        super().__init__(file=file,
                         table=table,
                         requiredKeys=requiredKeys)

db = MyDB()
for index in range(0, 10):
    db.create({'title': f'data_{index}', 'data': index})

v1 = jsonExport(db.readAll(), 'jsonData.json')
v2 = yamlExport(db.readAll(), 'yamlData.yaml')

# print(v1)
# print(v2)
# !cat jsonData.json
# !cat yamlData.json
