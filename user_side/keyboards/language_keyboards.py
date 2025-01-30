from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Marjona Sultonova
language_button = ReplyKeyboardMarkup(
    keyboard= [
        [
        # Emojilar oldinga o'tkazildi
            KeyboardButton(text="🇺🇿 Uz"),
            KeyboardButton(text="🇺🇸 Eng"),
            KeyboardButton(text="🇷🇺 Ru")
            
        ]      
    ],
    resize_keyboard=True
)