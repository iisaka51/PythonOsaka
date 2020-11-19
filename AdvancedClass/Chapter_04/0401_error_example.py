data = None
while data == None:
    filename = input('Filename: ? ')
    try:
        f = open(filename)
    except IOError:
        print('This error occors in python2.x.')
    except FileNotFoundError as e:
        print(e)
    else:
        data = f.read()
        f.close()

print(data)
