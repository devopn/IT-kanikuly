from aiogram import Router, types, F
from keyboards.questions_keyboard import get_questions_keyboard
from keyboards.scroll_questions_keyboard import get_scroll_keyboard
router = Router()
from db.base import get_session
from datetime import timedelta
from sqlalchemy import select
from db import service
import face_recognition
from db.models import *
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
@router.callback_query(F.data.startswith("questions:"))
async def questions_callback(callback: types.CallbackQuery, state: FSMContext):
    act = callback.data.split(":")[1]
    await callback.answer()
    match act:
        case "questions":
            async with await get_session() as session:
                achivments = await session.execute(select(Achievement).where(Achievement.owner_id == callback.from_user.id))
                achivments = achivments.scalars().all()
                questions = await session.execute(select(Question))
                questions = questions.scalars().all()
                questions = [question for question in questions if question.id not in [achivment.quest_id for achivment in achivments]]

                await callback.message.answer("Задания:\n"+"\n".join([f">>> {question.name} - {question.xp}xp" for question in questions]), reply_markup=get_questions_keyboard())
        case "achievements":
            async with await get_session() as session:
                achivments = await session.execute(select(Achievement).where(Achievement.owner_id == callback.from_user.id))
                achivments = achivments.scalars().all()
                await callback.message.answer("Достижения:\n" + "\n".join([f"{achivment.name}: {achivment.description}" for achivment in achivments]), reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=([[types.InlineKeyboardButton(text="назад", callback_data="questions:questions")]]
                )))
        case "my":
            async with await get_session() as session:
                achivments = await session.execute(select(Achievement).where(Achievement.owner_id == callback.from_user.id))
                achivments = achivments.scalars().all()
                questions = await session.execute(select(Question))
                questions = questions.scalars().all()
                questions = [question for question in questions if question.id not in [achivment.quest_id for achivment in achivments]]

                await state.update_data(questions=questions)
                await state.update_data(current=0)
                quest = questions[0]
                await callback.message.answer(f"{quest.name} - {quest.xp}xp + {quest.reward}\n{quest.description}", reply_markup=get_scroll_keyboard())


        case "next":
            data = await state.get_data()
            current = data.get("current")
            questions = data.get("questions")
            if current == len(questions) - 1:
                await callback.answer("Это было последнее задание")
            else:
                current += 1
                await state.update_data(current=current)
                quest = questions[current]
                await callback.message.edit_text(f"{quest.name} - {quest.xp}xp + {quest.reward}\n{quest.description}", reply_markup=get_scroll_keyboard())
        case "prev":
            data = await state.get_data()
            current = data.get("current")
            questions = data.get("questions")
            if current == 0:
                await callback.answer("Это первое задание")
            else:
                current -= 1
                await state.update_data(current=current)
                quest = questions[current]
                await callback.message.edit_text(f"{quest.name} - {quest.xp}xp + {quest.reward}\n{quest.description}", reply_markup=get_scroll_keyboard())

        case "submit":
            data = await state.get_data()
            current = data.get("current")
            questions = data.get("questions")
            quest:Question = questions[current]
            if quest.id == 0:
                await callback.message.answer("Отправь свою фото")
                await state.set_state("question_photo")

            elif quest.id == 1:
                await state.set_state("question_location")
                await callback.message.answer("Отправь свою геопозицию", reply_markup=types.ReplyKeyboardMarkup(
                    keyboard=([[types.KeyboardButton(text="Отправить", request_location=True)]]
                ), resize_keyboard=True))
            elif quest.id == 2:
                async with await get_session() as session:
                    user = await session.execute(select(User).where(User.id == callback.from_user.id))
                    if not user.scalars().first().school:
                        await callback.message.answer("Перед выполнением данного задания укажите учебное заведение в профиле", reply_markup=get_questions_keyboard())
                    elif datetime.now() - user.scalars().first().last_school < timedelta(days=1):
                        await callback.message.answer("Приходите на следующий день")
                    else:
                        await state.set_state("question_school")
                        await callback.message.answer("Отправь свою геопозицию", reply_markup=types.ReplyKeyboardMarkup(
                            keyboard=([[types.KeyboardButton(text="Отправить", request_location=True)]]
                        ), resize_keyboard=True))

@router.message(StateFilter("question_school"))
async def question_school(message: types.Message, state: FSMContext):
    await message.answer("Проверка", reply_markup=types.ReplyKeyboardRemove())
    async with await get_session() as session:
        user = await session.execute(select(User).where(User.id == message.from_user.id))
        user = user.scalars().first()
        codes = user.school
        lat = message.location.latitude
        lon = message.location.longitude
        if lat and lon:
            if ( codes["upperCorner"].split()[1]< lat < codes["upperCorner"].split()[1])and(codes["lowerCorner"].split()[0] < lon < codes["upperCorner"].split()[0]):
                await message.answer("Задание выполнено!")
                user.last_school = datetime.now()
                user.experience += 10
                achievement = Achievement()
                achievement.owner_id = message.from_user.id
                achievement.name = "Школьник"
                achievement.description = "Прилежный"
                await session.commit()

@router.message(StateFilter("question_location"))
async def question_photo(message: types.Message, state: FSMContext):
    await message.answer("Проверка", reply_markup=types.ReplyKeyboardRemove())
    lat = message.location.latitude
    lon = message.location.longitude
    if lat and lon:
        
        if 56.005113 < lat < 56.005634 and 36.915643 < lon < 36.916946:
            await message.answer("Задание выполнено! Твой инвентарь обновлен", reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[[types.InlineKeyboardButton(text="Назад", callback_data="questions:questions")]]
            ))
            async with await get_session() as session:
                achievment = Achievement()
                achievment.owner_id = message.from_user.id
                achievment.name = "Посетитель ФОК"
                achievment.description = "Прогулка не помешает, верно?"
                achievment.reward = "Кепка"
                achievment.quest_id = 1
                session.add(achievment)
                user = await session.execute(select(User).where(User.id == message.from_user.id))
                user = user.scalars().first()
                user.experience += 150
                if user.current_avatar != {}:
                    ca = dict(user.current_avatar)
                    ca.update({"Черная кепка": False})
                else:
                    ca = {"Черная кепка": False}
                
                user.current_avatar = ca

                await session.commit()
            

        else:
            await message.answer("Задание не выполнено", reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=([[types.InlineKeyboardButton(text="Назад", callback_data="questions:questions")]]
            )))
    else:
        await message.answer("Пожалуйста, отправьте свою геопозицию")


@router.message(StateFilter("question_photo"))
async def default_command(message: types.Message):
    try:
        user = await service.get_user(message.from_user.id)
        await message.bot.download(file=message.photo[-1].file_id, destination=f"photos/{user.id}pic.png")
        await message.bot.download(file=user.photo, destination=f"photos/{user.id}send.png")
        picture_of_me = face_recognition.load_image_file(f"photos/{user.id}pic.png")
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

        # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

        unknown_picture = face_recognition.load_image_file(f"photos/{user.id}send.png")
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
    except Exception as e:
        print(str(e))
        await message.answer("Я никого не вижу на фото, попробуй отправить еще раз")
    result = results[0]
    if result:
        await message.answer("Задание выполнено!", reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=([[types.InlineKeyboardButton(text="Назад", callback_data="questions:questions")]]
        )
        ))
        async with await get_session() as session:
            achievment = Achievement()
            achievment.owner_id = message.from_user.id
            achievment.name = "Покажи себя"
            achievment.description = "Вы доказали что вы настоящий"
            achievment.quest_id = 0
            achievment.reward = "Цепочка на шее"
            session.add(achievment)
            user = await session.execute(select(User).where(User.id == message.from_user.id))
            user = user.scalars().first()
            user.experience += 50
            print(user.avatar)
            if user.current_avatar != {}:
                ca = dict(user.current_avatar)
                ca.update({"Цепочка на шее": False})
            else:
                ca={"Цепочка на шее": False}
            user.current_avatar = ca

            await session.commit()
            
            
    else:
        await message.answer("Задание не выполнено", reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=([[types.InlineKeyboardButton(text="Назад", callback_data="questions:questions")]]
        )))