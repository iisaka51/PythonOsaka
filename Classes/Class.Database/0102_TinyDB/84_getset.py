from tinydb_base.getSet import GetSet

class Settings(GetSet):

    def __init__(self,
                 file: str = 'config.json',
                 table: str = __name__):
        super().__init__(file=file, table=table)

config = Settings()
config.set('logfile', '/tmp/sample.log')
# config.get('logfile')

