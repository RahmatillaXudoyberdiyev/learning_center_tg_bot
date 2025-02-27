from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from user_side.keyboards.language_keyboards import language_button
from user_side.states.process_track_state import ProcessTrack

# Botni ishga tushiruvchi funksiya
async def user_start_command(message: Message, state: FSMContext):
    """Botni ishga tushiradi va foydalanuvchidan til tanlashni so'raydi.

    Foydalanuvchiga salomlashish xabarini yuboradi, til tanlash klaviaturasini ko'rsatadi,
    FSM holatini tozalaydi va 'current_language' holatiga o'rnatadi.
    """
    await message.answer("Assalomu aleykum, iltimos tilni tanlang:", reply_markup=language_button)
    await state.clear()
    await state.set_state(ProcessTrack.current_language)




