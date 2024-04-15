from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_profile_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Изменить информацию", callback_data="profile:edit"))
    kb.add(types.InlineKeyboardButton(text="Меню", callback_data="menu:menu"))
    kb.adjust(2)
    return kb.as_markup()