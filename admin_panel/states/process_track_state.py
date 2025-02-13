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
	ask_remove_region = State()
	remove_region = State()
	branches = State()
	ask_remove_branch = State()
	get_branch_name = State()
	ask_add_branch_name = State()
	send_news = State()
	get_course_name = State()          
	ask_add_course_confirm = State()     
	ask_remove_course = State()   
	get_course_info = State()
	get_branch_info = State()
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