from aiogram.types import Message, KeyboardButton
from aiogram.fsm.context import FSMContext
from user_side.keyboards.list_based_keyboards import registration_back_button
from user_side.keyboards.entry_keyboards import menu_buttons
from user_side.states.process_track_state import ProcessTrack
from user_side.keyboards.language_keyboards import language_button
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Begzod Turdibekov
# Info : Kurslar ro'yxatini ko'rsatish uchun

import mysql.connector.pooling
from config import MySQL_password, MySQL_database, MySQL_host, MySQL_port, MySQL_user

db_config = {
    "host": MySQL_host,
    "port": MySQL_port,
    "user": MySQL_user,
    "password": MySQL_password,
    "database": MySQL_database,
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config  
)


# Begzod Turdibekov
# Info : Mavjud kurslarni namoyish etish uchun.
async def show_course_function(message: Message, state: FSMContext):
    await state.set_state(ProcessTrack.course)
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        query.execute("Select distinct course_name from course_branch_region")  # sql buyrug'i
        button_list = query.fetchall()  # natijalar list ko'rinishida olindi.
        await state.update_data(course_list=button_list, state='course')  # positsiya yangilandi.

        # Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
        await message.answer(text="Kurslar ro'yxati :", reply_markup= await create_course_list_buttons(button_list, state))

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()  # ulanish uzilmoqda.


# Begzod Turdibekov
# Info : Kurslar ro'yxati uchun keyboard yaratib beradigan funksiya

async def create_course_list_buttons(button_list, state: FSMContext):

    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list:
        buttons.button(text=value[0])

    buttons.adjust(2)  # Button tugmalarni 2 tadan qilib tartiblash.

    # "Ortga" va "Home" tugmalari
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.

# Begzod Turdibekov
# Info : Mos Viloyatlar chiqarilayapti.
async def show_region_function(message: Message, state: FSMContext):
    await state.set_state(ProcessTrack.region)


    data = await state.update_data()  # ma'lumotlarni statedan yuklab olishlik

    course_name = message.text
    if data.get('course_name'):
        course_name = data['course_name']
    connection = connection_pool.get_connection()

    try:
        query = connection.cursor()
        query.execute("SELECT distinct region_name FROM course_branch_region WHERE course_name = %s", (course_name,)) # sql buyrug'i
        button_list = query.fetchall()  # natijalar list ko'rinishida olindi.
        await state.update_data(region_list = button_list, state='region', course_name=course_name)  # kerakli qismlar yoki yangilanadi yoki yangidan saqlanadi.

        # Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
        await message.answer(text=await create_str_from_list(state) + f"\n<b>{course_name}</b> kursi mavjud bo'lgan viloyatlar!",
                             reply_markup=await create_branch_list_buttons(button_list, state), parse_mode="HTML")

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi

    finally:
        connection.close()  # ulanishni uzishni taminlash

# Begzod Turdibekov
# Info : regionlarnining tugmalarini xosil qiluvchi funksiya
async def create_region_list_buttons(button_list, state: FSMContext):
    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list:
        buttons.button(text=value[0])

    # Tugmalarni 2 ustunli qilib tartiblaymiz
    buttons.adjust(2, repeat=True)

    # "Kurslar" va "Home" tugmalari
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.

#-------------------------------

# Begzod Turdibekov
# Info : Mos filyallarni chiqaruvchi funksiya
async def show_branch_function(message: Message, state: FSMContext):
    await state.set_state(ProcessTrack.branch)
    data = await state.update_data()  # ma'lumotlarni statedan yuklab olishlik

    region_name = message.text
    if data.get('region_name'):
        region_name = data['region_name']

    connection = connection_pool.get_connection()

    try:
        query = connection.cursor()
        params = (data['course_name'], region_name)
        query.execute("SELECT DISTINCT branch_name FROM course_branch_region WHERE course_name = %s AND region_name = %s", params)  # sql buyrug'
        button_list = query.fetchall()  # natijalar list ko'rinishida olindi.
        await state.update_data(branch_list = button_list, state='region', region_name = region_name)  # kerakli qismlar yoki yangilanadi yoki yangidan saqlanadi.

        # Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
        await message.answer(text = await create_str_from_list(state) + f"<b>{data['course_name']}</b> ➡ <b>{region_name}</b> : Mavjuda filyallar!",
                             reply_markup=await create_branch_list_buttons(button_list, state), parse_mode="HTML")

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi

    finally:
        connection.close()  # ulanishni uzishni taminlash

# Begzod Turdibekov
# Info : filyallarning tugmalari chiqishi ta'minlovchi funksiya
async def create_branch_list_buttons(button_list, state: FSMContext):
    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list:
        buttons.button(text=value[0])

    # Tugmalarni 2 ustunli qilib tartiblaymiz
    buttons.adjust(2, repeat=True)

    # "Kurslar" va "Home" tugmalari
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.


#-----------------------------------

# Begzod Turdibekov
# Info : Kurs va filyal bo'yicha ma'lumotlarni chiqarish

async def show_info(message: Message, state: FSMContext):
    await state.set_state(ProcessTrack.info)
    data = await state.get_data()
    branch_name = message.text
    if data.get('branch_name'):
        branch_name = data['branch_name']
    await state.update_data(branch_name=branch_name)
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        params = (data['course_name'], data['region_name'], branch_name)
        query.execute(
            "SELECT course_info, branch_info FROM course_branch_region WHERE course_name = %s AND region_name = %s AND branch_name = %s", 
            params
        )
        info = query.fetchall()
        if info and info[0]:
            text = await create_str_from_list(state) + \
                   f"<b>{data['course_name']}</b> ➡ <b>{data['region_name']}</b> ➡ <b>{branch_name}</b>\n\n" + \
                   f"<b>Kurs ma'lumoti:</b> {info[0][0]}\n" + \
                   f"<b>Filial ma'lumoti:</b> {info[0][1]}"
            await message.answer(text=text, reply_markup=registration_back_button, parse_mode="HTML")
        else:
            await message.answer("Ma'lumot topilmadi.", reply_markup=registration_back_button)
        await state.update_data(state=None)
    except mysql.connector.Error as err:
        print(err)
    finally:
        connection.close()



# # Begzod Turdibekov
# # Info : Ortga qaytish funksiyasi

async def go_back_function(message: Message, state: FSMContext):
    current_state = await state.get_state() # state holati yuklab olinyapti. Dastur davomida ishlataman.
    data = await state.get_data() # Data ma'lumotlarlar yuklab olinyapti.
    if current_state == ProcessTrack.course: # Hozirgi state = course statiga, bitta ortga qaytish menu lar bo'limiga bo'ladi.
        print(message.text)
        await state.update_data(current_language=message.text)
        await message.answer("Iltimos kerakli menuni tanlang:", reply_markup=menu_buttons)
        await state.set_state(ProcessTrack.chosen_menu)
    elif current_state == ProcessTrack.region: # Hozir state = region bo'lsa, bitta ortga qaytish kurslar bo'limiga bo'ladi.
        print(message.text)
        await state.update_data(course_name = None)  # bitta ortga qaytilganda, agarda course_name bo'lsa uninig qiymatini None ga o'zlashtiraman.
        await show_course_function(message,state) # kurslarni chiqarish funksiyasini ishga tushirish
    elif current_state == ProcessTrack.branch: # Hozir state = branch bo'lsa, bitta ortga qaytish region lar bo'limiga bo'ladi.
        print(message.text)
        await state.update_data(region_name = None) # bitta ortga qaytilganda, agarda course_name bo'lsa uninig qiymatini None ga o'zlashtiraman.
        await show_region_function(message, state) # regionlarni chiqarish funksiyasini ishga tushirish
    elif current_state == ProcessTrack.info: # Hozir state = info bo'lsa, bitta ortga qaytish branch lar bo'limiga bo'ladi.
        print(message.text)
        await state.update_data(branch_name = None) # bitta ortga qaytilganda, agarda course_name bo'lsa uninig qiymatini None ga o'zlashtiraman.
        await show_branch_function(message, state) # brenchlarni chiqarish funksiyasini ishga tushirish


# Begzod Turdibekov
# Info : User haqida ma'lumot beruvchi funksiya

async def create_str_from_list(state : FSMContext):
    data = await state.get_data() # data yuklab olinyapti.
    info = "" # user info uchun bo'm bosh string ochib oldim.
    if data.get('course_name'): # Kelayotgan data lug'atidan course_name bormi yo'qmi tekshirib chiqayapman. Bo'lsa undagi ma'lumot bilan to'ldirib chiqayapman.
        info += f"Kurs ✅: {data['course_name']}\n"
    if data.get('region_name'): # Kelayotgan data lug'atidan region_name bormi yo'qmi tekshirib chiqayapman. Bo'lsa undagi ma'lumot bilan to'ldirib chiqayapman.
        info += f"Viloyat ✅: {data['region_name']}\n"
    if data.get('branch_name'): # Kelayotgan data lug'atidan branch_name bormi yo'qmi tekshirib chiqayapman. Bo'lsa undagi ma'lumot bilan to'ldirib chiqayapman.
        info += f"Filyal ✅: {data['branch_name']}\n"

    return info # natija qaytarilib yuborilayapti.
