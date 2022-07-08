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

# 関数でフィルタリング：関数 a(), b() だけ
current_module = sys.modules[__name__]
stats = yappi.get_func_stats(
    filter_callback=lambda x: yappi.func_matches(x, [a, b])
)
stats.print_all()
