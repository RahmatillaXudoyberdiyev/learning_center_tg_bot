from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_side.translations.translation_functions import translate_into

#Xudoyberdiyev Rahmatilla
def get_entry_keyboard(data):
    translations = translate_into("./user_side/translations/entry_translations.json", data, "entry_buttons")
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["courses"]),
                KeyboardButton(text=translations["about_us"])
            ]
        ],
        resize_keyboard=True
    )


