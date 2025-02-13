
from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext

from user_side.keyboards.entry_keyboards import menu_buttons
from user_side.states.process_track_state import ProcessTrack

# Rahmatilla Xudoyberdiyev
# Kirish qismi funksiyasi
async def entry_section_function(message: Message, state: FSMContext):
	print(message.text)
	await state.clear()
	await state.update_data(current_language = message.text)
	await message.answer("Iltimos kerakli menuni tanlang:", reply_markup=menu_buttons)
	await state.set_state(ProcessTrack.chosen_menu)


