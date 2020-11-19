x = [True, True, False]
print(any(x))                 # 少なくとも１つはTrue
print(all(x))                 # ひとつもFalseではない
print(any(x) and not all(x))  # 少なくとも１つはTrue、かつ、少なくとも１つはFalse
