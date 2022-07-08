from behold import Behold

letters  = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']

for index, letter in enumerate(letters):
    # Behold()の記述は次と同じ
    # print('index: {}, letter: {}'.format(index, letter))
    _ = Behold().show('index', 'letter')
