from shell import Shell

# -u : バッファリングをしないためのオプション

sh = Shell(has_input=True)
sh.run('cat -u')
sh.write('Hello World!')

# sh.output()
