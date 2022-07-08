from m2m_relation_db import *

bob = User(username='bob')
tim = User(username='tim')
jay = User(username='jay')

admin = Role(name='admin')
editor = Role(name='editor')

bob.addRole(admin)
bob.addRole(editor)
tim.addRole(editor)

v1 = bob.roles
v2 = tim.roles
v3 = jay.roles
v4 = admin.users
v5 =  editor.users

# print(v1)
# ...
# print(v5)
