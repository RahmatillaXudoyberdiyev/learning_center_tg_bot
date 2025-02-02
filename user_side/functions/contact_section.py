from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from user_side.keyboards.contact_keyboards import contact_button
from user_side.keyboards.language_keyboards import language_button
from user_side.states.process_track_state import ProcessTrack


# Marjona Sultonova
# Biz haqimizda
async def about_us_handler(message: Message, state: FSMContext):
    await message.answer("Biz haqimizda", reply_markup=contact_button)
    await state.set_state(ProcessTrack.about_us)

# Aloqaga chiqish
async def get_contact_info(message: Message, state: FSMContext):
    await message.answer_contact("99 136 28 16", "Marjona", "Sultonova", reply_markup=contact_button)
    

    

    





