from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
import sqlalchemy
from sqlalchemy.types import ARRAY, JSON, DateTime
from datetime import datetime
from .base import Base
import names

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)
    edo = Column(String, default=names.get_first_name)
    photo = Column(String)
    info = Column(String)
    avatar = Column(String)
    experience = Column(Integer, default=0)
    registered_at = Column(DateTime, default=datetime.now)
    seed = Column(Integer)
    school:dict = Column(JSON, default=None)
    last_school = Column(DateTime, default=datetime.now)
    current_avatar = Column(JSON, default={}) # [{name:..., status:...}]

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, index=True)
    name = Column(String)
    description = Column(String)
    reward = Column(String)
    quest_id = Column(Integer)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    reward = Column(String)
    xp = Column(Integer)
