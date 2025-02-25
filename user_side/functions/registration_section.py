from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext
import mysql.connector.pooling
from user_side.states.process_track_state import ProcessTrack
from user_side.keyboards.registration_keyboards import get_confirmation_keyboard
from user_side.keyboards.entry_keyboards import get_entry_keyboard
from config import MySQL_password, MySQL_database, MySQL_host, MySQL_port, MySQL_user, ADMIN_IDS
from config import ADMIN_IDS

from user_side.translations.translation_functions import translate_into

DB_CONFIG = {
    "host": MySQL_host,
    "port": MySQL_port,
    "user": MySQL_user,
    "password": MySQL_password,
    "database": MySQL_database,
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **DB_CONFIG
)

def get_course_and_branch_ids(course_name, branch_name):
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT c.id, b.id FROM courses c
        JOIN branches b ON c.branch_id = b.id
        WHERE c.name = %s AND b.name = %s
    """
    cursor.execute(query, (course_name, branch_name))
    
    result = cursor.fetchone()  
    cursor.fetchall() 

    cursor.close()
    connection.close()
    
    return result if result else (None, None)


def insert_user_data(fullname, phone_number, username, t_id, course_id, branch_id):
    connection = connection_pool.get_connection()
    cursor = connection.cursor()

    if username is None:
        username = ""
    query = """
        INSERT INTO users (full_name, phone, datetime, username, t_id, course_id, branch_id)
        VALUES (%s, %s, NOW(), %s, %s, %s, %s)
    """
    cursor.execute(query, (fullname, phone_number, username, t_id, course_id, branch_id))
    connection.commit()
    cursor.close()
    connection.close()


async def registration_fullname(message: Message, state: FSMContext):
    data = await state.get_data()
    translations = translate_into("./user_side/translations/registration_translations.json", data, "registration_messages")

    await message.answer(
        text=translations["enter_fullname"], 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ProcessTrack.fullname)

async def registration_phone_number(message: Message, state: FSMContext):
    data = await state.get_data()
    translations = translate_into("./user_side/translations/registration_translations.json", data, "registration_messages")

    if len(message.text.split()) == 2:
        await state.update_data(fullname=message.text)
        await message.answer(text=translations["enter_phone"])
        await state.set_state(ProcessTrack.phone_number)
    else:
        await message.answer(text=translations["fullname_error"])

import re

def phone_number_answer(phone_number):
    # Regex qoidasi
    uz_phone_regex = r'\d{9}$'
    # Tekshirish
    return bool(re.match(uz_phone_regex, phone_number))


async def registration_verification(message: Message, state: FSMContext):
    data = await state.get_data()
    translations = translate_into("./user_side/translations/registration_translations.json", data, "registration_messages")

    if phone_number_answer(message.text):
        await state.update_data(phone_number=message.text)
        data = await state.get_data()

        info_text = (f"{translations['confirm_info']}\n"
                     f"{translations['fullname']}: {data.get('fullname')}\n"
                     f"{translations['phone_number']}: {data.get('phone_number')}\n"
                     f"{translations['course']}: {data.get('course_name')}\n"
                     f"{translations['branch']}: {data.get('branch_name')}")

        await message.answer(info_text, reply_markup=get_confirmation_keyboard(data))
    else:
        await message.answer(translations["invalid_phone"])

async def send_info_to_admins(message: Message, state: FSMContext):
    data = await state.get_data()
    translations = translate_into("./user_side/translations/registration_translations.json", data, "entry_labels")
    
    course_id, branch_id = get_course_and_branch_ids(data.get("course_name"), data.get("branch_name"))
    
    if not course_id or not branch_id:
        await message.answer(translations["course_or_branch_not_found"])
        return
    
    insert_user_data(
        data.get("fullname"),
        data.get("phone_number"),
        message.from_user.username,
        message.from_user.id,
        course_id,
        branch_id
    )
    
    info_text = (f"{translations['new_registration']}\n"
                 f"{translations['fullname']}: {data.get('fullname')}\n"
                 f"{translations['phone_number']}: {data.get('phone_number')}\n"
                 f"{translations['course']}: {data.get('course_name')}\n"
                 f"{translations['branch']}: {data.get('branch_name')}")

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, info_text)
        except Exception as e:
            print(f"Xatolik yuz berdi admin bilan aloqa o'rnatishda: {e}")
    
    await message.answer(translations["sent_to_admins"])
    

    data1 = await state.get_data()
    await state.clear()

    if curr_language:=data1.get("current_language"): 
        if curr_language in ['russian', 'english', 'uzbek']:
            language = curr_language
    else:
        if message.text == '🇷🇺 Ru': language = 'russian'
        elif message.text == '🇺🇸 Eng': language = 'english'
        elif message.text == '🇺🇿 Uz': language = 'uzbek' 
        else: language = 'uzbek'

    await state.update_data(current_language = language)
    data2 = await state.get_data()
    await message.answer(translate_into("./user_side/translations/entry_translations.json", data2, "entry_labels"), reply_markup=get_entry_keyboard(data2))
    await state.set_state(ProcessTrack.chosen_menu)