from aiogram import types, Router, F
from db import service
from db.models import *
from keyboards.profile_keyboard import get_profile_keyboard
router = Router()

@router.callback_query(F.data.startswith("profile:"))
async def profile_callback(callback: types.CallbackQuery):
    act = callback.data.split(":")[1]
    user:User = await service.get_user(callback.from_user.id)
    await callback.answer()
    match act:
        case "profile":
            await callback.message.answer_photo(photo=user.photo)
            await callback.message.answer(f"{user.name} - {user.experience} опыта\n{user.info}", reply_markup=get_profile_keyboard())