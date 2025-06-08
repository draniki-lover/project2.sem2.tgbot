import json
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F

from services.storage_serv import GraphStorage

router = Router()


@router.message(Command("delete"))
async def delete_history(message: types.Message):
    storage = GraphStorage()

    # Очищаем файл с данными
    with open(storage.data_file, 'w') as f:
        json.dump({}, f)

    # Удаляем все файлы графиков из директории
    for file in storage.storage_dir.glob("*.png"):
        try:
            file.unlink()
        except OSError as e:
            print(f"Ошибка при удалении файла {file}: {e}")

    await message.answer("История графиков успешно очищена.")