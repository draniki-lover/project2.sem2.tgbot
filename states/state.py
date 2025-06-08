from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    waiting_communication_style = State()
    waiting_graph_type = State()
    waiting_function_input = State()
    waiting_standard_choice = State()