from aiogram import Router, types, F
from db.base import get_session
from db.models import *
from sqlalchemy import select
router = Router()
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yandex_api import get_image
import os

def get_inventory_keyboard(items: dict) -> types.InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for k,v in items.items():
        kb.add(types.InlineKeyboardButton(text=f'{k} - {"Активно" if v else "Неактивно"}', callback_data=f"change:{k}"))
    if len(items) == 0:
        kb.add(types.InlineKeyboardButton(text="К сожалению у тебя ничего нет", callback_data="menu:menu"))
    kb.adjust(1,1,1,1,1)
    kb.add(types.InlineKeyboardButton(text="Меню", callback_data="menu:menu"))
    kb.adjust(1)
    return kb.as_markup()

@router.callback_query(F.data.startswith("inventory:"))
async def inventory_callback(callback: types.CallbackQuery):
    await callback.answer()
    
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = user.scalars().first()
        avatar = user.current_avatar
        await callback.message.answer(f"Твой инвентарь", reply_markup=get_inventory_keyboard(avatar))
        

@router.callback_query(F.data.startswith("change:"))
async def change_callback(callback: types.CallbackQuery):
    await callback.answer()
    act = callback.data.split(":")[1]
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == callback.from_user.id))
        user = user.scalars().first()
        avatar:dict = dict(user.current_avatar)
        avatar.update({act: not avatar.get(act)})
        if os.path.exists(f"users/{user.id}{str(avatar)}.png"):
            file = types.FSInputFile(f"users/{user.id}{str(avatar)}.png")
        else:
            currect_promt = "Создай аватара - дракона. Он должен быть по центру кадра, белого цвета. Фон одноцветный. Стиль мультипликационный. Милый. Используй только белый цвет, другие цвета не допускаются. Используй ТОЛЬКО белый цвет. Драко должен быть БЕЛОГО цвета. Добавь на него следующие акссеуары:"
            for k,v in avatar.items():
                if v:
                    currect_promt += f" {k},".upper()*5
            await callback.message.answer("Я переодеваюсь!")
            seed = user.seed
            await callback.message.delete()
            image = await get_image(currect_promt, 0.6, currect_promt, seed) 
            file = types.BufferedInputFile(filename=f"users/{user.id}{str(avatar)}.png", file=image)
            with open(f"users/{user.id}{str(avatar)}.png", "wb") as f:
                f.write(image)
            
        photo = await callback.message.answer_photo(photo=file)
        user.avatar = photo.photo[0].file_id
        user.current_avatar = avatar
        await session.commit()
        await callback.message.answer(f"Твой инвентарь", reply_markup=get_inventory_keyboard(avatar))