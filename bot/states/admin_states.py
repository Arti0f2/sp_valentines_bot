# bot/states/admin_states.py
from aiogram.fsm.state import State, StatesGroup

class ManualTopupStates(StatesGroup):
    waiting_screenshot = State()