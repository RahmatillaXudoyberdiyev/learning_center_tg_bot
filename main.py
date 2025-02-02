# Asosiy funksiyalar
from aiogram import Bot, Dispatcher, F
from asyncio import run 
from aiogram.types import BotCommand
from aiogram.filters import Command

# Foydalanuvchi qismi funksiyalari
from user_side.functions.start_section import user_start_command
from user_side.functions.entry_section import entry_section_function
from user_side.functions.list_based_section import courses_function, region_show_function, show_course_info
from user_side.functions.contact_section import about_us_handler,get_contact_info
from user_side.functions.registration_section import registation_fullname, registation_phone_number, registration_verification, send_info_to_admins
# Foydalanuvchi qismi statelari
from user_side.states.process_track_state import ProcessTrack

# Foydalanuvchi qismi filterlari
from user_side.filters.checkCourse import check_in_region, check_in_course

# Admin qismi
from admin_panel.functions.start_section import admin_start_command

from config import API_TOKEN # Sizning API tokeningiz
from config import ADMIN_IDS


dp = Dispatcher()



# main dasturni yurgazuvchi funksiya
async def main():

	bot = Bot(token = API_TOKEN)

	# Marjona Sultonova
	# User uchun start va til tanlash buyruqlari
	dp.message.register(user_start_command, Command("start", "lang"), ~F.from_user.id.in_(ADMIN_IDS))

	# Rahmatilla Xudoyberdiyev
	# Admin uchun start buyrug'i
	dp.message.register(admin_start_command, Command("start"), F.from_user.id.in_(ADMIN_IDS))
	
	# Rahmatilla Xudoyberdiyev
	# User uchun kirish qismi (yoxud asosiy qism)
	dp.message.register(entry_section_function, ProcessTrack.current_language)

	#Begzod Turdibekov

    # Kurslar bo'limi
	dp.message.register(courses_function, F.text == 'Kurslar')
	dp.message.register(entry_section_function, F.text == '🏠 Bosh sahifaga qaytish')

    # Ortga tugmalari
	dp.message.register(entry_section_function, ProcessTrack.courses, F.text == 'Ortga')  # Back to menu
	dp.message.register(courses_function, ProcessTrack.region, F.text == 'Ortga')  # Back to courses list
	dp.message.register(region_show_function, ProcessTrack.registration, F.text == 'Ortga')  # Back to region list

    # Kurs tanlash va regionlarni chiqarish
	dp.message.register(region_show_function, check_in_course())
	dp.message.register(show_course_info, check_in_region())
	# dp.message.register(back_from_course, check_in_course_back())

	# Munisa Akbarovna
	dp.message.register(registation_fullname, F.text == "✍️ Ro'yxatdan o'tish")
	dp.message.register(registation_phone_number, ProcessTrack.fullname)
	dp.message.register(send_info_to_admins, F.text == "✅ Tastiqlash")
	dp.message.register(show_course_info, F.text == "🔄 Boshidan boshlash")
	dp.message.register(registration_verification, ProcessTrack.phone_number)
	
	# Marjona Sultonova
	dp.message.register(about_us_handler, F.text == "🗒 Biz haqimizda")
	dp.message.register(get_contact_info, F.text == "📞 Aloqaga chiqish")


	await bot.set_my_commands([
		BotCommand(command="/start", description="Botni ishga tushirish"),
		BotCommand(command="/lang", description="Tilni o'zgartirish")
	])
# __________
	await dp.start_polling(bot, skip_updates = True)

if __name__ == '__main__':
	run(main())

# Logs:
# Rahmatilla Xudoyberdiyev changed
# Stop function is removed by Rahmatilla Xudoyberdiyev