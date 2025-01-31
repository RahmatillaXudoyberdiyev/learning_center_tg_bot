from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from user_side.functions.main_section import create_course_list_buttons
from user_side.keyboards.language_keyboards import language_button
from user_side.states.process_track_state import ProcessTrack

#Begzod Turdibekov
# Info: inline buttonda "Next" qiymati bosilganda bajariladigan funksiya
async def next_action(callBackData : CallbackQuery, state : FSMContext):
    data = await state.get_data()
    position = data['course_button_position']
    await callBackData.message.edit_reply_markup(reply_markup= await create_course_list_buttons(button_list = data['course_list'], position = position + 1, state=state))

    await state.update_data(course_button_position = position + 1)

#Begzod Turdibekov
# Info: inline buttonda "Prev" qiymati bosilganda bajariladigan funksiya
async def prev_action(callBackData : CallbackQuery, state : FSMContext):
    data = await state.get_data()
    position = data['course_button_position']
    await callBackData.message.edit_reply_markup(reply_markup= await create_course_list_buttons(button_list=data['course_list'], position=position - 1, state = state))

    await state.update_data(course_button_position = position - 1)

#Begzod Turdibekov
# Info: inline buttonda "Home" qiymati bosilganda bajariladigan funksiya
async def home_action(callBackData : CallbackQuery, state : FSMContext):
    await callBackData.message.answer("Assalomu aleykum, iltimos tilni tanlang:", reply_markup=language_button)
    await state.clear() # Barcha malumotlarni tozalab tashladim.
    await state.set_state(ProcessTrack.current_language) # Til tanlash state i faollashdi.