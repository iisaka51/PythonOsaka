from collections import namedtuple

UserMixin = namedtuple("UserMixin", "id name email")
class  User(UserMixin):
    def get_profile(self):
        profile = f"{self.name} <{self.email}"
        return  profile

user = User(1, "Freddie", "freddie@example.com")

# user
# user.get_profile

