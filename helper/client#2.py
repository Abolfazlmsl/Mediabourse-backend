import websockets
from datetime import datetime
import asyncio

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year


async def hello():

    uri = "ws://192.168.0.155:8002"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                greeting = await websocket.recv()
                print(f"I am Client #2. Data : {greeting}")
            except Exception as e:
                print('Server disconnected', e)
                print('Try to reconnect')
                websocket = await websockets.connect(uri)

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
