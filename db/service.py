from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from .models import *
from typing import Union
import datetime
from aiogram import types
from db.base import get_session


async def get_user(id:str) -> User:
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        return user

async def create_user(message: types.Message) -> User:
    async with await get_session() as session:
        user = User(id=message.from_user.id, name=message.from_user.full_name)
        session.add(user)
        await session.commit()
        return user

