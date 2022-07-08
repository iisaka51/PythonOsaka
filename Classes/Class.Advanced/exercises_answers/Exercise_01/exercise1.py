import os

while True:
    try:
        dirpath = input('Input Directory Path (Q is quit): ')
        if dirpath == 'Q':
            break
        print('DIRECTORY : ', dirpath )
        files = os.listdir(dirpath)
        for file in files:
            print(file)
    except KeyboardInterrupt:
        pass
    except FileNotFoundError as msg:
        print(f'{msg}')
