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
from admin_panel.functions.start_section import admin_start_command,send_news, process_send_news
from admin_panel.functions.function import all_reports,today_reports
from admin_panel.functions.manage_function import show_regions_function, home_action_function, \
	go_back_function as admin_go_back_function, add_region_function, region_name_confirm_function, \
	region_name_add_action_function, ask_add_branch_function, show_branches_function as admin_show_branches_function, \
	admin_get_branch_name, admin_add_branch_function, admin_show_courses_function, admin_ask_remove_region_function, \
	admin_remove_region_function, admin_ask_remove_branch_function, admin_remove_branch_function
from admin_panel.states.process_track_state import ProcessTrack as AdminProcessTrack
from admin_panel.filters.checker import check_admin_state

from admin_panel.functions.manage_function import (
    ask_add_course_function,
    admin_get_course_name,
    admin_add_course_function,
    admin_ask_remove_course_function,
    admin_remove_course_function,
	ask_update_course_info_function,
    admin_update_course_info_function,
    ask_update_branch_info_function, admin_update_branch_info_function
)

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
	dp.message.register(admin_go_back_function,F.from_user.id.in_(ADMIN_IDS), F.text == "⏮ Ortga qaytish")


	dp.message.register(admin_add_branch_function, AdminProcessTrack.ask_add_branch_name, F.text == "➕ Qo'shish")


	dp.message.register(
        ask_update_branch_info_function,
        AdminProcessTrack.courses,
        F.text == "✏️ Filial info qo'shish"
    )
	dp.message.register(
        admin_update_branch_info_function,
        AdminProcessTrack.get_branch_info
    )

	dp.message.register(admin_ask_remove_region_function, AdminProcessTrack.region_chosen, F.text == "🗑 Viloyatni o'chirish")
	dp.message.register(admin_remove_region_function, AdminProcessTrack.ask_remove_region, F.text == "🗑 O'chirish")
	dp.message.register(admin_remove_branch_function, AdminProcessTrack.ask_remove_branch, F.text == "🗑 O'chirish")
	dp.message.register(admin_ask_remove_branch_function, AdminProcessTrack.courses, F.text == "🗑 Filialni o'chirish")

	dp.message.register(add_region_function, AdminProcessTrack.regions, F.text == "➕ Viloyat qo'shish")
	dp.message.register(ask_add_branch_function, F.text == "➕ Filial qo'shish",AdminProcessTrack.region_chosen)

	dp.message.register(show_regions_function, AdminProcessTrack.chosen_menu, F.text == "⚙ Manage")
	dp.message.register(admin_get_branch_name, AdminProcessTrack.get_branch_name)
	dp.message.register(admin_show_branches_function, AdminProcessTrack.regions)
	dp.message.register(admin_show_courses_function, AdminProcessTrack.region_chosen)

	dp.message.register(region_name_confirm_function, AdminProcessTrack.add_region)
	dp.message.register(region_name_add_action_function, AdminProcessTrack.add_region_name, F.text == "➕ Qo'shish")






	dp.message.register(ask_add_course_function, AdminProcessTrack.courses, F.text == "➕ Kurs qo'shish")
	dp.message.register(admin_get_course_name, AdminProcessTrack.get_course_name)
	dp.message.register(admin_add_course_function, AdminProcessTrack.ask_add_course_confirm, F.text == "➕ Qo'shish")
	dp.message.register(admin_ask_remove_course_function, AdminProcessTrack.courses)
	dp.message.register(admin_remove_course_function, AdminProcessTrack.ask_remove_course, F.text == "🗑 O'chirish")

	dp.message.register(ask_update_course_info_function, AdminProcessTrack.ask_remove_course, F.text == "✏️ Kurs info qo'shish")
	dp.message.register(admin_update_course_info_function, AdminProcessTrack.get_course_info)


	#Bahodir Sadullayev
	dp.message.register(all_reports, F.text == "To'liq hisobot", F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(today_reports, F.text == "Bugun o'tganlar", F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(send_news, F.text == "Yangilik jo'natish", F.from_user.id.in_(ADMIN_IDS))
	dp.message.register(process_send_news, AdminProcessTrack.send_news, F.from_user.id.in_(ADMIN_IDS))

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