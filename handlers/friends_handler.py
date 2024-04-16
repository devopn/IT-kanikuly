from aiogram import Router, types

from aiogram import Router, types, F
from db.base import get_session
from db.models import *
from sqlalchemy import select
router = Router()
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yandex_api import get_image
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


@router.callback_query(F.data.startswith("friends:"))
async def friends_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введи никнейм друга чтобы посмотреть на его дракончика")
    await state.set_state("friends:search")

@router.message(StateFilter("friends:search"))
async def friends_search(message: types.Message, state: FSMContext):
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.username == message.text).where(User.id != message.from_user.id))
        user = user.scalars().first()
        if user == None:
            await message.answer("Такого друга нет")
        else:
            await message.answer_photo(photo=user.avatar, caption=f"Дракончик {user.name} - {user.experience}xp", reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=([[types.InlineKeyboardButton(text="назад", callback_data="menu:menu")]]
            )))
    