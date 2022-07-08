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

# モジュールでフィルタリング：外部モジュールは除外
current_module = sys.modules[__name__]
stats = yappi.get_func_stats(
    filter_callback=lambda x: yappi.module_matches(x, [current_module])
)  # x is a yappi.YFuncStat object
stats.sort("name", "desc").print_all()
