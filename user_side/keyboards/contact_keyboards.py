from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Marjona Sultonova
# Aloqaga chiqish

contact_button = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "📞 Aloqaga chiqish"),
            KeyboardButton(text = "🏠 Bosh sahifaga qaytish")
        ]

    ],
    resize_keyboard = True
    

)