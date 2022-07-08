from pipe import rstrip


v1 =  'abc   ' | rstrip
v2 = '.,[abc] ] ' | rstrip('.,[] ')
