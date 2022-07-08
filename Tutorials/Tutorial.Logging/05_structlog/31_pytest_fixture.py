import pytest
import structlog
from structlog.testing import LogCapture
from some_module2 import some_function
from pprint import pprint

@pytest.fixture(name="log_output")
def fixture_log_output():
    return LogCapture()

@pytest.fixture(autouse=True)
def fixture_configure_structlog(log_output):
    structlog.configure(
        processors=[log_output]
    )

def test_my_stuff(log_output):
    some_function()
    pprint(log_output.entries)
    expect_entry = {'event': 'previous data',
                    'log_level': 'error',
                    'name': 'python'}
    assert log_output.entries == [expect_entry]
