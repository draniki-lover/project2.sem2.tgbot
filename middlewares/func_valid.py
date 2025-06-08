from aiogram import types
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any, Awaitable
import re
from states.state import Form


class FunctionValidatorMiddleware:
    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get('state')

        if state and await state.get_state() == Form.waiting_function_input.state:
            user_input = message.text.strip()

            if user_input == "Назад":
                return await handler(message, data)

            if not user_input:
                await message.answer("❌ Введи функцию, строка не может быть пустой")
                return

            if not self._validate_symbols(user_input):
                await message.answer(
                    "❌ Функция содержит недопустимые символы.\n"
                    "Разрешены: буквы, цифры, +-*/^()= и математические функции"
                )
                return

            if not self._validate_structure(user_input):
                await message.answer(
                    "❌ Неверный формат функции.\n"
                    "Примеры:\n"
                    "• y = x^2 + 3x - 5\n"
                    "• f(x) = sin(x)*cos(x)\n"
                    "• sqrt(x) + 1"
                )
                return

        return await handler(message, data)

    def _validate_symbols(self, text: str) -> bool:
        allowed = r"^[a-zA-Z0-9\s\^\.\+\-\*\/\(\)=\√π∞sin costan expln logabs]+$"
        return re.match(allowed, text) is not None

    def _validate_structure(self, text: str) -> bool:
        patterns = [
            r'^[yY]\s*=\s*.+$',
            r'^[fF]\([xX]\)\s*=\s*.+$',
            r'^[a-zA-Z]+\s*\(.+\)$',
            r'^[a-zA-Z0-9\+\-\*\/\^\(\)=\s]+$'
        ]
        return any(re.match(p, text) for p in patterns)