# bot/states/registration_states.py
from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()