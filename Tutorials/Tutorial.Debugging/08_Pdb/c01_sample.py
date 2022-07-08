def square(n):
    result = n ** 2
    print(result)
    return result

def main():
    for i in range(1,10):
        square(i)

if __name__ == "__main__":
    main()
