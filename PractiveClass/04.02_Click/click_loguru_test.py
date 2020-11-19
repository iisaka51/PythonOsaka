import os
from pathlib import Path

from click.testing import CliRunner
from click_loguru_demo1 import cli

def test_help():
    """Test help command."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    print(result.output)
    assert result.exit_code == 0

def test_version():
    """Test show_context command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    print(result.output)
    assert result.exit_code == 0

def test_show_context():
    """Test show_context command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["show-context"])
    print(result.output)
    assert result.exit_code == 0

def test_logging(tmp_path):
    """Test logging to a data file."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["test-logging"])
    assert result.exit_code == 0
    assert len(list(Path("tests/data/logs").glob("*"))) == 1

def test_quiet(tmp_path):
    """Test query of global quiet option."""
    runner = CliRunner()
    os.chdir(tmp_path)
    result = runner.invoke(cli, ["quiet-value"])
    assert result.exit_code == 0
    assert not bool(int(result.output))
    result = runner.invoke(cli, ["-q", "quiet-value"])
    assert result.exit_code == 0
    assert bool(int(result.output))

def test_retention(tmp_path):
    """Test keeping copies of the log file."""
    runner = CliRunner()
    os.chdir(tmp_path)
    log_count = 0
    while log_count < 10:
        result = runner.invoke(cli, ["test-logging"])
        assert result.exit_code == 0
        log_count += 1
    assert len(list(Path("tests/data/logs").glob("*"))) == 4

if __name__ == '__main__':
    test_help()
    test_version()
    test_show_context()
    test_logging('/tmp')
    test_quiet('/tmp')
    test_retention('/tmp')
