from aiogram import Router, F
from aiogram.filters import Command

from user_side.functions.start_section import user_start_command
from user_side.functions.entry_section import entry_section_function
from user_side.functions.list_based_section import show_course_function, show_region_function, show_branch_function, \
	show_info, go_back_function
from user_side.functions.contact_section import about_us_handler,get_contact_info
from user_side.functions.registration_section import registration_fullname, registration_phone_number, registration_verification, send_info_to_admins
# Foydalanuvchi qismi statelari
from user_side.states.process_track_state import ProcessTrack

# Foydalanuvchi qismi filterlari
from user_side.filters.checker import check_in_region, check_in_course, check_in_branch
from config import ADMIN_IDS

dp = Router()


# Constants
HOME_TEXTS = ["🏠 Bosh sahifaga qaytish", "🏠 Вернуться на главную", "🏠 Return to home"]
BACK_TEXTS = ["⏮ Ortga qaytish", "⏮ Назад", "⏮ Back"]
COURSES_TEXTS = ["Kurslar", "Курсы", "Courses"]
REGISTER_TEXTS = ["✍️ Ro'yxatdan o'tish", "✍️ Регистрация", "✍️ Register"]
CONFIRM_TEXTS = ["✅ Tasdiqlash", "✅ Подтвердить", "✅ Confirm"]
RESTART_TEXTS = ["🔄 Boshidan boshlash", "🔄 Начать заново", "🔄 Restart"]
ABOUT_US_TEXTS = ["🗒 Biz haqimizda", "🗒 О нас", "🗒 About us"]
CONTACT_TEXTS = ["📞 Aloqaga chiqish", "📞 Связаться", "📞 Contact us"]


# Marjona Sultonova
# User uchun start va til tanlash buyruqlari
dp.message.register(user_start_command, Command("start", "lang"), ~F.from_user.id.in_(ADMIN_IDS))

# Rahmatilla Xudoyberdiyev
# User uchun kirish qismi (yoxud asosiy qism)
dp.message.register(entry_section_function, ProcessTrack.current_language, ~F.from_user.id.in_(ADMIN_IDS))

# Begzod Turdibekov

# Kurslar bo'limi
dp.message.register(entry_section_function, F.text.in_(HOME_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))

# Ortga tugmalari
dp.message.register(go_back_function, ProcessTrack.course, F.text.in_(BACK_TEXTS),
                    ~F.from_user.id.in_(ADMIN_IDS))  # Back to menu
dp.message.register(go_back_function, ProcessTrack.region, F.text.in_(BACK_TEXTS),
                    ~F.from_user.id.in_(ADMIN_IDS))  # Back to courses list
dp.message.register(go_back_function, ProcessTrack.branch, F.text.in_(BACK_TEXTS),
                    ~F.from_user.id.in_(ADMIN_IDS))  # Back to region list
dp.message.register(go_back_function, ProcessTrack.info, F.text.in_(BACK_TEXTS),
                    ~F.from_user.id.in_(ADMIN_IDS))  # Back to brach list

# Kurs tanlash va regionlarni chiqarish

dp.message.register(show_course_function, F.text.in_(COURSES_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(show_region_function, check_in_course(), ProcessTrack.course, ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(show_branch_function, check_in_region(), ProcessTrack.region, ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(show_info, ProcessTrack.branch, ~F.text.in_(RESTART_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))

# Munisa Akbarovna

dp.message.register(registration_fullname, F.text.in_(REGISTER_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(registration_phone_number, ProcessTrack.fullname, ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(send_info_to_admins, F.text.in_(CONFIRM_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(show_info, F.text.in_(RESTART_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(registration_verification, ProcessTrack.phone_number, ~F.from_user.id.in_(ADMIN_IDS))

# Marjona Sultonova

dp.message.register(about_us_handler, F.text.in_(ABOUT_US_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))
dp.message.register(get_contact_info, F.text.in_(CONTACT_TEXTS), ~F.from_user.id.in_(ADMIN_IDS))