from zodb_mydata import *
from zodb_members import Member
import transaction

members = []

for name in ['Freddie', 'Brian', 'John', 'Roger']:
   member = Member()
   member.setName(name)
   members.append(member)

root.members=members
transaction.commit()

vocal = root.members[0]
vocal.setName('Adam')
transaction.commit()
connection.close()
