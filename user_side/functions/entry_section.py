from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext

from user_side.keyboards.entry_keyboards import get_entry_keyboard
from user_side.states.process_track_state import ProcessTrack

from user_side.translations.translation_functions import translate_into

# Rahmatilla Xudoyberdiyev
# Kirish qismi funksiyasi
async def entry_section_function(message: Message, state: FSMContext):
	data1 = await state.get_data()
	await state.clear()
	if curr_language:=data1.get("current_language"): 
		if curr_language in ['russian', 'english', 'uzbek']:
			language = curr_language
	else:
		if message.text == '🇷🇺 Ru': language = 'russian'
		elif message.text == '🇺🇸 Eng': language = 'english'
		elif message.text == '🇺🇿 Uz': language = 'uzbek' 
		else: language = 'uzbek'

	await state.update_data(current_language = language)
	data2 = await state.get_data()
	await message.answer(translate_into("./user_side/translations/entry_translations.json", data2, "entry_labels"), reply_markup=get_entry_keyboard(data2))
	await state.set_state(ProcessTrack.chosen_menu)



