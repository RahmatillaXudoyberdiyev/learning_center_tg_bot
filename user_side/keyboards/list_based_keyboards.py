from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Begzod Turdibekov
# Info : Kurlar ro'yxati tushganda 
registration_back_button = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = "⏮ Ortga qaytish"),
            KeyboardButton(text = "✍️ Ro'yxatdan o'tish")

        ],
        [KeyboardButton(text = "🏠 Bosh sahifaga qaytish")]
    ],
    resize_keyboard = True
)