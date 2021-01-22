from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
       return "<User('name={}', fullname={}, nickname={})>".format(
                     self.name, self.fullname, self.nickname)

# Base.metadata.create_all(engine)
