from aiogram import Router, types
from aiogram.filters import Command

from services.storage_serv import GraphStorage

router = Router()

@router.message(Command("history"))
async def show_history(message: types.Message):
    storage = GraphStorage()
    graph_data = storage.load_data()

    if not graph_data:
        await message.answer("История графиков пуста.")
        return

    response = "История построенных графиков:\n\n"
    for i, (formula, path) in enumerate(graph_data.items(), 1):
        response += f"{i}. {formula}\n"

    await message.answer(response)

    last_formula = list(graph_data.keys())[-1]
    last_path = graph_data[last_formula]

    with open(last_path, 'rb') as f:
        await message.answer_photo(
            types.BufferedInputFile(
                file=f.read(),
                filename="last_graph.png"
            ),
            caption=f"Последний график: {last_formula}"
        )