# bot/states/sending_states.py
from aiogram.fsm.state import State, StatesGroup

class SendValentineStates(StatesGroup):
    recipient_username = State() 
    message_text = State()       
    delivery_slot = State() 