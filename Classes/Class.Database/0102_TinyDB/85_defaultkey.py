from tinydb_base.getSet import GetSet

class Settings(GetSet):

    def __init__(self,
                 file: str = 'config.json',
                 table: str = __name__):
        super().__init__(file=file, table=table)
        self.defaultRows({
            'logfile': 'tmp/sample.log'
        })

config = Settings()
# config.get('logfile')

