ACTIONS = dict()

def register(func):
    ACTIONS[func.__name__] = func
    return func

@register
def greeting_english(name):
    return f"Hello {name}"

@register
def greeting_french(name):
    return f"Bonjour {name}"

def greeting(name):
    greeter, greeter_func = list(ACTIONS.items())[len(name)%2]
    return greeter_func(name)

print(greeting('Python'))
print(greeting('Freddie'))
print(greeting('David'))
