from datafiles import *
from datetime import datetime

data_dir = './datadir'
data_pattern = data_dir + '/isotimedb.yml'

class DateTimeConverter(converters.Converter):

    @classmethod
    def to_preserialization_data(cls, python_value, **kwargs):
        # datetimeオブジェクト をシリアライズ可能な値に変換
        return python_value.isoformat()

    @classmethod
    def to_python_value(cls, deserialized_data, **kwargs):
        # ファイルの値をdatetimeオブジェクトに戻す
        return datetime.fromisoformat(deserialized_data)

converters.register(datetime, DateTimeConverter)


@datafile(data_pattern)
class Timestamp:
    my_datetime: datetime = None

if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)
