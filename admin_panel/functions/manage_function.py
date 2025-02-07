from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from admin_panel.states.process_track_state import ProcessTrack
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
import mysql.connector.pooling
from config import MySQL_password, MySQL_database, MySQL_host, MySQL_port, MySQL_user
from admin_panel.functions.start_section import admin_start_command


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
# Info : "⚙ Manage" | Regionlarni ko'rsatuvchi funksiya
async def show_regions_function(message : Message, state : FSMContext):
    await state.set_state(ProcessTrack.regions)
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        query.execute("Select distinct name from regions")  # sql buyrug'i
        result = query.fetchall()  # natijalar list ko'rinishida olindi.

        button_list = [''] * len(result)
        for i in range(len(result)):
            button_list[i] = result[i][0]
            if result[i][0] in ProcessTrack.regions_list : # agarda setimni ichida nomi bo'lsa olib tashlayapman
                ProcessTrack.regions_list.remove(result[i][0])

        # Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
        await message.answer(text="Viloyatlar ro'yxati :",
                             reply_markup=await show_regions_function_btn(button_list, state))
        await state.update_data(region_list = set(button_list))  # positsiya yangilandi.

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()  # ulanish uzilmoqda.


# Begzod Turdibekov
# Info : show_regions_function_btn() funksiyasi uchun button yaratib beruvchi yordamchi funksiya
async def show_regions_function_btn(button_list, state: FSMContext):

    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list:
        buttons.button(text=value)

    buttons.adjust(2)  # Button tugmalarni 2 tadan qilib tartiblash.

    # "Ortga" va "Home" tugmalari
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'),KeyboardButton(text = "➕ Viloyat qo'shish"))
    buttons.row(KeyboardButton(text = "🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.

# Begzod Turdibekov
# Info : "⚙ Manage" -> "Chosen region" | Viloyatlardan biri tanlanganda unga mos filiallar chiqariladi.
async def region_chose_action_function(message : Message, state : FSMContext):
    await state.set_state(ProcessTrack.region_chosen)
    data = await state.get_data()
    if message.text in data['region_list']:
        connection = connection_pool.get_connection()
        try:
            query = connection.cursor()
            query.execute("SELECT branch_name FROM course_branch_region WHERE region_name = %s", (message.text,))
            result = query.fetchall() # querydan barcha kelgan natija listga o'zgartiriladi.
            button_list = [value[0] for value in result] # tugmalar uchun qiymatlarni yuklab oldim

            await state.update_data(admin_region_name = message.text)


            await message.answer(text = await path_str_info(state) + f"<b>{message.text}</b> -> Mos filyallar!",
                                 reply_markup= await region_chose_action_function_btn(button_list),
                                 parse_mode = "HTML")

        except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
            print(err)
            # Finallydagi close yetadi
        finally:
            connection.close()  # ulanish uzilmoqda.
    else:
        await message.answer("Iltimos tugmalardan birini tanlang!")


# Begzod Turdiekov
# Info : region_chose_action_function() funksiyasi uchun button yaratib beruvchi yordamchi funksiya
async def region_chose_action_function_btn(button_list):

    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list:
        buttons.button(text=value)

    buttons.adjust(2)  # Button tugmalarni 2 tadan qilib tartiblash.

    # "Ortga" va "Home" tugmalari
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'),KeyboardButton(text = "❌ O'chirish"))
    buttons.row(KeyboardButton(text = "🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.


# Begzod Turdibekov
# Info : "⚙ Manage" -> "➕ Viloyat qo'shish" |  Hali ro'yxatdan o'tilmagan viloyatlarni chiqarib beradi.
async def add_region_function(message : Message, state : FSMContext):
    await state.set_state(ProcessTrack.add_region) # state o'zgartirildi.

    await message.answer(text = "Xali ro'yxatda mavjud bo'lmagan viloyatlar!",
                         reply_markup= await add_region_function_btn(list(ProcessTrack.regions_list)))

# Begzod Turdibekov
# Info : add_region_function() uchun button yaratib beruvchi, yordamchi funksiya
async def add_region_function_btn(button_list):

    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list:
        buttons.button(text=value)

    buttons.adjust(2)  # Button tugmalarni 2 tadan qilib tartiblash.

    # "Ortga" va "Home" tugmalari
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text = "🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.

# Begzod Turdibekov
# Info : "⚙ Manage" -> "➕ Viloyat qo'shish" -> "Chosen one of regions" -> tanlagan viloyatni qo'shish mumkin.
async def region_name_confirm_function(message : Message, state : FSMContext):
    if message.text in ProcessTrack.regions_list:
        await state.set_state(ProcessTrack.add_region_name)

        buttons = ReplyKeyboardBuilder() # tugmalar yaratish tayyor variable

        buttons.row(KeyboardButton(text = '⏮ Ortga qaytish'), KeyboardButton(text = "➕ Qo'shish")) # tugmalar qo'shildi.

        await message.answer(f"Tanlangan viloyat : <b>{message.text}</b>.", reply_markup=buttons.as_markup(resize_keyboard=True), parse_mode = "HTML")
        await state.update_data(admin_add_region_name = message.text)
    else:
        await message.answer("Iltimos tugmalardan birini tanlang!")

# Begzod Turdibekov
# Info : "⚙ Manage" -> "➕ Viloyat qo'shish" -> "Chosen one of regions" -> "➕ Qo'shish" | Regionni ba'zaga qo'shadi.
async def region_name_add_action_function(message : Message, state : FSMContext):
    data = await state.get_data()
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        query.execute("INSERT INTO regions (name) VALUES (%s);", (data['admin_add_region_name'],))
        connection.commit()
        ProcessTrack.regions_list.remove(data['admin_add_region_name'])
        await state.update_data(admin_add_region_name = None)

        await message.answer(f"<b>{data['admin_add_region_name']}</b> viloyati qo'shildi! 👏", parse_mode = "HTML")

        await show_regions_function(message, state)

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()  # ulanish uzilmoqda.


# Begzod Turdibekov
# info : "⏮ Ortga qaytish" | Ortga qaytish uchun ishlatiladi.
async def go_back_function(message : Message, state : FSMContext):
    current_state = await state.get_state() # hozirgi ishlatilayotgan state yuklab olinayapti.

    # Har bir
    if current_state == ProcessTrack.regions:
        await admin_start_command(message, state)

    if current_state == ProcessTrack.add_region:
        await show_regions_function(message, state)

    if current_state == ProcessTrack.add_region_name:
        await add_region_function(message, state)

    if current_state == ProcessTrack.region_chosen:
        await show_regions_function(message, state)

# Begzod Turdibekov
# info : "🏠 Bosh sahifaga qaytish" | Bosh sahifaga o'tish uchun
async def home_action_function(message : Message, state : FSMContext):
    await admin_start_command(message, state)

# Begzod Turdibekov
# Info : Viloyat, filyal yoki kurs tanlagan bo'lsa ularni info sifatida string qilib jo'natadi.
async def path_str_info(state : FSMContext):
    data = await state.get_data() # data yuklab olinyapti.
    info = "" # user info uchun bo'm bosh string ochib oldim.
    if data.get('admin_region_name'): # Kelayotgan data lug'atidan course_name bormi yo'qmi tekshirib chiqayapman. Bo'lsa undagi ma'lumot bilan to'ldirib chiqayapman.
        info += f"Viloyat ✅: {data['admin_region_name']}\n"
    if data.get('admin_branch_name'): # Kelayotgan data lug'atidan region_name bormi yo'qmi tekshirib chiqayapman. Bo'lsa undagi ma'lumot bilan to'ldirib chiqayapman.
        info += f"Filyal ✅: {data['admin_branch_name']}\n"
    if data.get('admin_course_name'): # Kelayotgan data lug'atidan branch_name bormi yo'qmi tekshirib chiqayapman. Bo'lsa undagi ma'lumot bilan to'ldirib chiqayapman.
        info += f"Kurs ✅: {data['admin_course_name']}\n"

    return info # natija qaytarilib yuborilayapti.