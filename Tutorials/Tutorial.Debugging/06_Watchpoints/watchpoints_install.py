def square(n):
    result = n ** 2
    print(result)
    return result

def main():
    for i in range(1,10):
        watch(i)
        square(i)

if __name__ == "__main__":
    from watchpoints import watch
    watch.install()
    main()
