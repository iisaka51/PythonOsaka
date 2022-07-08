
import parsl
from parsl.app.app import bash_app

conf = parsl.load()

@bash_app
def echo(arg, inputs=[],
         stderr=parsl.AUTO_LOGNAME, stdout=parsl.AUTO_LOGNAME):
    cmdline = f'"echo {arg} {inputs[0]} {inputs[1]}"; exit 1'
    return cmdline

app = echo('Hello', inputs=['World', '!'])
app.result()     # タスクが完了するまでブロックされる

with open(app.stdout, 'r') as f:
    msg = f.read()
    print(msg)
