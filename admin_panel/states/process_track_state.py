from aiogram.fsm.state import StatesGroup, State

#Rahmatilla Xudoyberiyev
#Process Track
class ProcessTrack(StatesGroup):
	chosen_menu = State()
	todays_list = State()
	full_list = State()
	courses = State()
	regions = State()
	region_chosen = State()
	add_region = State()
	add_region_name = State()
	branches = State() 
	send_news = State()

	#Extra
	regions_list = {
		"Andijon",
		"Buxoro",
		"Farg‘ona",
		"Jizzax",
		"Xorazm",
		"Namangan",
		"Navoiy",
		"Qashqadaryo",
		"Qoraqalpog‘iston Respublikasi",
		"Samarqand",
		"Sirdaryo",
		"Surxondaryo",
		"Toshkent"
	}
	# ... (Keyinchalik qo'shiladi yana)

# This is a state for 'Ortga, Bosh sahifaga and etc.'