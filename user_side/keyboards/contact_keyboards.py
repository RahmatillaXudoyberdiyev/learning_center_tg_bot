from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_side.translations.translation_functions import translate_into

# Marjona Sultonova
# Aloqaga chiqish
def get_contact_keyboard(data):
    translations = translate_into("./user_side/translations/contact_translations.json", data, "contact_buttons")

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["contact"]),
                KeyboardButton(text=translations["home"])
            ]
        ],
        resize_keyboard=True
    )
