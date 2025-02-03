from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.fsm.context import  FSMContext

# Begzod Turdibekov
# Info : Kelayotgan habar most kurslarda borligini tekshirish

class check_in_course(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        data = await state.get_data() # ma'lumotlar yuklab olinyapti.
        if data.get('course_list'):
            for value in data['course_list']:
                if value[0] == message.text:
                    return True
        return False

# Begzod Turdibekov
# Info : Kelayotgan habarni mos viloyatlar ichida bor yo'qligini tekshirish
class check_in_region(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        data = await state.get_data() # ma'lumotlar yuklab olinyapti
        if data.get('region_list'):
            for value in data['region_list']:
                if value[0] == message.text:
                    return True
        return False

# Begzod Turdibekov
# Info : Kelayotgan habarni mos filyallar ichida bormi yo'qligini tekshirish
class check_in_branch(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        data = await state.get_data() # ma'lumotlar yuklab olinyapti
        if data.get('branch_list'):
            for value in data['branch_list']:
                if value[0] == message.text:
                    return True
        return False