from pipe import lstrip


v1 =  'abc   ' | lstrip
v2 = '.,[abc] ] ' | lstrip('.,[] ')
