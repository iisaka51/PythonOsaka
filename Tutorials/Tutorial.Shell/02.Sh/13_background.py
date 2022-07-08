import sh

sh.sleep(3)
print("...3 seconds later")

p = sh.sleep(3, _bg=True)
print("print immediately!")
p.wait()
print("...and 3 seconds later")
