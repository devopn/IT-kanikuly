from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_questions_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Мои достижения", callback_data="questions:achievements"))
    kb.add(types.InlineKeyboardButton(text="Мои задания", callback_data="questions:my"))
    kb.add(types.InlineKeyboardButton(text="Меню", callback_data="menu:menu"))
    kb.adjust(2,1)
    return kb.as_markup()