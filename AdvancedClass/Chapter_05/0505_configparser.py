import configparser as config
parser = config.ConfigParser()
parser.read('config.ini')

for section_name in parser.sections():
    print('SECTION: ', section_name)
    for item in parser.items(section_name):
        print('{key} => {val}'.format(key=item[0],val=item[1]))
