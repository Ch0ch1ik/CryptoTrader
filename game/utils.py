import asyncio
import json
import websockets

from game.models import CryptoCurrency


async def fetch_currency_data():
    uri = "wss://stream.coinmarketcap.com/price/latest"
    async with websockets.connect(uri) as websocket:
        request = {
            "method": "subscribe",
            "id": "price",
            "data": {
                "cryptoIds": ["1", "1027", "1839", "2010", "74", "1958", "1975", "1047", "512", "328"],
                "index": null
            }
        }
        await websocket.send(json.dumps(request))

        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if 'data' in data and data['id'] == 'price':
                currency_data = data['data']
                symbol = currency_data['cryptoSymbol']
                price = currency_data['quote']['USD']['price']
                currency, created = CryptoCurrency.objects.update_or_create(
                    symbol=symbol,
                    defaults={'price': price}
                )
                print(f'{currency.symbol} - {currency.price}')


async def start_fetching():
    while True:
        try:
            await fetch_currency_data()
        except:
            pass
        await asyncio.sleep(30)


async def connect():
    asyncio.create_task(start_fetching())
