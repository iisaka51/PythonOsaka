from watchpoints import watch
from pprint import pprint

a = 0
watch(a, custom_printer=pprint)
a = 1
