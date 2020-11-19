msg='Bonjour Python'
def greeting(name):
     msg = ''
     def say_hello():
         msg += f'Hello {name} '
         print(msg)
     return say_hello

action = greeting('Python')
action()
action()
print(msg)
