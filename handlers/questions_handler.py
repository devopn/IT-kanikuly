from aiogram import Router, types, F
from keyboards.questions_keyboard import get_questions_keyboard
router = Router()


@router.callback_query(F.data.startswith("questions:"))
async def questions_callback(callback: types.CallbackQuery):
    act = callback.data.split(":")[1]
    match act:
        case "questions":
            await callback.message.edit_text("Задания", reply_markup=get_questions_keyboard())
        case "my":
            pass
        case "daily":
            pass    