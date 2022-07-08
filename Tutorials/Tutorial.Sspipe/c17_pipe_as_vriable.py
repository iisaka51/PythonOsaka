_f1 = lambda x: x.strip().upper()
_f2 = lambda x: x.replace(' ','_')
_f3 = lambda x: _f2(_f1(x))
X = " ab cde "
X = _f3(X)
print(X)


from sspipe import p, px

to_upper = px.strip().upper()
to_underscore = px.replace(' ', '_')
normalize = to_upper | to_underscore
" ab cde " | normalize | p(print)
