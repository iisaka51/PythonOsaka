import c01_package_a as package_a
import yappi
import sys

def a():
    pass

def b():
    pass

yappi.start()
a()
b()
package_a.a()
yappi.stop()

# モジュール名でフィルタリング：package_a モジュールのものだけ
current_module = sys.modules[__name__]
stats = yappi.get_func_stats(
    filter_callback=lambda x: 'package_a' in x.module
)
stats.print_all()
