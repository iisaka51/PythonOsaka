from fabric2 import Connection, task

@task(name='remote')
def remote_exectutor(c, cmd):
    c.run(cmd)
