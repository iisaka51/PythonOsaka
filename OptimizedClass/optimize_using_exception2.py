list_of_strings = ['1', '2', '3', 'one', 'two', 'three', '4', '10']
list_of_numbers = []
for num in list_of_strings:
    try:
        list_of_numbers.append(int(num))
    except:
        print('String encountered')
