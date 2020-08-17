import asyncio
import websockets
import sys
import time


class Agent:
    def __init__(self):
        self.i = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(self.hello())
        asyncio.get_event_loop().run_forever()

    async def hello(self):
        uri = "ws://192.168.0.155:8002"
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    greeting = await websocket.recv()
                    print(f"I am Client #{self.i} and Data Received.")
                except Exception as e:
                    print('Server disconnected', e)
                    print('Try to reconnect')
                    websocket = await websockets.connect(uri)


print(f"Start agent {sys.argv[1]}")
agent = Agent()

# if __name__ == '__main__':
#     agent = Agent()
