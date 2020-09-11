from sqlalchemy import Column, Integer, String, Table, MetaData
from database import Base, engine


class User(Base):
     __tablename__ = 'users'

     user_id = Column(Integer, autoincrement=True, primary_key=True)
     first_name = Column(String(150))
     last_name = Column(String(250))
     username = Column(String(250), unique=True)
     email = Column(String(100), unique=True)
     password = Column(String(50))

     def __init__(self, first_name=None, last_name=None, username=None, email=None, password=None):
         self.first_name = first_name.title()
         self.last_name = last_name.title()
         self.username = username
         self.email = email.lower()
         self.password = password

     def __repr__(self):
        return "<User(first_name='%s', last_name='%s', username=%s, email='%s', password=%s)>" % (
                             self.first_name, self.last_name, self.username, self.email, self.password)


users = Table('users', MetaData(bind=engine),
            Column('user_id', Integer, autoincrement=True, primary_key=True, nullable=False),
            Column('first_name', String),
            Column('last_name', String),
            Column('username', String),
            Column('email', String),
            Column('password', String))
