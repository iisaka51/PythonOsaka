import pshell as sh

sh.mkdir('/tmp/work/foo')
with sh.pushd('/tmp/work'):
    sh.call('touch foo/hello.txt')
    print('--- 1st copy ')
    sh.copy('foo', 'bar')
    sh.call('find . ')
    print('--- 2nd copy ')
    sh.copy('foo', 'bar')
    sh.call('find . ')

sh.remove('/tmp/work', recursive=True)
