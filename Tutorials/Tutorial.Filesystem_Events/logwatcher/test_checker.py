"""Unit tests for checker interfaces."""

# standard libs
import os, sys

# external libs
import pytest

# internal libs
from checker_001 import FileChecker

# ensure temporary directory exists
TMPDIR = '/tmp/logwatcher/checker'
os.makedirs(TMPDIR, exist_ok=True)


# dummy data for testing
data = """\
Python Osaka.
Thanks God It's a Friday.
This is Error message.
Fatal: something wrong.
Should we go to drink beers
"""

ok_output1="""\
 File: dummy, Found in line 3: This is Error message.
 File: dummy, Found in line 4: Fatal: something wrong."""

ok_output2="""\
 File: dummy, Found in line 3: This is Error message."""

class Test_checker(object):
    """Unit test for checker """
    filepath = 'dummy'

    def test_init(self):
        """ Construct dummy data """
        with open(self.filepath, 'w') as fp:
            fp.write(data)

    def reset_offset(self):
        os.unlink(f'{self.filepath}.offset')

    def cleanup(self):
        os.unlink(f'{self.filepath}.offset')
        os.unlink(f'{self.filepath}')

    def test_pattern_list(self):
        checker = FileChecker(['ERROR', 'FATAL'])
        self.reset_offset()
        output = list()
        for msg in checker.check_pattern(self.filepath):
            output.append(msg)
        assert output == ok_output1.split('\n')

    def test_pattern_str(self):
        checker = FileChecker('ERROR')
        self.reset_offset()
        output = list()
        for msg in checker.check_pattern(self.filepath):
            output.append(msg)
            print(msg)
        assert output == ok_output2.split('\n')
