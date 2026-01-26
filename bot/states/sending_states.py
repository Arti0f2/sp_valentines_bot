# bot/states/sending_states.py
from aiogram.fsm.state import State, StatesGroup

class SendingStates(StatesGroup):
    waiting_recipient = State()
    waiting_message = State()
    waiting_confirmation = State()