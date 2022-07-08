from models import User

if __name__ == '__main__':
    user = User(first_name='David', last_name='Coverdale')
    print(user)
    print(user.__format__('this'))
    user_bytes = user.__bytes__()
    print(user_bytes)
    user_repr = repr(user)
    print(user_repr)
    user2 = eval(user_repr)
    assert user == user2
    user.debug()
    print(user.debug.__module__)
