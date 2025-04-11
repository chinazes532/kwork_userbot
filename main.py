import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.route import client, edit_message_in_channel


logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()


async def main():
    await client.start()
    logging.info("User bot started.")
    scheduler.add_job(edit_message_in_channel, 'interval', minutes=2)
    scheduler.start()
    try:
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        logging.info("User bot stopped.")


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
