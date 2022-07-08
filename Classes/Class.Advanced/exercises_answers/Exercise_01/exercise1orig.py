import os
while True:
    dirpath = input('Input Directory Path (Q is quit)')
    print('DIRECTORY : ', dirpath )
    files = os.listdir(dirpath)
    for file in files:
        print(file)
