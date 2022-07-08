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

# 関数名でフィルタリング： 関数名が a() のものだけ
current_module = sys.modules[__name__]
stats = yappi.get_func_stats(
    filter_callback=lambda x: 'a' in x.name
)
stats.print_all()
