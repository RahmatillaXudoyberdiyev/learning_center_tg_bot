from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
button_1 = KeyboardButton(text = "Bugun o'tganlar")
button_2 = KeyboardButton(text = "To'liq hisobot")
button_3 = KeyboardButton(text = "⚙ Manage")
button_4 = KeyboardButton(text = "Yangilik jo'natish")
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            button_1, button_2
        ],
        [
            button_3, button_4
        ]
    ],
    resize_keyboard = True

)
button_7 = KeyboardButton(text="Tasdiqlash ✅")
button_8 = KeyboardButton(text="❌ Bekor qilish")
keyboard1 = ReplyKeyboardMarkup(
    keyboard=[
        [
           button_7,button_8 
        ]
    ],
    resize_keyboard=True
)

def get_keyboard():
    return keyboard
def send_get_keyboard():
    return keyboard1