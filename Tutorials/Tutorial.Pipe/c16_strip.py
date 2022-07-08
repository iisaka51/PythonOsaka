from pipe import strip


v1 =  'abc   ' | strip
v2 = '.,[abc] ] ' | strip('.,[] ')
