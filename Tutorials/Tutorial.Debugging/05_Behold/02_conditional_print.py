from behold import Behold

letters  = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']

for index, letter in enumerate(letters):
    # Behold()の記述は次と同じ
    # if letter.upper() == letter and index % 2 == 0:
    #     print('index: {}'.format(index))
    _ = (Behold()
         .when(letter.upper() == letter and index % 2 == 0)
         .show('index'))
