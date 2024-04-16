from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_edit_keyboard() -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(types.InlineKeyboardButton(text="Имя", callback_data="edit:name"))
    kb.add(types.InlineKeyboardButton(text="Информацию о себе", callback_data="edit:info"))
    kb.add(types.InlineKeyboardButton(text="Фото", callback_data="edit:photo"))
    kb.adjust(2)
    return kb.as_markup()