from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from aiogram.fsm.context import FSMContext

from user_side.states.process_track_state import ProcessTrack
from user_side.keyboards.registration_keyboards import tastiqlash_tugmasi
from user_side.keyboards.entry_keyboards import menu_buttons

from config import ADMIN_IDS

async def registation_fullname(message: Message, state: FSMContext):
    await message.answer("Ro'yxatdan o'tish uchun ism-familiyangizni kiriting\nNamuna: Xoliyorova Munisa", reply_markup = ReplyKeyboardRemove())
    await state.set_state(ProcessTrack.fullname)

async def registation_phone_number(message: Message, state: FSMContext):
    if len(message.text.split()) == 2:
        await state.update_data(fullname=message.text)
        await message.answer("Telefon raqamingizni  kiriting\nNamuna: 995673412 ")
        await state.set_state(ProcessTrack.phone_number)
    else:
        await message.answer("Faqat ism va familiyangizni kiriting:")

import re

def phone_number_answer(phone_number):
    # Regex qoidasi
    uz_phone_regex = r'\d{9}$'
    # Tekshirish
    return bool(re.match(uz_phone_regex, phone_number))


async def registration_verification(message: Message, state: FSMContext):
    if phone_number_answer(message.text):
        await state.update_data(phone_number=message.text)
        data = await state.get_data()
        print(data)
        malumotlar = (f"Ma'lumotlaringizni tasdiqlang:\n"
                      f"Ism familiya: {data.get('fullname')}\n"
                      f"Telefon raqam: {data.get('phone_number')}\n"
                      f"Kurs: {data.get('course_name')}\n"
                      f"Fillial: {data.get('branch_name')}\n")
        await message.answer(malumotlar, reply_markup=tastiqlash_tugmasi)
    else:
        await message.answer("Iltimos, telefon raqamini to'g'ri formatda kiriting\nNa'muna: 997452346")

async def send_info_to_admins(message: Message, state: FSMContext):
    data = await state.get_data()
    malumotlar = (f"Yangi ro'yxatdan o'tgan foydalanuvchi ma'lumotlari:\n"
                  f"Ism familiya: {data.get('fullname')}\n"
                  f"Telefon raqam: {data.get('phone_number')}\n"
                  f"Kurs: {data.get('course_name')}\n"
                  f"Fillial: {data.get('branch_name')}\n")

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, malumotlar)
        except Exception as e:
            print(f"Xatolik yuz berdi admin bilan aloqa o'rnatishda: {e}")
    await message.answer("Adminlarga muvaffaqiyatli jo'naildi")
    await message.answer("Iltimos kerakli menuni tanlang:", reply_markup=menu_buttons)
    await state.clear()
    await state.set_state(ProcessTrack.chosen_menu)

