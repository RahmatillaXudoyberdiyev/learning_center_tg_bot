from tkinter.constants import FALSE

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from admin_panel.states.process_track_state import ProcessTrack

class check_admin_state(Filter):
    async def __call__(self, message : Message, state : FSMContext):
        current_state = await state.get_state()

        if current_state == ProcessTrack.chosen_menu:
            return True

        if current_state == ProcessTrack.todays_list:
            return True
        if current_state == ProcessTrack.full_list:
            return True
        if current_state == ProcessTrack.courses:
            return True
        if current_state == ProcessTrack.regions:
            return True
        if current_state == ProcessTrack.add_region:
            return True
        if current_state == ProcessTrack.add_region_name:
            return True

        if current_state == ProcessTrack.region_chosen:
            return True

        if current_state == ProcessTrack.branches:
            return True
        if current_state == ProcessTrack.send_news:
            return True
        return False