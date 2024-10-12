from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [7215866709]


class IsPrivateChat(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == 'private'


class IsGroupChat(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ['group', 'supergroup']

class CallGroupChat(Filter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.message.chat.type in ['group', 'supergroup']