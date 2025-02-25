from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_side.translations.translation_functions import translate_into

# Begzod Turdibekov
# Info: Kurslar ro'yxati tushganda
def get_registration_back_keyboard(data):
    translations = translate_into("./user_side/translations/list_based_translations.json", data, "registration_buttons")

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["back"]),
                KeyboardButton(text=translations["register"])
            ],
            [KeyboardButton(text=translations["home"])]
        ],
        resize_keyboard=True
    )
