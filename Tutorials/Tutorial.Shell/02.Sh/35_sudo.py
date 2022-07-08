import sh
import sys

if sys.platform == 'linux':
    syslog_file = '/var/log/messages'
elif sys.platform == 'darwin':
    syslog_file = '/var/log/system.log'
elif sys.platform.startswith('win32'):
    syslog_file = 'C:\Windows\System32\winevt\Log\system' # maybe...
else:
    syslog_file = '/tmp'    # unknown platform

with sh.contrib.sudo:
     print(sh.ls(syslog_file))
