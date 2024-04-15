from aiogram import types, Router
from aiogram.filters import Command
router = Router()
from keyboards.menu_keyboard import get_menu_keyboard
from db import service
@router.message(Command("start"))
async def start_command(message: types.Message):
    user = await service.get_user(message.from_user.id)
    if user is None:
        await message.answer("Привет, я Edo, давай учиться вместе?", reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Давай!", callback_data="registration")]
            ]
        ))
    else:
        await message.answer("Menu", reply_markup=get_menu_keyboard())