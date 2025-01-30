from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from user_side.keyboards.language_keyboard import language_button

# Botni ishga tushiruvchi funksiya
async def start_command_answer(message: Message, state: FSMContext):
    await message.answer("Assalomu aleykum,iltimos tilni tanlang:", reply_markup=language_button)
    await state.clear()
    




