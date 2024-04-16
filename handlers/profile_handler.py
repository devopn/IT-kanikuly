from aiogram import types, Router, F
from db import service
from db.models import *
from keyboards.profile_keyboard import get_profile_keyboard
from keyboards.edit_keyboard import get_edit_keyboard
router = Router()
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from db.base import get_session
from sqlalchemy import select
from yandex_api import geocode

@router.callback_query(F.data.startswith("profile:"))
async def profile_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    act = callback.data.split(":")[1]
    user:User = await service.get_user(callback.from_user.id)
    await callback.answer()
    match act:
        case "profile":
            await callback.message.answer_photo(photo=user.photo)
            await callback.message.answer(f"{user.name} - {user.experience} опыта\n{user.info}", reply_markup=get_profile_keyboard())
        case "edit":
            await callback.message.answer("Что вы хотите изменить?", reply_markup=get_edit_keyboard())
        case "setschool":
            await callback.message.answer("В каком учебном заведении вы учитесь?")
            await state.set_state("setschool")

@router.message(StateFilter("setschool"))
async def setschool(message: types.Message, state: FSMContext):
    try:
        codes = await geocode(message.text)
    except:
        await message.answer("Не удалось найти, укажите более точный адрес", reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="Назад", callback_data="profile:profile")]]
        ))
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == message.from_user.id))
        user.scalars().first().school = codes
        await session.commit()
        await state.clear()
        await message.answer("Учебное заведение добавлено", reply_markup=get_profile_keyboard())


@router.callback_query(F.data.startswith("edit:"))
async def edit_callback(callback: types.CallbackQuery, state: FSMContext):
    act = callback.data.split(":")[1]
    await callback.answer()
    await state.update_data(edit=act)
    await state.set_state("edit")
    await callback.message.answer("Как вы хотите изменить?")

@router.message(StateFilter("edit"))
async def edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == message.from_user.id))
        user = user.scalars().first()
        match data.get("edit"):
            case "name":
                user.name = message.text
            case "info":
                user.info = message.text
            case "photo":
                if message.photo:
                    photo = message.photo[-1].file_id
                    user.photo = photo
                else:
                    await message.answer("Пожалуйста пришлите фотографию")
                    return
        await session.commit()
        await state.clear()
        await message.answer("Изменения внесены", reply_markup=get_profile_keyboard())

