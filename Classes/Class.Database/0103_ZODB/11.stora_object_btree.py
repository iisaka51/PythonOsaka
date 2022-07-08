from zodb_mydata import *
from BTrees.OOBTree import BTree
from user_data import *

root.users = BTree()
root.users['devops'] = user_data
