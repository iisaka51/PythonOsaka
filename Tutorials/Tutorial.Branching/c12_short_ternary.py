def func1(real_name, nickname=None):
    if nickname:
        name = nickname
    else:
        name = real_name
    return(name)

def func2(real_name, nickname=None):
    name = nickname if nickname else real_name
    return(name)

def func3(real_name, nickname=None):
    name = nickname or real_name
    return(name)


v1 = ( func1('Freddie Bulsara'),
       func1('Freddie Bulsara', 'Freddie Mercury'))
v2 = ( func2('Freddie Bulsara'),
       func2('Freddie Bulsara', 'Freddie Mercury'))
v3 = ( func3('Freddie Bulsara'),
       func3('Freddie Bulsara', 'Freddie Mercury'))

assert v1 == v2 and v1 == v3
