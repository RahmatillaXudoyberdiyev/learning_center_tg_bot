import subprocess
try:
    from deep_translator import GoogleTranslator
except ImportError:
    subprocess.run(['pip', 'install', 'deep-translator'])
    from deep_translator import GoogleTranslator
from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext

from user_side.keyboards.entry_keyboards import menu_buttons
from user_side.states.process_track_state import ProcessTrack

# Rahmatilla Xudoyberdiyev
# Kirish qismi funksiyasi
async def entry_section_function(message: Message, state: FSMContext):
	await state.clear()
	if message.text == '🇷🇺 Ru': language = 'russian'
	elif message.text == '🇺🇸 Eng': language = 'english'
	else: language = 'uzbek'

	await state.update_data(current_language = language)
	translated_text = GoogleTranslator(source='auto', target=language).translate("Please select the required menu:")
    
	await message.answer(translated_text, reply_markup=menu_buttons)
	await state.set_state(ProcessTrack.chosen_menu)


