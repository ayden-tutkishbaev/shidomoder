from typing import Dict, Awaitable, Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from keyboards import inline as il

from dotenv import dotenv_values

dotenv = dotenv_values(".env")

CHANNEL_ID = int(dotenv['CHANNEL_LINK'])


class CheckSubscription(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        member = await event.bot.get_chat_member(CHANNEL_ID, event.from_user.id)

        if member.status == 'left':
            await event.answer("Подпишитесь на канал перед тем, как начать использовать бота",
                               reply_markup=il.subscription_button)
        else:
            return await handler(event, data)