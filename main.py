import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.database.models import create_db
from src.route import client, edit_message_in_channel, edit_message_in_channel_2


logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()


async def main():
    await client.start()
    await create_db()
    logging.info("User bot started.")
    scheduler.add_job(edit_message_in_channel, 'interval', minutes=2)
    scheduler.add_job(edit_message_in_channel_2, 'interval', minutes=3)
    scheduler.start()
    try:
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        logging.info("User bot stopped.")


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
