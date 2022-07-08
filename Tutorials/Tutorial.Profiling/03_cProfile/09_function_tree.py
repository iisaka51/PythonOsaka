import pstats
from pstats import SortKey

p = pstats.Stats('re_test.log')
t1 = p.print_callers(.5, 'init').print_stats(10)
