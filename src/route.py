import os
import logging

from telethon import TelegramClient, events
from dotenv import load_dotenv
from telethon.extensions import markdown
from telethon.tl import types
from telethon.tl.types import MessageEntityCustomEmoji

from src.parser import get_course_crypto, get_eur_rub_price, get_imoex_data, get_course_crypto_usd

from src.database.requests.first_message.add import set_first_message
from src.database.requests.first_message.select import get_first_message
from src.database.requests.second_message.add import set_second_message
from src.database.requests.second_message.select import get_second_message

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
channel_id = os.getenv("CHANNEL_ID")
channel_id_2 = os.getenv("CHANNEL_ID_2")

client = TelegramClient('userbot', int(api_id), api_hash)


class CustomMarkdown:
    @staticmethod
    def parse(text):
        text, entities = markdown.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return markdown.unparse(text, entities)


client.parse_mode = CustomMarkdown()
logging.basicConfig(level=logging.INFO)


@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Бот успешно запущен и готов к работе!")


# @client.on(events.NewMessage())
# async def get_premium(event):
#     # Check if the message contains entities
#     if event.message.entities:
#         for entity in event.message.entities:
#             # Check if the entity is a custom emoji
#             if isinstance(entity, MessageEntityCustomEmoji):
#                 print(f'Found custom emoji with document_id: {entity.document_id}')
#                 # Optionally, you can also send a message back with the document_id
#                 await event.respond(f'Custom emoji found with document_id: {entity.document_id}')


@client.on(events.NewMessage(pattern="/test"))
async def test(event):
    btc_course = await get_course_crypto_usd("bitcoin")
    eth_course = await get_course_crypto_usd("ethereum")
    usd_course = await get_course_crypto("tether")
    ton_course = await get_course_crypto_usd("the-open-network")
    euro_course = await get_eur_rub_price()
    url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
    imoex = await get_imoex_data(url)

    await event.reply(f"[️1️⃣](emoji/5382310654361233675) {usd_course}₽ [2️⃣](emoji/5382128036646770366) {euro_course}₽ "
                      f"[3️⃣](emoji/5381803053651357419) {imoex}\n\n"
                      f"[4️⃣](emoji/5382320541375947661) {btc_course}$ [5️⃣](emoji/5382255700254681367) {eth_course}$ "
                      f"[6️⃣](emoji/5382294333485510537) {ton_course}$")


@client.on(events.NewMessage(pattern="/send_1"))
async def send_1(event):
    try:
        first_message_db = await get_first_message(1)
        print(first_message_db)
        if first_message_db:
            await event.reply("Сообщение уже есть в закрепе")
            return

        btc_course = await get_course_crypto_usd("bitcoin")
        eth_course = await get_course_crypto_usd("ethereum")
        usd_course = await get_course_crypto("tether")
        ton_course = await get_course_crypto_usd("the-open-network")
        euro_course = await get_eur_rub_price()
        url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
        imoex = await get_imoex_data(url)

        first_message = await client.send_message(int(channel_id),
                                                  f"[️1️⃣](emoji/5382310654361233675) {usd_course}₽ [2️⃣](emoji/5382128036646770366) {euro_course}₽ "
                      f"[3️⃣](emoji/5381803053651357419) {imoex}\n\n"
                      f"[4️⃣](emoji/5382320541375947661) {btc_course}$ [5️⃣](emoji/5382255700254681367) {eth_course}$ "
                      f"[6️⃣](emoji/5382294333485510537) {ton_course}$")

        first_id = first_message.id
        await set_first_message(first_id)
        await event.reply("Сообщение было успешно отправлено.")
        logging.info("Сообщение успешно отправлено.")
    except Exception as e:
        logging.error(f"Произошла ошибка при отправке сообщения: {str(e)}")
        await event.reply("Произошла ошибка при отправке сообщения.")


async def edit_message_in_channel():
    try:
        btc_course = await get_course_crypto_usd("bitcoin")
        eth_course = await get_course_crypto_usd("ethereum")
        usd_course = await get_course_crypto("tether")
        ton_course = await get_course_crypto_usd("the-open-network")
        euro_course = await get_eur_rub_price()
        url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
        imoex = await get_imoex_data(url)

        first_message = await get_first_message(1)

        await client.edit_message(int(channel_id),
                                  first_message.message_id,
                                  f"[️1️⃣](emoji/5382310654361233675) {usd_course}₽ [2️⃣](emoji/5382128036646770366) {euro_course}₽ "
                      f"[3️⃣](emoji/5381803053651357419) {imoex}\n\n"
                      f"[4️⃣](emoji/5382320541375947661) {btc_course}$ [5️⃣](emoji/5382255700254681367) {eth_course}$ "
                      f"[6️⃣](emoji/5382294333485510537) {ton_course}$")
        logging.info("Сообщение успешно изменено.")
    except Exception as e:
        logging.error(f"Произошла ошибка при изменении сообщения: {str(e)}")


@client.on(events.NewMessage(pattern="/send_2"))
async def send_2(event):
    try:
        second_message_db = await get_second_message(1)
        if second_message_db:
            await event.reply("Сообщение уже есть в закрепе")
            return

        btc_course = await get_course_crypto_usd("bitcoin")
        eth_course = await get_course_crypto_usd("ethereum")
        usd_course = await get_course_crypto("tether")
        ton_course = await get_course_crypto_usd("the-open-network")
        euro_course = await get_eur_rub_price()
        url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
        imoex = await get_imoex_data(url)

        second_message = await client.send_message(int(channel_id_2),
                                                  f"[️1️⃣](emoji/5382310654361233675) {usd_course}₽ [2️⃣](emoji/5382128036646770366) {euro_course}₽ "
                      f"[3️⃣](emoji/5381803053651357419) {imoex}\n\n"
                      f"[4️⃣](emoji/5382320541375947661) {btc_course}$ [5️⃣](emoji/5382255700254681367) {eth_course}$ "
                      f"[6️⃣](emoji/5382294333485510537) {ton_course}$")

        second_id = second_message.id

        await set_second_message(second_id)
        await event.reply("Сообщение было успешно отправлено.")
        logging.info("Сообщение успешно отправлено 2.")
    except Exception as e:
        logging.error(f"Произошла ошибка при отправке сообщения 2: {str(e)}")
        await event.reply("Произошла ошибка при отправке сообщения.")


async def edit_message_in_channel_2():
    try:
        btc_course = await get_course_crypto_usd("bitcoin")
        eth_course = await get_course_crypto_usd("ethereum")
        usd_course = await get_course_crypto("tether")
        ton_course = await get_course_crypto_usd("the-open-network")
        euro_course = await get_eur_rub_price()
        url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
        imoex = await get_imoex_data(url)
        second_message = await get_second_message(1)

        await client.edit_message(int(channel_id_2),
                                  second_message.message_id,
                                  f"[️1️⃣](emoji/5382310654361233675) {usd_course}₽ [2️⃣](emoji/5382128036646770366) {euro_course}₽ "
                      f"[3️⃣](emoji/5381803053651357419) {imoex}\n\n"
                      f"[4️⃣](emoji/5382320541375947661) {btc_course}$ [5️⃣](emoji/5382255700254681367) {eth_course}$ "
                      f"[6️⃣](emoji/5382294333485510537) {ton_course}$")
        logging.info("Сообщение успешно изменено.")
    except Exception as e:
        logging.error(f"Произошла ошибка при изменении сообщения: {str(e)}")
