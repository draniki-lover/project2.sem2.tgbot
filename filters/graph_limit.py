from aiogram import types
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext

from states.state import Form
import asyncio


class GraphRateLimiter(BaseMiddleware):
    def __init__(self):
        self.rate_limit = 5
        self.period = timedelta(minutes=1)
        self.user_requests = {}

    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data['state']

        if await state.get_state() != Form.waiting_function_input:
            return await handler(message, data)

        user_id = message.from_user.id
        now = datetime.now()

        self._cleanup_old_requests(user_id, now)

        if len(self.user_requests.get(user_id, [])) >= self.rate_limit:
            next_request_time = self._get_next_request_time(user_id)
            wait_time = (next_request_time - now).seconds
            await message.answer(
                f"⚠️ Слишком много запросов. Подождите {wait_time} секунд "
                f"перед следующим построением графика.\n"
                f"Лимит: {self.rate_limit} запросов в минуту."
            )
            return

        if user_id not in self.user_requests:
            self.user_requests[user_id] = []
        self.user_requests[user_id].append(now)

        return await handler(message, data)

    def _cleanup_old_requests(self, user_id: int, now: datetime):
        if user_id in self.user_requests:
            self.user_requests[user_id] = [
                t for t in self.user_requests[user_id]
                if now - t < self.period
            ]

    def _get_next_request_time(self, user_id: int) -> datetime:
        oldest_request = min(self.user_requests[user_id])
        return oldest_request + self.period