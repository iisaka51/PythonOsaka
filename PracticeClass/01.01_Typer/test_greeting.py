from typer.testing import CliRunner
from greeting2 import app

runner = CliRunner()

def test_app():
  result = runner.invoke(app, ['--name', 'Peter'])
  assert result.exit_code == 0
  assert result.output == 'Hello Peter\n'

  result = runner.invoke(app, ['--name', 'Jack', '-C', '2'])
  assert result.exit_code == 0
  assert result.output == 'Hello Jack\nHello Jack\n'


if __name__ == '__main__':
    test_app()
