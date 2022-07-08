import crypt
import getpass as gw

# To generate hashed password,
# you should type bellows on REPL of python/IPython.
# import crypt;  print(crypt.crypt('YOUR_PASSWORD', 'SALT')

salt='administrator'
hashed_password='adk6oNRwypFwA'

if hashed_password == crypt.crypt(gw.getpass(), salt):
    print('Wellcome')
else:
    print('Worng password.')
