from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_side.translations.translation_functions import translate_into

def get_confirmation_keyboard(data):
    translations = translate_into("./user_side/translations/registration_translations.json", data, "confirmation_buttons")

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["confirm"]),
                KeyboardButton(text=translations["restart"])
            ]
        ],
        resize_keyboard=True
    )
