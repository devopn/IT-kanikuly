from aiogram import types, Router, F
from db import service
from db.models import *
from keyboards.profile_keyboard import get_profile_keyboard
router = Router()

@router.callback_query(F.data.startswith("profile:"))
async def profile_callback(callback: types.CallbackQuery):
    act = callback.data.split(":")[1]
    user:User = await service.get_user(callback.from_user.id)
    match act:
        case "profile":
            await callback.message.answer_photo(caption=f"{user.name} - {user.experience} опыта\n{user.info}", photo=user.avatar, reply_markup=get_profile_keyboard())
        