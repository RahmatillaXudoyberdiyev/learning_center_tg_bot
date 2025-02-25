from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from user_side.keyboards.contact_keyboards import get_contact_keyboard
from user_side.keyboards.language_keyboards import language_button
from user_side.states.process_track_state import ProcessTrack
from user_side.translations.translation_functions import translate_into


# Marjona Sultonova
# Biz haqimizda
async def about_us_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    print(dict(data))
    translations = translate_into("./user_side/translations/contact_translations.json", data, "about_us")

    await message.answer(translations["title"], reply_markup=get_contact_keyboard(data))
    await message.answer(translations["text"], reply_markup=get_contact_keyboard(data))
    await state.set_state(ProcessTrack.about_us)

# Aloqaga chiqish
async def get_contact_info(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer_contact("99 136 28 16", "Marjona", "Sultonova", reply_markup=get_contact_keyboard(data))
    
    

    





