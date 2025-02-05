from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
button_1 = KeyboardButton(text = "bugun otkanlar")
button_2 = KeyboardButton(text ="To'liq xisobot")
button_3 = KeyboardButton(text ="kurslar")
button_4 = KeyboardButton(text ="filiallar")
button_5 = KeyboardButton(text ="yangilik jo'natish")
button_6 = KeyboardButton(text ="viloyat")
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            button_1, button_2
        ],
        [
            button_3, button_4
        ],
        [
            button_5, button_6
        ]
    ],
    resize_keyboard = True

)
button_7 = KeyboardButton(text="tasdiqlash ✅")
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