import asyncio
import logging
import sys

from dotenv import dotenv_values

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import admins, group, chat

from database.queries import *
from middleware import CheckSubscription

config = dotenv_values(".env")


async def main() -> None:
    await async_main()
    dp = Dispatcher()
    dp.message.middleware(CheckSubscription())
    await add_data()
    bot = Bot(token=config['BOT_TOKEN'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(
        admins.rt,
        chat.rt,
        group.rt
    )
    # Запускаем aiogram polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("THE BOT IS OFF")