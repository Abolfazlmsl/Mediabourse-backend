import websockets
from datetime import datetime
import asyncio
import threading
import multiprocessing
from concurrent.futures import ProcessPoolExecutor


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
                print(f"I am Client #1. Data : {greeting}")
            except Exception as e:
                print('Server disconnected', e)
                print('Try to reconnect')
                websocket = await websockets.connect(uri)

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()

# async def yield_num(num, queue):
#     for i in range(num):
#         queue.put_nowait(i)
#         await asyncio.sleep(0.5)
#
#
# class AsyncIterable:
#     def __init__(self, queue):
#         self.queue = queue
#         self.done = []
#
#     def __aiter__(self):
#         return self
#
#     async def __anext__(self):
#         data = await self.fetch_data()
#         if data is not None:
#             return data
#         else:
#             raise StopAsyncIteration
#
#     async def fetch_data(self):
#         while not self.queue.empty():
#             self.done.append(self.queue.get_nowait())
#         if not self.done:
#             return None
#         return self.done.pop(0)
#
#
# async def consume_num(queue):
#     uri = "ws://192.168.0.155:8002"
#     async for i in AsyncIterable(queue):
#         async with websockets.connect(uri) as websocket:
#             # while True:
#             try:
#                 greeting = await websocket.recv()
#                 print(f"I am Client {i} _____ Data : {greeting}")
#             except Exception as e:
#                 print('Server disconnected', e)
#                 print('Try to reconnect')
#                 websocket = await websockets.connect(uri)
#
#
# def main():
#     event_loop = asyncio.get_event_loop()
#     queue = asyncio.Queue(loop=event_loop)
#     try:
#         event_loop.create_task(yield_num(10, queue))
#         event_loop.run_until_complete(consume_num(queue))
#     finally:
#         event_loop.close()
#
#
# if __name__ == '__main__':
#     while True:
#         main()

# async def aiter(num):
#     for i in range(num):
#         await asyncio.sleep(0.5)
#         yield i
#
#
# async def run(num):
#     uri = "ws://192.168.0.155:8002"
#     async for i in aiter(num):
#         async with websockets.connect(uri) as websocket:
#             # while True:
#             try:
#                 greeting = await websocket.recv()
#                 print(f"I am Client {i} _____ Data : {greeting}")
#             except Exception as e:
#                 print('Server disconnected', e)
#                 print('Try to reconnect')
#                 websocket = await websockets.connect(uri)
#
#
# def main():
#     event_loop = asyncio.get_event_loop()
#     try:
#         event_loop.run_until_complete(run(10))
#     finally:
#         event_loop.run_forever()
#
#
# if __name__ == '__main__':
#     main()
