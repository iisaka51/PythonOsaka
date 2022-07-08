from color import *
import sys

print(Fore.GREEN + 'GREEN set on stdout. ', end='')
print(Fore.RED + 'RED redirected stderr', file=sys.stderr)
print(
('Further stdout should be GREEN, '
 'i.e., the stderr redirection should not affect stdout.'))
