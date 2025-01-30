from aiogram import Bot, Dispatcher
from asyncio import run 
from MyToken import API_TOKEN # Your API token

# Marjona Sultonova
from user_side.functions.greetings import start_command_answer
from aiogram.types import BotCommand
from aiogram.filters import Command
#_____________

dp = Dispatcher()

# main dasturni yurgazuvchi funksiya
async def main():
	bot = Bot(API_TOKEN)
# Marjona Sultonova
	dp.message.register(start_command_answer, Command("start"))

	await bot.set_my_commands([
		BotCommand(command="/start", description="Botni ishga tushirish")
	])
# __________
	await dp.start_polling(bot, skip_updates = True)

if __name__ == '__main__':
	run(main())

# Logs:
# Rahmatilla Xudoyberdiyev changed
# Stop function is removed by Rahmatilla Xudoyberdiyev