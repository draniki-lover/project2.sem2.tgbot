from aiogram import types
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from states.state import Form


class EmptyFunctionCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data['state']
        if await state.get_state() == Form.waiting_function_input:
            if not message.text or not message.text.strip():
                await message.answer(
                    "❌ Ты ввел пустую строку. Пожалуйста, введи функцию.\n"
                    "Примеры:\n"
                    "• y = x^2 + 3x - 5\n"
                    "• f(x) = sin(x) * cos(x)\n"
                    "• y = sqrt(x) + 1"
                )
                return
        return await handler(message, data)
