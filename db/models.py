from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
import sqlalchemy
from sqlalchemy.types import ARRAY, JSON, DateTime
from pydantic import BaseModel, Field
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    name = Column(String)
    register_time = Column(DateTime, default=datetime.now)

    max_combo = Column(Integer, default=0)
    max_count = Column(Integer, default=0)
    # wave = Column(Integer, default=None, nullable=True)
    current_session_id = Column(Integer,default=None, nullable=True)

class UserSchema(BaseModel):
    id: int
    uuid: str
    name: str
    register_time: datetime
    current_session_id: int | None
