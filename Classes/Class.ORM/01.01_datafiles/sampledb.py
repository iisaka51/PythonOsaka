from datafiles import *

@datafile("sampledb/{self.key}.yml")
class Sample:

    key: int
    name: str
    value: float = 0.0


def populate_database():
    d = Sample(1, "Beer")
    d = Sample(2, "Sake")
    d = Sample(3, "Wine")

if __name__ == '__main__':
    populate_database()
