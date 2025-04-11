import aiohttp
import asyncio


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  # Проверка на ошибки HTTP
            return await response.json()


async def parse_data(data):
    # Извлекаем данные о секьюрите
    market_data = data.get('marketdata', {}).get('data', [])
    if market_data:
        market_info = market_data[0]
        current_value = market_info[4]  # Текущая цена
        return current_value
    return None


async def get_imoex_data(url):
    try:
        data = await fetch_data(url)
        current_value = await parse_data(data)
        return current_value
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


async def main():
    url = "https://iss.moex.com/iss/engines/stock/markets/index/boards/SNDX/securities/IMOEX.json"
    current_price = await get_imoex_data(url)
    if current_price is not None:
        print(f"Текущая цена IMOEX: {current_price}")
    else:
        print("Не удалось получить текущую цену.")


if __name__ == "__main__":
    asyncio.run(main())
