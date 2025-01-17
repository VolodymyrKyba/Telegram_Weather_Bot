from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from handlers import router
from config import BOT_TOKEN

bot  = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")