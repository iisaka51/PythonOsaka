from tinydb_base.getSetSercure import GetSetSercure as GetSetSecure

class Settings(GetSetSecure):

    def __init__(self,
                 file: str = 'config_secure.json',
                 table: str = __name__,
                 salt: str = 'this_is_my_salt',
                 pw: str = 'I_love_IPA'):
        super().__init__(file=file, table=table, salt=salt, pw=pw)

config = Settings()
config.set('password', 'myp@ssw0rd')
# config.get('password')

