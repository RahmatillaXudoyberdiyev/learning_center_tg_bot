from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext
from user_side.keyboards.menu_keyboards import menu_buttons, registration_back_button
from user_side.states.process_track_state import ProcessTrack
from user_side.keyboards.language_keyboards import language_button
from aiogram.utils.keyboard import  ReplyKeyboardBuilder

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
	import mysql.connector # mysql bilan connect qiluvchi funksiya

	connection = mysql.connector.connect(user = 'root', host = 'localhost', password = 'begzod', database='learning_center') # bazaga ulanib oldim.

	try :
		query = connection.cursor()
		query.execute("Select distinct name from course") # sql buyrug'i
		button_list = query.fetchall() # natijalar list ko'rinishida olindi.
		await state.update_data(course_button_position = 1, course_list = button_list, state = 'course') # positsiya yangilandi.

		# Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
		await message.answer(text = "Kurslar ro'yxati :", reply_markup = await create_course_list_buttons(button_list, 1, state))


	except mysql.connector.Error as err: # Biror bir xatolik yuz bersa.
		print(err)
		connection.close() # ulanish uzilmoqda.
	finally:
		connection.close() # ulanish uzilmoqda.



#Begzod Turdibekov
#Info : Kurslar ro'yxati uchun keyboard yaratib beradigan funksiya

async def create_course_list_buttons(button_list, position, state : FSMContext):

	# Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
	buttons = ReplyKeyboardBuilder()

	# Tugamalar joylanib chiqilyapti.
	for value in button_list:
		buttons.button(text = value[0])

	buttons.adjust(2) # Button tugmalarni 2 tadan qilib tartiblash.

	# "Ortga" va "Home" tugmalari
	buttons.row(KeyboardButton(text='Ortga'), KeyboardButton(text = "Home 🏠"))

	return buttons.as_markup(resize_keyboard=True) # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.


#Begzod Turdibekov
# Info: reply buttonda "Home" tugmasi bosilganda ishlaydigan funksiya
async def home_action(message : Message, state : FSMContext):
    await message.answer("Assalomu aleykum, iltimos tilni tanlang:", reply_markup=language_button)
    await state.clear() # Barcha malumotlarni tozalab tashladim.
    await state.set_state(ProcessTrack.current_language) # Til tanlash state i faollashdi.

#Begzod Turdibekov
# Info : Xabarni kurslar ichida bormi yo'qmi tekshiramiz. Agar Kurslarga to'g'ri kelsa Shu kursga mos Filyallarni chiqaramiz.
async def region_show_function(message : Message, state : FSMContext):
	data = await state.update_data() # ma'lumotlarni statedan yuklab olishlik

	import mysql.connector  # mysql bilan connect qiluv funksiya

	connection = mysql.connector.connect(user='root', host='localhost', password='begzod',
										 database='learning_center')  # bazaga ulanib oldim.
	try:
		query = connection.cursor()
		query.execute(f"Select distinct * from branch join course on branch.id = course.branch_id where course.name = '{message.text}'")  # sql buyrug'i
		button_list = query.fetchall()  # natijalar list ko'rinishida olindi.
		await state.update_data(course_button_position=1, course_list=button_list, state = 'region', course_name = message.text)  # kerakli qismlar yoki yangilanadi yoki yangidan saqlanadi.


		# Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
		await message.answer(text=f"<b>{message.text}</b> fani mavjud bo'lgan filyallar ro'yxati :",
							 reply_markup=await create_region_list_buttons(button_list, 1, state),parse_mode = "HTML")

	except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
		print(err)
		connection.close() # ulanishni uzishni ta'minlash
	finally:
		connection.close() # ulanishni uzishni taminlash

# Begzod Turdibekov
# Info : Regionlarni chiqarish uchun funksiya
async def create_region_list_buttons(button_list, position, state : FSMContext):
	# Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
	buttons = ReplyKeyboardBuilder()

	# Tugamalar joylanib chiqilyapti.
	for value in button_list:
		buttons.button(text=value[1])

	# Tugmalarni 2 ustunli qilib tartiblaymiz
	buttons.adjust(2, repeat=True)

	# "Kurslar" va "Home" tugmalari
	buttons.row(KeyboardButton(text='Kurslar'), KeyboardButton(text="Home 🏠"))

	return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.

# Begzod Turdibekov
# Info : Kurs va filyal bo'yicha ma'lumotlarni chiqarish

async def show_course_info(message : Message, state : FSMContext):
	data = await state.update_data() # statedan ma'lumot olinyapti.

	import mysql.connector  # mysql bilan connect qiluv funksiya

	connection = mysql.connector.connect(user='root', host='localhost', password='begzod',
										 database='learning_center')  # bazaga ulanib oldim.
	try:
		query = connection.cursor() # queryni ishlatish uchun sozlash
		query.execute(f"Select course.info from course join branch on branch.id = course.branch_id where course.name = '{data['course_name']}' and branch.name = '{message.text}'")  # sql buyrug'i
		info = query.fetchall()  # natijalar list ko'rinishida olindi.

		await message.answer(str(info[0][0]), reply_markup= registration_back_button)
		await state.update_data(state = None) # state bo'limi natijasi yangilanayapti.

	except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
		print(err)
		connection.close()
	finally:
		connection.close()

# Begzod Turdibekov
# Info : courselardan menu lar bo'limiga o'tish

async def back_from_course(message: Message, state : FSMContext):
	await state.update_data(state=None) # O'zim uchun vaqtinchalikdagi statesni yangilab turibman.
	await message.answer("Iltimos kerakli menuni tanlang:", reply_markup=menu_buttons) # menu button chiqadi.
