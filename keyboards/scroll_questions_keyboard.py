from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_scroll_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Предыдущее", callback_data="questions:prev"))
    kb.add(types.InlineKeyboardButton(text="Выполнить", callback_data="questions:submit"))
    kb.add(types.InlineKeyboardButton(text="Следующее", callback_data="questions:next"))
    kb.add(types.InlineKeyboardButton(text="Назад", callback_data="questions:questions"))
    kb.adjust(3)
    return kb.as_markup()