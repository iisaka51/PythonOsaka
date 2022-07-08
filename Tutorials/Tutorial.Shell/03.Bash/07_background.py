from bash import bash

bash('sleep 3')
print("...3 seconds later")

p = bash('sleep 3', sync=False)
print("print immediately!")
p.sync()
print("...and 3 seconds later")
