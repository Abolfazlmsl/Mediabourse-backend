from server_helper import ClientThread
import websockets
import sys
import json


import asyncio


sys.path.append('.')
import asyncio
import threading

stopFlag = False


class GetData(threading.Thread):
    '''
        This class Scrape and update the data continuously and returns the
        new data to the Handler.run function.
    '''

    def __init__(self, obj, data):
        threading.Thread.__init__(self)
        self.data = data
        self.lastData = 0
        self.obj = obj

    def get(self):
        if self.lastData is not self.data:
            self.lastData = self.obj.read()
            return self.lastData


class Handler(threading.Thread):
    '''
        This class do the followings:
            1- Add new client to the self.connected (if client become disconnected,
               the client will be removed).
            2- Get the new data from the GetData class
            3- Send the data to the each existed clients.
    '''

    def __init__(self):
        threading.Thread.__init__(self)
        self.connected = set()

    def run(self):
        while not stopFlag:
            data = getdata.get()
            if data:
                loop1 = asyncio.new_event_loop()
                asyncio.set_event_loop(loop1)
                loop1.run_until_complete(self.sendData(data))
                loop1.close()

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        print('connect successfully.')
        print('#' * 80)
        try:
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected.remove(websocket)

    async def sendData(self, data):
        for websocket in self.connected.copy():
            # print(websocket)
            
            await websocket.send(data)


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


async def hello2(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    # greeting = f"Hello {name}!"
    # وسپهر,ونفت,گوهران,ثامید,وپویا,فولاد,حکشتی,شاروم,خگستر
    namad = name.split(",")
    print(f"< {namad}")


    #namad = ['خمحرکه', 'شپنا']
    host = "localhost"  # '192.168.1.105'
    port = 8765  # 8000
    obj = ClientThread(host, port, namad)
    print('#' * 80)
    print('Please wait while scraping...')
    data = obj.scrape()
    print('Scrape completed.')
    print('#' * 80)
    getdata = GetData(obj, data)

    print(f"> {getdata.get()}")
    print(f"> {type(getdata.get())}")
    await websocket.send(getdata.get())

    asyncio.get_event_loop().stop()


if __name__ == "__main__":
    start_server = websockets.serve(hello2, "localhost", 8765)



    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()










    # namad = ['خمحرکه', 'شپنا']
    # host = "localhost" #'192.168.1.105'
    # port = 8765 #8000
    # obj = ClientThread(host, port, namad)
    # print('#' * 80)
    # print('Please wait while scraping...')
    # data = obj.scrape()
    # print('Scrape completed.')
    # print('#' * 80)
    # getdata = GetData(obj, data)
    # print('Waiting for client to connect...')
    # handle = Handler()
    #
    # try:
    #     handle.start()
    #
    #     # ws_server = websockets.serve(handle.handler, '192.168.0.155', 8002)
    #     ws_server = websockets.serve(handle.handler, 'localhost', 8765)
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(ws_server)
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     stopFlag = True
    #     print("Exiting program...")
