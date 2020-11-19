data = [ 1, 2, 3, 4, 5]

print( all( n > 3 for n in data) )    # 全部が３より大きいとき True
print( any( n > 3 for n in data) )    # 少なくとも１つは３より大きいとき True
