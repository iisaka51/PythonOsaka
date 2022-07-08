from datafiles import *
from datetime import datetime

data_dir = './datadir'
data_pattern = data_dir + '/timestampdb.yml'

class MyDateTime(converters.Converter, datetime):

     @classmethod
     def to_preserialization_data(cls, python_value, **kwargs):
         # MyDateTimeをシリアライズ可能な値に変換
         return python_value.isoformat()

     @classmethod
     def to_python_value(cls, deserialized_data, **kwargs):
         # ファイルの値をMyDateTimeオブジェクトに戻す
         return MyDateTime.fromisoformat(deserialized_data)


@datafile(data_pattern)
class Timestamp:
     my_datetime: MyDateTime = None

if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)
