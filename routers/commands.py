from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram import types, Router

from keyboards import inlines
from states.state import Form

router = Router()

@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.waiting_communication_style)
    await message.answer(f"{message.chat.full_name}, привет👋!\n"
                         "Это бот, который поможет тебе грамотно строить графики🌝\n"
                         "Нажми /help, если хочешь ближе ознакомиться с возможностями бота.\n"
                         "Что называется, let's try!!!",
                         reply_markup=inlines.start_kb())

@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer(f"{message.chat.full_name}, вот список команд, реализованных в этом боте:\n"
                         "- /about, чтобы узнать подробнее о проекте: сути, его полезности✍️,\n"
                         "- /start, чтобы начать коммуникацию с ботом заново🙌,\n"
                         "- /history, чтобы увидеть, какие графики были уже построены📐,\n"
                         "- /delete, чтобы очистить историю запущенных графиков."
                         )
