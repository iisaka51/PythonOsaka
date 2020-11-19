from click.testing import CliRunner
from click_hello import hello

def test_hello():
  runner = CliRunner()
  result = runner.invoke(hello, '--name Peter')
  assert result.exit_code == 0
  assert result.output == 'Hello Peter!\n'

  result = runner.invoke(hello, '--name Jack -C 2')
  assert result.exit_code == 0
  assert result.output == 'Hello Jack!\nHello Jack!\n'
  assert result.stdout == 'Hello Jack!\nHello Jack!\n'

  print(result.exc_info)
  print(result.stdout_bytes)

if __name__ == '__main__':
    test_hello()

