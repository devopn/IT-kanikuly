from aiogram import Router, types, F
from db import service
router = Router()
from keyboards.menu_keyboard import get_menu_keyboard
from random import choice
PHRASES = ["Чем позанимаемся сегодня?", "Ты молодец!", "Сколько заданий выполнишь на этот раз?", "Я в восторге!"]
@router.callback_query(F.data == "menu:menu")
async def menu_callback(callback: types.CallbackQuery):
    user = await service.get_user(callback.from_user.id)
    await callback.answer()
    await callback.message.answer_photo(photo=user.avatar)
    await callback.message.answer(choice(PHRASES), reply_markup=get_menu_keyboard())

