from sqlalchemy.orm import relationship

from . import db
from sqlalchemy import Column, Integer, String, Table, MetaData, Time, ForeignKey, DateTime
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from project.database import engine
from datetime import datetime



class User(UserMixin, db.Model):
     __tablename__ = 'users'

     user_id = Column(Integer, autoincrement=True, primary_key=True)
     first_name = Column(String(150), nullable=False)
     last_name = Column(String(250), nullable=False)
     username = Column(String(250), nullable=False, unique=True)
     email = Column(String(100), nullable=False, unique=True)
     password = Column(String(250), nullable=False)

     events = relationship("Event", back_populates='user', cascade="all, delete-orphan")
     notes = relationship("Note", back_populates='user', cascade="all, delete-orphan")

     def __init__(
             self,
             first_name=None,
             last_name=None,
             username=None,
             email=None,
             password=None
     ):
         self.first_name = first_name.title()
         self.last_name = last_name.title()
         self.username = username
         self.email = email.lower()
         self.password = password


     def get_id(self):
         return self.email


users = Table('users', MetaData(bind=engine),
            Column('user_id', Integer, autoincrement=True, primary_key=True, nullable=False),
            Column('first_name', String),
            Column('last_name', String),
            Column('username', String),
            Column('email', String),
            Column('password', String),
            Column('event_id', Integer))


class Event(db.Model):
    __tablename__ = 'events'

    event_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    start_time = Column(Time(), nullable=False)
    end_time = Column(Time(), nullable=False)
    day = Column(String(50), nullable=False)
    event_description = Column(String(500))
    section = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="events")

    def __init__(
            self,
            name=None,
            start_time=None,
            end_time=None,
            day=None,
            event_description=None,
            section=None,
            user_id=None
    ):
        self.name = name.title()
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        self.event_description = event_description
        self.section = section
        self.user_id = user_id

    events = Table('events', MetaData(bind=engine),
                  Column('event_id', Integer, autoincrement=True, primary_key=True, nullable=False),
                  Column('name', String),
                  Column('start_time', Time),
                  Column('end_time', Time),
                  Column('day', String),
                  Column('event_description', String),
                  Column('section', String),
                  Column('user_id', Integer)
                   )


class Note(db.Model):
    __tablename__ = 'notes'

    note_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    description = Column(String(1000), nullable=False)
    date_time = Column(DateTime(), default=datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    user = relationship("User", back_populates="notes")

    def __init__(self, date_time, user_id, description):
        self.description = description,
        self.date_time = date_time,
        self.user_id = user_id

    notes = Table('notes', MetaData(bind=engine),
                  Column('note_id', Integer, autoincrement=True, primary_key=True, nullable=False),
                  Column('description', String),
                  Column('date_time', DateTime),
                  Column('user_id', Integer)
                  )
