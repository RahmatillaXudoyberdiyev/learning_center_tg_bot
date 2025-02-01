from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Xudoyberdiyev Rahmatilla
menu_buttons = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="Kurslar"),
            KeyboardButton(text="Biz haqimizda")
        ]      
    ],
    resize_keyboard=True
)

# Begzod Turdibekov
# Info : Kurlar ro'yxati tushganda "
registration_back_button = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = "Ro'yxatdan o'tish"),
            KeyboardButton(text = "Kurslar")
        ]
    ],
    resize_keyboard = True
)