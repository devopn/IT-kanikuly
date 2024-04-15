from aiogram import types, Router, F
from db.base import get_session
from aiogram.filters import StateFilter
from db.models import *

# States
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from io import BytesIO
from yandex_api import get_image

router = Router()
from keyboards.menu_keyboard import get_menu_keyboard
@router.callback_query(F.data == "registration")
async def registration(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state("name")
    await callback.answer()
    await callback.message.answer(text="Как я могу тебя называть?", reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=callback.from_user.first_name)]], resize_keyboard=True
    ))


@router.message(StateFilter("name"))
async def reg_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state("info")
    await message.answer(f"Приятно познакомиться {message.text}. Расскажи немного о себе, это позволит мне познакомиться с тобой.", reply_markup=types.ReplyKeyboardRemove())

@router.message(StateFilter("info"))
async def reg_info(message: types.Message, state: FSMContext):
    await state.set_state("photo")
    await state.update_data(info=message.text)
    await message.answer("Спасибо что рассказал! А теперь скинь свою фотографию. В будущем она поможет мне проверять твои работы.",
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отправить фото из профиля")]], resize_keyboard=True))


def wrap_media(bytesio, **kwargs):
    """Wraps plain BytesIO objects into InputMediaPhoto"""
    # First, rewind internal file pointer to the beginning so the contents
    #  can be read by InputFile class
    BytesIO.seek(0)

    return types.InputMediaPhoto(types.InputFile(bytesio), **kwargs)

@router.message(StateFilter("photo"))
async def reg_photo(message: types.Message, state: FSMContext):
    if message.text == "Отправить фото из профиля":
        photos = await message.from_user.get_profile_photos().bot.get_user_profile_photos(message.from_user.id)
        if len(photos.photos) == 0:
            await message.answer("Вы ещё не загрузили свою фотографию")
            return
        photo = photos.photos[0][0].file_id
    else:
        if message.photo == None:
            await message.answer("Пожалуйста пришлите фотографию")
            return
        photo = message.photo[-1].file_id

    async with await get_session() as session:
        data = await state.get_data()
        user = User(id=message.from_user.id, name=data.get("name"), info=data.get("info"), photo=photo)
        await message.answer("Спасибо за регистрацию! Начал создавать тебе персонального аватара", reply_markup=types.ReplyKeyboardRemove())
        image = await get_image(user.info, 0.6, "Создай аватара - дракона. Он должен быть по центру кадра, белого цвета. Фон одноцветный. Стиль мультипликационный. Милый. ") 
        # photo = await message.from_user.get_profile_photos().bot.send_photo(message.from_user.id, image)
        with open(f"photos/{user.id}.png", "wb") as file:
            file.write(image)
        await message.answer_photo(photo=types.FSInputFile(path="photos/{user.id}.png"), caption=f"Привет я Edo.", reply_markup=get_menu_keyboard())
        session.add(user)
        await session.commit()
        await state.clear()
        