import pshell as sh

sh.mkdir('/tmp/work')
sh.symlink('/tmp/work/foo', '/tmp/work/bar')
sh.call('ls -l /tmp/work')
sh.remove('/tmp/work', recursive=True)

sh.mkdir('/tmp/work')
sh.symlink('/tmp/work/foo', '/tmp/work/bar', abspath=True)
sh.call('ls -l /tmp/work')
sh.remove('/tmp/work', recursive=True)
