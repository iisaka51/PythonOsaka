def info(**data):
    print("\nData type of argument:",type(data))
    for key, value in data.items():
        print(f'{key} is {value}')

info(Firstname="Freddie", Lastname="Mercury", Age=45, Phone=1234567890)
info(Firstname="Brian", Lastname="May",
      Midlename="Harold", Country="England", Age=75, Phone=9876543210)
