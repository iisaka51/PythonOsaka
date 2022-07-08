from datafiles import *

data_dir = './datadir'
data_pattern = data_dir + '/sampledb.yml'

class RoundedFloat(converters.Float):

    @classmethod
    def to_preserialization_data(cls, python_value, **kwargs):
        number = super().to_preserialization_data(python_value, **kwargs)
        return round(number, 2)

@datafile(data_pattern)
class Result:
    total: RoundedFloat = 0.0

if __name__ == '__main__':
    from pathlib import Path

    dir = Path(data_dir)
    dir.mkdir(exist_ok=True)
