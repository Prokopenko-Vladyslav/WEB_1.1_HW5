import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta


async def fetch_exchange_rate(session, date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}"
    async with session.get(url) as response:
        if response.status != 200:
            return {date.strftime('%d.%m.%Y'): 'Error fetching data'}
        data = await response.json()
        rates = data.get('exchangeRate', [])
        rate_dict = {}
        for rate in rates:
            if rate.get('currency') in ['USD', 'EUR']:
                rate_dict[rate['currency']] = {
                    'sale': rate.get('saleRate', 'N/A'),
                    'purchase': rate.get('purchaseRate', 'N/A')
                }
        return {date.strftime('%d.%m.%Y'): rate_dict}


async def main(days):
    if days < 1 or days > 10:
        print("Please specify a number of days between 1 and 10.")
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        start_date = datetime.now() - timedelta(days=days-1)
        for i in range(days):
            date = start_date + timedelta(days=i)
            tasks.append(fetch_exchange_rate(session, date))

        results = await asyncio.gather(*tasks)
        print(results)

if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python main.py <number_of_days>")
    else:
        days = int(sys.argv[1])
        asyncio.run(main(days))
