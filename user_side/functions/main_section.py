from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from user_side.keyboards.menu_keyboards import menu_buttons
from user_side.states.process_track_state import ProcessTrack
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Rahmatilla Xudoyberdiyev
# Asosiy qism funksiyasi
async def main_section_function(message: Message, state: FSMContext):
	print(message.text)
	await state.update_data(current_language = message.text)
	await message.answer("Iltimos kerakli menuni tanlang:", reply_markup=menu_buttons)
	await state.set_state(ProcessTrack.chosen_menu)

# Begzod Turdibekov
# Info : Kurslar ro'yxatini ko'rsatish uchun
async def courses_function(message : Message, state : FSMContext):
	import mysql.connector # mysql bilan connect qiluv funksiya

	connection = mysql.connector.connect(user = 'root', host = 'localhost', password = 'begzod', database='learning_center') # bazaga ulanib oldim.

	try :
		query = connection.cursor()
		query.execute("Select distinct name, info, branch_id from course") # sql buyrug'i
		button_list = query.fetchall() # natijalar list ko'rinishida olindi.
		await state.update_data(course_button_position = 1) # positsiya yangilandi.
		await state.update_data(course_list = button_list) # tugmalar qiymati yangilandi.

		# Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
		await message.answer(text = "Kurslar ro'yxati :", reply_markup = await create_course_list_buttons(button_list, 1, state))

	except mysql.connector.Error as err: # Biror bir xatolik yuz bersa.
		print(err)
	


#Begzod Turdibekov
#Info : Kurslar ro'yxati uchun keyboard yaratib beradigan funksiya

async def create_course_list_buttons(button_list, position, state : FSMContext):
	start = (position - 1) * 6 # boshlanish nuqta
	end = start + 6 # tugash nuqta

	if position * 6 > len(button_list): # end qiymati tugma uzunli oshib ketsa uni tugmalar uzunligiga tenglanadi.
		end = len(button_list)
		await state.update_data(course_button_position = len(button_list) // 6) # positsiya yangilanayapti.

	# Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
	buttons = InlineKeyboardBuilder()

	# Tugamalar joylanib chiqilyapti.
	for i in range(start, end):
		buttons.button(text = button_list[i][0], callback_data=button_list[i][0])

	# "Next" va "Prev" tugmalari
	if end != len(button_list):
		buttons.button(text='Next ⏭', callback_data='next')
	if start != 0:
		buttons.button(text='⏮ Prev', callback_data='prev')


	# "Home" tugmasi
	buttons.button(text='Home', callback_data='home')

	# Tugmalarni 2 ustunli qilib tartiblaymiz
	buttons.adjust(2, repeat = True)

	return buttons.as_markup() # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.
