def divide(a, b):
    v =  a / b
    return v

def main():
    data = [1, 2, 0, 4]
    for i, d in enumerate(data):
        divide(i, d)

if __name__ == "__main__":
    from context_debug import debug
    with debug():
        main()
