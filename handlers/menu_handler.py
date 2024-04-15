from aiogram import Router, types, F

router = Router()
from keyboards.menu_keyboard import get_menu_keyboard

@router.callback_query(F.data == "menu:menu")
async def menu_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Menu", reply_markup=get_menu_keyboard())

