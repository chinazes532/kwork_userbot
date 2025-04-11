import aiohttp
import pandas as pd
from io import StringIO


async def fetch_currency_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка при получении данных: {response.status}")
                return None


async def get_euro_rate():
    url = "https://www.fontanka.ru/currency.html"
    html_content = await fetch_currency_data(url)
    if html_content:
        df = pd.read_html(StringIO(html_content))[0]
        euro_data = df.loc[df['Валюта'].str.lower() == 'eur', ['Курс']]
        if not euro_data.empty:
            return euro_data.iloc[0, 0]
    return None

