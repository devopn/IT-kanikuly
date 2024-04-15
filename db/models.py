from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
import sqlalchemy
from sqlalchemy.types import ARRAY, JSON, DateTime
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(String)
    info = Column(String)
    avatar = Column(String)
    experience = Column(Integer, default=0)
    registered_at = Column(DateTime, default=datetime.now)
    


class Achievment(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, index=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    type = Column(String)

