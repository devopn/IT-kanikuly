from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from .models import *
from typing import Union
import datetime


# async def get_questions(session: AsyncSession, count: int, mode: int, type: Union[int, None]) -> list[Question]:
#     if mode == 0: # single
#         result = await session.execute(select(Question).where(Question.type == type).order_by(func.random()).limit(count))
#         return result.scalars().all()

#     else: # mixed
#         result = await session.execute(select(Question).order_by(func.random()).limit(count))
#         return result.scalars().all()


# async def get_user(db_session: AsyncSession, uuid:str) -> User:
#     user = await db_session.execute(select(User).where(User.uuid == uuid))
#     user = user.scalars().first()
#     if user is None:
#         raise AuthException("User not found")
#     return user
