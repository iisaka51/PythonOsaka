from filedb import *

data_pattern = data_dir + '/jsondb.yml'

@datafile(data_pattern, defaults=True)
class Sample(Base):
    fmt: str = "JavaScript Object Notation"

v1 = Sample(Nested(0), [Nested(1), Nested(2)])

# print(v1)
# !cat datadir/jsondb.yml
