from aiogram import Bot, Dispatcher, F
from asyncio import run 
from MyToken import API_TOKEN # Your API token


from aiogram.types import BotCommand
from aiogram.filters import Command
from user_side.functions.greetings import start_command_answer
from user_side.functions.main_section import main_section_function, courses_function
from  user_side.functions.callback_functions import next_action, prev_action, home_action
from user_side.states.process_track_state import ProcessTrack

dp = Dispatcher()

# main dasturni yurgazuvchi funksiya
async def main():
	bot = Bot(token = API_TOKEN)
	# Marjona Sultonova
	dp.message.register(start_command_answer, Command("start"))
	dp.message.register(main_section_function, ProcessTrack.current_language)

	#Begzod Turdibekov
	dp.message.register(courses_function, F.text == 'Kurslar')
	dp.callback_query.register(next_action, F.data =='next')
	dp.callback_query.register(prev_action, F.data == 'prev')
	dp.callback_query.register(home_action, F.data =='home')

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