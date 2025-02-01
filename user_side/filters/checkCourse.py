from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.fsm.context import  FSMContext

# Begzod Turdibekov
# Info : state 'course' ga teng bo'lganda, jo'natilgan xabar fanlar ichida bor mi yo'qmi.

class check_in_course(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        data = await state.get_data() # ma'lumotlar yuklab olinyapti.
        if data.get('state') and data['state'] == 'course': # tekshirivuchi Funksiya
            for value in data['course_list']:
                await state.update_data(course_name = message.text)
                if value[0] == message.text:
                    return True
        return False

# Begzod Turdibekov
# Info : state da 'region' qismi ishlab turganida, ishlash uchun
class check_in_region(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        data = await state.get_data() # ma'lumotlar yuklab olinyapti
        if data.get('state') and data['state'] == 'region':
            return True
        return False

# Begzod Turdibekov
# Info : state da 'course' bo'lsa faqat.

class check_in_course_back(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        data = await state.get_data() # ma'lumotlar yuklab olinyapti
        if data.get('state') and data['state'] == 'course':
            return True
        return False