from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_button = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="Uz"),
            KeyboardButton(text="Eng"),
            KeyboardButton(text="Ru")
            
        ]      
    ],
    resize_keyboard=True
)