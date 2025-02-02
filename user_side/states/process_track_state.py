from aiogram.fsm.state import StatesGroup, State

#Rahmatilla Xudoyberiyev
#Process Track
class ProcessTrack(StatesGroup):
	current_language = State()
	chosen_menu = State()
	about_us = State()
	contact_us = State()
	courses = State()
	region = State()
	branch = State()	
	registration = State()
	fullname = State()
	phone_number = State()
	verification = State()
	# ... (Keyinchalik qo'shiladi)

# This is a state for 'Ortga, Bosh sahifaga and etc.'