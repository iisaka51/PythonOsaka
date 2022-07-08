from shell import shell

# -u : バッファリングをしないためのオプション

sh = shell('cat -u ', has_input=True)
sh.write('Hello World!')

# sh.output()
