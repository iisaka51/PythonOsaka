from freezegun import freeze_time
import datetime

@freeze_time("2022-02-02 22:22:22")
def test():
    assert ( datetime.datetime.now()
             == datetime.datetime(2022, 2, 22, 22, 22, 22) )

# test()
#
# Offcouse, You can use pytest this demo.
# just type `pytest`.
