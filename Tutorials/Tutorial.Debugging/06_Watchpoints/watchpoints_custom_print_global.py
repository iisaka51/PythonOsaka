from watchpoints import watch
from pprint import pprint

watch.config(custom_printer=print)

a = 0
watch(a)
a = 1
