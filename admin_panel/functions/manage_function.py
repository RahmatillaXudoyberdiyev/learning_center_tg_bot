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
    from pprint import pprint as print
    print("'⚙ Manage'")
    await state.set_state(ProcessTrack.regions)
    connection = connection_pool.get_connection()
    try:
        from pprint import pprint as print
        query = connection.cursor()

        query.execute("Select id, name from regions")  # sql buyrug'i
        result = query.fetchall()  # natijalar list ko'rinishida olindi.

        button_list = dict()
        for i in range(len(result)):
            button_list[result[i][1]] = result[i][0]
            if result[i][1] in ProcessTrack.regions_list : # agarda setimni ichida nomi bo'lsa olib tashlayapman
                ProcessTrack.regions_list.remove(result[i][1])
        # Tugmalar yaratilib foydalanuvchi jo'natilmoqda.
        await message.answer(text="Viloyatlar ro'yxati :",
                             reply_markup=await show_regions_function_btn(button_list, state))
        await state.update_data(admin_region_list = button_list)  # positsiya yangilandi.

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
async def show_branches_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region'")
    await state.set_state(ProcessTrack.region_chosen)
    data = await state.get_data()

    region_name = message.text
    if data.get('admin_region_name'):
        region_name = data['admin_region_name']

    if region_name in data['admin_region_list']:
        connection = connection_pool.get_connection()
        try:
            region_id = data['admin_region_list'][region_name]
            query = connection.cursor()
            query.execute("SELECT id, name FROM branches WHERE region_id = %s", (region_id,))
            result = query.fetchall() # querydan barcha kelgan natija listga o'zgartiriladi.

            button_list = dict() # tugmalar uchun qiymatlarni yuklab oldim
            for id, name in result:
                button_list[name] = id

            await state.update_data(admin_region_name = region_name, admin_branch_list = button_list)


            await message.answer(text = await path_str_info(state) + f"<b>{region_name}</b> -> Mos filyallar!",
                                 reply_markup= await show_branches_function_btn(button_list),
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
async def show_branches_function_btn(button_list):

    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list.keys():
        buttons.button(text=value)

    buttons.adjust(2)  # Button tugmalarni 2 tadan qilib tartiblash.

    # "Ortga" va "Home" tugmalari
    buttons.row(KeyboardButton(text = "🗑 Viloyatni o'chirish"),KeyboardButton(text = "➕ Filial qo'shish"))
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text = "🏠 Bosh sahifaga qaytish"))

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.


# Begzod Turdibekov
# Info : "⚙ Manage" -> "➕ Viloyat qo'shish" |  Hali ro'yxatdan o'tilmagan viloyatlarni chiqarib beradi.
async def add_region_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> '➕ Viloyat qo'shish'")
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
    print("'⚙ Manage' -> '➕ Viloyat qo'shish' -> 'Chosen one of regions'")
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
    print("'⚙ Manage' -> '➕ Viloyat qo'shish' -> 'Chosen one of regions' -> '➕ Qo'shish'")
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
# Info : "⚙ Manage" + "Chosen region" + "➕ Filial qo'shis" | Filial qo'shish

async def ask_add_branch_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> '➕ Filial qo'shis'")

    await state.set_state(ProcessTrack.get_branch_name) # state o'zgartirildi.
    buttons = ReplyKeyboardBuilder()
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))

    await message.answer(text = "Iltimos filial nomini kiriting!",
                             reply_markup= buttons.as_markup(resize_keyboard = True))
# Begzod Turdibekov
# Info : "⚙ Manage" + "Chosen region" + "➕ Filial qo'shis" + "get_branch_name" | Filial nomini olish

async def admin_get_branch_name(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> '➕ Filial qo'shish' -> 'admin_get_branch_name()'")
    await state.set_state(ProcessTrack.ask_add_branch_name)

    buttons = ReplyKeyboardBuilder()
    buttons.row(KeyboardButton(text = "➕ Qo'shish"))
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))
    await state.update_data(admin_input_branch_name = message.text)
    await message.answer(f"Siz kiritgan filial nomi <b>{message.text}</b>!\n"
                         "Ushbu filialni qo'shishni xohlaysizmi ?",
                         reply_markup= buttons.as_markup(resize_keyboard = True),
                         parse_mode = "HTML")

# Begzod Turdibekov
# Info : "⚙ Manage" + "Chosen region" + "➕ Filial qo'shish" + "admin_add_branch_function()" | Filial qo'shish

async def admin_add_branch_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> '➕ Filial qo'shish' -> 'admin_add_branch_function()'")
    data = await state.get_data()
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        region_name = data['admin_region_name']
        region_id = data['admin_region_list'][region_name]

        input_branch_name = data['admin_input_branch_name']
        query.execute("INSERT INTO branches (name, region_id, info) VALUES (%s, %s, %s);", (input_branch_name, region_id, 'dfdf'))
        connection.commit()

        buttons = ReplyKeyboardBuilder()
        buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))

        await message.answer("Filial muaffaqiyatli qo'shildi ! ✅",
                             reply_markup=buttons.as_markup(resize_keyboard = True))

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()

# Begzod Turdibekov
# Info : '⚙ Manage' -> 'Chosen region' -> 'Chosen Branch' | Mos kurslarni ko'rsatish
async def admin_show_courses_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> 'Chosen Branch'")

    await state.set_state(ProcessTrack.courses)
    data = await state.get_data()

    branch_name = message.text
    if data.get('admin_branch_name'):
        branch_name = data['admin_branch_name']

    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        branch_id = data['admin_branch_list'][branch_name]
        query.execute("select id, name, info from courses where branch_id = %s", (branch_id,))

        course_list = dict()
        for row in query.fetchall():
            course_list[row[1]] = {'id' : row[0], 'info' : row[2]}


        await state.update_data(admin_branch_name = branch_name, admin_course_list = course_list)

        info = await path_str_info(state)
        await message.answer(f"{info}Kurslar:",
                             reply_markup= await admin_show_courses_function_btn(course_list))

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()

# ------------------------------------------

# Rahmatilla Xudoyberdiyev

async def ask_update_branch_info_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '✏️ Filial info qo'shish'")

    await state.set_state(ProcessTrack.get_branch_info)
    
    buttons = ReplyKeyboardBuilder()
    buttons.row(
        KeyboardButton(text='⏮ Ortga qaytish'),
        KeyboardButton(text="🏠 Bosh sahifaga qaytish")
    )
    
    await message.answer(
        "Iltimos filial uchun yangilangan ma'lumotni kiriting:",
        reply_markup=buttons.as_markup(resize_keyboard=True)
    )

async def admin_update_branch_info_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '✏️ Filial info qo'shish' -> 'admin_update_branch_info_function()'")
    data = await state.get_data()
    new_info = message.text


    branch_id = data.get('admin_branch_list', {}).get(data.get('admin_branch_name'))
    if not branch_id:
        await message.answer("Filial topilmadi!")
        return

    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        query.execute("UPDATE branches SET info = %s WHERE id = %s", (new_info, branch_id))
        connection.commit()
        await message.answer("Filial ma'lumotlari muvaffaqiyatli yangilandi!")

        await admin_show_courses_function(message, state)
    except mysql.connector.Error as err:
        print(err)
    finally:
        connection.close()

# --------------------------------------------------------




# Begzod Turdibekov
# Info : kurslar uchun button yasab beruvchi funksiya
async def admin_show_courses_function_btn(button_list):

    # Tugmalar bilan ishlash yangi o'zgaruvchi olindi.
    buttons = ReplyKeyboardBuilder()

    # Tugamalar joylanib chiqilyapti.
    for value in button_list.keys():
        buttons.button(text=value)

    buttons.adjust(2)  # Button tugmalarni 2 tadan qilib tartiblash.

    # "Ortga" va "Home" tugmalari

    buttons.row(
        KeyboardButton(text="✏️ Filial info qo'shish"),
        KeyboardButton(text="🗑 Filialni o'chirish"),
        KeyboardButton(text="➕ Kurs qo'shish")
    )
    buttons.row(
        KeyboardButton(text='⏮ Ortga qaytish'),
        KeyboardButton(text="🏠 Bosh sahifaga qaytish")
    )

    return buttons.as_markup(resize_keyboard=True)  # tugmalar markup holatiga o'tkazilib jo'natib yuborilayapti.


# Begzod Turdibekov
# Info : print("'⚙ Manage' -> 'Chosen region' -> 🗑 Viloyatni o'chirish") | Viloyatni o'chirishni so'rashlik
async def admin_ask_remove_region_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> '🗑 Viloyatni o'chirish'")
    await state.set_state(ProcessTrack.ask_remove_region)
    data = await state.get_data()
    info = f"Bu viloyatda {len(data['admin_branch_list'])} ta filial mavjud!\nUshbu viloyatni o'chirishni xohlaysizmi ?"
    buttons = ReplyKeyboardBuilder()
    buttons.row(KeyboardButton(text = "⏮ Ortga qaytish"), KeyboardButton(text = "🗑 O'chirish"))

    await message.answer(text = info, reply_markup=buttons.as_markup(resize_keyboard = True))

# Begzod Turdibekov
# Info : "'⚙ Manage' -> 'Chosen region' -> '🗑 Viloyatni o'chirish' -> '🗑 O'chirish' | Viloyatni o'chirish
async def admin_remove_region_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> '🗑 Viloyatni o'chirish' -> '🗑 O'chirish'")

    await state.set_state(ProcessTrack.courses)
    data = await state.get_data()


    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        query.execute("Delete from regions where name = %s", (data['admin_region_name'],))
        connection.commit()

        await message.answer(f"<b>{data['admin_region_name']}</b> viloyati o'chirildi.!", parse_mode = "HTML")
        ProcessTrack.regions_list.add(data['admin_region_name'])
        await state.update_data(admin_region_name = None)
        await show_regions_function(message, state)

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()


# Begzod Turdibekov
# Info : '⚙ Manage' -> 'Chosen region' -> 'Chosen Branch' -> '🗑 Filialni o'chirish' | Filialni o'chirishni so'rash

async def admin_ask_remove_branch_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> 'Chosen Branch' -> '🗑 Filialni o'chirish'")
    await state.set_state(ProcessTrack.ask_remove_branch)
    data = await state.get_data()
    info = f"Bu viloyatda <b>{len(data['admin_course_list'])}</b> ta kurslar mavjud!\nUshbu filialni o'chirishni xohlaysizmi?"
    buttons = ReplyKeyboardBuilder()
    buttons.row(KeyboardButton(text="⏮ Ortga qaytish"), KeyboardButton(text="🗑 O'chirish"))

    await message.answer(info, parse_mode = "HTML", reply_markup=buttons.as_markup(resize_keyboard = True))

# Begzod Turdibekov
# Info : '⚙ Manage' -> 'Chosen region' -> 'Chosen Branch' -> '🗑 Filialni o'chirish'-> '🗑 O'chirish'
async def admin_remove_branch_function(message : Message, state : FSMContext):
    print("'⚙ Manage' -> 'Chosen region' -> 'Chosen Branch' -> '🗑 Filialni o'chirish'-> '🗑 O'chirish'")

    data = await state.get_data()

    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        region_id = data['admin_region_list'][data['admin_region_name']]
        query.execute("Delete from branches where name = %s and region_id = %s", (data['admin_branch_name'], region_id))
        connection.commit()

        await message.answer(f"<b>{data['admin_branch_name']}</b> filiali muaffaqiyatli o'chirildi!", parse_mode="HTML")
        await state.update_data(admin_branch_name=None)
        await show_branches_function(message, state)

    except mysql.connector.Error as err:  # Biror bir xatolik yuz bersa.
        print(err)
        # Finallydagi close yetadi
    finally:
        connection.close()

# ------------------------------------------------------------------------

# Rahmatilla Xudoyberdiye
# Courses section

# Info : "➕ Kurs qo'shish" | Tanlangan filial uchun yangi kurs qo'shish uchun kurs nomini so'raydi.
async def ask_add_course_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '➕ Kurs qo'shish'")
    await state.set_state(ProcessTrack.get_course_name)
    buttons = ReplyKeyboardBuilder()
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))
    await message.answer(
        text="Iltimos kurs nomini kiriting!",
        reply_markup=buttons.as_markup(resize_keyboard=True)
    )

# Info : "➕ Kurs qo'shish" -> Kirilgan kurs nomini tasdiqlash so'rovi.
async def admin_get_course_name(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '➕ Kurs qo'shish' -> 'admin_get_course_name()'")
    await state.set_state(ProcessTrack.ask_add_course_confirm)
    buttons = ReplyKeyboardBuilder()
    buttons.button(text="➕ Qo'shish")
    buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))
    await state.update_data(admin_input_course_name=message.text)
    await message.answer(
        f"Siz kiritgan kurs nomi <b>{message.text}</b>!\nUshbu kursni qo'shishni xohlaysizmi?",
        reply_markup=buttons.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )

# Info : "➕ Kurs qo'shish" -> Tasdiqlangandan so'ng kursni ma'lumotlar bazasiga qo'shadi.
async def admin_add_course_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '➕ Kurs qo'shish' -> 'admin_add_course_function()'")
    data = await state.get_data()
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        branch_name = data['admin_branch_name']
        branch_id = data['admin_branch_list'][branch_name]
        input_course_name = data['admin_input_course_name']
        # Kurs uchun qo'shimcha ma'lumot hozircha standart qiymat sifatida berildi.
        course_info = "Yangi kurs ma'lumoti"
        query.execute(
            "INSERT INTO courses (name, branch_id, info) VALUES (%s, %s, %s);",
            (input_course_name, branch_id, course_info)
        )
        connection.commit()
        buttons = ReplyKeyboardBuilder()
        buttons.row(KeyboardButton(text='⏮ Ortga qaytish'), KeyboardButton(text="🏠 Bosh sahifaga qaytish"))
        await message.answer(
            "Kurs muaffaqiyatli qo'shildi! ✅",
            reply_markup=buttons.as_markup(resize_keyboard=True)
        )
        # Kurslar ro'yxatini yangilash:
        await admin_show_courses_function(message, state)
    except mysql.connector.Error as err:
        print(err)
    finally:
        connection.close()

# Info : "Kurs" | Agar admin mavjud kurs tugmasini bossagina, kursni o'chirishni so'raydi.
async def admin_ask_remove_course_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> 'Chosen Course' -> 'Kursni boshqarish'")
    await state.set_state(ProcessTrack.ask_remove_course)
    data = await state.get_data()
    course_name = message.text
    course_info = ""
    if course_name in data.get('admin_course_list', {}):
        course_info = data['admin_course_list'][course_name]['info']
    info = (
        f"Kurs: <b>{course_name}</b>\n"
        f"Ma'lumot: {course_info}\n"
        "Ushbu kursni o'chirish yoki ma'lumotini yangilashni xohlaysizmi?"
    )
    buttons = ReplyKeyboardBuilder()
    buttons.row(
        KeyboardButton(text="⏮ Ortga qaytish"),
        KeyboardButton(text="🗑 O'chirish")
    )
    # NEW: Button to update course info
    buttons.row(KeyboardButton(text="✏️ Kurs info qo'shish"))
    await state.update_data(admin_course_name=course_name)
    await message.answer(
        info,
        parse_mode="HTML",
        reply_markup=buttons.as_markup(resize_keyboard=True)
    )
# Info : "Kurs" | Kurs o'chirishni tasdiqlagach, uni ma'lumotlar bazasidan o'chiradi.
async def admin_remove_course_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> 'Chosen Course' -> '🗑 Kursni o'chirish' -> '🗑 O'chirish'")
    data = await state.get_data()
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        branch_id = data['admin_branch_list'][data['admin_branch_name']]
        course_data = data['admin_course_list'].get(data['admin_course_name'])
        if not course_data:
            await message.answer("Kurs topilmadi!")
            return
        course_id = course_data['id']
        query.execute("DELETE FROM courses WHERE id = %s AND branch_id = %s", (course_id, branch_id))
        connection.commit()
        await message.answer(
            f"<b>{data['admin_course_name']}</b> kursi muaffaqiyatli o'chirildi!",
            parse_mode="HTML"
        )
        await state.update_data(admin_course_name=None)
        # Kurslar ro'yxatini yangilash:
        await admin_show_courses_function(message, state)
    except mysql.connector.Error as err:
        print(err)
    finally:
        connection.close()

async def ask_update_course_info_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '✏️ Kurs info qo'shish'")
    # Here we use a new state to capture course info update.
    await state.set_state(ProcessTrack.get_course_info)
    buttons = ReplyKeyboardBuilder()
    buttons.row(
        KeyboardButton(text='⏮ Ortga qaytish'),
        KeyboardButton(text="🏠 Bosh sahifaga qaytish")
    )
    await message.answer(
        "Iltimos kurs uchun yangilangan ma'lumotni kiriting:",
        reply_markup=buttons.as_markup(resize_keyboard=True)
    )

async def admin_update_course_info_function(message: Message, state: FSMContext):
    print("'⚙ Manage' -> 'Chosen Branch' -> '✏️ Kurs info qo'shish' -> 'admin_update_course_info_function()'")
    data = await state.get_data()
    new_info = message.text
    course_data = data.get('admin_course_list', {}).get(data.get('admin_course_name'))
    if not course_data:
        await message.answer("Kurs topilmadi!")
        return
    course_id = course_data['id']
    connection = connection_pool.get_connection()
    try:
        query = connection.cursor()
        query.execute("UPDATE courses SET info = %s WHERE id = %s", (new_info, course_id))
        connection.commit()
        await message.answer("Kurs ma'lumotlari muvaffaqiyatli yangilandi!")
        await admin_show_courses_function(message, state)
    except mysql.connector.Error as err:
        print(err)
    finally:
        connection.close()



# -------------------------------------------------------------------------
# Begzod Turdibekov
# info : "⏮ Ortga qaytish" | Ortga qaytish uchun ishlatiladi.
async def go_back_function(message: Message, state: FSMContext):
    current_state = await state.get_state()  # hozirgi ishlatilayotgan state yuklab olinayapti.

    # Agar viloyatlar ro'yxatida bo'lsa
    if current_state == ProcessTrack.regions:
        await admin_start_command(message, state)
        await state.update_data(admin_region_list=dict())

    # Agar yangi viloyat qo'shish bosqichida bo'lsa
    elif current_state == ProcessTrack.add_region:
        await show_regions_function(message, state)

    # Agar viloyat nomini tasdiqlash bosqichida bo'lsa
    elif current_state == ProcessTrack.add_region_name:
        await add_region_function(message, state)

    # Agar tanlangan viloyat bosqichida bo'lsa
    elif current_state == ProcessTrack.region_chosen:
        await show_regions_function(message, state)
        await state.update_data(admin_region_name=None, admin_branch_list=dict())

    # Agar filial nomi kiritish yoki qo'shish bosqichida bo'lsa
    elif current_state == ProcessTrack.get_branch_name or current_state == ProcessTrack.ask_add_branch_name:
        await show_branches_function(message, state)

    # Agar kurslar bosqichida yoki filialdagi kurslar ko'rsatilayotgan bo'lsa
    elif current_state == ProcessTrack.courses:
        await state.update_data(admin_branch_name=None, admin_courses_list=dict())
        await show_branches_function(message, state)

    # Agar viloyatni o'chirishni so'rayotgan bosqichida bo'lsa
    elif current_state == ProcessTrack.ask_remove_region:
        await show_branches_function(message, state)

    # Agar filialni o'chirishni so'rayotgan bosqichida bo'lsa
    elif current_state == ProcessTrack.ask_remove_branch:
        await admin_show_courses_function(message, state)

    # --- NEW: Courses Section Go-Back Conditions ---
    # Agar admin yangi kurs nomini kiritayotgan bosqichida bo'lsa
    elif current_state == ProcessTrack.get_course_name:
        await admin_show_courses_function(message, state)

    # Agar admin kurs qo'shish tasdiqini kutayotgan bosqichida bo'lsa
    elif current_state == ProcessTrack.ask_add_course_confirm:
        await admin_show_courses_function(message, state)

    # Agar admin kursni o'chirishni tasdiqlayotgan bosqichida bo'lsa
    elif current_state == ProcessTrack.ask_remove_course:
        await admin_show_courses_function(message, state)

    # Agar admin kursni tahrirlash bosqichida bo'lsa
    elif current_state == ProcessTrack.get_course_info:
        await admin_show_courses_function(message, state)

    # Agar admin filialni tahrirlash bosqichida bo'lsa
    elif current_state == ProcessTrack.get_branch_info:
        await admin_show_courses_function(message, state)


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