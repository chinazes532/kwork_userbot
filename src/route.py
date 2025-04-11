import os
import logging

from telethon import TelegramClient, events
from dotenv import load_dotenv

from src.parser import get_course_crypto, get_euro_rate,get_imoex_data


load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_id = os.getenv("CHANNEL_ID")

client = TelegramClient('userbot', int(api_id), api_hash)

logging.basicConfig(level=logging.INFO)


@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Привет!\nДанный бот является небольшим пет-проектом")


@client.on(events.NewMessage(pattern="/edit"))
async def edit(event):
    btc_course = await get_course_crypto("bitcoin")
    eth_course = await get_course_crypto("ethereum")
    usd_course = await get_course_crypto("tether")
    ton_course = await get_course_crypto("the-open-network")
    euro_course = await get_euro_rate()
    imoex = await get_imoex_data()
    try:
        await client.edit_message(int(channel_id),
                                  117,
                                  f"Курс BTC: {btc_course}\n"
                                  f"Курс ETH: {eth_course}\n"
                                  f"Курс USDT: {usd_course}\n"
                                  f"Курс TON: {ton_course}\n"
                                  f"Курс EUR: {euro_course}\n"
                                  f"Курс IMOEX: {imoex}")
        logging.info("Сообщение успешно изменено.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


async def edit_message_in_channel():
    btc_course = await get_course_crypto("bitcoin")
    eth_course = await get_course_crypto("ethereum")
    usd_course = await get_course_crypto("tether")
    ton_course = await get_course_crypto("the-open-network")
    euro_course = await get_euro_rate()
    url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
    imoex = await get_imoex_data(url)
    try:
        await client.edit_message(int(channel_id),
                                  117,
                                  f"Курс BTC: {btc_course}\n"
                                  f"Курс ETH: {eth_course}\n"
                                  f"Курс USDT: {usd_course}\n"
                                  f"Курс TON: {ton_course}\n"
                                  f"Курс EUR: {euro_course}\n"
                                  f"Курс IMOEX: {imoex}")
        logging.info("Сообщение успешно изменено.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")




