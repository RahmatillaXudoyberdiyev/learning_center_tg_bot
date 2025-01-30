from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from user_side.keyboards.menu_keyboards import menu_buttons
from user_side.states.process_track_state import ProcessTrack

# Rahmatilla Xudoyberdiyev
# Asosiy qism funksiyasi
async def main_section_function(message: Message, state: FSMContext):
	print(message.text)
	await state.update_data(current_language = message.text)
	await message.answer("Iltimos kerakli menuni tanlang:", reply_markup=menu_buttons)
	await state.set_state(ProcessTrack.chosen_menu)