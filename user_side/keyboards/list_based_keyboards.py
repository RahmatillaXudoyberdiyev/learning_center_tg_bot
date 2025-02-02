from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Begzod Turdibekov
# Info : Kurlar ro'yxati tushganda 
registration_back_button = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = "✍️ Ro'yxatdan o'tish"),
            KeyboardButton(text = "Ortga")
        ]
    ],
    resize_keyboard = True
)