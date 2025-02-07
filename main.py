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
from admin_panel.functions.manage_function import show_regions_function, home_action_function, \
	go_back_function as admin_go_back_function, add_region_function, region_name_confirm_function, \
	region_name_add_action_function, region_chose_action_function
from admin_panel.states.process_track_state import ProcessTrack as AdminProcessTrack
from admin_panel.filters.checker import check_admin_state


from config import API_TOKEN # Sizning API tokeningiz
from config import ADMIN_IDS


dp = Dispatcher()



# main dasturni yurgazuvchi funksiya
async def main():

	bot = Bot(token = API_TOKEN)

	# admin panel
	# ------------------------------------------------------------------------------------------------------
	# Rahmatilla Xudoyberdiyev
	# Admin uchun start buyrug'i
	dp.message.register(admin_start_command, Command("start"), F.from_user.id.in_(ADMIN_IDS))

	# Begzod Turdibekov
	dp.message.register(home_action_function, F.text == "🏠 Bosh sahifaga qaytish", check_admin_state())
	dp.message.register(admin_go_back_function, F.text == "⏮ Ortga qaytish")

	# Begzod Turdibekov
	# Manage tugmasi bosilganda regionlar chiqishi
	dp.message.register(show_regions_function,AdminProcessTrack.chosen_menu, F.text == "⚙ Manage")
	dp.message.register(add_region_function, AdminProcessTrack.regions, F.text == "➕ Viloyat qo'shish")
	dp.message.register(region_chose_action_function, AdminProcessTrack.regions)
	dp.message.register(region_name_confirm_function, AdminProcessTrack.add_region)
	dp.message.register(region_name_add_action_function, AdminProcessTrack.add_region_name, F.text == "➕ Qo'shish")

	# user panel
	#----------------------------------------------------------------------------------------------
	# Marjona Sultonova
	# User uchun start va til tanlash buyruqlari
	dp.message.register(user_start_command, Command("start", "lang"), ~F.from_user.id.in_(ADMIN_IDS))


	
	# Rahmatilla Xudoyberdiyev
	# User uchun kirish qismi (yoxud asosiy qism)
	dp.message.register(entry_section_function, ProcessTrack.current_language, ~F.from_user.id.in_(ADMIN_IDS))

	#Begzod Turdibekov

    # Kurslar bo'limi
	dp.message.register(entry_section_function, F.text == '🏠 Bosh sahifaga qaytish', ~F.from_user.id.in_(ADMIN_IDS))

    # Ortga tugmalari
	dp.message.register(go_back_function, ProcessTrack.course, F.text ==  '⏮ Ortga qaytish', ~F.from_user.id.in_(ADMIN_IDS))  # Back to menu
	dp.message.register(go_back_function, ProcessTrack.region, F.text == '⏮ Ortga qaytish', ~F.from_user.id.in_(ADMIN_IDS))  # Back to courses list
	dp.message.register(go_back_function, ProcessTrack.branch, F.text == '⏮ Ortga qaytish', ~F.from_user.id.in_(ADMIN_IDS))  # Back to region list
	dp.message.register(go_back_function, ProcessTrack.info, F.text == '⏮ Ortga qaytish', ~F.from_user.id.in_(ADMIN_IDS)) # Back to brach list

    # Kurs tanlash va regionlarni chiqarish
	dp.message.register(show_course_function, F.text == 'Kurslar', ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(show_region_function, check_in_course(), ProcessTrack.course, ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(show_branch_function, check_in_region(), ProcessTrack.region, ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(show_info, ProcessTrack.branch, F.text != "🔄 Boshidan boshlash", ~F.from_user.id.in_(ADMIN_IDS))

	# Munisa Akbarovna
	dp.message.register(registation_fullname, F.text == "✍️ Ro'yxatdan o'tish", ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(registation_phone_number, ProcessTrack.fullname, ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(send_info_to_admins, F.text == "✅ Tastiqlash", ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(show_info, F.text == "🔄 Boshidan boshlash", ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(registration_verification, ProcessTrack.phone_number, ~F.from_user.id.in_(ADMIN_IDS))
	
	# Marjona Sultonova
	dp.message.register(about_us_handler, F.text == "🗒 Biz haqimizda", ~F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(get_contact_info, F.text == "📞 Aloqaga chiqish", ~F.from_user.id.in_(ADMIN_IDS))
	#Bahodir Sadullayev
	dp.message.register(all_reports, F.text == "To'liq xisobot", F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(today_reports, F.text == "bugun otkanlar", F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(send_news, F.text == "yangilik jo'natish", F.from_user.id.in_(ADMIN_IDS))


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