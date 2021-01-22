import plac

def main(n):
    for i in range(int(n)):
        yield i

result = plac.call(main, ['3'])
print(result)
