from aiogram import Router, F
from aiogram.filters import Command

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
from config import ADMIN_IDS


# Constants
HOME_TEXTS = ["🏠 Bosh sahifaga qaytish", "🏠 Вернуться на главную", "🏠 Return to home"]
BACK_TEXTS = ["⏮ Ortga qaytish", "⏮ Назад", "⏮ Back"]
COURSES_TEXTS = ["Kurslar", "Курсы", "Courses"]
REGISTER_TEXTS = ["✍️ Ro'yxatdan o'tish", "✍️ Регистрация", "✍️ Register"]
CONFIRM_TEXTS = ["✅ Tasdiqlash", "✅ Подтвердить", "✅ Confirm"]
RESTART_TEXTS = ["🔄 Boshidan boshlash", "🔄 Начать заново", "🔄 Restart"]
ABOUT_US_TEXTS = ["🗒 Biz haqimizda", "🗒 О нас", "🗒 About us"]
CONTACT_TEXTS = ["📞 Aloqaga chiqish", "📞 Связаться", "📞 Contact us"]

dp = Router()

# Rahmatilla Xudoyberdiyev
# Admin uchun start buyrug'i
dp.message.register(admin_start_command, Command("start"), F.from_user.id.in_(ADMIN_IDS))

# Begzod Turdibekov
dp.message.register(home_action_function, F.text.in_(HOME_TEXTS), check_admin_state())
dp.message.register(admin_go_back_function, F.from_user.id.in_(ADMIN_IDS), F.text.in_(BACK_TEXTS))

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

dp.message.register(admin_ask_remove_region_function, AdminProcessTrack.region_chosen,
                    F.text == "🗑 Viloyatni o'chirish")
dp.message.register(admin_remove_region_function, AdminProcessTrack.ask_remove_region, F.text == "🗑 O'chirish")
dp.message.register(admin_remove_branch_function, AdminProcessTrack.ask_remove_branch, F.text == "🗑 O'chirish")
dp.message.register(admin_ask_remove_branch_function, AdminProcessTrack.courses, F.text == "🗑 Filialni o'chirish")

dp.message.register(add_region_function, AdminProcessTrack.regions, F.text == "➕ Viloyat qo'shish")
dp.message.register(ask_add_branch_function, F.text == "➕ Filial qo'shish", AdminProcessTrack.region_chosen)

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

dp.message.register(ask_update_course_info_function, AdminProcessTrack.ask_remove_course,
                    F.text == "✏️ Kurs info qo'shish")
dp.message.register(admin_update_course_info_function, AdminProcessTrack.get_course_info)

# Bahodir Sadullayev
dp.message.register(all_reports, F.text == "To'liq hisobot", F.from_user.id.in_(ADMIN_IDS))
dp.message.register(today_reports, F.text == "Bugun o'tganlar", F.from_user.id.in_(ADMIN_IDS))
dp.message.register(send_news, F.text == "Yangilik jo'natish", F.from_user.id.in_(ADMIN_IDS))
dp.message.register(process_send_news, AdminProcessTrack.send_news, F.from_user.id.in_(ADMIN_IDS))
