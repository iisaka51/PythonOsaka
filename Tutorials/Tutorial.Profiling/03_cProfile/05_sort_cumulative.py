import pstats
from pstats import SortKey

p = pstats.Stats('re_test.log')
t1 = p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
