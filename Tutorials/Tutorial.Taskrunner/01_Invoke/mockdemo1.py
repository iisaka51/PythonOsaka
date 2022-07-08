import sys
from spec import trap
from invoke import MockContext, Result
from mytasks import show_platform

@trap
def test_show_platform_on_mac():
    c = MockContext(run=Result("Darwin\n"))
    show_platform(c)
    assert "Apple" in sys.stdout.getvalue()

@trap
def test_show_platform_on_linux():
    c = MockContext(run=Result("Linux\n"))
    show_platform(c)
    assert "desktop" in sys
