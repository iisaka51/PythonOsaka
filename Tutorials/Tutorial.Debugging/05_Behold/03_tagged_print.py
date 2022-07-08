from behold import Behold

letters  = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']

for index, letter in enumerate(letters):
# Behold の記述は次のコードと同じ
# if letter.upper() == letter and index % 2 == 0:
#   print('index: {}, letter:, {}, even_uppercase'.format(index, letter))
# if letter.upper() != letter and index % 2 != 0:
#   print('index: {}, letter: {} odd_lowercase'.format(index, letter))

    _ = (Behold(tag='even_uppercase')
         .when(letter.upper() == letter and index % 2 == 0)
         .show('index', 'letter'))
    _ = (Behold(tag='odd_lowercase')
         .when(letter.lower() == letter and index % 2 != 0)
         .show('index', 'letter'))

