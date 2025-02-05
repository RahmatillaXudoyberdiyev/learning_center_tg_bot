# Asosiy funksiyalar
from aiogram import Bot, Dispatcher, F
from asyncio import run 
from aiogram.types import BotCommand
from aiogram.filters import Command

# Foydalanuvchi qismi funksiyalari
from user_side.functions.start_section import user_start_command
from user_side.functions.entry_section import entry_section_function
from user_side.functions.list_based_section import show_course_function, show_region_function, show_branch_function, \
	show_info, go_back_function
from user_side.functions.contact_section import about_us_handler,get_contact_info
from user_side.functions.registration_section import registation_fullname, registation_phone_number, registration_verification, send_info_to_admins
# Foydalanuvchi qismi statelari
from user_side.states.process_track_state import ProcessTrack

# Foydalanuvchi qismi filterlari
from user_side.filters.checker import check_in_region, check_in_course, check_in_branch

# Admin qismi
from admin_panel.functions.start_section import admin_start_command,send_news
from admin_panel.functions.function import all_reports,today_reports

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
	dp.message.register(entry_section_function, F.text == '🏠 Bosh sahifaga qaytish')



    # Ortga tugmalari
	dp.message.register(go_back_function, ProcessTrack.course, F.text ==  '⏮ Ortga qaytish')  # Back to menu
	dp.message.register(go_back_function, ProcessTrack.region, F.text == '⏮ Ortga qaytish')  # Back to courses list
	dp.message.register(go_back_function, ProcessTrack.branch, F.text == '⏮ Ortga qaytish')  # Back to region list
	dp.message.register(go_back_function, ProcessTrack.info, F.text == '⏮ Ortga qaytish') # Back to brach list

    # Kurs tanlash va regionlarni chiqarish
	dp.message.register(show_course_function, F.text == 'Kurslar')
	dp.message.register(show_region_function, check_in_course(), ProcessTrack.course)
	dp.message.register(show_branch_function, check_in_region(), ProcessTrack.region)
	dp.message.register(show_info, ProcessTrack.branch, F.text != "🔄 Boshidan boshlash")

	# Munisa Akbarovna
	dp.message.register(registation_fullname, F.text == "✍️ Ro'yxatdan o'tish")
	dp.message.register(registation_phone_number, ProcessTrack.fullname)
	dp.message.register(send_info_to_admins, F.text == "✅ Tastiqlash")
	dp.message.register(show_info, F.text == "🔄 Boshidan boshlash")
	dp.message.register(registration_verification, ProcessTrack.phone_number)
	
	# Marjona Sultonova
	dp.message.register(about_us_handler, F.text == "🗒 Biz haqimizda")
	dp.message.register(get_contact_info, F.text == "📞 Aloqaga chiqish")
	#Bahodir Sadullayev
	dp.message.register(all_reports, F.text == "To'liq xisobot")
	dp.message.register(today_reports, F.text == "bugun otkanlar")
	dp.message.register(send_news, F.text == "yangilik jo'natish")

	dp.message.register(admin_start_command)


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