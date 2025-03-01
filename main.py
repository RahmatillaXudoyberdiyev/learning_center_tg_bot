# Asosiy funksiyalar
from aiogram import Bot, Dispatcher
from asyncio import run 
from aiogram.types import BotCommand
import logging
import user_side
import admin_panel

from config import API_TOKEN # Sizning API tokeningiz

dp = Dispatcher()

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',  # Loglar saqlanadigan fayl nomi
    filemode='a'  # 'a' - qo'shib yozish, 'w' - har safar yangidan yozish
)

# Logger obyektini yaratish
logger = logging.getLogger(__name__)

# main dasturni yurgazuvchi funksiya
async def main():
	"""Telegram botni ishga tushirish va sozlash.

    Ushbu funksiya API token yordamida botni ishlatadi, admin va foydalanuvchi
    routerlarini ulaydi, maxsus bot buyruqlarini ro'yxatga oladi va yangilanishlarni
    polling qilishni boshlaydi.
    """
	bot = Bot(token = API_TOKEN)

	dp.include_router(admin_panel.dp)
	dp.include_router(user_side.dp)


	await bot.set_my_commands([
		BotCommand(command="/start", description="Botni ishga tushirish"),
		BotCommand(command="/lang", description="Tilni o'zgartirish")
	])
# __________
	await dp.start_polling(bot, skip_updates = True)

if __name__ == '__main__':
	logger.info("Bot ishga tushdi!")
	run(main())

# Logs:
# Rahmatilla Xudoyberdiyev changed
# Stop function is removed by Rahmatilla Xudoyberdiyev