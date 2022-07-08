from blitzdb import Document, FileBackend
from datetime import datetime

data_dir = './hookdemo'
backend = FileBackend( data_dir )

class BaseDocument(Document):

    def before_save(self):
        self.foo = "before save"

    def before_delete(self):
        self.foo = "before delete"

    def after_load(self):
        self.bar = "after load"

    def before_update(self,set_fields,unset_fields):
        set_fields['updated_at'] = datetime.now()

class MyDoc(BaseDocument):
    pass


if __name__ == '__main__':
    import subprocess

    subprocess.call(['rm', '-rf', data_dir])
