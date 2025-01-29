from aiogram import Bot, Dispatcher
from asyncio import run 
from MyToken import API_TOKEN # Your API token

# Marjona Sultonova
from user_side.functions.start_stop import start_command_answer, stop_command_answer
from aiogram.types import BotCommand
from aiogram.filters import Command
#_____________

dp = Dispatcher()

# main dasturni yurgazuvchi funksiya
async def main():
	bot = Bot(API_TOKEN)
# Marjona Sultonova
	dp.message.register(start_command_answer, Command("start"))
	dp.message.register(stop_command_answer, Command("stop"))

	await bot.set_my_commands([
		BotCommand(command="/start", description="Botni ishga tushirish"),
		BotCommand(command="/stop", description="Bekor qilish")
	])
# __________
	await dp.start_polling(bot, skip_updates = True)

if __name__ == '__main__':
	run(main())

# Logs:
# Rahmatilla Xudoyberdiyev changed