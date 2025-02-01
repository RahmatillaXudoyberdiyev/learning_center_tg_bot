from aiogram.fsm.state import StatesGroup, State

#Rahmatilla Xudoyberiyev
#Process Track
class ProcessTrack(StatesGroup):
	chosen_menu = State()
	todays_list = State()
	full_list = State()
	courses = State()
	regions = State()
	branches = State() 
	send_news = State()

	# ... (Keyinchalik qo'shiladi yana)

# This is a state for 'Ortga, Bosh sahifaga and etc.'