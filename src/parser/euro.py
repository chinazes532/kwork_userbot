import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch_eur_rub():
    url = "https://ru.investing.com/currencies/eur-rub?ysclid=m9gwahzj3e644035753"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html


def parse_eur_rub(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_div = soup.find("div", {"data-test": "instrument-price-last"})
    if price_div:
        return round(float(price_div.text.replace(',', '.')), 2)
    return None


async def get_eur_rub_price():
    html = await fetch_eur_rub()
    price = parse_eur_rub(html)
    return price


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    price = loop.run_until_complete(get_eur_rub_price())
    print(f"Курс евро к рублю: {price} руб.")



# import aiohttp
# import pandas as pd
# from io import StringIO
#
#
# async def fetch_currency_data(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 return await response.text()
#             else:
#                 print(f"Ошибка при получении данных: {response.status}")
#                 return None
#
#
# async def get_euro_rate():
#     url = "https://www.fontanka.ru/currency.html"
#     html_content = await fetch_currency_data(url)
#     if html_content:
#         df = pd.read_html(StringIO(html_content))[0]
#         euro_data = df.loc[df['Валюта'].str.lower() == 'eur', ['Курс']]
#         if not euro_data.empty:
#             return euro_data.iloc[0, 0]
#     return None
#
