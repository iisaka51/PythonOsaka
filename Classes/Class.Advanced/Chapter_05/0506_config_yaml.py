import yaml

with open('config.yml') as conf:
    config = yaml.load(conf, Loader=yaml.SafeLoader)

for k in config.keys():
    print('dbhost => ', config[k]['dbhost'])
    print('  user => ', config[k]['user'])
    print('passwd => ', config[k]['passwd'])
    print('dbname => ', config[k]['dbname'])
