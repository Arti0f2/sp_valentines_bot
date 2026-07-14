# bot/states/admin_states.py
from aiogram.fsm.state import State, StatesGroup

class ManualTopupStates(StatesGroup):
    # адмін накладає скриншот доказу наданого монета
    waiting_screenshot = State()