from aiogram import Router, types, F
from db.base import get_session
from db.models import *
from sqlalchemy import select

router = Router()

@router.callback_query(F.data == "leaders:leaders")
async def leaders(callback: types.CallbackQuery):
    await callback.answer()
    async with await get_session() as session:
        users = await session.execute(select(User).order_by(User.experience.desc()))
        users = users.scalars().all()

        await callback.message.answer("Лидеры:\n" + "\n".join([f"{i+1}){users[i].name} - {users[i].experience} опыта" for i in range(min(10, len(users)))]),
                                      reply_markup=types.InlineKeyboardMarkup(
                                          inline_keyboard=[[types.InlineKeyboardButton(text="Назад", callback_data="menu:menu")]]
                                      ))