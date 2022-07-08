from time import sleep
from tinydb_base.getSet import GetSet, futureTimeStamp
from tinydb_base.exceptions import RowNotFound_Exception

class Settings(GetSet):

    def __init__(self,
                 file: str = 'config.json',
                 table: str = __name__):
        super().__init__(file=file, table=table)

config = Settings()
v1 = config.set('api-key', 'this_is_APIKEY', futureTimeStamp(second=10))
v2 = config.get('api-key')
sleep(20)
try:
    v3 = config.get('api-key')
except RowNotFound_Exception:
    v3 = None

# print(v1)
# print(v2)
# print(v3)
