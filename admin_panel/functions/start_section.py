from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Botni admin uchun ishga tushiruvchi funksiya
async def admin_start_command(message: Message, state: FSMContext):
    await message.answer("Assalomu aleykum admin botga xush kelibsiz")
    await state.clear()




