import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.handlers import schedule
from aiogram import Bot, Dispatcher
from app.database.database import debug

from app.handlers import router, get_reminders
from app.database.database import init_db
async def main():
    init_db()
    debug()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    loop = asyncio.get_event_loop()
    loop.create_task(schedule(bot))
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutdown")


