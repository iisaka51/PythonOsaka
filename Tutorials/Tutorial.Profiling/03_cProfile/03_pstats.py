import pstats
from pstats import SortKey

p = pstats.Stats('re_test.log')
t = p.strip_dirs().sort_stats(-1).print_stats()
