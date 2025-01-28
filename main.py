from aiogram import Bot, Dispatcher
from asyncio import run 
from MyToken import API_TOKEN # Your API token

dp = Dispatcher()

# main dasturni yurgazuvchi funksiya
async def main():
	bot = Bot(API_TOKEN)

	await dp.start_polling(bot, skip_updates = True)

if __name__ == '__main__':
	run(main())

# Logs:
# Rahmatilla Xudoyberdiyev changed