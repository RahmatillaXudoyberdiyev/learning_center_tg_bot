from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_panel.keyboards.begin_keyboards import get_keyboard,send_get_keyboard
from admin_panel.states.process_track_state import ProcessTrack

# Botni admin uchun ishga tushiruvchi funksiya
async def admin_start_command(message: Message, state: FSMContext):
    await message.answer("Assalomu aleykum admin botga xush kelibsiz",reply_markup=get_keyboard())
    await state.clear()
    await state.set_state(ProcessTrack.chosen_menu)


async def send_news(message : Message, state : FSMContext):
    await message.answer("Yuborilgan xabar hammaga boradi",reply_markup=send_get_keyboard())
    await state.clear()

