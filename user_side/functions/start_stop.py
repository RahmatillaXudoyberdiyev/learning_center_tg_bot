from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from user_side.keyboards.language_keyboard import language_button

# Botni ishga tushiruvchi funksiya
async def start_command_answer(message: Message):
    await message.answer("Assalomu aleykum,iltimos tilni tanlang:", reply_markup=language_button)

# Botni tozalab bosh sahifaga qaytaradi
async def stop_command_answer(message: Message, state: FSMContext):
    this_state = await state.get_state()
    if this_state == "None":
        await message.answer("Bekor qilish uchun ariza mavjud emas!")
    else:
        await state.clear()
        await message.answer("Joriy ariza bekor qilindi!")





