def greeting_english(name):
    print(f'Hello {name}!')

def greeting_french(name):
    print(f'Bonjour {name}!')

def handler(func, *args):
    return func(*args)

handler(greeting_english, 'Python')
handler(greeting_french, 'Python')
