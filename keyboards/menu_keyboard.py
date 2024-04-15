from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_menu_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Профиль", callback_data="profile:profile"))
    kb.add(types.InlineKeyboardButton(text="Задания", callback_data="questions:questions"))
    kb.add(types.InlineKeyboardButton(text="Настройки", callback_data="settings:settings"))
    kb.add(types.InlineKeyboardButton(text="Друзья", callback_data="friends:friends"))
    kb.adjust(2)
    return kb.as_markup()